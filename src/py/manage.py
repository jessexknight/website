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

  print(X['mlab']['pages']['tmp'])
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
  global newline
  
  # generate the navbar string
  [navstr, srcpaths, dstpaths] = make_navbar()
  
  # add the navbar to the template file
  template = file_read(X['template']['html'])
  template = add_to_template(template,'__navbar__',navstr)
  
  # for all pages, add their contents
  for p in range(0,len(srcpaths)):
    content = file_read(srcpaths[p])
    pagestr = add_to_template(template,'__content__',content)
    file_write(dstpaths[p], pagestr)

def add_to_template(template,keystr,content):
  for i in range(0,len(template)):
    if template[i].find(keystr) >= 0:
      idx = i
  pagestr = template[:idx]
  pagestr += content[:]
  pagestr += template[idx+1:]
  return pagestr

def make_navbar():
  global X
  global newline
  
  # build the paths from found pages
  def nav_link(file,navstr,srcpaths,dstpaths):
    pagename      = os.path.splitext(file)[0]
    link          = os.path.join(X['pages']['lnk'],file)
    # store the page names and links
    srcpaths.append(os.path.join(X['pages']['src'],file))
    dstpaths.append(os.path.join(X['pages']['dst'],file))
    # print the link to the string
    navstr  += "      " + print_navlink(link, pagename) + "\n"
    return [navstr,srcpaths,dstpaths]
  
  # find page names, and add them as links in the menu
  navstr  = "<ul class='expanded dropdown menu' data-dropdown-menu><li>\n"
  # ensure home page link is added at the top
  [navstr,srcpaths,dstpaths] = nav_link("Home.html",navstr,[],[])
  # main pages
  for root, dirs, files in os.walk(X['pages']['src']):
    for file in files:
      if file != "Home.html":
        [navstr,srcpaths,dstpaths] = nav_link(file,navstr,srcpaths,dstpaths)
  # matlab pages
  for root, dirs, files in os.walk(X['mlab']['pages']['dst']):
    for file in files:
      if file != "template.html":
        print(rel_link(os.path.join(root,file),X['pages']['src']))
  
  navstr += "    </li></ul>"
  return [navstr, srcpaths, dstpaths]
    
def print_navlink(pagelink,pagename):
  navlinkstr = "<a class='expanded button' href='" \
             + pagelink + "'>" + pagename + "</a>"
  return navlinkstr

def rel_link(src,dst):
  # find the relative link between paths
  def seps(path):
    return path.count('\\') + path.count('/')

  common = os.path.commonprefix([src,dst])
  backup = seps(src) - seps(common)
  link   = '../'*backup + dst.replace(common,'')
  return link
  
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

