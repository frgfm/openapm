<h1 align="center">
  OpenAPM: ligthweight APM for FastAPI backend applications
</h1>

<p align="center">
  <a href="https://github.com/frgfm/openapm/actions/workflows/build.yml">
    <img alt="CI Status" src="https://img.shields.io/github/actions/workflow/status/frgfm/openapm/build.yml?branch=main&label=CI&logo=github&style=flat-square">
  </a>
  <a href="https://github.com/astral-sh/ruff">
    <img src="https://img.shields.io/badge/Linter-Ruff-FCC21B?style=flat-square&logo=ruff&logoColor=white" alt="ruff">
  </a>
  <a href="https://github.com/astral-sh/ruff">
    <img src="https://img.shields.io/badge/Formatter-Ruff-FCC21B?style=flat-square&logo=Python&logoColor=white" alt="ruff">
  </a>
  <a href="https://app.codacy.com/gh/frgfm/openapm/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=frgfm/openapm&amp;utm_campaign=Badge_Grade"><img src="https://app.codacy.com/project/badge/Grade/b93f051065cc4f43bb3e7e46435ca98b"/></a>
  <a href="https://codecov.io/gh/frgfm/openapm">
    <img src="https://img.shields.io/codecov/c/github/frgfm/openapm.svg?logo=codecov&style=flat-square&label=Coverage" alt="Test coverage percentage">
  </a>
</p>
<p align="center">
  <a href="https://pypi.org/project/openapm/">
    <img src="https://img.shields.io/pypi/v/openapm.svg?logo=PyPI&logoColor=fff&style=flat-square&label=PyPI" alt="PyPi Version">
  </a>
  <img src="https://img.shields.io/pypi/pyversions/openapm.svg?logo=Python&label=Python&logoColor=fff&style=flat-square" alt="pyversions">
  <a href="https://github.com/frgfm/openapm/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/frgfm/openapm.svg?label=License&logoColor=fff&style=flat-square" alt="License">
  </a>
</p>
<p align="center">
  <a href="https://frgfm.github.io/openapm">
    <img src="https://img.shields.io/github/actions/workflow/status/frgfm/openapm/docs.yaml?branch=main&label=Documentation&logo=read-the-docs&logoColor=white&style=flat-square" alt="Documentation Status">
  </a>
</p>

Ready-to-use APM backend service and middleware to monitor your FastAPI applications.

## Quick Tour

### Using the middleware

OpenAPM leverages [FastAPI middlewares](https://fastapi.tiangolo.com/tutorial/middleware/#create-a-middleware) and [background tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/) easily retrieve performance information on your HTTP request processing.

You can find more information in the [documentation](https://frgfm.github.io/openapm/middlewares.html), then use it as follows:

```python
# Define your model
from openapm.middlewares import FastAPMMiddleware
from fastapi import FastAPI

app = FastAPI()
app.add_middleware(FastAPMMiddleware(endpoint="https://your-apm-endpoint.com"))
```


## Setup

Python 3.11 (or higher) and [pip](https://pip.pypa.io/en/stable/)/[conda](https://docs.conda.io/en/latest/miniconda.html) are required to install OpenAPM.

### Stable release

You can install the last stable release of the package using [pypi](https://pypi.org/project/openapm/) as follows:

```shell
pip install openapm
```

### Developer installation

Alternatively, if you wish to use the latest features of the project that haven't made their way to a release yet, you can install the package from source:

```shell
git clone https://github.com/frgfm/openapm.git
pip install -e openapm/.
```


## What else

### Documentation

The full package documentation is available [here](https://frgfm.github.io/openapm/) for detailed specifications.


## Citation

If you wish to cite this project, feel free to use this [BibTeX](http://www.bibtex.org/) reference:

```bibtex
@misc{openapm2024,
    title={OpenAPM: lightweight APM for FastAPI backend applications},
    author={François-Guillaume Fernandez},
    year={2024},
    month={November},
    publisher = {GitHub},
    howpublished = {\url{https://github.com/frgfm/openapm}}
}
```



## Contributing

Feeling like extending the range of supported backend framework? Or perhaps submitting a new metric capture? Any sort of contribution is greatly appreciated!

You can find a short guide in [`CONTRIBUTING`](CONTRIBUTING.md) to help grow this project!



## License

Distributed under the Apache 2.0 License. See [`LICENSE`](LICENSE) for more information.

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Ffrgfm%2Fopenapm.svg?type=large&issueType=license)](https://app.fossa.com/projects/git%2Bgithub.com%2Ffrgfm%2Fopenapm?ref=badge_large&issueType=license)
