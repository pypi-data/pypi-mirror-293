import numpy as np
import pandas as pd
import scanpy as sc
import squidpy as sq
from skimage import io
from typing import Tuple, Dict
from skimage import filters
import scipy
import math
import cv2
import warnings

class STData:
    """
    A class for handling and managing spatial transcriptomics data.

    This class processes and stores various components of spatial transcriptomics data,
    including image data, spot coordinates, and gene expression data.

    Args:
        section_name (str): Name of the tissue section.
        adata (sc.AnnData): AnnData object containing the spatial transcriptomics data.
        scale_factor (float): Scale factor for adjusting coordinates and image size.
        radius (float): Radius of spots in original scale.
        verbose (bool, optional): Flag for verbose output. Defaults to False.
    """

    def __init__(self,
                 adata: sc.AnnData,
                 section_name: str,
                 scale_factor: float,
                 radius: float,
                 verbose: bool = False):

        # Assign the input parameters to the class attributes
        image, spot_coord, spot_exp = read_from_anndata(adata)

        self.section_name = section_name
        self.scale_factor = scale_factor
        self.radius = int(radius / scale_factor)
        self.kernel_size = self.radius // 2 * 2 + 1
        self.verbose = verbose

        # Initialize the scores and save_paths dictionaries
        self.save_paths = None
        self.scores = {'NMF': None, 'GCN': None, 'VD': None, 'DeepFuseNMF': None}
        self.tissue_coord = None

        if self.verbose: print(f"*** Preparing data for {section_name}... ***")

        # Preprocess the data
        self._preprocess(spot_coord, image)

        # Store the spot expression data
        self.spot_exp = spot_exp

    def _preprocess(self,
                     spot_coord: np.ndarray,
                     image: np.ndarray):
        """
        Preprocess spot_coord and prepare the feasible domain and process the image.

        Args:
            spot_coord (np.ndarray): Array of original spot coordinates.
            image (np.ndarray): Original image data.

        """

        # Process the spot coordinates
        self.spot_coord = spot_coord / self.scale_factor - 1
        self.num_spots = self.spot_coord.shape[0]
        min_coords, max_coords = self.spot_coord.min(0).astype(int), self.spot_coord.max(0).astype(int)
        tmp_row_range = (max(0, min_coords[0] - self.radius), min(image.shape[0], max_coords[0] + self.radius + 1))
        tmp_col_range = (max(0, min_coords[1] - self.radius), min(image.shape[1], max_coords[1] + self.radius + 1))

        # Process the image
        image = image / np.max(image, axis=(0, 1), keepdims=True)

        hires_shape = (math.ceil(image.shape[0] / self.scale_factor), math.ceil(image.shape[1] / self.scale_factor))
        lowres_shape = (math.ceil(image.shape[0] / 16), math.ceil(image.shape[1] / 16))

        hires_image = cv2.resize(image, (hires_shape[1], hires_shape[0])).astype(np.float32)
        lowres_image = cv2.resize(image, (lowres_shape[1], lowres_shape[0])).astype(np.float32)

        self.image_type = _classify_image_type(lowres_image)
        if self.verbose: print(f"Image seems to be of type: {self.image_type}")

        self.image = np.transpose(hires_image, (2, 0, 1))

        # Create masks for outer regions
        gray = cv2.cvtColor(lowres_image, cv2.COLOR_RGB2GRAY)

        ## Apply Otsu's thresholding
        thresh = filters.threshold_otsu(gray)
        binary_mask = gray > thresh

        outer_mask = np.ones(lowres_shape, dtype=np.bool_)
        outer_mask[tmp_row_range[0]//16:tmp_row_range[1]//16, tmp_col_range[0]//16:tmp_col_range[1]//16] = 0

        ## Calculate variance for both classes in the outer region
        outer_pixels = gray[outer_mask]
        var_background = np.var(outer_pixels[binary_mask[outer_mask]])
        var_foreground = np.var(outer_pixels[~binary_mask[outer_mask]])

        ## Determine which class is the background based on lower variance and calculate background value
        background_pixels = lowres_image[outer_mask & binary_mask] if var_background < var_foreground else lowres_image[outer_mask & ~binary_mask]
        background_value = np.median(background_pixels, axis=0)

        # Create mask of image
        mask, tmp_mask = np.zeros(hires_shape, dtype=np.bool_), np.zeros(hires_shape, dtype=np.bool_)
        mask[np.where(np.mean(np.abs(hires_image - background_value[None, None, :]), axis=2) > 0.06)] = 1

        ## Overlap mask with spot coordinates
        tmp_mask[tmp_row_range[0]:tmp_row_range[1], tmp_col_range[0]:tmp_col_range[1]] = 1
        mask = np.logical_and(mask, tmp_mask)

        ## Close and open the mask
        if self.image_type == 'Protein':
            mask = cv2.morphologyEx(mask.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((int(self.radius*2), int(self.radius*2)), np.uint8)).astype(np.bool_)
        mask = cv2.morphologyEx(mask.astype(np.uint8), cv2.MORPH_OPEN, np.ones((int(self.radius/2), int(self.radius/2)), np.uint8)).astype(np.bool_)

        ## Get row and column ranges and final mask
        mask_idx = np.where(mask == 1)
        self.row_range = (np.min(mask_idx[0]), np.max(mask_idx[0]))
        self.col_range = (np.min(mask_idx[1]), np.max(mask_idx[1]))
        self.mask = mask[self.row_range[0]:self.row_range[1], self.col_range[0]:self.col_range[1]]

        # Create feasible domain
        self.feasible_domain = mask.copy()
        for (row, col) in self.spot_coord:
            row, col = round(row), round(col)
            row_range = np.arange(max(row - self.radius, 0), min(row + self.radius + 1, hires_shape[0]))
            col_range = np.arange(max(col - self.radius, 0), min(col + self.radius + 1, hires_shape[1]))
            self.feasible_domain[np.ix_(row_range, col_range)] = 0

def _classify_image_type(image):
    """
    Classify an image as either H&E stained or high dynamic range protein fluorescence.

    Args:
    image (numpy.ndarray): The input image. Can be high bit depth.

    Returns:
    str: 'HE' for H&E stained images, 'Protein' for protein fluorescence images.
    """

    # Calculate histogram
    hist, bin_edges = np.histogram(image.flatten(), bins=1000, range=(0, 1))

    # Calculate metrics
    low_intensity_ratio = np.sum(hist[:100]) / np.sum(hist)
    high_intensity_ratio = np.sum(hist[-100:]) / np.sum(hist)

    # Check for characteristics of protein fluorescence images
    if low_intensity_ratio > 0.5 and high_intensity_ratio < 0.05:
        return 'Protein'
    else:
        return 'HE'

def read_10x_data(data_path: str) -> sc.AnnData:
    """
    Read 10x Visium spatial transcriptomics data.

    Args:
        data_path (str): Path to the 10x Visium data directory.

    Returns:
        sc.AnnData: AnnData object containing the spatial transcriptomics data.
    """
    adata = sc.read_visium(data_path)
    return adata

def read_from_image_and_coord(image_path: str,
                              coord_path: str,
                              exp_path: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Read data from separate image, coordinate, and expression files.

    Args:
        image_path (str): Path to the H&E image file.
        coord_path (str): Path to the spot coordinates file.
        exp_path (str): Path to the gene expression file.

    Returns:
        Tuple containing:
            - image (np.ndarray): H&E image data.
            - spot_coord (np.ndarray): Spot coordinates.
            - spot_exp (np.ndarray): Gene expression data.
    """
    # Read image
    image = io.imread(image_path)

    # Read spot coordinates
    spot_coord = pd.read_csv(coord_path, index_col=0).values

    # Read gene expression data
    spot_exp = pd.read_csv(exp_path, index_col=0).values

    return image, spot_coord, spot_exp

def preprocess_data(adata: sc.AnnData,
                    n_top_genes: int = 3000) -> sc.AnnData:
    """
    Preprocess the spatial transcriptomics data, including normalization and SVG selection using squidpy.

    Args:
        adata (sc.AnnData): AnnData object containing the spatial transcriptomics data.
        n_top_genes (int, optional): Number of top SVGs to select. Defaults to 3000.

    Returns:
        sc.AnnData: Preprocessed AnnData object.
    """
    # Normalize data
    if adata.X.max() < 20:
        print("Data seems to be already normalized and log-transformed, skipping preprocessing.")
        return adata

    sc.pp.normalize_total(adata, target_sum=1e4)
    sc.pp.log1p(adata)

    # Compute spatial neighbors
    sq.gr.spatial_neighbors(adata)

    # Compute Moran's I for all genes
    sq.gr.spatial_autocorr(adata, mode="moran", genes=adata.var_names)

    # Select top SVGs based on Moran's I
    moran_scores = adata.uns['moranI']
    top_svgs = moran_scores.sort_values('I', ascending=False).head(n_top_genes).index
    adata = adata[:, top_svgs]

    return adata

def read_from_anndata(adata: sc.AnnData) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Extract relevant data from an AnnData object.

    Args:
        adata (sc.AnnData): AnnData object containing spatial transcriptomics data.

    Returns:
        Tuple containing:
            - image (np.ndarray): H&E image data.
            - spot_coord (np.ndarray): Spot coordinates.
            - spot_exp (np.ndarray): Gene expression data.
    """
    sc.pp.filter_cells(adata, min_genes=3)
    # Extract image
    image = adata.uns['spatial'][list(adata.uns['spatial'].keys())[0]]['images']['hires']

    # Extract spot coordinates
    spot_coord = adata.obsm['spatial']

    # Extract gene expression data
    spot_exp = adata.X.toarray() if isinstance(adata.X, scipy.sparse.spmatrix) else adata.X

    return image, spot_coord, spot_exp

def prepare_stdata(section_name: str,
                   section_paths: Dict[str, str],
                   scale_factor: float,
                   radius: float,
                   n_top_genes: int = 3000,
                   verbose: bool = False) -> STData:
    """
    Prepare STData object from various data sources with priority.

    Priority: AnnData > Visium > Scratch (image, coordinates, expression)

    Args:
        section_name (str): Name of the tissue section.
        section_paths (Dict[str, str]): Dictionary containing paths to different data sources.
        scale_factor (float): Scale factor for adjusting coordinates and image size.
        radius (float): Radius of spots in original scale.
        n_top_genes (int, optional): Number of top SVGs to select. Defaults to 3000.
        verbose (bool, optional): Flag for verbose output. Defaults to False.

    Returns:
        STData: Prepared STData object.
    """

    # Check for AnnData
    if section_paths.get('adata_path'):
        if verbose:
            print(f"*** Reading AnnData for section {section_name} ***")
        adata = sc.read_h5ad(section_paths['adata_path'])
        if any([section_paths.get('visium_path'), section_paths.get('image_path'),
                section_paths.get('spot_coord_path'), section_paths.get('spot_exp_path')]):
            warnings.warn("AnnData provided. Ignoring Visium and scratch data sources.")

    # Check for 10 Visium data if AnnData is not available
    elif section_paths.get('visium_path'):
        if verbose:
            print(f"*** Reading Visium data for section {section_name} ***")
        adata = sc.read_visium(section_paths['visium_path'])
        if any([section_paths.get('image_path'), section_paths.get('spot_coord_path'),
                section_paths.get('spot_exp_path')]):
            warnings.warn("Visium data provided. Ignoring scratch data sources.")

    # Read from scratch if neither AnnData nor 10 Visium is available
    else:
        if verbose:
            print(f"*** Reading data from scratch for section {section_name} ***")
        image_path = section_paths.get('image_path')
        spot_coord_path = section_paths.get('spot_coord_path')
        spot_exp_path = section_paths.get('spot_exp_path')

        if not all([image_path, spot_coord_path, spot_exp_path]):
            raise ValueError("Missing required paths for reading from scratch.")

        adata = sc.read_csv(spot_exp_path)

        spot_coord = pd.read_csv(spot_coord_path, index_col=0)
        spot_coord[['x_coord', 'y_coord']] = spot_coord.iloc[:, :2]
        spot_coord = spot_coord[['x_coord', 'y_coord']]

        # Add spot coordinates and image to adata
        adata.obsm['spatial'] = spot_coord.loc[adata.obs_names].values

        image = io.imread(image_path)
        adata.uns['spatial'] = {section_name: {'images': {'hires': image}}}


    # Preprocess data
    adata = preprocess_data(adata, n_top_genes=n_top_genes)

    # Create STData object
    st_data = STData(adata,
                     section_name=section_name,
                     scale_factor=scale_factor,
                     radius=radius,
                     verbose=verbose)

    return st_data