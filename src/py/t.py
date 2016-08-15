import re

andstr = 'Fanou, E M and Knight, Jesse and Aviv, R I and Hojjat, S-P and Symons, S P and Zhang, L and Wintermark, M'
authors = re.split(' and ',andstr)
str = ''
for i in range(0,len(authors)):
  [last,first] = re.split(', ',authors[i])
  inits = re.split(' ',first)
  if i == len(authors)-1:
    str += 'and '
  for init in inits:
    str += init[0] + ' '
  str += last + ', '
#print(str[:-2])




