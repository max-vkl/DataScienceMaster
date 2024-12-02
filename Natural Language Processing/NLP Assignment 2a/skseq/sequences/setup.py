from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(
    name='Structured Perceptron Cython',
    ext_modules=cythonize(["skseq/sequences/sequence_list_c.pyx","skseq/sequences/structured_perceptron_c.pyx"]),
    include_dirs=[numpy.get_include()]
)
