"""Packaging of acoutreams."""
import os

import numpy as np
from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext as _build_ext


if os.name == "nt":
    link_args = [
        "-Wl,-Bstatic,--whole-archive",
        "-lwinpthread",
        "-Wl,--no-whole-archive",
    ]
    compile_args = ["-DMS_WIN64"]

    class build_ext(_build_ext):
        """build_ext for Windows."""

        def finalize_options(self):
            """Set compiler to gcc."""
            super().finalize_options()
            self.compiler = "mingw32"

        # https://cython.readthedocs.io/en/latest/src/tutorial/appendix.html
        def build_extensions(self):
            """Add Windows specific compiler and linker arguments."""
            if self.compiler.compiler_type == "mingw32":
                for e in self.extensions:
                    e.extra_compile_args = compile_args
                    e.extra_link_args = link_args
            super().build_extensions()
else:
    build_ext = _build_ext



keys = {"include_dirs": [np.get_include()]}
compiler_directives = {"language_level": "3"}

extension_names = [
    "acoutreams.coeffsacoustics",
    "acoutreams.scw",
    "acoutreams.spw",
    "acoutreams.ssw",
    "acoutreams.wavesacoustics",
]
extensions = [
    Extension(name, [f"src/{name.replace('.', '/')}.pyx"], **keys)
    for name in extension_names
]


setup(ext_modules=extensions, cmdclass={"build_ext": build_ext})