# python-magic-pure

python-magic-pure is a pure python replacement for python-magic that does not require using libmagic.
It's actually just provides a python-magic compatible wrapper around the puremagic library.
This can be useful if you need to use python-magic but libmagic is not available (or too much of a pain to install, like in AWS lambda).

### Installation
`pip install python-magic-pure`


### Usage
```python
>>> import magic
>>> magic.from_file("testdata/test.pdf")
'PDF document, version 1.2'
# recommend using at least the first 2048 bytes, as less can produce incorrect identification
>>> magic.from_buffer(open("testdata/test.pdf", "rb").read(2048))
'PDF document, version 1.2'
>>> magic.from_file("testdata/test.pdf", mime=True)
'application/pdf'
```

### Caveats
I only implemented `from_file` and `from_buffer` methods.  It does not support the `Magic` class

