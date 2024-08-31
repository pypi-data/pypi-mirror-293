import numpy as np
import pandas as pd
import os
import cv2
import matplotlib.pyplot as plt
from pkg_resources import resource_filename
from ..data import STData

# Load color map
data_file_path = resource_filename(__name__, 'color.csv')
color_map = pd.read_csv(data_file_path, header=0)
color_map = np.array(
    [(int(color[5:7], 16), int(color[3:5], 16), int(color[1:3], 16)) for color in color_map['blue2red'].values],
    dtype=np.uint8)

def visualize_score(sections,
                    use_score: str,
                    index: int = None,
                    scale: float = 4.,
                    verbose: bool = False):
    """
    save score for given spot coordinates and region scores.

    Args:
        sections: Spatial_obj or dictionary containing the sections.
        use_score (str): The type of embedding to be visualized.
        index (int, optional): The index of the embedding to be visualized. Defaults to None.
        scale (float, optional): The scale factor for visualization. Defaults to 4.
        verbose (bool, optional): Whether to enable verbose output. Defaults to False.
    """

    if verbose: print(f"*** Visualizing and saving the embeddings of {use_score}... ***")

    if type(sections) == STData:
        sections = {sections.section_name: sections}

    # Visualize the embeddings of each section
    for _, section in sections.items():
        # Get section attributes
        mask = section.mask
        # row_range, col_range = section.row_range, section.col_range
        # image_shape = section.image.shape[1:]
        save_path = section.save_paths[use_score]
        score = section.scores[use_score]

        if index is None: os.makedirs(save_path, exist_ok=True)

        if use_score == 'DeepFuseNMF':
            os.makedirs(save_path + '/gray', exist_ok=True)
            os.makedirs(save_path + '/color', exist_ok=True)
        else:
            nearby_spots = section.nearby_spots if use_score == 'NMF' else section.all_nearby_spots

            score = score[nearby_spots, :]
            score = np.reshape(score, (mask.shape[0], mask.shape[1], score.shape[1]))
            score = np.transpose(score, (2, 0, 1))

        # Determine the pixel for max and min value
        background = np.where(cv2.resize(mask.astype(np.uint8), (int(mask.shape[1] / scale), int(mask.shape[0] / scale)), cv2.INTER_NEAREST) == 0)

        # Visualize DeepFuseNMF embeddings for each dimension
        for idx in range(score.shape[0]):
            if index is not None: idx = index

            # Normalize
            tmp_score = score[idx, :, :] if use_score == 'DeepFuseNMF' else score[idx, :, :] / score[idx, :, :].max()
            normalized_score = tmp_score * 255

            # Apply mask filtering
            filtered_score = normalized_score * mask

            # Visualize score of the specific index
            if index is not None:
                plt.imshow(filtered_score, cmap='gray_r')
                plt.show()
                break

            # Save the score image
            image_path = f"{save_path}/gray/Embedding_{idx}.png" if use_score == 'DeepFuseNMF' else f"{save_path}/Embedding_{idx}.png"
            cv2.imwrite(image_path, filtered_score)

            if use_score != 'DeepFuseNMF': continue

            # Colorize the score
            filtered_score = cv2.resize(filtered_score.astype(np.uint8),
                                        (int(filtered_score.shape[1] / scale), int(filtered_score.shape[0] / scale)))

            color_img = color_map[filtered_score]

            # Set the color of the background to gray
            color_img[background] = [128, 128, 128]

            # Save the colorized score image
            cv2.imwrite(f"{save_path}/color/Embedding_{idx}.png", color_img)
