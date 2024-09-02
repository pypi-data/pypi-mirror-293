from setuptools import setup

name = "types-Flask-Cors"
description = "Typing stubs for Flask-Cors"
long_description = '''
## Typing stubs for Flask-Cors

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`Flask-Cors`](https://github.com/corydolphin/flask-cors) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`Flask-Cors`.

This version of `types-Flask-Cors` aims to provide accurate annotations
for `Flask-Cors==5.0.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/Flask-Cors. All fixes for
types and metadata should be contributed there.

This stub package is marked as [partial](https://peps.python.org/pep-0561/#partial-stub-packages).
If you find that annotations are missing, feel free to contribute and help complete them.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit
[`001c3b6495e85c1516177f60e26c39c276f906e9`](https://github.com/python/typeshed/commit/001c3b6495e85c1516177f60e26c39c276f906e9) and was tested
with mypy 1.11.1, pyright 1.1.378, and
pytype 2024.4.11.
'''.lstrip()

setup(name=name,
      version="5.0.0.20240902",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/Flask-Cors.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['Flask>=2.0.0'],
      packages=['flask_cors-stubs'],
      package_data={'flask_cors-stubs': ['__init__.pyi', 'core.pyi', 'decorator.pyi', 'extension.pyi', 'version.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
