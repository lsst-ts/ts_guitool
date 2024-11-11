# Python QT Tool Code

## Platform

- AlmaLinux 8.10
- python: 3.11.10

## Needed Package

- numpy (install by `conda`)
- pyside6 (install by `conda`)
- qt6-charts (install by `conda`)
- xorg-x11-server-Xvfb (optional, install by `dnf`)
- qasync (install by `conda -c conda-forge`)
- [black](https://github.com/psf/black) (optional)
- [flake8](https://github.com/PyCQA/flake8) (optional)
- [isort](https://github.com/PyCQA/isort) (optional)
- [mypy](https://github.com/python/mypy) (optional)
- [documenteer](https://github.com/lsst-sqre/documenteer) (optional)
- pytest (optional, install by `conda`)
- pytest-flake8 (optional, install by `conda -c conda-forge`)
- pytest-qt (optional, install by `conda -c conda-forge`)
- pytest-xvfb (optional, install by `conda -c conda-forge`)

## Build the Document

To build project documentation, run `package-docs build` to build the documentation.
To clean the built documents, use `package-docs clean`.
See [Building single-package documentation locally](https://developer.lsst.io/stack/building-single-package-docs.html) for further details.

## Unit Tests

You can run the unit tests by:

```bash
pytest tests/
```

If you have the **Xvfb** and **pytest-xvfb** installed, you will not see the prompted windows when running the unit tests.

Note: If the variable of `PYTEST_QT_API` is not set, you might get the core dump error in the test.
