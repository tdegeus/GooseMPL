
********************
Notes for developers
********************

Create a new release
====================

1.  Update the version numbers by modifying ``__version__`` in ``setup.py``.

2.  Upload the changes to GitHub and create a new release there (with the correct version number).

3.  Upload the package to PyPi:

    .. code-block:: bash

      $ python3 setup.py bdist_wheel --universal
      $ twine upload dist/*

.. note::

  Get ``twine`` by

  .. code-block:: bash

    python3 -m pip install --user --upgrade twine

  Be sure to follow the possible directives about setting the user's path.

References
==========

The following StackOverflow questions:

*   `Why using 'package_data' and not 'data_files' in 'setup.py' <http://stackoverflow.com/questions/43800753/pip-tries-to-install-package-in-the-wrong-location/43801841#43801841>`_
*   `Work around to 'install' the '.mplstyle' files with the package <http://stackoverflow.com/questions/35851201/how-can-i-share-matplotlib-style/43801778#43801778>`_

