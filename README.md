# Zorix News

多语言静态新闻首页，可直接部署至 GitHub Pages。

## GitHub Pages

上传全部文件并将仓库根目录设为 Pages 来源。根页面通过浏览器语言自动跳转到 `/zh-CN/news/`、`/it/news/`、`/en/news/` 等路径。

## Cloudflare 地区头说明

GitHub Pages 无法读取 `CF-IPCountry` 请求头，因为纯静态浏览器 JavaScript无法访问该头。项目附带 `functions/index.js`，部署到 Cloudflare Pages 时可使用该函数按地区跳转。GitHub Pages 部署会自动忽略 `functions` 文件夹，并继续使用浏览器语言检测。

## 支持语言

简体中文、英语、意大利语、西班牙语、法语、德语、日语、韩语。
