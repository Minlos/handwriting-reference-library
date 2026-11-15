"""Portable DeepSeek replay helper. Explicit local budget and environment key required.
No credentials, headers or encoded request payloads are persisted or printed.
This module never buys credits, retries a request, or reads the study owner's account files.
"""
from pathlib import Path
import base64,fcntl,json,os,urllib.request
ROOT=Path(__file__).resolve().parent
MODELS={'deepseek':'deepseek-flash'}
MAX_OUTPUT=8192
RESERVE={'deepseek':0.04}
def write_json(path,data):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_suffix(path.suffix+f'.{os.getpid()}.tmp');tmp.write_text(json.dumps(data,ensure_ascii=False,indent=2));os.replace(tmp,path)
def update_budget(callback):
 with (ROOT/'replay-spend.lock').open('a') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX)
  p=ROOT/'replay-budget.json'
  if not p.exists():raise RuntimeError('Create a separate explicitly approved replay-budget.json before paid replay')
  data=json.loads(p.read_text());result=callback(data);write_json(p,data);return result
def reserve(provider,call_id):
 assert provider=='deepseek'
 def change(data):
  if call_id in data['calls']:raise RuntimeError('Existing call ID: paid request will not be repeated')
  committed=sum(x.get('cost_upper_usd',x['reserved_usd']) for x in data['calls'].values())
  if committed+RESERVE[provider]>data['approved_new_experiment_usd']:raise RuntimeError('Spending approval insufficient for next reserved call')
  data['calls'][call_id]=dict(provider=provider,status='reserved',reserved_usd=RESERVE[provider])
 update_budget(change)
def settle(call_id,cost,status):
 def change(data):
  row=data['calls'][call_id];row['status']=status
  if cost is not None:row['cost_upper_usd']=cost
 update_budget(change)
def credential(provider):
 assert provider=='deepseek';key=os.environ.get('DEEPSEEK_API_KEY','').strip()
 if len(key)<20 or any(x.isspace() for x in key):raise RuntimeError('Set DEEPSEEK_API_KEY in the process environment; never put a key in study files')
 return key
def content(parts,provider):
 assert provider=='deepseek';result=[]
 for kind,value in parts:
  if kind=='text':result.append({'type':'text','text':value})
  else:
   mime='image/png' if value.suffix.lower()=='.png' else 'image/jpeg';url='data:'+mime+';base64,'+base64.b64encode(value.read_bytes()).decode();result.append({'type':'image_url','image_url':{'url':url,'detail':'original'}})
 return result
def request(provider,key,prompt,parts,initial=None):
 assert provider=='deepseek' and initial is None
 payload=dict(model=MODELS[provider],messages=[{'role':'system','content':prompt},{'role':'user','content':content(parts,provider)}],thinking={'type':'disabled'},temperature=0,max_tokens=MAX_OUTPUT,stream=False)
 req=urllib.request.Request('https://api.deepseek.com/chat/completions',data=json.dumps(payload).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=180) as response:return json.load(response)
def extract(provider,response):
 assert provider=='deepseek';usage=response.get('usage',{});choice=response['choices'][0];text=choice['message'].get('content','');complete=choice['finish_reason']=='stop' and bool(text.strip())
 if 'completion_tokens' not in usage or 'prompt_tokens' not in usage:return text,complete,None
 hit=usage.get('prompt_cache_hit_tokens',0);miss=usage.get('prompt_cache_miss_tokens',usage['prompt_tokens']-hit);cost=(hit*.006+miss*.30+usage['completion_tokens']*1.20)/1e6
 return text,complete,cost
