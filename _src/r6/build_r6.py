# 2026-11-12 瀧田様の回答（電話受付 平日10時〜15時）の反映。前の版に重ねる
import sys
src, dst, old_tag, new_tag = sys.argv[1:5]
t = open(src, encoding='utf-8').read()
def rep(t, a, b, n):
    c = t.count(a)
    if c != n: sys.exit('置換件数が違う: %d != %d : %s' % (c, n, a[:60]))
    return t.replace(a, b)
t = rep(t, old_tag, new_tag, 1)
t = rep(t, '受付時間：（平日10：00～17：00）', '受付時間：（平日10：00～15：00）', 2)
open(dst, 'w', encoding='utf-8').write(t)
print('ok', t.count('17：00'), t.count('15：00'))
