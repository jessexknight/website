import os
import shutil
import errno
import re
from attrdict import AttrDict

root = AttrDict()
root.src  = 'C:/users/jesse/documents/dev/website/website/src/'
root.dst  = 'C:/users/jesse/documents/dev/website/website/live/'
root.live = root.dst
#root.live = 'http://www.uoguelph.ca/~jknigh04/'
root.cont = os.path.join(root.src,'content')
root.bib  = os.path.join(root.src,'docs','pubs.bib')
root.docs = os.path.join(root.live,'docs')
root.imgs = os.path.join(root.live,'img')
 
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

def file_read(fname):
  # read from file
  with open(fname,'r') as f:
    str = f.read()
  return str

def file_write(fname, str):
  # overwtrite file entirely
  with open(fname,'w') as f:
    f.write(str)

def get_dir_filenames(dir):
  filenames = []
  for rnames, dnames, fnames in os.walk(dir):
    for f in fnames:
      filenames.append(f)
  return filenames
  
def keystr(str):
  return '__'+str+'__'

def listlen(obj):
  if isinstance(obj,list):
    return len(obj)
  elif isinstance(obj,str):
    return 1
  elif isinstance(obj,unicode):
    return 1
  else:
    return 0

  