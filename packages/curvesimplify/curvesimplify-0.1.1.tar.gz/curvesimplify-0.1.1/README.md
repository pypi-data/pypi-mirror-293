# CurveSimplify

[![License](https://img.shields.io/github/license/JSS95/curvesimplify)](https://github.com/JSS95/curvesimplify/blob/master/LICENSE)
[![CI](https://github.com/JSS95/curvesimplify/actions/workflows/ci.yml/badge.svg)](https://github.com/JSS95/curvesimplify/actions/workflows/ci.yml)
[![CD](https://github.com/JSS95/curvesimplify/actions/workflows/cd.yml/badge.svg)](https://github.com/JSS95/curvesimplify/actions/workflows/cd.yml)
[![Docs](https://readthedocs.org/projects/curvesimplify/badge/?version=latest)](https://curvesimplify.readthedocs.io/en/latest/?badge=latest)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/curvesimplify.svg)](https://pypi.python.org/pypi/curvesimplify/)
[![PyPI Version](https://img.shields.io/pypi/v/curvesimplify.svg)](https://pypi.python.org/pypi/curvesimplify/)

![title](https://curvesimplify.readthedocs.io/en/latest/_images/plot-header.png)

A Python package for polygonal curve simplification.

List of supported algorithms:
- Imai-Iri algorithm (`curvesimplify.imaiiri`)
- Agarwal's algorithm (`curvesimplify.agarwal`)

## Usage

```python
>>> import numpy as np
>>> from curvesimplify.agarwal import min_err
>>> x = np.linspace(0, 5, 50)
>>> f = np.exp(-x) * np.cos(2 * np.pi * x)
>>> curve = np.column_stack([x, f])
>>> simp, err = min_err(curve, 10)
>>> len(simp)  # at most 10
10
```

## Installation

CurveSimplify can be installed using `pip`.

```
$ pip install curvesimplify
```

## Documentation

CurveSimplify is documented with [Sphinx](https://pypi.org/project/Sphinx/).
The manual can be found on Read the Docs:

> https://curvesimplify.readthedocs.io/

If you want to build the document yourself, get the source code and install with `[doc]` dependency.
Then, go to `doc` directory and build the document:

```
$ pip install .[doc]
$ cd doc
$ make html
```

Document will be generated in `build/html` directory. Open `index.html` to see the central page.
