#!/usr/bin/env python3
"""Static checks for ingested references, citation consistency, and HTML slide structure."""
from pathlib import Path
import json,sys,hashlib,re
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
errors=[]; passes=[]
def check(value,msg): (passes if value else errors).append(msg)

kb=json.loads((ROOT/'data/knowledge_base.json').read_text(encoding='utf-8'))
manifest=json.loads((ROOT/'data/source_manifest.json').read_text(encoding='utf-8'))
source_ids={x['id'] for x in manifest}
concepts={c['id']:c for c in kb['concepts']}
check(len(manifest)>=5,'五篇以上已 ingest 的資料')
check(len({x['url'] for x in manifest})==len(manifest),'來源 URL 無重複')
check(len(concepts)>=8,'Wiki 至少八個知識節點')
for s in manifest:
    source=ROOT/s['ingested_file'];check(source.is_file() and hashlib.sha256(source.read_bytes()).hexdigest()==s['sha256'],f'{s["id"]}: 筆記檔案存在且 SHA-256 與 manifest 一致')
for c in concepts.values():
    check(bool(c['sources']) and set(c['sources']).issubset(source_ids),f'{c["id"]}: 知識點有有效來源')
check(all((ROOT/name).is_file() for name in ['index.html','wiki.html','slides.html']),'三份入口 HTML 均存在')
wiki=BeautifulSoup((ROOT/'wiki.html').read_text(encoding='utf8'),'html.parser')
for c in concepts:
    check(wiki.find(id=c) is not None, f'{c}: Wiki 內容可透過錨點開啟')
for s in manifest:
    check(wiki.find(id='source-'+s['id']) is not None, f'{s["id"]}: Wiki 來源索引存在')
slides=BeautifulSoup((ROOT/'slides.html').read_text(encoding='utf8'),'html.parser')
sections=slides.select('section.slide')
check(len(sections)==12, f'簡報頁數 = 12，實得 {len(sections)}')
for ix,slide in enumerate(sections,1):
    label=f'第 {ix:02d} 頁'
    cids=[s for s in slide.get('data-concepts','').split(',') if s]
    sids=[s for s in slide.get('data-sources','').split(',') if s]
    check(bool(cids) and set(cids).issubset(concepts), f'{label}: 知識節點引用有效')
    check(bool(sids), f'{label}: 已附上至少一個來源 ID')
    check(set(sids).issubset(source_ids), f'{label}: 來源 ID 有效')
    derived={s for cid in cids if cid in concepts for s in concepts[cid]['sources']}
    check(set(sids)==derived,f'{label}: 簡報引用與 Wiki 知識來源完整一致')
    links=[a.get('href') for a in slide.select('.ref a')]
    check(all('wiki.html#source-'+sid in links for sid in sids),f'{label}: 頁腳來源可點回 Wiki')
check(bool(slides.select_one('#prev') and slides.select_one('#next')),'簡報有前後頁控制')
check(bool(slides.select_one('[data-reveal="answer-quiz"]')),'簡報有互動小測驗')
print('AI AGENTS WIKI PROJECT | QUALITY VALIDATION')
for m in passes: print('[PASS]',m)
for m in errors: print('[FAIL]',m)
print(f'\nRESULT | PASS={len(passes)} | FAIL={len(errors)} | SOURCES={len(manifest)} | CONCEPTS={len(concepts)} | SLIDES={len(sections)}')
sys.exit(1 if errors else 0)
