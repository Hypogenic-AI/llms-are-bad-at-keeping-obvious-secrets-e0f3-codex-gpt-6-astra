from pathlib import Path
import fitz
root=Path.cwd();assert (root/'.git').exists()
(root/'notes/rendered').mkdir(exist_ok=True)
for p in sorted((root/'papers/pages').glob('*chunk*.pdf')):
 if (root/'notes'/f'{p.stem}.txt').exists(): continue
 d=fitz.open(p); parts=[]
 for j,page in enumerate(d):
  parts.append(page.get_text())
  pix=page.get_pixmap(matrix=fitz.Matrix(1,1));pix.save(root/'notes/rendered'/f'{p.stem}_{j+1}.png')
 (root/'notes'/f'{p.stem}.txt').write_text('\n'.join(parts))
for p in sorted((root/'papers').glob('*.pdf')):
 d=fitz.open(p); print(p.name,len(d),'pages');(root/'notes'/f'{p.stem}_full.txt').write_text('\n'.join(x.get_text() for x in d))
