from pathlib import Path

css_file = Path("assets/style.css")
js_file = Path("assets/app.js")

if not css_file.exists():
    raise SystemExit("找不到 assets/style.css")

if not js_file.exists():
    raise SystemExit("找不到 assets/app.js")

css = css_file.read_text(encoding="utf-8")

marker = "/* ZORIX NEWSROOM COMPACT PATCH V3 */"

patch_css = r'''
/* ZORIX NEWSROOM COMPACT PATCH V3 */

:root {
  --news-max: 1060px;
  --article-max: 760px;
}

html {
  background: #ffffff;
}

body {
  background: #ffffff;
  color: #0a0a0a;
  font-family:
    "Noto Sans SC",
    "PingFang SC",
    "Microsoft YaHei",
    "Helvetica Neue",
    Arial,
    system-ui,
    -apple-system,
    sans-serif;
  font-weight: 400;
  letter-spacing: 0;
}

body::before {
  display: none;
}

.shell {
  width: min(var(--news-max), calc(100% - 48px));
}

.header {
  height: 88px;
  border-bottom: 1px solid #ededed;
}

.brand-logo {
  width: 44px;
  height: 44px;
  filter: none;
}

.brand-name {
  font-size: 21px;
  font-weight: 650;
  letter-spacing: -0.025em;
}

.brand-section {
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.09em;
}

.lang-button,
.back-link {
  background: transparent;
  border-color: #dedede;
  border-radius: 999px;
  font-weight: 500;
}

.hero {
  padding: 72px 0 38px;
  text-align: left;
}

.eyebrow {
  display: none;
}

.hero h1,
h1 {
  margin: 0;
  max-width: none;
  font-size: clamp(48px, 8vw, 82px);
  line-height: 1;
  font-weight: 500;
  letter-spacing: -0.055em;
}

.gradient-text {
  background: none;
  color: #090909;
  -webkit-text-fill-color: #090909;
}

.intro {
  max-width: 660px;
  margin: 28px 0 0;
  color: #5f6368;
  font-size: 18px;
  line-height: 1.65;
}

.news-panel {
  width: 100%;
  max-width: var(--news-max);
  margin: 0 auto 90px;
}

.newsroom-controls {
  margin: 0 0 42px;
}

.newsroom-categories {
  display: flex;
  align-items: center;
  gap: 34px;
  overflow-x: auto;
  padding: 18px 0 24px;
  border-bottom: 1px solid #e8e8e8;
  scrollbar-width: none;
}

.newsroom-categories::-webkit-scrollbar {
  display: none;
}

.newsroom-category {
  flex: 0 0 auto;
  appearance: none;
  padding: 0;
  border: 0;
  background: transparent;
  color: #737373;
  font: inherit;
  font-size: 18px;
  font-weight: 450;
  cursor: pointer;
  transition: color .18s ease;
}

.newsroom-category:hover,
.newsroom-category.active {
  color: #080808;
}

.newsroom-tools {
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 72px;
}

.newsroom-tool-group {
  display: flex;
  align-items: center;
  gap: 28px;
}

.newsroom-tool {
  appearance: none;
  border: 0;
  background: transparent;
  color: #111;
  padding: 8px 0;
  font: inherit;
  font-size: 16px;
  cursor: pointer;
}

.newsroom-tool-muted {
  color: #9b9b9b;
}

.news-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 74px;
  padding: 0 0 42px;
}

.news-tile {
  width: 100%;
  max-width: 860px;
  margin: 0 auto;
}

.news-tile-cover {
  width: 100%;
  aspect-ratio: 16 / 9;
  max-height: 480px;
  border-radius: 12px;
  background: #f2f2f2;
}

.news-tile-cover .news-media,
.news-tile-cover .news-media img {
  width: 100%;
  height: 100%;
}

.news-tile-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.news-tile:hover .news-tile-cover img {
  transform: none;
}

.news-tile-copy {
  padding-top: 22px;
}

.news-tile h2 {
  margin: 0 0 12px;
  color: #090909;
  font-size: clamp(27px, 4vw, 38px);
  line-height: 1.22;
  font-weight: 500;
  letter-spacing: -0.035em;
}

.news-tile-summary {
  display: block;
  max-width: 760px;
  margin: 0 0 17px;
  color: #555b61;
  font-size: 16px;
  line-height: 1.72;
  -webkit-line-clamp: 3;
}

.news-tile-meta {
  display: flex;
  align-items: center;
  gap: 18px;
  color: #707070;
  font-size: 15px;
}

.news-tile-meta span {
  color: #111;
}

.news-cover-placeholder {
  font-size: 20px;
  background:
    linear-gradient(135deg, #2563eb, #06b6d4 56%, #22c55e);
}

.article-page {
  max-width: 920px;
  margin: 0 auto;
  padding: 18px 0 90px;
}

.article-back {
  margin-bottom: 52px;
  color: #555;
  font-size: 15px;
  font-weight: 500;
}

.article-header {
  max-width: 850px;
}

.article-meta {
  margin-bottom: 20px;
  font-size: 15px;
}

.article-header h1 {
  margin: 0 0 28px;
  max-width: 850px;
  font-size: clamp(44px, 7vw, 72px);
  line-height: 1.08;
  font-weight: 500;
  letter-spacing: -0.052em;
}

.article-header > p {
  max-width: var(--article-max);
  color: #565b61;
  font-size: 20px;
  line-height: 1.65;
}

.article-hero {
  width: 100%;
  max-width: 860px;
  margin: 52px auto 48px;
  border-radius: 12px;
  overflow: hidden;
  background: #f1f1f1;
}

.article-hero .news-media {
  width: 100%;
}

.article-hero img {
  display: block;
  width: 100%;
  height: auto;
  max-height: 500px;
  object-fit: cover;
}

.article-body {
  max-width: var(--article-max);
  color: #202124;
  font-size: 18px;
  line-height: 1.92;
}

.article-body h2 {
  margin: 52px 0 20px;
  color: #090909;
  font-size: 32px;
  line-height: 1.25;
  font-weight: 550;
}

.article-body h3 {
  margin: 40px 0 16px;
  color: #111;
  font-size: 24px;
  font-weight: 550;
}

.article-body p {
  margin: 0 0 26px;
}

.article-body ul,
.article-body ol {
  padding-left: 25px;
  margin: 0 0 28px;
}

.article-body li {
  margin: 11px 0;
}

.article-body a {
  color: #075fd8;
}

.article-gallery {
  max-width: var(--article-max);
}

.article-gallery .news-media img {
  max-height: 520px;
  object-fit: cover;
}

.footer {
  border-color: #ededed;
}

@media (min-width: 900px) {
  .news-grid.grid-view {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 64px 28px;
  }

  .news-grid.grid-view .news-tile {
    max-width: none;
  }

  .news-grid.grid-view .news-tile-cover {
    aspect-ratio: 16 / 10;
  }

  .news-grid.grid-view .news-tile h2 {
    font-size: 28px;
  }
}

@media (max-width: 760px) {
  .shell {
    width: calc(100% - 30px);
  }

  .header {
    height: 72px;
  }

  .brand-logo {
    width: 38px;
    height: 38px;
  }

  .hero {
    padding: 48px 0 34px;
  }

  .hero h1,
  h1 {
    font-size: 52px;
  }

  .intro {
    display: block;
    margin-top: 20px;
    font-size: 16px;
  }

  .newsroom-controls {
    margin-bottom: 30px;
  }

  .newsroom-categories {
    gap: 25px;
    padding: 14px 0 20px;
  }

  .newsroom-category {
    font-size: 16px;
  }

  .newsroom-tools {
    min-height: 64px;
  }

  .newsroom-tool-group {
    gap: 20px;
  }

  .newsroom-tool {
    font-size: 15px;
  }

  .news-grid {
    gap: 56px;
  }

  .news-tile {
    max-width: 100%;
  }

  .news-tile-cover {
    aspect-ratio: 16 / 9;
    max-height: 330px;
    border-radius: 10px;
  }

  .news-tile-copy {
    padding-top: 17px;
  }

  .news-tile h2 {
    margin-bottom: 10px;
    font-size: 27px;
    line-height: 1.26;
  }

  .news-tile-summary {
    display: -webkit-box;
    margin-bottom: 14px;
    font-size: 15px;
    line-height: 1.65;
    -webkit-line-clamp: 2;
  }

  .news-tile-meta {
    font-size: 14px;
  }

  .article-page {
    padding-top: 8px;
  }

  .article-back {
    margin-bottom: 36px;
  }

  .article-header h1 {
    font-size: 42px;
    line-height: 1.1;
  }

  .article-header > p {
    font-size: 17px;
    line-height: 1.7;
  }

  .article-hero {
    margin: 36px auto 34px;
    border-radius: 10px;
  }

  .article-hero img {
    max-height: 360px;
  }

  .article-body {
    font-size: 17px;
    line-height: 1.86;
  }

  .article-body h2 {
    margin-top: 42px;
    font-size: 28px;
  }

  .article-body h3 {
    margin-top: 34px;
    font-size: 22px;
  }
}
'''

if marker not in css:
    css += "\n" + patch_css
else:
    start = css.index(marker)
    css = css[:start] + patch_css

css_file.write_text(css, encoding="utf-8")

js = js_file.read_text(encoding="utf-8")

toolbar_marker = "ZORIX_NEWSROOM_TOOLBAR_V3"

toolbar_code = r'''
  // ZORIX_NEWSROOM_TOOLBAR_V3
  const newsroomLabels = {
    'zh-CN': {
      all: '全部',
      company: '公司',
      research: '研究',
      product: '产品',
      safety: '安全',
      engineering: '工程',
      filter: '筛选',
      sort: '最新发布',
      grid: '网格视图',
      list: '列表视图'
    },
    en: {
      all: 'All',
      company: 'Company',
      research: 'Research',
      product: 'Product',
      safety: 'Safety',
      engineering: 'Engineering',
      filter: 'Filter',
      sort: 'Newest',
      grid: 'Grid view',
      list: 'List view'
    },
    it: {
      all: 'Tutto',
      company: 'Azienda',
      research: 'Ricerca',
      product: 'Prodotti',
      safety: 'Sicurezza',
      engineering: 'Ingegneria',
      filter: 'Filtra',
      sort: 'Più recenti',
      grid: 'Vista griglia',
      list: 'Vista elenco'
    }
  };

  const newsroomText =
    newsroomLabels[language] ||
    newsroomLabels[language.split('-')[0]] ||
    newsroomLabels.en;

  const newsroomControls = document.createElement('div');
  newsroomControls.className = 'newsroom-controls';
  newsroomControls.innerHTML = `
    <nav class="newsroom-categories" aria-label="News categories">
      <button class="newsroom-category active" type="button" data-news-category="all">${newsroomText.all}</button>
      <button class="newsroom-category" type="button" data-news-category="company">${newsroomText.company}</button>
      <button class="newsroom-category" type="button" data-news-category="research">${newsroomText.research}</button>
      <button class="newsroom-category" type="button" data-news-category="product">${newsroomText.product}</button>
      <button class="newsroom-category" type="button" data-news-category="safety">${newsroomText.safety}</button>
      <button class="newsroom-category" type="button" data-news-category="engineering">${newsroomText.engineering}</button>
    </nav>
    <div class="newsroom-tools">
      <div class="newsroom-tool-group">
        <button class="newsroom-tool" type="button" data-news-filter>${newsroomText.filter}</button>
        <button class="newsroom-tool" type="button" data-news-sort>${newsroomText.sort}</button>
      </div>
      <div class="newsroom-tool-group">
        <button class="newsroom-tool newsroom-tool-muted" type="button" data-view="grid" aria-label="${newsroomText.grid}">▦</button>
        <button class="newsroom-tool" type="button" data-view="list" aria-label="${newsroomText.list}">☰</button>
      </div>
    </div>
  `;

  newsRoot.parentNode.insertBefore(newsroomControls, newsRoot);

  newsroomControls.querySelectorAll('[data-view]').forEach(viewButton => {
    viewButton.addEventListener('click', () => {
      const grid = newsRoot.querySelector('.news-grid');
      if (!grid) return;

      const useGrid = viewButton.dataset.view === 'grid';
      grid.classList.toggle('grid-view', useGrid);

      newsroomControls.querySelectorAll('[data-view]').forEach(button => {
        button.classList.toggle('newsroom-tool-muted', button !== viewButton);
      });
    });
  });
'''

needle = "  const escapeHtml = value =>"

if toolbar_marker not in js:
    if needle not in js:
        raise SystemExit("无法在 app.js 中找到插入位置")
    js = js.replace(needle, toolbar_code + "\n\n" + needle, 1)

# 给 script 和 css 自动增加缓存版本
js_file.write_text(js, encoding="utf-8")

for html_file in Path(".").glob("*/news/index.html"):
    html = html_file.read_text(encoding="utf-8")

    html = html.replace(
        "../../assets/style.css",
        "../../assets/style.css?v=20260703-8"
    )

    html = html.replace(
        "../../assets/app.js",
        "../../assets/app.js?v=20260703-8"
    )

    # 防止重复添加参数
    html = html.replace(
        "style.css?v=20260703-8?v=20260703-8",
        "style.css?v=20260703-8"
    )
    html = html.replace(
        "app.js?v=20260703-8?v=20260703-8",
        "app.js?v=20260703-8"
    )

    html_file.write_text(html, encoding="utf-8")

print("补丁完成：")
print("- 封面尺寸已缩小")
print("- 手机端改为 16:9")
print("- 字体与排版已正式化")
print("- 已加入分类、筛选、排序和视图栏")
print("- 已更新 CSS/JS 缓存版本")
