# Rivertils

Scripts that are imported by packages you've deployed to pypi

## To publish to PyPi 

- increment the version number in pyproject.toml
- poetry build
- poetry publish --username __token__ --password (use the token in the pypi account) [text](https://pypi.org/manage/account/token/)
Set your username to __token__
Set your password to the token value, including the pypi- prefix
- git commit and push