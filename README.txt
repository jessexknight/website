# Website

## Overview

- `src`:  contains files used during development and compilation
- `live`: contains all files necessary to launch the website

### Main file
`manage.py`: the main file for generating all website pages automatically -- usage:\
`python manage.py [args]`\
Arguments:\
- awds  - build the page Awards.html
- mlab  - build the page MATLAB.html and convert all .m files into pretty html files
- pubs  - build the page Publications.html
- pages - build the navbar and update all pages with it.

## To Do
- package same name .m/other files into zip for download
- refactor entire code as OO
- fix `<pre>` double lines in code
- reconsider spacing of awards: fade to ... to avoid wrapping dates
- hover-over for descriptions: MATLAB & awards
- sticky menu for long content
- hidden menu in small screens


