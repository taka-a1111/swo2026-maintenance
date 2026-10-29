# SWO メンテナンス事務局 LP — ビルド元（source ブランチ）

- 組み立て：python3 -I _src/build.py _src out/index.html（出力を main の index.html に置く）
- 校正PDF用：python3 -I _src/build.py _src pdfsrc/index.html --comp（PIXTA 見本 pdfsrc/comp/95794004.jpg を置く。見本はリポジトリに入れない）→ python3 _src/make_pdf.py file:///…/pdfsrc/index.html pdf
- QA：python3 _src/qa.py <URL>
