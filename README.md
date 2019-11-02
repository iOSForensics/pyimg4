# pyimg4

[![GitHub license](https://img.shields.io/cran/l/devtools.svg)](LICENSE)

A python lib for manipulating IMG4, IM4M and IM4P files.

## Requirements
scapy


# Getting started


## Extracting IMG4P payload from an IMG4 file:
```python
with open("payload", 'w+') as outfile:
    with open("myfile.img4", 'rb') as infile:
        i =  IMG4(infile.read())
        i.show() # Show the img4 file content
        outfile.write(str(i.IM4P.DATA))
```

# How to contribute
Contributors are essential to PyIMG4 (as they are to most open source projects).
Drop me a line if you want to contribute.
I also accept pull request.


## Reporting issues
### Questions
It is OK so submit issues to ask questions (more than OK, encouraged). There is a label "question" that you can use for that.

### Bugs
If you have installed PyIMG4 through a package manager (from your Linux or BSD system, from PyPI, etc.), please get and install the current development code, and check that the bug still exists before submitting an issue.

Please label your issues "bug".

If you're not sure whether a behavior is a bug or not, submit an issue and ask, don't be shy!

Enhancements / feature requests
If you want a feature in PyIMG4, but cannot implement it yourself or want some hints on how to do that, open an issue with label "enhancement".

Explain if possible the API you would like to have (e.g., give examples of function calls, packet creations, etc.).
