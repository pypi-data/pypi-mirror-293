import os
from setuptools import setup, find_packages

path = os.path.abspath(os.path.dirname(__file__))

try:
    with open(os.path.join(path, 'README.md'), 'r', encoding='utf-8') as f:
        long_description = f.read()
except Exception as e:
    long_description = 'Interpretable super-resolution dimension reduction of spatial transcriptomics data by DeepFuseNMF'

print (find_packages())
setup(
    name='DeepFuseNMF',
    version='0.3.0',
    description='Interpretable super-resolution dimension reduction of spatial transcriptomics data by DeepFuseNMF',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT Licence',
    Home_page='https://github.com/sldyns/DeepFuseNMF',
    include_package_data=True,
    python_requires='>=3.9',
    packages=find_packages(),
    package_data={'DeepFuseNMF': ['utils/color.csv']},
    install_requires=[
        'numpy>=1.22',
        'cython>=0.29.24',
        'torch>=1.12',
        'scikit-learn>=1.0',
        'squidpy',
        'matplotlib',
        'tqdm',
        'h5py',
        'scanpy',
        'anndata',
        'pandas',
        'scikit-image',
        'opencv-python',
        'scipy',
    ],
    author='Kun Qian, Junjie Tang',
    author_email='kunqian@stu.pku.edu.cn, junjie.tang@pku.edu.cn',
    maintainer='Kun Qian',
    maintainer_email='kunqian@stu.pku.edu.cn'
)