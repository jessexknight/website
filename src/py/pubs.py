import os
import re
import numpy as np
import bibtexparser as bib
from utils import *

class Publication:
  def __init__(self,bibdata):
    self.data = bibdata
    self.type = bibdata.get('ENTRYTYPE')
  
  def get_data(self,dataname):
    return self.data.get(dataname)
  
  def print_author(self):
    authors = re.split(' and ',self.get_data('author'))
    authorstr = ''
    for i in range(0,len(authors)):
      [last,first] = re.split(', ',authors[i])
      inits = re.split(' ',first)
      if i == len(authors)-1:
        authorstr += 'and '
      for init in inits:
        authorstr += init[0]+' '
      authorstr += last+', '
    return authorstr
  
  def print_title(self):
    title = self.get_data('title')
    link  = os.path.join(root.dst,'docs',self.get_data('ID')+'.pdf')
    if os.path.isfile(link):
      titlestr = '"<a href="'+link+'" target="_blank">'+title+'</a>" '
    else:
      titlestr = '"'+title+'" '
    return titlestr
  
  def print_pubin(self):
    if (self.type in 'article'):
      pubinstr = self.get_data('journal')
    if (self.type in 'inproceedings')\
    or (self.type in 'incollection'):
      pubinstr = self.get_data('booktitle')
    if pubinstr is not None:
      pubinstr = '<i>'+pubinstr+'</i>. '
    else:
      pubinstr = ''
    return pubinstr
  
  def print_volno(self):
    vol = self.get_data('volume')
    no  = self.get_data('number')
    volnostr = ''
    if vol is not None:
      volnostr += '<b>'+vol+'</b>'
    if no is not None:
      volnostr += '('+no+')'
    if volnostr is not '':
      volnostr += ', '
    return volnostr
  
  def print_pages(self):
    pagestr = self.get_data('pages')
    if pagestr is not None:
      pagestr = pagestr.replace('--','-') + '. '
    else:
      pagestr = ''
    return pagestr
  
  def print_year(self):
    yearstr = self.get_data('year')
    if yearstr is not None:
      yearstr = yearstr+'.'
    else:
      yearstr = ''
    return yearstr
    
  def print_publisher(self):
    publisherstr = self.get_data('publisher')
    if publisherstr is not None:
      publisherstr = publisherstr+', '
    else:
      publisherstr = ''
    return publisherstr

  def write_string(self):
    string = '<p>'
    string += self.print_author()
    string += self.print_title()
    string += self.print_pubin()
    if   (self.type in 'article'):
      string += self.print_volno()
    elif (self.type in 'inproceedings'):
      string += self.print_publisher()
    elif (self.type in 'incollection'):
      pass
    string += self.print_pages()
    string += self.print_year()
    string += '</p>'
    return string

def write_all_publications(bibfile,templates):
  publications = get_list_publications(bibfile)
  years, publications = sort_pub_years(publications)
  pubstr = ''
  for i,publication in enumerate(publications):
    if (i==0) or (years[i] != years[i-1]): # current or changing year
      pubstr += templates['h2'].get_sub_content({'h2':years[i]})
    pubstr += publication.write_string()
  pubstr = templates['contentdiv'].get_sub_content({'content':pubstr,'width':'800px'})
  return pubstr
  
def get_list_publications(bibfile):
  with open(bibfile) as f:
    bibdata = bib.loads(f.read())
    P = []
    for data in bibdata.entries_dict.values():
      P.append(Publication(data))
    return P

def sort_pub_years(publications):
  years = []
  for i in range(0,len(publications)):
    years += [publications[i].get_data('year')]
    if years[i] is None:
      years[i] = 'Under Review & In Press'
  idx = np.argsort(years)[::-1]
  years        = [years[i]        for i in idx]
  publications = [publications[i] for i in idx]
  return years, publications
  
