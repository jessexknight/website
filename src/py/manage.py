import sys
import os
import numpy as np
import pubs
import awds

'''
USAGE:
python manage.py [args], args:
  pubs   - build the page Publications.html
  awards - build the page Awards.html
  pages  - build the navbar and update all pages with it.
'''
# ------------------------------------------------------------------------------
# globals
# ------------------------------------------------------------------------------

src_pubbib    = '../docs/pubs.bib'
src_pubhtml   = '../pages/Publications.html'
src_awardhtml = '../pages/Awards.html'
src_template  = '../template.html'

src_docs      = '../../live/docs/'
lnk_docs      = '../docs/'

src_pages     = '../pages/'          # where this script finds the source pages
dst_pages     = '../../live/pages/'  # where this script writes the output pages
lnk_pages     = '../pages/'          # how the output pages reference each other

newline       = '\n<br>'

# ------------------------------------------------------------------------------
# awards functions
# ------------------------------------------------------------------------------

def update_awards():
  awardstr = print_h1('Funding & Awards','800px')
  
  def print_awardlist(awards):
    awardstr = ''
    for award in awards:
      if award[1] == 1:
        awardstr += awds.print_desc(award)
      else:
        awardstr += awds.print_nodesc(award)
    return awardstr

  awardstr += print_h2('Funding')
  awardstr += print_awardlist(awds.funds())
  awardstr += newline + '&nbsp' + newline
  awardstr += print_h2('Awards')
  awardstr += print_awardlist(awds.awards())
  awardstr += '\n</div>\n'
  file_write(src_awardhtml,awardstr)

# ------------------------------------------------------------------------------
# pubs functions
# ------------------------------------------------------------------------------

def update_pubs():
  global src_pubbib
  global src_pubhtml
  global scr_docs
  global lnk_docs
  global newline
  
  # print formatted year seperator
  def print_yearstr(year):
    if year != np.inf:
      yearstr = print_h2(year)
    else:
      yearstr = print_h2('Under Review & In Press')
    return yearstr
  
  # build the string for writing to the file
  def build_str(B,years):
    pubstr = print_h1('Publications','100%')
    for i in range(len(B)):
      if (i==0) or (years[i] != years[i-1]): # current or changing year
        pubstr += print_yearstr(years[i])
      pubstr += '<p>'+pubs.printstr(B[i],[src_docs,lnk_docs])+'</p>'
    pubstr += "\n</div>\n"
    return pubstr
  
  # update_pubs main
  B = pubs.parse(src_pubbib)
  years, B = pubs.sortyears(B)
  pubstr = build_str(B,years)
  file_write(src_pubhtml,pubstr)

# ------------------------------------------------------------------------------
# pages functions
# ------------------------------------------------------------------------------

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
  navlinkstr = "<a class='expanded button' href='" \
             + pagelink + "'>" + pagename + "</a>"
  return navlinkstr

# ------------------------------------------------------------------------------
# general file printing functions
# ------------------------------------------------------------------------------

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
      f.write(line.encode('ascii', 'replace'))
      
def print_h1(str,contentwidth):
  return "<div class='divh1'><h1>"+str+"</h1></div>\n"+\
         "<div class='content' style='width: "+contentwidth+"; max-width: 100%;'>"

def print_h2(str):
  return "<div class='divh2'><h2>"+str+"</h2></div>\n"

# ------------------------------------------------------------------------------
# main
# ------------------------------------------------------------------------------

for arg in sys.argv[1:]:
  if arg in 'pubs':
    update_pubs()
  elif arg in 'awds':
    update_awards()
  elif arg in 'pages':
    update_pages()
  else:
    print('ERROR: ARG NAME')

