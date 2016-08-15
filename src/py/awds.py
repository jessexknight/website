newline = '\n<br>'

# ------------------------------------------------------------------------------
# definitions
# ------------------------------------------------------------------------------

def awards():
  # 1: display award?
  # 2: display description?
  # 3: award name
  # 4: date(s) recieved
  # 5: description
  return([ \
  [1, 0, 'Engineering Peer Helper of the Year',\
         'April  2015, 2016',\
         'Awareded to an enthusiastic and passionate Engineering Peer Helper who encourages others to develop confidence in independent learning through problem solving.'],\
  [1, 0, 'The Schumann Award',\
         'April 2016',\
         'Awarded to a student who is a leader in strategic, creative and critical uses of technology for learning, and has a broad appreciation of the impact of technology on education.'],\
  [1, 0, 'Peer Helper Program Academic Award of Achievement',\
         'May 2016',\
         'Awarded to the continuing Peer Helper with the highest cumulative average.'],\
  [1, 0, 'Top 3: Engineering Teaching Assistant of the Year',\
         'May 2016',\
         'Awarded by the Engineering Society to the best teaching assistant, as voted by the students.'],\
  [1, 1, 'E.B. MacNaughton Convocation Medal',\
         'July 2015',\
         'Awarded to the College of Physical and Engineering Science"s nominee for the W.C. Winegard Medal, the most prestigious graduating award at the University of Guelph.'],\
  [1, 1, 'Association of the Processional Engineers Medal',\
         'July 2015',\
         'In recognition of outstanding scholastic performance at the undergraduate level in an engineering program.'],\
  [1, 1, 'College of Physical and Engineering Science Society of Excellence',\
         'July 2015',\
         'Awarded for excellent academic achievement and outstanding contributions to the University of Guelph community and beyond throughout university career.'],\
  [1, 0, 'Helen Grade Tucker Design Award',\
         'July 2015',\
         'Graduating student with the highest overall average in ENGG 2100, ENGG 3100 and ENGG 41X0, the final design course.'],\
  [1, 0, 'Deans Scholarship (CPES)',\
         'May 2013, 2014, 2015',\
         'In recognition of achieving a high level of academic excellence within the college.'],\
  ])

def funds():
  # 1: display award?
  # 2: display description?
  # 3: award name
  # 4: date(s) recieved
  # 5: description
  return([ \
  [1, 0, 'Ontario Graduate Scholarship - M',\
         '2015 - 2016',\
         'Aims: to fully automate the segmentation of white matter lesions (WML) using FLAIR MRI alone. WML are implicated in Multiple Sclerosis, stroke, and other neurodegenerative diseases.'],\
  [1, 1, 'Canadian Graduate Scholarship - M (NSERC)',\
         '2016 - 2017',\
         'Aims: to fully automate the segmentation of white matter lesions (WML) using FLAIR MRI alone. WML are implicated in Multiple Sclerosis, stroke, and other neurodegenerative diseases.'],\
  ])

# ------------------------------------------------------------------------------
# printing styles
# ------------------------------------------------------------------------------

def print_desc(award):
  global newline
  return('<p class="aleft">'  + award[2] + '</p>'+\
         '<p class="aright">' + award[3] + '</p>'+newline+\
         '<div><p class="aleft" style="border-left: solid thick #CCCCCC; padding: 0 0 0 20"><i>'+\
         award[4]+'</i></p></div>')
  
def print_nodesc(award):
  return('<p class="aleft">'  + award[2] + '</p>'+\
         '<p class="aright">' + award[3] + '</p>')
  
  
  