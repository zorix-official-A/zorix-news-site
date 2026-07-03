# Zorix News 多语言静态站点

## 发布新闻

编辑 `data/news.json`。页面会自动读取其中的 `news` 数组；数组为空时显示“暂无新闻”。

可参考 `data/news.example.json`。支持：

- 多语言 `title`、`summary`、`category`、`html`
- 纯文本 `content`
- 直接渲染本地 JSON 中的 `html`
- PNG、JPG、JPEG、WebP 图片
- 单张 `image` 或多张 `images`
- `published: false` 隐藏新闻
- 按 `publishedAt` 自动倒序排列

图片建议放进 `assets/news/`，JSON 路径写成 `assets/news/example.jpg`。

> 安全提醒：`html` 会直接插入页面，只应编辑并提交你自己信任的本地 JSON，不要把未经审核的用户输入写入该字段。

## GitHub Pages

把 `zorix-news-site` 内所有内容上传到仓库根目录并启用 GitHub Pages。请通过网页地址访问，不要直接用 `file://` 打开，因为浏览器会阻止本地 `fetch()` 读取 JSON。

## 地区与语言

GitHub Pages 无法直接读取 `CF-IPCountry`。根页面使用浏览器语言跳转；`functions/index.js` 可在 Cloudflare Pages 中使用地区头跳转。
