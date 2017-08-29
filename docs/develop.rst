
********************
Notes for developers
********************

Create a new release
====================

1.  Update the version numbers by modifying `__version__` in `setup.py`.

2.  Upload the changes to GitHub and create a new release there (with the correct version number).

3.  Upload the package to PyPi:

    .. code-block:: bash

      $ python3 setup.py bdist_wheel --universal
      $ twine upload dist/*


