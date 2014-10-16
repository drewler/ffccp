# ffccp

Final Fantasy Crystal Chronicles (Gamecube) file parser. Written in Python 2

## What is this?

A tool to read/convert FFCC files (.chm, .tex, etc)

## What does it do?

* Reads a FFCC file, parsing its tags in some kind of tree structure
* Prints out the nested tag list of the different sections (tag.py)
* Converts CHM files to [OBJ files](http://en.wikipedia.org/wiki/Wavefront_.obj_file)

## Usage

    $ python tag.py example_file.[chm|tex|chd|...]
    $ python chm.py example_file.chm

## Current status

- [x] Tag parser
- [x] CHM parser refactor
- [x] CHM2OBJ
- [ ] TEX parser refactor
- [ ] TEX2IMG