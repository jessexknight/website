 def sub_vars(self,vars):
   regex = '##(.+?)##'
   for var, value in vars.iteritems():
     self.content = list_replace_var(self.content,regex,value)
     
def list_replace_var(list,oldregex,new):
  regex = re.compile(oldregex)
  out = list
  for i, item in enumerate(list):
    for match in re.finditer(regex,item):
      out[i] = out[i].replace(match.group(0),new)
  return out