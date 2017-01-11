# Website
A personal website: live files, and source code for template-based generation (like Genshi).

Mostly a fun project for learning web dev, and overcoming the deficiencies of LinkedIn.

Link to the live site: http://www.uoguelph.ca/~jknigh04

## Overview 

`src`:  contains files used during development and compilation
- `\py`: python class files and `main` file.
- `\templates`: template html snippits populated using `__example__`-style keywords
- `\content`: json "objects" which provide different content for each template
- `\pages`: main pages for the site

`live`: contains all files necessary to launch the website:
- `\pages`: written by `main.py`
- `\docs`: all documents (e.g. PDFs) linked from the site
- `\img`: all images

### Main file
`main.py`: the main file for generating all website pages automatically -- usage: `python main.py`

## To Do

#### General
- [x] refactor entire code as OO
- [x] sticky menu for long content
- [x] live links need to be relative
- [ ] put back awards page / transcripts (hide under sample work?)
- [ ] documentation of python
- [x] add command line option for "dev" mode: local links
- [x] add more sample work: ML course, poster

#### Mini-Projects
- [ ] Two templates: mini box and full page w. publications
- [ ] Develop sub-page framework

#### Abandoned
- [x] fix `<pre>` double lines in code
- [x] finish refactoring OO for Code pages - git instead
- [x] package same name .m/other files into zip for download - same as above
- [x] hidden menu in small screens - hamburgers are stupid
