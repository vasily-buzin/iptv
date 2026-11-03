from pathlib import Path
from urllib.request import Request, urlopen
import re

SOURCE = 'https://raw.githubusercontent.com/Free-TV/IPTV/master/lists/russia.md'
request = Request(SOURCE, headers={'User-Agent': 'IPTV-Russia-Playlist-Updater/1.0'})
with urlopen(request, timeout=30) as response:
    source = response.read().decode('utf-8-sig')

out = ['#EXTM3U']
section = 'Россия'
count = 0
for line in source.splitlines():
    heading = re.match(r'\s*<h2>(.*?)</h2>', line)
    if heading:
        section = re.sub(r'<[^>]*>', '', heading.group(1)).strip()
        continue
    if not line.lstrip().startswith('|'):
        continue
    cols = [c.strip() for c in line.strip().strip('|').split('|')]
    if len(cols) < 5:
        continue
    match = re.search(r'\[>\]\((https?://[^)]+)\)', cols[2])
    if not match:
        continue
    url = match.group(1)
    # Browser pages and DASH streams are not reliably playable as M3U IPTV entries.
    if not re.search(r'\.m3u8(?:\?|$)', url, re.I):
        continue
    name = re.sub(r'[ⓈⒼⓎⓋⓄ]', '', cols[1]).strip()
    logo = re.search(r'<img[^>]*\bsrc="([^"]+)"', cols[3])
    epg = cols[4].replace('\xa0', ' ').strip()
    attrs = [f'tvg-name="{name}"', f'group-title="Россия / {section}"']
    if epg:
        attrs.insert(0, f'tvg-id="{epg}"')
    if logo:
        attrs.insert(-1, f'tvg-logo="{logo.group(1)}"')
    out.extend([f'#EXTINF:-1 {" ".join(attrs)},{name}', url])
    count += 1
if not count:
    raise RuntimeError('No streams found; existing playlist will not be overwritten')
Path('russia.m3u').write_text('\n'.join(out) + '\n', encoding='utf-8')
print(f'Wrote {count} channels')
