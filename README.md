
### Dev setup

####OSX

`xcode-select --install`

`brew install pandoc`

`pip install pypandoc`

`pip-compile requirements.in > requirements.txt`

`pip-sync`


### Run tests

`pytest test/sample.py`
