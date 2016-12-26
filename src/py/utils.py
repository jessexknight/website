import os
import shutil
import errno
import re
from attrdict import AttrDict

root = AttrDict()
root.base = 'C:/users/jesse/documents/dev/website/website/'
root.src  = os.path.join(root.base,'src')
root.dst  = os.path.join(root.base,'live')
root.cont = os.path.join(root.base,'src','content')
 
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

  