"""CER = summed Levenshtein edits / reference characters; Unicode code points."""
import unicodedata

def normalize(text, mode='literal'):
 text=unicodedata.normalize('NFC',text)
 if mode=='reading':
  text=''.join(c for c in text.casefold() if not unicodedata.category(c).startswith('P'))
 elif mode!='literal':raise ValueError(mode)
 return ' '.join(text.split())

def distance(reference,hypothesis):
 previous=list(range(len(hypothesis)+1))
 for i,a in enumerate(reference,1):
  current=[i]
  for j,b in enumerate(hypothesis,1):current.append(min(current[-1]+1,previous[j]+1,previous[j-1]+(a!=b)))
  previous=current
 return previous[-1]

def score(reference,hypothesis,mode='literal'):
 r,h=normalize(reference,mode),normalize(hypothesis,mode)
 if not r:raise ValueError('Empty normalized reference cannot define CER')
 n=distance(r,h)
 return dict(edits=n,reference_characters=len(r),cer=n/len(r),reference_normalized=r,hypothesis_normalized=h)
