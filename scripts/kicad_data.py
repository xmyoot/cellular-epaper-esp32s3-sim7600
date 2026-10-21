"""Small read-only S-expression reader for source/BOM consistency checks."""
import re, json
class Q(str): pass
def parse(text):
 tokens=re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+',text); stack=[]; out=[]
 for t in tokens:
  if t=='(': n=[]; (stack[-1] if stack else out).append(n); stack.append(n)
  elif t==')': stack.pop()
  else: stack[-1].append(Q(json.loads(t)) if t.startswith('"') else t)
 return out[0]
def children(n,k):return [x for x in n if isinstance(x,list) and x and x[0]==k]
def one(n,k,default=None):return next(iter(children(n,k)),default)
def props(n):return {x[1]:x[2] for x in children(n,'property')}
