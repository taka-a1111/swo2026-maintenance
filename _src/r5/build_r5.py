# メンテナンス事務局 2026-11-11 瀧田様の回答（14:36）と「発注ルール 事務局トップページ」案（10:26）の反映
# 前の版の index.html（main）に重ねる。使い方: python3 -I build_r5.py <in.html> <out.html> <old_tag> <new_tag>
import sys, re
src, dst, old_tag, new_tag = sys.argv[1:5]
t = open(src, encoding='utf-8').read()

def rep(t, a, b, n):
    c = t.count(a)
    if c != n: sys.exit('置換件数が違う: %d != %d : %s' % (c, n, a[:70]))
    return t.replace(a, b)

t = rep(t, old_tag, new_tag, 1)

# 1) 料金 3ヶ月 30,000／6ヶ月 25,000／年間 20,000（トップと「料金・作業範囲」の2か所ずつ。低い方から順に置換）
t = rep(t, '<span class="mt-num">25,000</span>', '<span class="mt-num">20,000</span>', 2)
t = rep(t, '<span class="mt-num">35,000</span>', '<span class="mt-num">25,000</span>', 2)
t = rep(t, '<span class="mt-num">40,000</span>', '<span class="mt-num">30,000</span>', 2)

# 2) ステッカー（四角・斜め・赤と黒の文字）を料金の下に（トップと「料金・作業範囲」）
sticker = '''
    <div class="mt-sticker-wrap">
      <div class="mt-sticker" role="note">
        <p class="mt-st-l1">期間限定</p>
        <p class="mt-st-l2">脆弱性に勝つプラン</p>
        <p class="mt-st-l3">特別割引</p>
        <p class="mt-st-l4"><span class="mt-st-num">100,000</span>円</p>
        <p class="mt-st-l5">4ヶ月間</p>
        <p class="mt-st-l6">2026年12月1日から<br>2027年3月31日まで。</p>
      </div>
    </div>'''
t = rep(t, '<p class="mt-tax mt-tax-top">※消費税別</p>', '<p class="mt-tax mt-tax-top">※消費税別</p>' + sticker, 1)
t = rep(t, '<p class="mt-tax">※消費税別</p>', '<p class="mt-tax">※消費税別</p>' + sticker, 1)

# 3) 「その他の実績を見る」「その他のFAQを見る」は11月期は隠す（HTMLのコメントにする）
for a in ('<div class="mt-more"><a class="mt-more-btn" href="#works">その他の実績を見る ＞</a></div>',
          '<div class="mt-more"><a class="mt-more-btn" href="#faq">その他のFAQを見る ＞</a></div>'):
    t = rep(t, a, '<!-- 11月期は非表示（2026-11-11 瀧田様の発注ルール）' + a + '-->', 1)

# 4) 「03 料金・作業範囲」の下段にも「ご相談はこちら」「お見積はこちら」（トップと同じボタン・同じ宛先）
m = re.findall(r'<a class="btn mt-btn-talk" href="mailto:([^"]+)">ご相談はこちら ＞</a>', t)
if len(m) != 2 or len(set(m)) != 1: sys.exit('ご相談ボタンが2件・同じ宛先でない: %s' % m)
mail = m[0]
btns = '''
    <div class="mt-btns mt-btns-price">
      <a class="btn mt-btn-talk" href="mailto:%s">ご相談はこちら ＞</a>
      <a class="btn mt-btn-quote" href="mailto:%s">お見積はこちら ＞</a>
    </div>''' % (mail, mail)
anchor = '\n  </div>\n</section>\n\n</div>\n\n<!-- ===================== メンテナンス事務局３'
t = rep(t, anchor, btns + anchor, 1)

css = '''
/* ===== 2026-11-11 料金・ステッカー・ボタン（瀧田様 10:26 の案・14:36 の回答）：ここから ===== */
.mt-sticker-wrap{display:flex;justify-content:center;margin:34px 0 40px;}
.mt-sticker{width:clamp(220px,28vw,280px);aspect-ratio:1/1;box-sizing:border-box;padding:14px 12px;background:#fff;border:4px solid #D32F2F;border-radius:6px;box-shadow:0 6px 16px rgba(0,0,0,.18);transform:rotate(-6deg);display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;gap:2px;}
.mt-sticker p{margin:0;line-height:1.35;}
.mt-sticker .mt-st-l1{display:inline-block;border:2px solid #D32F2F;color:#D32F2F!important;font-weight:900;font-size:14px;padding:1px 12px;border-radius:3px;margin-bottom:4px;}
.mt-sticker .mt-st-l2{color:#111!important;font-weight:900;font-size:clamp(17px,2vw,21px);}
.mt-sticker .mt-st-l3{color:#D32F2F!important;font-weight:900;font-size:15px;margin-top:4px;}
.mt-sticker .mt-st-l4{color:#D32F2F!important;font-weight:900;font-size:18px;line-height:1.15;}
.mt-sticker .mt-st-num{font-size:clamp(34px,4vw,42px);letter-spacing:-.02em;}
.mt-sticker .mt-st-l5{color:#111!important;font-weight:900;font-size:16px;}
.mt-sticker .mt-st-l6{color:#111!important;font-size:12px;font-weight:700;}
.mt-btns.mt-btns-price{margin-top:28px;}
/* ===== 2026-11-11：ここまで ===== */
'''
t = rep(t, '</style>', css + '</style>', 1)
open(dst, 'w', encoding='utf-8').write(t)
for w in ('40,000', '35,000', 'mt-sticker"', 'mt-btn-talk"', '<div class="mt-more">'):
    print('件数', w, t.count(w))
print('宛先', mail)
print('ok')
