@ECHO OFF

python -c "from setuptools import setup; from Cython.Build import cythonize; setup(ext_modules=cythonize('*.pyx'))" build_ext -i
