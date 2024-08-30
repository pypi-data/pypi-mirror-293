=======================
My First Sample package
=======================

this is a demo of my first package


python .\setup.py sdist  

python .\setup.py bdist_wheel

twine check .\dist\* # to check for errors

=============================
To upload to testpypi or live
=============================



twine upload --verbose  --repository testpypi dist/*

twine upload --verbose  dist/*

