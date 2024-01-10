# Survey Framework
This is a Python script intended to make building survey paper websites easier, inspired by [TreeVis](https://treevis.net). 
The script sets up a React website that has basic search functionality and a clean interface.

| component | completion |
| --------- | ---------- |
| Extraction script | ✔️ |
| Backend API | ✔️   |
| Frontend scaffolding | ✔️ |

## Installation
The easiest way to install this package is through [poetry](https://python-poetry.org/).
With `poetry` installed, simply run `poetry install`.

## Extract 
The extraction script, ran with `survey_extract`, reads a directory and extracts its contents to a mongoDB database.

| flag  | description |
| ----  | ----------- |
| -i    | Directory to copy images to from the images/ subdirectory. If using the API, leave this blank. |
| -c    | Directory to copy icons to from the icons/ subdirectory. If using the API, leave this blank. |
| -n    | Name of the database to store the survey in. Defaults to the name of the subdirectory containing your data. This should be the value used in constants.js as {SURVEY_NAME}.
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
icon="sectionA_icon.svg"
color="#ABCDEF"

[SectionA.SubSectionB.SubSubSectionA]
...
```
Note that the header section MUST be designated with a `.`, this is also true for sections nested even further in the taxonomy. 
Otherwise, your subsections will be treated as main sections.

You can additionally specify a color for each section / subsection, with parent sections
passing their colors down to their children unless overwritten.
This lets you specify an overall color scheme for a section, with children being able
to use their own colors.

You can also specify an icon (SVG format only) that will be displayed throughout the UI. 
Please see the `icons` section below for more details.

### papers.bib 
Next to the `metadata.toml` file should be a `papers.bib` file. 
This should be a bibtex file containing all of the papers you plan to reference.
This file is optional if you are not adding any new papers to an existing database.

### icons/
An optional `icons` directory can be provided. 
The extraction script will check for an `icon` property in the metadata.toml file
and load the corresponding icon into the API's icon folder if found.

Please note that icons *MUST* be SVG files. 
If using Adobe Illustrator, make sure to export icons with "Styling" set to "Presentation Attributes".

## Building the website 
First, get your paper information and metadata in the format described in the *extract* section.
Run the survey_extract executable - this place all of the assets (images, data, icons) in the front-end's source code. 

Next, you need to compile the website. Edit `constants.js` to use the survey you extracted with the extraction script. Then, run `npm install` and `npm run build`. 

Once that is complete, all you need to do is host the `dist` folder in `front` with a http server of your choice. 

## Contributing
Install the development requirements with `poetry install --with dev`. 
Use `black`, `isort` and `flake8` for formatting / linting, and `pyright` for LSP features.
Run tests with `pytest -r tests`.
