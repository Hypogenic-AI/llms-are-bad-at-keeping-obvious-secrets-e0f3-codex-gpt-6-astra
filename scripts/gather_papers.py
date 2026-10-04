import requests, pathlib, concurrent.futures, json, re, subprocess, hashlib
ROOT=pathlib.Path.cwd(); assert (ROOT/'.git').exists()
ids='2605.10794 2505.14352 2510.01070 2601.06973 2603.25187 2511.12381 2310.17884 2502.06258 2404.00859 2402.17119'.split()
def get(i):
    out={'id':i}
    for kind in ['abs','pdf']:
        url=f'https://arxiv.org/{kind}/{i}'
        try:
            r=requests.get(url,timeout=90); r.raise_for_status()
            if kind=='pdf':
                assert r.content.startswith(b'%PDF'); p=ROOT/'papers'/f'{i}.pdf';p.write_bytes(r.content)
                out['sha256']=hashlib.sha256(r.content).hexdigest()
                subprocess.run([str(ROOT/'.venv/bin/python'),'.codex/skills/paper-finder/scripts/pdf_chunker.py',str(p),'--pages-per-chunk','3'],check=True,capture_output=True)
            else:
                (ROOT/'notes'/f'{i}_metadata.html').write_text(r.text)
                for key in ['title','author','date']:
                    out[key]=re.findall(r'<meta name="citation_'+key+r'" content="([^"]+)"',r.text)
        except Exception as e:out[kind+'_error']=str(e)
    return out
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex: rows=list(ex.map(get,ids))
(ROOT/'notes/paper_manifest.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))
