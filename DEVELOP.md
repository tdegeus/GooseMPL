
# Upload to PyPi

Using the following three commands:

```bash
python3 setup.py sdist
python3 setup.py bdist_wheel --universal
twine upload dist/*
```

# References

The following StackOverflow questions:

*   [Why using `package_data` and not `data_files` in `setup.py`](http://stackoverflow.com/questions/43800753/pip-tries-to-install-package-in-the-wrong-location/43801841#43801841)
*   [Work around to 'install' the `.mplstyle` files with the package](http://stackoverflow.com/questions/35851201/how-can-i-share-matplotlib-style/43801778#43801778)
