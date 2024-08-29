import numpy
from Cython.Build import cythonize
from setuptools import Extension


def pdm_build_update_setup_kwargs(context, setup_kwargs):
    extensions = [
        Extension(
            "aau_gomapedge_etl.clustering.ecadbscan.ecadbscan",
            ["src/aau_gomapedge_etl/clustering/ecadbscan/ecadbscan.pyx"],
            include_dirs=[numpy.get_include()],
        )
    ]
    setup_kwargs.update(ext_modules=cythonize(extensions))
