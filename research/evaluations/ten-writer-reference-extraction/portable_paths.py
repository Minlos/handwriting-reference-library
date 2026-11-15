"""Resolve frozen audit paths without editing immutable records or image bytes."""
from pathlib import Path
def resolve(root,path):
 root=Path(root);p=Path(path)
 marker='work/ten-writer-study/'
 if marker in str(path):return root/str(path).split(marker,1)[1]
 if not p.is_absolute():return root/p
 if p.is_file():return p
 raise FileNotFoundError('Frozen path unavailable; extract the data archive beside the replay scripts')
