import os

def seps(path):
  return path.count('\\') + path.count('/')

src = '../matlab/show/clrmaps/america.html'
dst = '../pages/home.html'

common = os.path.commonprefix([src,dst])
backup = seps(src) - seps(common)
link = '../'*backup + dst.replace(common,'')
print(link)

