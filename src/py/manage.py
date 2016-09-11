import sys
import os
import shutil
import errno
import numpy as np
import pubs
import awds

'''
USAGE:
python manage.py [args], args:
  awds  - build the page Awards.html
  mlab  - build the page MATLAB.html
  pubs  - build the page Publications.html
  pages - build the navbar and update all pages with it.
'''

# ------------------------------------------------------------------------------
# globals
# ------------------------------------------------------------------------------

newline = '\n<br>'
X = {\
'template':{\
  'html' : '../template.html'},\
'awds':{\
  'html' : '../pages/Awards.html'},\
'pubs':{\
  'html' : '../pages/Publications.html',\
  'bib'  :'../docs/pubs.bib'},\
'mlab':{\
  'html' : '../pages/MATLAB.html',\
  'pages':{\
    'tmp': '../matlab/template.html',\
    'dst': '../../live/matlab/',\
    'lnk': '../matlab/'},\
  'code' :{\
    'src': '../matlab/',\
    'dst': '../../live/matlab/',\
    'lnk': '../matlab/'}},\
'docs':{\
  'src'  : '../../live/docs/',\
  'lnk'  : '../docs/'},\
'pages':{\
  'src'  : '../pages/',\
  'dst'  : '../../live/pages/',\
  'lnk'  : ''}\
}

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
  awardstr += '<p style="clear:both">'+newline+'</p>'
  awardstr += print_h2('Awards')
  awardstr += print_awardlist(awds.awards())
  awardstr += '\n</div>\n'
  file_write(X['awds']['html'],awardstr)

# ------------------------------------------------------------------------------
# pubs functions
# ------------------------------------------------------------------------------

def update_pubs():
  global X
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
      pubstr += '<p>'+pubs.printstr(B[i],[X['docs']['src'],X['docs']['lnk']])+'</p>'
    pubstr += "\n</div>\n"
    return pubstr
  
  # update_pubs main
  B = pubs.parse(X['pubs']['bib'])
  years, B = pubs.sortyears(B)
  pubstr = build_str(B,years)
  file_write(X['pubs']['html'],pubstr)

# ------------------------------------------------------------------------------
# matlab functions
# ------------------------------------------------------------------------------

def update_matlab():
  global newline
  global X
  
  def mlab_link(mlabstr,root,file):
    # names
    subdir   = root.replace(X['mlab']['code']['src'],'')
    pagename = file.replace('.m','.html')
    # html pages
    link     = os.path.join(X['mlab']['pages']['lnk'],subdir,pagename)
    src      = os.path.join(root,file)
    dst      = os.path.join(X['mlab']['pages']['dst'],subdir,pagename)
    # add the link to main page
    mlabstr += '\n' + print_matlink(link,file)
    return [mlabstr,pagename,src,dst]
  
  # update_matlab main
  mlabstr = "<div class='divh1'><h1>MATLAB Code</h1></div>"

  # copy all source code
  copyover(X['mlab']['code']['src'], X['mlab']['code']['dst'])

  # generate template file
  template = file_read(X['mlab']['pages']['tmp'])

  # walk the source
  for root, dirs, files in os.walk(X['mlab']['code']['src']):
    if root != X['mlab']['code']['src']: # don't copy template
      for file in files:
        if '.m' in file:
          # create the link
          [mlabstr,pagename,src,dst] = mlab_link(mlabstr,root,file)
          # create the page
          pagestr = template
          codestr = file_read(src)
          pagestr = add_to_template(pagestr,'__filename__',file)
          pagestr = add_to_template(pagestr,'__download__',file)
          pagestr = add_to_template(pagestr,'__link__',file)
          pagestr = add_to_template(pagestr,'__code__',codestr)
          file_write(dst,pagestr)

  file_write(X['mlab']['html'],mlabstr)
      
def print_matlink(pagelink,pagename):
  matlinkstr = "<p><pre><a href='" \
               + pagelink + "'>" \
               + pagename + "</a></pre></p>"
  return matlinkstr
  
# ------------------------------------------------------------------------------
# pages functions
# ------------------------------------------------------------------------------

def update_pages():
  global X
  
  # main pages
  for root, dirs, pages in os.walk(X['pages']['src']):
    for page in pages:
      src = os.path.join(root,page)
      dst = os.path.join(X['pages']['dst'],page)
      print_page(src,dst)
  # MATLAB pages
  for root, dirs, pages in os.walk(X['mlab']['pages']['dst']):
    for page in pages:
      src = os.path.join(root,page)
      dst = os.path.join(root,page)
      print_page(src,dst)

def print_page(src,dst):
  # read the template
  template = file_read(X['template']['html'])
  # read the file contents
  content  = file_read(src)
  # generate the navbar using relative links
  navstr   = print_navbar(dst)
  # add the content and navbar
  pagestr  = add_to_template(template,'__content__',content)
  pagestr  = add_to_template(pagestr, '__navbar__',navstr)
  # write to file
  file_write(dst,pagestr)

def print_navbar(filepath):
  # print the navbar for any particular html page
  global X
  
  # print the navlink from the html page to one of the main pages
  def nav_link(navstr,linkbase,page):
    pagename = os.path.splitext(page)[0]
    link     = os.path.join(linkbase,page)
    navstr  += "      " + print_navlink(link, pagename) + "\n"
    return navstr
  
  # get the relative link path
  linkbase = rel_link(filepath,X['pages']['dst'])
  
  # Home first
  navstr  = "<ul class='expanded dropdown menu' data-dropdown-menu><li>\n"
  navstr = nav_link(navstr,linkbase,"Home.html")
  # walk the other main pages for the navbar
  for root, dirs, pages in os.walk(X['pages']['src']):
    for page in pages:
      if page != "Home.html":
        navstr = nav_link(navstr,linkbase,page)
  navstr += "    </li></ul>"
  return navstr  
    
def print_navlink(pagelink,pagename):
  navlinkstr = "<a class='expanded button' href='" \
             + pagelink + "'>" + pagename + "</a>"
  return navlinkstr

# ------------------------------------------------------------------------------
# misc. functions
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
      f.write(line)#.encode('ascii', 'replace'))
      
def print_h1(str,contentwidth):
  return "<div class='divh1'><h1>"+str+"</h1></div>\n"+\
         "<div class='content' style='width: "+contentwidth+"; max-width: 100%;'>"

def print_h2(str):
  return "<div class='divh2'><h2>"+str+"</h2></div>\n"

def copyover(src,dst):
  try:
    if os.path.exists(dst):
      shutil.rmtree(dst)
    shutil.copytree(src,dst)
  except OSError as e:
    if e.errno == errno.ENOTDIR:
      shutil.copy(src,dst)
    else:
      print('%s' % e)

def add_to_template(template,keystr,content):
  for i in range(0,len(template)):
    if template[i].find(keystr) >= 0:
      idx = i
  pagestr = template[:idx]
  pagestr += content[:]
  pagestr += template[idx+1:]
  return pagestr
  
def rel_link(src,dst):
  # find the relative link between paths
  def seps(path):
    return path.count('\\') + path.count('/')

  common = os.path.commonprefix([src,dst])
  backup = seps(src) - seps(common)
  link   = '../'*backup + dst.replace(common,'')
  return link
  
      
# ------------------------------------------------------------------------------
# main
# ------------------------------------------------------------------------------

for arg in sys.argv[1:]:
  if arg in 'awds':
    update_awards()
  elif arg in 'mlab':
    update_matlab()
  elif arg in 'pubs':
    update_pubs()
  elif arg in 'pages':
    update_pages()
  else:
    print('ERROR: ARG NAME')

