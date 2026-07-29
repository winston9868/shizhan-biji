# 老田的 AI 实战笔记 · 静态知识库站点

一个零依赖、单文件自包含的静态站点，用于 WorkBuddy / 企业微信 实战经验的沉淀与分享。
配色沿用青绿 + 天蓝主题，结构对标「小饭的 AI 实战笔记」。

## 目录结构
```
site/
├── build_site.py   # 生成器：改这里的内容数据，重新跑即可重建全部页面
├── index.html      # 首页（Hero + 六大板块 + 最新文章筛选）
├── manual.html     # 使用手册（左目录树 + 正文 + 右 TOC 进度）
├── cases.html      # 案例篇
├── advanced.html   # 进阶篇
├── skills.html     # Skills 专栏（技能卡片）
├── community.html  # 交流（关于我 / 联系方式 / 反馈）
└── README.md       # 本文件
```

## 本地预览
直接双击 `index.html` 即可在浏览器打开。
或在目录下起一个本地服务（推荐，避免个别浏览器对 file:// 的限制）：
```bash
python -m http.server 8080
# 浏览器访问 http://localhost:8080
```

## 如何更新内容
所有内容都集中在 `build_site.py` 的数据区：
- `MANUAL` / `CASES` / `ADVANCED`：文档页的章节（id, 编号, 标题, 徽标, 正文 HTML）
- `HOME_ARTICLES`：首页「最新文章」卡片
- `SKILLS`：Skills 专栏卡片
- `SECTIONS` / `SITE_TITLE` 等：站点级配置

改完后重建：
```bash
python build_site.py
```
> 每个 HTML 都是自包含的（CSS/JS 内联），改样式就改 `build_site.py` 里的 `CSS` 常量，然后统一重建。

## 部署到 GitHub Pages（公网可访问）
1. 在 GitHub 新建一个仓库，例如 `workbuddy-notes`。
2. 把 `site/` 目录下所有文件推上去（建议直接放在仓库根目录，或放在 `docs/` 目录）。
3. 仓库 Settings → Pages → Source 选 `main` 分支、目录选 `/ (root)`（或 `/docs`）。
4. 等待约 1 分钟，访问 `https://<你的用户名>.github.io/workbuddy-notes/`。

> 因为是纯静态、零依赖，丢到任意静态托管（腾讯云静态网站、云开发、Vercel、CloudStudio）都行。

## 双备份提醒
交付 / 发布前，记得本地一份 + 乐享知识库一份。
