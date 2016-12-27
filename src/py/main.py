import re
from utils import *
from links import *
from parts import *
from pages import *
from pubs  import *

# read all the templates and the pages
templates         = get_dict_parts(os.path.join(root.src,'templates'))
pages             = get_dict_pages()
# build the navbar and add the temaplate to all the pages
templates,pages   = set_page_templates(templates,pages)
# add json parts to specific pages
pages['Home']     = add_json_parts(templates['project'],pages['Home'])
pages['Home']     = add_json_parts(templates['linkimg'],pages['Home'])
pages['Home'].set_sub_content({'imgwidth':'25%'})
pages['Teaching'] = add_json_parts(templates['course'], pages['Teaching'])
pages['Links']    = add_json_parts(templates['linktxt'],pages['Links'])
pubstr            = write_all_publications(os.path.join(root.src,'docs','pubs.bib'),templates)
pages['Publications'].set_sub_content({'publications':pubstr})
write_pages(pages)
