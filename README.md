# ffccp

Final Fantasy Crystal Chronicles (Gamecube) file parser. Written in Python 2

## What is this?

A tool to read/convert FFCC files (.chm, .tex, etc)

## What does it do?

* Reads a FFCC file, parsing its tags in some kind of tree structure
* Prints out the nested tag list of the different sections (tag.py)
* Converts CHM files to [OBJ files](http://en.wikipedia.org/wiki/Wavefront_.obj_file)
* Converts TEX files to PNG files

## Usage

    $ python tag.py example_file.[chm|tex|chd|...]
    $ python chm.py example_file.chm
    $ python tex.py example_file.tex
    
A folder named "example_file" will be created. OBJ & PNG files will be created inside this folder

## Current status

- [x] Tag parser
- [x] CHM parser refactor
- [x] CHM2OBJ
- [x] TEX parser refactor
- [x] TEX2IMG
- [ ] Write link between model, texture and other attributes (.mtl)
- [ ] Read more texture formats (other than [CMPR](http://hitmen.c02.at/files/yagcd/yagcd/chap17.html))
- [ ] Read bone info
- [ ] CHA parser
- [ ] CHD parser
- [ ] Write docs about file structure