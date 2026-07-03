(() => {
  const picker = document.querySelector('.language');
  const button = document.querySelector('.lang-button');
  if (button && picker) {
    button.addEventListener('click', () => {
      const opened = picker.classList.toggle('open');
      button.setAttribute('aria-expanded', String(opened));
    });
    document.addEventListener('click', event => {
      if (!picker.contains(event.target)) {
        picker.classList.remove('open');
        button.setAttribute('aria-expanded', 'false');
      }
    });
  }

  const year = document.querySelector('[data-year]');
  if (year) year.textContent = new Date().getFullYear();

  const newsRoot = document.querySelector('[data-news-root]');
  if (!newsRoot) return;

  // Resolve files from the actual app.js URL, so GitHub Pages repository paths
  // and custom domains both work reliably.
  const scriptUrl = document.currentScript?.src || new URL('../../assets/app.js', window.location.href).href;
  const siteRoot = new URL('../', scriptUrl);
  const dataUrl = new URL('data/news.json', siteRoot).href;

  const language = document.documentElement.lang || 'en';
  const fallbackLanguage = 'en';
  const dictionary = {
    'zh-CN': { loading: '正在加载新闻', emptyTitle: '暂无新闻', emptyText: '最新动态即将发布', errorTitle: '新闻加载失败', errorText: '请检查 data/news.json 的格式或路径。', published: '发布于', updated: '更新于', imageAlt: '新闻配图' },
    en: { loading: 'Loading news', emptyTitle: 'No news yet', emptyText: 'The latest updates will be published here.', errorTitle: 'Unable to load news', errorText: 'Check the format and path of data/news.json.', published: 'Published', updated: 'Updated', imageAlt: 'News image' },
    it: { loading: 'Caricamento delle notizie', emptyTitle: 'Nessuna notizia', emptyText: 'I prossimi aggiornamenti saranno pubblicati qui.', errorTitle: 'Impossibile caricare le notizie', errorText: 'Controlla il formato e il percorso di data/news.json.', published: 'Pubblicato il', updated: 'Aggiornato il', imageAlt: 'Immagine della notizia' },
    es: { loading: 'Cargando noticias', emptyTitle: 'Todavía no hay noticias', emptyText: 'Las próximas novedades se publicarán aquí.', errorTitle: 'No se pudieron cargar las noticias', errorText: 'Comprueba el formato y la ruta de data/news.json.', published: 'Publicado', updated: 'Actualizado', imageAlt: 'Imagen de la noticia' },
    fr: { loading: 'Chargement des actualités', emptyTitle: 'Aucune actualité', emptyText: 'Les prochaines informations seront publiées ici.', errorTitle: 'Impossible de charger les actualités', errorText: 'Vérifiez le format et le chemin de data/news.json.', published: 'Publié le', updated: 'Mis à jour le', imageAlt: 'Image de l’actualité' },
    de: { loading: 'Nachrichten werden geladen', emptyTitle: 'Noch keine Nachrichten', emptyText: 'Neue Mitteilungen werden hier veröffentlicht.', errorTitle: 'Nachrichten konnten nicht geladen werden', errorText: 'Prüfen Sie Format und Pfad von data/news.json.', published: 'Veröffentlicht', updated: 'Aktualisiert', imageAlt: 'Nachrichtenbild' },
    ja: { loading: 'ニュースを読み込んでいます', emptyTitle: 'ニュースはまだありません', emptyText: '最新情報はここに掲載されます。', errorTitle: 'ニュースを読み込めませんでした', errorText: 'data/news.json の形式またはパスを確認してください。', published: '公開日', updated: '更新日', imageAlt: 'ニュース画像' },
    ko: { loading: '뉴스를 불러오는 중', emptyTitle: '아직 뉴스가 없습니다', emptyText: '최신 소식이 이곳에 게시됩니다.', errorTitle: '뉴스를 불러오지 못했습니다', errorText: 'data/news.json의 형식과 경로를 확인하세요.', published: '게시일', updated: '수정일', imageAlt: '뉴스 이미지' }
  };
  const t = dictionary[language] || dictionary[language.split('-')[0]] || dictionary.en;


  const escapeHtml = value => String(value ?? '').replace(/[&<>'"]/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[char]));
  const localized = value => {
    if (value == null) return '';
    if (typeof value !== 'object' || Array.isArray(value)) return value;
    return value[language] ?? value[language.split('-')[0]] ?? value[fallbackLanguage] ?? Object.values(value)[0] ?? '';
  };
  const formatDate = value => {
    if (!value) return '';
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return value;
    return new Intl.DateTimeFormat(language, { year: 'numeric', month: 'long', day: 'numeric' }).format(date);
  };
  const resolveAsset = path => {
    if (!path) return '';
    if (/^(https?:|data:|\/)/i.test(path)) return path;
    return new URL(String(path).replace(/^\.\//, ''), siteRoot).href;
  };

  const state = (title, text, loading = false) => `
    <div class="empty ${loading ? 'is-loading' : ''}">
      <div class="empty-mark" aria-hidden="true">
        <svg viewBox="0 0 48 48" fill="none"><rect x="8" y="9" width="32" height="30" rx="8" stroke="#2563EB" stroke-width="2.4"/><path d="M15 18h18M15 24h13M15 30h9" stroke="#06B6D4" stroke-width="2.4" stroke-linecap="round"/><circle cx="34" cy="31" r="3" fill="#22C55E"/></svg>
      </div><h2>${escapeHtml(title)}</h2><p>${escapeHtml(text)}</p>
    </div>`;

  const renderImage = (image, title) => {
    if (!image) return '';
    const source = typeof image === 'string' ? image : image.src;
    if (!source) return '';
    const alt = typeof image === 'object' ? localized(image.alt) : '';
    const caption = typeof image === 'object' ? localized(image.caption) : '';
    return `<figure class="news-media"><img src="${escapeHtml(resolveAsset(source))}" alt="${escapeHtml(alt || title || t.imageAlt)}" loading="lazy" decoding="async">${caption ? `<figcaption>${escapeHtml(caption)}</figcaption>` : ''}</figure>`;
  };

  const articleUrl = article => {
    const url = new URL(window.location.href);
    url.searchParams.set('article', article.id || '');
    url.hash = '';
    return url.href;
  };

  const coverOf = article => {
    if (article.cover) return article.cover;
    if (article.image) return article.image;
    return Array.isArray(article.images) && article.images.length ? article.images[0] : null;
  };

  const renderCard = article => {
    const title = localized(article.title);
    const summary = localized(article.summary || article.excerpt);
    const category = localized(article.category);
    const published = formatDate(article.publishedAt || article.date);
    const cover = coverOf(article);
    const href = articleUrl(article);
    return `<article class="news-tile">
      <a class="news-tile-cover" href="${escapeHtml(href)}" aria-label="${escapeHtml(title)}">
        ${cover ? renderImage(cover, title) : `<div class="news-cover-placeholder" aria-hidden="true"><span>ZORIX</span></div>`}
      </a>
      <div class="news-tile-copy">
        <a class="news-title-link" href="${escapeHtml(href)}"><h2>${escapeHtml(title)}</h2></a>
        ${summary ? `<p class="news-tile-summary">${escapeHtml(summary)}</p>` : ''}
        <div class="news-tile-meta">${category ? `<span>${escapeHtml(category)}</span>` : ''}${published ? `<time datetime="${escapeHtml(article.publishedAt || article.date)}">${escapeHtml(published)}</time>` : ''}</div>
      </div>
    </article>`;
  };

  const renderDetail = article => {
    const title = localized(article.title);
    const summary = localized(article.summary || article.excerpt);
    const html = localized(article.html || article.contentHtml);
    const text = localized(article.content || article.text);
    const category = localized(article.category);
    const images = Array.isArray(article.images) ? article.images : (article.image ? [article.image] : []);
    const cover = coverOf(article);
    const published = formatDate(article.publishedAt || article.date);
    const updated = formatDate(article.updatedAt);
    const listUrl = new URL(window.location.href); listUrl.searchParams.delete('article'); listUrl.hash = '';
    const extraImages = images.filter((_, i) => !(cover && i === 0));
    return `<article class="article-page">
      <a class="article-back" href="${escapeHtml(listUrl.href)}" aria-label="Back"><span aria-hidden="true">←</span>${escapeHtml(language === 'zh-CN' ? '返回新闻' : language === 'it' ? 'Torna alle notizie' : 'Back to news')}</a>
      <header class="article-header">
        <div class="article-meta">${category ? `<span>${escapeHtml(category)}</span>` : ''}${published ? `<time datetime="${escapeHtml(article.publishedAt || article.date)}">${escapeHtml(published)}</time>` : ''}</div>
        <h1>${escapeHtml(title)}</h1>
        ${summary ? `<p>${escapeHtml(summary)}</p>` : ''}
        ${updated ? `<div class="article-updated">${escapeHtml(t.updated)} ${escapeHtml(updated)}</div>` : ''}
      </header>
      ${cover ? `<div class="article-hero">${renderImage(cover, title)}</div>` : ''}
      <div class="article-body rich-content">${html || (text ? escapeHtml(text).replace(/\n/g, '<br>') : '')}</div>
      ${extraImages.length ? `<div class="article-gallery">${extraImages.map(image => renderImage(image, title)).join('')}</div>` : ''}
    </article>`;
  };

  newsRoot.innerHTML = state(t.loading, '', true);
  fetch(dataUrl, { cache: 'no-store' })
    .then(response => {
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.json();
    })
    .then(data => {
      const items = Array.isArray(data) ? data : (Array.isArray(data.news) ? data.news : []);
      const visible = items.filter(item => item && item.published !== false).sort((a, b) => new Date(b.publishedAt || b.date || 0) - new Date(a.publishedAt || a.date || 0));
      const selectedId = new URL(window.location.href).searchParams.get('article');
      const selected = selectedId ? visible.find(item => String(item.id) === selectedId) : null;
      if (selectedId && !selected) {
        newsRoot.innerHTML = state(t.errorTitle, language === 'zh-CN' ? '未找到这篇新闻。' : 'Article not found.');
        return;
      }
      newsRoot.innerHTML = selected ? renderDetail(selected) : (visible.length ? `<div class="news-grid">${visible.map(renderCard).join('')}</div>` : state(t.emptyTitle, t.emptyText));
    })
    .catch(error => {
      console.error('Zorix News JSON error:', error, 'URL:', dataUrl);
      newsRoot.innerHTML = state(t.errorTitle, t.errorText);
    });
})();
