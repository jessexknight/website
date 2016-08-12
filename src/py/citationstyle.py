def basic():
  return (['{author}, ',
           '<a href="../docs/{ID}.pdf" target="_blank">',
           '{title}</a>, ',
           '<i>{journal}</i>, ',
           'vol. {volume}, ',
           'no. {number}, ',
           '{pages}, ',
           '{year}.'])

def abstract():
  return (['{author}, ',
           '{title}, ',
           '<i>{journal}</i>, ',
           'vol. {volume}, ',
           'no. {number}, ',
           '{year}.',
           '{pages}, ',
           '<br>{abstract}'])
  
