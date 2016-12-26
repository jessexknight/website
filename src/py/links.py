import os
from utils import *

class link:
  def __init__(self,path):
    self.path = path
  
  def get_path(self):
    return self.path
  
  def relative_path(self,path):
      commonpath = os.path.commonprefix([self.path,path])
      ups = self.depth(self.path) - self.depth(commonpath)
      print(commonpath)
      return '../'*ups + path.replace(commonpath,'')

  @staticmethod
  def depth(path):
    return path.count('\\') + path.count('/')