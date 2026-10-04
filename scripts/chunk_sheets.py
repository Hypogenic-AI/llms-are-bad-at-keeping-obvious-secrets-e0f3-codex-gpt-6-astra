from pathlib import Path
from PIL import Image
root=Path.cwd(); assert (root/'.git').exists()
for p in sorted((root/'papers/pages').glob('*chunk*.pdf')):
 ims=[Image.open(q).convert('RGB') for q in sorted((root/'notes/rendered').glob(p.stem+'_*.png'))]
 if not ims: continue
 sheet=Image.new('RGB',(sum(i.width for i in ims),max(i.height for i in ims)),'white');x=0
 for im in ims:sheet.paste(im,(x,0));x+=im.width
 sheet.save(root/'notes/rendered'/f'{p.stem}.png')
