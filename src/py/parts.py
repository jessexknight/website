import sys
import os
import numpy as np
from utils import *
from links import *

class Part:
  def __init__(self,name,src):
    self.name    = name
    self.src     = link(src)
    self.load_content()
  
  def get_name(self):
    return self.name
  
  def get_src_link(self):
    return self.src.get_path()
    
  def get_content(self):
    return self.content

  def load_content(self):
    if os.path.isfile(self.src.get_path()):
      self.content = file_read(self.src.get_path())

  def get_sub_content(self, keys):
    # check for same broadcast size, if any
    argsizes = np.unique([listlen(value) for key,value in keys.iteritems()])
    assert len(argsizes) <= 2
    N = max(argsizes)
    # initial copying for broadcast
    content = [self.content[:] for i in range(N)]
    for key, value in keys.iteritems():
      # broadcast the value if singular
      if listlen(value) is 1:
        value = [value for i in range(N)]
      # write the substitutions
      for i in range(N):
        content[i] = content[i].replace(keystr(key),value[i])
    content = ''.join(content)
    return content
  
  def set_content(self, content):
    self.content = content
  
  def set_sub_content(self, keys):
    self.content = self.get_sub_content(keys)

class Template(Part):
  def __init__(self,name,src):
    Part.__init__(self,name,src)

class Page(Part):
  def __init__(self,name,src,dst):
    Part.__init__(self,name,src)
    self.dst = link(dst)

  def get_dst_link(self):
    return self.dst.get_path()
    
  def write(self):
    file_write(self.dst.get_path(), self.get_content())
     
def get_dict_parts(dirname):
  dir = os.path.join(root.src,dirname)
  filenames = get_dir_filenames(dir)
  X = {}
  for filename in filenames:
    name = os.path.splitext(filename)[0]
    X.update({name:Part(name,os.path.join(dir,filename))})
  return X

def get_dict_templates():
  dir = os.path.join(root.src,'templates')
  filenames = get_dir_filenames(dir)
  T = {}
  for filename in filenames:
    name = os.path.splitext(filename)[0]
    T.update({name:Template(name,os.path.join(dir,filename))})
  return T
  
def get_dict_pages():
  dir = os.path.join(root.src,'pages')
  filenames = get_dir_filenames(dir)
  P = {}
  for filename in filenames:
    name = os.path.splitext(filename)[0]
    P.update({name:Page(name,os.path.join(dir,filename),\
                             os.path.join(root.dst,'pages',filename))})
  return P

def part_list_fun(parts, fun):
  if isinstance(parts, list):
    return [getattr(part,fun)() for part in parts]
  if isinstance(parts, dict):
    return [getattr(part,fun)() for key, part in parts.iteritems()]


