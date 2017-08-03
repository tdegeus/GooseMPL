# New release

1.  Update the version number as follows:

    -   Modify `__version__` in `setup.py`.

2.  Upload the changes to GitHub and create a new release there (with the correct version number).

3.  Upload the package to PyPi:

    ```bash
    $ python3 setup.py bdist_wheel --universal
    $ twine upload dist/*
    ```
