# thesis

## Installation requirements

```
pip install -r requirements.txt
```

Citations for scientific library dependencies:

`Hagberg, Aric, Pieter J. Swart, and Daniel A. Schult. Exploring network structure, dynamics, and function using NetworkX. No. LA-UR-08-05495; LA-UR-08-5495. Los Alamos National Laboratory (LANL), Los Alamos, NM (United States), 2008.`

`Harris, Charles R., et al. "Array programming with NumPy." Nature 585.7825 (2020): 357-362.`

`Hunter, John D. "Matplotlib: A 2D graphics environment." Computing in science & engineering 9.03 (2007): 90-95.`

`McKinney, Wes. "Data structures for statistical computing in Python." SciPy. Vol. 445. No. 1. 2010.`

`Virtanen, Pauli, et al. "SciPy 1.0: fundamental algorithms for scientific computing in Python." Nature methods 17.3 (2020): 261-272.`

`Waskom, M. L. "seaborn: Statistical data visualization: Journal of Open Source Software, v. 6." (2021).`

## Releasing
(For internal reference only; users should disregard this section.) How to create a release.

Run pytests.
```
pytest .
```

Run pytype checks.
```
pytype . -j auto -d import-error,pyi-error -k
```

Build the source distribution and wheel.
```
python setup.py sdist bdist_wheel
```

Check for twine errors.
```
twine check dist/*
```

Upload package to PyPi.
```
twine upload dist/*
```
