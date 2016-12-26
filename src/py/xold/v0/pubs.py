import os.path
import re
import numpy as np
import bibtexparser as bib

# ------------------------------------------------------------------------------
# main modules 
# ------------------------------------------------------------------------------

# load and parse the bib file
def parse(src_pubbib):
  with open(src_pubbib) as f:
    bibdata = bib.loads(f.read())
    return bibdata.entries_dict.values()

# sort by year (n.d. to inf)
def sortyears(B):
  years = []
  for i in range(0,len(B)):
    years += [B[i].get('year')]
    if years[i] is None:
      years[i] = np.inf
  idx = np.argsort(years)[::-1]
  years = [years[i] for i in idx]
  B     = [B[i]     for i in idx]
  return years, B

# print a bibliographic entry to html
def printstr(bibdata,docs):
  pubtype = bibdata.get('ENTRYTYPE')
  if pubtype in 'article':
    pubstr = print_article(bibdata,docs)
  elif pubtype in 'inproceedings':
    pubstr = print_inproceedings(bibdata,docs)
  elif pubtype in 'incollection':
    pubstr = print_incollection(bibdata,docs)
  else: # defualt
    print(pubtype)
    pubstr = article(bibdata,docs)
  return pubstr

# ------------------------------------------------------------------------------
# string building components
# ------------------------------------------------------------------------------

# print list of authors: J Knight, ... and ... style.
def authors(strauthor):
  authors = re.split(' and ',strauthor)
  authorstr = ''
  for i in range(0,len(authors)):
    [last,first] = re.split(', ',authors[i])
    inits = re.split(' ',first)
    if i == len(authors)-1:
      authorstr += 'and '
    for init in inits:
      authorstr += init[0] + ' '
    authorstr += last + ', '
  return authorstr

# print the title of the publication, attempt to link the .pdf
def title(strtitle, pubid, src_docs, lnk_docs):
  if os.path.isfile(os.path.join(src_docs,pubid+'.pdf')):
    titlestr = '"<a href="' + os.path.join(lnk_docs,pubid+'.pdf')\
             + '" target="_blank">' + strtitle + '</a>"'
  else:
    titlestr = '"'+strtitle+'"'
  return titlestr

# print the pages of the publcation
def pages(strpages):
  if strpages is not None:
    pagestr = strpages.replace('--','-') + '. '
  else:
    pagestr = ''
  return pagestr

# print the year of the publication
def year(stryear):
  if stryear is not None:
    yearstr = stryear+'.'
  else:
    yearstr = ''
  return yearstr

# print the volume & number of the article
def volno(strvol,strno):
  volnostr = ''
  if strvol is not None:
    volnostr += '<b>'+strvol+'</b>'
  if strno is not None:
    volnostr += '('+strno+')'
  if volnostr is not '':
    volnostr += ', '
  return volnostr

# print the journal of the article
def journal(strjournal):
  if strjournal is not None:
    journalstr = '<i>'+strjournal+'</i>. '
  else:
    journalstr = ''
  return journalstr

def publisher(strpublisher):
  if strpublisher is not None:
    publisherstr = strpublisher+', '
  else:
    publisherstr = ''
  return publisherstr

# ------------------------------------------------------------------------------
# types of publications
# ------------------------------------------------------------------------------

def print_article(B, docs):
  pubstr = authors   (B.get('author')) \
         + title     (B.get('title'),B.get('ID'),docs[0],docs[1]) + '. ' \
         + journal   (B.get('journal')) \
         + volno     (B.get('volume'),B.get('number')) \
         + pages     (B.get('pages')) \
         + year      (B.get('year'))
  return pubstr

def print_incollection(B, docs):
  pubstr = authors   (B.get('author')) \
         + title     (B.get('title'),B.get('ID'),docs[0],docs[1]) + ' in ' \
         + journal   (B.get('booktitle')) \
         + publisher (B.get('publisher')) \
         + pages     (B.get('pages')) \
         + year      (B.get('year'))
  return pubstr

def print_inproceedings(B, docs):
  pubstr = authors   (B.get('author')) \
         + title     (B.get('title'),B.get('ID'),docs[0],docs[1]) + ' in ' \
         + journal   (B.get('booktitle')) \
         + pages     (B.get('pages')) \
         + year      (B.get('year'))
  return pubstr
  
