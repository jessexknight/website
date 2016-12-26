import sys
import os
import numpy as np
from utils import *
from links import *

class part:
  def __init__(self,name,src):
    self.name    = name
    self.src     = link(src)
    self.content = file_read(self.src.get_path())
  
  def get_name(self):
    return self.name
  
  def get_content(self):
    return self.content
    
  def set_content(self, content):
    self.content = content
  
  def get_sub_content(self, keys):
    content = self.content
    for key, value in keys.iteritems():
      content = list_replace(content,keystr(key),value)

