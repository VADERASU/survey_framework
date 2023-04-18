# Survey Framework
This is a Python framework intended to make building survey paper websites easier, inspired by [TreeVis](https://treevis.net). 
The goal is to have an API that sets itself up using the papers you provide. 

| component | completion |
| --------- | ---------- |
| Extraction script | ✔️  |
| Backend API | ☐   |
| Frontend scaffolding | ☐ |

## Extract ✔️
The extraction script, ran with `survey_extract`, reads a directory and extracts its contents to a mongoDB database.

| flag  | description |
| ----  | ----------- |
| -i    | Directory to copy images to from the images/ subdirectory. If using the API, leave this blank. |
| -h    | Prints help text. |

The directory needs to be structured in a specific way for the script to work.

### images/
An `images` subdirectory should reside within the target directory. 
Internally, the `images` directory can be organized in any arbitrary fashion, as long as the image files are named `{CITATION_KEY}[_XYZ].extension`.
This naming scheme allows the script to link images to papers. 
The underscore is included only if you have multiple images from the same paper to avoid conflicts in the filesystem.

### metadata.toml
There needs to be a `metadata.toml` file in the directory you are trying to extract data from.
It should contain the taxonomy you are developing for your paper, specified as sections within the toml file.
Within each section, an array called images needs to be declared which maps the images to your taxonomic keyword.
A sample section could look like this:
```
[SectionA.SubSectionA]
images=['image1.png','image2.png']

[SectionA.SubSectionB.SubSubSectionA]
...
```
Note that the header section MUST be designated with a `.`, this is also true for sections nested even further in the taxonomy. 
Otherwise, your subsections will be treated as main sections.

### papers.bib 
Next to the `metadata.toml` file should be a `papers.bib` file. 
This should be a bibtex file containing all of the papers you plan to reference.

## Installation
The easiest way to install this package is through [poetry](https://python-poetry.org/).
With `poetry` installed, simply run `poetry install`.

## Contributing
Install the development requirements with `poetry install --with dev`. 
Use `black`, `isort` and `flake8` for formatting / linting, and `pyright` for LSP features.
Run tests with `pytest -r tests`.
