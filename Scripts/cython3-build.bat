@ECHO OFF

SET DISTUTILS_USE_SDK=1
CALL "C:\Program Files\Microsoft SDKs\Windows\v7.1\Bin\SetEnv.Cmd" /Release /x64
CALL "C:\Program Files (x86)\Microsoft Visual Studio 10.0\Common7\Tools\VCVarsQueryRegistry.bat" no32bit 64bit

CALL python3.bat -c "from setuptools import setup; from Cython.Build import cythonize; setup(ext_modules=cythonize('*.pyx'))" build_ext -i --compiler=msvc
