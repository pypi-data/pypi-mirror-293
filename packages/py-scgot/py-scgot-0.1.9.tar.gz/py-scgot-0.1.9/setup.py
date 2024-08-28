from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
import numpy

# 定义 Cython 扩展模块
extensions = [
            Extension(
                        "interpolator",  # Cython 文件的模块名（.pyx 文件名去掉后缀）
                                ["./pygot/interpolator.pyx"],  # Cython 文件路径
                                        include_dirs=[numpy.get_include()]  # 如果使用了 NumPy，可以添加 NumPy 的头文件路径
                                            )
            ]

setup(
    name='py-scgot',
    version='0.1.9',
    author='Ruihong Xu',
    author_email='xuruihong@big.ac.cn',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    ext_modules=cythonize(extensions),  # 编译 Cython 扩展
    include_package_data=True,
    install_requires=[
        "cython",
        "anndata==0.10.8",
        "cellrank==2.0.4",
        "decoupler==1.6.0",
        "hnswlib==0.8.0",
        "joblib==1.3.2",
        "matplotlib==3.6.2",
        "networkx>=3.1",
        "numpy==1.24.3",
        "pygam>=0.9.0",
        "numba==0.58.1",
        "llvmlite==0.41.1",
        "pandas>=2.1",
        "POT==0.9.3",
        "scanpy==1.9.6",
        "scikit-learn==1.1.3",
        "scipy==1.11.4",
        "scvelo>=0.3.0",
        "seaborn==0.12.2",
        "torch>=2.0.1",
        "torchdiffeq==0.2.4",
        "tqdm",
        "plotly",
        "setuptools",
        "statsmodels"
],


)
