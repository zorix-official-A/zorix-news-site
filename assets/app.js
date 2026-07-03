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
    return `../../${String(path).replace(/^\.\//, '')}`;
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

  const renderArticle = article => {
    const title = localized(article.title);
    const summary = localized(article.summary || article.excerpt);
    const html = localized(article.html || article.contentHtml);
    const text = localized(article.content || article.text);
    const category = localized(article.category);
    const images = Array.isArray(article.images) ? article.images : (article.image ? [article.image] : []);
    const published = formatDate(article.publishedAt || article.date);
    const updated = formatDate(article.updatedAt);
    const id = escapeHtml(article.id || '');
    return `<article class="news-card" ${id ? `id="${id}"` : ''}>
      ${images[0] ? renderImage(images[0], title) : ''}
      <div class="news-card-body">
        <div class="news-meta">${category ? `<span class="news-category">${escapeHtml(category)}</span>` : ''}${published ? `<time datetime="${escapeHtml(article.publishedAt || article.date)}">${escapeHtml(t.published)} ${escapeHtml(published)}</time>` : ''}${updated ? `<span>${escapeHtml(t.updated)} ${escapeHtml(updated)}</span>` : ''}</div>
        ${title ? `<h2>${escapeHtml(title)}</h2>` : ''}
        ${summary ? `<p class="news-summary">${escapeHtml(summary)}</p>` : ''}
        ${html ? `<div class="news-content rich-content">${html}</div>` : (text ? `<div class="news-content">${escapeHtml(text).replace(/\n/g, '<br>')}</div>` : '')}
        ${images.slice(1).map(image => renderImage(image, title)).join('')}
      </div>
    </article>`;
  };

  newsRoot.innerHTML = state(t.loading, '', true);
  fetch('../../data/news.json', { cache: 'no-store' })
    .then(response => {
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.json();
    })
    .then(data => {
      const items = Array.isArray(data) ? data : (Array.isArray(data.news) ? data.news : []);
      const visible = items.filter(item => item && item.published !== false).sort((a, b) => new Date(b.publishedAt || b.date || 0) - new Date(a.publishedAt || a.date || 0));
      newsRoot.innerHTML = visible.length ? `<div class="news-list">${visible.map(renderArticle).join('')}</div>` : state(t.emptyTitle, t.emptyText);
    })
    .catch(error => {
      console.error('Zorix News JSON error:', error);
      newsRoot.innerHTML = state(t.errorTitle, t.errorText);
    });
})();
