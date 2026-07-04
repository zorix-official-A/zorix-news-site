from __future__ import annotations

import asyncio
import html
import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

import edge_tts


ROOT = Path(__file__).resolve().parent
NEWS_JSON = ROOT / "data" / "news.json"
AUDIO_ROOT = ROOT / "assets" / "audio" / "news"
TEMP_ROOT = AUDIO_ROOT / ".tmp"

# 当前新闻站支持的语言和语音
VOICE_CONFIG = {
    "zh-CN": {
        "voice": "zh-CN-XiaoxiaoNeural",
        "rate": "-4%",
        "volume": "+0%",
        "pitch": "+0Hz",
        "label": "中文",
    },
    "en": {
        "voice": "en-US-AriaNeural",
        "rate": "-3%",
        "volume": "+0%",
        "pitch": "+0Hz",
        "label": "English",
    },
    "it": {
        "voice": "it-IT-ElsaNeural",
        "rate": "-3%",
        "volume": "+0%",
        "pitch": "+0Hz",
        "label": "Italiano",
    },
}

# 避免把这些网页内容直接朗读出来
REMOVE_TAGS = {
    "script",
    "style",
    "svg",
    "pre",
    "code",
    "noscript",
}


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.skip_depth = 0

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        if tag.lower() in REMOVE_TAGS:
            self.skip_depth += 1

        if not self.skip_depth and tag.lower() in {
            "p",
            "h1",
            "h2",
            "h3",
            "h4",
            "li",
            "blockquote",
            "br",
        }:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in REMOVE_TAGS and self.skip_depth:
            self.skip_depth -= 1

        if not self.skip_depth and tag.lower() in {
            "p",
            "h1",
            "h2",
            "h3",
            "h4",
            "li",
            "blockquote",
        }:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self.skip_depth:
            self.parts.append(data)

    def get_text(self) -> str:
        text = html.unescape(" ".join(self.parts))

        # 删除网址，避免语音逐字符读取
        text = re.sub(r"https?://\S+", " ", text)

        # 删除邮箱
        text = re.sub(
            r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b",
            " ",
            text,
        )

        # 规范空格和换行
        text = text.replace("\xa0", " ")
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n\s*\n+", "\n", text)
        text = re.sub(r" *\n *", ". ", text)
        text = re.sub(r"\.{2,}", ".", text)
        text = re.sub(r"\s+", " ", text)

        return text.strip(" .")


def localized(
    value: Any,
    lang: str,
    fallback: str = "",
) -> str:
    if isinstance(value, str):
        return value.strip()

    if isinstance(value, dict):
        candidates = [
            lang,
            lang.lower(),
            lang.split("-")[0],
            "en",
            "zh-CN",
            "it",
        ]

        for key in candidates:
            result = value.get(key)
            if isinstance(result, str) and result.strip():
                return result.strip()

    return fallback


def html_to_text(source: str) -> str:
    parser = TextExtractor()
    parser.feed(source)
    parser.close()
    return parser.get_text()


def build_speech_text(
    article: dict[str, Any],
    lang: str,
) -> str:
    title = localized(article.get("title"), lang)
    summary = localized(article.get("summary"), lang)
    body_html = localized(article.get("html"), lang)
    body = html_to_text(body_html)

    parts: list[str] = []

    if title:
        parts.append(title)

    if summary and summary not in body:
        parts.append(summary)

    if body:
        parts.append(body)

    text = ". ".join(parts)
    text = re.sub(r"\s+", " ", text).strip()

    # 改善部分品牌词读法
    replacements = {
        "ZorixScript": "Zorix Script",
        "ForgeBench": "Forge Bench",
        "Nex Coder": "Nex Coder",
        "26C": "26 C",
        "26B": "26 B",
        "26A": "26 A",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text


def split_text(
    text: str,
    max_chars: int = 2800,
) -> list[str]:
    if len(text) <= max_chars:
        return [text]

    sentences = re.split(
        r"(?<=[。！？.!?])\s+",
        text,
    )

    chunks: list[str] = []
    current = ""

    for sentence in sentences:
        sentence = sentence.strip()

        if not sentence:
            continue

        if len(sentence) > max_chars:
            if current:
                chunks.append(current.strip())
                current = ""

            for start in range(0, len(sentence), max_chars):
                chunks.append(
                    sentence[start:start + max_chars].strip()
                )
            continue

        candidate = (
            f"{current} {sentence}".strip()
            if current
            else sentence
        )

        if len(candidate) > max_chars:
            chunks.append(current.strip())
            current = sentence
        else:
            current = candidate

    if current:
        chunks.append(current.strip())

    return chunks


async def synthesize_chunk(
    text: str,
    output: Path,
    config: dict[str, str],
    retries: int = 3,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)

    last_error: Exception | None = None

    for attempt in range(1, retries + 1):
        try:
            communicate = edge_tts.Communicate(
                text=text,
                voice=config["voice"],
                rate=config["rate"],
                volume=config["volume"],
                pitch=config["pitch"],
            )

            await communicate.save(str(output))

            if not output.exists() or output.stat().st_size < 1000:
                raise RuntimeError(
                    f"生成的音频文件异常：{output}"
                )

            return
        except Exception as error:
            last_error = error
            print(
                f"  第 {attempt}/{retries} 次生成失败：{error}",
                file=sys.stderr,
            )

            if output.exists():
                output.unlink()

            await asyncio.sleep(attempt * 2)

    raise RuntimeError(
        f"无法生成音频：{output}"
    ) from last_error


def concat_mp3(
    parts: list[Path],
    output: Path,
) -> None:
    if len(parts) == 1:
        output.parent.mkdir(parents=True, exist_ok=True)
        parts[0].replace(output)
        return

    list_file = output.parent / f".{output.stem}-concat.txt"

    lines = []

    for part in parts:
        escaped = str(part.resolve()).replace("'", "'\\''")
        lines.append(f"file '{escaped}'")

    list_file.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    command = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(list_file),
        "-c",
        "copy",
        str(output),
    ]

    try:
        subprocess.run(
            command,
            check=True,
        )
    finally:
        list_file.unlink(missing_ok=True)

    for part in parts:
        part.unlink(missing_ok=True)


async def generate_article_audio(
    article: dict[str, Any],
    lang: str,
    config: dict[str, str],
) -> tuple[str, str] | None:
    article_id = str(article.get("id", "")).strip()

    if not article_id:
        print("跳过没有 ID 的新闻")
        return None

    speech_text = build_speech_text(article, lang)

    if len(speech_text) < 20:
        print(
            f"跳过 {article_id} / {lang}：没有足够正文"
        )
        return None

    output_dir = AUDIO_ROOT / article_id
    output_file = output_dir / f"{lang}.mp3"
    temp_dir = TEMP_ROOT / article_id / lang

    output_dir.mkdir(parents=True, exist_ok=True)
    temp_dir.mkdir(parents=True, exist_ok=True)

    chunks = split_text(speech_text)

    print(
        f"生成 {article_id} / {lang}："
        f"{len(speech_text)} 字符，{len(chunks)} 段"
    )

    part_files: list[Path] = []

    for index, chunk in enumerate(chunks, start=1):
        part = temp_dir / f"{index:03d}.mp3"

        print(
            f"  语音段 {index}/{len(chunks)}"
        )

        await synthesize_chunk(
            chunk,
            part,
            config,
        )

        part_files.append(part)

    concat_mp3(
        part_files,
        output_file,
    )

    if not output_file.exists() or output_file.stat().st_size < 1000:
        raise RuntimeError(
            f"最终音频无效：{output_file}"
        )

    relative_url = (
        f"/assets/audio/news/{article_id}/{lang}.mp3"
    )

    print(
        f"  完成：{output_file.stat().st_size / 1024:.1f} KB"
    )

    return lang, relative_url


async def main() -> None:
    if not NEWS_JSON.exists():
        raise SystemExit("找不到 data/news.json")

    data = json.loads(
        NEWS_JSON.read_text(encoding="utf-8")
    )

    news = data.get("news")

    if not isinstance(news, list):
        raise SystemExit(
            "data/news.json 中没有 news 数组"
        )

    AUDIO_ROOT.mkdir(parents=True, exist_ok=True)
    TEMP_ROOT.mkdir(parents=True, exist_ok=True)

    generated = 0
    failed: list[str] = []

    for article in news:
        if not isinstance(article, dict):
            continue

        if article.get("published") is False:
            continue

        article_id = str(
            article.get("id", "unknown")
        )

        audio = article.setdefault("audio", {})

        for lang, config in VOICE_CONFIG.items():
            try:
                result = await generate_article_audio(
                    article,
                    lang,
                    config,
                )

                if result is None:
                    continue

                result_lang, url = result

                audio[result_lang] = {
                    "src": url,
                    "type": "audio/mpeg",
                    "voice": config["voice"],
                    "label": config["label"],
                }

                generated += 1

            except Exception as error:
                failed.append(
                    f"{article_id}/{lang}: {error}"
                )
                print(
                    f"失败：{article_id}/{lang}: {error}",
                    file=sys.stderr,
                )

    NEWS_JSON.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    # 清理空临时目录
    if TEMP_ROOT.exists():
        for path in sorted(
            TEMP_ROOT.rglob("*"),
            reverse=True,
        ):
            if path.is_dir():
                try:
                    path.rmdir()
                except OSError:
                    pass

        try:
            TEMP_ROOT.rmdir()
        except OSError:
            pass

    print()
    print(f"完成生成：{generated} 个音频文件")

    if failed:
        print()
        print("以下音频生成失败：")

        for failure in failed:
            print(f"- {failure}")

        raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(main())
PY 

