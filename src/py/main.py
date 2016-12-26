import simplejson as json
import re
from utils import *
from links import *
from parts import *
from pubs  import *

def add_navbar(templates,pages):
  pagenames = part_list_fun(pages,'get_name')
  pagelinks = part_list_fun(pages,'get_dst_link')
  navlinks  = templates['navlink'].get_sub_content({'pagename':pagenames,'pagelink':pagelinks})
  navbar    = templates['navbar'].get_sub_content({'navlink':navlinks})
  templates['page'].set_sub_content({'navbar':navbar})
  for name,_ in pages.iteritems():
    pages[name].set_content(templates['page'].get_sub_content({'content':pages[name].get_content()}))
    pages[name].set_sub_content({'pagename':name})
  return templates, pages

def add_parts(template, pages):
  partname = template.get_name()
  parts = get_dict_parts(os.path.join(root.cont, partname))
  for itemname,_ in parts.iteritems():
    itemdict = json.loads(parts[itemname].get_content())
    itemkey  = partname+'.'+itemname
    for pagename,_ in pages.iteritems():
      pages[pagename].set_sub_content({itemkey:template.get_sub_content(itemdict)})
  return pages

def write_pages(pages):
  for _,page in pages.iteritems():
    page.write()

templates       = get_dict_templates()
pages           = get_dict_pages()
templates,pages = add_navbar(templates,pages)
pages           = add_parts(templates['project'],pages)
pages           = add_parts(templates['link'],pages)
pubstr          = write_all_publications(os.path.join(root.src,'docs','pubs.bib'),templates)
#print pages['Publications'].get_content()
pages['Publications'].set_sub_content({'publications':pubstr})
#print pages['Publications'].get_content()
write_pages(pages)
