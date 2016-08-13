import sys
import os
import re
import numpy as np
import bibtexparser as bib
import pubs
import awards as awd

'''
USAGE:
python manage.py [args], args:
  pubs   - build the page Publications.html
  awards - build the page Awards.html
  pages  - build the navbar and update all pages with it.
'''

# globals ----------------------------------------------------------------------
src_pubbib    = '../docs/pubs.bib'
src_pubhtml   = '../pages/Publications.html'
src_awardhtml = '../pages/Awards.html'
src_template  = '../template.html'

src_pages     = '../pages/'          # where this script finds the source pages
dst_pages     = '../../live/pages/'  # where this script writes the output pages
lnk_pages     = '../pages/'          # how the output pages reference each other
newline       = '\n<br>'

# awards functions ---------------------------------------------------------------
def update_awards():
  awards = awd.define()
  awardstr = title_block('Honours & Awards','600px')
  for award in awards:
    if award[1] == 1:
      awardstr += newline + awd.style_desc(award)
    else:
      awardstr += newline + awd.style_nodesc(award)
  awardstr += '\n</div>\n'

  file_write(src_awardhtml,awardstr)

# pubs functions ---------------------------------------------------------------
def update_pubs():
  global src_pubbib
  global src_pubhtml
  global newline
  
  # load and parse the bib file
  def get_pubs(src_pubbib):
    with open(src_pubbib) as f:
      bibdata = bib.loads(f.read())
      return bibdata.entries_dict.values()
  
  # sort by year
  def year_sort(B):
    years = []
    for i in range(0,len(B)):
      years += [B[i].get('year')]
      if years[i] is None:
        years[i] = 3000
    idx = np.argsort(years)[::-1]
    years = [years[i] for i in idx]
    B     = [B[i]     for i in idx]
    return years, B
  
  # print formatted year
  def print_yearstr(year):
    if year != 3000:
      yearstr = "<h3>" + year + "</h3>"
    else:
      yearstr = "<h3>Under Review & In Press</h3>"
    return yearstr
  
  # build the string for writing to the file
  def build_str(B,years):
    pubstr = title_block('Publications','100%')
    for i in range(len(B)):
      pubstr += newline + newline
      if (i==0) or (years[i] != years[i-1]): # current or changing year
        pubstr += newline + print_yearstr(years[i])
      pubstr += print_pubstr(B[i])
    pubstr += "\n</div>"
    return pubstr
  
  # update_pubs main
  B = get_pubs(src_pubbib)
  years, B = year_sort(B)
  pubstr = build_str(B,years)
  file_write(src_pubhtml,pubstr)
  
def print_pubstr(bibdata):
  # puberence format
  specs = pubs.basic()
  # building the string
  pubstr = ''
  # for all elements
  for e in specs:
    # get this pub's data\{([^}]*)\}
    key = re.search('(\{[^)]*\})',e).group(0)
    data = bibdata.get(key[1:-1])
    if data is not None:
      # find the keyword to replace
      pubstr += e.replace(key,data)
      
  return pubstr

# pages functions ---------------------------------------------------------------
def update_pages():
  global src_template
  global src_pages
  global dst_pages
  global lnk_pages
  global newline
  
  # generate the navbar string
  [navstr, srcpaths, dstpaths] = make_navbar(src_pages,dst_pages,lnk_pages)
  
  # add the navbar to the template file
  template = file_read(src_template)
  for i in range(0,len(template)):
    template[i] = template[i].replace('__navbar__',navstr)
    if template[i].find('__content__') > 0:
      idx = i

  # for all pages, add their contents
  for p in range(0,len(srcpaths)):
    pagestr = template[:]
    pagestr[idx:idx+1] = file_read(srcpaths[p])
    file_write(dstpaths[p],pagestr)

def make_navbar(src_pages,dst_pages,lnk_pages):
  global newline
  # find page names, and add them as links in the menu
  navstr  = "<ul class='expanded dropdown menu' data-dropdown-menu><li>\n"
  srcpaths = []
  dstpaths = []
  for root, dirs, files in os.walk(src_pages):
    for file in files:
      # find the page name, define the links, and store the file locations
      pagename = os.path.splitext(file)[0]
      link     = os.path.join(lnk_pages,file)
      srcpath  = os.path.join(src_pages,file)
      dstpath  = os.path.join(dst_pages,file)
      # print the link to the string
      navstr  += "      " + print_navlink(link, pagename) + "\n"
      # store the page names and links
      srcpaths.append(srcpath)
      dstpaths.append(dstpath)
  navstr += "    </li></ul>"
  return [navstr, srcpaths, dstpaths]

def print_navlink(pagelink,pagename):
  navlinkstr = "<a class='expanded alert button' href='" \
             + pagelink + "'>" + pagename + "</a>"
  return navlinkstr

# general file printing functions ----------------------------------------------
def file_read(fname):
  # read from file
  with open(fname,'r') as f:
    lines = []
    for line in f.readlines():
      lines.append(line)
  return lines

def file_write(fname, lines):
  # overwtrite file entirely
  with open(fname,'w') as f:
    for line in lines:
      f.write(line)
      
def title_block(title,contentwidth):
  return "<div class='title'><h1>"+title+"</h1></div>\n"+\
         "<div class='content' style='width: "+contentwidth+"; max-width: 100%;'>"

# main -------------------------------------------------------------------------
if len(sys.argv) == 2:
  useroption = sys.argv[1]
  if useroption in 'pubs':
    update_pubs()
  elif useroption in 'awards':
    update_awards()
  elif useroption in 'pages':
    update_pages()
  else:
    print('ERROR: ARG NAME')
else:
  print('ERROR: # ARGS')

