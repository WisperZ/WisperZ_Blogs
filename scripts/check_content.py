from pathlib import Path
from urllib.parse import unquote,urlsplit
import re,json,tomllib,posixpath,sys
import yaml

ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'
KEYS=['id','title','description','status','created','updated','tags','aliases']
errors=[];ids=set();links=0;pages=sorted(DOCS.rglob('*.md'))
files={p.relative_to(DOCS).as_posix() for p in DOCS.rglob('*') if p.is_file()}
for p in pages:
 rel=p.relative_to(DOCS).as_posix();text=p.read_text(encoding='utf-8-sig')
 m=re.match(r'^---\n(.*?)\n---\n?',text,re.S)
 if not m:errors.append(f'{rel}: 缺少头部');continue
 meta=yaml.safe_load(m[1])
 if list(meta)!=KEYS:errors.append(f'{rel}: 头部字段或顺序不一致')
 ident=meta.get('id')
 if not isinstance(ident,str) or not re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*',ident):errors.append(f'{rel}: id 格式错误')
 if ident in ids:errors.append(f'{rel}: id 重复')
 ids.add(ident)
 for field in ['title','description']:
  if not isinstance(meta.get(field),str) or not meta[field].strip():errors.append(f'{rel}: {field} 不能为空')
 for field in ['tags','aliases']:
  if not isinstance(meta.get(field),list) or any(not isinstance(x,str) for x in meta[field]):errors.append(f'{rel}: {field} 必须为字符串列表')
 if meta.get('status') not in ['Todo','InProgress','Done','Archive']:errors.append(f'{rel}: status 无效')
 for field in ['created','updated']:
  if meta.get(field) is not None and not re.fullmatch(r'\d{4}-\d{2}-\d{2}(?:[ T]\d{2}:\d{2}(?::\d{2})?)?',str(meta[field])):errors.append(f'{rel}: {field} 日期格式错误')
 fence=None
 for n,line in enumerate(text[m.end():].splitlines(),1):
  fm=re.match(r'^\s*(`{3,}|~{3,})',line)
  if fm:fence=None if fence else fm[1][0];continue
  if fence:continue
  if re.search(r'!\[\[',line):errors.append(f'{rel}: 未转换的 Obsidian 图片')
  for match in re.finditer(r'(!?)\[[^\]\n]*\]\(([^\n]*?)\)',line):
   raw=match[2]
   if re.match(r'(?i)(?:[a-z][\w+.-]*:|//|#)',raw):continue
   target=posixpath.normpath(posixpath.join(posixpath.dirname(rel),unquote(raw.split('#')[0]).strip('<>')))
   links+=1
   if target not in files:errors.append(f'{rel}: 链接目标不存在或大小写错误: {raw}')
 if fence:errors.append(f'{rel}: 代码围栏未闭合')
for p in DOCS.rglob('*'):
 if p.is_file() and p.suffix.lower() in {'.png','.jpg','.jpeg','.webp','.gif','.svg','.bmp','.ico','.pdf'} and not p.relative_to(DOCS).as_posix().startswith('_resources/'):
  errors.append(f'{p.relative_to(DOCS)}: 附件未归入 _resources')
config=tomllib.loads((ROOT/'zensical.toml').read_text(encoding='utf-8-sig'))
nav=set()
def paths(node):
 if isinstance(node,list):
  for x in node:paths(x)
 elif isinstance(node,dict):
  for x in node.values():paths(x)
 elif isinstance(node,str) and node.endswith('.md'):nav.add(node)
paths(config['project'].get('nav',[]))
expected={p.relative_to(DOCS).as_posix() for p in pages}
if nav!=expected:errors.append('导航与实际文章不一致: '+str(sorted(nav^expected)))
for old,new in config['project']['plugins'].get('redirects',{}).get('redirect_maps',{}).items():
 if new.split('#')[0] not in files:errors.append(f'跳转目标不存在: {old} -> {new}')
 if old.split('#')[0] in files and '#' not in old:errors.append(f'跳转源与当前文章冲突: {old}')
result={'pages':len(pages),'metadata_ids':len(ids),'local_links':links,'redirects':len(config['project']['plugins'].get('redirects',{}).get('redirect_maps',{})),'errors':errors}
print(json.dumps(result,ensure_ascii=False,indent=2))
if errors:sys.exit(1)
