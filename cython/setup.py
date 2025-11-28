from setuptools import Extension, setup
from Cython.Build import cythonize
files = ["ml_interpreter_cython.pyx"]
setup(
    ext_modules = cythonize([
        Extension(
            "ml_interpreter_cython",
            files,
        extra_compile_args=["-O3", "-march=native"],
        )],
        language_level="3")
)

