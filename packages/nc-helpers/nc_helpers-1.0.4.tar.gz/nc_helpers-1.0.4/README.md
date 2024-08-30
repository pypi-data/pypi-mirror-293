# Build instructions
## First time installing build env  
`python3 -m pip install --upgrade build`  
`python3 -m pip install twine`  
## Building/uploading new package
`python3 -m build`  
`python3 -m twine upload dist/<PACKAGE NAME>`  