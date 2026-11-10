# メンテナンス事務局 直し3点（2026-11-10 瀧田様 15:43「直し２点」・15:50「直し１点の追加」）
# 前の版の index.html（main）に重ねる。使い方: python3 -I build_r4.py <in.html> <out.html> <old_tag> <new_tag>
import sys
src, dst, old_tag, new_tag = sys.argv[1:5]
t = open(src, encoding='utf-8').read()

def rep(t, a, b, n):
    c = t.count(a)
    if c != n: sys.exit('置換件数が違う: %d != %d : %s' % (c, n, a[:70]))
    return t.replace(a, b)

t = rep(t, old_tag, new_tag, 1)

# 直し3）料金 6ヶ月 35,000／年間 25,000（トップの3プランと「料金・作業範囲」の2か所ずつ）
t = rep(t, '<span class="mt-num">30,000</span>', '<span class="mt-num">35,000</span>', 2)
t = rep(t, '<span class="mt-num">20,000</span>', '<span class="mt-num">25,000</span>', 2)

# 直し2）フッターの社名（Science Web株式会社 のときだけ置換。すでに日本語なら0件）
n = t.count('<p class="ft-brand">Science Web株式会社</p>')
if n:
    t = rep(t, '<p class="ft-brand">Science Web株式会社</p>', '<p class="ft-brand">サイエンスウェブ株式会社</p>', 1)
    t = rep(t, '<p class="ft-copy">© Science Web株式会社 All Rights Reserved.</p>', '<p class="ft-copy">© サイエンスウェブ株式会社 All Rights Reserved.</p>', 1)
print('フッター置換', n)

# 直し1）大見出し 濃いオレンジ・左寄せ（キャッチの1行も見出しにそろえて左寄せ）
css = '''
/* ===== 2026-11-10 直し（瀧田様 15:43・15:50）：ここから ===== */
.mt-hero .mt-hero-c{text-align:left;}
.mt-hero .mt-h1.mt-h1-big{color:#E65100;}
/* ===== 2026-11-10 直し：ここまで ===== */
'''
t = rep(t, '</style>', css + '</style>', 1)
open(dst, 'w', encoding='utf-8').write(t)
for w in ('30,000', '20,000', 'Science Web株式会社</p>'):
    print('残り', w, t.count(w))
print('ok')
