from pathlib import Path
from html.parser import HTMLParser
import html
import json
import re

ROOT = Path(".")
NEWS_PATH = ROOT / "data/news.json"

SITE_ORIGIN = "https://news.zorix.it"

LANGS = ["zh-CN", "en", "it"]

LANG_LABELS = {
    "zh-CN": "中文",
    "en": "English",
    "it": "Italiano",
}

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag in {"script", "style", "svg", "noscript"}:
            self.skip += 1
        if self.skip == 0 and tag in {"p", "h1", "h2", "h3", "li", "blockquote", "br"}:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in {"script", "style", "svg", "noscript"} and self.skip:
            self.skip -= 1
        if self.skip == 0 and tag in {"p", "h1", "h2", "h3", "li", "blockquote"}:
            self.parts.append("\n")

    def handle_data(self, data):
        if self.skip == 0:
            self.parts.append(data)

    def text(self):
        value = html.unescape(" ".join(self.parts))
        value = value.replace("\xa0", " ")
        value = re.sub(r"\s+", " ", value)
        return value.strip()

def localized(value, lang, fallback=""):
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict):
        for key in [lang, lang.lower(), lang.split("-")[0], "en", "zh-CN", "it"]:
            v = value.get(key)
            if isinstance(v, str) and v.strip():
                return v.strip()
    return fallback

def clean_html_to_text(value):
    parser = TextExtractor()
    parser.feed(value or "")
    parser.close()
    return parser.text()

def absolute_url(path):
    if not path:
        return ""
    if path.startswith("http://") or path.startswith("https://"):
        return path
    if not path.startswith("/"):
        path = "/" + path
    return SITE_ORIGIN + path

def resolve_src(value, lang):
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        for key in [lang, lang.lower(), lang.split("-")[0], "en", "zh-CN", "it", "src"]:
            v = value.get(key)
            if isinstance(v, str) and v.strip():
                return v.strip()
    return ""

def main():
    if not NEWS_PATH.exists():
        raise SystemExit("找不到 data/news.json")

    data = json.loads(NEWS_PATH.read_text(encoding="utf-8"))
    news = data.get("news", [])

    feed_items = []
    by_language = {lang: [] for lang in LANGS}

    for item in news:
        if not isinstance(item, dict):
            continue

        if item.get("published") is False:
            continue

        article_id = item.get("id")
        if not article_id:
            continue

        published_at = item.get("publishedAt", "")
        updated_at = item.get("updatedAt", published_at)

        cover = item.get("cover", {})
        cover_src = ""
        cover_alt = ""

        if isinstance(cover, dict):
            cover_src = cover.get("src", "")
            cover_alt_data = cover.get("alt", "")
        else:
            cover_alt_data = ""

        audio = item.get("audio", {})

        for lang in LANGS:
            title = localized(item.get("title"), lang)
            summary = localized(item.get("summary"), lang)
            category = localized(item.get("category"), lang)
            body_html = localized(item.get("html"), lang)
            body_text = clean_html_to_text(body_html)

            if not title:
                continue

            article_url = f"{SITE_ORIGIN}/{lang}/news/?article={article_id}"

            audio_src = ""
            audio_voice = ""

            if isinstance(audio, dict):
                audio_value = audio.get(lang) or audio.get(lang.lower()) or audio.get(lang.split("-")[0])
                if isinstance(audio_value, str):
                    audio_src = audio_value
                elif isinstance(audio_value, dict):
                    audio_src = audio_value.get("src", "")
                    audio_voice = audio_value.get("voice", "")

            entry = {
                "id": article_id,
                "language": lang,
                "languageLabel": LANG_LABELS.get(lang, lang),
                "title": title,
                "summary": summary,
                "category": category,
                "publishedAt": published_at,
                "updatedAt": updated_at,
                "url": article_url,
                "path": f"/{lang}/news/?article={article_id}",
                "cover": {
                    "src": cover_src,
                    "url": absolute_url(cover_src),
                    "alt": localized(cover_alt_data, lang),
                },
                "audio": {
                    "src": audio_src,
                    "url": absolute_url(audio_src),
                    "voice": audio_voice,
                },
                "text": body_text,
                "html": body_html,
            }

            feed_items.append(entry)
            by_language[lang].append(entry)

    feed_items.sort(
        key=lambda x: (x.get("publishedAt", ""), x.get("id", "")),
        reverse=True,
    )

    for lang in by_language:
        by_language[lang].sort(
            key=lambda x: (x.get("publishedAt", ""), x.get("id", "")),
            reverse=True,
        )

    output = {
        "site": {
            "name": "Zorix News",
            "origin": SITE_ORIGIN,
            "homepage": SITE_ORIGIN,
        },
        "feed": {
            "version": "1.0",
            "generatedFrom": "/data/news.json",
            "paths": {
                "primary": "/data/news-feed.json",
                "mirror": "/news-feed.json",
            },
            "description": "Dedicated multilingual JSON feed for Zorix News crawling and indexing.",
            "languages": LANGS,
            "totalLocalizedItems": len(feed_items),
            "totalArticles": len({item["id"] for item in feed_items}),
        },
        "items": feed_items,
        "byLanguage": by_language,
    }

    for out_path in [
        ROOT / "data/news-feed.json",
        ROOT / "news-feed.json",
    ]:
        out_path.write_text(
            json.dumps(output, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print("已生成:", out_path)

if __name__ == "__main__":
    main()
