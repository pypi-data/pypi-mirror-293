# noqa

from setuptools import Extension, setup

ghorse_sources = [
    "ghorse/_ghorse/src/" + name for name in ["module.c", "freeze.c", "graph.c"]
]

ghorse_extension = Extension(
    name="ghorse._ghorse",
    sources=ghorse_sources,
    include_dirs=["ghorse/_ghorse/include"],
    define_macros=[("PY_SSIZE_T_CLEAN", None)],
)

setup(
    name="ghorse",
    packages=["ghorse"],
    ext_modules=[ghorse_extension],
)
