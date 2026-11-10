# SWO メンテナンス事務局 修正版 ver3.0（公開中ページ＝ver2.3＋佐々木様の調整 を土台に重ねる）
import sys, shutil, pathlib
NAVY='#0F62B4'
from PIL import Image, ImageDraw, ImageFont
src = pathlib.Path('live/index.html').read_text(encoding='utf-8')
out = pathlib.Path('out'); (out/'images').mkdir(parents=True, exist_ok=True)

def rep(t, a, b, n=1):
    c = t.count(a)
    if c != n: sys.exit('置換件数が違う: %d != %d : %s' % (c, n, a[:60]))
    return t.replace(a, b)

t = src
t = rep(t, 'swo2026_maintenance_ver2.3 / 2026-10-29', 'swo2026_maintenance_ver3.0 / 2026-11-10')

# 1 大見出し（3行）＋ 2 画像を大見出しの下・左右いっぱい
a = t.index('    <div class="mt-hero-grid">')
b = t.index('    <div class="mt-worry">')
old = t[a:b]
s1 = old.index('      <div class="media-slot mt-top-slot mt-slides"')
s2 = old.rindex('    </div>')          # mt-hero-grid の閉じ
slides = old[s1:s2].rstrip()
assert slides.endswith('</div>') and slides.count('mt-slide"') + slides.count('mt-slide on"') == 4, 'スライドの切り出し'
slides = slides.replace('class="media-slot mt-top-slot mt-slides"', 'class="media-slot mt-top-slot mt-slides mt-wide"')
slides = '\n'.join(l[4:] if l.startswith('      ') else l for l in slides.split('\n'))
new = '''    <div class="mt-hero-txt mt-hero-c">
      <p class="mt-catch">大切なWeb環境を、ずっと安心して使い続けるために。</p>
      <h1 class="mt-h1 mt-h1-big">
        <span class="mt-line">メンテナンス事務局が</span>
        <span class="mt-line">サーバーとメールを</span>
        <span class="mt-line">まるごとサポート</span>
      </h1>
    </div>
  </div>
''' + slides + '''
  <div class="wrap">

    <ul class="mt-plans mt-plans-top" aria-label="料金">
      <li class="mt-plan"><p class="mt-plan-name">3ヶ月プラン</p><p class="mt-plan-price"><span class="mt-num">40,000</span><span class="mt-unit">円／月</span></p></li>
      <li class="mt-plan"><p class="mt-plan-name">6ヶ月プラン</p><p class="mt-plan-price"><span class="mt-num">30,000</span><span class="mt-unit">円／月</span></p><p class="mt-plan-free"><span class="nobr">初月無料</span><span class="nobr">サービス</span></p></li>
      <li class="mt-plan"><p class="mt-plan-name">年間プラン</p><p class="mt-plan-price"><span class="mt-num">20,000</span><span class="mt-unit">円／月</span></p><p class="mt-plan-free"><span class="nobr">初月無料</span><span class="nobr">サービス</span></p></li>
    </ul>
    <p class="mt-tax mt-tax-top">※消費税別</p>

    <p class="mt-mail"><span class="mt-mail-lbl">メールでのご相談</span><a class="mt-mail-a" href="mailto:maintenance@science-web.online"><img src="images/mail-maintenance.png" alt="maintenance@science-web.online" width="1040" height="96"></a></p>

'''
t = t[:a] + new + t[b:]

# 3 料金（料金・作業範囲の画面）
t = rep(t, '<span class="mt-num">35,000</span>円／月', '<span class="mt-num">30,000</span>円／月')
t = rep(t, '<span class="mt-num">25,000</span>円／月', '<span class="mt-num">20,000</span>円／月')

# 構造化データ・meta に旧料金が残っていないか
for w in ('35,000', '25,000', '35000', '25000', 'サーバー・ドメイン・メールの管理を'):
    if w in t: print('残り:', w, t.count(w))

css = '''
/* ===== 2026-11-10 修正：ここから ===== */
.mt-hero{padding-top:36px;}
.mt-hero-c{text-align:center;}
.mt-hero-c .mt-catch{font-size:clamp(11px,3.5vw,20px);white-space:nowrap;margin-bottom:8px;}
.mt-h1.mt-h1-big{font-size:clamp(26px,8.2vw,88px);line-height:1.25;letter-spacing:.02em;}
.mt-h1-big .mt-line{white-space:nowrap;}
.mt-wide{width:100%;max-width:none;margin:22px 0 0;border-radius:0;border-left:0!important;border-right:0!important;aspect-ratio:16/7;max-height:560px;}
.mt-wide .mt-slide img{width:100%;height:100%;object-fit:cover;}
@media (max-width:760px){ .mt-wide{aspect-ratio:3/2;margin-top:16px;} }
.mt-plans.mt-plans-top{grid-template-columns:repeat(3,minmax(0,1fr));margin-top:24px;gap:12px;}
.mt-plans-top .mt-plan{background:#fff;border:2px solid var(--navy);padding:16px 8px;}
.mt-plans-top .mt-plan-name{font-size:clamp(13px,2.2vw,20px);}
.mt-plans-top .mt-plan-price{font-size:clamp(11px,1.8vw,18px);white-space:normal;}
.mt-plans-top .mt-num{font-size:clamp(19px,4.4vw,40px);line-height:1.2;}
.mt-plans-top .mt-unit{display:inline-block;}
.mt-plans-top .mt-plan-free{font-size:clamp(10px,1.6vw,14px);padding:2px 6px;line-height:1.4;}
.mt-tax-top{margin:6px 0 0;text-align:right;font-size:13px;}
.mt-mail{margin:18px 0 0;display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:8px 16px;}
.mt-mail-lbl{font-size:15px;font-weight:800;color:var(--navy);border:1px solid var(--navy);border-radius:4px;padding:2px 10px;background:#fff;}
.mt-mail-a{display:block;width:min(100%,520px);}
.mt-mail-a img{width:100%;height:auto;}
@media (max-width:480px){
  .mt-plans.mt-plans-top{gap:6px;}
  .mt-plans-top .mt-plan{padding:12px 3px;border-width:1.5px;}
  .mt-plans-top .mt-num{display:block;}
}
@media print{ .mt-wide{max-height:none;} }
/* ===== 2026-11-10 修正：ここまで ===== */
'''
t = rep(t, '</style>', css + '</style>') if t.count('</style>') == 1 else None
if t is None: sys.exit('style が複数')
(out/'index.html').write_text(t, encoding='utf-8')
for f in pathlib.Path('live/images').iterdir(): shutil.copy(f, out/'images'/f.name)

# メールアドレスの画像
txt = 'maintenance@science-web.online'
font = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Bold.otf', 56)
W, H = 1040, 96
im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
bb = d.textbbox((0, 0), txt, font=font)
assert bb[2]-bb[0] < W-20, bb
d.text(((W-(bb[2]-bb[0]))/2 - bb[0], (H-(bb[3]-bb[1]))/2 - bb[1]), txt, font=font, fill=NAVY)
d.line([(W-(bb[2]-bb[0]))/2, H-6, (W+(bb[2]-bb[0]))/2, H-6], fill=NAVY, width=3)
im.save(out/'images'/'mail-maintenance.png', optimize=True)
print('ok', len(t))
