"""SWO メンテナンス事務局 LP（Ver.1）を組み立てる
使い方: python3 -I build.py <srcフォルダ> <出力HTML> [--comp]
--comp を付けると、トップの画像エリアに PIXTA 95794004 の見本（透かし入り）を仮に置いた校正PDF用のHTMLを出す
（見本は出力HTMLと同じフォルダの comp/95794004.jpg を参照）。
納品・確認用URLのHTMLには付けない（見本画像は公開しない）。
"""
import sys, os, json, re

src, out = sys.argv[1], sys.argv[2]
comp = '--comp' in sys.argv
BUILD_TAG = 'swo2026_maintenance_ver1.0 / 2026-10-28'

t = open(os.path.join(src, 'template.html'), encoding='utf-8').read()
css = open(os.path.join(src, 'base_v1.css'), encoding='utf-8').read() + open(os.path.join(src, 'add.css'), encoding='utf-8').read()

def rep(s, old, new, n=1):
    c = s.count(old)
    if c != n:
        raise SystemExit(f'置換数が違う: {old[:40]!r} {c}件（期待 {n}）')
    return s.replace(old, new)

# FAQPage の構造化データは表示中のＱ＆Ａから作る（表示と必ず一致させる）
qa = re.findall(r'<dt><span class="mt-q">Q\.</span>(.*?)</dt>\s*<dd><span class="mt-a">A\.</span>(.*?)</dd>', t)
if len(qa) != 4:
    raise SystemExit(f'FAQの数が違う: {len(qa)}')
ld = {"@context": "https://schema.org", "@type": "FAQPage",
      "mainEntity": [{"@type": "Question", "name": q,
                      "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]}

t = rep(t, '{{BUILD_TAG}}', BUILD_TAG)
t = rep(t, '{{CSS}}', css)
t = rep(t, '{{FAQ_LD}}', json.dumps(ld, ensure_ascii=False, indent=1))
t = rep(t, '{{MORE_WORKS}}', '#works')
t = rep(t, '{{MORE_FAQ}}', '#faq')
for k in ('CASE1_IMG', 'CASE2_IMG', 'CASE3_IMG'):
    t = rep(t, '{{%s}}' % k, '')
if comp:
    img = ('<img src="comp/95794004.jpg" alt="仮画像" class="on">'
           '<span class="comp-badge">仮画像：PIXTA 95794004 の見本（ご購入後に差し替え）</span>')
    t = rep(t, '{{TOP_IMG}}', img)
    t = rep(t, '/* ===== メンテナンス事務局：ここまで ===== */',
            '.media-slot img{object-fit:contain;background:#eef2f6;}\n'
            '.comp-badge{position:absolute;left:10px;top:10px;z-index:2;background:var(--red);color:#fff;'
            'font-size:13px;font-weight:800;padding:4px 10px;border-radius:4px;}\n'
            '/* ===== メンテナンス事務局：ここまで ===== */')
else:
    t = rep(t, '{{TOP_IMG}}', '')
assert '{{' not in t, '置き換え残り'
open(out, 'w', encoding='utf-8').write(t)
print('built', out, len(t), 'comp' if comp else 'deliver')
