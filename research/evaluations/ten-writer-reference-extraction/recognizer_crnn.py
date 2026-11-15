"""Russian CRNN architecture based on achimrabus/polyscriptor, inference_pylaia_native.py.
Weights: https://huggingface.co/achimrabus/crnn-ctc-russian
Original inference source: https://github.com/achimrabus/polyscriptor/blob/main/inference_pylaia_native.py
"""
import torch
from torch import nn
import numpy as np
from PIL import Image
class CRNN(nn.Module):
 def __init__(self,classes):
  super().__init__();layers=[];channels=1
  for filters,pool in zip([12,24,48,48],[2,2,0,2]):
   layers.extend([nn.Conv2d(channels,filters,3,padding=1),nn.BatchNorm2d(filters),nn.LeakyReLU(.2,inplace=True)])
   if pool:layers.append(nn.MaxPool2d(2,2))
   channels=filters
  self.cnn=nn.Sequential(*layers);self.rnn=nn.LSTM(48*16,256,3,dropout=.5,bidirectional=True);self.lin_dropout=nn.Dropout(.5);self.fc=nn.Linear(512,classes)
 def forward(self,x):
  x=self.cnn(x);b,c,h,w=x.shape;x=x.permute(3,0,1,2).reshape(w,b,c*h);x,_=self.rnn(x);return self.fc(self.lin_dropout(x)).log_softmax(2)
class Recognizer:
 def __init__(self,path):
  torch.set_num_threads(2);p=torch.load(path,map_location='cpu',weights_only=True);self.model=CRNN(p['model_state_dict']['fc.weight'].shape[0]);self.model.load_state_dict(p['model_state_dict'],strict=True);self.model.eval();self.chars={int(k):(' ' if v.lower()=='<space>' else v) for k,v in p['idx2char'].items()}
 def read(self,path):
  im=Image.open(path).convert('L');im=im.resize((int(128*im.width/im.height),128),Image.Resampling.LANCZOS);x=torch.from_numpy(np.array(im,dtype=np.float32)/255.).sub(.5).div(.5)[None,None]
  with torch.inference_mode():ids=self.model(x).argmax(2).flatten().tolist()
  result=[];last=None
  for i in ids:
   if i!=last and i:result.append(self.chars.get(i,''))
   last=i
  return ''.join(result)
if __name__=='__main__':
 import sys
 r=Recognizer(sys.argv[1])
 for p in sys.argv[2:]:print(p,repr(r.read(p)))
