import simplejson as json
import os
from utils import *
from links import *
from parts import *

class Page(Part):
  def __init__(self,name,src,dst):
    Part.__init__(self,name,src)
    self.dst = link(dst)

  def get_dst_link(self):
    return self.dst.get_path()
    
  def write(self):
    file_write(self.dst.get_path(), self.get_content())
    
def get_dict_pages():
  dir = os.path.join(root.src,'pages')
  filenames = get_dir_filenames(dir)
  P = {}
  for filename in filenames:
    name = os.path.splitext(filename)[0]
    P.update({name:Page(name,os.path.join(dir,filename),\
                             os.path.join(root.dst,'pages',filename))})
  return P

def write_pages(pages):
  if isinstance(pages,Page):
    pages.write()
  elif isinstance(pages,dict):
    for _,page in pages.iteritems():
      page.write()
  else:
    print '(!) Page must be singular or dictionary of Pages.'

def set_page_templates(templates,pages):
  # get the page names and links
  pagenames = part_list_fun(pages,'get_name')
  pagelinks = part_list_fun(pages,'get_dst_link')
  # build the navbar using the navlink template
  for pagename,pagelink in zip(pagenames,pagelinks):
    pagedict = {'pagename':pagename,'pagelink':pagelink}
    navlink  = templates['navlink'].get_sub_content(pagedict)
    templates['navbar'].set_sub_content({'navlink.'+pagename:navlink})
  # update the page template with the navbar and icon
  templates['page'].set_sub_content(\
    {'navbar':templates['navbar'].get_content(),\
     'icon':os.path.join(root.dst,'img','icon.png')})
  # add the template wrapper to each page
  for name,_ in pages.iteritems():
    pagedict = {'content':pages[name].get_content()}
    pages[name].set_content(templates['page'].get_sub_content(pagedict))
    pages[name].set_sub_content({'pagename':name})
  return templates, pages

def add_json_parts(template, pages):
  partname = template.get_name()
  parts = get_dict_parts(os.path.join(root.cont, partname))
  for itemname,_ in parts.iteritems():
    itemdict = json.loads(parts[itemname].get_content())
    itemkey  = partname+'.'+itemname
    if isinstance(pages,Page):
      pages.set_sub_content({itemkey:template.get_sub_content(itemdict)})
    elif isinstance(pages,dict):
      for pagename,_ in pages.iteritems():
        pages[pagename].set_sub_content({itemkey:template.get_sub_content(itemdict)})
    else:
      print '(!) Page must be singular or dictionary of Pages.'
  return pages