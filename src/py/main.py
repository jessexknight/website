import re
from utils import *
from links import *
from parts import *
from pages import *
from pubs  import *

# set the path variables
mode = sys.argv[1]
if mode == 'dev':
  root.live = root.dst
  root.docs = os.path.join(root.live,'docs')
  root.imgs = os.path.join(root.live,'img')

# read all the templates and the pages
templates            = get_dict_parts(os.path.join(root.src,'templates'))
pages                = get_dict_pages()
# build the navbar and add the temaplate to all the pages
templates,pages      = set_page_templates(templates,pages)
# parse the publications
publications         = get_list_publications(root.bib)
pubstr               = write_list_publications(publications,templates,True)
# add json parts to specific pages
pages['Home']        = add_json_parts(templates['projectbox'],pages['Home'],'project')
pages['Home']        = add_json_parts(templates['linkimg'],pages['Home'])
pages['Teaching']    = add_json_parts(templates['course'], pages['Teaching'])
pages['Teaching']    = add_json_parts(templates['samplebox'],pages['Teaching'],'sample')
pages['Links']       = add_json_parts(templates['linktxt'],pages['Links'])
pages['Sample Work'] = add_json_parts(templates['samplebox'],pages['Sample Work'],'sample')
# some special case clean-up
pages['Publications'].set_sub_content({'publications':pubstr})
pages['Home'].set_sub_content({'imgwidth':'25%'})
# cleaning up any missing docs/img links
for key in pages.keys():
  pages[key].set_sub_content({'docs':os.path.join(root.docs,'')})
  pages[key].set_sub_content({'img':os.path.join(root.imgs,'')})
  
write_pages(pages)
