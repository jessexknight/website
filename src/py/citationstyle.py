def basic():
  return (['{author}, ',
<<<<<<< HEAD
           '<a href="../docs/{ID}.pdf" target="_blank">',
           '{title}</a>, ',
=======
           '{title}, ',
>>>>>>> 682cecdfc7576750dd4358b50380ac80ed70a22c
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
  
