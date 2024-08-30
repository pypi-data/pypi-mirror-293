# A binned Hawkes process for dynamic multilayer graphs

Matthew Sit (2024). matthew.sit22@imperial.ac.uk

Supervised by Dr. Francesco Sanna Passino.

Submitted in partial fulfillment of the requirements for the MSc in Machine Learning and Data Science of Imperial College London.

## Usage
There are two options for using this code:

1. pip install our package, which provides the trainable model and evaluation functions, but does not include data or any other application specific artifacts.

    Install our package via pip.
    ```
    pip install binned-hawkes-multilayer
    ```

    Then you'll be able to import it:
    ```
    from binned_hawkes_multilayer.proposed import ProposedModel
    ```

    See [`pkg_demo.py`](pkg_demo.py) for an end-to-end usage example.

2. git clone this repository, which is complete with all of the above and more; everything needed to fully reproduce all our results. The remainder of this README details the contents.

## Installation requirements

After cloning this repository, ensure all necessary requirements are satisfied by running:
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
*(For internal reference only; users should disregard this section.)* How to create a release.

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

Cleanup.
```
rm -r build dist binned_hawkes_multilayer.egg-info
```
