import json,subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[1];assert Path.cwd()==root and (root/'.git').exists()
repos=['cywinski/eliciting-secret-knowledge','rramnauth2220/representational-suppression','Chacioc/Concise-SAE','wang2226/CI-Steering','yangkevin2/doc-story-generation']
pins={'cywinski/eliciting-secret-knowledge': '45aae57930a7d6ef5503a9b9b23e0b23fd8068ca', 'rramnauth2220/representational-suppression': '1b44dfc61c6e7c3acb21874a940670238bf44d54', 'Chacioc/Concise-SAE': 'ac735478607ebecf3b1ebc4c34c57279c12956d9', 'wang2226/CI-Steering': '5c5edc3261f9cdf11319b47107894e08b2b40c60', 'yangkevin2/doc-story-generation': '9d727cdbae40c72169ab03b729bff4419a113dac'}
manifest=[]
for repo in repos:
 print(root,flush=True);assert (root/'.git').exists()
 path=Path('code')/repo.split('/')[1]
 if not path.exists():
  subprocess.run(['git','clone','--depth','1','--filter=blob:none','--sparse','https://github.com/'+repo+'.git',str(path)],check=True)
  subprocess.run(['git','-C',str(path),'fetch','--depth','1','origin',pins[repo]],check=True)
  subprocess.run(['git','-C',str(path),'checkout','--detach',pins[repo]],check=True)
  subprocess.run(['git','-C',str(path),'sparse-checkout','set','--no-cone','/*','!/results*/','!/outputs/','!/figures/'],check=True)
 sha=subprocess.check_output(['git','-C',str(path),'rev-parse','HEAD'],text=True).strip()
 assert sha==pins[repo], f'Existing checkout differs from pinned commit: {path}'
 manifest.append(dict(repo=repo,url='https://github.com/'+repo,path=str(path),commit=sha,sparse_exclusions=['results*','outputs','figures']))
Path('code/manifest.json').write_text(json.dumps(manifest,indent=2))
