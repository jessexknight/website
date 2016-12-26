import os
from utils import *
from links import *

class template:
  def __init__(self,name,src):
    self.name = keystr(name)
    self.src  = link(os.path.join(root.rel,root.src,'templates',src))
    self.content = file_read(self.src.get_path())

  def get_name(self):
    return self.name
  
  def get_content(self):
    return self.content
    
  def get_sub_content(self,keys):
    content = self.content
    for key, value in keys.iteritems():
      content = list_replace(content,keystr(key),value)
    return content

def get_all_templates():
  tdir = os.path.join(root.rel,root.src,'templates')
  filenames = get_dir_files(tdir)
  T = []
  for filename in filenames:
    T.append(template(os.path.splitext(filename)[0],os.path.join(tdir,filename)))
  return T

def get_template_names(T):
  names = []
  for t in T:
    names.append(t.get_name())
  return names


  
