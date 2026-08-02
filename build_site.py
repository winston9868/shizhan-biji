# -*- coding: utf-8 -*-
"""
生成「老田的 AI 实战笔记」静态知识库站点。
单文件自包含：每个 HTML 内联 CSS + JS，零外部依赖，可直接双击打开或部署 GitHub Pages。

分区策略（2026-07-29 调整）：
- 使用手册、案例篇 按产品分区：企业微信 / WorkBuddy 各一套（共 4 个页面）
- 进阶篇、Skills、交流 保持 WorkBuddy 相关，不分区
- 视觉双色标：企业微信绿 #07C160 / WorkBuddy 翡翠绿 #10B981（站点品牌仍用 ima 薄荷绿渐变）

运行：python build_site.py  -> 在当前目录生成 8 个 html + README.md
"""
import os, json

# ============================ 站点配置 ============================
SITE_TITLE = "老田的 AI 实战笔记"
SITE_DESC = "腾讯产品商务顾问的 WorkBuddy / 企业微信 实战沉淀与分享"
AUTHOR = "田伟"
CITY = "长沙"

# 产品色板
C_WECOM = "#07C160"   # 企业微信绿
C_WB    = "#10B981"   # WorkBuddy 翡翠绿
C_WECOM_SOFT = "rgba(7,192,96,.12)"
C_WB_SOFT    = "rgba(16,185,129,.12)"
C_INDUSTRY   = "#0EA5E9"  # 岗位与行业落地（天蓝）
C_TOOLS      = "#06B6D4"  # AI 工具评测（青）
C_LLM        = "#A855F7"  # 大模型横评（紫）
C_AGENT      = "#F59E0B"  # AI 案例（琥珀）

# 笔记类别（首页卡片与下拉菜单共用）
NOTEBOOK_SECTIONS = [
    ("WB手册",  "manual-wb.html",    "📘", C_WB,    "从 0 到 1，把 WorkBuddy 用起来"),
    ("WB案例",  "cases-wb.html",     "📂", C_WB,    "真实任务的完整复现"),
]

# AI 生态栏目（顶部导航下拉 + 首页文章系列卡片共用）
ECOSYSTEM_SECTIONS = [
    ("AI 工具评测", "ai-tools.html",       "🛠", C_TOOLS,    "6 款主流 AI 工具深度横评"),
    ("大模型横评",  "llm-compare.html",    "🧠", C_LLM,      "跑分、定价与选型指南"),
    ("行业落地拆解", "ai-industry.html",   "🏭", C_INDUSTRY, "AI 在 6 大行业怎么落地"),
    ("AI 案例",     "ai-agent-cases.html", "⚡", C_AGENT,    "自己跑通的真实项目复盘"),
]

# 顶部导航栏目（name, href, icon, 产品色, 产品分组, 下拉项）
# 下拉项格式：[(名称, 链接, 颜色), ...]，为 None 时是普通链接
SECTIONS = [
    ("首页",   "index.html",              "🏠", "",         "", None),
    ("新闻动态", "index.html#news",       "📰", C_WB,      "", None),
    ("笔记类别", "index.html#notebooks",  "📝", "#10B981",  "", None),
    ("AI生态专栏", "index.html#ecosystem", "🌐", C_TOOLS,   "", None),
    ("Skills", "skills.html",             "🧩", "#A855F7", "", None),
    ("交流",   "community.html",          "💬", "#64748B", "", None),
]

# ============================ 共享 CSS ============================
CSS = """
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --c-teal:#10B981; --c-blue:#06B6D4; --c-coral:#F59E0B; --c-purple:#A855F7;
  --c-wecom:#07C160;
  --accent:#10B981; --accent-soft:rgba(16,185,129,.12); --accent-grad:#10B981;
  --bg:#FAFAF9; --bg-card:#FFFFFF; --bg-soft:#F5F5F4;
  --bg-hero:linear-gradient(135deg,#F0FDFA 0%,#ECFEFF 30%,#F0F9FF 60%,#FDF4FF 100%);
  --text-primary:#292524; --text-secondary:#57534E; --text-tertiary:#A8A29E;
  --border:#E7E5E4; --border-hover:#99F6E4;
  --shadow-sm:0 1px 3px rgba(0,0,0,.04),0 1px 2px rgba(0,0,0,.03);
  --shadow-md:0 4px 16px rgba(0,0,0,.05),0 2px 8px rgba(0,0,0,.03);
  --shadow-lg:0 12px 40px rgba(16,185,129,.08),0 4px 16px rgba(0,0,0,.04);
  --shadow-hover:0 8px 28px rgba(16,185,129,.12),0 4px 12px rgba(0,0,0,.05);
  --sidebar-w:240px; --reading-w:760px; --topbar-h:56px;
  /* ===== 一页纸（A4）排版参数：210mm @96dpi = 794px ===== */
  --paper-w:794px;          /* 纸面宽度 */
  --paper-pad-x:102px;      /* 左右页边距（公文 28mm/26mm 等比折算） */
  --paper-bg:#EDEBE7;       /* 纸张外的桌面底色 */
  --doc-line:1.7;           /* 长文网页标准行距：中文正文舒适区 1.6~1.8，取 1.7 */
  --doc-ink:#1F1F1F;        /* 公文正文墨色 */
  /* ===== 公文字体族（缺字时按顺序回退） ===== */
  --font-fs:'Songti SC','SimSun','宋体','Source Han Serif SC','Noto Serif SC',serif;
  --font-hei:'Microsoft YaHei','PingFang SC','Heiti SC',SimHei,sans-serif;
  --font-kai:'Kaiti SC','KaiTi','楷体',STKaiti,serif;
  --font-xbs:'方正小标宋简体',FZXiaoBiaoSong-B05S,'Songti SC',SimSun,'宋体',serif;
  --font-serif:Georgia,'Noto Serif SC','Songti SC',serif;
  --font-sans:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;
  --font-mono:'JetBrains Mono','Fira Code',Consolas,monospace;
  --radius-sm:8px; --radius-md:12px; --radius-lg:16px; --radius-xl:20px;
}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--text-primary);font-family:var(--font-fs);
  font-size:14px;line-height:1.85;-webkit-font-smoothing:antialiased}
a{color:var(--c-teal);text-decoration:none;transition:color .2s}
a:hover{color:#047857}
img{max-width:100%;height:auto}

/* ===== 全站字体系统（2026-08-02 确立）：正文宋体 · 标题/导航/UI 控件黑体 · 大标题方正小标宋 ===== */
h1,h2,h3,h4,h5,h6{font-family:var(--font-hei);font-weight:600}
.topbar-nav a,.nav-dropdown-menu a,button,.btn,input,textarea,select,
  .badge,.badge-hot,.badge-cat,.chapter-badge,.news-tab,.tag,.pill,.chip,
  .search-input,.search-hint{font-family:var(--font-hei)}

/* ===== Top Nav ===== */
.topbar{position:fixed;top:0;left:0;right:0;height:var(--topbar-h);
  background:rgba(255,255,255,.85);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);
  border-bottom:1px solid var(--border);z-index:100;display:flex;align-items:center;padding:0 24px}
.topbar-inner{max-width:1320px;margin:0 auto;width:100%;display:flex;align-items:center;
  justify-content:space-between;gap:16px}
.blog-logo{display:flex;align-items:center;gap:8px;font-family:var(--font-xbs);font-size:16px;
  font-weight:500;color:var(--text-primary);text-decoration:none;white-space:nowrap}
.blog-logo:hover{color:var(--c-teal)}
.blog-logo-icon{width:30px;height:30px;background:linear-gradient(135deg,#4DEE9E,#D6E807);
  border-radius:var(--radius-sm);display:flex;align-items:center;justify-content:center;
  color:#fff;font-size:12px;font-weight:700;letter-spacing:.5px;font-family:var(--font-sans);
  box-shadow:0 2px 8px rgba(16,185,129,.3)}
.topbar-nav{display:flex;align-items:center;gap:2px;flex-wrap:wrap;justify-content:flex-end}
.topbar-nav a{padding:6px 11px;border-radius:var(--radius-xl);font-size:14px;font-weight:600;
  color:var(--text-secondary);text-decoration:none;transition:all .2s;display:inline-flex;align-items:center}
.topbar-nav a:hover{background:var(--bg-soft);color:var(--text-primary)}
.topbar-nav a.active{background:var(--accent-soft);color:var(--accent);font-weight:600}
.nav-dot{width:7px;height:7px;border-radius:50%;display:inline-block;margin-right:6px;flex-shrink:0}
.menu-btn{display:none;background:none;border:none;font-size:20px;cursor:pointer;color:var(--text-secondary)}

/* ===== Nav dropdown ===== */
.nav-dropdown{position:relative;display:inline-block}
.nav-dropdown>a .caret{font-size:10px;margin-left:3px;opacity:.7}
.nav-dropdown-menu{position:absolute;top:calc(100% + 6px);left:0;background:#fff;border:1px solid var(--border);border-radius:var(--radius-md);
  box-shadow:var(--shadow-md);min-width:170px;padding:6px 0;display:none;z-index:101}
.nav-dropdown:hover .nav-dropdown-menu,.nav-dropdown.open .nav-dropdown-menu{display:block}
.nav-dropdown-menu a{display:flex;align-items:center;padding:8px 14px;font-size:13px;color:var(--text-secondary);white-space:nowrap}
.nav-dropdown-menu a:hover{background:var(--bg-soft);color:var(--text-primary)}
.nav-dropdown-menu .nav-dot{width:7px;height:7px}
.nav-dropdown-menu a.active{background:var(--accent-soft);color:var(--accent);font-weight:600}
.nav-dropdown>a.active .caret{color:var(--accent)}

/* ===== Hero (home) ===== */
.hero{margin-top:var(--topbar-h);padding:72px 24px 56px;
  background:var(--bg-hero);border-bottom:1px solid var(--border);text-align:center}
.hero-name{font-family:var(--font-xbs);font-size:40px;font-weight:700;letter-spacing:.5px;
  background:linear-gradient(120deg,#047857,#10B981,#84CC16);-webkit-background-clip:text;
  background-clip:text;-webkit-text-fill-color:transparent}
.hero-tagline{margin:18px auto 0;max-width:620px;color:var(--text-secondary);font-size:16px;line-height:1.9}
.hero-tags{margin-top:26px;display:flex;flex-wrap:wrap;gap:10px;justify-content:center}
.hero-tag{padding:6px 16px;border-radius:var(--radius-xl);font-size:13px;font-weight:500;
  border:1px solid transparent}
.hero-tag.wecom{background:rgba(7,192,96,.12);color:#047857}
.hero-tag.teal{background:rgba(16,185,129,.12);color:#047857}
.hero-tag.blue{background:rgba(6,182,212,.14);color:#0E7490}
.hero-tag.coral{background:rgba(245,158,11,.14);color:#B45309}
.hero-tag.purple{background:rgba(168,85,247,.14);color:#7E22CE}

/* ===== Generic section ===== */
.section{max-width:1180px;margin:0 auto;padding:56px 24px}
.section-head{margin-bottom:28px}
.section-head h2{font-size:24px;font-weight:700;display:flex;align-items:center;gap:10px}
.section-head .bar{width:5px;height:22px;border-radius:3px;background:linear-gradient(180deg,#4DEE9E,#D6E807)}
.section-head .bar.wecom{background:linear-gradient(180deg,#34D399,#07C160)}
.section-head p{margin-top:8px;color:var(--text-tertiary);font-size:14px}
#notebooks{scroll-margin-top:calc(var(--topbar-h) + 24px)}

/* ===== Cards grid (home sections) ===== */
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px}
@media(min-width:1100px){.cards{grid-template-columns:repeat(4,1fr)}}
.card{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius-lg);
  padding:24px;box-shadow:var(--shadow-sm);transition:all .25s;position:relative;overflow:hidden}
.card:hover{transform:translateY(-4px);box-shadow:var(--shadow-hover);
  border-color:var(--border-hover)}
.card-ico{width:42px;height:42px;border-radius:var(--radius-md);display:flex;align-items:center;
  justify-content:center;font-size:20px;margin-bottom:0}
.card-header{display:flex;align-items:center;gap:12px;margin-bottom:14px}
.card h3{font-size:17px;font-weight:600;margin-bottom:0}
.card p{color:var(--text-secondary);font-size:13.5px;line-height:1.8;font-weight:700}
.card .meta{margin-top:14px;font-size:12px;color:var(--text-tertiary)}
.card .arrow{position:absolute;right:20px;bottom:18px;font-size:18px;color:var(--text-tertiary);
  transition:transform .25s,color .25s}
.card:hover .arrow{transform:translateX(4px);color:var(--c-teal)}

/* ===== Filter pills (home articles) ===== */
/* ===== Filter pills (home articles) · 青色柔和版（B 方案） ===== */
.filter-pills{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:24px}
.filter-pill{padding:7px 18px;border:1px solid var(--border);border-radius:var(--radius-xl);
  background:var(--bg-card);color:var(--text-secondary);font-size:13px;cursor:pointer;transition:all .2s}
.filter-pill:hover{border-color:#7DD3E8;color:#0891B2}
.filter-pill.active{background:#0891B2;color:#fff;border-color:transparent;font-weight:600}

/* ===== Article list · 图2 风格 / 青色柔和版（B 方案） ===== */
.article-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:16px}
.article-card{display:block;background:var(--bg-card);border:1px solid var(--border);
  border-left:4px solid #7DD3E8;border-radius:var(--radius-md);padding:18px 20px;
  box-shadow:var(--shadow-sm);transition:all .22s;text-decoration:none}
.article-card:hover{transform:translateY(-3px);box-shadow:var(--shadow-md);border-color:#7DD3E8;border-left-color:#0891B2;color:inherit}
.article-card-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px}
.article-cat{display:inline-block;font-size:11px;font-weight:600;padding:3px 10px;
  border-radius:var(--radius-xl);background:rgba(6,182,212,.12);color:#0891B2}
.article-cat.cat-case{background:rgba(168,85,247,.12);color:#9333EA}
.article-cat.cat-advanced{background:rgba(37,99,235,.12);color:#1D4ED8}
.article-cat.cat-industry{background:rgba(217,119,6,.12);color:#B45309}
.article-ch{font-size:12px;color:var(--text-tertiary);font-weight:500}
.article-card h4{font-size:15.5px;font-weight:700;color:var(--text-primary);margin:0 0 6px;line-height:1.45}
.article-card p{font-size:13px;color:var(--text-secondary);line-height:1.75;margin:0;
  display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}

/* ===== Doc layout (manual/cases/advanced/industry)：A4 一页纸 ===== */
body.doc-body{background:var(--paper-bg)}
.layout{max-width:calc(var(--sidebar-w) + var(--paper-w) + 82px);margin:0 auto;
  padding:calc(var(--topbar-h) + 28px) 24px 80px;justify-content:center;
  display:grid;grid-template-columns:var(--sidebar-w) minmax(0,var(--paper-w));gap:34px}
.sidebar{position:sticky;top:calc(var(--topbar-h) + 24px);align-self:start;max-height:calc(100vh - var(--topbar-h) - 48px);overflow-y:auto}
.sidebar-header{font-size:12px;font-weight:600;color:var(--text-tertiary);text-transform:uppercase;
  letter-spacing:1px;margin-bottom:12px;padding-left:6px}
.sidebar-back{display:inline-flex;align-items:center;gap:6px;font-size:13px;color:var(--text-secondary);margin-bottom:14px}
.sidebar-part{margin-bottom:3px}
.sidebar-part-header{display:flex;align-items:center;gap:9px;padding:9px 10px;border-radius:var(--radius-sm);
  cursor:pointer;transition:background .2s;user-select:none}
.sidebar-part-header:hover{background:var(--bg-soft)}
.sidebar-part-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}
.sidebar-part-name{font-size:14px;font-weight:500;color:var(--text-primary);flex:1}
.sidebar-part-chevron{transition:transform .25s;color:var(--text-tertiary)}
.sidebar-part.expanded .sidebar-part-chevron{transform:rotate(90deg)}
.sidebar-chapters{max-height:0;overflow:hidden;transition:max-height .3s ease}
.sidebar-part.expanded .sidebar-chapters{max-height:1000px}
.sidebar-chapter{display:block;padding:6px 10px 6px 27px;font-size:13px;color:var(--text-secondary);
  border-radius:var(--radius-sm);transition:all .18s;border-left:2px solid transparent;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:calc(var(--sidebar-w) - 20px)}
.sidebar-chapter:hover{background:rgba(16,185,129,.10);color:var(--text-primary)}
.sidebar-chapter.active{color:#059669;border-left-color:var(--accent);background:rgba(16,185,129,.15);font-weight:600}

.reading-section{min-width:0}
/* 纸面：白纸 + 投影，宽度 = A4，左右按公文页边距留白 */
.reading-page{background:#fff;border:1px solid rgba(0,0,0,.07);border-radius:3px;
  padding:56px var(--paper-pad-x) 68px;
  box-shadow:0 1px 2px rgba(0,0,0,.05),0 10px 32px rgba(0,0,0,.07)}
/* 文档大标题：方正小标宋 · 居中（对应 Word 二号标题） */
.reading-page>.page-title{font-family:var(--font-xbs);font-size:26px;font-weight:400;
  color:var(--doc-ink);text-align:center;letter-spacing:1px;margin-bottom:10px;line-height:1.5}
.reading-page>.page-sub{font-family:var(--font-kai);color:var(--text-secondary);font-size:15px;
  text-align:center;margin-bottom:30px;padding-bottom:22px;border-bottom:1px solid var(--border)}
.chapter{scroll-margin-top:calc(var(--topbar-h) + 24px);margin-bottom:42px}
.chapter-header{display:flex;align-items:center;gap:12px;margin-bottom:18px}
.chapter-badge{font-size:12px;font-weight:600;padding:3px 11px;border-radius:var(--radius-xl);
  background:var(--accent-soft);color:var(--accent);white-space:nowrap}
.chapter-title{font-family:var(--font-hei);font-size:21px;font-weight:400;color:var(--doc-ink)}
.chapter:not(:last-child){border-bottom:1px solid var(--border);padding-bottom:36px;margin-bottom:36px}
/* ===== 正文：宋体（屏幕衬线）· 网页标准行距 CSS 1.7 · 首行缩进 2 字符 · 两端对齐 · 段间 0.8em 自然间距 ===== */
.chapter-body{font-family:var(--font-fs);color:var(--doc-ink);font-size:16.5px;
  line-height:var(--doc-line);text-align:justify}
.chapter-body p{margin:0 0 0.8em;color:var(--doc-ink);text-indent:2em}
.chapter-body p:has(> img),.chapter-body p:has(> .img-missing){text-indent:0}
.chapter-body ul,.chapter-body ol{margin:12px 0;padding-left:2.4em;color:var(--doc-ink)}
.chapter-body li{margin:5px 0;text-indent:0}
.chapter-body li p{text-indent:0;margin:4px 0}
.chapter-body strong,.chapter-body b{font-family:var(--font-hei);font-weight:600;color:#000}
/* 标题分级：一级黑体（对应「一、」）· 二级楷体不加粗（对应「（一）」）· 三级宋体加粗 */
.chapter-body h3{font-family:var(--font-kai);font-size:19px;font-weight:400;
  color:var(--doc-ink);margin:24px 0 10px;text-indent:0}
.chapter-body h4{font-family:var(--font-fs);font-size:16.5px;font-weight:700;
  color:var(--doc-ink);margin:20px 0 8px;text-indent:0}
.chapter-body :not(pre) > code{font-family:var(--font-mono);font-size:13px;background:var(--bg-soft);
  padding:2px 6px;border-radius:5px;color:#047857}
.callout{margin:16px 0;padding:14px 16px;border-radius:var(--radius-md);font-size:14px;line-height:1.8;
  border-left:4px solid var(--c-teal);background:rgba(16,185,129,.07);
  font-family:var(--font-sans);color:var(--text-secondary);text-indent:0;text-align:left}
.callout p,.callout li{text-indent:0;color:inherit;font-family:inherit}
.callout.warn{border-left-color:var(--c-coral);background:rgba(245,158,11,.08)}
.callout.info{border-left-color:var(--c-blue);background:rgba(6,182,212,.08)}
.callout .ttl{font-weight:600;display:block;margin-bottom:4px}
.callout.key{border-left:4px solid var(--c-teal);background:linear-gradient(90deg,rgba(16,185,129,.16),rgba(16,185,129,.04));
  padding:16px 18px;font-weight:500}
.callout.key .ttl{color:#047857;margin-bottom:6px}
.callout.key p{margin:0}
pre{margin:16px 0;background:#1E293B;color:#E2E8F0;border:1px solid var(--border);border-radius:var(--radius-md);padding:16px 18px;
  overflow-x:auto;font-size:13px;line-height:1.7}
pre code{font-family:var(--font-mono);color:inherit;background:none;padding:0}
table{width:100%;border-collapse:collapse;margin:18px 0;font-size:13.5px}
th,td{border:1px solid var(--border);padding:10px 12px;text-align:left}
th{background:var(--bg-soft);font-weight:600;color:var(--text-primary)}
td{color:var(--text-secondary)}
.chapter-body h2{font-family:var(--font-hei);font-size:21px;font-weight:400;margin:28px 0 12px;
  padding-bottom:8px;border-bottom:1px solid var(--border);color:var(--doc-ink);text-indent:0}
/* ===== 公文表格：黑体表头 + 浅蓝底 #D9E2F3 + 细黑边框 · 无斑马纹 ===== */
.chapter-body table{width:100%;border-collapse:collapse;margin:18px 0;font-size:15px;
  font-family:var(--font-fs);text-indent:0}
.chapter-body th{background:#D9E2F3;font-family:var(--font-hei);font-weight:400;color:#000;
  border:1px solid #4A4A4A;padding:9px 12px;text-align:left}
.chapter-body td{background:transparent;color:var(--doc-ink);border:1px solid #4A4A4A;
  padding:9px 12px;text-align:left}
/* 代码 / 预格式块内不参与首行缩进 */
.chapter-body pre,.chapter-body code,.chapter-body figure{text-indent:0;text-align:left}
.chapter-body img{max-width:100%;height:auto;display:block;margin:16px auto;
  border-radius:var(--radius-md);border:1px solid var(--border);background:var(--bg-soft)}
.chapter-body figure{margin:16px 0;padding:12px 14px;border:1px solid var(--border);
  border-radius:var(--radius-md);background:var(--bg-soft)}
.chapter-body figure pre{margin:0}
.img-missing{margin:16px auto;padding:18px;text-align:center;font-size:13px;color:var(--text-tertiary);
  border:1px dashed var(--border);border-radius:var(--radius-md);background:var(--bg-soft)}




/* ===== Skills page ===== */
.skill-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:20px}
.skill-card{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius-lg);
  padding:22px;box-shadow:var(--shadow-sm);transition:all .25s;display:flex;flex-direction:column}
.skill-card:hover{transform:translateY(-4px);box-shadow:var(--shadow-lg);border-color:var(--border-hover)}
.skill-top{display:flex;align-items:center;gap:12px;margin-bottom:12px}
.skill-ava{width:44px;height:44px;border-radius:var(--radius-md);display:flex;align-items:center;
  justify-content:center;font-size:22px;background:rgba(16,185,129,.08);color:var(--c-teal);flex-shrink:0}
.skill-card h3{font-size:16px;font-weight:600}
.skill-card .ver{font-size:11px;color:var(--text-tertiary);margin-top:2px}
.skill-card p{color:var(--text-secondary);font-size:13px;line-height:1.8;flex:1}
.skill-tags{margin-top:14px;display:flex;flex-wrap:wrap;gap:6px}
.skill-tags span{font-size:11px;padding:3px 10px;border-radius:var(--radius-xl);
  background:var(--bg-soft);color:var(--text-secondary)}
.skill-meta{margin-top:14px;padding-top:12px;border-top:1px solid var(--border);
  font-size:12px;color:var(--text-tertiary);display:flex;justify-content:space-between}

/* ===== Community page ===== */
.cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px}
.info-card{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius-lg);
  padding:24px;box-shadow:var(--shadow-sm)}
.info-card .ic-ico{width:42px;height:42px;border-radius:var(--radius-md);display:flex;align-items:center;
  justify-content:center;font-size:20px;background:var(--accent-soft);margin-bottom:12px}
.info-card h3{font-size:16px;font-weight:600;margin-bottom:8px}
.info-card p,.info-card li{color:var(--text-secondary);font-size:13.5px;line-height:1.85}
.info-card ul{padding-left:20px;margin-top:8px}
.info-card a{font-weight:500}
.profile{display:flex;gap:24px;align-items:center;background:var(--bg-card);border:1px solid var(--border);
  border-radius:var(--radius-lg);padding:28px;box-shadow:var(--shadow-sm);margin-bottom:28px;flex-wrap:wrap}
.profile .ava{width:84px;height:84px;border-radius:50%;background:rgba(16,185,129,.08);
  display:flex;align-items:center;justify-content:center;color:var(--c-teal);font-size:30px;font-weight:600;flex-shrink:0}
.profile .pinfo h2{font-size:22px;font-weight:700}
.profile .pinfo .role{color:var(--c-teal);font-weight:500;margin:4px 0}
.profile .pinfo p{color:var(--text-secondary);font-size:13.5px;margin-top:6px;max-width:560px}

/* ===== Footer ===== */
.footer{margin-top:40px;border-top:1px solid var(--border);background:var(--bg-card)}
.footer-inner{max-width:1180px;margin:0 auto;padding:32px 24px;display:flex;justify-content:space-between;
  align-items:center;flex-wrap:wrap;gap:14px;color:var(--text-tertiary);font-size:13px}
.footer a{color:var(--text-secondary)}
.footer .links{display:flex;gap:14px;flex-wrap:wrap}

/* ===== Back to top ===== */
#backTop{position:fixed;right:26px;bottom:26px;width:44px;height:44px;border-radius:50%;
  background:linear-gradient(135deg,#4DEE9E,#D6E807);color:#fff;border:none;cursor:pointer;font-size:18px;
  box-shadow:0 6px 20px rgba(20,184,166,.35);opacity:0;pointer-events:none;transition:opacity .3s;z-index:90}
#backTop.show{opacity:1;pointer-events:auto}

/* ===== Skills page v2 ===== */
.skills-hero{margin-top:var(--topbar-h);padding:80px 24px 60px;text-align:center;
  background:linear-gradient(135deg,#F0F9FF 0%,#FDF2F8 50%,#F5F3FF 100%);border-bottom:1px solid var(--border)}
.skills-hero h1{font-family:var(--font-xbs);font-size:40px;font-weight:700;
  background:linear-gradient(120deg,#0EA5E9,#8B5CF6,#EC4899);-webkit-background-clip:text;
  background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:.5px}
.skills-hero p{max-width:640px;margin:18px auto 0;color:var(--text-secondary);font-size:15px;line-height:1.9}
.skill-cats{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin-bottom:32px}
.skill-cat{padding:7px 16px;border:1px solid var(--border);border-radius:var(--radius-xl);
  background:var(--bg-card);color:var(--text-secondary);font-size:13px;cursor:pointer;transition:all .2s}
.skill-cat:hover{border-color:var(--border-hover);color:var(--c-teal)}
.skill-cat.active{background:linear-gradient(120deg,#10B981,#06B6D4);color:#fff;border-color:transparent;font-weight:600}
.skill-grid-v2{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px}
.skill-card-v2{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius-lg);
  padding:22px;box-shadow:var(--shadow-sm);transition:all .25s;cursor:pointer;position:relative}
.skill-card-v2:hover{transform:translateY(-4px);box-shadow:var(--shadow-hover);border-color:var(--border-hover)}
.skill-card-v2.hidden{display:none}
.skill-card-v2 .top{display:flex;align-items:flex-start;gap:14px;margin-bottom:14px}
.skill-card-v2 .ava{width:52px;height:52px;border-radius:var(--radius-md);display:flex;align-items:center;
  justify-content:center;font-size:26px;background:rgba(16,185,129,.08);color:var(--c-teal);flex-shrink:0}
.skill-card-v2 .tit{flex:1}
.skill-card-v2 h3{font-size:16px;font-weight:600;margin-bottom:4px}
.skill-card-v2 .badges{display:flex;gap:6px;flex-wrap:wrap}
.skill-card-v2 .badge-hot{font-size:10px;padding:2px 8px;border-radius:var(--radius-xl);
  background:linear-gradient(120deg,#F59E0B,#EF4444);color:#fff;font-weight:600}
.skill-card-v2 .badge-cat{font-size:10px;padding:2px 8px;border-radius:var(--radius-xl);
  background:var(--bg-soft);color:var(--text-tertiary)}
.skill-card-v2 .desc{color:var(--text-secondary);font-size:13px;line-height:1.8;margin-bottom:16px;
  display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.skill-card-v2 .foot{display:flex;align-items:center;justify-content:space-between;font-size:12px;color:var(--text-tertiary)}
.skill-card-v2 .foot .more{color:var(--c-teal);font-weight:500}

/* Skill detail modal */
.skill-modal{position:fixed;inset:0;background:rgba(0,0,0,.45);z-index:200;display:none;
  align-items:center;justify-content:center;padding:24px;backdrop-filter:blur(4px)}
.skill-modal.show{display:flex}
.skill-modal-box{background:var(--bg-card);border-radius:var(--radius-lg);width:100%;max-width:760px;
  max-height:calc(100vh - 48px);overflow-y:auto;box-shadow:0 24px 80px rgba(0,0,0,.2);position:relative}
.skill-modal-close{position:absolute;top:16px;right:16px;width:36px;height:36px;border-radius:50%;
  border:none;background:var(--bg-soft);color:var(--text-secondary);font-size:20px;cursor:pointer;transition:all .2s}
.skill-modal-close:hover{background:var(--border);color:var(--text-primary)}
.skill-modal-head{padding:28px 32px 22px;border-bottom:1px solid var(--border);display:flex;gap:18px;align-items:flex-start}
.skill-modal-head .ava{width:64px;height:64px;border-radius:var(--radius-md);display:flex;align-items:center;
  justify-content:center;font-size:32px;background:rgba(16,185,129,.08);color:var(--c-teal);flex-shrink:0}
.skill-modal-head .tit h2{font-size:22px;font-weight:700;margin-bottom:8px}
.skill-modal-head .badges{display:flex;gap:6px;flex-wrap:wrap}
.skill-modal-body{padding:28px 32px 32px}
.skill-modal-sec{margin-bottom:26px}
.skill-modal-sec:last-child{margin-bottom:0}
.skill-modal-sec .sec-title{display:flex;align-items:center;gap:8px;font-size:15px;font-weight:600;
  color:var(--c-teal);margin-bottom:12px}
.skill-modal-sec .sec-ico{width:20px;height:20px;display:flex;align-items:center;justify-content:center;
  font-size:14px;color:#fff;background:var(--c-teal);border-radius:50%}
.skill-modal-sec p,.skill-modal-sec li{color:var(--text-secondary);font-size:13.5px;line-height:1.85}
.skill-modal-sec ol{padding-left:20px}
.skill-modal-sec ol li{margin:8px 0}
.skill-modal-sec .example{background:var(--bg-soft);border-left:4px solid var(--c-teal);border-radius:var(--radius-md);
  padding:14px 16px;font-size:13.5px;line-height:1.85;color:var(--text-secondary)}
.skill-modal-sec .scenarios{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:10px}
.skill-modal-sec .scenario{background:var(--bg-soft);border-radius:var(--radius-md);padding:12px 14px;
  font-size:13px;line-height:1.7;color:var(--text-secondary);border-left:3px solid var(--c-purple)}

/* ===== AI 提示词社区（参照 simouxuan.com 的 AI 提示词社区模块） ===== */
.prompt-hero{margin:72px auto 8px;max-width:760px;text-align:center;padding:0 24px}
.prompt-hero h2{font-family:var(--font-xbs);font-size:30px;font-weight:700;letter-spacing:.5px;
  background:linear-gradient(120deg,#047857,#10B981,#06B6D4);-webkit-background-clip:text;
  background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:12px}
.prompt-hero p{color:var(--text-secondary);font-size:15px;line-height:1.9}
.prompt-search{margin:24px auto 0;max-width:560px;position:relative}
.prompt-search input{width:100%;padding:12px 16px 12px 42px;border:1.5px solid var(--border);
  border-radius:var(--radius-xl);background:var(--bg-card);color:var(--text-primary);
  font-size:14px;outline:none;transition:border-color .2s,box-shadow .2s;box-sizing:border-box}
.prompt-search input::placeholder{color:var(--text-muted)}
.prompt-search input:focus{border-color:var(--c-teal);box-shadow:0 0 0 3px rgba(16,185,129,.15)}
.prompt-search .search-icon{position:absolute;left:15px;top:50%;transform:translateY(-50%);
  color:var(--text-muted);font-size:16px;pointer-events:none}
.prompt-cats{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin:28px 0 32px}
.prompt-cat{padding:7px 16px;border:1px solid var(--border);border-radius:var(--radius-xl);
  background:var(--bg-card);color:var(--text-secondary);font-size:13px;cursor:pointer;transition:all .2s}
.prompt-cat:hover{border-color:var(--border-hover);color:var(--c-teal)}
.prompt-cat.active{background:linear-gradient(120deg,#10B981,#06B6D4);color:#fff;border-color:transparent;font-weight:600}
.prompt-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px}
.prompt-card{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius-lg);
  padding:22px;box-shadow:var(--shadow-sm);transition:all .25s;cursor:pointer;position:relative}
.prompt-card:hover{transform:translateY(-4px);box-shadow:var(--shadow-hover);border-color:var(--border-hover)}
.prompt-card.hidden{display:none}
.prompt-card .top{display:flex;align-items:flex-start;gap:14px;margin-bottom:12px}
.prompt-card .ava{width:52px;height:52px;border-radius:var(--radius-md);display:flex;align-items:center;
  justify-content:center;font-size:26px;background:rgba(16,185,129,.08);color:var(--c-teal);flex-shrink:0}
.prompt-card .tit{flex:1}
.prompt-card h3{font-size:16px;font-weight:600;margin-bottom:4px}
.prompt-card .badges{display:flex;gap:6px;flex-wrap:wrap}
.prompt-card .badge-cat{font-size:10px;padding:2px 8px;border-radius:var(--radius-xl);
  background:var(--bg-soft);color:var(--text-tertiary)}
.prompt-card .desc{color:var(--text-secondary);font-size:13px;line-height:1.8;margin-bottom:12px;
  display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.prompt-card .ex{font-size:12px;color:var(--text-tertiary);background:var(--bg-soft);
  border-radius:var(--radius-md);padding:10px 12px;line-height:1.7;margin-bottom:12px;
  display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.prompt-card .foot{display:flex;align-items:center;justify-content:space-between;font-size:12px;color:var(--text-tertiary)}
.prompt-card .foot .views{color:var(--c-teal);font-weight:500}

/* Prompt detail modal */
.prompt-modal{position:fixed;inset:0;background:rgba(0,0,0,.45);z-index:200;display:none;
  align-items:center;justify-content:center;padding:24px;backdrop-filter:blur(4px)}
.prompt-modal.show{display:flex}
.prompt-modal-box{background:var(--bg-card);border-radius:var(--radius-lg);width:100%;max-width:760px;
  max-height:calc(100vh - 48px);overflow-y:auto;box-shadow:0 24px 80px rgba(0,0,0,.2);position:relative}
.prompt-modal-close{position:absolute;top:16px;right:16px;width:36px;height:36px;border-radius:50%;
  border:none;background:var(--bg-soft);color:var(--text-secondary);font-size:20px;cursor:pointer;transition:all .2s}
.prompt-modal-close:hover{background:var(--border);color:var(--text-primary)}
.prompt-modal-head{padding:28px 32px 22px;border-bottom:1px solid var(--border);display:flex;gap:18px;align-items:flex-start}
.prompt-modal-head .ava{width:64px;height:64px;border-radius:var(--radius-md);display:flex;align-items:center;
  justify-content:center;font-size:32px;background:rgba(16,185,129,.08);color:var(--c-teal);flex-shrink:0}
.prompt-modal-head .tit h2{font-size:22px;font-weight:700;margin-bottom:8px}
.prompt-modal-head .badges{display:flex;gap:6px;flex-wrap:wrap}
.prompt-modal-body{padding:28px 32px 32px}
.prompt-modal-sec{margin-bottom:26px}
.prompt-modal-sec:last-child{margin-bottom:0}
.prompt-modal-sec .sec-title{display:flex;align-items:center;gap:8px;font-size:15px;font-weight:600;
  color:var(--c-teal);margin-bottom:12px}
.prompt-modal-sec .sec-ico{width:20px;height:20px;display:flex;align-items:center;justify-content:center;
  font-size:14px;color:#fff;background:var(--c-teal);border-radius:50%}
.prompt-modal-sec p,.prompt-modal-sec li{color:var(--text-secondary);font-size:13.5px;line-height:1.85}
.prompt-modal-sec .example{background:var(--bg-soft);border-left:4px solid var(--c-teal);border-radius:var(--radius-md);
  padding:14px 16px;font-size:13.5px;line-height:1.85;color:var(--text-secondary)}
.prompt-box{background:#0F172A;border-radius:var(--radius-md);padding:18px 20px;position:relative}
.prompt-box pre{color:#E2E8F0;font-family:var(--font-mono);font-size:12.5px;line-height:1.8;
  white-space:pre-wrap;word-break:break-word;margin:0;padding-right:96px}
.copy-btn{position:absolute;top:14px;right:14px;background:linear-gradient(120deg,#10B981,#06B6D4);
  color:#fff;border:none;border-radius:var(--radius-xl);padding:7px 16px;font-size:12px;font-weight:600;cursor:pointer;transition:all .2s}
.copy-btn:hover{opacity:.9}
.copy-btn.copied{background:#047857}

/* ===== Responsive ===== */
@media(max-width:1100px){.layout{grid-template-columns:var(--sidebar-w) minmax(0,1fr)}
  }
@media(max-width:768px){.topbar-nav{display:none}.menu-btn{display:block}
  .layout{grid-template-columns:1fr;padding-left:16px;padding-right:16px}
  .sidebar{position:static;max-height:none;display:none}
  .sidebar.open{display:block}
  .reading-page{padding:24px 18px}
  .hero-name{font-size:30px}.section{padding:40px 16px}}
  .news-grid,.eco-grid,.case-grid{grid-template-columns:1fr}}

/* ===== 打印 / 导出 PDF：按公文页面设置输出（Ctrl+P 即得规整 PDF） ===== */
@page{size:A4;margin:37mm 26mm 35mm 28mm}
@media print{
  body,body.doc-body{background:#fff!important}
  .topbar,.sidebar,.footer,.menu-btn,.chapter-end,.reading-progress,
  .search-box,.nav-dropdown-menu,.sidebar-back{display:none!important}
  .layout{display:block!important;max-width:none!important;margin:0!important;padding:0!important}
  .reading-page{background:#fff!important;border:none!important;border-radius:0!important;
    box-shadow:none!important;padding:0!important}
  .reading-header{margin:0 0 16pt!important}
  .chapter-body{font-size:14pt;line-height:1.5;color:#000}
  .chapter-body p{orphans:3;widows:3}
  .chapter{border:none!important;margin:0 0 12pt!important;padding:0!important}
  .chapter-title,.chapter-body h2,.chapter-body h3,.chapter-body h4{
    break-after:avoid;page-break-after:avoid}
  .chapter-body img,.chapter-body table,.chapter-body pre,.chapter-body figure,.callout{
    break-inside:avoid;page-break-inside:avoid}
  .chapter-body img{border:none!important;box-shadow:none!important;background:none!important}
  /* 深色代码块打印会吃墨，改浅底黑字 */
  pre{background:#F5F5F5!important;color:#000!important;border:1px solid #999!important}
  pre code{color:#000!important}
  .callout{background:#F5F5F5!important;border-left:3pt solid #666!important;color:#000!important}
  .chapter-badge{background:none!important;color:#000!important;border:1px solid #999;font-weight:400}
  a{color:#000!important;text-decoration:none}
}

/* ===== Homepage: news hotspot (4 sub-category tabs) ===== */
.news-section{background:var(--bg-card)}
/* ===== Homepage: global search ===== */
.search-section{padding:32px 24px 24px;background:transparent;text-align:center}
.search-box{position:relative;max-width:680px;margin:0 auto}
.search-input{width:100%;padding:14px 48px 14px 48px;font-size:15px;font-family:var(--font-sans);
  background:var(--bg-card);border:1.5px solid var(--border);border-radius:var(--radius-xl);
  box-shadow:var(--shadow-sm);transition:all .2s;color:var(--text-primary)}
.search-input:focus{outline:none;border-color:var(--c-teal);box-shadow:0 0 0 4px var(--accent-soft)}
.search-icon{position:absolute;left:18px;top:50%;transform:translateY(-50%);color:var(--text-tertiary);font-size:18px;pointer-events:none}
.search-clear{position:absolute;right:14px;top:50%;transform:translateY(-50%);
  width:24px;height:24px;border:none;border-radius:50%;background:var(--bg-soft);
  color:var(--text-secondary);cursor:pointer;display:none;align-items:center;justify-content:center;font-size:14px}
.search-clear.show{display:flex}
.search-results{position:absolute;top:calc(100% + 8px);left:0;right:0;max-height:440px;overflow-y:auto;
  background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius-lg);
  box-shadow:var(--shadow-lg);z-index:50;display:none;text-align:left}
.search-results.show{display:block}
.search-result{padding:12px 16px;border-bottom:1px solid var(--border);cursor:pointer;
  display:flex;gap:12px;align-items:flex-start;transition:background .15s}
.search-result:last-child{border-bottom:none}
.search-result:hover,.search-result.focused{background:var(--bg-soft)}
.search-result-ico{width:32px;height:32px;border-radius:8px;display:flex;align-items:center;
  justify-content:center;font-size:16px;flex-shrink:0;background:var(--accent-soft);color:var(--c-teal)}
.search-result-body{flex:1;min-width:0}
.search-result-title{font-size:14px;font-weight:600;color:var(--text-primary);margin-bottom:2px;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.search-result-title mark{background:rgba(16,185,129,.2);color:var(--text-primary);padding:0 2px;border-radius:3px}
.search-result-snippet{font-size:12px;color:var(--text-tertiary);
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;line-height:1.5}
.search-result-snippet mark{background:rgba(16,185,129,.18);color:var(--text-secondary);padding:0 2px;border-radius:3px}
.search-result-cat{display:inline-block;font-size:11px;padding:2px 8px;border-radius:var(--radius-xl);
  background:var(--bg-soft);color:var(--text-secondary);margin-right:6px;vertical-align:middle}
.search-empty{padding:24px;text-align:center;color:var(--text-tertiary);font-size:13px}
.search-hint{margin-top:14px;color:var(--text-tertiary);font-size:12px}
.search-hint kbd{font-family:var(--font-mono);background:var(--bg-card);border:1px solid var(--border);
  border-radius:4px;padding:1px 6px;font-size:11px;margin:0 2px}
.news-tabs{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:24px}
.news-tab{padding:8px 18px;border:1px solid var(--border);border-radius:var(--radius-xl);
  background:var(--bg-card);color:var(--text-secondary);font-size:14px;font-weight:600;cursor:pointer;transition:all .2s}
.news-tab:hover{border-color:var(--tc);color:var(--tc)}
.news-tab.active{background:var(--tc);color:#fff;border-color:transparent}
.news-panel{display:none}
.news-panel.active{display:block;animation:fade .3s ease}
@keyframes fade{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.news-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.news-card{background:var(--bg-soft);border:1px solid var(--border);border-radius:var(--radius-lg);padding:20px;
  text-decoration:none;color:inherit;display:flex;flex-direction:column;gap:10px;transition:all .2s}
.news-card:hover{transform:translateY(-3px);box-shadow:var(--shadow-hover);border-color:var(--border-hover)}
.news-tag{font-size:11px;font-weight:600;padding:3px 10px;border-radius:var(--radius-xl);align-self:flex-start}
.news-card h4{font-size:15px;font-weight:600;line-height:1.5}
.news-card p{font-size:13px;color:var(--text-secondary);line-height:1.7;flex:1}
.news-go{font-size:12px;color:var(--tc);font-weight:600}

/* ===== Homepage: AI ecosystem showcase ===== */
.eco-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:18px}
.eco-card{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius-lg);padding:24px;
  text-decoration:none;color:inherit;position:relative;transition:all .25s;overflow:hidden}
.eco-card:hover{transform:translateY(-4px);box-shadow:var(--shadow-hover);border-color:var(--ec)}
.eco-card::before{content:"";position:absolute;top:0;left:0;right:0;height:3px;background:var(--ec)}
.eco-ico{width:48px;height:48px;border-radius:var(--radius-md);display:flex;align-items:center;justify-content:center;
  font-size:24px;margin-bottom:14px}
.eco-card h4{font-size:17px;font-weight:600;margin-bottom:8px}
.eco-card p{font-size:13px;color:var(--text-secondary);line-height:1.7}
.eco-card .arrow{position:absolute;right:22px;bottom:22px;color:var(--ec);font-weight:700;font-size:18px}

/* ===== Homepage: case showcase ===== */
.case-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:18px}
.case-card{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius-lg);padding:24px;
  text-decoration:none;color:inherit;position:relative;transition:all .25s}
.case-card:hover{transform:translateY(-4px);box-shadow:var(--shadow-hover);border-color:var(--cc)}
.case-ico{width:48px;height:48px;border-radius:var(--radius-md);display:flex;align-items:center;justify-content:center;
  font-size:24px;margin-bottom:14px}
.case-card h4{font-size:17px;font-weight:600;margin-bottom:8px}
.case-card p{font-size:13px;color:var(--text-secondary);line-height:1.7;margin-bottom:10px}
.case-card .meta{font-size:12px;color:var(--text-tertiary);margin-bottom:6px}
.case-card .arrow{color:var(--cc);font-weight:700;font-size:18px}

/* ===== Ecosystem detail page ===== */
.eco-hero{margin-top:var(--topbar-h);padding:64px 24px 52px;text-align:center;border-bottom:1px solid var(--border)}
.eco-hero .eco-badge{display:inline-flex;align-items:center;gap:8px;font-size:13px;font-weight:600;
  padding:6px 16px;border-radius:var(--radius-xl);margin-bottom:18px}
.eco-hero h1{font-family:var(--font-xbs);font-size:38px;font-weight:700;letter-spacing:.5px}
.eco-hero p{max-width:680px;margin:18px auto 0;color:var(--text-secondary);font-size:15px;line-height:1.9}
.eco-layout{max-width:1100px;margin:0 auto;padding:40px 24px 80px;display:grid;
  grid-template-columns:200px minmax(0,1fr);gap:40px;align-items:start}
.eco-toc{position:sticky;top:calc(var(--topbar-h) + 20px);display:flex;flex-direction:column;gap:4px}
.eco-toc a{font-size:13px;color:var(--text-secondary);text-decoration:none;padding:8px 12px;border-radius:8px;
  border-left:3px solid transparent;transition:all .2s}
.eco-toc a:hover{background:var(--bg-soft);color:var(--text-primary)}
.eco-toc a.active{color:var(--accent);border-left-color:var(--accent);background:var(--accent-soft);font-weight:600}
.eco-main{min-width:0}
.eco-section{margin-bottom:48px;scroll-margin-top:calc(var(--topbar-h) + 20px)}
.eco-section-head{display:flex;align-items:center;gap:12px;margin-bottom:8px}
.eco-section-head .si{font-size:22px}
.eco-section-head h2{font-size:24px;font-weight:700}
.eco-section .intro{color:var(--text-secondary);font-size:14px;line-height:1.8;margin:6px 0 18px}
.eco-subgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px}
.eco-subcard{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius-lg);padding:18px}
.eco-subhead{display:flex;align-items:center;justify-content:space-between;margin-bottom:8px}
.eco-subhead h4{font-size:15px;font-weight:600}
.eco-tag{font-size:11px;padding:2px 10px;border-radius:var(--radius-xl);background:var(--bg-soft);color:var(--text-tertiary)}
.eco-subcard p{font-size:13px;color:var(--text-secondary);line-height:1.7;margin-bottom:12px}
.pc{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.pc-col.pro{background:rgba(16,185,129,.06)}
.pc-col.con{background:rgba(239,68,68,.06)}
.pc-col{border-radius:10px;padding:10px 12px}
.pc-h{font-size:12px;font-weight:600;display:block;margin-bottom:6px}
.pc-col.pro .pc-h{color:var(--c-teal)}
.pc-col.con .pc-h{color:#EF4444}
.pc-col ul{margin:0;padding-left:18px}
.pc-col li{font-size:12px;color:var(--text-secondary);line-height:1.7}
.cmp{width:100%;border-collapse:collapse;font-size:13px;margin:8px 0;background:var(--bg-card);
  border:1px solid var(--border);border-radius:var(--radius-lg);overflow:hidden}
.cmp th,.cmp td{padding:10px 14px;text-align:left;border-bottom:1px solid var(--border)}
.cmp th{background:var(--bg-soft);font-weight:600;color:var(--text-primary)}
.cmp tr:last-child td{border-bottom:none}
.cmp tbody tr:hover{background:var(--bg-soft)}
.eco-conclusion{background:var(--bg-card);border:1px solid var(--border);border-left:4px solid var(--accent);
  border-radius:var(--radius-lg);padding:22px 26px}
.eco-conclusion h3{font-size:18px;font-weight:700;margin-bottom:10px}
.eco-conclusion p,.eco-conclusion div{font-size:14px;color:var(--text-secondary);line-height:1.9}
.eco-todo{background:rgba(245,158,11,.08);border:1px dashed #F59E0B;border-radius:10px;padding:14px 16px;
  font-size:13px;color:#B45309;line-height:1.7}
.eco-cta{text-align:center;margin-top:40px;padding:32px;background:var(--bg-soft);border-radius:var(--radius-lg)}
.eco-cta h3{font-size:20px;font-weight:700;margin-bottom:10px}
.eco-cta a{display:inline-block;margin:6px;padding:10px 22px;border-radius:var(--radius-xl);text-decoration:none;
  font-weight:600;font-size:14px;background:var(--accent);color:#fff}
.eco-cta a.ghost{background:var(--bg-card);color:var(--accent);border:1px solid var(--accent)}
@media(max-width:768px){.eco-layout{grid-template-columns:1fr;padding:24px 16px}.eco-toc{display:none}
  .pc{grid-template-columns:1fr}}
"""

# ============================ 共享 JS ============================
JS = """
function toggleSidebarPart(el){el.parentElement.classList.toggle('expanded');}
function filterArticles(part){
  document.querySelectorAll('.filter-pill').forEach(function(p){
    p.classList.toggle('active', p.getAttribute('data-part')===part);});
  document.querySelectorAll('.article-card-wrap').forEach(function(w){
    var show = !part || w.getAttribute('data-part')===part;
    w.style.display = show ? '' : 'none';});
}
function goTop(){window.scrollTo({top:0,behavior:'smooth'});}
window.addEventListener('scroll',function(){
  var bt=document.getElementById('backTop');
  if(bt) bt.classList.toggle('show', window.scrollY>400);
});

function toggleMenu(){
  var sb=document.getElementById('sidebar');
  if(sb) sb.classList.toggle('open');
}

// Skills page: category filter + modal + hash routing
function filterSkills(cat){
  document.querySelectorAll('.skill-cat').forEach(function(p){
    p.classList.toggle('active', p.getAttribute('data-cat')===cat);});
  document.querySelectorAll('.skill-card-v2').forEach(function(c){
    var show = cat==='全部' || c.getAttribute('data-cat')===cat;
    c.classList.toggle('hidden', !show);});
}
function openSkillModal(id){
  var m=document.getElementById('skillModal');
  var c=document.getElementById('skillContent-' + id);
  if(!m||!c) return;
  document.getElementById('skillModalInner').innerHTML = c.innerHTML;
  m.classList.add('show');
  document.body.style.overflow='hidden';
  if(history.replaceState) history.replaceState(null,null,'#skill-' + id);
}
function closeSkillModal(){
  var m=document.getElementById('skillModal');
  if(m) m.classList.remove('show');
  document.body.style.overflow='';
  if(history.replaceState) history.replaceState(null,null,location.pathname + location.search);
}
document.addEventListener('DOMContentLoaded',function(){
  var hash=location.hash;
  if(hash.indexOf('#skill-')===0){
    var id=hash.replace('#skill-','');
    setTimeout(function(){openSkillModal(id);},100);
  }
});
window.addEventListener('hashchange',function(){
  var hash=location.hash;
  if(hash.indexOf('#skill-')===0) openSkillModal(hash.replace('#skill-',''));
  else closeSkillModal();
});

// AI 提示词社区: 分类筛选 + 弹窗 + 一键复制
function filterPrompts(cat){
  document.querySelectorAll('.prompt-cat').forEach(function(p){
    p.classList.toggle('active', p.getAttribute('data-cat')===cat);});
  applyPromptFilter(cat);
}
function searchPrompts(q){
  var activeCat = '';
  document.querySelectorAll('.prompt-cat.active').forEach(function(p){activeCat = p.getAttribute('data-cat');});
  applyPromptFilter(activeCat, q);
}
function applyPromptFilter(cat, q){
  q = (q || '').toLowerCase().trim();
  document.querySelectorAll('.prompt-card').forEach(function(c){
    var matchCat = cat==='全部' || c.getAttribute('data-cat')===cat;
    var matchQ = !q;
    if(q && !matchQ){
      var txt = (c.textContent || '').toLowerCase();
      matchQ = txt.indexOf(q) !== -1;
    }
    c.classList.toggle('hidden', !(matchCat && matchQ));
  });
}
function openPromptModal(id){
  var m=document.getElementById('promptModal');
  var c=document.getElementById('promptContent-' + id);
  if(!m||!c) return;
  document.getElementById('promptModalInner').innerHTML = c.innerHTML;
  m.classList.add('show');
  document.body.style.overflow='hidden';
}
function closePromptModal(){
  var m=document.getElementById('promptModal');
  if(m) m.classList.remove('show');
  document.body.style.overflow='';
}
function copyPrompt(id, btn){
  var el=document.getElementById('promptText-' + id);
  if(!el) return;
  var text=el.innerText || el.textContent;
  function flash(){ if(!btn) return; var o=btn.textContent; btn.textContent='已复制 ✓'; btn.classList.add('copied'); setTimeout(function(){btn.textContent=o; btn.classList.remove('copied');},1800); }
  if(navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(text).then(flash, function(){fallbackCopy(text); flash();});
  } else { fallbackCopy(text); flash(); }
}
function fallbackCopy(text){
  var ta=document.createElement('textarea'); ta.value=text; ta.style.position='fixed'; ta.style.opacity='0';
  document.body.appendChild(ta); ta.select(); try{document.execCommand('copy');}catch(e){} document.body.removeChild(ta);
}

// Homepage: news hotspot tab switch (4 sub-categories)
function switchNews(key){
  document.querySelectorAll('.news-tab').forEach(function(b){
    b.classList.toggle('active', b.getAttribute('data-tab')===key);});
  document.querySelectorAll('.news-panel').forEach(function(p){
    p.classList.toggle('active', p.id==='news-'+key);});
}

// Homepage: global search (substring match over content/search-index.json)
var _SEARCH={data:null,loaded:false,q:'',focused:-1};
function _searchInit(){
  var inp=document.getElementById('global-search');
  if(!inp||_SEARCH.loaded) return;
  _SEARCH.loaded=true;
  fetch('content/search-index.json').then(function(r){return r.json();}).then(function(d){
    _SEARCH.data=d.items||[];}).catch(function(e){console.warn('search index load failed',e);});
  inp.addEventListener('input',function(){_searchRun(inp.value);});
  inp.addEventListener('keydown',function(e){
    var rs=document.querySelectorAll('.search-result');
    if(e.key==='ArrowDown'){e.preventDefault();_SEARCH.focused=Math.min(_SEARCH.focused+1,rs.length-1);_searchFocus();}
    else if(e.key==='ArrowUp'){e.preventDefault();_SEARCH.focused=Math.max(_SEARCH.focused-1,0);_searchFocus();}
    else if(e.key==='Enter'){if(_SEARCH.focused>=0&&rs[_SEARCH.focused]){e.preventDefault();rs[_SEARCH.focused].click();}}
    else if(e.key==='Escape'){inp.value='';_searchRun('');}
  });
  document.addEventListener('click',function(e){
    var box=document.querySelector('.search-box');
    if(box&&!box.contains(e.target)){document.getElementById('search-results').classList.remove('show');}
  });
}
function _searchHighlight(s,q){
  if(!q) return _escapeHtml(s);
  var i=s.toLowerCase().indexOf(q.toLowerCase());
  if(i<0) return _escapeHtml(s);
  return _escapeHtml(s.slice(0,i))+'<mark>'+_escapeHtml(s.slice(i,i+q.length))+'</mark>'+_escapeHtml(s.slice(i+q.length));
}
function _escapeHtml(s){
  return String(s).replace(/[&<>"']/g,function(c){return ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c];});
}
function _searchRun(q){
  _SEARCH.q=q; _SEARCH.focused=-1;
  var box=document.getElementById('search-results');
  var clr=document.querySelector('.search-clear');
  if(clr) clr.classList.toggle('show',!!q);
  q=q.trim();
  if(!q||!_SEARCH.data){box.classList.remove('show');return;}
  var ql=q.toLowerCase();
  var hits=[];
  for(var i=0;i<_SEARCH.data.length&&hits.length<30;i++){
    var it=_SEARCH.data[i];
    var t=it.t||''; var s=it.s||'';
    var tl=t.toLowerCase(), sl=s.toLowerCase();
    var score=0;
    var idxT=tl.indexOf(ql); var idxS=sl.indexOf(ql);
    if(idxT<0&&idxS<0) continue;
    // 标题命中权重 10，简介命中权重 1；标题前缀匹配再加 5
    if(idxT>=0){score+=10; if(idxT===0) score+=5;}
    if(idxS>=0) score+=1;
    // 同分类匹配稍微加权（让同类结果靠前）
    hits.push({i:i, score:score, it:it});
  }
  hits.sort(function(a,b){return b.score-a.score;});
  if(!hits.length){
    box.innerHTML='<div class="search-empty">未找到与「'+_escapeHtml(q)+'」相关的内容，试试更短的关键词</div>';
    box.classList.add('show'); return;
  }
  var html='';
  for(var j=0;j<hits.length;j++){
    var h=hits[j]; var it=h.it;
    var isExternal=String(it.u).indexOf('http')===0;
    var target=isExternal?' target="_blank" rel="noopener"':'';
    var icoBg=(it.color&&it.color.length===7)?(it.color+'22'):'var(--accent-soft)';
    var icoFg=it.color||'var(--c-teal)';
    html+='<a class="search-result" href="'+_escapeHtml(it.u)+'"'+target+' data-idx="'+j+'">'
      +'<div class="search-result-ico" style="background:'+icoBg+';color:'+icoFg+'">'+_escapeHtml(it.ico||'🔎')+'</div>'
      +'<div class="search-result-body">'
      +'<div class="search-result-title"><span class="search-result-cat">'+_escapeHtml(it.c||'')+'</span>'+_searchHighlight(it.t,q)+'</div>'
      +'<div class="search-result-snippet">'+_searchHighlight(it.s||'',q)+'</div>'
      +'</div></a>';
  }
  box.innerHTML=html; box.classList.add('show');
}
function _searchFocus(){
  var rs=document.querySelectorAll('.search-result');
  rs.forEach(function(r,i){r.classList.toggle('focused',i===_SEARCH.focused);});
  if(_SEARCH.focused>=0&&rs[_SEARCH.focused]) rs[_SEARCH.focused].scrollIntoView({block:'nearest'});
}
function _searchClear(){
  var inp=document.getElementById('global-search');
  if(inp){inp.value='';inp.focus();_searchRun('');}
}
document.addEventListener('DOMContentLoaded',_searchInit);

// Ecosystem detail page: TOC scroll-spy
function initEcoToc(){
  var links=document.querySelectorAll('.eco-toc a');
  if(!links.length) return;
  var secs=[].map.call(links, function(a){
    return document.getElementById(a.getAttribute('href').slice(1));}).filter(Boolean);
  function onScroll(){
    var pos=window.scrollY+130, cur=secs[0];
    secs.forEach(function(s){ if(s.offsetTop<=pos) cur=s; });
    links.forEach(function(a){ a.classList.toggle('active', cur && a.getAttribute('href')==='#'+cur.id); });
  }
  window.addEventListener('scroll', onScroll); onScroll();
}
if(document.querySelector('.eco-layout')) initEcoToc();
"""

# ============================ 公共片段 ============================
def hex_rgba(h, a):
    h = h.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return 'rgba(%d,%d,%d,%.2f)' % (r, g, b, a)

def topbar(active):
    navs = ""
    for (name, href, ico, color, grp, dropdown) in SECTIONS:
        dot = '<span class="nav-dot" style="background:%s"></span>' %  color if color else ''
        if dropdown is None:
            cls = "active" if name == active else ""
            navs += ('<a class="' + cls + '" href="' + href + '">' + dot +
                     name + '</a>')
        else:
            # 下拉菜单：父项高亮 = 父名匹配 或 任一子项匹配
            child_active = any(ch == active for (_, ch, _) in dropdown)
            cls = "active" if (name == active or child_active) else ""
            menu = '<div class="nav-dropdown' + (' open' if cls else '') + '">'
            menu += ('<a class="' + cls + '" href="' + href + '">' + dot + name +
                     '<span class="caret">▼</span></a>')
            menu += '<div class="nav-dropdown-menu">'
            for (cn, ch, cc) in dropdown:
                ccls = "active" if ch == active else ""
                cdot = '<span class="nav-dot" style="background:%s"></span>' % cc if cc else ''
                menu += ('<a class="' + ccls + '" href="' + ch + '">' + cdot + cn + '</a>')
            menu += '</div></div>'
            navs += menu
    return ('<header class="topbar"><div class="topbar-inner">'
            '<a class="blog-logo" href="index.html">'
            '<span class="blog-logo-icon">TW</span>老田的 AI 实战笔记</a>'
            '<button class="menu-btn" onclick="toggleMenu()">☰</button>'
            '<nav class="topbar-nav">' + navs + '</nav></div></header>')

def footer():
    links = ('<a href="index.html">首页</a>'
             '<a href="manual-wb.html">WB手册</a>'
             '<a href="cases-wb.html">WB案例</a>'
             '<a href="advanced.html">进阶篇</a>'
             '<a href="industry.html">岗位与行业落地</a>'
             '<a href="skills.html">Skills</a><a href="community.html">交流</a>')
    return ('<footer class="footer"><div class="footer-inner">'
            '<span>© ' + str(__import__('datetime').datetime.now().year) + ' ' + AUTHOR + ' · ' + CITY + ' · 用 WorkBuddy 沉淀</span>'
            '<div class="links">' + links + '</div></div></footer>'
            '<button id="backTop" onclick="goTop()" title="回到顶部">↑</button>')

def article_wrap(product, num, title, desc, href, cat=None):
    if cat is None: cat = product
    _cat_cls = {"使用手册":"","案例篇":"cat-case","进阶篇":"cat-advanced","岗位与行业落地":"cat-industry"}.get(cat,"")
    return ('<div class="article-card-wrap" data-part="' + product + '">'
            '<a class="article-card" href="' + href + '">'
            '<div class="article-card-top">'
            '<span class="article-cat' + (' '+_cat_cls if _cat_cls else '') + '">' + cat + '</span>'
            '<span class="article-ch">CH.' + num + '</span></div>'
            '<h4>' + title + '</h4>'
            '<p>' + desc + '</p>'
            '</a></div>')

# ============================ 内容数据 ============================
# 每个文档页：章节列表 (id, num, title, badge, body_html)
def ch_body(intro, blocks):
    # blocks: list of (type, content)
    out = '<p>' + intro + '</p>'
    for t, c in blocks:
        if t == 'p': out += '<p>' + c + '</p>'
        elif t == 'h3': out += '<h3>' + c + '</h3>'
        elif t == 'ul': out += '<ul>' + ''.join('<li>' + x + '</li>' for x in c) + '</ul>'
        elif t == 'callout': out += '<div class="callout"><span class="ttl">提示</span>' + c + '</div>'
        elif t == 'callout-warn': out += '<div class="callout warn"><span class="ttl">注意</span>' + c + '</div>'
        elif t == 'callout-info': out += '<div class="callout info"><span class="ttl">说明</span>' + c + '</div>'
        elif t == 'callout-key': out += '<div class="callout key"><span class="ttl">重点</span>' + c + '</div>'
        elif t == 'code': out += '<pre><code>' + c + '</code></pre>'
        elif t == 'table': out += c
    return out

# ---------- WorkBuddy 使用手册（复刻自「小饭的 AI 实战笔记」使用手册，共 11 章） ----------
def _load_manual_wb():
    _p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wb_manual.json")
    with open(_p, encoding="utf-8") as _f:
        return json.load(_f)["chapters"]
MANUAL_WB = _load_manual_wb()

# ---------- WorkBuddy 案例 ----------
CASES_WB = [
 ("chapter-1","01","第 1 章 从整理桌面文件这些小事做起", "WB案例",
  ch_body("桌面发票是典型的「电脑在替人承受混乱」的场景：电子发票、截图、PDF、微信下载文件、邮件附件混在一起，命名方式各不相同。人不在电脑前时，最烦的不是不知道怎么报销，而是不知道哪几张发票已经在电脑里、哪些字段还缺、哪些文件可能重复。",
   [('h3','整理桌面发票，不再回电脑前翻文件'),
    ('h3','场景痛点'),
    ('ul',['发票散落在桌面、下载目录、微信文件目录，格式可能是 PDF、JPG、PNG。',
           '文件名经常只叫"发票.pdf""image.png""微信图片_2026xxxx.jpg"。',
           '报销真正需要的是结构化字段：抬头、税号、金额、开票日期、发票号码、销售方。',
           '远程批量整理最怕误删、覆盖、移动原件，导致后面找不回来。']),
    ('h3','提示词示例'),
    ('code','请帮我整理电脑里的发票，但不要删除、移动或覆盖原文件。\n扫描范围只包括桌面、Downloads 和微信文件接收目录，时间范围为最近 30 天。\n候选条件：文件名包含"发票""电子发票""invoice"，或内容识别为发票的 PDF、JPG、PNG。\n第一步先返回候选清单和数量。\n第二步识别抬头、税号、金额、开票日期、发票号码、销售方、文件路径。\n第三步生成 invoice-ledger.xlsx，并列出"重复发票"和"无法识别字段"的人工确认清单。'),
    ('callout-key','执行后仅新增台账文件，桌面原发票不移动、不改名、不删除。')])),
 ("chapter-2","02","第 2 章 办公三件套：Word、Excel、PPT","WB案例", "<div><p>办公三件套是多数人第一次感受到 WorkBuddy 价值的地方。</p><p>该章节聚焦三类最常见的办公产物：Word 文档、Excel 表格和 PPT 汇报。</p><h2  id=\"ch11-办公三件套的共同工作流\">办公三件套的共同工作流 </h2><p>无论文档类型是什么，都建议先把任务拆成五个问题。很多“AI 做得不好”的办公任务，根源不是模型不会写，而是人没有把交付标准说清楚。</p><table tabindex=\"0\"><thead><tr><th>问题</th><th>要说清什么</th><th>示例</th></tr></thead><tbody><tr><td>目标</td><td>这份材料要帮助谁做什么决定</td><td>给部门负责人看，用于判断项目是否继续投入。</td></tr><tr><td>受众</td><td>阅读者是谁，懂不懂背景</td><td>管理层只看结论；项目组需要过程和责任人。</td></tr><tr><td>材料</td><td>哪些文件是事实来源，哪些只是参考</td><td><code>data.xlsx</code> 是唯一数据口径，旧版 PPT 只参考结构。</td></tr><tr><td>格式</td><td>要 Word、Excel、PPT，还是三者联动</td><td>输出一份项目复盘 Word、一张风险台账 Excel、一份 8 页汇报 PPT。</td></tr><tr><td>验收</td><td>怎么判断结果可用</td><td>数字能回到源文件，表格公式可刷新，PPT 投屏不溢出。</td></tr></tbody></table><h2  id=\"ch11-先选对-skill-办公任务的推荐组合\">先选对 Skill：办公任务的推荐组合 </h2><p>SkillHub上有很多办公效率、文档处理、表格处理、PPT 生成和会议纪要相关技能。</p><table tabindex=\"0\"><thead><tr><th>Skill 名称</th><th>适合处理</th><th>本章怎么用</th><th>注意点</th></tr></thead><tbody><tr><td>Word / DOCX</td><td>Word 文档</td><td>创建、检查、编辑 DOCX，处理标题、编号、表格、修订记录。</td><td>适合本地 docx 文件。</td></tr><tr><td>Excel / XLSX</td><td>Excel 表格</td><td>读取、清洗、写入工作簿，处理公式、日期、格式和模板保留。</td><td>先确认数据口径。</td></tr><tr><td>Powerpoint / PPTX</td><td>PPT 文件</td><td>创建、编辑、检查 PPTX，处理版式、占位符、备注、图表和视觉质检。</td><td>适合需要可编辑 PPTX 的场景。</td></tr><tr><td>Office Document Specialist Suite</td><td>Word / Excel / PPT</td><td>综合处理 Office 文件，适合自动化报告和多文件联动任务。</td><td>复杂任务建议分步验收。</td></tr><tr><td>wps</td><td>WPS 三件套</td><td>面向中国用户的 WPS Office 工作流，覆盖文字、表格、演示。</td><td>适合 WPS 生态用户。</td></tr><tr><td>腾讯文档 TENCENT DOCS</td><td>在线文档协作</td><td>创建、读取、编辑、搜索腾讯文档，覆盖在线 Word、Excel、幻灯片。</td><td>通常需要 API Key 或授权。</td></tr><tr><td>kdocs skill</td><td>金山文档 / WPS 云文档</td><td>处理 WPS 云文档、智能文档、表格、PPT、PDF、知识库。</td><td>通常需要 API Key。</td></tr><tr><td>Markdown Converter</td><td>材料解析</td><td>把 PDF、Word、PPT、Excel 转成 Markdown，方便模型先理解内容。</td><td>适合读材料，不等于最终排版。</td></tr><tr><td>PPT Generator / PPT Workflow</td><td>PPT 生成</td><td>从主题、讲稿或材料自动生成演示稿，适合初稿和结构化汇报。</td><td>生成后仍要人工审稿。</td></tr><tr><td>PowerPoint Automation</td><td>PPT 批改与导出</td><td>读取大纲、导出 PDF/图片、替换文字、统一字体和主题。</td><td>更适合 Windows + PowerPoint/WPS。</td></tr><tr><td>Excel公式生成</td><td>公式问题</td><td>把自然语言转换为 Excel/WPS/Google Sheets 公式，并解释防错版本。</td><td>公式要在样例数据上验证。</td></tr><tr><td>腾讯会议</td><td>会议到文档</td><td>预约会议、获取转写、获取 AI 纪要，再转成 Word 纪要、Excel 待办、PPT 汇报。</td><td>需要会议平台授权。</td></tr></tbody></table><p>一个实用的搭配思路是：本地文件优先用 <strong>Word / DOCX、Excel / XLSX、Powerpoint / PPTX</strong>；在线协作优先用 <strong>腾讯文档</strong> 或 <strong>kdocs skill</strong>；材料很多时先用 <strong>Markdown Converter</strong> 抽取结构；会议类办公流再叠加 <strong>腾讯会议</strong> 或会议纪要类 Skill。</p><h2  id=\"ch11-word-从空白页到正式文档\">Word：从空白页到正式文档 </h2><h3  id=\"ch11-这个场景的痛点\">这个场景的痛点 </h3><p>Word 看起来只是写字，但真实办公里的难点通常有四个：不知道该按什么结构写、语气不够正式、标题和编号混乱、内容没有证据来源。</p><p>尤其是方案、通知、报告、会议纪要、制度、申请、PRD 这类文档，如果开头就让 AI 自由发挥，结果往往像“万能模板”，读起来完整，却很难直接提交。</p><p>WorkBuddy 适合解决的不是“替你拍脑袋”，是把已有材料变成结构稳定、语气一致、可以继续修改的文档初稿。</p><p>要把文档目标、提交对象、语气和结构要求一次说清楚；生成后再用差异化反馈继续修改，而不是每次从头生成。</p><h3  id=\"ch11-适合交给-word-的任务\">适合交给 Word 的任务 </h3><ul><li><strong>正式方案</strong>：活动策划、项目方案、营销方案、培训方案。</li><li><strong>管理文档</strong>：制度、通知、申请、会议纪要、复盘报告、周报月报。</li><li><strong>产品材料</strong>：PRD、需求说明、竞品分析、用户访谈总结。</li></ul><h3  id=\"ch11-推荐流程\">推荐流程 </h3><table tabindex=\"0\"><thead><tr><th>步骤</th><th>WorkBuddy 做什么</th><th>人要确认什么</th></tr></thead><tbody><tr><td>1</td><td>读取材料，列出可用信息和缺失项。</td><td>哪些材料是事实来源，哪些只是参考。</td></tr><tr><td>2</td><td>生成文档大纲和写作口径。</td><td>读者是谁，文档是汇报、审批还是执行。</td></tr><tr><td>3</td><td>按大纲生成 Word 初稿。</td><td>标题层级、章节顺序、关键信息是否完整。</td></tr><tr><td>4</td><td>根据反馈润色、补充、删减。</td><td>哪些内容可以定稿，哪些必须标“待确认”。</td></tr><tr><td>5</td><td>输出可编辑 docx 和修改说明。</td><td>是否能直接发给同事审阅。</td></tr></tbody></table><h3  id=\"ch11-提示词示例-生成一份团建活动策划-word\">提示词示例：生成一份团建活动策划 Word </h3><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>帮我生成一份公司团建活动策划的 Word 文档框架。</span></span>\n<span class=\"line\"><span>公司约 80 人，包含：活动目标、活动主题建议、整体流程安排（含时间节点）、分组与互动游戏建议、预算构成清单、人员分工、风险预案和注意事项。</span></span>\n<span class=\"line\"><span>语言简洁实用，不需要写得过于详细，重点把整体框架和关键决策项列清楚，适合直接拿去和领导确认活动方向。</span></span></code></pre></div><p><img src=\"images/001_image_PhFMbu3kTo.CCU-WQ6L.webp\" alt=\"\"></p><p><img src=\"images/002_image_UVm5bKLrZo.BMziDVBr.webp\" alt=\"\"></p><h3  id=\"ch11-二次修改不要重写-要说差异\">二次修改不要重写，要说差异 </h3><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>请在上一版公司团建活动策划 Word 文档基础上进行修改，不要重新生成整篇。</span></span>\n<span class=\"line\"><span>修改要求：</span></span>\n<span class=\"line\"><span>将活动目标压缩为 3 条，每条不超过 50 字；</span></span>\n<span class=\"line\"><span>将流程安排改成表格，列为：时间、环节、主要内容、负责人、所需物料；</span></span>\n<span class=\"line\"><span>在节目类型建议中增加适合 100 人规模公司的互动环节，并删除执行难度过高的方案；</span></span>\n<span class=\"line\"><span>将预算构成进一步细化，增加：预算项目、预计金额、数量、单价、备注，并补充预算总额；</span></span>\n<span class=\"line\"><span>新增风险预案部分，覆盖人员迟到、设备故障、节目超时和突发安全问题；</span></span>\n<span class=\"line\"><span>整体语言更加正式、简洁，适合直接提交给领导审批。</span></span>\n<span class=\"line\"><span>输出修改后的 v2 版 Word 文档，并在 changelog.md 中列出本次修改内容。</span></span></code></pre></div><p><img src=\"images/003_image_IoOLbfEcvo.Bc4_8Cwe.webp\" alt=\"\"></p><p><img src=\"images/004_image_V1RpbVGuno.D2r0SEOZ.webp\" alt=\"\"></p><h3  id=\"ch11-进阶实战-比较两版制度-合同或方案\">进阶实战：比较两版制度、合同或方案 </h3><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>比较 policy-v3.docx 与 policy-v4.docx。</span></span>\n<span class=\"line\"><span>输出新增、删除、修改和仅格式变化四类差异，附章节和原文定位。</span></span>\n<span class=\"line\"><span>重点标记金额、日期、责任主体、审批条件、例外和否定表达。</span></span>\n<span class=\"line\"><span>生成影响清单和待确认问题，不给法律结论，不修改原文件。</span></span></code></pre></div><p><img src=\"images/011_image_HqbtbVTw3o.Cpu_Pvix.webp\" alt=\"\"></p><p><img src=\"images/012_image_MhArbb6Woo.DRhTsk5J.webp\" alt=\"\"></p><p>文档对比适合发现变化，不替代法务、财务或制度责任人的最终判断。</p><h2  id=\"ch11-excel-把表格变成能回答问题的分析\">Excel：把表格变成能回答问题的分析 </h2><h3  id=\"ch11-这个场景的痛点-2\">这个场景的痛点 </h3><p>Excel 的问题通常不在“会不会做图”，而在“这个表到底能回答什么问题”。</p><p>很多表格混着日期、文本、空值、合并单元格、多个口径和临时备注，直接让 AI 分析，很容易得到一份看似专业、其实没有业务价值的图表。</p><p>建议先导入 Excel 或 CSV，再一次说明分析指标、图表类型、统计维度、时间范围和是否需要报告。这个顺序很重要：先定义业务问题，再决定图表，而不是先生成漂亮图。</p><h3  id=\"ch11-适合交给-excel-的任务\">适合交给 Excel 的任务 </h3><ul><li><strong>数据清洗</strong>：去重、补空值、统一日期格式、拆分字段、合并多个表。</li><li><strong>经营分析</strong>：销售额、利润率、转化率、客单价、续费率、库存周转。</li><li><strong>报表生成</strong>：周报、月报、预算执行、考勤汇总、项目进度台账。</li><li><strong>公式辅助</strong>：生成或解释复杂公式，排查 <code>#N/A</code>、<code>#VALUE!</code>、循环引用。</li><li><strong>可视化</strong>：柱状图、折线图、饼图、透视表、仪表盘、异常点提示。</li></ul><h3  id=\"ch11-推荐流程-2\">推荐流程 </h3><table tabindex=\"0\"><thead><tr><th>阶段</th><th>提示重点</th><th>输出</th></tr></thead><tbody><tr><td>读表</td><td>先描述工作簿结构、字段含义、样例行和明显脏数据。</td><td>数据字典、问题清单。</td></tr><tr><td>定指标</td><td>说明要回答的业务问题，而不是只说“分析一下”。</td><td>指标口径表。</td></tr><tr><td>清洗</td><td>说明空值、重复值、异常值如何处理。</td><td>清洗后的 xlsx / csv。</td></tr><tr><td>计算</td><td>生成公式、透视表或统计表，并保留可刷新结构。</td><td>汇总表、公式说明。</td></tr><tr><td>可视化</td><td>根据业务问题选择图表，避免图表堆砌。</td><td>图表、分析结论。</td></tr></tbody></table><h3  id=\"ch11-提示词示例-销售数据分析\">提示词示例：销售数据分析 </h3><div class=\"language-Plain vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">Plain</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>请读取 电商销售数据.xlsx，先不要修改原文件。</span></span>\n<span class=\"line\"><span>业务问题：分析本月各产品线的销售表现和盈利能力，判断哪些产品线贡献高、哪些利润表现较弱，并识别本月销售过程中的异常波动。</span></span>\n<span class=\"line\"><span>请输出：</span></span>\n<span class=\"line\"><span>说明数据字段含义，并检查缺失值、重复记录、异常值和字段格式问题；</span></span>\n<span class=\"line\"><span>按产品线统计销售额、毛利、毛利率、销售额占比和毛利贡献占比，并进行排名；</span></span>\n<span class=\"line\"><span>按日汇总销售额和毛利率，分析本月销售表现的日度变化；如果数据跨度和完整性允许，再补充按周统计；</span></span>\n<span class=\"line\"><span>生成柱状图对比各产品线销售额和毛利，生成折线图展示本月每日销售额变化；</span></span>\n<span class=\"line\"><span>识别销售额、毛利率或单笔订单金额明显异常的日期或记录，并结合数据说明异常表现，不要在缺少依据时推测业务原因；</span></span>\n<span class=\"line\"><span>总结本月表现最好的产品线、需要重点关注的产品线，以及 3 条可直接用于业务复盘的结论。</span></span>\n<span class=\"line\"><span>输出 output/sales-analysis.xlsx 和 output/summary.md。</span></span>\n<span class=\"line\"><span>要求：保留原始数据，统计过程和公式可追溯；图表标题直接表达主要结论；无法从数据中确认的原因明确标注为待核实，不要自行编造。</span></span></code></pre></div><p><img src=\"images/005_image_I118b7wyUo.C76TSBT_.webp\" alt=\"\"></p><p><img src=\"images/006_image_BWkRb60JPo.3MkdMOWG.webp\" alt=\"\"></p><p><img src=\"images/007_image_XtfQbkCqio.vRy7ZTaX.webp\" alt=\"\"></p><h3  id=\"ch11-进阶实战-多表合并-对账与异常清单\">进阶实战：多表合并、对账与异常清单 </h3><p>基础办公中最有价值的不是“做个图表”，而是把数据口径和异常暴露出来：</p><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>合并 input/sales 中 6 个区域的周销售表。</span></span>\n<span class=\"line\"><span>先检查列名、数据类型、日期范围、币种和主键，不一致时停止并列差异。</span></span>\n<span class=\"line\"><span>按订单号去重，但保留重复来源；汇总前输出总行数、空值、异常值和重复数。</span></span>\n<span class=\"line\"><span>生成 clean-sales.xlsx、exception-list.xlsx 和 reconciliation.md。</span></span>\n<span class=\"line\"><span>金额汇总必须与各源表合计对账，差异不为 0 时不生成管理结论。</span></span></code></pre></div><p><img src=\"images/009_image_UNEqbRnJfo.DOMis77x.webp\" alt=\"\"></p><p><img src=\"images/010_image_L25tbHIUeo.bdit0dCN.webp\" alt=\"\"></p><div class=\"callout key\"><p><strong>验收</strong>：输入总量、清洗变化和输出总量守恒；公式可重算；异常没有被静默删除；图表使用的字段和汇总表一致。</p></div><h2  id=\"ch11-ppt-不是套模板-而是把材料变成叙事\">PPT：不是套模板，而是把材料变成叙事 </h2><h3  id=\"ch11-这个场景的痛点-3\">这个场景的痛点 </h3><p>PPT 最容易被误用。</p><p>很多人把任务写成“帮我做一份高级感 PPT”，结果 AI 只能猜风格，生成一堆好看的空话。真正可用的 PPT 必须先回答三个问题：这次汇报给谁看、对方听完要做什么决定、你有多少时间讲。</p><p>PPT 生成强调同时提供素材、页数要求、受众对象和风格偏好。对 WorkBuddy 来说，PPT Skill 可以负责页面生成，但故事线必须先确认。否则页面越漂亮，越容易掩盖逻辑问题。</p><h3  id=\"ch11-适合交给-ppt-的任务\">适合交给 PPT 的任务 </h3><ul><li><strong>项目汇报</strong>：项目进展、阶段复盘、里程碑计划、风险与资源请求。</li><li><strong>经营汇报</strong>：月度经营分析、销售复盘、预算执行、用户增长复盘。</li><li><strong>培训课件</strong>：新人培训、产品培训、客户培训、内部分享。</li><li><strong>方案展示</strong>：客户方案、竞标材料、商业计划、产品发布。</li></ul><h3  id=\"ch11-推荐流程-3\">推荐流程 </h3><table tabindex=\"0\"><thead><tr><th>步骤</th><th>WorkBuddy 做什么</th><th>人要确认什么</th></tr></thead><tbody><tr><td>1</td><td>把 Word、Excel、图片、旧 PPT 转成材料摘要。</td><td>哪些内容必须保留，哪些可以删。</td></tr><tr><td>2</td><td>生成 6-10 页故事线和每页标题。</td><td>汇报对象、时长、决策目标。</td></tr><tr><td>3</td><td>根据确认后的大纲制作 PPT。</td><td>每页是否只有一个核心观点。</td></tr><tr><td>4</td><td>补图表、备注、来源映射和导出版本。</td><td>关键数字是否来自 Excel。</td></tr><tr><td>5</td><td>做版式检查：文字溢出、图片缺失、字号、颜色。</td><td>投屏后是否能读，是否适合现场讲。</td></tr></tbody></table><h3  id=\"ch11-提示词示例-从材料包制作汇报-ppt\">提示词示例：从材料包制作汇报 PPT </h3><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>请根据当前工作区材料制作一份 8 页以内的 AI Agent 主题分享 PPT。</span></span>\n<span class=\"line\"><span>受众：对 AI 有基础认知，但不了解 Agent 的业务和管理人员。</span></span>\n<span class=\"line\"><span>汇报时长：10 分钟。</span></span>\n<span class=\"line\"><span></span></span>\n<span class=\"line\"><span>目标：让听众理解 AI Agent 是什么、与普通 AI 对话工具有什么区别、能解决哪些问题，以及企业应该如何判断是否值得落地。</span></span>\n<span class=\"line\"><span>素材：</span></span>\n<span class=\"line\"><span>AI术语全景手册.md 是主要内容材料；</span></span>\n<span class=\"line\"><span>不要补充工作区材料之外的事实和数据。</span></span>\n<span class=\"line\"><span>全文控制在 8 页以内，每页只表达一个核心结论；</span></span>\n<span class=\"line\"><span>案例、数据和关键判断必须标注素材来源，无法确认的内容不要自行补充；</span></span>\n<span class=\"line\"><span>PPT 标题尽量直接表达观点，不使用 AI Agent 介绍、应用场景这类泛化标题；</span></span>\n<span class=\"line\"><span>输出 output/ai-agent.pptx；</span></span>\n<span class=\"line\"><span>生成后检查文字溢出、页面留白、图表口径、图片缺失、字体一致性和页码。</span></span>\n<span class=\"line\"><span></span></span>\n<span class=\"line\"><span>整体风格：专业、简洁、有科技感，但不要过度使用渐变、发光和装饰性元素，适合正式分享和内部汇报。</span></span></code></pre></div><p><img src=\"images/008_image_ABXObcQeeo.DF8YQc0z.webp\" alt=\"\"></p><h2  id=\"ch11-三件套联动案例-会议之后自动形成交付包\">三件套联动案例：会议之后自动形成交付包 </h2><p>很多办公任务不是单文件，而是“会议之后要有东西”。</p><p>比如开完一次产品评审会，会议里有用户反馈、功能决策、待办事项和下个版本计划。手工做法通常是：先整理纪要，再补 PRD，再做任务表，最后做汇报 PPT。</p><p>WorkBuddy 的价值就在于把这些交付物串成同一条事实链。</p><h3  id=\"ch11-场景痛点\">场景痛点 </h3><ul><li>会议讨论是口语化的，决议、分歧和待办混在一起。</li><li>PRD 需要结构化，但会议纪要里没有标准格式。</li><li>Excel 任务表需要负责人、截止日期和状态字段，不能只是一段总结。</li><li>PPT 汇报需要给老板看，不能把会议全文搬进去。</li></ul><h3  id=\"ch11-可用-skill-组合\">可用 Skill 组合 </h3><table tabindex=\"0\"><thead><tr><th>环节</th><th>推荐 Skill</th><th>作用</th></tr></thead><tbody><tr><td>获取会议内容</td><td>腾讯会议 / 智能会议纪要类 Skill</td><td>获取转写、AI 纪要、决议、行动项。</td></tr><tr><td>生成 PRD</td><td>Word / DOCX、腾讯文档、kdocs skill</td><td>把会议内容改写成产品需求文档。</td></tr><tr><td>生成任务表</td><td>Excel / XLSX、Excel/WPS 表格自动化工具</td><td>输出负责人、截止日期、优先级、状态和验收标准。</td></tr><tr><td>生成汇报</td><td>Powerpoint / PPTX、PPT Workflow、PPT Generator</td><td>把 PRD 和任务进度转成管理层汇报。</td></tr></tbody></table><h3  id=\"ch11-提示词示例-会议到-prd-任务表-汇报\">提示词示例：会议到 PRD、任务表、汇报 </h3><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>请读取本次产品评审会议的转写和 AI 纪要，生成一个办公交付包。</span></span>\n<span class=\"line\"><span>目标：把会议内容转成可以推进研发的材料。</span></span>\n<span class=\"line\"><span>请输出：</span></span>\n<span class=\"line\"><span>1. Word：output/feature-prd.docx，包含背景、目标用户、核心问题、需求列表、流程说明、验收标准、风险和待确认问题；</span></span>\n<span class=\"line\"><span>2. Excel：output/action-items.xlsx，字段包含事项、负责人、优先级、截止日期、依赖、状态、验收标准；</span></span>\n<span class=\"line\"><span>3. PPT：output/review-summary.pptx，6 页以内，面向管理层，突出本次会议决议、资源请求和风险。</span></span>\n<span class=\"line\"><span>约束：</span></span>\n<span class=\"line\"><span>- 会议中没有明确确认的内容，不要写成既定结论；</span></span>\n<span class=\"line\"><span>- 人名、日期、功能范围必须保留来源；</span></span>\n<span class=\"line\"><span>- 如果缺少负责人或时间，请标为待确认；</span></span>\n<span class=\"line\"><span>- 先输出大纲和任务表字段预览，等我确认后再生成文件。</span></span></code></pre></div><h2  id=\"ch11-常见错误与修正方式\">常见错误与修正方式 </h2><table tabindex=\"0\"><thead><tr><th>常见错误</th><th>为什么会发生</th><th>更好的写法</th></tr></thead><tbody><tr><td>“帮我做个 PPT，要高级一点”</td><td>没有受众、目标和材料约束。</td><td>说明受众、汇报时长、页数、决策目标、参考模板和必须保留的数据。</td></tr><tr><td>“分析一下这个 Excel”</td><td>没有业务问题，模型只能泛泛总结。</td><td>说明要回答什么问题、统计哪些指标、按什么维度比较。</td></tr><tr><td>“写一份报告”</td><td>没有文档类型和语气要求。</td><td>说明是方案、总结、申请、纪要还是 PRD，并指定读者。</td></tr><tr><td>“全部自动完成，不用问我”</td><td>关键口径没确认，风险会被放大。</td><td>先让 WorkBuddy 输出材料清单、风险清单和大纲，确认后再生成。</td></tr><tr><td>“把这堆材料合成一个文件”</td><td>没有区分事实、参考和待确认。</td><td>指定唯一数据源、参考文件和不能编造的字段。</td></tr></tbody></table></div>"),
    ("chapter-3","03","第 3 章 远程控制你的电脑，不用发愁不在电脑前","WB案例","<p>你人不在电脑前，WorkBuddy 小程序可以成为远程任务入口，把指令发回正在运行的电脑端，让电脑继续查文件、读资料、整理发票、处理微信文件，甚至持续汇报一个长任务的进展。</p><h2 id=\"小程序远程控制电脑\">小程序远程控制电脑 </h2><p><img src=\"images/case3-01.jpg\" alt=\"\" loading=\"lazy\"></p><p>传统远程办公通常有两种方式：一种是把电脑屏幕投到手机上，自己点鼠标；另一种是把文件先传到云端，再在手机上处理。</p><p>WorkBuddy 的远程方式介于二者之间：用户不直接操控鼠标，而是把任务说清楚；电脑端 WorkBuddy 根据授权范围读取本地文件、调用 Skill 或本地工具，把中间结果和最终产物回传到手机端。</p><table tabindex=\"0\"><thead><tr><th>能力层</th><th>解决什么问题</th><th>使用时要确认什么</th></tr></thead><tbody><tr><td><strong>手机端入口</strong></td><td>在路上、会议间隙、客户现场也能发起任务</td><td>账号已登录，消息能送达，语音转文字没有关键错误</td></tr><tr><td><strong>电脑端执行</strong></td><td>读取本机目录、调用本地软件、处理私有资料</td><td>电脑在线，WorkBuddy 正在运行，目录权限已授权</td></tr><tr><td><strong>任务回传</strong></td><td>把候选文件、摘要、表格、截图、压缩包返回给手机</td><td>输出路径明确，不覆盖原文件，敏感信息先脱敏</td></tr><tr><td><strong>人工确认</strong></td><td>避免远程状态下误删、误发、误改重要资料</td><td>高风险动作必须暂停确认，不把“执行完”当成“验收完”</td></tr></tbody></table><h2 id=\"先分清-云端模式还是本机模式\">先分清：云端模式还是本机模式 </h2><p>移动端适合在通勤、出差、跨设备办公时继续推进任务。但在使用前，必须先判断任务究竟应该跑在云端，还是跑在本机。</p><p>这个判断会直接影响它能否读取电脑文件、是否需要电脑在线，以及数据是否适合进入云端环境。</p><p><img src=\"images/case3-02.jpg\" alt=\"\" loading=\"lazy\"></p><table tabindex=\"0\"><thead><tr><th>判断问题</th><th>云端模式</th><th>本机模式</th></tr></thead><tbody><tr><td>是否需要电脑在线</td><td>通常不需要</td><td>需要电脑在线，并且 WorkBuddy 处于可响应状态</td></tr><tr><td>能否读取电脑目录</td><td>不能直接读取</td><td>可以读取已授权范围内的本地目录</td></tr><tr><td>适合任务</td><td>公开资料调研、写提纲、生成轻量文本</td><td>查找本机文件、读取私有资料、调用本地 Skill 或软件</td></tr><tr><td>主要风险</td><td>资料是否适合进入云端</td><td>目录权限、误操作、电脑离线、结果未验收</td></tr></tbody></table><h2 id=\"人在外面-临时要电脑里的文件\">人在外面，临时要电脑里的文件 </h2><p>这是最容易让用户第一次感受到远程控制价值的场景。合作方突然问培训课件、项目汇报、合同版本、报价单、活动海报源文件在哪里，而资料都在办公室电脑里。过去只能回复“我回去找一下”，现在可以在小程序里语音发起任务，让电脑端 WorkBuddy 在指定目录中查找候选文件，读取内容并整理摘要。</p><h3 id=\"场景痛点\">场景痛点 </h3><ul><li>文件名不一定记得完整，只记得“培训”“项目汇报”“某客户”等关键词。</li><li>电脑里可能有多个版本，远程状态下不能凭感觉直接发。</li><li>临时需求往往只需要先给对方一个摘要或确认口径，不一定马上发送原文件。</li></ul><h3 id=\"推荐流程\">推荐流程 </h3><ol><li>先限定目录，比如桌面、Downloads、项目资料、training 文件夹。</li><li>让 WorkBuddy 只读扫描，列出候选文件、修改时间、文件大小和可能匹配原因。</li><li>确认目标文件后，再读取内容并生成手机端可转发的摘要。</li><li>需要发送文件时，先整理到一个单独输出目录，不直接移动原文件。</li></ol><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>你帮我看一下，我电脑上在我这个local long GPT里边有一个关于xx公司的一些PPT，然后你整理一下内容发给我。</span></span></code></pre></div><p><img src=\"images/case3-03.jpg\" alt=\"\" loading=\"lazy\"></p><h2 id=\"微信文件直接处理-不必先搬来搬去\">微信文件直接处理，不必先搬来搬去 </h2><p>很多任务不是从电脑文件夹开始，而是从微信聊天里突然冒出来：客户发来一个合同 PDF，朋友发来一张票据照片，同事丢来一个 Excel，供应商转来一个压缩包。传统流程是先下载到手机，再传电脑，再找目录，再打开软件。小程序更适合把“微信上下文里的文件”直接变成 WorkBuddy 的输入。</p><p><img src=\"images/case3-04.jpg\" alt=\"\" loading=\"lazy\"></p><h2 id=\"远程监控长任务-让手机成为任务看板\">远程监控长任务，让手机成为任务看板 </h2><p>远程控制还有一个更进阶的用法：不是让 WorkBuddy 做一个几秒钟的小任务，而是让它持续推进一个需要等待、分阶段处理或容易失败的任务。比如批量转换文件、整理大目录、生成网站、处理会议录音、运行代码测试、下载资料、爬取公开网页、自动化检查系统状态。</p><h3 id=\"远程监控适合什么\">远程监控适合什么 </h3><ul><li>任务耗时超过 3 分钟，需要阶段汇报。</li><li>任务中间可能遇到失败项，需要记录并继续处理其他文件。</li><li>任务结果需要先看预览，再决定是否批量执行下一步。</li><li>任务过程中可能触发登录、付款、发送消息、覆盖文件等高风险动作。</li></ul><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>请启动这个批量处理任务，并把手机端当作进度看板。</span></span></code></pre></div><p><img src=\"images/case3-05.jpg\" alt=\"\" loading=\"lazy\"></p><div class=\"language-Plain vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">Plain</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>你控制摄像头拍张照片，描述一下电脑前面的画面</span></span></code></pre></div><p><img src=\"images/case3-06.png\" alt=\"\" loading=\"lazy\"></p></div></div>"),
    ("chapter-4","04","第 4 章 生活助手的价值，是减少琐碎","WB案例","<h2 id=\"生活问题比办公问题更模糊\">生活问题比办公问题更模糊 </h2><p>“帮我规划旅行”“看看体检报告”“今天吃什么”“给我算算运势”，看起来都只需一句话，背后却混合了偏好、实时数据、隐私和风险。办公文件做错还可以返工，医疗、付款、签证和重大决定做错，代价可能完全不同。</p><p>因此生活场景先分三类：</p><table tabindex=\"0\"><thead><tr><th>类型</th><th>WorkBuddy 可以做什么</th><th>人必须做什么</th></tr></thead><tbody><tr><td>信息整理型</td><td>收集偏好、比较候选、生成清单</td><td>确认事实与最终选择</td></tr><tr><td>实时决策型</td><td>查询天气、路线、库存和规则，标注时间</td><td>回到官方或服务商页面核验并操作</td></tr><tr><td>高风险或娱乐型</td><td>整理就医问题、提供娱乐性解读</td><td>医疗交给专业人员，命理不作为决策依据</td></tr></tbody></table><h2 id=\"场景一-三天旅行-不想打开二十个-app\">场景一：三天旅行，不想打开二十个 App </h2><p>攻略、地图、天气、酒店、交通、预算和同行人偏好都存在于不同应用中。普通 AI 规划的行程看起来完整，却可能把相距很远的地点排在一起，有的会引用过期营业时间，甚至虚构餐厅。</p><ul><li><a href=\"https://skillhub.cn/skills/travelassistant\" target=\"_blank\" rel=\"noreferrer\">旅游助手</a>：行程、目的地、住宿、美食和行李清单；</li><li><a href=\"https://skillhub.cn/skills/tencentmap-map-assistant\" target=\"_blank\" rel=\"noreferrer\">腾讯地图地图助手</a>：POI、路线、距离、天气与地图；</li><li><a href=\"https://skillhub.cn/skills/smart-packing-list-new\" target=\"_blank\" rel=\"noreferrer\">旅游行李清单</a>：按天气、天数和人群生成打包清单；</li><li><a href=\"https://skillhub.cn/skills/weather-8tour\" target=\"_blank\" rel=\"noreferrer\">旅游天气风险</a>：需要精细天气风险时补充。</li></ul><h3 id=\"第一步-先收集约束\">第一步：先收集约束 </h3><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>先不要排行程，用不超过 8 个问题收集旅行约束：</span></span> <span class=\"line\"><span>出发地、日期、同行人、预算、交通偏好、每日步行上限、兴趣、</span></span> <span class=\"line\"><span>饮食禁忌、必须去和明确不去的地点。</span></span> <span class=\"line\"><span>已经提供的信息不要重复询问。</span></span></code></pre></div><h3 id=\"第二步-候选路线与实时核验\">第二步：候选路线与实时核验 </h3><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>为 2 名成人规划 7 月 18-20 日上海到泉州的 3 天自由行。</span></span> <span class=\"line\"><span>预算 5000 元，偏好人文与本地小吃，每天步行不超过 15000 步。</span></span> <span class=\"line\"><span>先给两个路线方向并解释取舍，我确认后再生成逐日计划。</span></span> <span class=\"line\"><span></span></span> <span class=\"line\"><span>使用地图能力核对地点顺序、路程和预计交通时间；</span></span> <span class=\"line\"><span>把票价、开放时间、预约、天气和交通班次标注查询时间与来源。</span></span> <span class=\"line\"><span>无法实时核验的内容写“待确认”，不要补造。</span></span> <span class=\"line\"><span>输出雨天替代方案、预算区间和行李清单。</span></span> <span class=\"line\"><span>不要登录、预订、付款或代替我接受退改条款。</span></span></code></pre></div><p><img src=\"images/case4-01.png\" alt=\"\" loading=\"lazy\"></p><p>WorkBuddy 在执行过程中并不是一来就直接帮你做决定，而是尽可能详尽的再向你询问一些问题，确保真的像个专属导游那样帮你规划行程。</p><p><img src=\"images/case4-02.png\" alt=\"\" loading=\"lazy\"></p><h3 id=\"执行链与交付物\">执行链与交付物 </h3><p>偏好问卷 → 两个路线草案 → 人工选方向 → 地图优化 → 天气与开放信息核验 → 预算与行李 → 可分享行程页。真正可用的交付物应包含了地图行程规划、合理的游玩和交通时间规划、数据来源与真实的车次，而不只是一张漂亮日程表。</p><p>预订前由人再次确认库存、价格、签证、证件、保险和退改政策。涉及老人、儿童、孕妇、慢性病或无障碍需求时，要把限制明确写入任务，不能由模型自行推断。</p><p><img src=\"images/case4-03.png\" alt=\"\" loading=\"lazy\"></p><h2 id=\"场景二-旅行结束后-把照片和账单变成可复用记录\">场景二：旅行结束后，把照片和账单变成可复用记录 </h2><p>WorkBuddy 还可以在旅行后完成照片按日期地点整理、票据分类、预算复盘和攻略草稿，但不要默认读取整本相册或删除原图。</p><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>只读取 trip-quanzhou/import 中的照片和票据副本。</span></span> <span class=\"line\"><span>按拍摄时间生成每日时间线，识别失败的文件列入人工确认。</span></span> <span class=\"line\"><span>票据按交通、住宿、餐饮、门票分类，金额汇总后与预算对比。</span></span> <span class=\"line\"><span>根据我确认的地点和感受生成一份私人旅行记录，</span></span> <span class=\"line\"><span>人物照片、定位和订单号在公开版本中全部脱敏。</span></span> <span class=\"line\"><span>不移动、不删除原文件。</span></span></code></pre></div><p>这个场景最终可以反哺自媒体章：私人记录确认后，再选择哪些信息适合做小红书攻略或公众号长文。</p><h2 id=\"场景三-体检报告看不懂-先准备一次更有效的就医\">场景三：体检报告看不懂，先准备一次更有效的就医 </h2><p>体检指标和症状记录很多，用户容易在网上搜索后自行诊断；部分健康 Skill 甚至宣称可以给出患病概率。蓝皮书不采用这种写法。</p><ul><li><a href=\"https://skillhub.cn/skills/health-coach-pro\" target=\"_blank\" rel=\"noreferrer\">健康管理顾问</a>：强调生活方式、体检数据理解和就医准备，不诊断、不处方；</li><li>腾讯健康相关临床 Skill 只应在符合资质、授权和实际医疗工作流时使用；普通用户不能把输出当诊断结论；</li><li>用药安全问题应优先咨询医生或药师，不让通用 Agent 决定停药、换药和剂量。</li></ul><p>世界卫生组织在 AI 健康治理中强调，应把伦理、人权和问责置于技术设计与使用中心。对个人用户而言，最实用的边界是：AI 帮助整理信息和准备问题，不代替临床判断。<a href=\"https://www.who.int/publications/i/item/9789240029200\" target=\"_blank\" rel=\"noreferrer\">参考：WHO《Ethics and governance of artificial intelligence for health》</a></p><h3 id=\"安全指令\">安全指令 </h3><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>把我提供的体检报告和症状记录整理成一页就医准备材料。</span></span> <span class=\"line\"><span>输出：症状时间线、报告中的原始指标与参考区间、</span></span> <span class=\"line\"><span>我还需要补充的信息、挂号时可询问的问题、日常观察模板。</span></span> <span class=\"line\"><span></span></span> <span class=\"line\"><span>不得给出确定诊断、患病概率、处方、剂量、停药或换药建议；</span></span> <span class=\"line\"><span>不得把相关性写成因果。发现可能需要及时线下处理的信息时，</span></span> <span class=\"line\"><span>只提示我联系当地医疗机构或急救服务，不继续在线推演。</span></span></code></pre></div><p><img src=\"images/case4-04.png\" alt=\"\" loading=\"lazy\"></p><p>以上是我从网上找的一份就诊记录，当我把这份不太详尽的就诊记录同步给WorkBuddy，他会帮我分析并生成就医材料。</p><p><img src=\"images/case4-05.png\" alt=\"\" loading=\"lazy\"></p><h2 id=\"场景四-健康习惯与饮食计划-可以做得更日常\">场景四：健康习惯与饮食计划，可以做得更日常 </h2><p>低风险健康管理更适合 WorkBuddy：饮水、睡眠、运动、膳食记录和复诊提醒。可选 <a href=\"https://skillhub.cn/skills/nutrition-and-health\" target=\"_blank\" rel=\"noreferrer\">营养健康</a>、<a href=\"https://skillhub.cn/skills/healthy-recipe-recommender\" target=\"_blank\" rel=\"noreferrer\">健康食谱推荐</a>等 Skill，但仍需声明过敏、疾病、用药、孕期和专业限制。</p><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>根据我确认的饮食偏好、过敏信息、预算和可用厨具，</span></span> <span class=\"line\"><span>生成 5 天晚餐候选与采购清单。每餐说明主要食材、预计时间和替换项。</span></span> <span class=\"line\"><span>不要声称治疗疾病或保证减重效果。</span></span> <span class=\"line\"><span>涉及糖尿病、肾病、孕期或药物相互作用时，停止个性化建议，</span></span> <span class=\"line\"><span>改为列出需要向医生或注册营养专业人员确认的问题。</span></span></code></pre></div><p><img src=\"images/case4-06.png\" alt=\"\" loading=\"lazy\"></p><p><img src=\"images/case4-07.png\" alt=\"\" loading=\"lazy\"></p><p>同样的在执行过程中会仔细询问我的饮食结构和目前厨房里可用的厨具，给出真正的属于我自己的晚餐计划，而不是一份看似精确但对我个人并不适配的医疗饮食方案。</p><p><img src=\"images/case4-08.png\" alt=\"\" loading=\"lazy\"></p><h2 id=\"场景五-算命、星盘与卜卦-怎样写得有趣又不越界\">场景五：算命、星盘与卜卦，怎样写得有趣又不越界 </h2><p>传统文化和娱乐测试是很多普通用户接触 Agent 的入口，可以用于传统文化体验、社交互动、写作灵感和自我提问。</p><p>不过出生时间、地点和家庭信息属于个人信息；解释结果容易被写成确定预言；用户也可能据此做医疗、投资、招聘、婚恋或职业决定。</p><p>更稳妥的指令</p><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>使用传统文化娱乐方式，根据我主动提供的信息生成一份八字文化解读。</span></span> <span class=\"line\"><span>开头明确“仅供娱乐与文化体验，不预测确定未来”。</span></span> <span class=\"line\"><span>区分排盘计算、传统说法和现代反思问题，不把传统解释写成事实。</span></span> <span class=\"line\"><span>不提供医疗、投资、法律、婚恋或职业决策建议。</span></span> <span class=\"line\"><span>结尾把每个结论改写成可验证的自我提问，并提供至少一个反例角度。</span></span> <span class=\"line\"><span>不要长期保存出生时间和地点，任务结束后提醒我清理输入。</span></span></code></pre></div><p><img src=\"images/case4-09.png\" alt=\"\" loading=\"lazy\"></p><h2 id=\"场景六-穿搭、家庭清单和消费比较\">场景六：穿搭、家庭清单和消费比较 </h2><p>生活助手还有很多低风险、但非常实用的场景：</p><p>使用天气查询和 <a href=\"https://skillhub.cn/skills/daily-outfit-inspiration\" target=\"_blank\" rel=\"noreferrer\">每日穿搭灵感</a>，输入城市、场合、已有衣物和不喜欢的风格。结果应优先使用衣柜现有单品，不要默认推荐购买。</p><p>把证件、药品、充电设备、儿童用品和宠物安排做成按人分组的清单，明确负责人和完成状态。自动化负责提醒，不负责确认药品是否适合某个家庭成员。</p><p>让 WorkBuddy 建立参数、价格、售后、隐私和长期成本表，再由人查看官方页面和真实合同。广告软文、联盟链接和商家评分要单独标记，不能混入事实列。</p><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>比较 3 款扫地机器人，只使用厂商官网、说明书和我提供的报价。</span></span> <span class=\"line\"><span>表格列出清洁结构、避障、耗材、隐私、保修、价格和不确定项。</span></span> <span class=\"line\"><span>把营销表述与可验证参数分开，不根据销量自动推荐。</span></span> <span class=\"line\"><span>最后根据“家中有宠物、门槛 2cm、重视隐私”给条件性建议，</span></span> <span class=\"line\"><span>不要代替我下单或接受服务条款。</span></span></code></pre></div><p><img src=\"images/case4-10.png\" alt=\"\" loading=\"lazy\"></p><h2 id=\"场景七-情绪记录与现实支持\">场景七：情绪记录与现实支持 </h2><p>WorkBuddy 可以帮助记录情绪触发点、睡眠、事件和应对方式，生成复盘问题或与咨询师沟通的摘要。它不会冒充心理医生，也不会让用户只依赖 Agent。</p><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>把我本周的情绪记录按“事件、想法、感受、身体反应、采取行动”整理。</span></span> <span class=\"line\"><span>只总结重复模式，不诊断、不贴人格标签。</span></span> <span class=\"line\"><span>生成 5 个我可以与可信赖的人或专业人员讨论的问题。</span></span> <span class=\"line\"><span>如果内容出现自伤、他伤或即时危险信号，停止普通复盘，</span></span> <span class=\"line\"><span>提示我立即联系当地紧急服务、专业机构或身边可信赖的人。</span></span></code></pre></div><p><img src=\"images/case4-11.png\" alt=\"\" loading=\"lazy\"></p><h2 id=\"生活-skill-安装前的四项检查\">生活 Skill 安装前的四项检查 </h2><ol><li><strong>实时性</strong>：天气、价格、库存、政策和营业时间从哪里来，查询日期是什么；</li><li><strong>隐私</strong>：出生信息、位置、健康数据和家庭资料发送到哪里，能否只在本地处理；</li><li><strong>动作权限</strong>：是否会登录、预订、付款、发送消息或修改日历，能否在动作前暂停；</li><li><strong>专业边界</strong>：是否把娱乐写成事实，把健康建议写成诊断，把推荐写成保证。</li></ol></div></div>"),
 ("chapter-5","05","第 5 章 资讯整合：把信息流变成每日通知","WB案例","<p>资讯整合最怕两件事：一是信息太多，真正重要的内容被淹没；二是通知太吵，最后所有人都把它当背景噪音。</p><p>WorkBuddy 把多个信息源变成可筛选、可解释、可追踪的通知系统。比如，GitHub 热点项目每日通知、AIHOT 行业日报、论文与技术趋势追踪、公众号和博客监控、新闻与热榜舆情、事实核查与来源补证。</p><p>让用户每天少错过真正值得看的东西。</p><h2 id=\"资讯通知的共同工作流\">资讯通知的共同工作流 </h2><p>无论是 GitHub 项目、AI 新闻、论文、政策还是热榜，稳定的资讯通知都可以拆成同一条链路：先收集，再去重，再筛选，再摘要，最后按人群和场景推送。</p><figure class=\"wb-mermaid\" aria-label=\"流程图\" data-v-dbf03737><pre class=\"wb-mermaid__fallback\" data-v-dbf03737><code data-v-dbf03737>flowchart LR     A[订阅源与检索任务] --&gt; B[抓取与去重]     B --&gt; C[分类与重要性评分]     C --&gt; D[摘要、翻译和影响判断]     D --&gt; E[来源补证与事实核查]     E --&gt; F[生成通知卡片]     F --&gt; G[推送到飞书、微信、邮件或文档]     G --&gt; H[归档与复盘关键词] </code></pre><!----></figure><table tabindex=\"0\"><thead><tr><th>环节</th><th>要解决什么</th><th>常见输出</th></tr></thead><tbody><tr><td>收集</td><td>从新闻、热榜、GitHub、arXiv、RSS、公众号、搜索引擎拉取候选内容。</td><td>候选列表、原始链接、发布时间、来源。</td></tr><tr><td>去重</td><td>同一事件可能被多个来源重复报道。</td><td>合并同源事件，保留首发和权威来源。</td></tr><tr><td>筛选</td><td>不是所有新内容都值得推送。</td><td>重要性评分、相关性评分、风险等级。</td></tr><tr><td>摘要</td><td>把长文章、论文、项目 README 转成可读摘要。</td><td>三句话摘要、影响判断、适用人群。</td></tr><tr><td>核查</td><td>避免把传闻、营销稿、错误信息当事实。</td><td>证据表、可信度、待确认项。</td></tr><tr><td>通知</td><td>用固定格式推送给对应人群。</td><td>飞书卡片、微信群消息、日报文档、邮件摘要。</td></tr></tbody></table><h2 id=\"可用的资讯类-skill\">可用的资讯类 Skill </h2><p><img src=\"images/case5-01.png\" alt=\"\" loading=\"lazy\"></p><p>大致可以分成六类：新闻、AI 行业、开发者趋势、科研论文、内容监控、事实核查与搜索补证。</p><table tabindex=\"0\"><thead><tr><th>Skill / 工具</th><th>适合通知什么</th><th>本章怎么用</th></tr></thead><tbody><tr><td>腾讯新闻</td><td>国内外热点、早晚报、实时资讯、领域新闻。</td><td>适合做管理层早报、行业新闻通知、突发事件提醒。</td></tr><tr><td>AIHOT</td><td>AI 模型、产品、行业、论文动态。</td><td>适合做 AI 行业日报和团队技术雷达。</td></tr><tr><td>GitHub 热门项目</td><td>今日、本周、本月热门项目，支持语言过滤。</td><td>适合给研发团队做每日开源项目推荐。</td></tr><tr><td>GitHub AI 趋势追踪</td><td>GitHub AI 热门项目趋势报告。</td><td>适合做 AI 工程团队每周趋势简报。</td></tr><tr><td>ArXiv 论文追踪</td><td>最新研究论文搜索与总结。</td><td>适合研究、算法和产品策略团队跟踪论文动向。</td></tr><tr><td>新闻摘要</td><td>从 RSS 源获取新闻并生成摘要和语音播报。</td><td>适合固定源日报、行业资讯语音简报。</td></tr><tr><td>博客监控</td><td>监控博客和 RSS 订阅源更新。</td><td>适合关注竞品博客、官方 changelog、技术团队博客。</td></tr><tr><td>wechat-article-search</td><td>搜索公众号文章标题、摘要、发布时间、来源账号和链接。</td><td>适合监控行业 KOL、竞品公众号和爆款选题。</td></tr><tr><td>Twitter 分析</td><td>Twitter 研究与内容情报分析。</td><td>适合跟踪海外 AI、开源、投资和产品讨论。</td></tr><tr><td>多引擎搜索 / Tavily / Exa / Perplexity / 元宝搜索标准版</td><td>多源搜索、深度研究、引用来源补证。</td><td>适合给重要新闻、论文、项目做二次验证。</td></tr><tr><td>jiaozhen-factcheck / 鹅厂辟谣助手</td><td>事实查证、谣言识别、腾讯相关辟谣辅助。</td><td>适合在通知前给争议信息加可信度判断。</td></tr></tbody></table><h2 id=\"github-热点项目每日通知\">GitHub 热点项目每日通知 </h2><p>比如：每天 9 点抓取 GitHub Trending 和 AI 热门项目。按语言、主题、star 增长、最近提交、license 过滤。只推送 Top 5-10 个，并给出“是否值得试用”的判断。</p><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span> 定时每天早上7点返回gthub热门项目，并输出项目大概简介</span></span></code></pre></div><p><img src=\"images/case5-02.png\" alt=\"\" loading=\"lazy\"></p><p><img src=\"images/case5-03.png\" alt=\"\" loading=\"lazy\"></p><h2 id=\"aihot-生成-ai-行业日报\">AIHOT 生成 AI 行业日报 </h2><p>AI 行业信息更新快，AIHOT 可以作为一个现成的信息源。它面向 AI 动态提供精选内容，覆盖模型、产品、行业和论文等方向，并支持 Agent 使用。</p><p>比如：每天固定时间从 AIHOT 拉取 AI 动态。按模型、产品、行业、论文、开源项目、商业化分组。对每条内容做“影响范围、可信度、与本团队相关性”评分。只推送 5-8 条重点，其余进入文档归档。对高影响内容追加二次检索，补充原始链接或官方来源。</p><p>安装aihot skill，</p><div class=\"language-Plain vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">Plain</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>帮我安装这个 skill：https://aihot.virxact.com/aihot-skill/</span></span></code></pre></div><p><img src=\"images/case5-04.png\" alt=\"\" loading=\"lazy\"></p><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>请看一下最近 OpenAI 发布了什么新东西</span></span></code></pre></div><p><img src=\"images/case5-05.png\" alt=\"\" loading=\"lazy\"></p><div class=\"language-Plain vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">Plain</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>总结今日热点新闻，值关注AI大模型方向</span></span></code></pre></div><p><img src=\"images/case5-06.png\" alt=\"\" loading=\"lazy\"></p><table tabindex=\"0\"><thead><tr><th>日报模块</th><th>写什么</th><th>通知对象</th></tr></thead><tbody><tr><td>今日三件大事</td><td>最值得打扰所有人的变化。</td><td>全员或管理层。</td></tr><tr><td>模型与产品</td><td>新模型、新功能、新 API、新价格。</td><td>产品、研发、运营。</td></tr><tr><td>开源项目</td><td>可试用工具、框架、Agent 项目。</td><td>研发团队。</td></tr><tr><td>论文研究</td><td>可能影响技术路线的新方法。</td><td>算法、技术负责人。</td></tr><tr><td>机会与风险</td><td>竞品动作、替代方案、合规变化。</td><td>业务负责人。</td></tr></tbody></table></div></div>"),
 ("chapter-6","06","第 6 章 收藏不是知识管理，能再次用起来才是","WB案例","<h2 id=\"工具都装了-知识还是散的\">工具都装了，知识还是散的 </h2><p>继续向前一步：如果一个人同时使用 WPS、ima、Obsidian、微信收藏、会议记录和本地文件，怎样分工才能避免“每个地方都有一份，但没有一份可信”。</p><h2 id=\"先决定主版本-再连接工具\">先决定主版本，再连接工具 </h2><p>一个稳健的个人知识系统可以有多个入口，但只能有清楚的主版本：</p><table tabindex=\"0\"><thead><tr><th>系统</th><th>推荐角色</th><th>不建议承担</th></tr></thead><tbody><tr><td>WPS / Kdocs</td><td>工作文档、表格、协作笔记和团队知识</td><td>同时充当所有私人原始资料的唯一备份</td></tr><tr><td>ima</td><td>微信生态收集、移动问答和知识库检索</td><td>保存没有来源的二手结论</td></tr><tr><td>Obsidian</td><td>本地 Markdown、双链、专题 Wiki 和长期迁移</td><td>未备份情况下让自动化批量移动或重命名</td></tr><tr><td>微信收藏 / 灵感工具</td><td>低摩擦入口和临时收件箱</td><td>永久归档与结构化检索</td></tr><tr><td>飞书 / 腾讯文档</td><td>团队协作、评论和发布副本</td><td>默认扩大私人资料可见范围</td></tr></tbody></table><h2 id=\"场景一-灵感来了-只记下一句话\">场景一：灵感来了，只记下一句话 </h2><p>灵感最怕两种处理：一种是没来得及记，另一种是 AI 立刻把一句话扩写成一篇看似完整、却已经偏离原意的文章。</p><ul><li><a href=\"https://skillhub.cn/skills/inspiration-hunter-skill\" target=\"_blank\" rel=\"noreferrer\">灵感捕手</a>：自动分类并写入 Markdown 收件箱；</li><li><a href=\"https://skillhub.cn/skills/ima-skills\" target=\"_blank\" rel=\"noreferrer\">ima-skills</a>或 <a href=\"https://skillhub.cn/skills/ima-pro\" target=\"_blank\" rel=\"noreferrer\">ima</a>：移动端记录、知识库读写与检索；</li><li>Obsidian 本地目录作为长期主版本时，可接入后文的 Wiki Skill。</li></ul><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>把下面内容记入“灵感收件箱”，保留我的原话，不扩写、不评价：“AI 工具真正的门槛不是提示词，而是验收结果。”</span></span></code></pre></div><p><img src=\"images/case6-01.png\" alt=\"\" loading=\"lazy\"></p><h2 id=\"场景二-微信收藏很多-真正写作时还是搜不到\">场景二：微信收藏很多，真正写作时还是搜不到 </h2><ul><li><a href=\"https://skillhub.cn/skills/wechat-favorite\" target=\"_blank\" rel=\"noreferrer\">微信收藏知识库</a>：导出、分类，并可选择进入 ima、Obsidian 或 Notion；</li><li><a href=\"https://skillhub.cn/skills/url-to-obsidian\" target=\"_blank\" rel=\"noreferrer\">URL to Obsidian</a>：抓取网页、总结并保存到 Vault；</li><li><a href=\"https://skillhub.cn/skills/wxpublic-fetch\" target=\"_blank\" rel=\"noreferrer\">公众号内容提取</a>：将公众号文章保存为本地 Markdown。</li></ul><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>处理本周微信收藏，只读，不删除原收藏。</span></span></code></pre></div><p><img src=\"images/case6-02.jpg\" alt=\"\" loading=\"lazy\"></p><h2 id=\"场景三-ima-作为移动知识入口\">场景三：ima 作为移动知识入口 </h2><p>ima 的优势不是“问答更聪明”，而是手机收集、知识库读写和微信上下文衔接。使用 <a href=\"https://skillhub.cn/skills/ima-skills\" target=\"_blank\" rel=\"noreferrer\">ima-skills</a> 时，先明确目标知识库和写入规则。</p><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>将我刚选择的 3 份文件放入 ima“WorkBuddy 案例库”的收件箱。</span></span></code></pre></div><p><img src=\"images/case6-03.png\" alt=\"\" loading=\"lazy\"></p><h2 id=\"场景四-obsidian-不是文件夹-而是可维护的-wiki\">场景四：Obsidian 不是文件夹，而是可维护的 Wiki </h2><ul><li><a href=\"https://skillhub.cn/skills/obsidian-core-notes\" target=\"_blank\" rel=\"noreferrer\">Obsidian 资料整理</a>：维护核心笔记、专题综合和目录链接；</li><li><a href=\"https://skillhub.cn/skills/obsidian-memory\" target=\"_blank\" rel=\"noreferrer\">agent + Obsidian 长期记忆</a>：在明确项目边界后读写长期记忆。</li></ul><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>把一篇公众号文章交给 WorkBuddy 解析，再要求放进指定的 Obsidian 素材目录。</span></span></code></pre></div><p>WorkBuddy 能识别文章正文和作者，并生成 Markdown 条目。</p><p><img src=\"images/case6-04.png\" alt=\"\" loading=\"lazy\"></p></div></div>"),
 ("chapter-7","07","第 7 章 会议结束不是终点，工作才刚刚开始","WB案例","<h2 id=\"日常办公为什么总在重复搬运\">日常办公为什么总在重复搬运 </h2><p>很多办公室的一天由同一组动作组成：约会议、找材料、开会、记笔记、发纪要、建待办、追进度、写周报、做汇报。每个动作看似不难，真正消耗精力的是信息不断从聊天、会议、邮件、文档和表格之间流转，而且每流转一次都可能丢掉上下文。</p><figure class=\"wb-mermaid\" aria-label=\"流程图\" data-v-dbf03737><pre class=\"wb-mermaid__fallback\" data-v-dbf03737><code data-v-dbf03737>flowchart LR     A[会前目标与议程] --&gt; B[创建会议与日历邀请]     B --&gt; C[会议录制与转写]     C --&gt; D[事实、决策、分歧和待办]     D --&gt; E[任务系统与会后通知]     D --&gt; F[PRD / 方案 / PPT]     E --&gt; G[日报、周报与进度跟踪]     F --&gt; G     G --&gt; H[项目记忆与下一次会议] </code></pre><!----></figure><h2 id=\"主案例-一次产品评审会-怎样真正推动项目\">主案例：一次产品评审会，怎样真正推动项目 </h2><p>场景设定：产品团队要评审“会议纪要自动生成待办”功能。过去会后由产品经理回听录音、整理纪要，再把行动项逐个录入任务系统，通常要半天，而且参会人对“谁答应了什么”经常理解不同。</p><p>这条协同链不追求无人值守。它在创建会议、读取录制、创建待办和确认 PRD 四处保留人工检查点。</p><h3 id=\"第一步-会前先定义要做出什么决定\">第一步：会前先定义要做出什么决定 </h3><p>没有议程的会议，转写再完整也只是大量对话。会前最重要的不是发链接，而是明确会议类型、要回答的问题和期望产物。</p><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>为“会议纪要自动生成待办”产品评审准备 45 分钟议程。</span></span> <span class=\"line\"><span>参会角色：产品、研发、设计、测试、运营。</span></span> <span class=\"line\"><span>本次必须形成三个决定：首期范围、待办字段、上线验收指标。</span></span> <span class=\"line\"><span></span></span> <span class=\"line\"><span>读取 project/meeting-to-task 中的需求草案和上次决策记录，</span></span> <span class=\"line\"><span>输出：会议目标、会前材料、按分钟议程、每个议题的主持人、</span></span> <span class=\"line\"><span>需要当场决定的问题、可以会后异步处理的问题。</span></span> <span class=\"line\"><span>事实与建议分开；缺少的信息列入会前补充，不自行补造。</span></span></code></pre></div><h3 id=\"第二步-创建腾讯会议-并同步日历\">第二步：创建腾讯会议，并同步日历 </h3><p><a href=\"https://skillhub.cn/skills/tencent-meeting-skill\" target=\"_blank\" rel=\"noreferrer\">腾讯会议 Skill</a>用于会议全生命周期：创建、修改、取消、查询会议，查看参会成员，并在权限允许时获取录制、转写和智能纪要。官方说明要求通过环境变量保存 Token，并提醒使用者遵守企业数据和隐私要求。</p><p>腾讯会议 Skill 不等于通用日历。正确顺序是：先创建会议得到会议号和链接，再通过日历或办公协作连接器创建日程、邀请参会人和预定会议室。</p><p>创建前必须确认的字段</p><table tabindex=\"0\"><thead><tr><th>字段</th><th>示例</th><th>为什么要确认</th></tr></thead><tbody><tr><td>主题</td><td>会议纪要自动生成待办 - 首期评审</td><td>避免会议列表中无法识别</td></tr><tr><td>开始与结束</td><td>7 月 8 日 14:00-14:45</td><td>相对时间容易理解错</td></tr><tr><td>时区</td><td>Asia/Shanghai</td><td>跨地区协作必须明确</td></tr><tr><td>参会人</td><td>产品、研发、设计、测试、运营</td><td>会议权限和责任边界</td></tr><tr><td>周期规则</td><td>单次</td><td>周期会议取消影响更大</td></tr><tr><td>入会与等候室</td><td>企业内可直接入会</td><td>涉及外部人员时需调整</td></tr><tr><td>录制与转写</td><td>会中由主持人确认</td><td>涉及告知、权限和隐私</td></tr></tbody></table><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>使用腾讯会议 Skill 创建一场会议。</span></span> <span class=\"line\"><span>主题：会议纪要自动生成待办 - 首期评审</span></span> <span class=\"line\"><span>时间：2026-07-08 14:00-14:45，时区 Asia/Shanghai，单次会议。</span></span> <span class=\"line\"><span>先返回拟创建信息让我确认；确认后创建会议。</span></span> <span class=\"line\"><span></span></span> <span class=\"line\"><span>创建成功后，把会议号、链接、开始结束时间写入 meeting-brief.md。</span></span> <span class=\"line\"><span>再生成日历邀请草稿，包含议程和会前材料链接；</span></span> <span class=\"line\"><span>不要自行添加参会人、发送邀请或预定会议室，等待我确认名单。</span></span></code></pre></div><p>创建、修改和取消是不同风险等级。取消会议、修改周期规则、扩大参会范围前要展示目标会议和影响范围，不能只凭一句“把下午的会取消”。</p><p>ps：以上提示词可以根据自己的会议修改。</p><h3 id=\"第三步-会后获取录制、转写和会议内容\">第三步：会后获取录制、转写和会议内容 </h3><p>会议结束后，最容易犯的错误是把“有录音”当成“已经有可用信息”。录制可能没有开启，转写可能尚未生成，调用人也可能没有查看权限。</p><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>查询会议号 123 456 789 对应的已结束会议。</span></span> <span class=\"line\"><span>先返回主题、时间和主持人，确认是目标会议后，再查询录制列表。</span></span> <span class=\"line\"><span>如果有权限，获取转写全文、分段信息和智能纪要；</span></span> <span class=\"line\"><span>如果无权限，停止读取并返回所需授权，不尝试绕过。</span></span> <span class=\"line\"><span>下载或保存前说明文件类型、大小、目标目录和保留期限。</span></span></code></pre></div><p><img src=\"images/case7-01.png\" alt=\"\" loading=\"lazy\"></p><p>在这个过程中需要连接腾讯会议连接器，按照提示在连接管理器中找到“腾讯会议”，并授权连接就行。</p><p><img src=\"images/case7-02.png\" alt=\"\" loading=\"lazy\"></p><p>腾讯会议能力通常需要先把 9 位会议号转换成内部 <code>meeting_id</code>，再查询详情、录制和转写。这个过程由 Skill 完成，不需手工转换，但保留会议号、会议 ID、录制 ID、查询时间和权限状态，方便排错。</p><p><img src=\"images/case7-03.png\" alt=\"\" loading=\"lazy\"></p><p>录制与转写的边界</p><ul><li>会前或会中明确告知录制和转写安排；</li><li>不把录制链接转发给没有权限的人；</li><li>不因获取失败而把聊天截图或未经同意的录音当替代来源；</li><li>转写是机器识别结果，专有名词、数字、责任人和否定句必须回听核对；</li><li>企业会议遵守所在组织的保留期限、数据分类和合规要求。</li></ul><h3 id=\"第四步-从转写生成可执行会议纪要\">第四步：从转写生成可执行会议纪要 </h3><p>一份纪要，包含五类信息</p><table tabindex=\"0\"><thead><tr><th>类型</th><th>例子</th><th>处理方式</th></tr></thead><tbody><tr><td>背景事实</td><td>当前纪要平均需 40 分钟整理</td><td>附来源或发言时间</td></tr><tr><td>已确认决定</td><td>首期只支持会后生成待办草稿</td><td>记录决定人和时间</td></tr><tr><td>行动项</td><td>产品补充字段映射表</td><td>负责人、截止日期、验收物</td></tr><tr><td>未决问题</td><td>是否支持跨项目复制待办</td><td>进入下次决策，不伪装成结论</td></tr><tr><td>讨论建议</td><td>研发提出先做异步队列</td><td>标记为建议，不写成承诺</td></tr></tbody></table><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>生成会议纪要，不得只依赖平台智能摘要；关键数字、责任人和否定表达回到转写核验。</span></span> <span class=\"line\"><span></span></span> <span class=\"line\"><span>输出：</span></span> <span class=\"line\"><span>1. 会议基本信息；</span></span> <span class=\"line\"><span>2. 三句话结论；</span></span> <span class=\"line\"><span>3. 按议题整理的讨论摘要；</span></span> <span class=\"line\"><span>4. 决策表：决定、理由、决定人、时间戳；</span></span> <span class=\"line\"><span>5. 行动项表：任务、负责人、截止日期、交付物、依赖；</span></span> <span class=\"line\"><span>6. 未决问题与下次确认时间；</span></span> <span class=\"line\"><span>7. 转写中无法确认的人名、数字和术语。</span></span> <span class=\"line\"><span></span></span> <span class=\"line\"><span>没有明确负责人的任务写“待认领”，没有明确日期写“待确认”，</span></span> <span class=\"line\"><span>不得根据语气猜测负责人或截止时间。</span></span></code></pre></div><p><img src=\"images/case7-04.png\" alt=\"\" loading=\"lazy\"></p><h3 id=\"第五步-纪要里的待办-不能直接静默写入任务系统\">第五步：纪要里的待办，不能直接静默写入任务系统 </h3><p>为什么要两步确认</p><p>会中发言和正式任务不是同一件事。把“可以看看”直接变成分派给某人的任务，会制造额外管理成本。</p><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>读取 minutes-approved.md 中的行动项，只生成待办导入预览。</span></span> <span class=\"line\"><span>每条显示：标题、描述、负责人、截止日期、优先级、验收物、来源会议。</span></span> <span class=\"line\"><span>负责人或日期缺失的条目进入“待补充”，不要创建。</span></span> <span class=\"line\"><span>先按负责人分组让我确认；确认后再写入指定任务清单。</span></span> <span class=\"line\"><span>写入完成后返回成功、失败、跳过和重复四个清单，不发送催办消息。</span></span></code></pre></div><p><img src=\"images/case7-05.png\" alt=\"\" loading=\"lazy\"></p><p>这里由于我这次的会议主要是为了演示用，所以待办项的相关责任人都是待确认状态。</p><p>稳定流程是：纪要草稿 → 参会人确认 → 待办预览 → 人工补齐责任与日期 → 写入任务系统 → 返回任务链接。重复运行时使用“会议 ID + 行动项序号”作为幂等键，避免创建重复任务。</p><h3 id=\"第六步-会后通知和跟踪\">第六步：会后通知和跟踪 </h3><p>会议后可以生成邮件或群消息草稿，但发送前必须确认对象和可见范围：</p><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>根据会议记录生成两份会后通知草稿：</span></span> <span class=\"line\"><span>A. 发给全体参会人：结论、行动项、未决问题和纪要链接；</span></span> <span class=\"line\"><span>B. 发给管理层：三句话结论、关键风险和需要支持的决定。</span></span> <span class=\"line\"><span>不要包含录制下载地址、内部争议原话或未确认个人责任。</span></span> <span class=\"line\"><span>只生成草稿，不发送。</span></span></code></pre></div><p><img src=\"images/case7-06.png\" alt=\"\" loading=\"lazy\"></p><p>批量重命名要保留映射表；同名冲突不覆盖；合同、财务和人事文件按组织规则处理，不能只按文件名猜分类。</p><h2 id=\"会后延伸-把会议纪要变成汇报-ppt\">会后延伸：把会议纪要变成汇报 PPT </h2><p>先确定汇报对象和结论，再设计页面：</p><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>根据会议纪要生成 8 页项目汇报 PPT。</span></span> <span class=\"line\"><span>受众是管理层，目标是确认首期范围和资源缺口。</span></span> <span class=\"line\"><span>页面：结论、背景、用户问题、已确认范围、进度、风险、资源请求、下一步。</span></span> <span class=\"line\"><span>每页只表达一个结论；数字来自状态表，决定来自纪要；</span></span> <span class=\"line\"><span>不使用无法解释的装饰图表。先返回页级大纲和证据映射，确认后再生成 PPT。</span></span></code></pre></div><p><img src=\"images/case7-07.png\" alt=\"\" loading=\"lazy\"></p><h2 id=\"一套基础办公-skill-栈\">一套基础办公 Skill 栈 </h2><table tabindex=\"0\"><thead><tr><th>任务层</th><th>可选能力</th><th>默认安全动作</th></tr></thead><tbody><tr><td>会议</td><td>腾讯会议 Skill、日历连接器</td><td>创建前预览，取消前二次确认</td></tr><tr><td>内容</td><td>录制、转写、会议纪要模板</td><td>保留来源和时间戳</td></tr><tr><td>协作</td><td>任务、邮件、IM、腾讯文档/WPS</td><td>先生成草稿或导入预览</td></tr><tr><td>产品</td><td>PRD 模板、自定义产品经理 Skill</td><td>只使用确认需求，保留未决问题</td></tr><tr><td>文件</td><td>DOCX、PDF、OCR、文件整理</td><td>复制优先，不覆盖、不删除</td></tr><tr><td>数据</td><td>Excel、公式、图表、数据分析</td><td>先对账，再分析</td></tr><tr><td>汇报</td><td>PPT、图表和品牌模板</td><td>先页级大纲和证据映射</td></tr><tr><td>自动化</td><td>日报、周报、提醒和归档</td><td>小范围试运行，失败可接管</td></tr></tbody></table><p>不要一开始安装十几个 Skill。先选择一个每周都会发生、输入稳定、结果容易验收的任务，例如会议纪要到待办；连续跑通后，再把 PRD、周报和汇报接到同一条链上。</p></div></div>"),
 ("chapter-8","08","第 8 章 把投资分析变成你的日常","WB案例","<p>投资本身就是一件<strong>高度信息密集、强结构化、又极度依赖判断</strong>的事：读不完的财报、理不清的行业、吵不停的多空。而整理碎片信息、拆解复杂材料、把思考过程摆到台面上，恰好是 AI 擅长的。</p><p><strong>在一次完整的股票研究里，AI 到底能替你做掉哪些低质量的重复劳动，把精力还给判断本身。</strong></p><h2 id=\"先想清楚-ai-在投资里该干什么\">先想清楚：AI 在投资里该干什么 </h2><p>多数人对“AI 炒股”的想象是让它预测涨跌。但从真实的高频用法看，绝大多数有价值的提示词其实只集中在四类事上：</p><ul><li>读不完的财报，帮我总结；</li><li>行业太复杂，帮我把逻辑理一遍；</li><li>市场吵得太凶，帮我把多空观点放进一张表；</li><li>我怕自己自嗨，帮我找反证。</li></ul><p>这四类都不是“预测涨跌”，而是<strong>减少低质量思考的时间</strong>。AI 在投资里最合理的位置，是一个不知疲倦、不带情绪、随叫随到的研究助理——它负责把事实底座打牢，把判断留给你。</p><p>和办公三件套一样，动手前先用五个问题给这次研究定标。很多“AI 分析得不好”，根源不是模型不会分析，而是人没把研究目标说清楚。</p><table tabindex=\"0\"><thead><tr><th>问题</th><th>要说清什么</th><th>示例</th></tr></thead><tbody><tr><td>目标</td><td>这次研究要支撑什么决定</td><td>判断是否把某只票纳入观察池，还是决定当下加减仓。</td></tr><tr><td>标的</td><td>具体是哪家公司、哪个行业</td><td>天孚通信（300394），光通信 / CPO 板块。</td></tr><tr><td>材料</td><td>哪些是事实来源，哪些只是参考</td><td>年报、三季报、券商研报是事实来源；股吧观点只作情绪参考。</td></tr><tr><td>深度</td><td>只要事实梳理，还是要到估值和多空推演</td><td>先做事实底座（Prompt 1-3），再上尽调级 DeepResearch（Prompt 8）。</td></tr><tr><td>验收</td><td>怎么判断结果可用</td><td>每个判断都能追到数据来源，事实与观点分开标注。</td></tr></tbody></table><h2 id=\"先选对工具-金融场景的-skill-组合\">先选对工具：金融场景的 Skill 组合 </h2><p>在进入提示词之前，先认识本章会用到的几个 Skill。它们分工不同，可以单用，也可以像流水线一样串起来。</p><table tabindex=\"0\"><thead><tr><th>Skill 名称</th><th>适合处理</th><th>本章怎么用</th><th>注意点</th></tr></thead><tbody><tr><td><code>stock-advisor</code></td><td>单只股票的端到端分析</td><td>上传截图或给出代码，自动跑完技术面、基本面、交叉验证、私董会、排版</td><td>本章主线，第三、四节详解</td></tr><tr><td><code>a-share-analyst</code></td><td>A 股日常行情与选股</td><td>实时行情、技术指标、量化选股、每日报告</td><td>偏日常盯盘与批量筛选</td></tr><tr><td><code>financial-expert</code></td><td>金融数据查询与筛选</td><td>选股、基金筛选、财务指标、宏观 / 行业时序、券商研报检索</td><td>依赖数据源 MCP，需先配置</td></tr><tr><td><code>peers-advisory-group</code></td><td>多视角决策讨论</td><td>四位“幕僚”围绕一个议题交叉辩论</td><td>被 <code>stock-advisor</code> 作为决策模块调用</td></tr></tbody></table><p>一个实用的搭配思路是：<strong>日常盯盘和批量选股用 <code>a-share-analyst</code> 与 <code>financial-expert</code>；要对一只票下深功夫、出一份完整报告，用 <code>stock-advisor</code>；需要跳出单一视角、逼自己看反面时，叫上 <code>peers-advisory-group</code>。</strong></p><h2 id=\"从查资料到下判断-一套可复用的研究提示词链路\">从查资料到下判断：一套可复用的研究提示词链路 </h2><p>这一节是纯提示词。它们按“<strong>最简单 → 相对复杂</strong>”排列，覆盖了从“查资料”到“下判断”的完整链路。你不必每条都用——先用前三条建立事实底座，需要深挖时再往后走。第 8 条是把前面所有环节压进一个框架的“全家桶”，也是日常在 ChatGPT、Gemini、豆包、千问的 DeepResearch 里最常用的一条。</p><blockquote><p>每条提示词的用法统一是：把方括号 <code>【】</code> 里的占位换成你的标的，粘贴运行即可。</p></blockquote><h3 id=\"prompt-1-最基础-给公司建一个“事实底座”\">Prompt 1｜最基础：给公司建一个“事实底座” </h3><p><strong>解决的场景</strong>：刚接触一家公司，先别急着判断，先搞清楚它到底是干什么的。很多错误判断，从第一步认错了业务就开始了——你以为它靠 A 赚钱，结果利润主要来自 B。这一步的价值，是<strong>压缩你“搞清楚事实”的时间成本</strong>。</p><div class=\"language-markdown vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">markdown</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">请帮我系统梳理【XXX 公司】的基础情况，输出结构化总结，包括：</span></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">1）核心业务与主要产品线</span></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">2）收入与利润来源构成</span></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">3）主要客户与应用场景</span></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">4）公司在产业链中的位置</span></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">5）近几年最重要的战略变化</span></span> <span class=\"line\"></span> <span class=\"line\"><span style=\"--shiki-light:#005CC5;--shiki-light-font-weight:bold;--shiki-dark:#79B8FF;--shiki-dark-font-weight:bold;\">## 要求：</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 只使用可核实的信息</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 每一部分用 3–5 条要点说明</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 不做投资建议，只做事实整理</span></span></code></pre></div><h3 id=\"prompt-2-行业视角-这是不是一个“好行业”\">Prompt 2｜行业视角：这是不是一个“好行业” </h3><p><strong>解决的场景</strong>：股票研究里一个常被低估的问题——你选的往往不是公司，而是行业。AI 很适合做行业的“第一性梳理”。但行业拐点、价格见底这种问题，别指望它给答案。</p><div class=\"language-markdown vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">markdown</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">请从行业研究的角度，分析【&lt;XXX公司&gt;】所在的【&lt;XXX行业&gt;】：</span></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">1）行业所处的周期阶段（复苏/扩张/衰退/萧条）</span></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">2）供需关系与主要驱动因素</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\"> -</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 产能、开工率、库存、订单/交付周期</span></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">3）价格变化机制与历史波动</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\"> -</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 产品价格指数/价差/成本传导</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\"> -</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 资本开支：Capex趋势、扩产项目、行业新增产能</span></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">4）行业集中度与竞争格局</span></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">5）影响行业的关键外部变量（政策、技术、宏观）</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\"> -</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 政策与外部变量：利率、汇率、监管、补贴、贸易限制</span></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">请明确指出：哪些是长期结构性因素，哪些是短期波动因素。输出周期阶段判断 + 关键证据图表清单 + 领先指标(3个)与滞后指标(3个)。</span></span></code></pre></div><h3 id=\"prompt-3-业务拆解-钱到底是怎么赚来的\">Prompt 3｜业务拆解：钱到底是怎么赚来的 </h3><p><strong>解决的场景</strong>：从“看公司”到“看生意”的关键一步。很多“看起来很美”的公司，核心利润来源其实很脆弱。<strong>混杂型公司</strong>（主业 A、利润却来自 B）尤其适合让 AI 帮你看清楚。</p><div class=\"language-markdown vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">markdown</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">请你以【价值投资 / 基本面研究】视角，对【XXX 公司】进行&quot;业务拆解&quot;，目标是回答一个核心问题：</span></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">👉 这家公司【真正、长期】是靠什么赚钱的？</span></span> <span class=\"line\"></span> <span class=\"line\"><span style=\"--shiki-light:#005CC5;--shiki-light-font-weight:bold;--shiki-dark:#79B8FF;--shiki-dark-font-weight:bold;\">## 要求</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 仅基于可验证信息（年报、招股书、定期公告、投资者交流纪要、权威行业报告等）</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 明确区分【事实】与【判断】，所有判断必须给出证据或逻辑链</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 输出为 Markdown 结构化报告</span></span> <span class=\"line\"></span> <span class=\"line\"><span style=\"--shiki-light:#005CC5;--shiki-light-font-weight:bold;--shiki-dark:#79B8FF;--shiki-dark-font-weight:bold;\">## 必答结构</span></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">一、公司&quot;赚钱方式&quot;的一句话结论</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 用不超过 50 字，概括公司最核心的赚钱逻辑（卖什么 → 卖给谁 → 为什么能赚钱）</span></span> <span class=\"line\"></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">二、业务结构全拆解（必须量化）</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">1.</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 业务板块拆分</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">   -</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 列出所有核心业务 / 产品线 / 服务线</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">   -</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 对每一块给出：收入占比、毛利率、增长趋势（近 3–5 年）</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">2.</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 利润来源判断</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">   -</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 哪些业务&quot;贡献了大部分利润&quot;</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">   -</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 哪些业务&quot;收入大但不赚钱 / 甚至亏钱&quot;</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">   -</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 是否存在【主业≠利润核心】的情况？（如：主业A，利润来自B）</span></span> <span class=\"line\"></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">三、赚钱机制拆解（Business Engine）</span></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">对核心业务逐条回答：</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 钱是怎么收进来的？（一次性/订阅/持续复购/项目制）</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 成本主要花在哪？（原材料、人力、渠道、研发、营销）</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 毛利率由什么决定？是结构性优势还是周期红利？</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 是否具备规模效应？规模扩大后，哪一项成本会被摊薄？</span></span> <span class=\"line\"></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">四、客户、渠道与定价权</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 核心客户是谁？是否集中？（Top5/Top10 客户占比）</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 销售渠道结构（直销 / 经销 / 平台 / 政府 / 大客户）</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 是否具备定价权？历史是否成功提价？证据是什么？</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 客户更换供应商的成本高不高？为什么？</span></span> <span class=\"line\"></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">五、子公司 / 联营公司 / 非经常性业务</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 列出重要子公司、联营公司及其业务性质</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 明确哪些利润来自：</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">  -</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 可持续经营</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">  -</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 周期波动</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">  -</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 投资收益 / 政策补贴 / 资产处置</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 判断这些&quot;非主营利润&quot;对长期估值逻辑的影响（正面 / 负面 / 干扰）</span></span> <span class=\"line\"></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">六、商业模式的&quot;稳定性与脆弱点&quot;</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 哪些假设一旦被破坏，赚钱逻辑就会失效？</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 最容易被竞争 / 技术 / 政策冲击的环节在哪里？</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 用 3–5 条&quot;关键监控指标&quot;总结如何持续验证这门生意是否还成立</span></span> <span class=\"line\"></span> <span class=\"line\"><span style=\"--shiki-light:#005CC5;--shiki-light-font-weight:bold;--shiki-dark:#79B8FF;--shiki-dark-font-weight:bold;\">## 最终输出</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 一句话商业本质总结</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 业务结构表（收入 / 利润 / 毛利率）</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 赚钱机制逻辑链（文字 + 列点）</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 对长期投资者最重要的 3 个判断结论</span></span></code></pre></div><h3 id=\"prompt-4-财务质量-这家公司赚的钱干不干净\">Prompt 4｜财务质量：这家公司赚的钱干不干净 </h3><p><strong>解决的场景</strong>：财务调研指标很多，这里给一个通用格式。核心是强制做“利润 vs 现金流”的交叉验证——账面利润漂亮，现金流跟不上，往往是第一个预警信号。</p><div class=\"language-markdown vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">markdown</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">请分析【&lt;公司&gt;】近几年的财务质量：</span></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">1）收入、利润与经营现金流的匹配情况</span></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">2）应收账款、存货、合同资产变化</span></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">3）非经常性损益对利润的影响</span></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">4）是否存在一次性项目或会计口径变化</span></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">5）可能需要重点关注的财务风险点</span></span> <span class=\"line\"></span> <span class=\"line\"><span style=\"--shiki-light:#005CC5;--shiki-light-font-weight:bold;--shiki-dark:#79B8FF;--shiki-dark-font-weight:bold;\">## 研究原则</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 不预测股价，只判断财务&quot;质量&quot;</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 强制进行&quot;利润 vs 现金流&quot;的交叉验证</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 对所有异常必须给出解释假设与验证路径</span></span> <span class=\"line\"></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">请重点指出：哪些指标值得持续跟踪。</span></span></code></pre></div><h3 id=\"prompt-5-股权与治理-老板和你是不是一条船上的\">Prompt 5｜股权与治理：老板和你是不是一条船上的 </h3><p><strong>解决的场景</strong>：生意好 + 治理差 = 高波动风险资产。股权质押、减持、关联交易、激励条款，这些“筹码面”的信息很分散，适合让 AI 一次性梳理成时间表和风险雷达。</p><div class=\"language-markdown vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">markdown</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">1、梳理【&lt;公司&gt;】股权结构与关键股东：</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 实控人、控股股东、董事会结构</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 股权质押比例与变化、减持计划、潜在控制权变更风险</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 关联交易、同业竞争、资金占用风险</span></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">输出：治理结构图（文字版即可）+ 风险雷达(高/中/低) + 需要跟踪的公告清单。</span></span> <span class=\"line\"></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">2、请建立【&lt;公司&gt;】未来&lt;12个月&gt;的&quot;筹码事件时间表&quot;：限售解禁、员工持股解锁、定增/配股、回购进度。</span></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">对每个事件给出：潜在抛压/承接能力判断、对估值中枢的影响路径、历史上类似事件的股价反应统计（如能找到）。</span></span> <span class=\"line\"></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">3、分析【&lt;公司&gt;】管理层薪酬与股权激励：</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 激励指标是否容易&quot;做账达成&quot;？（收入/利润/现金流/ROIC）</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 目标难度与行业对比</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 是否存在短期行为激励（冲收入、降研发等）</span></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">输出：同向性结论 + 关键条款摘录 + 改进建议。</span></span></code></pre></div><h3 id=\"prompt-6-市场分歧-多空到底在吵什么\">Prompt 6｜市场分歧：多空到底在吵什么 </h3><p><strong>解决的场景</strong>：多空双方的观点最有信息量。这一步不是告诉你该信谁，而是帮你把分歧摊平，看清楚<strong>未来该盯哪些数据来验证</strong>。</p><div class=\"language-markdown vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">markdown</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">请整理市场对【XXX 公司】的主要分歧点：</span></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">1）多方核心逻辑</span></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">2）空方核心逻辑</span></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">3）各自最重要的论据</span></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">4）哪些分歧可以被未来数据验证</span></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">5）关键验证节点是什么</span></span> <span class=\"line\"></span> <span class=\"line\"><span style=\"--shiki-light:#005CC5;--shiki-light-font-weight:bold;--shiki-dark:#79B8FF;--shiki-dark-font-weight:bold;\">## 分析要求</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 不得站队</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 不给投资建议</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 不使用情绪化或立场性语言</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 所有判断必须可被未来数据或事件验证</span></span></code></pre></div><h3 id=\"prompt-7-估值与护城河-市场在押什么假设\">Prompt 7｜估值与护城河：市场在押什么假设 </h3><p><strong>解决的场景</strong>：护城河和估值，是价值投资绕不开的两块。下面两条一条评护城河强度，一条搭 DCF 反推市场隐含预期。</p><div class=\"language-markdown vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">markdown</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">以价值投资视角分析【&lt;公司&gt;】的护城河，必须引用公司披露/权威来源。</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">1)</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 定价权：过去&lt;5-10年&gt;毛利率/提价能力/成本转嫁证据？</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">2)</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 转换成本：客户更换供应商的成本是什么（系统、流程、合规、生态）？</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">3)</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 网络效应/规模效应：规模如何降低单位成本或提升体验？</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">4)</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 无形资产：品牌、专利、牌照、数据、渠道壁垒的可验证证据？</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">5)</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 竞争反应：主要对手如何攻击，公司如何防守（历史战役）？</span></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">输出：护城河强度评分(0-5)+证据表+最可能被侵蚀的点与监控指标。</span></span></code></pre></div><div class=\"language-markdown vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">markdown</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">请为【&lt;公司&gt;】构建 DCF 估值（允许使用公开财务数据，必须引用来源）：</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 明确WACC/折现率假设与依据</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 预测5-10年自由现金流：收入、利润率、再投资率</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 给出敏感性分析表（折现率×永续增长率 或 折现率×利润率）</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 反推：当前市值隐含的收入增速/利润率路径</span></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">输出：估值区间 + 关键假设清单 + 最容易错的2个假设及验证方案。</span></span></code></pre></div><h3 id=\"prompt-8-全家桶-一份尽调级-deepresearch\">Prompt 8｜全家桶：一份尽调级 DeepResearch </h3><p><strong>解决的场景</strong>：这是把前七步的逻辑压进同一个框架的“投资者尽职调查报告”。它强制区分事实与判断、强制交叉验证、强制推演空方逻辑与黑天鹅——用来对抗人最容易犯的“确认偏误”。这条在各家 AI 的 DeepResearch 模式里都很好用。</p><div class=\"language-markdown vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">markdown</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">我需要你帮我完成一份投资者尽职调查报告。目标是对标的 </span><span style=\"--shiki-light:#005CC5;--shiki-dark:#79B8FF;\">`&lt;股票名称/代码&gt;`</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 进行全方位的商业模式、财务质量、行业周期及估值逻辑推演。</span></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">请严格按照以下逻辑框架进行推演。</span></span> <span class=\"line\"></span> <span class=\"line\"><span style=\"--shiki-light:#005CC5;--shiki-light-font-weight:bold;--shiki-dark:#79B8FF;--shiki-dark-font-weight:bold;\">## Constraints &amp; Standards (研究原则)</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">1.</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 数据时效性与跨度：财务数据需涵盖</span><span style=\"--shiki-light:#24292E;--shiki-light-font-weight:bold;--shiki-dark:#E1E4E8;--shiki-dark-font-weight:bold;\">**过去 3-5 年**</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">的趋势（CAGR），估值分位需回溯</span><span style=\"--shiki-light:#24292E;--shiki-light-font-weight:bold;--shiki-dark:#E1E4E8;--shiki-dark-font-weight:bold;\">**过去 5-10 年**</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">的历史区间。</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">2.</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 事实底座优先：区分【事实 Fact】与【判断 Opinion】。所有判断必须基于可验证的数据（年报、招股书、监管问询函）。</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">3.</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 双重验证：必须进行&quot;利润 vs 现金流&quot;的交叉验证，以及&quot;公司 vs 同行&quot;的对比验证。</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">4.</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 反直觉思考：必须包含&quot;空方逻辑&quot;与&quot;黑天鹅风险&quot;推演，避免确认偏误。</span></span> <span class=\"line\"></span> <span class=\"line\"><span style=\"--shiki-light:#005CC5;--shiki-light-font-weight:bold;--shiki-dark:#79B8FF;--shiki-dark-font-weight:bold;\">## Research Context (用户输入)</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-light-font-weight:bold;--shiki-dark:#E1E4E8;--shiki-dark-font-weight:bold;\"> **研究标的**</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">：[</span><span style=\"--shiki-light:#032F62;--shiki-light-text-decoration:underline;--shiki-dark:#DBEDFF;--shiki-dark-text-decoration:underline;\">在此输入股票名称/代码</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">]</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-light-font-weight:bold;--shiki-dark:#E1E4E8;--shiki-dark-font-weight:bold;\"> **投资风格**</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">：[如：价值投资 / 成长接力 / 困境反转]</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">-</span><span style=\"--shiki-light:#24292E;--shiki-light-font-weight:bold;--shiki-dark:#E1E4E8;--shiki-dark-font-weight:bold;\"> **持有周期**</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">：[如：中长线 1-3 年]</span></span> <span class=\"line\"></span> <span class=\"line\"><span style=\"--shiki-light:#005CC5;--shiki-light-font-weight:bold;--shiki-dark:#79B8FF;--shiki-dark-font-weight:bold;\">## Workflow</span></span> <span class=\"line\"><span style=\"--shiki-light:#005CC5;--shiki-light-font-weight:bold;--shiki-dark:#79B8FF;--shiki-dark-font-weight:bold;\">### Phase 1: 商业模式与护城河拆解 (Business Engine &amp; Moat)</span></span> <span class=\"line\"><span style=\"--shiki-light:#22863A;--shiki-dark:#85E89D;\">&gt; 核心任务：搞清楚它真正靠什么赚钱，剔除噪音，看清本质。</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">1.</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 业务透视与提纯：</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">    -</span><span style=\"--shiki-light:#24292E;--shiki-light-font-weight:bold;--shiki-dark:#E1E4E8;--shiki-dark-font-weight:bold;\"> **拆解营收/利润结构**</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">：核心业务是什么？是否存在&quot;主业赚吆喝，副业（投资/补贴）赚利润&quot;的现象？</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">    -</span><span style=\"--shiki-light:#24292E;--shiki-light-font-weight:bold;--shiki-dark:#E1E4E8;--shiki-dark-font-weight:bold;\"> **子公司/联营公司穿透**</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">：深挖主要子公司和联营公司的实际贡献，</span><span style=\"--shiki-light:#24292E;--shiki-light-font-weight:bold;--shiki-dark:#E1E4E8;--shiki-dark-font-weight:bold;\">**剔除噪音**</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">，明确指出哪些业务是拖累，哪些是隐形金矿。</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">2.</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 护城河判定：</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">    -</span><span style=\"--shiki-light:#24292E;--shiki-light-font-weight:bold;--shiki-dark:#E1E4E8;--shiki-dark-font-weight:bold;\"> **定价权**</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">：是否有提价能力？（证据：毛利率是否随成本波动？还是能转嫁成本？）</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">    -</span><span style=\"--shiki-light:#24292E;--shiki-light-font-weight:bold;--shiki-dark:#E1E4E8;--shiki-dark-font-weight:bold;\"> **核心壁垒**</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">：是品牌溢价、极高的转换成本、网络效应，还是单纯的低成本优势？</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">    -</span><span style=\"--shiki-light:#24292E;--shiki-light-font-weight:bold;--shiki-dark:#E1E4E8;--shiki-dark-font-weight:bold;\"> **行业天花板**</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">：该行业 TAM 有多大？当前市场份额分布如何？公司是否触及增长天花板？</span></span> <span class=\"line\"></span> <span class=\"line\"><span style=\"--shiki-light:#005CC5;--shiki-light-font-weight:bold;--shiki-dark:#79B8FF;--shiki-dark-font-weight:bold;\">### Phase 2: 行业周期与供需格局 (Industry Context)</span></span> <span class=\"line\"><span style=\"--shiki-light:#22863A;--shiki-dark:#85E89D;\">&gt; 核心任务：判断是顺风还是逆风，是红海还是蓝海。</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">1.</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 周期定位：行业目前处于哪个阶段（复苏/过热/滞胀/衰退/萧条）？请引用库存水平、开工率、Capex（资本开支）趋势作为证据。</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">2.</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 供需剪刀差：寻找&quot;领先指标&quot;与&quot;滞后指标&quot;。未来 1-2 年行业是否有大规模新增产能投放？</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">3.</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 竞争格局变化：行业集中度（CR5）是在提升还是分散？主要竞争对手近期有什么大动作（价格战/技术突破）？</span></span> <span class=\"line\"></span> <span class=\"line\"><span style=\"--shiki-light:#005CC5;--shiki-light-font-weight:bold;--shiki-dark:#79B8FF;--shiki-dark-font-weight:bold;\">### Phase 3: 财务健康度与质量扫雷 (Financial Health)</span></span> <span class=\"line\"><span style=\"--shiki-light:#22863A;--shiki-dark:#85E89D;\">&gt; 核心任务：这笔钱赚得干不干净？增长是否有质量？</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">1.</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 核心指标趋势：</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">    -</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 计算过去 3-5 年的 </span><span style=\"--shiki-light:#24292E;--shiki-light-font-weight:bold;--shiki-dark:#E1E4E8;--shiki-dark-font-weight:bold;\">**营收 CAGR**</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 和 </span><span style=\"--shiki-light:#24292E;--shiki-light-font-weight:bold;--shiki-dark:#E1E4E8;--shiki-dark-font-weight:bold;\">**净利润 CAGR**</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">，判断增长的持续性。</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">    -</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 分析 </span><span style=\"--shiki-light:#24292E;--shiki-light-font-weight:bold;--shiki-dark:#E1E4E8;--shiki-dark-font-weight:bold;\">**ROE（净资产收益率）**</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 的驱动因素（杜邦分析：是靠加杠杆，还是靠周转快，还是利润高？）。</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">    -</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 绘制 </span><span style=\"--shiki-light:#24292E;--shiki-light-font-weight:bold;--shiki-dark:#E1E4E8;--shiki-dark-font-weight:bold;\">**毛利率与净利率**</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 趋势图，判断盈利能力的稳定性。</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">2.</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 异常排查（扫雷）：</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">    -</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 周转率警报：存货周转率、应收账款周转天数是否有恶化（变长）趋势？</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">    -</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 含金量测试：经营性现金流净额 / 净利润是否匹配？（长期 &lt;1 则为危险信号）。</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">    -</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 非经常性损益：剔除一次性收益后，扣非净利润是否依然健康？</span></span> <span class=\"line\"></span> <span class=\"line\"><span style=\"--shiki-light:#005CC5;--shiki-light-font-weight:bold;--shiki-dark:#79B8FF;--shiki-dark-font-weight:bold;\">### Phase 4: 治理结构与资本配置 (Governance &amp; Allocation)</span></span> <span class=\"line\"><span style=\"--shiki-light:#22863A;--shiki-dark:#85E89D;\">&gt; 核心任务：管理层是股东的伙伴，还是收割者？</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">1.</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 资本运作回顾：</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">    -</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 盘点近 2 年的增发、回购、股权激励或重大并购。这些动作对中小股东是</span><span style=\"--shiki-light:#24292E;--shiki-light-font-weight:bold;--shiki-dark:#E1E4E8;--shiki-dark-font-weight:bold;\">**增厚 EPS**</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 还是</span><span style=\"--shiki-light:#24292E;--shiki-light-font-weight:bold;--shiki-dark:#E1E4E8;--shiki-dark-font-weight:bold;\">**稀释权益**</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">？</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">2.</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 股权与筹码：</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">    -</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 实控人持股比例？是否有</span><span style=\"--shiki-light:#24292E;--shiki-light-font-weight:bold;--shiki-dark:#E1E4E8;--shiki-dark-font-weight:bold;\">**高比例质押**</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">风险？是否有重要股东（大基金/高管）持续减持？</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">3.</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 管理层画像：</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">    -</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 他们的言行是否一致？</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">    -</span><span style=\"--shiki-light:#24292E;--shiki-light-font-weight:bold;--shiki-dark:#E1E4E8;--shiki-dark-font-weight:bold;\"> **资本配置能力**</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">：历史上赚到的钱投向了哪里（瞎投资/扩产/分红/回购）？回报率（ROIC）如何？</span></span> <span class=\"line\"></span> <span class=\"line\"><span style=\"--shiki-light:#005CC5;--shiki-light-font-weight:bold;--shiki-dark:#79B8FF;--shiki-dark-font-weight:bold;\">### Phase 5: 估值逻辑与风险反脆弱 (Valuation &amp; Risk)</span></span> <span class=\"line\"><span style=\"--shiki-light:#22863A;--shiki-dark:#85E89D;\">&gt; 核心任务：价格是否包含了过高的预期？</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">1.</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 相对估值（纵向+横向）：</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">    -</span><span style=\"--shiki-light:#24292E;--shiki-light-font-weight:bold;--shiki-dark:#E1E4E8;--shiki-dark-font-weight:bold;\"> **历史分位**</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">：当前 PE/PB/PS 处于历史（过去 5-10 年）的什么分位点？</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">    -</span><span style=\"--shiki-light:#24292E;--shiki-light-font-weight:bold;--shiki-dark:#E1E4E8;--shiki-dark-font-weight:bold;\"> **同行对比**</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">：与同行业主要竞争对手相比，估值是溢价还是折价？理由充分吗？</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">2.</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 绝对估值（反向思维）：</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">    -</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 不仅仅做预测，请进行</span><span style=\"--shiki-light:#24292E;--shiki-light-font-weight:bold;--shiki-dark:#E1E4E8;--shiki-dark-font-weight:bold;\">**反向 DCF 推演**</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">：当前股价隐含了未来 3-5 年多少的净利润增速？这个隐含预期是否过于乐观？</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">3.</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 风险与空方逻辑：</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">    -</span><span style=\"--shiki-light:#24292E;--shiki-light-font-weight:bold;--shiki-dark:#E1E4E8;--shiki-dark-font-weight:bold;\"> **空方视角**</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">：全网搜索看空该股票的核心理由（做空报告/负面舆情）。</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">    -</span><span style=\"--shiki-light:#24292E;--shiki-light-font-weight:bold;--shiki-dark:#E1E4E8;--shiki-dark-font-weight:bold;\"> **黑天鹅**</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">：政策监管风险、技术路径被颠覆风险、地缘政治风险。</span></span> <span class=\"line\"></span> <span class=\"line\"><span style=\"--shiki-light:#005CC5;--shiki-light-font-weight:bold;--shiki-dark:#79B8FF;--shiki-dark-font-weight:bold;\">## Output Format (输出结构)</span></span> <span class=\"line\"><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">请以结构化输出，并在文末附上【引用来源清单】：</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">1.</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 投资结论摘要</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">    -</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 信号灯评级：🟢买入 / 🟡观望 / 🔴卖出</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">    -</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 核心逻辑总结（One-liner）</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">2.</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 关键财务数据表（含 CAGR, ROE, 现金流匹配度）</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">3.</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 深度分析正文（按上述 5 个 Phase 展开，每个结论需附带数据支持）</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">4.</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 估值仪表盘（历史分位 + 隐含预期 + 同行对比）</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">5.</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 未来监控清单</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">    -</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 只有当 [</span><span style=\"--shiki-light:#032F62;--shiki-light-text-decoration:underline;--shiki-dark:#DBEDFF;--shiki-dark-text-decoration:underline;\">事件A</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">] 发生时，才强化买入逻辑。</span></span> <span class=\"line\"><span style=\"--shiki-light:#E36209;--shiki-dark:#FFAB70;\">    -</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\"> 一旦 [</span><span style=\"--shiki-light:#032F62;--shiki-light-text-decoration:underline;--shiki-dark:#DBEDFF;--shiki-dark-text-decoration:underline;\">数据B</span><span style=\"--shiki-light:#24292E;--shiki-dark:#E1E4E8;\">] 恶化（如毛利率跌破X%），逻辑证伪，立即退出。</span></span></code></pre></div><p>到这里，一套从“查资料”到“下判断”的提示词链路就齐了。但你可能已经发现一个问题——<strong>它们是散装的</strong>。每换一只票，你都要一条条重新粘贴、手动把上一步的结论喂给下一步、最后还要自己整理成报告。下一节，我们把这套链路装进一个 Skill。</p><h2 id=\"从提示词到-skill-stock-advisor-是怎么长出来的\">从提示词到 Skill：<code>stock-advisor</code> 是怎么长出来的 </h2><h3 id=\"这个场景的痛点\">这个场景的痛点 </h3><p>上一节的提示词单独看都好用，但真要完整研究一只票，痛点很明确：</p><ul><li><strong>要手动串</strong>：技术面、基本面、多空、估值，八条提示词得一条条跑，还要人肉把中间结论搬来搬去；</li><li><strong>换标的重来</strong>：每分析一只新股票，整个流程从头走一遍；</li><li><strong>数据靠眼睛</strong>：截图里的数字全靠人核对，容易看错；</li><li><strong>决策容易自嗨</strong>：一个人分析，很难跳出自己的立场；</li><li><strong>交付靠手工</strong>：最后整理成一份像样的报告，又是一轮体力活。</li></ul><p><code>stock-advisor</code> 要解决的，就是把这条链路<strong>从“一堆提示词”变成“一条按一次就跑完的流水线”</strong>。</p><p><img src=\"images/case8-01.png\" alt=\"\" loading=\"lazy\"></p><h3 id=\"创作原理-编排-而不是重写\">创作原理：编排，而不是重写 </h3><p><code>stock-advisor</code> 的设计核心是一个词——<strong>编排（Orchestration）</strong>。它没有把所有能力重新造一遍，而是把“已经好用的部件”按顺序接成一条流水线：</p><div class=\"language- vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\"></span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>用户输入（截图 / 股票代码）</span></span> <span class=\"line\"><span>        │</span></span> <span class=\"line\"><span>        ▼</span></span> <span class=\"line\"><span>  ① 技术面分析 → ② 基本面分析 → ③ 多维交叉验证 → ④ 私董会讨论 → ⑤ 排版输出</span></span></code></pre></div><p>五个模块各司其职：</p><table tabindex=\"0\"><thead><tr><th>模块</th><th>做什么</th><th>关键设计</th></tr></thead><tbody><tr><td>① 技术面分析</td><td>从 K 线图识别形态、均线、MACD 等，并用行情数据交叉验证</td><td>图像识别 + 数据双轨，<strong>冲突时以数据为准并标注差异</strong></td></tr><tr><td>② 基本面分析</td><td>识别财报关键指标，补充估值与行业对比，给综合评级</td><td>技术 / 基本 / 资金三面各自打分，再合成评级</td></tr><tr><td>③ 多维交叉验证</td><td>联网检索研报、行业动态、重大新闻、政策</td><td>出现矛盾信号（如技术看涨但研报看空）<strong>必须明确标注分歧</strong></td></tr><tr><td>④ 私董会讨论</td><td>调用 <code>peers-advisory-group</code>，四位幕僚就这只票交叉辩论</td><td>复用现成 Skill，把“找反证”制度化</td></tr><tr><td>⑤ 排版输出</td><td>整理成结构化报告，转杂志风 HTML / PDF，可上传飞书</td><td>复用 <code>magazine-layout</code> 与 <code>lark-doc</code></td></tr></tbody></table><p>这里藏着 Skill 创作最值得学的一点：<strong>复用而非重写</strong>。<code>stock-advisor</code> 的依赖清单里，技术指标脚本复用了 <code>a-share-analyst</code>，决策讨论复用了 <code>peers-advisory-group</code>，排版复用了 <code>magazine-layout</code>，上传复用了 <code>lark-doc</code>。它自己新写的，只有“基本面分析”“HTML 转 PDF”等少数几块。</p><blockquote><p>换句话说，做一个复杂 Skill，不一定要从零写一个庞然大物。<strong>先把已有的能力当积木，缺哪块补哪块，再用一条主线把它们编排起来</strong>——这就是 <code>stock-advisor</code> 的创作方法论，也是把个人经验沉淀成工具的通用思路。</p></blockquote><p>它还有两个体现“产品化”意识的小设计：</p><ul><li><strong>首次使用建档</strong>：第一次跑会问你 3-4 个问题（风险偏好、投资周期、关注行业、仓位上限），存进记忆，之后的建议会按你的风格调权重；</li><li><strong>两种入口同一条流水线</strong>：上传截图走“图像识别 + 数据验证”，直接给代码走“纯数据驱动”，差异只在取数方式，后面完全一致。</li></ul><h3 id=\"它到底解决了什么问题\">它到底解决了什么问题 </h3><p>一句话：<strong>把“一次严肃的股票研究”从半天的手工活，压缩成一次对话。</strong> 你提供截图或代码，它自动完成取数、多面分析、交叉验证、多视角辩论和报告排版。人要做的，从“搬运和拼接”变成了“拍板和质疑”——这正是第一节说的，把精力还给判断。</p><blockquote><p><img src=\"images/case8-02.png\" alt=\"\" loading=\"lazy\"></p><p>在 WorkBuddy 里触发 <code>stock-advisor</code> Skill 的界面（技能被识别、开始执行的那一刻）。</p></blockquote><hr><h2 id=\"实战案例-用-stock-advisor-跑一遍天孚通信-300394\">实战案例：用 <code>stock-advisor</code> 跑一遍天孚通信（300394） </h2><p>光讲原理不够，下面是一次真实的完整对话。标的是<strong>天孚通信（300394）</strong>，光通信 / CPO 板块。整个过程分三步递进：先看图、再看财报、最后开一场私董会。</p><h3 id=\"第一步-上传-k-线图-先要一份技术面速读\">第一步：上传 K 线图，先要一份技术面速读 </h3><p>我上传了这只票的 K 线日线图和 MACD 指标图，让它先做技术分析。用的提示词就是第二节思路的实操版：</p><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>我上传了一只 A 股的 K 线日线图和技术指标图（MACD）。请你作为一位专业的技术分析师，完成以下任务：</span></span> <span class=\"line\"><span>1. 识别股票信息：这是哪只股票？当前股价大约是多少？</span></span> <span class=\"line\"><span>2. K 线形态分析：近期呈现什么形态？近 5 日 K 线的具体表现？</span></span> <span class=\"line\"><span>3. 均线系统分析：MA5/MA10/MA20 的排列状态，最近是否出现金叉或死叉</span></span> <span class=\"line\"><span>4. MACD 分析：DIF 和 DEA 的位置关系，柱状图趋势，是否出现背离</span></span> <span class=\"line\"><span>请以表格 + 文字结合的方式输出技术面速读报告。</span></span></code></pre></div><blockquote><p><img src=\"images/case8-03.png\" alt=\"\" loading=\"lazy\"></p><p>上传 K 线图 + 输入上述提示词的对话界面。</p></blockquote><p>WorkBuddy 先从图里识别出这是<strong>天孚通信（300394）</strong>，当前股价约 368.70 元，然后给出了结构化的技术面速读。核心结论：</p><ul><li><strong>趋势</strong>：MA5 &gt; MA10 &gt; MA20，标准多头排列，未见死叉，仍在主升浪；</li><li><strong>风险信号</strong>：当日一根长上影线（最高冲 376.10 回落到 368.70），MACD 红柱开始缩短，乖离率偏大；</li><li><strong>关键位</strong>：支撑看 MA5（347）/ MA10（319），压力看当日高点 376。</li></ul><blockquote><p><img src=\"images/case8-04.png\" alt=\"\" loading=\"lazy\"></p><p>技术面速读报告的完整输出（含 K 线形态、均线、MACD 四张小表）</p><p><img src=\"images/case8-05.png\" alt=\"\" loading=\"lazy\"></p></blockquote><p>一句话点评：这一步它没有猜涨跌，而是把“图里能读到的事实”结构化了——形态、均线、指标、支撑压力，一目了然。</p><p><img src=\"images/case8-06.png\" alt=\"\" loading=\"lazy\"></p><h3 id=\"第二步-补上财报截图-做一次全面分析\">第二步：补上财报截图，做一次全面分析 </h3><p>接着我又上传了 2025 年三季报和全年预增公告的截图，让它把基本面接进来，做一次完整评级：</p><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>我又上传了这只股票的 2025 年三季度报数据和 2025 年全年预增数据。</span></span> <span class=\"line\"><span>现在请你：</span></span> <span class=\"line\"><span>1. 先识别截图中的所有财务指标数据</span></span> <span class=\"line\"><span>2. 然后结合第一轮的技术面分析，帮我做一次全面的 A 股分析：</span></span> <span class=\"line\"><span>   - 技术面总评（综合 K 线、均线、MACD、KDJ 给出方向判断）</span></span> <span class=\"line\"><span>   - 基本面总评（营收增速、盈利能力、估值水平）</span></span> <span class=\"line\"><span>   - 资金面观察（成交量变化趋势）</span></span> <span class=\"line\"><span>   - 综合评级：强烈推荐 / 推荐 / 中性 / 谨慎 / 回避</span></span> <span class=\"line\"><span>3. 给出短期（1-2 周）、中期（1-3 月）的操作建议</span></span> <span class=\"line\"><span>4. 明确标注关键支撑位和压力位，请按照专业研报的格式输出。</span></span></code></pre></div><blockquote><p><img src=\"images/case8-07.png\" alt=\"\" loading=\"lazy\"></p><p>上传财报截图 + 输入上述提示词的对话界面。</p></blockquote><p>这一轮它先把截图里的财务指标逐条识别出来（营收 39.18 亿、同比 +63.63%，归母净利 14.65 亿、ROE 31.30%、毛利率 51.87%，PE 146.70……），然后合成了一张综合评级表：</p><table tabindex=\"0\"><thead><tr><th>维度</th><th>评分</th><th>权重</th><th>加权得分</th></tr></thead><tbody><tr><td>技术面</td><td>4.0 / 5.0</td><td>25%</td><td>1.00</td></tr><tr><td>基本面</td><td>4.5 / 5.0</td><td>30%</td><td>1.35</td></tr><tr><td>估值水平</td><td>2.0 / 5.0</td><td>25%</td><td>0.50</td></tr><tr><td>资金面</td><td>4.0 / 5.0</td><td>20%</td><td>0.80</td></tr><tr><td><strong>综合评分</strong></td><td>—</td><td>—</td><td><strong>3.65 / 5.0</strong></td></tr></tbody></table><p><strong>最终评级：推荐。</strong> 核心结论是一句很克制的话：<strong>中期趋势向好（CPO 高景气 + 高成长），但短期估值透支、涨幅过大，不宜追高，等回调再择机。</strong> 它还给了分投资者类型的仓位建议、四档支撑位和三档压力位。</p><blockquote><p><img src=\"images/case8-08.png\" alt=\"\" loading=\"lazy\"></p><p><img src=\"images/case8-09.png\" alt=\"\" loading=\"lazy\"></p><p>全面分析报告的完整输出（财务识别表 + 综合评级表 + 操作建议 + 支撑压力位）。</p></blockquote><p>值得注意的是，这一步已经体现了模块二的设计：<strong>技术、基本、资金三面分开打分，再加权合成</strong>，估值太贵就在总分里扣回来——不会因为成长性好就无脑看多。</p><p>还可以从不同角度去分析，使用`a-share-analyst` `skill去完成。</p><p><img src=\"images/case8-10.png\" alt=\"\" loading=\"lazy\"></p><h3 id=\"第三步-拿不定主意-开一场私董会\">第三步：拿不定主意，开一场私董会 </h3><p>评级出来了，但“推荐”不等于“现在就买”。这时候我叫上了第四个模块——<strong>私董会</strong>，请四位风格迥异的幕僚就这只票交叉辩论：</p><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>但我对这只股票还是拿不定主意。现在请帮我启动一场私董会，我要请四位幕僚来讨论这只股票是否值得投资：</span></span> <span class=\"line\"><span>- 巴菲特：从价值投资的角度（内在价值、护城河、安全边际）</span></span> <span class=\"line\"><span>- 马斯克：从科技趋势和颠覆性创新的角度</span></span> <span class=\"line\"><span>- 比尔·盖茨：从商业模式和行业格局的角度</span></span> <span class=\"line\"><span>- 乔布斯：从产品力和用户体验的角度</span></span> <span class=\"line\"><span>讨论要求：</span></span> <span class=\"line\"><span>1. 每位幕僚先各自发表 3-5 分钟的独立观点。</span></span> <span class=\"line\"><span>2. 然后进入交叉质询环节——幕僚之间互相挑战对方观点。</span></span> <span class=\"line\"><span>3. 最后每人用一句话给出&quot;买入/持有/卖出&quot;的最终建议。</span></span> <span class=\"line\"><span>4. 你作为私董会主持人，综合四位意见给出最终执行方案。</span></span> <span class=\"line\"><span>请基于前两轮的分析数据来展开讨论，让幕僚们&quot;带着数据聊&quot;。</span></span></code></pre></div><blockquote><p><img src=\"images/case8-11.png\" alt=\"\" loading=\"lazy\"></p><p>启动私董会的对话界面。</p></blockquote><p>私董会环节里，系统先联网更新了四位幕僚的近况，还<strong>补检索了更新的数据</strong>（2025 全年营收 51.63 亿、净利 20.17 亿，2026 Q1 环比下滑，以及和中际旭创、新易盛的横向对比）——这正是模块三“多维交叉验证”在起作用，把讨论从截图数据推进到了全网最新事实。</p><p>四位幕僚各自独立发言、再互相质询，观点很快分成两派：</p><blockquote><p><img src=\"images/case8-12.png\" alt=\"\" loading=\"lazy\"></p><p><img src=\"images/case8-13.png\" alt=\"\" loading=\"lazy\"></p><p>四位幕僚独立观点 +</p><p><img src=\"images/case8-14.png\" alt=\"\" loading=\"lazy\"></p><p>交叉质询环节（篇幅较长，建议分屏截图）。</p></blockquote><p>最后每人一句话定调，形成了鲜明的“2:2”分裂：</p><ul><li><strong>巴菲特（回避）</strong>：“PE 142，安全边际为零，护城河在收窄。除非跌到 200 元以下，否则这不是投资，是赌博。”</li><li><strong>比尔·盖茨（等待 / 换仓）</strong>：“基本面尚可，但估值太贵、竞争格局恶化。建议等 PE 回到 60 倍以下，或换性价比更高的新易盛 / 中际旭创。”</li><li><strong>马斯克（All in）</strong>：“CPO 是光通信的 iPhone 时刻，天孚是上游的铲子王。超买是最后的上车机会，不是下车理由。”</li><li><strong>乔布斯（有条件持有）</strong>：“相信 CPO 革命就现在持有，但前提是 CPO FAU 在 2026 H2 如期兑现，否则果断离场。”</li></ul><p><img src=\"images/case8-15.png\" alt=\"\" loading=\"lazy\"></p><p>主持人最后综合出一份<strong>分投资者类型的执行方案</strong>，而不是一个笼统的“买或不买”：</p><table tabindex=\"0\"><thead><tr><th>投资者类型</th><th>建议</th><th>执行要点</th></tr></thead><tbody><tr><td>价值投资者</td><td>坚决回避</td><td>等 PE &lt; 40</td></tr><tr><td>成长投资者</td><td>可持有，需止损</td><td>保留 3-5 成，跌破 MA5(347) 减仓，跌破 MA10(319) 清仓</td></tr><tr><td>趋势投资者</td><td>谨慎参与</td><td>等回调至 MA10 / MA20，KDJ 回落至 50 以下再介入</td></tr><tr><td>激进投资者</td><td>小仓位试仓</td><td>最多 3 成，跌破 300 元清仓</td></tr></tbody></table><p>并且把决策挂到了几个<strong>未来验证节点</strong>上：8 月中报预告看 Q2 是否环比改善，H2 看 CPO FAU 能否放量、毛利率能否回到 55%+，10 月三季报看营收增速。逻辑证伪就退出。</p><blockquote><p><img src=\"images/case8-16.png\" alt=\"\" loading=\"lazy\"></p><p>主持人的综合执行方案（分类型建议表 + 决策节点表 + 替代标的）。</p></blockquote><h3 id=\"最后-一键成稿\">最后：一键成稿 </h3><p>对话结束后，让它把整场分析生成一份杂志风格的报告，<code>stock-advisor</code> 会调用排版模块出成品，可以本地存 PDF，也可以直接上传飞书云文档。</p><blockquote><p><img src=\"images/case8-17.png\" alt=\"\" loading=\"lazy\"></p><p>杂志风格投资分析报告成品（首屏 / 封面）。</p></blockquote><p>回头看这一个案例，<code>stock-advisor</code> 把第二节那八条散装提示词，变成了一次三轮对话就跑完的完整研究：<strong>看图 → 看财报 → 开私董会 → 出报告</strong>。而全程它没有替我做那个最关键的决定——买还是不买。它只是把该看的都看了，把该吵的都吵了，最后把判断权，干干净净地交回到我手里。</p><hr><h2 id=\"常见错误与使用边界\">常见错误与使用边界 </h2><p>金融是强监管、强风险的场景，比办公三件套更需要守住边界。下面几条，是把 AI 用在投资上最容易踩的坑。</p><table tabindex=\"0\"><thead><tr><th>常见错误</th><th>为什么错</th><th>正确做法</th></tr></thead><tbody><tr><td>让 AI 给“买点 / 卖点”</td><td>它不掌握实时全量信息，也不为你的钱负责</td><td>只用它做事实梳理和多空推演，买卖由你拍板</td></tr><tr><td>完全相信截图识别的数字</td><td>图像识别会看错，财报口径也会变</td><td>关键数字要交叉验证——本案例私董会环节的数据就比前两轮更新</td></tr><tr><td>指望它判断行业拐点、价格见底</td><td>这类判断依赖前瞻信息和经验，AI 给不了</td><td>让它梳理“该盯哪些领先指标”，拐点自己盯</td></tr><tr><td>只看多方逻辑，越看越上头</td><td>确认偏误，AI 会顺着你的语气强化观点</td><td>用 Prompt 6 和私董会，强制它给空方逻辑和反证</td></tr><tr><td>把 AI 报告直接当投资依据</td><td>报告是研究辅助，不是投资建议</td><td>报告结论仅供参考，决策与风险自负</td></tr></tbody></table><blockquote><p><strong>风险提示：股市有风险，投资需谨慎。</strong> **本章所有提示词、Skill 与案例，均以“辅助研究”为目的，不构成任何投资建议。**AI 只是把事实和分歧摆到你面前的工具，最终的判断和后果，始终在人这一边。据此操作，风险自担。</p></blockquote></div></div>"),
 ("chapter-9","09","第 9 章 一句话召唤 AI 视频团队","WB案例","<p>在 WorkBuddy 里把短视频工作拆成两支 AI 专家团：一支负责自动生产视频，一支负责拆解爆款视频。</p><p><img src=\"images/case9-01.png\" alt=\"\" loading=\"lazy\"></p><table tabindex=\"0\"><thead><tr><th>团队</th><th>负责什么</th><th>适合什么任务</th></tr></thead><tbody><tr><td><strong>视频生成团队</strong></td><td>从主题出发，完成热点采集、选题筛选、脚本、分镜、配音、渲染、字幕和发布。</td><td>AI 周报、产品更新、知识科普、行业分析、产品评测。</td></tr><tr><td><strong>爆款视频拆解团队</strong></td><td>从视频链接出发，下载视频、提取音频、转写文案、分析镜头语言，生成拆解报告和仿拍建议。</td><td>学习爆款结构、复盘竞品视频、沉淀拍摄手册、给生成团队提供参考。</td></tr></tbody></table><p>这两个团队并不是互相替代的关系。视频生成团队解决“今天怎么做一条出来”，爆款拆解团队解决“为什么别人那条能火，我能学到什么”。一个负责生产，一个负责学习，组合起来才有持续迭代的可能。</p><p><img src=\"images/case9-02.png\" alt=\"\" loading=\"lazy\"></p><h2 id=\"如何召唤-从一句话开始-但不要停在一句话\">如何召唤：从一句话开始，但不要停在一句话 </h2><p><img src=\"images/case9-03.png\" alt=\"\" loading=\"lazy\"></p><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>召唤视频生成团队，制作一条 46 秒 AI 周报短视频。</span></span></code></pre></div><h2 id=\"第一支团队-视频生成团队\">第一支团队：视频生成团队 </h2><p>视频生成团队里有四个核心角色：视频生成团队主理人凌导、信息采集员灵阅、内容策划师灵枢、视频制作师灵映。它们不是四个换名字的聊天窗口，而是一条有上下游交接关系的视频生产线。</p><p><img src=\"images/case9-04.png\" alt=\"\" loading=\"lazy\"></p><table tabindex=\"0\"><thead><tr><th>角色</th><th>定位</th><th>交付物</th></tr></thead><tbody><tr><td>凌导</td><td>主理人 / 团长</td><td>拆解任务、安排并行与串行流程、汇总产物、处理检查点。</td></tr><tr><td>灵阅</td><td>信息采集员</td><td>热点池、来源表、去重后的结构化摘要、选题候选。</td></tr><tr><td>灵枢</td><td>内容策划师</td><td>选题判断、脚本、分镜、旁白、转场、素材清单、BGM 和字幕节奏。</td></tr><tr><td>灵映</td><td>视频制作师</td><td>HTML 视频工程、配音、字幕对齐、转场动画、素材拼接、渲染成片。</td></tr></tbody></table><p>这才是多 Agent 的关键：不是角色越多越好，而是每个角色都有清晰输入和输出。信息采集员不直接写成片脚本，策划师不重新编造热点，制作师不重写事实，团长负责让流程不断档。</p><p><img src=\"images/case9-05.png\" alt=\"\" loading=\"lazy\"></p><h3 id=\"底层生产引擎-hyperframes\">底层生产引擎：HyperFrames </h3><p>文章提到，这条视频流水线基于 HyperFrames 搭建。它的核心思路是用 HTML 渲染视频，天然适合 Agent 生成结构化工程，再交给渲染工具输出 MP4。它还带有 CLI 工具链、TTS、字幕、去背景和视频组件模板。</p><p><img src=\"images/case9-06.png\" alt=\"\" loading=\"lazy\"></p><h3 id=\"生成流程一-信息采集员先让热点有来源\">生成流程一：信息采集员先让热点有来源 </h3><p>做视频最耗时间的往往不是剪辑，而是“今天到底拍什么”。所以视频生成团队先让信息采集员灵阅抓 RSS、搜新闻、扫社媒、聚合 AI 热点，并去重输出结构化摘要。</p><p><img src=\"images/case9-07.png\" alt=\"\" loading=\"lazy\"></p><p>这个阶段的产物至少应该包含：标题、来源、发布时间、事件发生时间、原始链接、热度线索、为什么值得关注。热度只能帮助排序，不能替代事实核验。</p><h3 id=\"生成流程二-内容策划师把主题变成镜头\">生成流程二：内容策划师把主题变成镜头 </h3><p>选题有了之后，真正费脑子的是“这条视频怎么讲”。内容策划师灵枢负责选题评估、脚本写作、分镜设计、旁白文案、镜头节奏，以及转场建议、素材清单、BGM 节奏、字幕停顿和情绪节点。</p><p><img src=\"images/case9-08.png\" alt=\"\" loading=\"lazy\"></p><p>这里建议设置第一次人工检查：开头 3 秒是否有钩子，46 秒是否塞入过多信息，旁白是否准确，画面是否真的支撑观点。脚本不过关时，不要进入配音和渲染。</p><h3 id=\"生成流程三-视频制作师把分镜变成成片\">生成流程三：视频制作师把分镜变成成片 </h3><p>灵映会把确认后的脚本转成 HTML，再调用 HyperFrames 渲染 MP4。文章里提到，系统会自动完成 Azure TTS 配音、Whisper 字幕对齐、动画与转场生成、素材拼接、字幕叠加和视频渲染。</p><p><img src=\"images/case9-09.png\" alt=\"\" loading=\"lazy\"></p><p><img src=\"images/case9-10.png\" alt=\"\" loading=\"lazy\"></p><p>成片验收不要只看“能不能播放”。至少检查旁白与字幕是否一致、镜头时长是否匹配、文字是否遮挡主体、BGM 是否可用、素材是否有版权风险、画面是否适合目标平台安全区。</p><h3 id=\"生成流程四-发布可以自动化-但默认要人工确认\">生成流程四：发布可以自动化，但默认要人工确认 </h3><p>发布 Agent 自动生成标题、自动打标签、自动上传封面，并通过云手机发布到抖音、视频号和 B 站。这是很强的自动化能力，但蓝皮书建议默认不要直接自动发布，除非账号、素材、标题和合规边界都已经过人工确认。</p><p><img src=\"images/case9-11.png\" alt=\"\" loading=\"lazy\"></p><p><img src=\"images/case9-12.png\" alt=\"\" loading=\"lazy\"></p><h2 id=\"第二支团队-爆款视频拆解团队\">第二支团队：爆款视频拆解团队 </h2><p>光会生成还不够。</p><p>内容创作者真正需要的是理解“为什么别人能爆”，把一条爆款视频拆成可以参考的操作手册：提取视频、转录文案、分析景别运镜、剪辑节奏、色调风格，并给出仿拍建议。</p><p><img src=\"images/case9-13.png\" alt=\"\" loading=\"lazy\"></p><p><img src=\"images/case9-14.png\" alt=\"\" loading=\"lazy\"></p><table tabindex=\"0\"><thead><tr><th>角色</th><th>职责</th><th>工具 / 技术</th></tr></thead><tbody><tr><td>阿爆</td><td>团长 / 拆解总控</td><td>任务调度、流程编排、结果汇总。</td></tr><tr><td>小凯</td><td>音频处理与转录</td><td>ffmpeg、ASR，把视频音频转成完整口播文案。</td></tr><tr><td>小淼</td><td>视频理解与镜头裁切</td><td>视频理解 API、ffmpeg，分析镜头语言并裁切片段。</td></tr></tbody></table><h3 id=\"拆解流程一-视频下载要有降级策略\">拆解流程一：视频下载要有降级策略 </h3><p>爆款拆解的第一步是拿到视频。文章里专门提到，最复杂的是视频下载，所以设计了一套三层降级策略：官方 API、Playwright、yt-dlp。只要有一层成功，流程就继续。</p><p><img src=\"images/case9-15.png\" alt=\"\" loading=\"lazy\"></p><p>这里必须加上边界：视频下载和分析要遵守平台条款、版权授权和合理使用范围。拆解的目的应该是学习结构和方法，不是搬运原视频。</p><h3 id=\"拆解流程二-音频提取与文案转写\">拆解流程二：音频提取与文案转写 </h3><p>视频下载完成后，小凯用 ffmpeg 提取音频，把 video.mp4 转成 audio.mp3，再调用语音识别 API 自动转录完整口播文案。以前一句句听、一句句敲的工作，现在可以被稳定自动化。</p><p><img src=\"images/case9-16.png\" alt=\"\" loading=\"lazy\"></p><p><img src=\"images/case9-17.png\" alt=\"\" loading=\"lazy\"></p><h3 id=\"拆解流程三-视频理解与镜头语言分析\">拆解流程三：视频理解与镜头语言分析 </h3><p>接下来是最有意思的一步：视频理解。小淼会分析整条视频的景别、运镜、转场、剪辑节奏、色调、镜头时长。很多看起来“有感觉”的爆款视频，背后其实有稳定的镜头规律。</p><p><img src=\"images/case9-18.png\" alt=\"\" loading=\"lazy\"></p><p><img src=\"images/case9-19.png\" alt=\"\" loading=\"lazy\"></p><h2 id=\"两支团队如何形成闭环\">两支团队如何形成闭环 </h2><p>两个专家团可以合作。先用爆款拆解团队学习镜头语言和节奏，再让视频生成团队生产新视频，发布之后继续分析数据，再反过来优化下一版内容。</p><figure class=\"wb-mermaid\" aria-label=\"流程图\" data-v-dbf03737><pre class=\"wb-mermaid__fallback\" data-v-dbf03737><code data-v-dbf03737>flowchart LR     A[爆款视频链接] --&gt; B[拆解团队：转写、镜头、节奏、仿拍建议]     B --&gt; C[形成拍摄手册和内容规律]     C --&gt; D[生成团队：热点、脚本、分镜、渲染]     D --&gt; E[人工验收与发布]     E --&gt; F[数据复盘]     F --&gt; B </code></pre><!----></figure><p>这就是专家团比单个工具更有意义的地方。它不只是帮你做一条视频，而是让“学习、生产、发布、复盘”变成一个可以重复运转的系统。</p></div></div>"),
 ("chapter-10","10","第 10 章 自媒体不只是靠努力，而是一条增长闭环","WB案例","<h2 id=\"内容没人看-往往不是因为你不够努力\">内容没人看？往往不是因为你不够努力 </h2><p>一个人做自媒体，做自媒体最浪费时间的事，就是一上来就把内容打磨到满分。</p><p>听起来很反常识，但我真踩过这个坑。你写得很深，资料查得很全，结构改了三遍。结果发出去，阅读量个位数。</p><p>后来我才意识到，起号前期真正要先解决的，不是“写得够不够好”，而是“有没有人愿意点进来”。</p><h2 id=\"工作流\">工作流 </h2><figure class=\"wb-mermaid\" aria-label=\"流程图\" data-v-dbf03737><pre class=\"wb-mermaid__fallback\" data-v-dbf03737><code data-v-dbf03737>flowchart LR     A[趋势、评论与用户问题] --&gt; B[选题池]     B --&gt; C[事实包与观点]     C --&gt; D[标题和结构]     D --&gt; E[公众号 / 小红书 / 视频脚本]     E --&gt; F[封面、长图与分镜]     F --&gt; G[合规和发布前体检]     G --&gt; H[草稿或人工发布]     H --&gt; I[数据与人工修改回流]     I --&gt; B </code></pre><!----></figure><p>Skill 的作用是补上其中一个环节，不是接管账号判断。下面用八个具体工作现场说明。</p><h2 id=\"场景一-每天刷热点-仍然不知道账号该写什么\">场景一：每天刷热点，仍然不知道账号该写什么 </h2><p>热榜告诉你“大家正在看什么”，却不告诉你“这个账号为什么值得写”。只跟热点，容易得到同质化内容；只凭感觉，又很难判断用户是否真的关心。</p><ul><li><a href=\"https://skillhub.cn/skills/gzh-explosive-content-detector\" target=\"_blank\" rel=\"noreferrer\">公众号热门文章查询</a>：观察同主题热门文章；</li><li><a href=\"https://skillhub.cn/skills/xhs-hotnotes\" target=\"_blank\" rel=\"noreferrer\">小红书爆款笔记查询</a>：获取热门笔记和数据线索；</li><li><a href=\"https://skillhub.cn/skills/xhs-comment-insights\" target=\"_blank\" rel=\"noreferrer\">小红书评论洞察</a>：从评论中提取问题、反对意见和未满足需求；</li><li><a href=\"https://skillhub.cn/skills/inspiration-hunter-skill\" target=\"_blank\" rel=\"noreferrer\">灵感捕手</a>：把临时想到的角度放进统一收件箱。</li></ul><h3 id=\"指令怎样写\">指令怎样写 </h3><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>围绕“AI 办公自动化”建立本周选题池，不直接写文章。</span></span> <span class=\"line\"><span>分别收集公众号与小红书近 30 天的高互动内容，记录标题、发布日期、</span></span> <span class=\"line\"><span>核心承诺、内容结构、互动信号和原链接。</span></span> <span class=\"line\"><span>再从评论中提取：重复问题、反对意见、失败经历和用户原话。</span></span> <span class=\"line\"><span></span></span> <span class=\"line\"><span>结合我的账号定位：面向非技术职场人，强调真实流程和结果验收。</span></span> <span class=\"line\"><span>输出 12 个候选选题，每个包含：目标读者、真实问题、已有内容缺口、</span></span> <span class=\"line\"><span>我能提供的新证据、适合平台、制作成本和时效性。</span></span> <span class=\"line\"><span>不要把阅读量高直接解释成选题一定适合我。</span></span></code></pre></div><p><img src=\"images/case10-01.png\" alt=\"\" loading=\"lazy\"></p><h3 id=\"执行流程与结果\">执行流程与结果 </h3><p>WorkBuddy 先生成跨平台样本表，再把评论聚成问题簇，最后把“热度、账号匹配、新增价值、证据充足度、制作成本”分别评分。交付物是一张可以人工删选的选题看板。</p><p><img src=\"images/case10-02.png\" alt=\"\" loading=\"lazy\"></p><h3 id=\"有时候光找热门还不够-我们还需要去找低粉爆款。\"><strong>有时候光找热门还不够，我们还需要去找低粉爆款。</strong> </h3><p>大家应该都听过，<strong>起号要找低粉爆款去抄</strong>，这确实是这样的。</p><p><em>PS：这里说的抄，是抄选题，不是原封不动的抄内容。</em></p><p>推荐一个叫<a href=\"https://github.com/kangarooking/kangarooking-skills/tree/main/viral-topic\" target=\"_blank\" rel=\"noreferrer\"><strong>viral-topic</strong></a><strong>的skill</strong>，它可以获取各个平台近期的指定领域的多个低粉爆款内容。</p><p>比如获取公众号最近7天的AI领域低粉爆款文章。</p><p><img src=\"images/case10-03.png\" alt=\"\" loading=\"lazy\"></p><p>筛选X上的低粉爆款</p><p><img src=\"images/case10-04.png\" alt=\"\" loading=\"lazy\"></p><p>以及YouTube的低粉爆款</p><p><img src=\"images/case10-05.png\" alt=\"\" loading=\"lazy\"></p><h2 id=\"场景二-想要爆款标题-但不想标题党\">场景二：想要爆款标题，但不想标题党 </h2><p>“给我 20 个爆款标题”很容易得到数字、悬念和夸张承诺，却没有任何标题能准确兑现正文。标题不是独立文案，它是读者与正文之间的一份承诺。</p><ul><li><a href=\"https://skillhub.cn/skills/gzh-official-account-title-generator\" target=\"_blank\" rel=\"noreferrer\">公众号标题生成与评分</a>；</li><li><a href=\"https://skillhub.cn/skills/redbook-writer\" target=\"_blank\" rel=\"noreferrer\">小红书爆款笔记自动生成器</a>中的标题与标签模块；</li><li><a href=\"https://skillhub.cn/skills/bozo-video-gz\" target=\"_blank\" rel=\"noreferrer\">短视频钩子方案生成</a>。</li></ul><h3 id=\"指令怎样写-1\">指令怎样写 </h3><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>读取 approved-article.md，只根据正文已经出现的事实生成标题。</span></span> <span class=\"line\"><span>分别生成：公众号标题 8 个、小红书标题 8 个、短视频开场钩子 5 个。</span></span> <span class=\"line\"><span></span></span> <span class=\"line\"><span>每个候选都输出：</span></span> <span class=\"line\"><span>1. 面向谁；2. 承诺什么；3. 正文哪一段能够兑现；</span></span> <span class=\"line\"><span>4. 采用的问题/结果/清单/案例/反常识角度；</span></span> <span class=\"line\"><span>5. 可信度、具体性、平台适配和夸大风险评分。</span></span> <span class=\"line\"><span></span></span> <span class=\"line\"><span>删除无法证明的数字、绝对化承诺、虚假稀缺和与正文不一致的结论。</span></span> <span class=\"line\"><span>不要自动选择最终标题，先让我确认内容承诺。</span></span></code></pre></div><p><img src=\"images/case10-06.png\" alt=\"\" loading=\"lazy\"></p><h3 id=\"验收方法\">验收方法 </h3><p>把标题单独给一个不了解正文的人看，请他写出“我预计点进去会得到什么”。再与正文核对。预期与实际不一致，标题分数再高也不能用。</p><p>workbuddy通过这几个skill，生成的标题还真有那味儿。特别是小红书的标题，很有小红书的感觉。</p><p><img src=\"images/case10-07.png\" alt=\"\" loading=\"lazy\"></p><p>可以进行 A/B 测试，但一次只改变一个主要变量，例如“问题式”与“结果式”。不要同时改标题、封面、发布时间和正文开头，否则数据无法解释。</p><p>再推荐一个标题skill：<a href=\"https://github.com/kangarooking/kangarooking-skills/tree/main/viral-title\" target=\"_blank\" rel=\"noreferrer\"><strong>viral-</strong></a><a href=\"https://github.com/kangarooking/kangarooking-skills/tree/main/viral-title\" target=\"_blank\" rel=\"noreferrer\"><strong>title</strong></a><strong>，很适合用来给公众号起标题</strong></p><p><img src=\"images/case10-08.png\" alt=\"\" loading=\"lazy\"></p><h2 id=\"场景三-公众号封面每次从空白画布开始\">场景三：公众号封面每次从空白画布开始 </h2><p>封面既要让人看懂主题，又要适配大小封面、安全区和账号品牌。直接说“做一张高级感封面”，通常会得到与正文无关的装饰图、错误文字或失真的 Logo。</p><ul><li><a href=\"https://skillhub.cn/skills/explosive-cover-generator-gzh\" target=\"_blank\" rel=\"noreferrer\">公众号爆款封面生成</a>：分析同赛道视觉规律并给出方案；</li><li><a href=\"https://skillhub.cn/skills/generate-wechat-official-account-images\" target=\"_blank\" rel=\"noreferrer\">公众号图片生成器</a>：处理大小封面、文内配图和引导图；</li><li>海报设计或图像生成 Skill：执行已确认的视觉 brief。</li></ul><h3 id=\"指令怎样写-2\">指令怎样写 </h3><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>为文章《收藏不是知识管理，能再次用起来才是》制作公众号封面 brief。</span></span> <span class=\"line\"><span>目标读者：知识工作者；核心信息：从收藏走向可复用知识流。</span></span> <span class=\"line\"><span>品牌色：#1677FF、白、黑；禁止紫色渐变、夸张科技光效和虚构产品界面。</span></span> <span class=\"line\"><span></span></span> <span class=\"line\"><span>先输出 3 个构图方向，每个包含：主体、层级、封面文案、色彩、留白、</span></span> <span class=\"line\"><span>大小封面裁切风险和正文对应段落。我确认后再生成图片。</span></span> <span class=\"line\"><span>生成后检查：文字是否准确、Logo 是否变形、主体是否被小封面裁掉、</span></span> <span class=\"line\"><span>是否使用未经授权的人物或素材。不要直接上传公众号。</span></span></code></pre></div><h3 id=\"结果是否可用\">结果是否可用 </h3><p><img src=\"images/case10-09.png\" alt=\"\" loading=\"lazy\"></p><p>生成的封面还不错，有汉字、封面负责表达的主题也比较贴切，如果换成更强的生图模型，效果应该会更好。</p><h2 id=\"场景四-小红书不只是-把长文切成九张图\">场景四：小红书不只是“把长文切成九张图” </h2><p>公众号文章改成小红书时，常见做法是截短段落、加入表情符号，再把文字铺到九张卡片上。结果信息很多，但封面没有钩子，第二页没有承接，最后一页没有行动，移动端也难读。</p><ul><li><a href=\"https://skillhub.cn/skills/xiaohongshu-cover\" target=\"_blank\" rel=\"noreferrer\">小红书封面图制作</a>；</li><li><a href=\"https://skillhub.cn/skills/any2xiaohongshu\" target=\"_blank\" rel=\"noreferrer\">小红书图片生成器</a>：将结构化内容渲染为竖版卡片；</li><li><a href=\"https://skillhub.cn/skills/xhs-ops-copilot\" target=\"_blank\" rel=\"noreferrer\">小红书运营副驾</a>：发布前体检与复盘。</li></ul><h3 id=\"工作流-1\">工作流 </h3><ol><li>从长文提取不带平台语气的事实包；</li><li>选择一个核心问题，删除与它无关的支线；</li><li>设计“封面承诺 → 问题共鸣 → 方法 → 示例 → 误区 → 清单”的滑动节奏；</li><li>先输出逐页线框和字数，再生成图片；</li><li>在真实手机宽度检查字号、断行、边距和重点；</li><li>最终标题、正文、标签和图片逐一核对数字与专有名词。</li></ol><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>把 approved-article.md 改造成 8 页小红书图文，不新增事实。</span></span> <span class=\"line\"><span>第 1 页只表达一个承诺；第 2 页写读者正在经历的问题；</span></span> <span class=\"line\"><span>第 3-6 页每页只讲一个动作并给一个例子；第 7 页写常见误区；</span></span> <span class=\"line\"><span>第 8 页给可保存的检查清单。</span></span> <span class=\"line\"><span>先返回逐页文案、视觉层级和预计字数，我确认后再调用封面与长图 Skill。</span></span></code></pre></div><p><img src=\"images/case10-10.png\" alt=\"\" loading=\"lazy\"></p><h2 id=\"场景五-一段长文怎样变成可拍的短视频\">场景五：一段长文怎样变成可拍的短视频 </h2><p>“改成 60 秒口播”通常只是把文章压缩成更快的朗读稿，没有镜头、节奏、证据画面和停顿，也没有说明谁能拍、需要什么素材。</p><ul><li><a href=\"https://skillhub.cn/skills/short-video-topic-research\" target=\"_blank\" rel=\"noreferrer\">短视频选题素材研究</a>；</li><li><a href=\"https://skillhub.cn/skills/shortvideo-content-factory-cn-v1-zt\" target=\"_blank\" rel=\"noreferrer\">短视频脚本与矩阵内容工厂</a>；</li><li><a href=\"https://skillhub.cn/skills/seedance-director\" target=\"_blank\" rel=\"noreferrer\">AI 短视频导演</a>用于分镜和生成提示；</li><li>配乐 Skill 只在确认版权和商用范围后使用。</li></ul><h3 id=\"指令怎样写-3\">指令怎样写 </h3><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>把这篇文章改造成 60 秒真人口播，目标是让第一次使用 WorkBuddy 的人</span></span> <span class=\"line\"><span>理解“为什么任务简报比一句模糊需求更重要”。</span></span> <span class=\"line\"><span>输出时间轴表格：时长、景别、画面、口播、屏幕文字、素材来源、转场。</span></span> <span class=\"line\"><span>前 3 秒必须提出真实问题，不夸大收益；20 秒前展示一次产品过程证据；</span></span> <span class=\"line\"><span>结尾给一个可以立即尝试的指令，不做虚假互动承诺。</span></span> <span class=\"line\"><span>同时列出必须实拍、可用产品截图、可由 AI 生成的画面，禁止伪造用户反馈。</span></span></code></pre></div><p><img src=\"images/case10-11.png\" alt=\"\" loading=\"lazy\"></p><p>生成的口播文案，效果还不错哦。</p><h2 id=\"场景六-发布前-别让自动化越过责任边界\">场景六：发布前，别让自动化越过责任边界 </h2><ul><li><a href=\"https://skillhub.cn/skills/gzh-prohibited-word\" target=\"_blank\" rel=\"noreferrer\">公众号违禁词检测</a>：标记风险表达；</li><li><a href=\"https://skillhub.cn/skills/md-to-wechat\" target=\"_blank\" rel=\"noreferrer\">公众号排版 Skill</a>：渲染 Markdown 并创建草稿；</li><li><a href=\"https://skillhub.cn/skills/unclecheng-reduce-ai-perception-v2\" target=\"_blank\" rel=\"noreferrer\">文章去 AI 味工具</a>：只用于减少套话，不用于伪装来源或原创。</li></ul><div class=\"language-Plain vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">Plain</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>检查本次公众号文章是否有违禁词，如有请标记出来，并对每个违禁词给出修改建议。检查整体内容的 AI 味，并降低AI味，最后把文章排版。</span></span></code></pre></div><p>发布链建议停在草稿箱：事实检查 → 引用与版权 → 品牌与合规 → 链接检查 → 手机预览 → 人工确认账号 → 发布。自动点赞、批量私信、刷评论、绕过平台风控和未经确认的群发，不属于本书推荐的效率场景。</p><p><img src=\"images/case10-12.png\" alt=\"\" loading=\"lazy\"></p><p><img src=\"images/case10-13.png\" alt=\"\" loading=\"lazy\"></p><p><img src=\"images/case10-14.png\" alt=\"\" loading=\"lazy\"></p><h2 id=\"场景七-发布后不复盘-下一篇仍从零开始\">场景七：发布后不复盘，下一篇仍从零开始 </h2><p>复盘主要是把AI写的和人工修改后的终稿进行对比，让skill自动进化，下一次，它将写出更好的内容。</p><p>可以使用 <a href=\"https://skillhub.cn/skills/skill-article-evolution\" target=\"_blank\" rel=\"noreferrer\">公众号写作自我迭代</a> 或小红书运营副驾，把人工修改和数据写回风格库：</p><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>读取本期内容数据、发布版本和人工修改记录，生成复盘。</span></span> <span class=\"line\"><span>先陈述数据事实，再列出最多 3 个可验证假设，不把相关性写成因果。</span></span> <span class=\"line\"><span>把表现按选题、标题、封面、开头、结构、发布时间和渠道拆开。</span></span> <span class=\"line\"><span>为下轮设计 2 个单变量实验，并说明成功指标和停止条件。</span></span> <span class=\"line\"><span>将长期有效的修改规则写入 style-guide.md；一次性热点不要写入永久规则。</span></span></code></pre></div><p>把AI最开始产出的文案和终稿都丢进去，最终产出复盘报告和style-guide.md，下次AI写的东西就能离你的期望更进一步啦～</p><p><img src=\"images/case10-15.png\" alt=\"\" loading=\"lazy\"></p><p><img src=\"images/case10-16.png\" alt=\"\" loading=\"lazy\"></p><h2 id=\"一套够用的自媒体-skill-栈\">一套够用的自媒体 Skill 栈 </h2><table tabindex=\"0\"><thead><tr><th>层级</th><th>先装什么</th><th>何时再增加</th></tr></thead><tbody><tr><td>入门</td><td>热门内容查询、标题评分、图片生成</td><td>已能稳定完成一篇内容</td></tr><tr><td>稳定</td><td>评论洞察、封面、排版草稿、违禁词检测</td><td>已明确账号定位和审核人</td></tr><tr><td>多平台</td><td>小红书卡片、短视频脚本、平台适配</td><td>已有统一事实包</td></tr><tr><td>进阶</td><td>数据回流、风格迭代、定时选题雷达</td><td>人工流程已连续跑通 4 周</td></tr></tbody></table></div></div>"),
 ("chapter-11","11","第 11 章 WorkBuddy也能做GEO专家","WB案例","<p>GEO 是 Generative Engine Optimization，中文常叫生成式引擎优化。</p><p>过去做品牌，很多人关心的是 SEO：用户在搜索引擎里搜某个关键词，官网、文章、媒体报道能不能排到前面。现在越来越多用户直接问元宝、DeepSeek、豆包、Kimi 这类生成式 AI：“哪个产品适合我？”“某个领域有哪些工具？”“这家公司靠谱吗？”品牌面对的问题就变了：AI 回答里有没有你，提到你时准不准，推荐你时有没有信任依据。</p><h2 id=\"geo-诊断到底解决什么问题\">GEO 诊断到底解决什么问题 </h2><p>GEO 不是让 AI 帮你写一篇品牌软文，而是回答一个更基础的问题：在用户真实提问的场景里，你的品牌有没有被 AI 理解、引用和推荐。</p><table tabindex=\"0\"><thead><tr><th>问题</th><th>要看什么</th><th>例子</th></tr></thead><tbody><tr><td>可见度</td><td>AI 回答里是否提到品牌</td><td>用户问“有没有能统一管理多个 AI Agent 的桌面软件”，WeSight 是否被提及。</td></tr><tr><td>准确性</td><td>AI 对品牌描述是否正确</td><td>功能、适用平台、目标用户、价格、开源状态是否被说错。</td></tr><tr><td>竞争位</td><td>同一个问题下，AI 把推荐位给了谁</td><td>竞品被频繁推荐，而你的产品几乎不出现。</td></tr><tr><td>信任源</td><td>AI 能不能找到可信资料支撑回答</td><td>官网、GitHub、媒体报道、自媒体矩阵、用户评价是否形成闭环。</td></tr><tr><td>行动点</td><td>诊断之后应该先改哪里</td><td>补官网说明、优化 README、补竞品对比页、处理负面舆情。</td></tr></tbody></table><h2 id=\"先选对专家-品牌-geo-诊断专家\">先选对专家：品牌 GEO 诊断专家 </h2><p>GEO 诊断 Skill 上架到了 WorkBuddy 的专家市场，变成一个可以直接召唤的“品牌 GEO 诊断专家”，已经封装好一套诊断流程：从品牌输入、问题集设计、平台测试，到可见度、基建、竞品、舆情、路线图输出。</p><p><img src=\"images/case11-01.png\" alt=\"\" loading=\"lazy\"></p><h3 id=\"这个专家适合谁用\">这个专家适合谁用 </h3><ul><li><strong>产品团队</strong>：想知道产品在 AI 搜索里的可见度、竞品压力和内容短板。</li><li><strong>企业品牌</strong>：想知道公司是否被 AI 准确识别，官网和媒体资料是否足够可信。</li><li><strong>个人 IP / 自媒体</strong>：想知道自己的名字、账号、代表作品是否被 AI 正确召回。</li><li><strong>市场和增长团队</strong>：想把“发内容”变成有目标、有复测、有证据的 GEO 优化计划。</li></ul><h3 id=\"推荐输入材料\">推荐输入材料 </h3><table tabindex=\"0\"><thead><tr><th>输入项</th><th>为什么需要</th><th>示例</th></tr></thead><tbody><tr><td>官网 / 产品页</td><td>作为品牌事实的第一信源</td><td>官网、产品介绍页、定价页、帮助中心。</td></tr><tr><td>项目地址</td><td>技术产品需要证明活跃度和能力边界</td><td>GitHub、开源仓库、更新日志。</td></tr><tr><td>官方账号</td><td>让 AI 能识别权威发布渠道</td><td>公众号、知乎、掘金、小红书、B 站、视频号。</td></tr><tr><td>目标用户</td><td>问题集要从真实用户意图出发</td><td>开发者、企业管理者、内容创作者、采购负责人。</td></tr><tr><td>竞品名单</td><td>判断语义推荐位被谁占据</td><td>2-5 个已知竞品或替代方案。</td></tr></tbody></table><h2 id=\"geo-诊断\">GEO 诊断 </h2><p>GEO 诊断也可以先拆成一条稳定工作流。不要一上来就问“我的 GEO 怎么样”，而是让专家先把诊断范围、测试问题和评分口径说清楚。</p><figure class=\"wb-mermaid\" aria-label=\"流程图\" data-v-dbf03737><pre class=\"wb-mermaid__fallback\" data-v-dbf03737><code data-v-dbf03737>flowchart LR     A[确认品牌与官方资料] --&gt; B[建立用户真实问题集]     B --&gt; C[选择测试平台与采样口径]     C --&gt; D[记录提及率与回答准确性]     D --&gt; E[检查官网、内容矩阵与权威来源]     E --&gt; F[分析竞品、收录和舆情]     F --&gt; G[生成报告与 30/60/90 天行动计划] </code></pre><!----></figure><table tabindex=\"0\"><thead><tr><th>步骤</th><th>WorkBuddy 做什么</th><th>人要确认什么</th></tr></thead><tbody><tr><td>1</td><td>读取品牌官网、项目地址和公开资料。</td><td>哪些信息是官方事实，哪些只是参考资料。</td></tr><tr><td>2</td><td>生成一组用户真实问题，而不是只测品牌名。</td><td>这些问题是否真的来自目标用户的搜索意图。</td></tr><tr><td>3</td><td>在多个 AI 平台或搜索场景中测试品牌提及情况。</td><td>测试平台、采样次数、是否登录、测试日期。</td></tr><tr><td>4</td><td>分析 AIVO、用户画像、竞品、基建、舆情和收录。</td><td>每个分数能不能追溯到样本和证据。</td></tr><tr><td>5</td><td>输出 HTML / 飞书文档报告和优化路线图。</td><td>哪些行动先做，哪些结论需要人工复核。</td></tr></tbody></table><p><img src=\"images/case11-02.png\" alt=\"\" loading=\"lazy\"></p><h3 id=\"提示词示例-产品-geo-诊断\">提示词示例：产品 GEO 诊断 </h3><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>召唤“品牌 GEO 诊断专家”，帮我诊断 WeSight 这个产品的 GEO 情况。</span></span> <span class=\"line\"><span>官方资料：官网、开源项目地址、官方账号。</span></span> <span class=\"line\"><span>目标用户：需要统一管理多个 AI Agent、桌面工作流和开发工具的用户。</span></span> <span class=\"line\"><span>已知竞品：请先根据用户问题自动识别，再让我确认。</span></span> <span class=\"line\"><span>请先输出测试问题集、测试平台、采样次数、评分口径和局限，等待我确认后再执行。</span></span> <span class=\"line\"><span>最终输出：诊断概览、AIVO 评分、用户画像、搜索可见性、基建评估、竞品分析、收录效果、舆情分析和优化路线图。</span></span> <span class=\"line\"><span>无法重复验证的结果标为“样本观察”，不要写成绝对事实。</span></span></code></pre></div><p><img src=\"images/case11-03.png\" alt=\"\" loading=\"lazy\"></p><p><strong>可得到的结果</strong>：不是一句“GEO 做得好不好”，而是一份能拆解问题的报告。案例中，WeSight 的问题不是产品没有差异化，而是在测试样本里 AI 搜索可见度和竞品对比优势偏弱，导致综合得分被拖低。</p><h3 id=\"报告模块一-诊断概览与风险提示\">报告模块一：诊断概览与风险提示 </h3><p>诊断概览的作用是先给经营者一个全局判断：当前品牌总体表现如何、最主要风险是什么、哪些问题应该立刻处理。它不应该只给一个分数，而要解释分数从哪里来。</p><p><img src=\"images/case11-04.png\" alt=\"\" loading=\"lazy\"></p><table tabindex=\"0\"><thead><tr><th>概览里要看</th><th>为什么重要</th><th>如何复核</th></tr></thead><tbody><tr><td>综合评分</td><td>快速判断当前 GEO 基础水平</td><td>确认评分口径和测试样本，不把一次分数当永久结论。</td></tr><tr><td>关键发现</td><td>找到最影响结果的短板</td><td>每条发现都要能回到具体平台、具体问题、具体回答。</td></tr><tr><td>风险提示</td><td>提前发现会影响推荐的负面因素</td><td>区分事实风险、内容缺口和模型误解。</td></tr></tbody></table><p>比如 WeSight 仅支持 macOS Apple Silicon 这类产品边界，如果官网、README 和外部资料没有解释清楚，AI 可能会在推荐时附带限制提醒，甚至把它排除在部分用户需求之外。</p><h3 id=\"报告模块二-aivo-评分-看清短板在哪\">报告模块二：AIVO 评分，看清短板在哪 </h3><p>把 GEO 拆成四个维度：AI 搜索可见度、基建完善度、竞品对比优势、舆情健康度。这个拆法比单一总分更有价值，因为它能告诉你到底是“没人提你”，还是“有人提你但说不准”，或者“竞品资料更强”。</p><p><img src=\"images/case11-05.png\" alt=\"\" loading=\"lazy\"></p><table tabindex=\"0\"><thead><tr><th>维度</th><th>它衡量什么</th><th>低分时先做什么</th></tr></thead><tbody><tr><td>AI 搜索可见度</td><td>用户问相关问题时，品牌被提及的比例和位置。</td><td>补用户问题对应的内容页、对比页和场景页。</td></tr><tr><td>基建完善度</td><td>官网、官方账号、技术文档、权威来源是否完整。</td><td>修正官网事实、统一名称、补充结构化介绍。</td></tr><tr><td>竞品对比优势</td><td>同一条 query 下，AI 更容易推荐谁。</td><td>写清差异化、适用边界和与竞品的取舍。</td></tr><tr><td>舆情健康度</td><td>外部评价、负面信息、风险提示对推荐的影响。</td><td>处理真实问题，补充官方澄清和可信第三方证据。</td></tr></tbody></table><p>WeSight 的案例中，综合得分约 38 分；舆情健康度相对较好，但 AI 搜索可见度和竞品对比优势偏弱。这个结果说明问题不一定在产品本身，而在“用户提问语义”和“品牌内容供给”之间存在断层。</p><h3 id=\"报告模块三-用户画像与意图漏斗偏移\">报告模块三：用户画像与意图漏斗偏移 </h3><p>很多品牌做内容时只写自己想表达的卖点，但 GEO 更关心用户真实怎么问。公众号案例中，专家发现用户在大模型里更容易提出“有没有能统一管理多个 AI Agent 的桌面软件”这类问题。这意味着用户关心的是场景和任务，而不一定知道你的品牌名。</p><p><img src=\"images/case11-06.png\" alt=\"\" loading=\"lazy\"></p><h3 id=\"报告模块四-搜索可见性-提及率就是新的排名\">报告模块四：搜索可见性，提及率就是新的排名 </h3><p>在传统搜索里，用户至少还会看到一页链接；在 AI 搜索里，用户往往只看一段回答。品牌是否被提及、在什么位置被提及、是否被作为推荐项出现，就成了新的“搜索排名”。</p><p><img src=\"images/case11-07.png\" alt=\"\" loading=\"lazy\"></p><h3 id=\"报告模块五-数字基建-先让-ai-有可信资料可读\">报告模块五：数字基建，先让 AI 有可信资料可读 </h3><p>GEO 不是只靠“发声量”。生成式 AI 需要可引用、可验证、相互印证的可信来源。把基建评估拆成三类：官网评估、自媒体矩阵、权威媒体背书。</p><p><img src=\"images/case11-08.png\" alt=\"\" loading=\"lazy\"></p><h3 id=\"报告模块六-竞品分析-争的是语义心智份额\">报告模块六：竞品分析，争的是语义心智份额 </h3><p>GEO 的竞品分析不是简单列出市场竞品，而是看同一条用户问题下，AI 把推荐位给了谁。你和竞品争夺的不是网页排名，而是语义心智份额。</p><p><img src=\"images/case11-09.png\" alt=\"\" loading=\"lazy\"></p><h3 id=\"报告模块七-收录效果-最终看-ai-回答里有没有你\">报告模块七：收录效果，最终看 AI 回答里有没有你 </h3><p>收录效果可以理解为 GEO 的结果指标。前面的官网、内容矩阵、舆情、竞品分析最终都要落到一个问题：AI 回答里有没有你。</p><p><img src=\"images/case11-10.png\" alt=\"\" loading=\"lazy\"></p><p>这里最容易犯的错误，是只测品牌名。品牌名能被搜到，不代表用户问场景问题时会出现你。正确做法是把问题分层：</p><ul><li><strong>品牌名问题</strong>：某品牌是什么，官网是什么，是否开源。</li><li><strong>品类问题</strong>：某类工具有哪些，适合谁，怎么选。</li><li><strong>场景问题</strong>：我遇到某个具体任务，有什么产品能解决。</li><li><strong>对比问题</strong>：A 和 B 有什么区别，哪个更适合某类用户。</li></ul><h3 id=\"报告模块八-舆情分接绕开。\">报告模块八：舆情分接绕开。 </h3><p><img src=\"images/case11-11.png\" alt=\"\" loading=\"lazy\"></p><table tabindex=\"0\"><thead><tr><th>舆情类型</th><th>处理方式</th><th>注意事项</th></tr></thead><tbody><tr><td>真实产品问题</td><td>先修产品，再公开说明修复进展。</td><td>不要只做内容压制。</td></tr><tr><td>过期信息</td><td>在官网和权威渠道更新最新事实。</td><td>让新资料能被 AI 明确识别。</td></tr><tr><td>误解或谣言</td><td>用 FAQ、澄清文、第三方证据纠偏。</td><td>避免情绪化回应。</td></tr><tr><td>竞品对比劣势</td><td>明确适用边界和差异化场景。</td><td>不要把所有对比都写成“我最好”。</td></tr></tbody></table><h2 id=\"个人-ip-也可以做-geo-诊断\">个人 IP 也可以做 GEO 诊断 </h2><p>GEO 不只适合产品和企业，也适合个人 IP。用“苍何”做个人 IP 诊断，得到约 72 分，并用元宝做了额外搜索验证。</p><p><img src=\"images/case11-12.png\" alt=\"\" loading=\"lazy\"></p><h3 id=\"个人-ip-诊断要额外注意什么\">个人 IP 诊断要额外注意什么 </h3><ul><li><strong>身份消歧</strong>：同名人物很多，必须提供所在地、职业、代表作品、官方账号。</li><li><strong>平台分散</strong>：公众号、知乎、小红书、B 站、视频号的信息可能不一致。</li><li><strong>代表作品</strong>：AI 需要知道你最重要的作品、观点和标签。</li><li><strong>内容定位</strong>：个人 IP 不只是“被搜到”，还要看 AI 如何描述你。</li></ul><div class=\"language-text vp-adaptive-theme\"><button title=\"Copy Code\" class=\"copy\"></button><span class=\"lang\">text</span><pre class=\"shiki shiki-themes github-light github-dark vp-code\" tabindex=\"0\"><code><span class=\"line\"><span>召唤“品牌 GEO 诊断专家”，帮我诊断个人 IP 的 GEO 情况。</span></span> <span class=\"line\"><span>姓名 / 昵称：____。</span></span> <span class=\"line\"><span>身份消歧：所在地、职业、公司或组织、代表作品、官方账号。</span></span> <span class=\"line\"><span>目标问题：用户问哪些主题时，我希望被 AI 正确提到？</span></span> <span class=\"line\"><span>请测试品牌名问题、领域问题、作品问题和对比问题。</span></span> <span class=\"line\"><span>输出：可见度、身份准确性、代表作品识别、同名混淆风险、内容缺口和 30 天优化建议。</span></span></code></pre></div><h2 id=\"企业品牌诊断-不要为了-geo-而-geo\">企业品牌诊断，不要为了 GEO 而 GEO </h2><p>企业做 GEO 最容易走偏：还没诊断，就开始批量买内容、铺渠道、刷曝光。公众号案例里提到，给企业做 GEO 诊断时，真正重要的是先知道品牌在 AI 眼里是什么样：有没有被提及，是否被误解，风险在哪里，竞品为什么更容易被推荐。</p><h3 id=\"企业品牌建议重点检查\">企业品牌建议重点检查 </h3><table tabindex=\"0\"><thead><tr><th>检查项</th><th>关键问题</th><th>常见行动</th></tr></thead><tbody><tr><td>品牌基础事实</td><td>公司是谁，做什么，服务谁，核心优势是什么。</td><td>统一官网、百科、媒体稿、产品页的表达。</td></tr><tr><td>业务场景</td><td>用户问哪些业务问题时应该出现你。</td><td>补场景页、解决方案页、行业案例。</td></tr><tr><td>可信背书</td><td>有没有客户案例、媒体报道、行业评价。</td><td>建立可引用的公开资料矩阵。</td></tr><tr><td>负面与风险</td><td>AI 是否会提到负面、过期或错误信息。</td><td>处理真实问题，发布事实澄清和更新说明。</td></tr></tbody></table><h3 id=\"从诊断到行动-不要追求一次性刷高分\">从诊断到行动：不要追求一次性刷高分 </h3><p>一份 GEO 报告如果不能转成行动，就只是漂亮仪表盘。给出快速赢利点、优先行动建议和阶段路线图，比如补齐 GEO 曝光、处理舆情、优化可信来源等。</p><p><img src=\"images/case11-13.png\" alt=\"\" loading=\"lazy\"></p><p><img src=\"images/case11-14.png\" alt=\"\" loading=\"lazy\"></p><table tabindex=\"0\"><thead><tr><th>阶段</th><th>优先行动</th><th>复测方式</th></tr></thead><tbody><tr><td>30 天</td><td>修正官网、README、官方账号中的名称、定位、功能边界和过期信息。</td><td>重测品牌名问题和核心场景问题，检查回答准确性。</td></tr><tr><td>60 天</td><td>补用户真实 query 对应的场景页、对比页、案例页和 FAQ。</td><td>重测品类问题和场景问题，观察提及率变化。</td></tr><tr><td>90 天</td><td>建设外部可信来源：媒体报道、客户案例、社区讨论、行业观点。</td><td>检查引用来源多样性、竞品推荐位和舆情风险变化。</td></tr></tbody></table></div></div>"),
]

# ---------- 进阶篇（WorkBuddy 相关，不分区） ----------
ADVANCED = [
 ("chapter-22","01","把 SOP 沉淀为 Skill", "进阶篇",
  ch_body("你反复在干的那类活，值得固化成一个 Skill，下次一句话调用。",
   [('h3','沉淀路径'),
    ('ul',['写下标准流程（SOP）','整理成 SKILL.md：何时用、怎么做、注意什么','放进技能库，复用 + 迭代']),
    ('callout-info','除了自写，也可以把书和视频「蒸馏」成可执行 Skill。')])),
 ("chapter-23","02","多 Agent 协作工作流", "进阶篇",
  ch_body("复杂项目拆给多个专家 Agent 并行，再由一个总控汇总，效率与质量都上台阶。",
   [('ul',['内容生产：选题 / 写作 / 审核 三只虾协作','短视频：生产 Agent + 拆解 Agent 并行']),
    ('callout','设计原则：职责单一、接口清晰、人工在关键节点把关。')])),
 ("chapter-24","03","自动化可靠性实践", "进阶篇",
  ch_body("从「手动跑一次」到「定时稳定跑」，要处理失败、超时与通知。",
   [('h3','可靠性清单'),
    ('ul',['明确失败时的动作（通知而非静默）','设置重试与超时边界','保留可审计的运行日志']),
    ('callout-warn','老田偏好：任务失败时发企业微信消息通知，而不是静默失败或自动重试。')])),
 ("chapter-25","04","知识库双备份体系", "进阶篇",
  ch_body("交付物本地存一份，乐享知识库再存一份，防止单点丢失。",
   [('ul',['本地：实战笔记 / 月报系统目录','云端：乐享知识库对应空间','命名与结构两端保持一致']),
    ('callout','每次交付主动提醒：记得双备份。')])),
]

# ---------- 岗位与行业落地（按岗位 / 行业视角组织） ----------
INDUSTRY = [
 ("industry-1","01","销售岗位落地", "岗位落地",
  ch_body("把企业微信与 WorkBuddy 用在销售日常工作流中，提升跟进效率与转化。",
   [('h3','典型场景'),
    ('ul',['客户拜访纪要自动整理','销售日报与月报自动生成','客户需求跟踪与提醒']),
    ('callout-info','本栏目建设中，后续补充真实客户场景与 SOP。')])),
 ("industry-2","02","外贸岗位落地", "岗位落地",
  ch_body("面向外贸业务的询盘、报价、跟进与物流信息同步。",
   [('h3','典型场景'),
    ('ul',['询盘信息结构化提取','报价单与利润测算','多语言客户沟通草稿']),
    ('callout-info','以 Steinmann Metalltechnik GmbH 的 AlMg3 试单为例，逐步沉淀。')])),
 ("industry-3","03","零售行业落地", "行业落地",
  ch_body("零售门店的会员运营、社群运营与每日资讯推送。",
   [('h3','典型场景'),
    ('ul',['会员标签与分层运营','门店日报与数据汇总','鲜花/零售/政策资讯自动简报']),
    ('callout-info','结合老田每日资讯简报自动化实践。')])),
 ("industry-4","04","制造行业落地", "行业落地",
  ch_body("制造企业的内部协同、知识沉淀与订单数据对接。",
   [('h3','典型场景'),
    ('ul',['生产日报与异常提醒','WorkBuddy 对接麦德邻云系统抓订单数据','设备维保知识库']),
    ('callout-warn','客户数据与生产数据属敏感信息，处理前确认授权范围。')])),
]

# Home 文章卡片数据（product 用于筛选与色标）
HOME_ARTICLES = [
    # 使用手册（WB手册 1-11 章）
    ("使用手册","01","第 1 章 初识 WorkBuddy","从回答到交付的 AI 工作台","manual-wb.html#chapter-1"),
    ("使用手册","02","第 2 章 下载、安装、登录与更新","多端安装与常见问题","manual-wb.html#chapter-2"),
    ("使用手册","03","第 3 章 主界面、任务与工作区","三区域/三模式/模型选择","manual-wb.html#chapter-3"),
    ("使用手册","04","第 4 章 快速完成第一个任务","任务说明怎么写","manual-wb.html#chapter-4"),
    ("使用手册","05","第 5 章 加载一个真正用得上的 Skill","Skill 原理与使用","manual-wb.html#chapter-5"),
    ("使用手册","06","第 6 章 专家和专家团","召唤/创建专家与专家团","manual-wb.html#chapter-6"),
    ("使用手册","07","第 7 章 使用连接器","MCP 与连接器加载","manual-wb.html#chapter-7"),
    ("使用手册","08","第 8 章 接入小程序与 IM 助理","微信/飞书/钉钉接入","manual-wb.html#chapter-8"),
    ("使用手册","09","第 9 章 如何接入外部 API","开放能力扩展","manual-wb.html#chapter-9"),
    ("使用手册","10","第 10 章 自动化任务","从想法到定时任务","manual-wb.html#chapter-10"),
    ("使用手册","11","第 11 章 课外阅读：一章看懂 AI 工作系统","五类角色：模型·Agent·Skill·工具·人","manual-wb.html#chapter-11"),
    # 案例篇（WB案例）
    ("案例篇","01","第 1 章 从整理桌面文件这些小事做起","桌面发票扫描与台账生成","cases-wb.html#chapter-1"),
    ("案例篇","02","第 2 章 办公三件套：Word、Excel、PPT","三件套联动实战","cases-wb.html#chapter-2"),
    ("案例篇","03","第 3 章 远程控制你的电脑，不用发愁不在电脑前","小程序远程控制电脑实战","cases-wb.html#chapter-3"),
    ("案例篇","04","第 4 章 生活助手的价值，是减少琐碎","WB案例","cases-wb.html#chapter-4"),
 ("案例篇","05","第 5 章 资讯整合：把信息流变成每日通知","资讯整合：把信息流变成每日通知","cases-wb.html#chapter-5"),
 ("案例篇","06","第 6 章 收藏不是知识管理，能再次用起来才是","收藏不是知识管理，能再次用起来才是","cases-wb.html#chapter-6"),
 ("案例篇","07","第 7 章 会议结束不是终点，工作才刚刚开始","会议结束不是终点，工作才刚刚开始","cases-wb.html#chapter-7"),
 ("案例篇","08","第 8 章 把投资分析变成你的日常","把投资分析变成你的日常","cases-wb.html#chapter-8"),
 ("案例篇","09","第 9 章 一句话召唤 AI 视频团队","一句话召唤 AI 视频团队","cases-wb.html#chapter-9"),
 ("案例篇","10","第 10 章 自媒体不只是靠努力，而是一条增长闭环","自媒体不只是靠努力，而是一条增长闭环","cases-wb.html#chapter-10"),
 ("案例篇","11","第 11 章 WorkBuddy也能做GEO专家","WorkBuddy也能做GEO专家","cases-wb.html#chapter-11"),
    # 进阶篇
    ("进阶篇","01","把 SOP 沉淀为 Skill","把反复干的活固化成技能","advanced.html#chapter-22"),
    ("进阶篇","03","自动化可靠性实践","失败通知而非静默","advanced.html#chapter-24"),
    # 岗位与行业落地（industry 4 章）
    ("岗位与行业落地","01","销售岗位落地","客户拜访纪要、销售日报、需求跟踪","industry.html#industry-1"),
    ("岗位与行业落地","02","外贸岗位落地","询盘提取、报价测算、多语言沟通","industry.html#industry-2"),
    ("岗位与行业落地","03","零售行业落地","会员运营、门店日报、资讯简报","industry.html#industry-3"),
    ("岗位与行业落地","04","制造行业落地","生产日报、订单对接、维保知识库","industry.html#industry-4"),
]

SKILL_CATEGORIES = ["全部", "写作排版", "内容生产", "数据分析", "自动化", "企业微信", "销售获客", "文件与知识管理", "法务合规", "人力资源", "财务行政", "产品营销", "协作办公", "金融", "设计", "开发"]

# ============================ AI 提示词社区（参照 simouxuan.com/skills.html 的「AI 提示词社区」模块） ============================
PROMPT_CATEGORIES = ["全部", "内容创作", "开发", "教育", "效率工具", "AI绘画"]
PROMPTS = [
  {"id":"p1","ico":"📝","title":"公众号文章自动写作与发布","category":"内容创作",
   "desc":"你是一位资深的公众号内容策划师和写手，具备10年以上新媒体运营经验，擅长商业深度、案例驱动的写作风格。\n\n你的任务是根据用户提供的主题，撰写一篇1500-3000字的公众号文章。要求：标题吸引眼球但不标题党，开头3秒抓住读者，正文逻辑清晰、案例丰富，结尾有行动号召。",
   "example":"帮我写一篇关于AI提效工具的公众号文章，目标读者是中小企业老板",
   "author":"老田·2026/07/15","views":892},
  {"id":"p2","ico":"🛒","title":"小鹅通课程数据智能分析","category":"效率工具",
   "desc":"你是一位小鹅通平台运营专家和数据分析师，精通课程销售数据解读、用户画像构建和推广策略优化。\n\n你的任务是分析小鹅通店铺的课程销售数据，生成包含以下内容的分析报告：1)销售趋势图表描述 2)TOP5热门课程排名 3)用户画像分析 4)改进建议和推广策略。",
   "example":"帮我分析上个月的课程销售数据，看看哪些课程卖得好，用户主要是什么群体",
   "author":"老田·2026/07/14","views":645},
  {"id":"p3","ico":"🤖","title":"WorkBuddy Skill 技能搭建指南","category":"开发",
   "desc":"你是一位WorkBuddy技能开发专家，精通SKILL.md编写、技能架构设计和部署流程。\n\n你的任务是指导用户从零搭建一个WorkBuddy Skill。包括：1)确定技能功能和适用场景 2)编写SKILL.md文件 3)设计技能目录结构 4)编写核心逻辑脚本 5)测试和部署上线。",
   "example":"我想做一个自动生成周报的Skill，每周五下午自动收集本周工作内容并生成报告",
   "author":"老田·2026/07/13","views":1203},
  {"id":"p4","ico":"📚","title":"IMA 知识库智能问答搭建","category":"效率工具",
   "desc":"你是一位知识管理专家，精通IMA OpenAPI的使用，能够将文档、网页、笔记等知识源整合到知识库中，实现基于内容的智能问答。\n\n你的任务是帮助用户搭建IMA知识库智能问答系统。步骤：1)获取IMA OpenAPI凭证 2)创建知识库 3)导入文档和网页 4)配置问答权限 5)测试智能搜索和问答效果。",
   "example":"我有100多份行业报告PDF，想做一个可以随时提问的知识库",
   "author":"老田·2026/07/12","views":534},
  {"id":"p5","ico":"🎨","title":"AI 绘画提示词工程模板","category":"AI绘画",
   "desc":"你是一位AI绘画提示词工程师，精通Midjourney、Stable Diffusion等主流AI绘画工具的提示词编写，擅长风格控制、构图设计和细节描述。\n\n你的任务是根据用户的需求描述，生成结构化的AI绘画提示词。输出格式：1)画面主体描述 2)风格设定 3)色彩方案 4)构图布局 5)光影效果 6)质量参数 7)负面提示词。",
   "example":"帮我生成一张赛博朋克风格的城市夜景，要有霓虹灯和飞行器",
   "author":"老田·2026/07/11","views":1567},
  {"id":"p6","ico":"📊","title":"Excel 数据自动化处理专家","category":"效率工具",
   "desc":"你是一位Excel数据处理专家，精通VBA、Power Query、数据透视表等高级功能，能够自动化处理各种复杂的数据清洗、转换和分析任务。\n\n你的任务是根据用户提供的数据处理需求，编写完整的自动化处理方案。包括：1)数据清洗规则 2)处理步骤说明 3)VBA/Python代码 4)输出格式设计 5)异常处理方案。",
   "example":"我有一个包含5000行销售数据的Excel，需要按地区汇总、去重、生成图表",
   "author":"老田·2026/07/10","views":789},
  {"id":"p7","ico":"🗣️","title":"会议纪要自动生成与分发","category":"效率工具",
   "desc":"你是一位会议管理专家，能够从会议录音转写文本中提取关键信息，生成结构化的会议纪要，并自动分发给参会人员。\n\n你的任务是处理会议转写文本，生成标准会议纪要。输出包含：1)会议基本信息 2)参会人员 3)议题摘要 4)决议事项 5)待办任务（含负责人和截止日期）6)下次会议安排。",
   "example":"这是一场产品评审会的录音转写文本，帮我生成会议纪要并发送给相关人",
   "author":"老田·2026/07/09","views":456},
  {"id":"p8","ico":"💡","title":"商业计划书智能撰写","category":"内容创作",
   "desc":"你是一位资深的商业计划书撰写顾问，具备投资银行和咨询公司背景，擅长从零开始构建完整的商业计划书。\n\n你的任务是根据用户的创业项目描述，撰写一份完整的商业计划书。包含：1)执行摘要 2)公司介绍 3)市场分析 4)产品/服务描述 5)商业模式 6)营销策略 7)团队介绍 8)财务预测 9)融资计划。",
   "example":"我在做一个AI教育平台，面向K12学生，想融资500万，帮我写商业计划书",
   "author":"老田·2026/07/08","views":1023},
  {"id":"p9","ico":"🔧","title":"代码审查与优化助手","category":"开发",
   "desc":"你是一位资深的全栈开发工程师，精通多种编程语言和框架，具备代码审查、性能优化、安全漏洞检测的专业能力。\n\n你的任务是对用户提供的代码进行全面审查。输出包含：1)代码质量评分 2)潜在Bug列表 3)安全漏洞检测 4)性能优化建议 5)代码规范检查 6)重构建议 7)优化后的代码。",
   "example":"帮我审查这段Python爬虫代码，看看有什么问题和优化空间",
   "author":"老田·2026/07/07","views":678},
  {"id":"p10","ico":"🎓","title":"教育培训课程设计","category":"教育",
   "desc":"你是一位教育培训课程设计师，具备10年以上课程开发经验，擅长将复杂知识体系化、模块化，设计互动性强的教学方案。\n\n你的任务是根据用户的教学主题和目标受众，设计完整的课程方案。包含：1)课程大纲 2)学习目标 3)教学模块划分 4)每个模块的教案 5)互动练习设计 6)考核评估方案 7)教学材料清单。",
   "example":"我要给企业员工做一场AI工具提效培训，半天时间，50人参加",
   "author":"老田·2026/07/06","views":412},
  {"id":"p11","ico":"📱","title":"小红书爆款文案生成","category":"内容创作",
   "desc":"你是一位小红书运营专家和爆款文案写手，深谙平台算法和用户心理，擅长写出高互动率的种草文案。\n\n你的任务是根据用户提供的产品或主题，生成小红书爆款文案。输出包含：1)吸引眼球的标题（20字以内）2)正文文案（含emoji和分段）3)话题标签（8-10个）4)配图建议 5)发布时间建议。",
   "example":"帮我写一篇推荐AI写作工具的小红书文章，目标读者是自媒体创作者",
   "author":"老田·2026/07/05","views":1342},
  {"id":"p12","ico":"🔍","title":"SEO 优化策略生成器","category":"开发",
   "desc":"你是一位SEO优化专家，精通搜索引擎算法、关键词策略、内容优化和技术SEO，能够为网站制定全面的搜索优化方案。\n\n你的任务是根据用户的网站信息和目标，生成完整的SEO优化策略。包含：1)关键词分析 2)竞品分析 3)站内优化建议 4)内容策略 5)外链建设方案 6)技术SEO检查清单 7)效果追踪指标。",
   "example":"我的电商网站卖手工皮具，想在百度和Google上排名靠前",
   "author":"老田·2026/07/04","views":389},
  {"id":"p13","ico":"🎬","title":"短视频脚本分镜设计","category":"内容创作",
   "desc":"你是一位短视频创作导演和编剧，精通抖音、B站等平台的视频内容策划，擅长设计节奏紧凑、情绪饱满的分镜脚本。\n\n你的任务是根据用户的视频主题，设计完整的分镜脚本。输出包含：1)视频风格设定 2)角色设定 3)逐镜头描述（含时间码、画面描述、镜头运动、旁白/台词）4)BGM建议 5)字幕样式 6)发布文案。",
   "example":"帮我设计一个2分钟的AI科技产品开箱视频脚本",
   "author":"老田·2026/07/03","views":967},
  {"id":"p14","ico":"🌐","title":"多语言翻译与本地化","category":"效率工具",
   "desc":"你是一位专业的翻译和本地化专家，精通中英日韩等多种语言，能够处理技术文档、营销文案、法律文件等不同类型的内容翻译。\n\n你的任务是将用户提供的原文翻译为目标语言，并进行本地化适配。输出包含：1)翻译文本 2)本地化调整说明 3)文化注意事项 4)专业术语对照表 5)翻译质量自检报告。",
   "example":"帮我把这份产品说明书从中文翻译成英文和日文",
   "author":"老田·2026/07/02","views":298},
  {"id":"p15","ico":"📈","title":"社交媒体运营日历生成","category":"内容创作",
   "desc":"你是一位社交媒体运营总监，精通多平台内容规划和排期管理，能够根据品牌调性和用户画像制定系统化的内容发布策略。\n\n你的任务是根据用户的品牌信息和目标，生成一个月的社交媒体运营日历。包含：1)内容主题规划 2)每日发布内容概要 3)平台适配建议 4)互动策略 5)热点借势计划 6)数据追踪指标。",
   "example":"我的品牌是卖健康轻食的，需要一个月的小红书和抖音内容规划",
   "author":"老田·2026/07/01","views":723},
  {"id":"p16","ico":"🧪","title":"科研论文写作辅助","category":"教育",
   "desc":"你是一位学术研究方法论专家和论文写作导师，具备丰富的SCI/SSCI论文发表经验，擅长指导研究设计、文献综述和论文结构优化。\n\n你的任务是辅助用户完成科研论文写作。包括：1)研究问题梳理 2)文献综述框架 3)研究方法设计 4)数据分析方案 5)论文结构大纲 6)摘要和关键词撰写 7)参考文献格式规范。",
   "example":"我要写一篇关于AI在教育领域应用的综述论文，目标期刊是SSCI",
   "author":"老田·2026/06/30","views":545},
  {"id":"p17","ico":"🎯","title":"用户画像与需求分析","category":"开发",
   "desc":"你是一位产品经理和用户研究专家，精通用户画像构建、需求挖掘和产品策略制定，擅长从数据中洞察用户行为模式。\n\n你的任务是根据用户提供的数据或描述，构建详细的用户画像。输出包含：1)人口统计特征 2)行为习惯分析 3)痛点与需求 4)使用场景 5)决策路径 6)用户分层建议 7)产品优化方向。",
   "example":"我们的APP用户主要是25-35岁的城市白领，想了解他们的核心需求",
   "author":"老田·2026/06/29","views":421},
  {"id":"p18","ico":"🎪","title":"活动策划方案生成","category":"内容创作",
   "desc":"你是一位资深活动策划师，拥有丰富的线上线下活动组织经验，擅长创意策划、流程设计和资源协调。\n\n你的任务是根据用户的活动需求，生成完整的活动策划方案。包含：1)活动主题和定位 2)目标人群分析 3)活动流程设计 4)场地和物料清单 5)预算预估 6)人员分工 7)宣传推广方案 8)应急预案。",
   "example":"公司要办一场200人的年会，预算10万，主题是AI未来",
   "author":"老田·2026/06/28","views":567},
  {"id":"p19","ico":"💼","title":"简历优化与面试准备","category":"教育",
   "desc":"你是一位资深HR和职业规划顾问，拥有500强企业招聘经验，精通简历优化、面试技巧培训和职业发展指导。\n\n你的任务是帮助用户优化简历并准备面试。输出包含：1)简历问题诊断 2)优化后的简历 3)面试常见问题预测 4)回答策略和话术 5)薪资谈判技巧 6)职业发展建议。",
   "example":"我有5年产品经理经验，想跳槽到大厂，帮我优化简历和准备面试",
   "author":"老田·2026/06/27","views":1189},
  {"id":"p20","ico":"🏗️","title":"系统架构设计咨询","category":"开发",
   "desc":"你是一位资深系统架构师，精通微服务、云原生、分布式系统设计，能够为不同规模的业务提供技术架构方案。\n\n你的任务是根据用户的业务需求，设计系统架构方案。包含：1)架构概述 2)技术选型 3)模块划分 4)数据流设计 5)接口定义 6)部署方案 7)性能和安全考量 8)扩展性规划。",
   "example":"我们要开发一个日均10万DAU的电商小程序，需要设计后端架构",
   "author":"老田·2026/06/26","views":503},
]

SKILLS = [
{
  "id":"tianwei-word-formatter",
  "ico":"📄",
  "title":"公文标准排版 v1.3",
  "desc":"所有 Word 文档统一采用公文标准 + 1.5 倍行距：大标题方正小标宋、一级标题黑体、正文仿宋。",
  "category":"写作排版",
  "status":"已落地",
  "hot":True,
  "overview":"将 Markdown 或纯文本内容按 GB/T 9704 路线一键排版为 Word：大标题方正小标宋简体二号、一级标题黑体三号、二级标题楷体_GB2312、正文仿宋_GB2312四号，1.5 倍行距，页边距上37mm/下35mm/左28mm/右26mm。<br>⚠️ 注意事项：<br>① 正式公文含落款与数据，生成后务必人工复核无误；<br>② 字体依赖本机安装，缺字体时自动回退，首次用测试文档验证效果；<br>③ 技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "在 WorkBuddy 技能市场搜索「tianwei-word-formatter」",
    "一键加载到当前任务或加入全局技能库",
    "确保系统已安装方正小标宋、仿宋_GB2312、楷体_GB2312（缺字体时自动回退宋体/楷体/仿宋）",
    "首次使用先用测试文档验证字体回退与页边距效果"
  ],
  "steps":[
    "用 Markdown 准备正文：# 大标题、## 一级标题、### 二级标题、正文段落",
    "输入指令：「用公文标准排版把以下内容生成 Word」",
    "检查页边距、行距、标题层级与页脚页码",
    "保存 .docx 并双备份到本地 + 乐享知识库"
  ],
  "example":"用公文标准排版生成一份《企业微信管理员培训方案》Word 文档，包含培训背景、课程大纲、实操演练、考核方式四个部分，落款右对齐。",
  "scenarios":[
    "月度/年度工作汇报快速成文",
    "客户培训方案、实施方案正式交付",
    "内部通知、会议纪要等公文样式文档"
  ]
},
{
  "id":"tianwei-style",
  "ico":"✍️",
  "title":"老田写作风格",
  "desc":"融合多写作技能精华的四档语域切换，去 AI 味、五步成文。",
  "category":"写作排版",
  "status":"已落地",
  "hot":False,
  "overview":"把通用 AI 输出转换成老田的口吻：日常闲聊、工作讨论、正式交付、散文四档语域自动切换；内置 11 维风格量化、去 AI 味规则、五步写作框架与平台适配（公众号/小红书/知乎/头条）。<br>⚠️ 注意事项：<br>① 风格模仿用于辅助草稿，对外正式交付前仍须人工把关语气与事实；<br>② 涉及具体数据/客户名时 AI 可能编造，须核对；<br>③ 技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "在 WorkBuddy 技能市场搜索「tianwei-style」",
    "加载后输入 /skill 激活老田风格模式",
    "告诉它当前场景（日常/工作/正式/散文）与目标平台",
    "首次使用可先用一段自己的旧文做风格校准"
  ],
  "steps":[
    "明确文章主题、目标读者与发布平台",
    "输入指令：「用我的风格写一篇关于 XX 的文章，语域：工作讨论」",
    "AI 按选题→大纲→初稿→润色→平台改写五步输出",
    "对不满意段落圈出来要求「再老田一点」或「更正式」"
  ],
  "example":"用我的风格写一篇关于「企业微信客户联系功能」的工作讨论文，面向销售团队，要求口语化、有网感但不浮夸，800 字左右。",
  "scenarios":[
    "朋友圈/社群推广文案快速出稿",
    "公众号、小红书、知乎多平台改写",
    "商务邮件、方案前言去 AI 味润色"
  ]
},
{
  "id":"monthly-report",
  "ico":"🗓️",
  "title":"月度报告生成",
  "desc":"日报聚合 → 月报 → 企微群 + 邮件推送，每月最后一天自动触发。",
  "category":"自动化",
  "status":"运行中",
  "hot":True,
  "overview":"基于固定格式的日报（YYYY-MM/YYYY-MM-DD.md），月底自动汇总工作事项、产出成果与下月计划，生成公文标准排版月报，并推送到企业微信群与 QQ 邮箱。<br>⚠️ 注意事项：<br>① 月报含业务数据，推送前确认接收群与邮箱的成员范围及权限；<br>② 自动化失败会按设置通知，勿静默重试；<br>③ 技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "确认日报目录结构：月报系统/YYYY-MM/YYYY-MM-DD.md",
    "配置自动化任务 automation-1782695947091，每月最后一天 18:00 触发",
    "绑定企微群 webhook key 与 QQ 邮箱 alias_id",
    "设置失败通知到企业微信，而非静默重试"
  ],
  "steps":[
    "每天按模板填写日报",
    "月底自动化脚本读取当月所有日报",
    "聚合关键成果、数据与待办，生成月报 Word",
    "自动上传文件到企微群并发送邮件副本"
  ],
  "example":"运行月报自动化，生成本月工作月报并推送到「销售团队」企微群和你的 QQ 邮箱。",
  "scenarios":[
    "销售/顾问岗位月度汇报",
    "项目团队月底复盘",
    "个人工作日志自动归档"
  ]
},
{
  "id":"wecom-doc",
  "ico":"💼",
  "title":"企微文档管理",
  "desc":"新建 / 读取 / 覆写企业微信在线文档，打通团队知识沉淀。",
  "category":"企业微信",
  "status":"已落地",
  "hot":False,
  "overview":"通过 wecomcli-doc 连接器操作企业微信在线文档：按 docid 或文档 URL 读取 Markdown 内容、覆写正文、新建空白文档。适合把本地报告同步到团队知识库。<br>⚠️ 注意事项：<br>① 覆写会覆盖原文，操作前先本地备份；<br>② 确认账号有目标文档编辑权限，避免越权；<br>③ 技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "确保 WorkBuddy 已安装并授权 wecom 连接器",
    "在技能市场加载「企业微信文档」skill",
    "确认当前账号有目标文档的编辑权限",
    "测试读取一篇已有文档验证连通性"
  ],
  "steps":[
    "提供文档 URL 或 docid",
    "输入读取/覆写/新建指令",
    "核对转换后的 Markdown 与原文格式",
    "覆写前建议先本地备份"
  ],
  "example":"读取这篇企微文档 https://work.weixin.qq.com/... 的内容，提取要点后更新到本地月报。",
  "scenarios":[
    "团队周报/月报统一归档到企微文档",
    "客户交付物云端双备份",
    "会议纪要在线协同编辑"
  ]
},
{
  "id":"qq-mail",
  "ico":"📧",
  "title":"QQ 邮箱操作",
  "desc":"看邮件、发邮件、附件下载，含 SendMessage 规范与两步确认。",
  "category":"企业微信",
  "status":"已落地",
  "hot":False,
  "overview":"通过 qq-mail 连接器收发 QQ 邮件。发送遵循老田规范：先 GetMe 取 alias_id、分两步走（Phase 1 拿 confirmation_token，Phase 2 发送）、正文控制在 500 字以内、to 字段只传 email。<br>⚠️ 注意事项：<br>① confirmation_token 有效期 5 分钟，超时需重新走 Phase 1；<br>② 正文超 500 字时分段或转附件，避免发送失败；<br>③ 技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "确保 WorkBuddy 已授权 qq-mail 连接器",
    "加载「qq-mail」skill",
    "首次发送前调用 GetMe 获取最新 alias_id",
    "确认 QQ 邮箱在网页端已登录且可用"
  ],
  "steps":[
    "发邮件前先调用 GetMe 刷新 alias_id",
    "Phase 1：不带 confirmation_token 获取 token",
    "Phase 2：5 分钟内携带 token 正式发送",
    "正文超过 500 字时分段或转附件"
  ],
  "example":"给 zhangsan@example.com 发一封邮件，主题是「月报已生成」，正文 300 字以内，附件为本月月报.docx。",
  "scenarios":[
    "月报、日报自动邮件抄送",
    "客户正式交付物发送",
    "群发通知但需控制正文长度"
  ]
},
{
  "id":"wecomcli-msg",
  "ico":"💬",
  "title":"企微消息",
  "desc":"会话列表、消息记录、多媒体获取与发送。",
  "category":"企业微信",
  "status":"已落地",
  "hot":False,
  "overview":"通过 wecomcli-msg 连接器拉取企业微信会话与消息记录，支持文本/图片/文件/语音/视频类型；也可向指定会话发送文本消息，常用于自动化简报推送。<br>⚠️ 注意事项：<br>① 拉取会话涉及隐私，仅用于授权范围内的群/会话；<br>② 发送文件需先 upload_media 取 media_id（3 天有效），超期重传；<br>③ 技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "确保 WorkBuddy 已授权 wecom 连接器",
    "加载「wecomcli-msg」skill",
    "确认机器人账号在目标群/会话中",
    "测试拉取最近 10 条消息验证权限"
  ],
  "steps":[
    "指定会话或群名称",
    "选择拉取记录或发送消息",
    "如发送文件，先通过 upload_media 获取 media_id",
    "检查消息是否成功到达"
  ],
  "example":"拉取「销售团队」群最近 50 条消息，汇总今日客户反馈与待办。",
  "scenarios":[
    "每日资讯简报自动推送到企微群",
    "多群消息汇总成日报",
    "客户群关键信息自动提取"
  ]
},
{
  "id":"tianwei-work-report",
  "ico":"📋",
  "title":"工作汇报系统",
  "desc":"3 分钟口述日报 → YAML 结构化存储 → 月底全自动出月报 → Word 附件 + 企微 webhook 双通道推送。",
  "category":"自动化",
  "status":"已落地",
  "hot":True,
  "overview":"面向销售/商务岗的日报→月报全自动化管线：口语输入自动转结构化日报（销售专属字段：电话/微信/拜访/商机/成交），月底从当月所有日报自动汇总月报，公文标准排版出 Word，QQ 邮箱附件 + 企微群 webhook 双通道推送。区分事实/推断/待补充，标注不确定性。<br>⚠️ 注意事项：<br>① 含销售/客户数据，确认接收端（企微群+邮箱）权限；<br>② 口语输入转结构化，关键数字口述后建议核对；<br>③ 技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "在技能库加载「tianwei-work-report」skill",
    "确认日报存储目录与 YAML 字段模板",
    "绑定企微群 webhook key 与 QQ 邮箱",
    "配合月底自动化任务定时触发月报生成"
  ],
  "steps":[
    "每天口述式输入：「填日报：今天打了 20 个电话，拜访 2 家…」",
    "AI 自动抽取字段生成结构化日报存档",
    "月底说「生成月报」或等自动化触发",
    "月报 Word 自动推送到企微群 + 邮箱"
  ],
  "example":"填日报：今天电话 18 个，加微信 5 个，拜访了瑞升工贸聊 WorkBuddy 方案，新增商机 1 个预计下月签。",
  "scenarios":[
    "销售/商务顾问的日常汇报减负",
    "月底述职材料自动成文",
    "团队管理者收集统一格式日报"
  ]
},
{
  "id":"sanzhixia",
  "ico":"🦐",
  "title":"三只虾内容流水线",
  "desc":"选题虾 → 文案虾 → 审核虾：选题挖掘、成文改写、6 维度审核门禁，问题清零才放行。",
  "category":"内容生产",
  "status":"已落地",
  "hot":True,
  "overview":"内容生产三技能流水线：选题虾负责从口水稿/热点/主题挖掘选题并入选题库；文案虾负责大纲→初稿→Humanizer 去 AI 味润色→多平台改写（公众号/小红书/知乎/头条）；审核虾做 6 维度质量门禁（标题吸引力/小标题简洁性/数据准确性/逻辑/表达/废话清除），P0=0 且 P1≤2 才放行归档。<br>⚠️ 注意事项：<br>① 审核虾 P0=0 且 P1≤2 才放行，勿为赶工跳过门禁；<br>② AI 生成内容含数据/案例须人工核实，长文多平台改写消耗 token 注意成本；<br>③ 技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "在技能库依次加载「选题虾」「文案虾」「审核虾」",
    "配合 humanizer 技能做去 AI 味润色",
    "设定选题库与文章归档目录",
    "首次使用先跑一篇短文验证全链路"
  ],
  "steps":[
    "「选题虾，根据我的口水稿出 5 个选题」",
    "选定后「文案虾，基于选题 2 写公众号长文」",
    "文案虾完成后自动触发审核虾 6 维度审核",
    "问题清零后归档，可追加多平台改写"
  ],
  "example":"选题虾，围绕「企业微信客户流失预警」抓 3 个热点选题；选定后让文案虾出公众号版和小红书版。",
  "scenarios":[
    "公众号/小红书/知乎多平台内容量产",
    "产品推广软文批量生产",
    "个人 IP 内容日更管线"
  ]
},
{
  "id":"excel-to-html-report",
  "ico":"📊",
  "title":"Excel 数据可视化报告",
  "desc":"xlsx 一键分析：维度统计、TOP 排名、环比增长、下滑预警，产出单文件离线 HTML 报告。",
  "category":"数据分析",
  "status":"已落地",
  "hot":True,
  "overview":"pandas 跑完全部统计（groupby 排名、月份环比 pct_change、品类×月份透视找持续下滑），生成单文件 HTML：KPI 卡片 + 柱状图 + 双轴折线 + 饼图 + 下滑预警表 + 可执行建议。Chart.js 内嵌不依赖 CDN，离线可打开；数字全部来自脚本输出，禁止心算。<br>⚠️ 注意事项：<br>① 数字全部来自脚本输出，禁止心算/估算；<br>② Chart.js 已内嵌不依赖 CDN，离线可打开，勿改回 CDN 引用；<br>③ 技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "在技能库加载「excel-to-html-report」skill",
    "确认虚拟环境已装 pandas / openpyxl",
    "下载 chart.umd.min.js 内嵌（禁用 CDN 引用）",
    "用样例表跑一次验证图表完整渲染"
  ],
  "steps":[
    "提供 xlsx 文件并说明分析诉求（维度/排名/环比）",
    "脚本预览 sheet 结构后一段跑完全部统计",
    "生成 KPI + 三图 + 预警表 + 结论建议的 HTML",
    "验证 canvas 与 Chart 实例完整后交付"
  ],
  "example":"分析这份 Q2 销售明细.xlsx：按区域和品类统计、给 TOP10 排名、算月环比、找出持续下滑的品类，生成 HTML 报告。",
  "scenarios":[
    "季度/月度销售数据复盘",
    "给客户演示的业务数据可视化",
    "多 sheet 明细表快速出结论"
  ]
},
{
  "id":"wecom-group-push",
  "ico":"🤖",
  "title":"企微群机器人推送",
  "desc":"webhook 群机器人发 markdown / 文件：Python urllib 上传取 media_id，绕开 curl 空响应坑。",
  "category":"企业微信",
  "status":"已落地",
  "hot":False,
  "overview":"通过企微群 webhook 推送报表与文件的标准做法：markdown 消息群内直接渲染关键数据；文件推送两步走——先 upload_media 取 media_id（3 天有效）再发 file 消息。关键坑：Git Bash 下 curl -F 上传返回空响应，必须用 Python urllib 原生 multipart 上传。<br>⚠️ 注意事项：<br>① 文件类型群内不渲染，成员需下载后用浏览器查看；<br>② media_id 仅 3 天有效，超期需重新 upload_media；<br>③ webhook key 属敏感信息勿泄露公开仓库，技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "在目标企微群添加群机器人，获取 webhook key",
    "在技能库加载「wecom-group-push」skill",
    "准备 Python urllib multipart 上传脚本",
    "先发一条测试 markdown 验证 key 可用"
  ],
  "steps":[
    "关键数据整理成 markdown 消息直接推送",
    "文件先用 Python 脚本 upload_media 取 media_id",
    "再 POST send 发 file 类型消息",
    "群成员下载附件用浏览器查看全貌"
  ],
  "example":"把这份月度经营分析.html 推送到「销售团队」企微群，并同步发一条 markdown 摘要列出三个关键指标。",
  "scenarios":[
    "月报/周报定时推送到客户群",
    "HTML 报告文件分发",
    "自动化任务的结果通知"
  ]
},
{
  "id":"wecom-image-briefing",
  "ico":"🖼️",
  "title":"企微图片简报",
  "desc":"Markdown 资讯 → 深色竖版长图 + 可点击链接消息组合推送，好看且可点。",
  "category":"企业微信",
  "status":"已落地",
  "hot":False,
  "overview":"解决企微群 image 消息内链接不可点的问题：Pillow 自动把 Markdown 简报渲染成深色竖版长图（编号徽章、来源标签），先发图片消息保证视觉冲击，再补一条 markdown 链接汇总消息保证每条资讯可点击跳转原文。<br>⚠️ 注意事项：<br>① image 消息内链接不可点，须配 markdown 链接消息补全跳转；<br>② 长图清晰度依赖源 Markdown 与配图质量；<br>③ 技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "在技能库加载「wecom-image-briefing」skill",
    "确认 Python 环境已装 Pillow",
    "按约定准备 Markdown 源文件（标题/摘要/原文链接）",
    "绑定目标群 webhook key"
  ],
  "steps":[
    "整理当日资讯为「简报名称_YYYY-MM-DD.md」",
    "运行 daily_briefing.py 生成竖版长图",
    "脚本自动推送长图 + markdown 链接消息",
    "群内核对图片清晰度与链接可点性"
  ],
  "example":"把今天的鲜花行业速览.md 做成长图简报推送到客户群，要求每条资讯的原文链接可点击。",
  "scenarios":[
    "每日晨报/行业速览群推送",
    "带视觉封面的资讯汇总",
    "活动通知的图文组合触达"
  ]
},
{
  "id":"note-capture",
  "ico":"📝",
  "title":"随手记 note-capture",
  "desc":"「帮我记住」「记一笔」一句话触发，自动归档到个人写作系统，可检索可回看。",
  "category":"文件与知识管理",
  "status":"已落地",
  "hot":False,
  "overview":"对话中流露保存/记忆/提醒意图即自动触发：内容写入个人写作系统 Markdown 库，自动判断类型并记录标题、类型标签、创建时间、来源对话摘要与正文；含链接时额外抓取摘要一并保存，存好后一句话告知。<br>⚠️ 注意事项：<br>① 触发词可能误触发，重要事项建议二次确认已归档；<br>② 链接类会自动抓摘要，注意来源网页可访问性；<br>③ 技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "在技能库加载「note-capture」skill",
    "设定写作系统根目录（content 文件夹）",
    "确认触发词表（帮我记住/记一笔/提醒我等）",
    "试存一条验证文件命名与归档结构"
  ],
  "steps":[
    "对话中说「帮我记住 XX」或「这个值得记录」",
    "AI 自动判断类型（笔记/灵感/待办/资源）",
    "结构化写入写作系统对应目录",
    "回一句确认，不打断当前对话"
  ],
  "example":"帮我记住：瑞升工贸的 IT 负责人下周三上午有空，拜访时重点聊云服务器迁移成本。",
  "scenarios":[
    "客户沟通要点随手归档",
    "灵感与选题素材积累",
    "口头待办不遗漏"
  ]
},
{
  "id":"dormant-customer-activation",
  "ico":"🎯",
  "title":"沉睡客户激活包",
  "desc":"按行业生成激活方案 + 钩子资料 + 话术 + 测试名单追踪表，价值先行不硬推销。",
  "category":"销售获客",
  "status":"已落地",
  "hot":False,
  "overview":"针对企微好友多但转化低的 B 端销售场景：按行业设计激活钩子资料（Word/PDF 指南）、分层触达话术和 Excel 测试追踪表。核心原则：价值先行、分层触达、先选 50~100 人小步测试、数据驱动迭代（发送/回复/意向/成交全程记录）。<br>⚠️ 注意事项：<br>① 先小步测试 50~100 人、数据驱动迭代，避免大规模硬推；<br>② 话术与钩子资料发送须符合企微频率与合规规则；<br>③ 技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "在技能库加载「dormant-customer-activation」skill",
    "梳理现有沉睡好友规模与主攻行业",
    "确认历史成交客户画像",
    "准备好企微侧发送通道"
  ],
  "steps":[
    "确认行业与销售现状（卡在找不到/聊不动/成交难）",
    "生成行业钩子资料：《行业+痛点+可量化结果+方法》",
    "输出分层激活话术与跟进 SOP",
    "用追踪表跑 50~100 人测试，按数据迭代"
  ],
  "example":"我企微里有 800 个制造业沉睡好友，帮我做一套激活包：钩子资料、首触话术和测试追踪表。",
  "scenarios":[
    "企微存量好友二次激活",
    "新产品线向老客户渗透",
    "代理商销售团队标准化获客"
  ]
},
{
  "id":"workbuddy-promo-copy",
  "ico":"📣",
  "title":"WorkBuddy 推广文案",
  "desc":"一个卖点三版输出：公众号长文（决策者）、小红书种草（职场人）、朋友圈短文案。",
  "category":"内容生产",
  "status":"已落地",
  "hot":False,
  "overview":"WorkBuddy 产品多渠道营销文案定制技能：围绕降本增效与开箱即用两大核心卖点，按渠道人群定制三版输出——公众号长文版面向企业决策者、小红书种草版面向职场人士、朋友圈短文案做极简传播。<br>⚠️ 注意事项：<br>① 多平台文案须过审核虾再发，避免 AI 味/违规；<br>② 含数据/案例须核实，长文改写消耗 token 注意成本；<br>③ 技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "在技能库加载「workbuddy-promo-copy」skill",
    "明确本次推广的核心卖点与目标人群",
    "可叠加「老田写作风格」去 AI 味",
    "准备好配图素材（可配合海报技能）"
  ],
  "steps":[
    "说明推广主题与投放渠道",
    "AI 按渠道输出对应版本文案",
    "对标题与钩子句做打开率打磨",
    "终稿过一遍审核虾再发布"
  ],
  "example":"围绕「WorkBuddy 自动生成月报」写三版推广文案：公众号版给企业老板看，小红书版给行政文员看，朋友圈版 50 字以内。",
  "scenarios":[
    "产品发布与功能更新宣传",
    "代理商朋友圈日常种草",
    "线下沙龙活动引流文案"
  ]
},
{
  "id":"skill-install-audit",
  "ico":"🛡️",
  "title":"技能安装安全审计",
  "desc":"先审计后安装：静态审查外部 skill 是否投毒（curl|bash、凭证外送、未锁版本依赖）。",
  "category":"文件与知识管理",
  "status":"已落地",
  "hot":False,
  "overview":"安装 SkillHub / GitHub / 社区来源技能的标准流程：强制「先安全审计、后安装」硬顺序，静态审查 SKILL.md 及配套脚本是否含 curl|bash、os.system、凭证外送、未锁版本依赖等风险，确认安全后再落地到技能目录，Python 依赖进虚拟环境并锁版本。<br>⚠️ 注意事项：<br>① 所有外部技能安装前强制过此审计，勿跳过；<br>② 审计报告中 P0 风险项须人工确认后方可落地；<br>③ 技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "在技能库加载「skill-install-audit」skill",
    "设定风险分级标准（P0 强警告 / P1 提示确认）",
    "准备虚拟环境用于隔离安装依赖",
    "把它设为所有外部技能安装的前置门禁"
  ],
  "steps":[
    "拿到外部技能的仓库地址或压缩包",
    "静态审查 SKILL.md 与 scripts/ 全部文件",
    "输出审计报告：风险项 + 分级 + 建议",
    "确认安全后按稳健方式落地安装"
  ],
  "example":"从 GitHub 装这个 pdf-tools 技能之前，先做一遍安全审计，重点查有没有外发凭证和危险命令。",
  "scenarios":[
    "安装社区/第三方来源技能前把关",
    "批量迁移技能库时统一体检",
    "团队内技能分发的安全规范"
  ]
},
{
  "id":"file-batch-rename",
  "ico":"🗂️",
  "title":"文件批量重命名",
  "desc":"按「日期_主题_类型.扩展名」规范批量改名，先预览再执行，冲突处理 + 安全备份。",
  "category":"文件与知识管理",
  "status":"已落地",
  "hot":False,
  "overview":"把散乱命名的文件统一为「日期_主题_类型.扩展名」格式：执行前先输出改名预览清单，自动处理重名冲突，改名前做安全备份，小批量执行随时可回退，不碰目标目录以外的文件。<br>⚠️ 注意事项：<br>① 执行前自动备份，异常可从备份恢复，勿跳过关；<br>② 小批量分批执行，避免大范围误操作；<br>③ 技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "在技能库加载「file-batch-rename」skill",
    "指定目标目录与命名规则",
    "确认备份目录位置",
    "先用少量文件试跑验证规则"
  ],
  "steps":[
    "指定要整理的文件夹",
    "AI 输出改名前后对照预览表",
    "确认无误后执行（自动备份原文件）",
    "抽查结果，异常可从备份恢复"
  ],
  "example":"把 E:\\workbuddy\\案例 目录下的文件按「日期_客户名_文档类型」格式批量重命名，先给我预览。",
  "scenarios":[
    "客户交付物归档整理",
    "下载目录周期性清理规范化",
    "项目移交前的文件标准化"
  ]
},
{
  "id":"tc-style-poster",
  "ico":"🎨",
  "title":"腾讯云风格海报提示词",
  "desc":"分析内容 → 出 5 个封面选题 5 选 1 → 输出可直接用的腾讯云品牌风图像提示词。",
  "category":"内容生产",
  "status":"已落地",
  "hot":False,
  "overview":"腾讯云官方品牌视觉（腾云驾雾风格）的图像提示词生成器：先分析文章/内容，生成 5 个封面选题供挑选，选定后输出可直接投喂图像模型的高质量提示词。覆盖公众号封面、活动物料、朋友圈海报、产品图、信息图等场景。<br>⚠️ 注意事项：<br>① 提示词投喂图像模型后仍需人工筛选成图；<br>② 出图消耗 token/算力，批量生产评估成本；<br>③ 技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "在技能库加载「tencent-cloud-style-poster-generator」skill",
    "准备要配图的文章或活动信息",
    "确认出图通道（内置 ImageGen 或第三方）",
    "首次使用先出一张验证风格符合预期"
  ],
  "steps":[
    "提供文章内容或海报主题",
    "AI 分析后给出 5 个封面选题",
    "5 选 1 确定方向",
    "输出完整图像提示词，直接生成海报"
  ],
  "example":"给这篇《WorkBuddy 月报自动化实战》文章配公众号封面，腾讯云风格，先给我 5 个选题。",
    "scenarios":[
    "公众号/博客封面图量产",
    "活动物料与朋友圈海报",
    "产品宣传视觉统一风格"
  ]
},
{
  "id":"wechat-auto-publish",
  "ico":"📝",
  "title":"公众号文章自动写作与发布",
  "desc":"从选题到发布的全自动化公众号工作流：刘润风格写作、AI 封面图、wenyan 排版推送草稿箱。",
  "category":"内容生产",
  "status":"已落地",
  "hot":True,
  "overview":"通过 WorkBuddy 公众号写作技能 + 文颜（wenyan）发布链路，实现从选题到发布的全自动化公众号内容工作流：AI 按刘润风格成文、ImageGen 生成封面图、wenyan 自动排版（lapis 主题 + solarized-light 代码高亮）并推送到公众号草稿箱，登录后台审核后一键发布。<br>⚠️ 注意事项：<br>① 草稿箱≠已发布，需人工审核，且 AI 生成内容务必人工校对事实与数据，规避合规风险；<br>② 长文 3000–5000 字 + 封面图生成均消耗 token/算力，批量生产请评估成本；<br>③ “30 分钟全流程”指配置完成后的日常运行耗时，首次部署含安装与凭据配置更久；<br>④ 技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "在 WorkBuddy「技能中心」搜索并安装公众号写作技能：基础版 wechat-write（文案创作）或专业版 wechat-article-pro（含 AI 配图 + 刘润风格，推荐直接用专业版，二者无需重复安装）",
    "安装 wechat-publisher 技能（Markdown 转公众号草稿箱，内部调用 wenyan 完成排版与上传）",
    "配置公众号凭据：在 .env 中写入 WECHAT_APP_ID=你的AppID, WECHAT_APP_SECRET=你的密钥（文颜官方变量名，供 wenyan 调用）",
    "安装文颜 CLI：npm install -g @wenyan-md/cli",
    "（仅直连公众号 API 时需要）在公众号后台「设置-开发-IP白名单」添加运行机器 IP；若走 Server 模式或技能代理可绕过此步",
    "如需 AI 配图与刘润风格，确保已启用 wechat-article-pro 专业版"
  ],
  "steps":[
    "输入指令：「帮我写一篇关于 XX 主题的公众号文章，刘润风格」（用 wechat-article-pro 或 wechat-write）",
    "AI 自动生成 3000-5000 字文章，含标题、正文、配图建议",
    "输入指令：「用 ImageGen 生成一张封面图，主题是 XX」",
    "输入指令：「推送到公众号草稿箱」",
    "wechat-publisher 自动编排：调用 wenyan 完成排版（lapis 主题 + solarized-light 代码高亮）并上传至草稿箱，无需手动执行命令",
    "登录公众号后台审核草稿内容，确认无误后发布"
  ],
  "example":"帮我写一篇关于「AI Agent 如何改变教培行业」的公众号文章，要求：刘润风格、案例驱动、3000 字左右、有数据支撑。写完后用 ImageGen 生成封面图，然后推送到草稿箱。",
  "scenarios":[
    "每日公众号内容自动化生产，从选题到草稿箱全程无人值守",
    "热点事件快速响应，30 分钟内完成选题-写作-配图-推送全流程（配置完成后）",
    "多账号矩阵运营，一次生成多版本适配不同公众号定位"
  ]
},
{
  "id":"stock-analysis",
  "ico":"📊",
  "title":"股票综合分析",
  "desc":"输入股票名称或代码，自动获取数据并进行基本面、新闻面、资金面三维分析，输出投资建议和买卖点位参考。",
  "category":"金融",
  "status":"已落地",
  "hot":True,
  "overview":"使用 stock-analyzer 技能，输入股票名称或代码，自动从东方财富网获取数据，进行基本面（PE/PB/ROE/营收增速）、新闻面（利好利空事件）、资金面（主力资金流向）三维分析，输出分析报告含投资建议与买卖点位参考。支持 A 股、港股、美股等东方财富覆盖的所有市场。<br><br>⚠️ 注意事项：AI 生成的买入/卖出价位为基于历史数据的预测参考，**不构成任何投资建议**，实际交易决策请结合自身风险承受能力与专业顾问意见；东方财富数据存在延迟（通常 15–30 分钟），盘中实时性有限；「每日定时推送」需额外配置自动化任务（非技能本体功能），技能本身仅提供单次分析能力；技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "在 WorkBuddy 技能中心安装 stock-analyzer 技能",
    "该技能内置东方财富网数据接口，无需额外配置 API 密钥",
    "确保网络能正常访问东方财富网（eastmoney.com）"
  ],
  "steps":[
    "输入指令：「分析一下贵州茅台这只股票」或「分析股票 600519」",
    "技能自动获取股票基本信息、财务数据、近期新闻",
    "AI 进行三维分析：基本面（PE/PB/ROE/营收增速）、新闻面（利好利空事件）、资金面（主力资金流向）",
    "输出分析报告，包含投资建议、建议买入价位参考、建议卖出价位参考",
    "可追加指令：「帮我监控这只股票，每天早上 8 点推送分析」（需单独配置自动化任务）"
  ],
  "example":"帮我分析一下宁德时代（300750），重点关注最近的新能源行业政策和三季报数据，给出短期和长期的投资建议。",
  "scenarios":[
    "个股深度分析，辅助投资决策",
    "每日持仓股票自动巡检，异常波动及时预警（配合自动化任务）",
    "行业板块对比分析，发现投资机会"
  ]
},
{
  "id":"xiaohongshu-poster",
  "ico":"🎨",
  "title":"小红书海报批量生成",
  "desc":"通过 Python Pillow 库 + 预设海报模板，根据文章内容自动生成小红书风格的海报图片。支持多种排版模板、配色方案和字体选择。",
  "category":"设计",
  "status":"已落地",
  "hot":True,
  "overview":"基于 Python Pillow 图像处理库与预设海报模板，输入文章内容后自动提取关键要点与金句，按小红书竖版比例（1080×1440）批量渲染海报：背景图 + 标题文字 + 正文要点卡片 + 品牌水印。支持知识分享/好物推荐/教程类等多套排版模板切换，以及粉色系/莫兰迪色系等多套配色方案。<br><br>⚠️ 注意事项：**中文字体是必需依赖**——Pillow 渲染中文必须指定中文字体文件（如思源黑体、阿里巴巴普惠体），缺失会导致文字显示为方块或直接报错；字体文件需用户自行准备（放入项目 fonts/ 目录），请确认所用字体的商用授权；海报模板图片同样需用户自行准备（放入 templates/ 目录），技能本身不自带模板素材；「10 分钟出 10 张」指配置好模板和字体后的日常运行耗时，首次部署（含模板制作+字体下载）会更久；build_posters.py 为可选增强脚本（非必须），技能核心功能不依赖它；技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "WorkBuddy 已内置 Python 3.13 环境，无需额外安装 Python",
    "安装 Pillow 图像处理库：pip install Pillow",
    "准备字体文件（推荐思源黑体或阿里巴巴普惠体，均为开源可商用字体），放入项目 fonts/ 目录",
    "将海报模板图片（背景底图）放入 templates/ 目录，技能会根据内容类型自动匹配模板",
    "可选：安装 build_posters.py 增强脚本（提供更多自定义排版选项，非必须）"
  ],
  "steps":[
    "输入指令：「根据这篇文章内容帮我做 10 张小红书海报」",
    "AI 分析文章内容，提取关键要点和金句",
    "自动选择适合的海报模板（知识分享 / 好物推荐 / 教程类等）",
    "Pillow 自动渲染合成：背景图 + 标题文字 + 正文要点卡片 + 品牌水印",
    "批量生成海报图片，输出到 posters/ 目录",
    "可追加指令：「换一套配色方案，用莫兰迪色系重新生成」"
  ],
  "example":"帮我根据这篇公众号文章做 10 张小红书海报，要求：尺寸 1080×1440，配色用粉色系，每张海报一个核心要点，底部加品牌水印。",
  "scenarios":[
    "公众号文章转小红书图文，一鱼多吃，一次生产多平台分发",
    "知识卡片批量制作，适合教育类内容传播与课程配套物料",
    "活动宣传海报快速生成，配置好后 10 分钟出 10 张"
  ]
},
{
  "id":"qcc-company-query",
  "ico":"🏢",
  "title":"企业工商信息查询",
  "desc":"通过企查查 Connector 对接，查询中国境内企业的工商登记数据、股东与实控人穿透、董监高人员、财务尽调等信息。",
  "category":"法务合规",
  "status":"已落地",
  "hot":False,
  "overview":"使用企查查（qcc-company）MCP 连接器，输入企业名称或统一社会信用代码，自动调用企查查 API 获取中国境内企业工商数据：基本信息（注册资本/法人/成立日期）、股东结构及实控人穿透、对外投资列表、历史变更记录、董监高信息等。支持单次查询与批量多企业一次查完，可导出为 Excel 格式尽调报告。<br><br>⚠️ 注意事项：**该能力基于企查查 MCP 连接器实现**，需先在 WorkBuddy 连接器管理中启用「企查查 (qcc-company)」并完成 Token 认证；Token 需从企查查开放平台申请（需注册企查查开发者账号）；工商数据涉及企业敏感信息（股东穿透、对外投资等），使用时请遵守《个人信息保护法》及相关合规要求，仅用于合法商业场景（商务合作背调/投资尽调/竞品分析），不得用于非法用途或数据倒卖；API 查询有频率限制和计费规则，批量查询前请确认配额；技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "在 WorkBuddy 连接器管理中找到「企查查 (qcc-company)」连接器",
    "点击「信任」启用企查查 MCP 连接器",
    "如需要 Token 认证，前往企查查开放平台申请 API Token（需注册开发者账号）",
    "在 WorkBuddy 的 MCP 配置文件中设置 Token（或在连接器授权页面填入）",
    "安装 qcc-company 技能（技能中心搜索「企业查询」或「企查查」）"
  ],
  "steps":[
    "输入指令：「查询腾讯科技（深圳）有限公司的工商信息」",
    "技能调用企查查 API，返回企业基本信息（注册资本、法人、成立日期等）",
    "可追问：「这个公司的股权结构是什么？穿透到实控人」",
    "可追问：「这家公司有哪些对外投资？高管团队是谁？」",
    "可追问：「导出为 Excel 格式的尽调报告」",
    "支持批量查询：输入多个企业名称一次查完"
  ],
  "example":"帮我查询「字节跳动有限公司」的完整工商信息，包括股权穿透图、对外投资列表、历史变更记录，整理成一份尽调报告。",
  "scenarios":[
    "商务合作前的企业背景调查，快速了解对方资质与信用状况",
    "投资尽职调查，穿透股权结构找到实际控制人与关联方",
    "竞品分析，监控竞争对手的对外投资布局和业务版图变化"
  ]
},
{
  "id":"github-pages-deploy",
  "ico":"🚀",
  "title":"网站一键部署 GitHub Pages",
  "desc":"使用 web-deploy-github 技能，自动创建 GitHub 仓库、上传静态网站文件、启用 GitHub Pages，一步完成部署。也可使用 CloudStudio 部署到腾讯云沙箱。",
  "category":"开发",
  "status":"已落地",
  "hot":False,
  "overview":"通过 web-deploy-github 技能实现静态网站一键上线：AI 自动生成 HTML/CSS/JS 网站代码 → 创建 GitHub 仓库并上传构建产物（dist/ 或 build/ 目录下的 index.html）→ 启用 GitHub Pages 服务 → 返回线上访问 URL。支持自定义域名绑定（GitHub Pages 设置中添加 CNAME 记录）。备选方案：使用 CloudStudio 部署到腾讯云沙箱环境，适合国内访问速度要求更高的场景。<br><br>⚠️ 注意事项：**仅适用于静态网站**（纯 HTML/CSS/JS，无服务端渲染）；GitHub Pages 免费版有 1GB 仓库大小限制和每月 100GB 带宽软限制；自定义域名需自行配置 DNS 解析（CNAME 指向 <用户名>.github.io）；CloudStudio 部署为腾讯云沙箱环境，有免费额度但非永久；部署前请确认 index.html 在 dist/ 或 build/ 目录根路径；技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "安装 web-deploy-github 技能（技能中心搜索「网站部署」）",
    "确保 GitHub 连接器已启用（连接器管理中启用 GitHub）",
    "如果使用 CloudStudio 部署，无需额外配置（自动使用腾讯云沙箱）",
    "准备好网站构建产物：确保 dist/ 或 build/ 目录下有 index.html",
    "可选：配置自定义域名（GitHub Pages 设置中添加 CNAME 记录）"
  ],
  "steps":[
    "输入指令：「帮我做一个个人作品集网站并部署上线」",
    "AI 生成 HTML/CSS/JS 网站代码",
    "输入指令：「部署到 GitHub Pages」",
    "技能自动执行：创建仓库 → 上传文件 → 启用 Pages → 等待构建完成",
    "返回线上访问 URL（https://<用户名>.github.io/<仓库名>）",
    "也可用 CloudStudio 部署：输入「部署到 CloudStudio」获得沙箱 URL"
  ],
  "example":"帮我创建一个简洁的个人简历网页，包含头像、教育背景、工作经历、项目展示，部署到 GitHub Pages。配色用蓝白主题，响应式设计。",
  "scenarios":[
    "个人作品集/简历网站快速上线",
    "活动落地页、产品介绍页部署",
    "开源项目文档站搭建"
  ]
},
{
  "id":"scheduled-automation",
  "ico":"⏰",
  "title":"定时自动化任务",
  "desc":"使用 WorkBuddy 内置 automation_update 工具，创建定时自动化任务。支持每日、每周、每月循环执行，也可设置一次性定时提醒。任务存储在本地 SQLite 数据库中。",
  "category":"自动化",
  "status":"已落地",
  "hot":True,
  "overview":"基于 WorkBuddy 内置的 automation_update 工具（无需额外安装），创建和管理定时自动化任务。支持 RFC 5545 RRULE 标准定时规则（每日 FREQ=DAILY、每周 FREQ=WEEKLY、每月 FREQ=MONTHLY），可设置任务有效期（validFrom / validUntil）、关联特定工作目录和专家 ID。任务状态管理：ACTIVE（激活）/ PAUSED（暂停）/ 删除（软删除可恢复）。数据存储在本地 SQLite 数据库（~/.workbuddy/workbuddy.db），断网离线也能正常调度。<br><br>⚠️ 注意事项：**automation_update 是 WorkBuddy 内置工具**，无需安装任何技能或连接器；RRULE 规则遵循 RFC 5545 标准，时区默认使用系统本地时间；任务执行依赖 WorkBuddy 进程在线——若客户端完全关闭则无法触发（建议保持后台运行或使用服务器版）；「每日早上8点」等自然语言时间会被 AI 自动转换为 RRULE 参数；暂停的任务不会执行但保留配置，删除为软删除可恢复；技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "无需额外安装，WorkBuddy 内置 automation_update 工具",
    "支持 RFC 5545 RRULE 标准的定时规则语法",
    "可设置任务有效期（validFrom / validUntil）",
    "可关联特定的工作目录和专家 ID",
    "任务状态管理：ACTIVE（激活）/ PAUSED（暂停）/ 软删除恢复"
  ],
  "steps":[
    "输入指令：「每天早上8点帮我查看WorkBuddy的最新活动并整理成简报」",
    "AI 创建自动化任务，scheduleType=recurring，rrule=FREQ=DAILY;HOUR=8",
    "每天8点自动执行：抓取活动信息 → 整理简报 → 输出到对话",
    "管理任务：「查看我所有的自动化任务」→ 列出所有任务",
    "暂停任务：「暂停XX任务」→ status=PAUSED",
    "删除任务：「删除XX任务」→ 软删除，可恢复"
  ],
  "example":"帮我设置一个自动化任务：每周一早上9点，分析上周的A股市场表现，整理成周报格式，包含板块涨跌幅、北向资金流向、重点个股分析。",
  "scenarios":[
    "每日数据监控（股价、新闻、竞品动态）自动推送",
    "周报/月报自动生成，减少重复劳动",
    "定时提醒（会议、截止日期、待办事项）"
  ]
},
{
  "id":"image-gen",
  "ico":"🖼️",
  "title":"多模态图片生成",
  "desc":"使用 ImageGen 工具，通过文字描述生成高质量图片，或对已有图片进行风格变换。支持写实、插画、水彩、3D等多种风格。每张图片消耗约 5-10 积分。",
  "category":"内容生产",
  "status":"已落地",
  "hot":True,
  "overview":"调用 ImageGen 内置工具实现 AI 图片生成，支持两种模式：**文生图**（text-to-image）：输入文字描述，AI 理解语义后生成对应图片；**图生图**（image-to-image）：上传一张参考图片 + 文字指令，对图片进行风格变换、局部修改等操作。支持写实摄影、插画、水彩、油画、3D 渲染、像素风等多种艺术风格。生成结果保存为本地文件，可在对话中直接预览。每次调用消耗约 5–10 积分（具体以实际扣费为准）。<br><br>⚠️ 注意事项：**ImageGen 是 WorkBuddy 内置工具**，无需安装任何技能或连接器；积分消耗按次计费，批量生成前请确认余额充足；首次使用会提示积分消耗确认；生成结果保存在本地临时目录，重要图片请及时另存到指定位置；文字描述越详细（主体/风格/构图/光影/色调），生成效果越好；图生图模式需要先上传参考图片再给变换指令；不支持生成涉及违法违规、暴力、色情等内容；技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "无需安装，ImageGen 是 WorkBuddy 内置工具",
    "在对话中直接调用，首次使用会提示积分消耗",
    "支持 text-to-image（文生图）和 image-to-image（图生图）两种模式",
    "生成结果保存在本地文件，可直接在对话中预览",
    "注意：每次调用消耗 5-10 积分"
  ],
  "steps":[
    "文生图模式：输入「帮我生成一张封面图，主题是AI赋能教育，风格科技感」",
    "AI 理解描述，调用模型生成图片",
    "图片保存为本地文件，在对话中展示预览",
    "图生图模式：上传一张图片 + 「把这张图变成水彩画风格」",
    "可追加指令：「重新生成，分辨率改为 1920x1080」",
    "可追问：「再生成3张不同风格的变体」"
  ],
  "example":"帮我生成一张公众号封面图，要求：16:9比例，主题是「AI Agent 重塑企业效率」，风格是科技蓝色调+未来感，不要出现文字。",
  "scenarios":[
    "公众号/小红书封面图自动生成",
    "产品宣传图、活动海报素材",
    "PPT配图、博客文章插图"
  ]
},
{
  "id":"model-3d-gen",
  "ico":"🧊",
  "title":"3D 模型生成",
  "desc":"使用 3D模型与视频特效技能（buddy-multimodal-generation），支持文生3D模型和图生3D模型。生成的模型可用于游戏开发、产品展示、原型设计等场景。",
  "category":"内容生产",
  "status":"已落地",
  "hot":False,
  "overview":"基于 buddy-multimodal-generation 内置技能（builtin-skills/buddy-multimodal-generation），实现 AI 3D 模型生成。支持两种输入方式：**文生3D**——输入文字描述物体的外观、材质、风格，AI 生成对应 3D 模型；**图生3D**——上传一张产品照片，AI 将其转化为 3D 模型。输出格式为标准 3D 模型文件（GLB/GLTF），可在 3D 查看器中预览，也兼容 Blender、Unity、Three.js 等主流 3D 工具导入使用。<br><br>⚠️ 注意事项：该技能为 **WorkBuddy 内置技能**（buddy-multimodal-generation），无需额外安装，直接在对话中触发即可；生成过程通常需要等待 1–3 分钟完成；3D 模型复杂度越高（细节多/纹理复杂），生成时间和文件体积越大；生成的模型适合用于展示原型和概念验证，工业级精度可能需要后期在 Blender 等工具中精修；图生3D模式的效果取决于参考照片的角度和清晰度，建议使用正面平光照片；技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "该技能为 WorkBuddy 内置技能（builtin-skills/buddy-multimodal-generation）",
    "无需额外安装，直接在对话中触发",
    "支持输入文本描述或上传参考图片",
    "输出格式为标准 3D 模型文件（GLB/GLTF）",
    "生成结果保存在本地，可在 3D 查看器中预览"
  ],
  "steps":[
    "文生3D：输入「帮我生成一个3D模型：一只可爱的卡通猫咪，圆润造型」",
    "AI 解析描述，调用 3D 生成模型",
    "等待 1-3 分钟生成完成，模型保存为 .glb 文件",
    "图生3D：上传一张产品照片 + 「根据这张图生成3D模型」",
    "模型可在 Blender、Unity、Three.js 等工具中使用",
    "可追问：「调整模型比例，让猫咪更胖一些」"
  ],
  "example":"帮我生成一个3D模型：一个简约风格的咖啡杯，白色陶瓷质感，带把手，适合放在电商产品展示页面中使用。",
  "scenarios":[
    "电商产品3D展示，提升购物体验",
    "游戏开发快速原型，降低建模成本",
    "建筑设计可视化，方案展示"
  ]
},
{
  "id":"video-fx-gen",
  "ico":"🎬",
  "title":"视频特效制作",
  "desc":"使用 buddy-multimodal-generation 技能的视频特效功能，基于预设模板对图片应用动效。支持拥抱、变身、万物归尘等热门特效模板。",
  "category":"内容生产",
  "status":"已落地",
  "hot":True,
  "overview":"基于 buddy-multimodal-generation 内置技能的视频特效功能，将静态图片转化为动态短视频。工作流程：上传一张人物/场景照片 → 选择特效模板（拥抱动效/变身效果/万物归尘/其他热门模板）→ AI 识别图片内容并匹配特效参数 → 等待 1–3 分钟生成视频特效 → 输出 MP4 格式视频文件。生成的视频可在对话中预览，不满意可重新生成。<br><br>⚠️ 注意事项：该能力基于 **WorkBuddy 内置技能** buddy-multimodal-generation 实现，无需额外安装；**必须提供一张输入图片作为特效素材**，不能纯文字生成视频；特效模板为预设选项（拥抱/变身/万物归尘等），不支持自定义模板；生成视频时长通常为 5 秒左右短视频片段，非长视频制作；每次生成消耗较多算力资源，建议确认效果满意后再批量处理；输出格式固定为 MP4；老照片动效制作时，照片清晰度越高效果越好；技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "该技能为 WorkBuddy 内置技能",
    "在对话中说「对图片应用特效」即可触发",
    "需要提供一张输入图片作为特效素材",
    "选择特效模板（拥抱/变身/万物归尘等）",
    "生成的视频保存为 MP4 格式"
  ],
  "steps":[
    "上传一张人物照片",
    "输入指令：「对这张图应用拥抱特效模板」",
    "AI 识别图片内容，匹配特效模板",
    "等待 1-3 分钟生成视频特效",
    "视频保存为本地 MP4 文件",
    "可在对话中预览效果，不满意可重新生成"
  ],
  "example":"我上传了一张我奶奶的旧照片，帮我用「拥抱」特效模板生成一个视频，让照片里的人物动起来，像是在拥抱的效果。",
  "scenarios":[
    "老照片动效制作，让回忆鲜活起来",
    "社交媒体创意内容制作",
    "节日祝福视频快速生成"
  ]
},
{
  "id":"prd-writing",
  "ico":"📋",
  "title":"产品需求文档 PRD 编写",
  "desc":"使用 pmaster 技能，覆盖需求分析、PRD编写、BRD/MRD、用户故事、KANO模型、5W1H、优先级排序、SWOT分析、波特五力、PESTLE等全套产品工作方法论。",
  "category":"产品营销",
  "status":"已落地",
  "hot":False,
  "overview":"基于 pmaster 技能的全套产品工作流：从需求背景到 PRD 文档交付的一站式 AI 辅助。内置完整的产品方法论框架——需求分析（5W1H）、用户故事与画像、功能列表与优先级排序（KANO/MoSCoW）、业务流程图与原型描述、BRD（商业需求文档）/MRD（市场需求文档）、竞品分析（SWOT/波特五力/PESTLE）、数据指标定义。支持导出为 Markdown 或 Word 格式，并可配合腾讯文档技能实现多人协作编辑。<br><br>⚠️ 注意事项：**PRD 是产品经理的核心交付物**，AI 生成的框架和初稿需结合实际业务场景人工审核修正——特别是功能优先级、数据指标目标值、技术可行性评估等关键决策点；KANO 模型分类（基本型/期望型/兴奋型/无差异型/反向型）需基于真实用户调研数据，AI 只能做初步推断；MoSCoW 排序（Must/Should/Could/Won't）应与研发团队对齐确认；导出为腾讯文档可实现多人协作，但需注意权限设置；技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "在 WorkBuddy 技能中心安装 pmaster 技能",
    "该技能内置完整的产品方法论框架，无需额外配置",
    "支持输出标准 PRD 文档格式",
    "可导出为 Markdown / Word 格式",
    "建议配合腾讯文档技能使用，实现多人协作"
  ],
  "steps":[
    "输入指令：「帮我写一份 XX产品的PRD文档」",
    "AI 引导你补充需求背景：目标用户、核心场景、业务目标",
    "自动生成 PRD 框架：需求概述、用户故事、功能列表、流程图、原型描述",
    "可追问：「用 KANO 模型分析这些需求的优先级」",
    "可追问：「把功能列表按 MoSCoW 方法排序」",
    "可追问：「导出为腾讯文档，分享给团队」"
  ],
  "example":"帮我写一份「AI智能客服系统」的PRD文档，目标用户是电商商家，核心场景是自动回复买家咨询。需要包含：需求背景、用户故事、功能列表、数据流程、优先级排序。",
  "scenarios":[
    "新产品立项，快速产出 PRD 初稿",
    "需求评审前准备，结构化呈现需求",
    "团队协作，PRD 文档多人在线编辑"
  ]
},
{
  "id":"official-doc-writing",
  "ico":"📄",
  "title":"官方公文写作",
  "desc":"使用 official-document-skill 技能，支持中国党政机关公文、事务文书、申论应用文的起草、修改、润色和质量检查。采用人民日报风格政务表达。",
  "category":"写作排版",
  "status":"已落地",
  "hot":False,
  "overview":"基于 official-document-skill 技能的专业公文写作能力，覆盖中国党政机关公文体系（GB/T 9704-2012 标准）：15 种法定公文种类（决定/决议/通知/通报/报告/请示/批复/函/意见/公报/公告/议案/命令/纪要等），以及事务文书（总结/计划/方案/讲话稿等）和申论应用文。内置公文质量检查规则，自动校验格式规范（标题层级/主送机关/正文结构/落款/日期）、用语规范性（政务表达/逻辑/避错）。输出风格对标人民日报评论风，语言正式庄重、结构严谨。<br><br>⚠️ 注意事项：**公文具有法定效力和严肃性**，AI 生成的草稿仅作为起草辅助，正式发文前必须经相关负责人审核把关；GB/T 9704-2012 是推荐性国家标准，不同单位可能有内部行文规范补充（如字体/字号/页边距的具体要求），请以本单位规定为准；涉密公文严禁使用 AI 工具处理；「润色正文」「调整语气」「改请示文种」等追问指令可迭代优化；批量修改（如「把所有『关于』改为『有关』」）支持全文替换；技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "在 WorkBuddy 技能中心安装 official-document-skill 技能",
    "该技能内置党政机关公文格式规范（GB/T 9704-2012）",
    "支持 15 种法定公文种类的起草",
    "支持事务文书：总结、计划、方案、讲话稿等",
    "内置公文质量检查规则，自动检查格式、用语、逻辑"
  ],
  "steps":[
    "输入指令：「帮我起草一份关于 XX工作的通知」",
    "AI 按公文格式生成：标题、主送机关、正文、落款、日期",
    "可追问：「润色正文，语言更正式一些」",
    "可追问：「检查公文格式是否合规」",
    "可追问：「改为请示文种，语气调整为请示上级」",
    "支持批量修改：「把所有『关于』改为『有关』」"
  ],
  "example":"帮我起草一份《关于推进2026年数字化转型工作的通知》，主送各区县人民政府，内容包含工作目标、重点任务、保障措施三个部分，字数2000字左右，人民日报评论风格。",
  "scenarios":[
    "政府机关日常公文起草，提高写作效率",
    "国企事业单位工作报告、方案撰写",
    "申论考试练习，规范政务表达"
  ]
},
{
  "id":"legal-search-pkulaw",
  "ico":"⚖️",
  "title":"法律智能检索",
  "desc":"使用 pkulaw（北大法宝）技能，对接北大法宝法律智能检索系统，支持法律法规、司法案例、合同模板、法律期刊的全文检索和智能分析。",
  "category":"法务合规",
  "status":"已落地",
  "hot":False,
  "overview":"基于北大法宝（pkulaw）MCP 连接器 + pkulaw 技能的双件套方案，实现法律法规全库智能检索与分析。覆盖四大数据库：**法规库**（法律/行政法规/部门规章/地方性法规/司法解释）、**案例库**（指导案例/典型案例/裁判文书）、**合同库**（各类合同模板与条款参考）、**期刊库**（法学核心期刊论文）。支持自然语言查询（如「搜索关于数据安全保护的法律法规」），AI 自动分析检索结果、提炼关键条款和裁判要旨，并可对比多个案例的判决差异、生成法律意见书草稿。<br><br>⚠️ 注意事项：**该能力基于北大法宝 MCP 连接器实现**，需先在 WorkBuddy 连接器管理中启用「北大法宝 (pkulaw)」连接器；需要北大法宝有效账号（机构版或个人版），在连接器配置中填入认证信息；检索结果仅供参考和学习研究使用，不构成正式法律意见，重大法律决策请咨询执业律师；合同模板仅为参考范本，具体条款需根据实际情况修改并由法务审核；技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "在 WorkBuddy 连接器管理中启用「北大法宝 (pkulaw)」连接器",
    "需要北大法宝有效账号（机构版或个人版）",
    "在连接器配置中填入认证信息",
    "安装 pkulaw 技能（技能中心搜索「法律检索」）",
    "支持法规、案例、合同、期刊四大数据库检索"
  ],
  "steps":[
    "法规检索：「搜索关于数据安全保护的法律法规」",
    "案例检索：「查找近三年劳动合同纠纷的典型案例」",
    "合同模板：「下载股权转让合同的模板」",
    "AI 自动分析检索结果，提炼关键条款和裁判要旨",
    "可追问：「对比这些案例的判决差异」",
    "可追问：「生成一份法律意见书草稿」"
  ],
  "example":"帮我检索关于「个人信息保护」的最新法律法规，重点关注企业合规义务和数据跨境传输的规定，整理成一份合规要点清单。",
  "scenarios":[
    "企业法务合规检查，快速检索适用法规",
    "律师办案准备，类案检索和裁判规则分析",
    "合同审查，快速找到合同模板和条款参考"
  ]
},
{
  "id":"patent-search-patsnap",
  "ico":"🔬",
  "title":"专利文献检索",
  "desc":"使用 patsnap-search（智慧芽）技能，对接智慧芽专利与文献融合检索平台，支持全球专利数据检索、技术趋势分析、竞争对手专利监控。",
  "category":"法务合规",
  "status":"已落地",
  "hot":False,
  "overview":"基于智慧芽（patsnap-search）MCP 连接器 + patsnap-search 技能的双件套方案，实现全球专利数据的智能检索与分析。覆盖中国、美国、欧洲、日本等全球主要专利数据库，支持按申请人/发明人/技术领域/申请日期等多维度筛选。核心能力：**专利检索**（按关键词/分类号/申请人检索专利列表，含标题/申请人/摘要/法律状态）、**技术趋势分析**（某领域的专利布局热点、技术路线演进）、**竞争监控**（跟踪竞争对手最新专利申请动态）、**分析报告导出**（含技术分布图/专利地图，支持 Excel 格式）。<br><br>⚠️ 注意事项：**该能力基于智慧芽 MCP 连接器实现**，需先在 WorkBuddy 连接器管理中启用「智慧芽 (patsnap-search)」连接器；需要智慧芽平台有效账号，在连接器配置中填入 API 认证信息；专利数据有更新延迟（通常 1–2 周），最新申请可能尚未入库；专利分析结论供研发决策参考，不构成侵权判定依据（FTO 分析需专业专利律师出具意见）；导出的 Excel 报告可用于内部汇报，对外披露请注意保密；技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "在 WorkBuddy 连接器管理中启用「智慧芽 (patsnap-search)」连接器",
    "需要智慧芽平台有效账号",
    "在连接器配置中填入 API 认证信息",
    "安装 patsnap-search 技能",
    "支持中国、美国、欧洲、日本等全球专利数据库"
  ],
  "steps":[
    "输入指令：「检索 AI 大模型相关的专利，按申请时间排序」",
    "AI 调用智慧芽 API，返回专利列表（标题、申请人、摘要、法律状态）",
    "可追问：「分析这些专利的技术趋势，哪些方向最热」",
    "可追问：「监控竞争对手 XX 公司的最新专利申请」",
    "可追问：「生成一份专利分析报告，包含技术分布图」",
    "支持导出为 Excel 格式"
  ],
  "example":"帮我检索「固态电池」领域的核心专利，重点关注丰田、宁德时代、三星SDI三家公司的专利布局，分析技术路线差异，生成竞品专利分析报告。",
  "scenarios":[
    "研发立项前的专利检索，避免侵权风险",
    "竞争对手专利监控，掌握技术动态",
    "专利布局规划，发现技术空白点"
  ]
},
{
  "id":"tencent-meeting-mgmt",
  "ico":"📅",
  "title":"腾讯会议管理",
  "desc":"使用 tencent-meeting-skill 和 tmeet-skill 技能，对接腾讯会议 OpenAPI，实现会议预约、管理、录制、AI纪要、转写等全流程自动化。",
  "category":"企业微信",
  "status":"已落地",
  "hot":False,
  "overview":"基于腾讯会议（tmeet）MCP 连接器 + 双技能（tencent-meeting-skill 图形界面操作 + tmeet-skill CLI 命令行操作）的全流程会议管理方案。通过 OAuth 授权登录腾讯会议企业版/开发者账号后，可实现：**会议创建与预约**（设定主题/时间/参会人/自动录制）、**会议查询与管理**（查看列表/取消/添加参会人）、**录制管理**（下载录制视频/AI 智能纪要/转写文本）、**会议转写全文检索**（搜索会议记录中的讨论要点）。双技能互补：tencent-meeting-skill 适合常规 GUI 操作，tmeet-skill CLI 支持脚本化批量操作。<br><br>⚠️ 注意事项：**需要腾讯会议企业版账号或开发者账号**，个人免费版部分 API 权限受限；首次使用需完成 OAuth 授权登录（在浏览器中授权）；tmeet-skill 为 CLI 命令行工具，适合高级用户和脚本化场景，普通用户用 tencent-meeting-skill 即可；AI 纪要功能依赖腾讯会议云端转录能力，需在会议开启时勾选「云录制」；会议转写内容可能含敏感商业信息，分享前请注意脱敏；技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "在 WorkBuddy 连接器管理中启用「腾讯会议 (tmeet)」连接器",
    "需要腾讯会议企业版账号或开发者账号",
    "完成 OAuth 授权登录（首次使用需要在浏览器中授权）",
    "安装 tencent-meeting-skill 技能",
    "可选：安装 tmeet-skill CLI 工具（命令行操作，适合脚本化场景）"
  ],
  "steps":[
    "创建会议：「帮我预约一个明天下午2点的会议，主题是XX，邀请A和B」",
    "查询会议：「查看我本周的会议列表」",
    "会议管理：「把C也加入明天的会议」「取消明天的会议」",
    "录制管理：「下载上周产品评审会的录制视频」",
    "AI 纪要：「生成昨天会议的 AI 智能纪要」",
    "转写全文：「搜索会议转写中提到『预算』的部分」"
  ],
  "example":"帮我预约一个明天上午10点的腾讯会议，主题是「Q3产品规划评审」，邀请产品部全体成员，设置自动录制，会议结束后生成AI智能纪要并发给我。",
  "scenarios":[
    "会议自动化管理，减少行政开销",
    "会后 AI 纪要自动生成，关键决策不遗漏",
    "会议转写内容搜索，快速定位讨论要点"
  ]
},
{
  "id":"knowledge-base-qa",
  "ico":"📚",
  "title":"知识库智能问答",
  "desc":"使用 IMA 技能（ima-skill），支持知识库管理和笔记管理。上传文件到知识库，基于知识库内容进行智能问答、语义检索，让 AI 成为你的私有知识助手。",
  "category":"文件与知识管理",
  "status":"已落地",
  "hot":True,
  "overview":"基于 IMA 知识库（ima-mcp）连接器 + ima-skill 技能的知识管理与智能问答方案。核心流程：**创建知识库**（命名+分类）→ **上传文件**（支持 PDF/Word/图片/网页等多格式）→ **智能问答**（基于知识库内容的 RAG 检索增强生成，回答精准且有据可查）→ **语义检索**（在知识库中模糊搜索相关内容）→ **笔记管理**（创建笔记/记录要点/浏览库内文件）。支持创建多个知识库（如「产品文档」「客户资料」「学习笔记」），每个知识库独立索引互不干扰。<br><br>⚠️ 注意事项：**该能力基于 IMA 知识库 MCP 连接器实现**，需先在 WorkBuddy 连接器管理中启用「IMA知识库 (ima-mcp)」连接器；需要完成 IMA 平台 OAuth 授权登录；问答质量取决于知识库内容的质量和完整性——垃圾进垃圾出，上传前请确保文件内容准确且结构清晰；知识库有容量上限，大量文件建议按主题拆分为多个知识库；语义检索基于向量相似度，精确匹配（如具体数字/型号名）可能不如关键词检索准；客服场景使用时，注意定期更新知识库内容以保证回答时效性；技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "在 WorkBuddy 连接器管理中启用「IMA知识库 (ima-mcp)」连接器",
    "完成 IMA 平台 OAuth 授权登录",
    "安装 ima-skill 技能（技能中心搜索「知识库」）",
    "支持上传 PDF、Word、图片、网页等多格式文件",
    "知识库支持分类管理，可创建多个知识库"
  ],
  "steps":[
    "创建知识库：「帮我创建一个名为『产品文档』的知识库」",
    "上传文件：「把这个PDF上传到知识库」或「把这个网页添加到知识库」",
    "智能问答：「根据知识库内容回答：我们的产品有哪些核心功能？」",
    "语义检索：「在知识库中搜索关于『用户增长』的内容」",
    "笔记管理：「创建一条笔记，记录今天的会议要点」",
    "知识库浏览：「列出知识库中的所有文件」"
  ],
  "example":"帮我把公司所有的产品文档（共50个PDF）上传到知识库，然后回答：我们有哪些产品线？每条产品线的目标用户是谁？核心功能有什么差异？",
  "scenarios":[
    "企业内部知识管理，员工快速查找资料",
    "个人学习笔记整理，构建第二大脑",
    "客服知识库，基于产品文档自动回答用户问题"
  ]
},
{
  "id":"humanizer",
  "ico":"✨",
  "title":"消除 AI 写作痕迹",
  "desc":"使用 humanizer 技能，检测并修复文本中的 AI 写作痕迹。识别 AI 高频词汇、过度结构化表达、机械化连接词、公式化结尾等问题，让文字读起来更像人类写作。",
  "category":"写作排版",
  "status":"已落地",
  "hot":True,
  "overview":"基于 humanizer 技能的 AI 文本去痕能力：粘贴需要优化的文本（或引用之前 AI 生成的内容），AI 自动检测并修复以下典型 AI 痕迹——**高频词汇**（“综上所述““值得注意的是““总而言之“等）、**过度结构化表达**（每段都“首先...其次...最后...“）、**虚假客观性**（滥用“客观地说““不可否认“）、**机械化连接词**、**完美主义陷阱**（没有口语化波动）、**公式化结尾**（总结段千篇一律）。支持中文和英文文本，可对任意长度文本进行检测和修复，也支持批量处理（一次粘贴多段文本）。<br><br>⚠️ 注意事项：humanizer 是纯文本处理技能，无需额外连接器配置；优化后的文本仍需人工审读确认——去 AI 味不等于内容准确，事实/数据/逻辑错误不会因润色而自动修正；「只修复AI高频词汇」的精准模式适合保留原文结构的微调场景；学术类论文使用时请注意保持学术规范用语不被过度口语化；技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "在 WorkBuddy 技能中心安装 humanizer 技能",
    "该技能为纯文本处理，无需额外连接器配置",
    "支持中文和英文文本",
    "可对任意长度文本进行检测和修复",
    "支持批量处理：一次粘贴多段文本"
  ],
  "steps":[
    "粘贴需要优化的文本（或引用之前AI生成的内容）",
    "输入指令：「帮我去掉这段文字的AI味」",
    "AI 检测以下问题：AI 高频词汇、过度结构化、虚假客观性、机械化连接词、完美主义陷阱、公式化结尾、过度修饰",
    "逐项修复，输出优化后的文本",
    "可追问：「再自然一些，增加一些口语化表达」",
    "可追问：「只修复AI高频词汇，保持其他不变」"
  ],
  "example":"帮我检查并优化这段文章的AI痕迹：「综上所述，我们可以清晰地看到，AI技术正在深刻地改变着我们的生活方式。首先，它提高了生产效率；其次，它降低了成本；最后，它创造了新的价值。」",
  "scenarios":[
    "公众号/知乎文章发布前去 AI 味",
    "学术论文润色，避免 AI 检测工具识别",
    "商业文案优化，让内容更有温度和个性"
  ]
},
{
  "id":"financial-data-search",
  "ico":"💰",
  "title":"财务数据智能检索",
  "desc":"使用 neodata-financial-search 和 westock-data 技能，支持自然语言查询股票、基金、ETF、指数、宏观经济数据。覆盖 A 股、港股、美股、期货、外汇、可转债等市场。",
  "category":"金融",
  "status":"已落地",
  "hot":True,
  "overview":"双引擎金融数据检索方案：**neodata-financial-search**（WorkBuddy 内置 builtin-skill）提供自然语言金融数据查询接口；**westock-data**（腾讯自选股 MCP 连接器 + westock-data/westock-tool 技能）提供结构化行情/财报/研报/新闻/公告/股东/分红/宏观数据查询与选股筛选能力。覆盖市场：A 股/港股/美股/期货/外汇/可转债/基金/ETF/指数。核心查询类型：**行情查询**（股价/涨跌幅）、**财报查询**（资产负债表/利润表/现金流关键指标）、**研报查询**（券商研报推荐与评级）、**选股筛选**（按条件批量筛选，如 PE<20 且 ROE>15%）、**宏观数据**（CPI/PPI/GDP 等）。<br><br>⚠️ 注意事项：neodata-financial-search 为 **WorkBuddy 内置技能**，westock-data 需安装腾讯自选股 MCP 连接器；金融数据存在延迟（通常 15–30 分钟），盘中实时性有限；历史财务数据以公司披露为准，AI 分析结论仅供参考，投资决策请结合专业顾问意见；选股筛选结果基于历史数据回测，不代表未来表现；无需额外 API 密钥，开箱即用；技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "WorkBuddy 内置 neodata-financial-search 技能（builtin-skill），无需安装",
    "安装 westock-data 技能（腾讯自选股数据查询）",
    "可选：启用 westock-mcp 连接器获取实时行情",
    "可选：安装 westock-tool 技能进行条件选股",
    "无需额外 API 密钥，开箱即用"
  ],
  "steps":[
    "行情查询：「查询贵州茅台最新股价和涨跌幅」",
    "财报查询：「宁德时代2025年三季报的主要财务指标」",
    "研报查询：「最近有哪些券商研报推荐了AI板块」",
    "选股筛选：「帮我筛选PE小于20、ROE大于15%的A股股票」",
    "宏观数据：「查询中国最新的CPI和PPI数据」",
    "可追问：「把这些数据整理成表格」"
  ],
  "example":"帮我查询比亚迪（002594）的最新行情、2025年年报关键财务数据、最近30天的券商研报评级，以及新能源汽车板块的整体走势，整理成一份投资分析简报。",
  "scenarios":[
    "投资研究，快速获取多维度金融数据",
    "量化选股，按条件批量筛选标的",
    "行业研究，宏观数据+板块数据联动分析"
  ]
},
{
  "id":"weiyun-file-mgmt",
  "ico":"☁️",
  "title":"微云网盘文件管理",
  "desc":"使用 weiyun 技能，对接腾讯微云网盘 MCP 接口，实现文件列表、按分类浏览、上传下载、删除、分享链接生成、重命名等完整文件管理功能。",
  "category":"文件与知识管理",
  "status":"已落地",
  "hot":False,
  "overview":"基于腾讯微云（tencent-weiyun）MCP 连接器 + weiyun 技能的云端文件管理方案。通过 OAuth 授权登录腾讯微云账号后，可完整操作网盘文件：**浏览文件**（列出全部文件或按图片/文档/视频/音乐分类查看）、**上传文件**（从本地上传至微云）、**下载文件**（从微云下载到本地指定目录）、**分享文件**（自动生成分享链接）、**文件管理**（重命名/删除）、**批量操作**（如一键下载某分类下所有文件）。适合替代手动浏览器操作，实现文件管理的自动化。<br><br>⚠️ 注意事项：**该能力基于腾讯微云 MCP 连接器实现**，需先在连接器管理中启用「微云 (tencent-weiyun)」并完成 OAuth 授权（QQ/微信账号登录）；微云有免费存储空间限制（通常 10GB 免费额度），超出后需付费扩容；大文件上传/下载受网络带宽影响，超大型文件建议分批处理；分享链接有时效性和访问权限设置，分享前请确认；删除操作不可恢复（微云无回收站机制），执行前务必确认；技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "在 WorkBuddy 连接器管理中启用「微云 (tencent-weiyun)」连接器",
    "需要腾讯微云账号（QQ/微信登录）",
    "完成 OAuth 授权登录",
    "安装 weiyun 技能",
    "支持文档、图片、视频、音乐等分类浏览"
  ],
  "steps":[
    "浏览文件：「列出我微云里的所有文件」或「查看图片分类」",
    "上传文件：「把这个文件上传到微云」",
    "下载文件：「下载微云里的XX文件到本地」",
    "分享文件：「生成XX文件的分享链接」",
    "文件管理：「把XX文件重命名为YY」「删除XX文件」",
    "批量操作：「把微云里所有图片下载到本地」"
  ],
  "example":"帮我把微云里所有2025年的文档下载到本地 D:/Documents/2025/ 目录，然后生成一个分享链接包含这些文件。",
  "scenarios":[
    "云盘文件批量管理，替代手动操作",
    "大文件分享，自动生成分享链接",
    "本地与云端文件同步"
  ]
},
{
  "id":"tencent-docs-collab",
  "ico":"📝",
  "title":"腾讯文档在线协作",
  "desc":"使用 tencent-docs 技能，对接腾讯文档 OpenAPI，创建、编辑、管理在线文档（文档/表格/幻灯片），支持多人实时协作、权限管理、版本历史。",
  "category":"文件与知识管理",
  "status":"已落地",
  "hot":True,
  "overview":"基于腾讯文档（tencent-docs）MCP 连接器的在线协作能力，支持三种文档类型的全生命周期管理：**文档**（Word 类在线编辑）、**Excel 表格**（结构化数据处理）、**PPT 幻灯片**（演示文稿制作）。核心能力：创建空白文档/从模板创建、编辑正文/追加内容、创建表格并填充数据、权限管理（设置协作者及可编辑/只读权限）、读取文档内容、搜索文档（按关键词查找）。天然支持多人实时协作和版本历史追踪。<br><br>⚠️ 注意事项：**该能力基于腾讯文档 MCP 连接器实现**，需先在连接器管理中启用「腾讯文档 (tencent-docs)」并完成 QQ/微信账号 OAuth 授权；个人版和企业版功能略有差异（企业版支持更多权限粒度和审批流程）；文档有字数/行数上限（个人版单文档约 5 万字）；权限变更对所有已授权协作者即时生效，修改权限时请谨慎；搜索仅限当前账号有权限访问的文档范围；技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "在 WorkBuddy 连接器管理中启用「腾讯文档 (tencent-docs)」连接器",
    "需要腾讯文档账号（QQ/微信登录）",
    "完成 OAuth 授权",
    "安装 tencent-docs 技能",
    "支持文档、Excel 表格、PPT 幻灯片三种类型"
  ],
  "steps":[
    "创建文档：「帮我创建一个腾讯文档，标题是XX」",
    "编辑内容：「在文档中添加以下内容......」",
    "创建表格：「创建一个 Excel 表格，包含以下列......」",
    "权限管理：「把这个文档分享给A，设置为可编辑权限」",
    "读取文档：「读取XX文档的内容」",
    "搜索文档：「搜索包含『Q3规划』的文档」"
  ],
  "example":"帮我创建一个腾讯在线表格，标题是「2026年Q1产品路线图」，包含以下列：功能名称、优先级、负责人、预计上线时间、状态。然后分享给产品团队，设置为可编辑权限。",
  "scenarios":[
    "团队协作文档自动创建和分发",
    "会议纪要实时记录到在线文档",
    "项目管理表格自动化创建和更新"
  ]
},
{
  "id":"xiaoe-workbuddy-integration",
  "ico":"🔗",
  "title":"小鹅通打通 WorkBuddy 流程",
  "desc":"小鹅通是国内主流的知识付费与私域运营平台，WorkBuddy 是 AI Agent 工作平台。通过 xiaoe-claw 技能和 xiaoe-cloud-cli 连接器，把两个平台打通：在小鹅通里产生的课程、订单、用户、学习数据，可以自动同步到 WorkBuddy，由 AI Agent 进行内容生产、用户分层、运营动作和数据分析。",
  "category":"协作办公",
  "status":"已落地",
  "hot":False,
  "overview":"打通知识付费平台（小鹅通）与 AI Agent 平台（WorkBuddy）的双向数据管道。基于 xiaoe-claw 技能（小鹅通店铺全能管理助手）+ xiaoe-cloud-cli MCP 连接器（小鹅通连接器），实现七大运营动作自动化：**商品/课程同步**（查看店铺上架商品）、**订单数据打通**（查询近期订单并导出 Excel）、**用户画像分析**（付费用户画像、复购率、留存率）、**学习数据洞察**（课程完课率、学习时长、次留率）、**内容自动生产**（课程大纲→公众号文章→小红书海报→群发推广）、**运营自动化**（未复购用户优惠券推送）、**闭环监控**（每日店铺运营日报自动输出）。<br><br>⚠️ 注意事项：**需要小鹅通商家账号**（店铺管理员权限），并在 xiaoe-tech.com 开放平台创建应用获取 AppID 和 AppSecret——这两个凭据需填入 .env 或 MCP 配置中，对外站点请用占位符替代；xiaoe-cloud-cli 为 MCP 连接器，xiaoe-claw 为技能层，两者配合使用；小鹅通 API 有频率限制，批量拉取时注意控制节奏；用户数据和订单数据涉及隐私，使用时遵守《个人信息保护法》；技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "在 WorkBuddy 技能中心安装「xiaoe-claw」技能（小鹅通店铺全能管理助手）",
    "在 WorkBuddy 连接器管理中启用「xiaoe-cloud-cli」小鹅通连接器",
    "准备小鹅通商家账号，并确保有店铺管理员权限",
    "登录小鹅通开放平台（https://xiao-e-tech.com/），创建应用获取 AppID 和 AppSecret",
    "在 WorkBuddy 的 .env 或 MCP 配置中填入：XIAOE_APPID=你的AppID, XIAOE_APPSECRET=你的AppSecret",
    "点击连接器「信任」按钮完成授权，测试连接：「查看我店铺里所有上架的商品」",
    "如需知识库联动，开启 ima 或知识库连接器，把课程内容同步给 WorkBuddy 做问答调用"
  ],
  "steps":[
    "商品/课程同步：「查看小鹅通店铺里所有上架的课程商品」",
    "订单数据打通：「查询最近7天的订单，按金额排序，导出到 Excel」",
    "用户画像分析：「分析店铺用户画像，付费用户有多少，复购率是多少」",
    "学习数据洞察：「查看课程 XX 的完课率、学习时长、次留率」",
    "内容自动生产：「根据课程大纲生成一篇公众号推广文章」→ 用 wechat-publisher 推到草稿箱",
    "运营自动化：「给最近30天未复购的用户创建一张满100减20的优惠券」",
    "闭环监控：每天早上8点自动输出「昨日小鹅通店铺运营日报」"
  ],
  "example":"帮我把小鹅通店铺和 WorkBuddy 打通。现在店铺里有一个教培行业课程包，我需要：1）查看这个课程包的订单和用户画像；2）根据课程大纲生成一篇公众号文章；3）给30天内未付费的潜在用户推一张优惠券；4）把最近7天的销售数据整理成腾讯文档日报。",
  "scenarios":[
    "知识付费店铺日常运营自动化：商品、订单、用户、数据一站式管理",
    "课程营销内容自动化：课程大纲→公众号文章→小红书海报→群发推广",
    "私域用户分层运营：按付费/完课/沉默等标签自动触达，提高复购和转化",
    "小鹅通 + 公众号 + 视频号矩阵：一个 WorkBuddy 工作流串联多个平台"
  ]
},
{
  "id":"hr-recruitment",
  "ico":"👤",
  "title":"招聘 JD 生成与简历智能筛选",
  "desc":"利用 WorkBuddy 的自然语言能力，结合企业信息查询（企查查/天眼查）和文档处理，实现招聘全流程自动化：从岗位 JD 生成、简历批量解析、人岗匹配评分到面试问题智能生成。",
  "category":"人力资源",
  "status":"已落地",
  "hot":False,
  "overview":"基于多技能组合的招聘自动化流水线：**JD 生成**——输入岗位名称和要求，AI 按行业标准生成完整 JD（岗位职责/任职要求/加分项/薪资范围）；**简历解析**——将收到的简历文件拖入对话，AI 提取关键信息（学历/工作年限/技能栈/项目经验）；**人岗匹配评分**——按自定义规则打分（学历权重20%、经验权重40%、技能匹配30%、加分项10%），输出匹配度排名表；**面试题生成**——为高匹配候选人自动生成针对性技术/行为面试题。依赖技能：qcc-company 或 tyc-mcp（企业背景调查）、tencent-docs（简历表格读写）。可选扩展：在 .workbuddy/skills/ 下创建 hr-recruitment 自定义技能固化评分模板。<br><br>⚠️ 注意事项：**人岗匹配评分仅为辅助参考**，最终录用决策应结合面试表现和综合判断；评分权重（学历/经验/技能/加分项）可根据岗位类型调整（技术岗重技能、管理岗重经验），建议先跑几轮验证合理性；简历含敏感个人信息（手机号/身份证号），处理时注意隐私保护，不要外传或公开存储；JD 中的薪资范围建议参考行业薪酬报告而非随意填写；技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "安装 qcc-company（企查查）或 tyc-mcp（天眼查）技能，用于查询企业基本信息",
    "安装 tencent-docs 技能，用于简历表格的读写和导出",
    "在 .workbuddy/skills/ 下创建自定义技能 hr-recruitment，定义 JD 模板和评分规则",
    "配置简历解析规则：学历权重20%、经验权重40%、技能匹配30%、加分项10%",
    "设置定时任务：每天早上自动从邮箱拉取新简历并解析"
  ],
  "steps":[
    "输入指令：「帮我写一份高级Java工程师的JD，要求5年经验，熟悉微服务，工作地点长沙」",
    "AI 根据行业标准生成完整 JD（岗位职责、任职要求、加分项、薪资范围）",
    "将收到的简历文件拖入对话，输入「解析这些简历，按匹配度排序」",
    "AI 逐份解析简历关键信息（学历、工作年限、技能栈、项目经验）",
    "自动评分并输出匹配度排名表，标注每份简历的优劣势",
    "输入「为匹配度最高的3位候选人生成面试问题」→ AI 生成针对性技术面试题"
  ],
  "example":"我们公司正在招一名产品经理，base长沙，3-5年经验，需要熟悉B端SaaS。帮我：1）写一份JD；2）把这10份简历按匹配度排序打分；3）为前3名候选人各生成5道面试题。",
  "scenarios":[
    "批量招聘季快速筛选：一次处理上百份简历，30分钟出结果",
    "多岗位并行招聘：同时生成多个岗位的JD和面试题",
    "简历库沉淀：历史简历自动归档，后续有匹配岗位直接召回"
  ]
},
{
  "id":"training-assessment",
  "ico":"👥",
  "title":"员工培训方案与绩效评估",
  "desc":"结合 WorkBuddy 文档生成能力和知识库管理，实现员工培训全流程：培训需求分析、课程方案设计、培训效果评估。同时支持绩效评估报告自动生成和面谈术建议。",
  "category":"人力资源",
  "status":"已落地",
  "hot":False,
  "overview":"基于多技能组合的人才发展管理方案：**需求分析**——输入岗位/团队信息，AI 从知识库调取岗位能力模型，对比现有技能差距输出需求分析；**方案设计**——根据需求自动生成培训计划（课程大纲/每周目标/考核方式/讲师安排）；**效果评估**——培训结束后输入考核成绩，AI 自动生成培训效果评估报告（含改进建议和面谈话术）。依赖技能组合：tencent-docs（方案文档生成）、ima-skills（知识库存制度/岗位说明书）、official-document-skill（正式培训通知/考核文件）。可选：在知识库中建立「培训资源库」和「绩效考核标准库」，季度末自动汇总数据生成评估报告。<br><br>⚠️ 注意事项：**培训方案需结合企业实际情况调整**——AI 生成的框架和课程大纲仅供参考，具体讲师人选、时间安排、预算需与 HR 部门和业务负责人确认；绩效考核数据涉及员工切身利益，评估报告生成前应确保数据来源准确且经过适当脱敏；面谈话术建议语气温和、建设性为主，避免直接批评；季度/年度评估任务可通过 automation_update 设置定时触发；技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "安装 tencent-docs 技能，用于生成培训方案文档和绩效评估报告",
    "安装 ima-skills 知识库技能，将公司制度、岗位说明书导入知识库",
    "安装 official-document-skill（公文写作技能），生成正式培训通知和考核文件",
    "在知识库中建立「培训资源库」和「绩效考核标准库」",
    "设置定时任务：季度末自动汇总绩效数据生成评估报告"
  ],
  "steps":[
    "输入指令：「分析技术部Q3培训需求，岗位包括前端、后端、测试」",
    "AI 从知识库调取岗位能力模型，对比现有技能差距，输出需求分析",
    "输入「为前端工程师设计为期4周的Vue3培训方案」",
    "AI 生成完整方案：课程大纲、每周计划、讲师安排、考核方式",
    "培训结束后输入「根据考核成绩生成培训效果评估报告」",
    "季度绩效输入「根据以下KPI数据生成绩效评估报告并给出面谈话术」"
  ],
  "example":"技术部有15人需要Vue3培训，其中5人是转岗。帮我设计一个4周的培训方案，包括课程大纲、每周目标、考核方式。培训结束后根据考核成绩生成效果评估报告，并给每位参训员工写一段绩效面谈话术。",
  "scenarios":[
    "新员工入职培训：自动生成定制化培训计划和考核试题",
    "季度/年度绩效评估：KPI 数据自动汇总，生成报告和改进建议",
    "转岗培训：针对新旧岗位技能差异设计专属培训路径"
  ]
},
{
  "id":"expense-reimbursement",
  "ico":"🧾",
  "title":"发票智能识别与报销自动化",
  "desc":"利用 WorkBuddy 多模态能力识别发票图片信息，结合腾讯文档实现报销流程自动化：发票 OCR 识别、真伪校验、报销单自动生成、审批流程跟踪、费用统计分析。",
  "category":"财务行政",
  "status":"已落地",
  "hot":False,
  "overview":"基于多模态图像识别 + 腾讯文档 + 微云的报销自动化流水线：**发票识别**——将发票拍照/截图发送给对话窗口，AI 通过 OCR 自动提取关键字段（发票号码/开票日期/金额/税额/购买方/销售方）；**真伪校验**——与税务局查验接口比对（如已配置），标注异常发票；**报销单生成**——根据公司差旅标准（经济舱机票+300元/天酒店+100元/天餐补）自动计算可报销金额，生成腾讯文档格式报销单供审批；**费用统计**——按月/部门自动汇总报销数据生成可视化报表。依赖技能：tencent-docs（报销单表格）、weiyun（发票图片统一存储）。可选扩展：创建 expense-reimbursement 自定义技能固化报销规则模板。<br><br>⚠️ 注意事项：**发票 OCR 识别准确率非100%**，金额、税号等关键字段务必人工复核后再提交审批；税务局查验接口有调用频率限制，大批量发票建议分批校验；报销标准（机票/酒店/餐补限额）需按公司实际财务制度配置，示例中的数值仅为演示；异常发票预警（重复报销/金额异常/过期发票）为辅助提示，最终判定以财务审核为准；可设置每月1号自动生成上月费用统计表的定时任务；技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "安装 tencent-docs 技能，用于创建和管理报销单表格",
    "安装 weiyun（微云）技能，用于发票图片统一存储",
    "在 .workbuddy/skills/ 下创建 expense-reimbursement 自定义技能",
    "配置报销规则模板：差旅标准、餐补标准、交通报销规则",
    "设置定时任务：每月1号自动生成上月费用统计报表"
  ],
  "steps":[
    "将发票拍照/图片发送到对话窗口",
    "输入「识别这些发票，提取关键信息并校验」",
    "AI 自动提取：发票号码、开票日期、金额、税额、购买方、销售方",
    "与税务局查验接口比对（如已配置），标注异常发票",
    "输入「根据报销标准生成报销单」→ AI 自动填充腾讯文档报销表",
    "输入「生成上月费用统计报表，按部门分类」"
  ],
  "example":"这是我这次出差的5张发票（图片），帮我识别提取信息，按公司差旅报销标准（经济舱机票+300元/天酒店+100元/天餐补）生成报销单，然后创建一个腾讯文档报销表让我审批。",
  "scenarios":[
    "差旅报销批量处理：一次提交多张发票，自动分类汇总",
    "月度费用统计：自动汇总各部门报销数据生成可视化报表",
    "异常发票预警：重复报销、金额异常、过期发票自动标记"
  ]
},
{
  "id":"budget-analysis",
  "ico":"📈",
  "title":"财务报表分析与预算编制",
  "desc":"结合 WorkBuddy 的 westock-data 金融数据能力和腾讯文档，实现财务分析全流程：三大报表分析、关键财务指标计算、预算模板自动生成、预算执行差异分析，输出专业财务分析报告。",
  "category":"财务行政",
  "status":"已落地",
  "hot":False,
  "overview":"基于 westock-data（上市公司财务对标）+ tencent-docs（报告输出）+ neo-crm（销售数据辅助预算编制）+ budget-analysis 自定义技能的财务分析闭环：**报表分析**——上传或输入资产负债表/利润表/现金流量表数据，AI 自动计算关键财务指标（流动比率/速动比率/资产负债率/ROE/ROA/毛利率等）；**行业对标**——通过 westock-data 获取同行业上市公司数据进行对比分析；**预算编制**——根据历史数据趋势自动生成下一年度预算（收入预算/成本预算/费用预算），输出为腾讯文档格式。<br><br>⚠️ 注意事项：**财务数据敏感性极高**——上传的报表数据可能含公司机密，处理时注意信息安全，不建议在公共环境或对外渠道展示分析过程；AI 计算的财务指标基于输入数据的准确性，垃圾进垃圾出，请确保原始数据无误；行业对标选取的同业公司样本量影响对比结论的可靠性，建议至少选择 3 家以上可比公司；预算编制为预测性质，实际执行中需根据业务变化动态调整；技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "安装 westock-data 技能，获取上市公司财务数据作为行业对标",
    "安装 tencent-docs 技能，用于生成财务分析报告和预算表",
    "安装 neo-crm（销售易CRM）技能，拉取营收数据辅助预算编制",
    "在知识库中导入历史三年财务报表作为分析基准",
    "创建 budget-analysis 自定义技能，定义预算科目和编制规则"
  ],
  "steps":[
    "上传或输入资产负债表、利润表、现金流量表数据",
    "输入「分析这三张报表，计算关键财务指标」",
    "AI 自动计算：流动比率、速动比率、资产负债率、ROE、ROA、毛利率等",
    "输入「与行业对标分析」→ 调取同行业上市公司数据进行对比",
    "输入「根据历史数据和增长趋势编制下一年度预算」",
    "AI 生成预算表（腾讯文档），含收入预算、成本预算、费用预算"
  ],
  "example":"这是我们公司2024年三季度的资产负债表和利润表数据。帮我：1）计算关键财务指标；2）与同行业（选3家上市公司）对标分析；3）根据历史趋势编制2025年年度预算，包括收入预算、成本预算、费用预算，输出到腾讯文档。",
  "scenarios":[
    "季度/年度财务分析：自动生成专业财务分析报告",
    "预算编制与执行监控：预算vs实际差异实时跟踪",
    "融资分析：为融资计划准备财务数据包和商业计划书"
  ]
},
{
  "id":"contract-review",
  "ico":"📄",
  "title":"合同智能审查与风险提示",
  "desc":"结合北大法宝/华宇元典法律数据库和 WorkBuddy 文档分析能力，实现合同全流程智能审查：条款逐条审查、风险点标注、修改建议生成、合规性检查，输出审查报告。",
  "category":"法务合规",
  "status":"已落地",
  "hot":False,
  "overview":"基于法律数据库 + AI 文档分析的合同审查四件套：**pkulaw（北大法宝）**——提供法律法规和合同范本数据库；**yuandian-mcp（华宇元典）**——提供裁判判例数据用于风险点类比；**tencent-docs**——生成合同审查报告文档；**contract-review 自定义技能**——定义审查规则和风险等级体系。审查流程：上传/粘贴合同文本 → AI 逐条审查（主体资格/标的条款/付款条款/违约责任/争议解决）→ 每个风险点标注等级（高/中/低）并引用相关法条 → 输出完整审查报告（含修改建议和风险提示）。<br><br>⚠️ 注意事项：**AI 合同审查为辅助工具，不替代专业律师审核**——重大合同（金额大/期限长/条款复杂）必须经法务或执业律师最终把关；风险等级判定基于通用规则，特殊行业（金融/医疗/建筑）可能有额外合规要求需人工补充；引用的法条可能存在更新滞后，重要条款应以最新法规为准；合同文本可能含商业机密，审查过程中注意保密；技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "安装 pkulaw（北大法宝）技能，接入法律法规和合同范本数据库",
    "安装 yuandian-mcp（华宇元典）技能，获取案例判例数据",
    "安装 tencent-docs 技能，用于生成合同审查报告",
    "在知识库中导入公司合同模板库和审查标准",
    "创建 contract-review 自定义技能，定义审查规则和风险等级"
  ],
  "steps":[
    "将合同文本上传或粘贴到对话窗口",
    "输入「审查这份合同，标注风险点并给出修改建议」",
    "AI 逐条审查：主体资格、标的条款、付款条款、违约责任、争议解决等",
    "每个风险点标注等级（高/中/低），引用相关法条",
    "输入「对比我们的标准模板，列出差异条款」",
    "AI 输出完整审查报告，含修改建议和风险提示"
  ],
  "example":"这是一份供应商合同，对方是深圳XX科技公司。帮我审查这份合同，重点关注：1）付款条款是否有利；2）违约责任是否对等；3）知识产权归属是否清晰；4）争议解决条款是否合理。标注所有风险点并给出修改建议，输出审查报告。",
  "scenarios":[
    "采购/销售合同审查：批量审查，30分钟出报告",
    "劳动合同合规检查：对照劳动法逐条审查",
    "合同模板库管理：标准模板+审查规则，新合同自动对标"
  ]
},
{
  "id":"curriculum-design",
  "ico":"🎓",
  "title":"课程大纲与试题自动生成",
  "desc":"结合 WorkBuddy 文档生成和知识库能力，实现教育培训内容全流程自动化：教学大纲设计、知识点拆解、题库批量生成、评分标准制定，支持多种题型和难度级别。",
  "category":"人力资源",
  "status":"已落地",
  "hot":False,
  "overview":"基于文档生成 + 知识库 + 小鹅通的培训内容生产流水线：**大纲设计**——输入课程主题/目标人群/课时数，AI 按认知规律拆解知识点，生成周计划（学习目标+知识点+实践项目）；**题库生成**——按章节/题型/难度批量生成题目（选择题/填空题/编程题），每题附答案解析和难度标注；**试卷组装**——按难度比例（如 3:5:2）从题库抽取题目组成期中/期末试卷，输出完整试卷文档（腾讯文档格式）；**发布分发**——可直接打印或发布到小鹅通知识付费平台。依赖技能组合：tencent-docs（文档输出）、ima-skills（教材/标准导入知识库）、xiaoe-cloud-cli（发布到小鹅通）。可选扩展：创建 curriculum-design 自定义技能固化教学设计规则。<br><br>⚠️ 注意事项：**教学内容的专业准确性是底线**——AI 生成的课程大纲和试题需经领域专家审核后方可使用，尤其是技术类/医学类/法律类专业内容；难度分级（初级/中级/高级/专家级）为相对概念，同一道题对不同学员难度感知不同，建议结合学员实际水平调整；题库答案解析需确保正确性，首次生成的题目建议抽样验证；发布到小鹅通前请预览排版效果；技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "安装 tencent-docs 技能，用于生成课程大纲和试卷文档",
    "安装 ima-skills 知识库技能，导入教材和课程标准",
    "安装 xiaoe-cloud-cli（小鹅通）技能，直接发布到知识付费平台",
    "在知识库建立「课程标准库」和「题库模板库」",
    "创建 curriculum-design 自定义技能，定义知识点拆解规则"
  ],
  "steps":[
    "输入指令：「为Python入门课程设计16周教学大纲，面向零基础学员」",
    "AI 按认知规律拆解知识点，生成周计划（学习目标+知识点+实践项目）",
    "输入「为第3章的数据类型章节生成20道练习题，合选择题/填空题/编程题」",
    "AI 批量生成题目，每题附答案解析和难度标注",
    "输入「生成期中试卷，难度比3:5:2，合评分标准」",
    "输出完整试卷文档（腾讯文档），可直接打印或发布到小鹅通"
  ],
  "example":"我要开一门「AI办公效率提升」的线上课程，12课时，面向职场白领。帮我：1）设计课程大纲，每课时含学习目标和案例；2）为第4课时「AI文文档」生成15道课后练习题；3）生成期末考核方案和评分标准。所有内容输出到腾讯文档。",
  "scenarios":[
    "培训机构课程开发：快速产出标准化课程包",
    "企业内训内容生产：岗位技能课程+考核题库一键生成",
    "知识付费内容创作：课程大纲+题库+营销文案一条龙"
  ]
},
{
  "id":"competitor-marketing",
  "ico":"🎯",
  "title":"竞品分析与营销方案策划",
  "desc":"结合企查查企业信息、westock-data 行业数据和 WorkBuddy 内容生成能力，实现营销全链路：竞品调研、SWOT 分析、营销日历、投放策略、文案撰写，输出完整营销方案。",
  "category":"产品营销",
  "status":"已落地",
  "hot":True,
  "overview":"基于「数据采集→分析→策略→内容→投放」五步营销闭环的多技能组合方案：**竞品调研**——通过 qcc-company 查询竞品工商信息和融资情况，通过网页搜索获取产品信息；**SWOT 分析**——AI 综合竞品数据做优势/劣势/机会/威胁四象限分析；**方案制定**——输出 Q3/Q4 营销方案（目标用户/渠道策略/内容日历/预算分配/KPI 指标）；**文案生产**——通过 wechat-write / wechat-article-pro 生成各渠道营销文案（公众号长文/小红书种草/朋友圈短文案）；**投放执行**——通过 tencentads（腾讯营销投放）获取广告投放数据辅助决策。全程可在知识库中维护品牌手册和营销策略模板。<br><br>⚠️ 注意事项：**竞品分析数据来源于公开渠道**（企查查工商信息/官网/公开报道），内部数据（营收/用户量/转化率）为估算值，标注时请明确区分；营销方案中的预算分配和 KPI 目标需结合公司实际资源设定，AI 给出的仅为框架参考；广告投放数据（tencentads）需要腾讯广告账号授权；不同渠道的文案风格和长度规范差异较大（公众号长文 vs 朋友圈140字 vs 小红书 emoji 风），生成后需按平台特性微调；技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "安装 qcc-company（企查查）技能，查询竞品工商和融资信息",
    "安装 tencentads（腾讯营销投放）技能，获取广告投放数据",
    "安装 wechat-write 技能，生成营销软文和推广文案",
    "安装 tencent-docs 技能，输出营销方案文档",
    "在知识库导入品牌手册和营销策略模板"
  ],
  "steps":[
    "输入「分析 XX 行业的3个主要竞品，做 SWOT 分析」",
    "AI 调取企查查数据（融资轮次/规模/团队）+ 网页搜索产品信息",
    "生成竞品对比表和 SWOT 分析图",
    "输入「根据竞品分析制定Q3营销方案」",
    "AI 生成方案：目标用户、渠道策略、内容日历、预算分配、KPI 指标",
    "输入「为方案中的5个营销节点各写一篇推广文案」"
  ],
  "example":"我们的产品是一款AI办公助手，竞品是Notion AI和飞书智能伙伴。帮我：1）查询这三家公司的融资和团队信息；2）做产品功能对比和SWOT分析；3）制定Q3小红书+公众号号营销方案，包括内容日历和投放预算；4）为前3个营销节点写推广文案。",
  "scenarios":[
    "新品上市营销策划：竞品分析→定位→方案→文案一条龙",
    "季度营销规划：内容日历+渠道策略+预算分配",
    "品牌舆情监控：定时抓取竞品动态和用户评价"
  ]
},
{
  "id":"meeting-minutes-tracker",
  "ico":"🚩",
  "title":"会议纪要自动化与任务追踪",
  "desc":"结合腾讯会议 AI 纪要和 WorkBuddy 文档能力，实现会议全流程自动化：录音转写、纪要自动生成、任务分配与追踪、决议跟进提醒，让行政管理工作效率提升10倍。",
  "category":"协作办公",
  "status":"已落地",
  "hot":False,
  "overview":"基于「会议录制→纪要提取→任务拆解→跟进追踪」四步闭环的行政自动化方案：**会议纪要生成**——通过 tmeet-skill 从腾讯会议拉取录制文件和 AI 智能纪要，AI 进一步转写全文并按公司标准格式输出纪要文档；**任务提取**——AI 从纪要中自动识别待办事项（参会人员/议题/讨论要点/决议/待办事项）；**任务分配**——将待办事项创建为任务，分配对应负责人和截止日期；**进度追踪**——任务同步到 TAPD 项目管理工具，每天推送进度提醒。依赖技能：tmeet-skill（腾讯会议）、tencent-docs（纪要文档）、tapd（项目管理）。可在知识库中维护会议纪要模板和任务追踪规范。<br><br>⚠️ 注意事项：**AI 纪要提取的待办事项可能遗漏或误判**——重要决议和任务分配建议人工复核后再录入 TAPD；TAPD 任务同步需要 tapd 连接器授权（企业版 TAPD）；会议纪要格式（标题/参会人/时间/议题/决议/待办）可按公司规范自定义模板；跨部门会议的任务分配涉及多人协作，建议在纪要中抄送相关方确认；可设置每天早上9点推送未完成任务提醒的定时任务；技能名称以 WorkBuddy 技能中心实时搜索结果为准。",
  "deploy":[
    "安装 tmeet-skill（腾讯会议）技能，获取会议录制和 AI 智能纪要",
    "安装 tencent-docs 技能，生成会议纪要文档和任务追踪表",
    "安装 tapd 技能，将会议任务直接创建为 TAPD 工作项",
    "配置定时任务：每天早上推送当日待跟进的会议决议",
    "在知识库导入会议纪要模板和任务追踪规范"
  ],
  "steps":[
    "会议结束后输入「获取今天下午产品评审会的 AI 纪要」",
    "AI 从腾讯会议拉取智能纪要和转写全文",
    "输入「根据纪要生成会议纪要文档，按标准格式」",
    "AI 自动提取：参会人员、议题、讨论要点、决议、待办事项",
    "输入「把待办事项创建为任务，分配给对应负责人」",
    "任务自动同步到 TAPD，每天推送进度提醒"
  ],
  "example":"今天下午2点开了一个产品需求评审会，参会人有产品、设计、开发共8人。帮我：1）从腾讯会议拉取AI纪要；2）按公司标准格式生成会议纪要；3）把讨论中确定的5个待办事项分配给对应的人并创建TAPD任务；4）设置每天早上9点推送未完成任务提醒。",
  "scenarios":[
    "周会/月会纪要自动化：30秒生成标准纪要文档",
    "项目评审会任务追踪：决议→任务→TAPD→进度推送",
    "跨部门会议协调：纪要自动分发，任务自动分配"
  ]
}
]

# ============================ 页面构建 ============================
def doc_sidebar(active_name):
    # 分区 part：笔记（WB 手册/案例）+ 进阶篇 + 岗位与行业落地 + Skills / 交流
    parts = [
        ("WB手册",  MANUAL_WB,  C_WB,    "manual-wb.html"),
        ("WB案例",  CASES_WB,   C_WB,    "cases-wb.html"),
        ("进阶篇",  ADVANCED,   C_WB,    "advanced.html"),
        ("岗位与行业落地", INDUSTRY, C_INDUSTRY, "industry.html"),
    ]
    out = ""
    for name, chs, color, href in parts:
        is_active = (name == active_name)
        chapters = "".join(
            '<a class="sidebar-chapter" href="' + href + '#' + c[0] + '">' + c[2] + '</a>'
            for c in chs)
        out += ('<div class="sidebar-part ' + ('expanded active' if is_active else '') + '">'
                '<div class="sidebar-part-header" onclick="toggleSidebarPart(this)">'
                '<span class="sidebar-part-dot" style="background:' + color + '"></span>'
                '<span class="sidebar-part-name">' + name + '</span>'
                '<svg class="sidebar-part-chevron" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>'
                '</div><div class="sidebar-chapters">' + chapters + '</div></div>')
    others = ('<div class="sidebar-part"><div class="sidebar-part-header" onclick="location.href=\'skills.html\'">'
              '<span class="sidebar-part-dot" style="background:#A855F7"></span>'
              '<span class="sidebar-part-name">Skills</span></div></div>'
              '<div class="sidebar-part"><div class="sidebar-part-header" onclick="location.href=\'community.html\'">'
              '<span class="sidebar-part-dot" style="background:#64748B"></span>'
              '<span class="sidebar-part-name">交流</span></div></div>')
    return ('<aside class="sidebar" id="sidebar"><div class="sidebar-header">导航</div>'
            '<a class="sidebar-back" href="index.html">← 返回首页</a>' + out + others + '</aside>')

def doc_toc(chs):
    return '' 

def reading_page(title, sub, chs):
    body = '<div class="reading-page"><div class="page-title">' + title + '</div>' \
           '<div class="page-sub">' + sub + '</div>'
    for c in chs:
        body += ('<section class="chapter" id="' + c[0] + '">'
                 '<div class="chapter-header"><span class="chapter-badge">' + c[3] + '</span>'
                 '<span class="chapter-title">' + c[2] + '</span></div>'
                 '<div class="chapter-body">' + c[4] + '</div></section>')
    body += '</div>'
    return body

def build_doc(active_name, title, sub, chs, fname, pcolor, topbar_active=None):
    accent = ('<style>:root{--accent:' + pcolor + ';--accent-soft:' + hex_rgba(pcolor, .12) +
              ';--accent-grad:' + pcolor + '}</style>')
    html = ('<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<meta name="description" content="' + SITE_DESC + '">'
            '<title>' + title + ' · ' + SITE_TITLE + '</title><style>' + CSS + '</style>' + accent + '</head>'
            '<body class="doc-body">' + topbar(topbar_active if topbar_active is not None else active_name) +
            '<div class="layout">' + doc_sidebar(active_name) +
            '<main class="reading-section">' + reading_page(title, sub, chs) + '</main>' +
            doc_toc(chs) + '</div>' + footer() +
            '<script>' + JS + '</script></body></html>')
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(html)
    print("生成:", fname)

# ============================ WB 手册：单页单章切换阅读器 ============================
# 体验：打开 manual-wb.html 直接是第 1 章，一页只显示一章；
# 底部「下一章」按钮手动切换；左侧边栏点击章节不刷新页面直接切换；
# URL 保持 #chapter-N 可单章分享。
READER_CSS = """
.reading-header{display:flex;flex-direction:column;gap:14px;margin:0 0 30px;align-items:center;
  padding-bottom:22px;border-bottom:1px solid var(--border)}
.reading-header h1{font-family:var(--font-xbs);font-size:26px;margin:0;color:var(--doc-ink);
  font-weight:400;text-align:center;letter-spacing:1px;line-height:1.5}
.reading-progress{display:flex;align-items:center;gap:14px;font-size:13px;color:var(--text-tertiary);
  font-weight:500;width:100%;max-width:460px}
.progress-bar{flex:1;height:10px;background:var(--border);border-radius:6px;overflow:hidden;max-width:420px}
.progress-fill{height:100%;background:var(--accent);border-radius:6px;transition:width .3s ease}
.chapter-content{min-height:60vh}
.chapter-content .chapter-header{margin-bottom:18px}
.chapter-end{min-height:200px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:18px;margin:48px 0 0;padding:44px 0;border-top:1px dashed var(--border);text-align:center}
.chapter-end p{color:var(--text-tertiary);margin:0;font-size:14px}
.chapter-end-action{padding:14px 32px;border-radius:10px;background:var(--accent);color:#fff;font-weight:700;font-size:15px;text-decoration:none;transition:.15s;box-shadow:0 4px 14px var(--accent-soft)}
.chapter-end-action:hover{opacity:.92;transform:translateY(-1px)}
.chapter-end-finish{color:var(--text-tertiary);font-size:15px}
.sidebar-chapter.active{color:var(--accent);font-weight:700;background:var(--accent-soft);border-radius:6px}
@media (max-width:900px){
  .progress-bar{max-width:200px}
}
"""

CHAPTERS_JS = json.dumps([
    {"id": c[0], "num": c[1], "title": c[2], "cat": c[3], "html": c[4]}
    for c in MANUAL_WB
], ensure_ascii=False, separators=(',', ':'))

READER_JS = """
(function(){
  var chapters = __CHAPTERS__;
  var total = chapters.length;
  var contentEl = document.getElementById('chapter-content');
  if (!contentEl) return;            // 仅 manual-wb.html 执行，其他页面忽略
  var titleEl = document.getElementById('chapter-title');
  var progressText = document.getElementById('progress-text');
  var progressFill = document.getElementById('progress-fill');
  var endNext = document.getElementById('chapter-end-next');
  var endFinish = document.getElementById('chapter-end-finish');

  function getIdxFromHash(){
    var m = location.hash.match(/chapter-(\\d+)/);
    var idx = m ? parseInt(m[1], 10) - 1 : 0;
    return Math.max(0, Math.min(total - 1, idx));
  }

  function render(idx, pushState){
    var ch = chapters[idx];
    titleEl.textContent = ch.title;
    progressText.textContent = '第 ' + (idx + 1) + ' / ' + total + ' 章';
    progressFill.style.width = ((idx + 1) / total * 100) + '%';
    contentEl.innerHTML = '<section class="chapter" id="' + ch.id + '">' +
      '<div class="chapter-header"><span class="chapter-badge">' + ch.cat + '</span>' +
      '<span class="chapter-title">' + ch.title + '</span></div>' +
      '<div class="chapter-body">' + ch.html + '</div></section>';

    // 章节底部「下一章」按钮（手动点）
    if (idx < total - 1){
      endNext.style.display = 'inline-flex';
      endNext.textContent = '下一章：' + chapters[idx + 1].title + ' →';
      endNext.onclick = function(){ go(idx + 1); };
      endFinish.style.display = 'none';
    } else {
      endNext.style.display = 'none';
      endFinish.style.display = 'block';
    }

    // 侧边栏高亮：只匹配当前展开分类下的章节，避免跨分类索引错位
    document.querySelectorAll('.sidebar-part.expanded .sidebar-chapter').forEach(function(a, i){
      if (i === idx) a.classList.add('active');
      else a.classList.remove('active');
    });

    if (pushState !== false){
      var newHash = '#chapter-' + (idx + 1);
      if (location.hash !== newHash){
        history.pushState({idx: idx}, '', newHash);
      }
    }
    window.scrollTo({top: 0, behavior: 'smooth'});
  }

  function go(idx){ render(idx, true); }

  // 侧边栏 hash 链接点击切换（不刷新页面）
  document.querySelectorAll('.sidebar-part.expanded .sidebar-chapter').forEach(function(a){
    a.addEventListener('click', function(e){
      var m = a.getAttribute('href').match(/chapter-(\\d+)/);
      if (m){
        e.preventDefault();
        go(parseInt(m[1], 10) - 1);
      }
    });
  });

  // 注意：已去掉「滚动到底自动切换」与右下角浮窗，改为底部「下一章」按钮手动点（避免误触）

  window.addEventListener('popstate', function(e){
    render(getIdxFromHash(), false);
  });

  render(getIdxFromHash(), false);
})();
"""

def build_reader(active_name, page_title, chs, fname, pcolor, topbar_active=None):
    """单页单章切换阅读器：与 WB手册 完全一致的排版（目录/文章标题均为「第*章+标题」，
    底部「下一章」手动翻页，每页只显示一个章节）。cases-wb 与 manual-wb 共用此函数。"""
    chapters_js = json.dumps(
        [{"id": c[0], "num": c[1], "title": c[2], "cat": c[3], "html": c[4]} for c in chs],
        ensure_ascii=False, separators=(',', ':'))
    reader_js = READER_JS.replace('__CHAPTERS__', chapters_js)
    accent = ('<style>:root{--accent:' + pcolor + ';--accent-soft:'
              + hex_rgba(pcolor, .12) + ';--accent-grad:' + pcolor + '}</style>')
    sidebar = doc_sidebar(active_name)
    body = ('<div class="reading-page">'
            '<div class="reading-header">'
            '<h1 id="chapter-title">' + page_title + '</h1>'
            '<div class="reading-progress"><span id="progress-text">第 1 / ' + str(len(chs)) + ' 章</span>'
            '<div class="progress-bar"><div class="progress-fill" id="progress-fill"></div></div></div></div>'
            '<div class="chapter-content" id="chapter-content"></div>'
            '<div class="chapter-end">'
            '<a class="chapter-end-action" id="chapter-end-next" href="javascript:;">下一章 →</a>'
            '<p class="chapter-end-finish" id="chapter-end-finish" style="display:none">🎉 已读完最后一章</p>'
            '<p>读完本章，点击下方按钮手动切换到下一章</p></div></div>')
    html = ('<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<meta name="description" content="' + SITE_DESC + '">'
            '<title>' + page_title + ' · ' + SITE_TITLE + '</title>'
            '<style>' + CSS + READER_CSS + '</style>' + accent + '</head>'
            '<body class="doc-body">' + topbar(topbar_active if topbar_active is not None else active_name) +
            '<div class="layout">' + sidebar +
            '<main class="reading-section">' + body + '</main></div>' + footer() +
            '<script>' + JS + '</script>'
            '<script>' + reader_js + '</script></body></html>')
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(html)
    print("生成:", fname)

def build_index():
    # Hero
    hero = ('<section class="hero"><div class="hero-name">老田的 AI 实战笔记</div>'
            '<p class="hero-tagline">WorkBuddy 一线实战沉淀 —— 使用手册、真实案例、'
            '进阶心法与可复用 Skill。边用边记，持续更新。</p>'
            '<div class="hero-tags">'
            '<span class="hero-tag teal">WorkBuddy</span>'
            '<span class="hero-tag coral">实战案例</span>'
            '<span class="hero-tag purple">Skill 沉淀</span></div></section>')
    # 板块卡片（笔记类别）：仅保留 WorkBuddy 相关内容
    cards = [
        ("📘","WB手册","从 0 到 1，用好 WorkBuddy","📝 11 篇文章","manual-wb.html",C_WB),
        ("📂","WB案例","真实任务的完整复现","📝 11 篇文章","cases-wb.html",C_WB),
        ("🚀","进阶篇","从案例到系统，构建你的工作流","📝 4 篇文章","advanced.html",C_WB),
        ("🎯","岗位与行业落地","按岗位 / 行业视角组织实战内容","📝 4 篇文章","industry.html",C_INDUSTRY),
    ]
    card_html = '<div class="cards">'
    for ico, name, desc, meta, href, color in cards:
        card_html += ('<a class="card" href="' + href + '">'
                      '<div class="card-header">'
                      '<div class="card-ico" style="background:' + color + '22;color:' + color + '">' + ico + '</div>'
                      '<h3>' + name + '</h3></div>'
                      '<p>' + desc + '</p>'
                      '<div class="meta">' + meta + '</div><span class="arrow">→</span></a>')
    card_html += '</div>'
    # 全部文章 + 类别筛选（图2 风格）
    pills = ('<div class="filter-pills">'
             '<span class="filter-pill active" data-part="" onclick="filterArticles(\'\')">全部</span>'
             '<span class="filter-pill" data-part="使用手册" onclick="filterArticles(\'使用手册\')">使用手册</span>'
             '<span class="filter-pill" data-part="案例篇" onclick="filterArticles(\'案例篇\')">案例篇</span>'
             '<span class="filter-pill" data-part="进阶篇" onclick="filterArticles(\'进阶篇\')">进阶篇</span>'
             '<span class="filter-pill" data-part="岗位与行业落地" onclick="filterArticles(\'岗位与行业落地\')">岗位与行业落地</span>'
             '</div>')
    wraps = "".join(article_wrap(p[0],p[1],p[2],p[3],p[4]) for p in HOME_ARTICLES)
    list_html = '<div class="article-list">' + wraps + '</div>'
    body = ('<div>' + hero +
            build_search_section() +
            build_news_section() +
            '<section class="section" id="notebooks"><div class="section-head"><h2><span class="bar"></span>笔记类别</h2>'
            '<p>手册、案例、进阶、岗位与行业落地，按类别快速进入，内容持续补充中</p></div>' + card_html + '</section>'
            + build_ecosystem_showcase() +
            '<section class="section" style="padding-top:0"><div class="section-head"><h2>全部文章</h2>'
            '<p>点击任意文章跳转到对应篇章阅读</p></div>' + pills + list_html + '</section>'
            + build_case_showcase() + '</div>')
    html = wrap_page("首页", body)
    with open("index.html","w",encoding="utf-8") as f: f.write(html)
    print("生成: index.html")

def build_skills():
    # Hero
    hero = ('<section class="skills-hero"><h1>WorkBuddy Skills</h1>'
            '<p>' + str(len(SKILLS)) + ' 个已落地 / 运行中的实战技能，覆盖写作排版、内容生产、数据分析、自动化、企业微信、销售获客、文件与知识管理、法务合规、人力资源、财务行政、产品营销、协作办公、金融、设计、开发等场景。'
            '点击任意卡片查看部署方法、使用步骤和示例指令。</p></section>')

    # 分类标签
    cats = "".join(
        '<span class="skill-cat ' + ('active' if c == '全部' else '') + '" data-cat="' + c + '" onclick="filterSkills(\'' + c + '\')">' + c + '</span>'
        for c in SKILL_CATEGORIES
    )

    # 卡片网格
    grid = '<div class="skill-grid-v2">'
    details = ""
    for s in SKILLS:
        hot = '<span class="badge-hot">热门</span>' if s.get('hot') else ''
        grid += ('<div class="skill-card-v2" data-cat="' + s['category'] + '" onclick="openSkillModal(\'' + s['id'] + '\')">'
                 '<div class="top"><div class="ava">' + s['ico'] + '</div>'
                 '<div class="tit"><h3>' + s['title'] + '</h3>'
                 '<div class="badges">' + hot + '<span class="badge-cat">' + s['category'] + '</span></div></div></div>'
                 '<p class="desc">' + s['desc'] + '</p>'
                 '<div class="foot"><span>状态：' + s['status'] + '</span><span class="more">点击查看详情 →</span></div></div>')

        # 详情模板（弹窗用）
        deploy = "".join('<li>' + x + '</li>' for x in s['deploy'])
        steps = "".join('<li>' + x + '</li>' for x in s['steps'])
        scenarios = "".join('<div class="scenario">' + x + '</div>' for x in s['scenarios'])
        details += ('<div id="skillContent-' + s['id'] + '" style="display:none">'
                    '<div class="skill-modal-head">'
                    '<div class="ava">' + s['ico'] + '</div>'
                    '<div class="tit"><h2>' + s['title'] + '</h2>'
                    '<div class="badges">' + hot + '<span class="badge-cat">' + s['category'] + '</span><span class="badge-cat">' + s['status'] + '</span></div></div></div>'
                    '<div class="skill-modal-body">'
                    '<div class="skill-modal-sec"><div class="sec-title"><span class="sec-ico">①</span>技能概述</div><p>' + s['overview'] + '</p></div>'
                    '<div class="skill-modal-sec"><div class="sec-title"><span class="sec-ico">②</span>部署方法</div><ol>' + deploy + '</ol></div>'
                    '<div class="skill-modal-sec"><div class="sec-title"><span class="sec-ico">③</span>使用步骤</div><ol>' + steps + '</ol></div>'
                    '<div class="skill-modal-sec"><div class="sec-title"><span class="sec-ico">④</span>示例指令</div><div class="example">' + s['example'] + '</div></div>'
                    '<div class="skill-modal-sec"><div class="sec-title"><span class="sec-ico">⑤</span>应用场景</div><div class="scenarios">' + scenarios + '</div></div>'
                    '</div></div>')
    grid += '</div>'

    # 弹窗容器
    modal = ('<div class="skill-modal" id="skillModal" onclick="if(event.target===this)closeSkillModal()">'
             '<div class="skill-modal-box" onclick="event.stopPropagation()">'
             '<button class="skill-modal-close" onclick="closeSkillModal()">×</button>'
             '<div id="skillModalInner"></div></div></div>')

    body = (hero +
            '<section class="section"><div class="skill-cats">' + cats + '</div>' + grid + '</section>' +
            modal + details +
            build_prompts_section())
    html = wrap_page("Skills", body, active="Skills")
    with open("skills.html","w",encoding="utf-8") as f: f.write(html)
    print("生成: skills.html")

def build_prompts_section():
    """生成「AI 提示词社区」区块 HTML 片段（嵌入 skills.html，样式/内容参照 simouxuan.com 的 AI 提示词社区模块）"""
    cats = "".join(
        '<span class="prompt-cat ' + ('active' if c == '全部' else '') + '" data-cat="' + c + '" onclick="filterPrompts(\'' + c + '\')">' + c + '</span>'
        for c in PROMPT_CATEGORIES
    )
    hero = ('<section class="prompt-hero"><h2>AI 提示词社区</h2>'
            '<p>20 个精选 AI 提示词模板，覆盖内容创作、开发、教育、效率工具等场景。'
            '点击卡片查看完整提示词，支持一键复制。</p></section>')
    grid = '<div class="prompt-grid">'
    details = ""
    for p in PROMPTS:
        views = format(p['views'], ',')
        grid += ('<div class="prompt-card" data-cat="' + p['category'] + '" onclick="openPromptModal(\'' + p['id'] + '\')">'
                 '<div class="top"><div class="ava">' + p['ico'] + '</div>'
                 '<div class="tit"><h3>' + p['title'] + '</h3>'
                 '<div class="badges"><span class="badge-cat">' + p['category'] + '</span></div></div></div>'
                 '<p class="desc">' + p['desc'] + '</p>'
                 '<div class="ex">示例：' + p['example'] + '</div>'
                 '<div class="foot"><span>' + p['author'] + '</span><span class="views">👁 ' + views + '</span></div></div>')
        prompt_text = "【角色设定】\n" + p['desc'] + "\n\n【示例指令】\n" + p['example']
        details += ('<div id="promptContent-' + p['id'] + '" style="display:none">'
                    '<div class="prompt-modal-head">'
                    '<div class="ava">' + p['ico'] + '</div>'
                    '<div class="tit"><h2>' + p['title'] + '</h2>'
                    '<div class="badges"><span class="badge-cat">' + p['category'] + '</span>'
                    '<span class="badge-cat">' + p['author'] + '</span></div></div></div>'
                    '<div class="prompt-modal-body">'
                    '<div class="prompt-modal-sec"><div class="sec-title"><span class="sec-ico">①</span>角色设定</div><p>' + p['desc'] + '</p></div>'
                    '<div class="prompt-modal-sec"><div class="sec-title"><span class="sec-ico">②</span>示例指令</div><div class="example">' + p['example'] + '</div></div>'
                    '<div class="prompt-modal-sec"><div class="sec-title"><span class="sec-ico">③</span>完整提示词（可复制）</div>'
                    '<div class="prompt-box"><pre id="promptText-' + p['id'] + '">' + prompt_text + '</pre>'
                    '<button class="copy-btn" onclick="copyPrompt(\'' + p['id'] + '\',this)">一键复制</button></div></div>'
                    '</div></div>')
    grid += '</div>'
    modal = ('<div class="prompt-modal" id="promptModal" onclick="if(event.target===this)closePromptModal()">'
             '<div class="prompt-modal-box" onclick="event.stopPropagation()">'
             '<button class="prompt-modal-close" onclick="closePromptModal()">×</button>'
             '<div id="promptModalInner"></div></div></div>')
    return ('<section class="section prompt-section">' + hero
            + '<div class="prompt-search"><span class="search-icon">🔍</span>'
            + '<input type="text" id="promptSearchInput" placeholder="搜索提示词标题、内容或标签..." oninput="searchPrompts(this.value)"></div>'
            + '<div class="prompt-cats">' + cats + '</div>'
            + grid + '</section>' + modal + details)


def build_community():
    profile = ('<div class="profile"><div class="ava">田</div><div class="pinfo">'
               '<h2>' + AUTHOR + '</h2><div class="role">腾讯产品商务顾问 · ' + CITY + '</div>'
               '<p>5 年企业用户腾讯产品落地服务经验，专注企业微信与 WorkBuddy 的培训、落地与销售。'
               '这个站点用于把一线实战经验沉淀下来，也方便分享给同事和客户。</p></div></div>')
    cols = [
        ("📞","联系电话","17752848966","可直接拨打或短信沟通。",[]),
        ("📧","企业邮箱",'<a href="mailto:tianwei@qqhn.net">tianwei@qqhn.net</a>',"正式交付与商务沟通。",[]),
        ("💬","企业微信",'<img src="wechat-qr.png" alt="企业微信二维码" style="width:140px;border-radius:8px;margin-top:4px">',"扫码添加，日常协作与通知主阵地。",[]),
    ]
    col_html = '<div class="cols">'
    for ico,title,sub,desc,items in cols:
        col_html += ('<div class="info-card"><div class="ic-ico">' + ico + '</div>'
                     '<h3>' + title + '</h3><p style="color:var(--c-teal);font-weight:500">' + sub + '</p>'
                     '<p>' + desc + '</p><ul>' + "".join('<li>' + x + '</li>' for x in items) + '</ul></div>')
    col_html += '</div>'
    guide = ('<section class="section"><div class="section-head"><h2><span class="bar"></span>交流 & 反馈</h2>'
             '<p>欢迎就内容准确性、案例补全、Skill 共建进行交流。</p></div>'
             '<div class="cols"><div class="info-card"><div class="ic-ico">💡</div><h3>内容共建</h3>'
             '<p>发现错漏或有更好的实战做法，直接在企业微信找我，或提 PR 到本站仓库。</p></div>'
             '<div class="info-card"><div class="ic-ico">🔔</div><h3>更新节奏</h3>'
             '<p>随项目推进持续补充；每月末由月报自动化汇总一次。</p></div>'
             '<div class="info-card"><div class="ic-ico">⚠️</div><h3>数据安全</h3>'
             '<p>客户与业务敏感信息不入库；处理前确认授权范围，不外泄。</p></div></div></section>')
    body = ('<section class="section" style="padding-bottom:24px">' + profile + '</section>'
            + '<section class="section" style="padding-top:0"><div class="section-head">'
            '<h2><span class="bar"></span>联系方式</h2><p>以下为公开可联系的渠道</p></div>' + col_html + '</section>'
            + guide)
    html = wrap_page("交流", body, active="交流")
    with open("community.html","w",encoding="utf-8") as f: f.write(html)
    print("生成: community.html")

def wrap_page(title, body, active="首页"):
    return ('<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<meta name="description" content="' + SITE_DESC + '">'
            '<title>' + title + ' · ' + SITE_TITLE + '</title><style>' + CSS + '</style></head>'
            '<body>' + topbar(active) + body + footer() + '<script>' + JS + '</script></body></html>')

# ============================ 执行 ============================
# ============================ 首页新增板块：新闻热点 / AI 生态专栏 / 实战案例 ============================
def _load_news():
    try:
        with open("content/news.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"updated": "", "tabs": []}

def build_search_section():
    """首页全站搜索框。读 search-index.json 实时 substring 匹配，跳转到对应页/锚点。"""
    return ('<section class="search-section" id="search">'
            '<div class="search-box">'
            '<span class="search-icon">🔍</span>'
            '<input id="global-search" class="search-input" type="search" '
            'placeholder="搜索全站：手册章节、新闻、技能、提示词、工具评测..." autocomplete="off">'
            '<button class="search-clear" onclick="_searchClear()" title="清空">×</button>'
            '<div id="search-results" class="search-results"></div>'
            '</div>'
            '<p class="search-hint">试试搜 <kbd>群机器人</kbd> <kbd>月报</kbd> <kbd>公文排版</kbd> <kbd>Kimi</kbd> <kbd>DeepSeek</kbd></p>'
            '</section>')

def build_news_section():
    data = _load_news()
    tabs = data.get("tabs", [])
    if not tabs:
        return ""
    head = '<div class="news-tabs">'
    panels = ""
    for i, t in enumerate(tabs):
        key = t["key"]; name = t["name"]; ico = t.get("ico", ""); color = t.get("color", "#10B981")
        active = " active" if i == 0 else ""
        head += ('<button class="news-tab' + active + '" data-tab="' + key + '" style="--tc:' + color +
                 '" onclick="switchNews(\'' + key + '\')">' + ico + ' ' + name + '</button>')
        cards = ""
        for it in t.get("items", []):
            cards += ('<a class="news-card" href="' + it["url"] + '" target="_blank" rel="noopener">'
                      '<span class="news-tag" style="background:' + color + '1a;color:' + color + '">' +
                      t.get("tag", name) + '</span>'
                      '<h4>' + it["title"] + '</h4><p>' + it["desc"] + '</p>'
                      '<span class="news-go">阅读原文 →</span></a>')
        panels += ('<div class="news-panel' + active + '" id="news-' + key + '"><div class="news-grid">' +
                   cards + '</div></div>')
    head += '</div>'
    return ('<section class="section news-section" id="news"><div class="section-head"><h2><span class="bar"></span>新闻动态</h2>'
            '<p>实时追踪 WorkBuddy、AI 办公与前沿模型动态 · 更新于 ' + data.get("updated", "") + '</p></div>'
            + head + panels + '</section>')

def build_ecosystem_showcase():
    cards = ""
    for (n, h, ico, c, d) in ECOSYSTEM_SECTIONS:
        cards += ('<a class="eco-card" href="' + h + '" style="--ec:' + c + '">'
                  '<div class="eco-ico" style="background:' + c + '1a;color:' + c + '">' + ico + '</div>'
                  '<h4>' + n + '</h4><p>' + d + '</p><span class="arrow">→</span></a>')
    return ('<section class="section" id="ecosystem"><div class="section-head"><h2><span class="bar"></span>AI 生态专栏</h2>'
            '<p>工具横评、模型选型、行业拆解与真实案例 —— 边测边写，持续更新</p></div>'
            '<div class="eco-grid">' + cards + '</div></section>')

def build_case_showcase():
    cols = [
        ("⚡", "AI 实战案例", "自己跑通的真实项目复盘", "ai-agent-cases.html", C_AGENT,
         "需求拆解 → 工具选型 → 落地步骤 → 复盘"),
        ("📂", "WorkBuddy 案例", "一线任务完整复现", "cases-wb.html", C_WB,
         "月报 / 透视表 / 培训方案 / 发票处理"),
    ]
    html = '<div class="case-grid">'
    for ico, t, desc, h, color, meta in cols:
        html += ('<a class="case-card" href="' + h + '" style="--cc:' + color + '">'
                 '<div class="case-ico" style="background:' + color + '1a;color:' + color + '">' + ico + '</div>'
                 '<h4>' + t + '</h4><p>' + desc + '</p><div class="meta">' + meta + '</div>'
                 '<span class="arrow">→</span></a>')
    html += '</div>'
    return ('<section class="section" id="cases"><div class="section-head"><h2><span class="bar"></span>实战案例展示</h2>'
            '<p>不是 PPT 方案，是真正跑通过的活儿</p></div>' + html + '</section>')

# ============================ AI 生态详情页（框架，内容待老田填充） ============================
# 每个页面：hero + 目录 + 若干 section（含子卡片优劣双栏）+ 横向对比总表 + 结论 + CTA
# subs 格式：(名称, 标签, 描述, [优势], [不足])；优势/不足留空则渲染「待补充」
ECOSYSTEM_PAGE_DATA = {
    "ai-tools": {
        "fname": "ai-tools.html", "color": C_TOOLS, "ico": "🛠",
        "title": "AI 工具评测",
        "tagline": "6 款主流 AI 工具深度横评 —— 从对话写作、图像设计到办公效率，告诉你哪个真的好用、哪个是智商税。",
        "sections": [
            {"id": "method", "icon": "📐", "title": "评测方法论",
             "intro": "先定标准再测工具，避免「凭感觉打分」。",
             "body": '<div class="eco-todo">【待老田补充：评测维度（易用性 / 准确性 / 中文能力 / 价格 / 生态）、打分权重、测试任务清单】</div>'},
            {"id": "chat", "icon": "💬", "title": "对话与写作类",
             "intro": "日常用得最多的品类，重点看中文表达与长文能力。",
             "subs": [("WorkBuddy", "主力", "腾讯出品，本地+云端双形态", [], []),
                      ("Kimi", "长文本", "超长上下文，论文/合同友好", [], []),
                      ("豆包", "免费", "字节系，日常问答够用", [], []),
                      ("文心一言", "百度", "中文知识问答", [], [])]},
            {"id": "image", "icon": "🎨", "title": "图像与设计类",
             "intro": "出图、做图、做海报，谁更稳。",
             "subs": [("即梦", "字节", "中文 prompt 友好", [], []),
                      ("Midjourney", "海外", "质感天花板", [], []),
                      ("Canva AI", "模板", "套模板出图快", [], [])]},
            {"id": "office", "icon": "🏢", "title": "办公与效率类",
             "intro": "和微信 / 文档打通的才真省事。",
             "subs": [("腾讯文档 AI", "协作", "人机双写", [], []),
                      ("飞书", "字节", "All-in-one", [], []),
                      ("Notion AI", "海外", "知识库强", [], [])]},
        ],
        "compare": ('<table class="cmp"><thead><tr><th>工具</th><th>品类</th><th>中文能力</th><th>价格</th><th>一句话</th></tr></thead><tbody>'
                    '<tr><td>WorkBuddy</td><td>综合</td><td>优</td><td>待补充</td><td>本地+云端，商务场景强</td></tr>'
                    '<tr><td>Kimi</td><td>长文本</td><td>优</td><td>待补充</td><td>超长上下文</td></tr>'
                    '<tr><td>即梦</td><td>图像</td><td>优</td><td>待补充</td><td>中文出图首选</td></tr>'
                    '<tr><td>Midjourney</td><td>图像</td><td>中</td><td>待补充</td><td>质感强但英文为主</td></tr>'
                    '<tr><td>腾讯文档 AI</td><td>办公</td><td>优</td><td>待补充</td><td>协作流畅</td></tr>'
                    '<tr><td>Notion AI</td><td>知识库</td><td>中</td><td>待补充</td><td>结构化强</td></tr>'
                    '</tbody></table>'),
        "conclusion": '<div class="eco-todo">【待老田补充：综合结论 + 按人群选型建议（商务顾问 / 学生 / 设计师）】</div>',
    },
    "llm-compare": {
        "fname": "llm-compare.html", "color": C_LLM, "ico": "🧠",
        "title": "大模型横评",
        "tagline": "跑分、定价与选型指南 —— 把国内外主流大模型拉到同一张桌子上比，帮你在「够用」和「省钱」之间做对选择。",
        "sections": [
            {"id": "dims", "icon": "📏", "title": "评测维度",
             "intro": "看什么，决定了你信什么。",
             "body": '<div class="eco-todo">【待老田补充：评测维度（综合跑分 / 价格 / 上下文长度 / 中文能力 / 工具调用 / 速度）与数据来源】</div>'},
            {"id": "oversea", "icon": "🌐", "title": "国际厂商",
             "intro": "旗舰密集发布的七月，几家都交了新卷。",
             "subs": [("GPT-5.6", "OpenAI", "综合能力标杆", [], []),
                      ("Claude Opus 5", "Anthropic", "长文与代码强", [], []),
                      ("Gemini 3.6 Flash", "Google", "速度与多模态", [], [])]},
            {"id": "domestic", "icon": "🇨🇳", "title": "国内厂商",
             "intro": "国产阵营今年明显提速，性价比是杀手锏。",
             "subs": [("DeepSeek V4", "深度求索", "开源 + 低价", [], []),
                      ("Qwen3.8", "阿里", "生态完整", [], []),
                      ("Kimi K3", "月之暗面", "超长上下文", [], []),
                      ("智谱 GLM", "智谱", "政务/企业友好", [], [])]},
        ],
        "compare": ('<table class="cmp"><thead><tr><th>模型</th><th>厂商</th><th>上下文</th><th>输入价(每M tok)</th><th>亮点</th></tr></thead><tbody>'
                    '<tr><td>GPT-5.6</td><td>OpenAI</td><td>待补充</td><td>待补充</td><td>综合最强</td></tr>'
                    '<tr><td>Claude Opus 5</td><td>Anthropic</td><td>待补充</td><td>待补充</td><td>长文/代码</td></tr>'
                    '<tr><td>Gemini 3.6 Flash</td><td>Google</td><td>待补充</td><td>待补充</td><td>速度/多模态</td></tr>'
                    '<tr><td>DeepSeek V4</td><td>深度求索</td><td>待补充</td><td>待补充</td><td>开源低价</td></tr>'
                    '<tr><td>Qwen3.8</td><td>阿里</td><td>待补充</td><td>待补充</td><td>生态全</td></tr>'
                    '<tr><td>Kimi K3</td><td>月之暗面</td><td>待补充</td><td>待补充</td><td>超长上下文</td></tr>'
                    '</tbody></table>'),
        "conclusion": '<div class="eco-todo">【待老田补充：选型指南（按预算 / 场景 / 合规要求推荐）】</div>',
    },
    "ai-industry": {
        "fname": "ai-industry.html", "color": C_INDUSTRY, "ico": "🏭",
        "title": "行业落地拆解",
        "tagline": "AI 在 6 大行业怎么落地 —— 不谈概念，只拆真实场景、数据闭环与 ROI，让「能不能用」变成「怎么用」。",
        "sections": [
            {"id": "method", "icon": "🔧", "title": "落地方法论",
             "intro": "别从「上 AI」开始，从「痛点」开始。",
             "body": '<div class="eco-todo">【待老田补充：落地四步（找场景 / 接数据 / 定指标 / 跑闭环）+ ROI 测算模板】</div>'},
            {"id": "mfg", "icon": "🏭", "title": "制造业", "intro": "质检、排产、设备运维是高频场景。",
             "body": '<div class="eco-todo">【待老田补充：典型场景 + 案例 + 工具组合】</div>'},
            {"id": "retail", "icon": "🛒", "title": "零售", "intro": "导购、客服、选品是 AI 最先啃下的骨头。",
             "body": '<div class="eco-todo">【待老田补充：典型场景 + 案例 + 工具组合】</div>'},
            {"id": "trade", "icon": "🌏", "title": "外贸", "intro": "多语言客服与邮件是刚需。",
             "body": '<div class="eco-todo">【待老田补充：典型场景 + 案例 + 工具组合】</div>'},
            {"id": "edu", "icon": "🎓", "title": "教育", "intro": "个性化辅导与批改提效明显。",
             "body": '<div class="eco-todo">【待老田补充：典型场景 + 案例 + 工具组合】</div>'},
            {"id": "medical", "icon": "🏥", "title": "医疗", "intro": "合规是前提，辅助诊断与文书是切口。",
             "body": '<div class="eco-todo">【待老田补充：典型场景 + 案例 + 工具组合】</div>'},
            {"id": "finance", "icon": "💰", "title": "金融", "intro": "风控、研报、投顾是重点场景。",
             "body": '<div class="eco-todo">【待老田补充：典型场景 + 案例 + 工具组合】</div>'},
        ],
        "compare": ('<table class="cmp"><thead><tr><th>行业</th><th>首选场景</th><th>关键数据</th><th>合规要点</th></tr></thead><tbody>'
                    '<tr><td>制造业</td><td>质检/排产</td><td>待补充</td><td>待补充</td></tr>'
                    '<tr><td>零售</td><td>导购/客服</td><td>待补充</td><td>待补充</td></tr>'
                    '<tr><td>外贸</td><td>多语言客服</td><td>待补充</td><td>待补充</td></tr>'
                    '<tr><td>教育</td><td>个性辅导</td><td>待补充</td><td>待补充</td></tr>'
                    '<tr><td>医疗</td><td>辅助诊断</td><td>待补充</td><td>待补充</td></tr>'
                    '<tr><td>金融</td><td>风控/研报</td><td>待补充</td><td>待补充</td></tr>'
                    '</tbody></table>'),
        "conclusion": '<div class="eco-todo">【待老田补充：跨行业共性结论 + 落地避坑清单】</div>',
    },
    "ai-agent-cases": {
        "fname": "ai-agent-cases.html", "color": C_AGENT, "ico": "⚡",
        "title": "AI 案例",
        "tagline": "自己跑通的真实项目复盘 —— 每个案例都拆到「需求 → 选型 → 步骤 → 复盘」，能抄作业的程度。",
        "sections": [
            {"id": "tpl", "icon": "📋", "title": "案例模板说明",
             "intro": "统一格式，方便你对照自己的业务抄。",
             "body": '<div class="eco-todo">【待老田补充：每个案例固定结构说明（背景 / 目标 / 工具 / 步骤 / 成本 / 复盘）】</div>'},
            {"id": "case1", "icon": "①", "title": "案例一（待命名）",
             "intro": "一句话说清这个案例解决什么问题。",
             "body": '<div class="eco-todo">【待老田补充：案例一正文】</div>'},
            {"id": "case2", "icon": "②", "title": "案例二（待命名）",
             "intro": "一句话说清这个案例解决什么问题。",
             "body": '<div class="eco-todo">【待老田补充：案例二正文】</div>'},
            {"id": "case3", "icon": "③", "title": "案例三（待命名）",
             "intro": "一句话说清这个案例解决什么问题。",
             "body": '<div class="eco-todo">【待老田补充：案例三正文】</div>'},
            {"id": "review", "icon": "🔁", "title": "复盘方法论",
             "intro": "踩过的坑，才是真资产。",
             "body": '<div class="eco-todo">【待老田补充：通用复盘框架（哪些该做 / 哪些别做）】</div>'},
        ],
        "compare": ('<table class="cmp"><thead><tr><th>案例</th><th>领域</th><th>核心工具</th><th>耗时</th><th>效果</th></tr></thead><tbody>'
                    '<tr><td>案例一</td><td>待补充</td><td>待补充</td><td>待补充</td><td>待补充</td></tr>'
                    '<tr><td>案例二</td><td>待补充</td><td>待补充</td><td>待补充</td><td>待补充</td></tr>'
                    '<tr><td>案例三</td><td>待补充</td><td>待补充</td><td>待补充</td><td>待补充</td></tr>'
                    '</tbody></table>'),
        "conclusion": '<div class="eco-todo">【待老田补充：案例共性结论 + 什么业务适合用 AI 跑】</div>',
    },
}

# ---------- 全站搜索索引 ----------
# 构建期遍历所有数据源，生成 content/search-index.json，前端 fetch 后 substring 匹配。
# 只索引「标题 + 一句话简介」，点击直达对应页/锚点，不扫正文（避免噪声+索引过大）。
import re as _re
_HTML_TAG = _re.compile(r'<[^>]+>')
_WS = _re.compile(r'\s+')
def _strip_html(html, limit=80):
    """去 HTML 标签，合并空白，取前 limit 字符作为 snippet。"""
    if not html:
        return ""
    t = _HTML_TAG.sub(' ', html)
    t = _WS.sub(' ', t).strip()
    return t[:limit]

def _search_chapters(items, chapters, fname, cat_label, ico, page_color=""):
    """把 [chapter_tuple, ...] 格式的章节列表追加进 items。
    chapter_tuple: (id, num, title, cat, html)
    """
    for (cid, num, title, cat, html) in chapters:
        # snippet 优先用标题后的正文第一段；若 html 是字符串直接 strip
        snippet = _strip_html(html, 80)
        if not snippet:
            snippet = title
        items.append({"t": title, "s": snippet, "c": cat_label,
                      "u": fname + "#" + cid, "ico": ico, "color": page_color})

def _build_search_index():
    items = []
    # 1) WB 手册 11 章（从 wb_manual.json）
    _search_chapters(items, MANUAL_WB, "manual-wb.html", "WB手册", "📘", C_WB)
    # 2) WB 案例
    _search_chapters(items, CASES_WB, "cases-wb.html", "WB案例", "📂", C_WB)
    # 3) 进阶篇
    _search_chapters(items, ADVANCED, "advanced.html", "进阶篇", "🚀", C_WB)
    # 4) 岗位与行业落地
    _search_chapters(items, INDUSTRY, "industry.html", "岗位落地", "🎯", C_INDUSTRY)
    # 5) 新闻动态（外链，每条新闻独立条目）
    try:
        nd = _load_news()
        for tab in nd.get("tabs", []):
            cat_label = "新闻·" + tab["name"]
            for it in tab.get("items", []):
                items.append({"t": it["title"], "s": it["desc"][:80],
                              "c": cat_label, "u": it["url"], "ico": tab.get("ico", "📰"),
                              "color": tab.get("color", "")})
    except Exception:
        pass
    # 6) Skills（每个技能）
    for sk in SKILLS:
        snippet = _strip_html(sk.get("overview", "") or sk.get("desc", ""), 80)
        items.append({"t": sk["title"], "s": snippet, "c": "Skills",
                      "u": "skills.html#skill-" + sk["id"], "ico": sk.get("ico", "🧩"),
                      "color": "#A855F7"})
    # 7) 提示词
    for p in PROMPTS:
        snippet = _strip_html(p.get("example", "") or p.get("desc", ""), 80)
        items.append({"t": p["title"], "s": snippet, "c": "提示词·" + p["category"],
                      "u": "skills.html#prompt-" + p["id"], "ico": p.get("ico", "✨"),
                      "color": "#A855F7"})
    # 8) AI 生态 4 个独立页（每个 section + subs 工具/模型名）
    for key, pg in ECOSYSTEM_PAGE_DATA.items():
        for sec in pg.get("sections", []):
            items.append({"t": sec["title"], "s": _strip_html(sec.get("intro", ""), 80),
                          "c": pg["title"], "u": pg["fname"] + "#" + sec["id"],
                          "ico": sec.get("icon", pg.get("ico", "📄")),
                          "color": pg.get("color", "")})
            for sub in sec.get("subs", []):
                # sub: (name, badge, desc, [], [])
                sname, sbadge, sdesc = sub[0], sub[1], sub[2] if len(sub) > 2 else ""
                if not sname:
                    continue
                items.append({"t": sname + " · " + sbadge, "s": _strip_html(sdesc, 60),
                              "c": pg["title"], "u": pg["fname"] + "#" + sec["id"],
                              "ico": sec.get("icon", pg.get("ico", "📄")),
                              "color": pg.get("color", "")})
    # 去重（同标题+同 URL 保留第一个）
    seen = set()
    dedup = []
    for it in items:
        k = (it["t"], it["u"])
        if k in seen:
            continue
        seen.add(k)
        dedup.append(it)
    # 写出
    import datetime as _dt
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "content")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "search-index.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"updated": _dt.date.today().isoformat(),
                   "count": len(dedup),
                   "items": dedup}, f, ensure_ascii=False, separators=(",", ":"))
    return out_path, len(dedup)

def eco_subcards(subs):
    if not subs:
        return ""
    h = '<div class="eco-subgrid">'
    for name, tag, desc, pros, cons in subs:
        pros_li = "".join("<li>" + x + "</li>" for x in pros) or '<li style="color:#B45309">待补充</li>'
        cons_li = "".join("<li>" + x + "</li>" for x in cons) or '<li style="color:#B45309">待补充</li>'
        h += ('<div class="eco-subcard"><div class="eco-subhead"><h4>' + name + '</h4>'
              '<span class="eco-tag">' + tag + '</span></div>'
              '<p>' + desc + '</p>'
              '<div class="pc"><div class="pc-col pro"><span class="pc-h">✓ 优势</span><ul>' + pros_li + '</ul></div>'
              '<div class="pc-col con"><span class="pc-h">✗ 不足</span><ul>' + cons_li + '</ul></div></div></div>')
    h += '</div>'
    return h

def build_ecosystem_page(key):
    d = ECOSYSTEM_PAGE_DATA[key]
    color, ico, title, tagline = d["color"], d["ico"], d["title"], d["tagline"]
    toc = '<nav class="eco-toc">'
    for s in d["sections"]:
        toc += '<a href="#' + s["id"] + '">' + s["icon"] + ' ' + s["title"] + '</a>'
    toc += '<a href="#compare">📊 横向对比</a><a href="#conclusion">✅ 结论</a></nav>'
    main = ""
    for s in d["sections"]:
        inner = s.get("body", "") + (eco_subcards(s.get("subs")) if s.get("subs") else "")
        main += ('<section class="eco-section" id="' + s["id"] + '">'
                 '<div class="eco-section-head"><span class="si">' + s["icon"] + '</span><h2>' + s["title"] + '</h2></div>'
                 '<p class="intro">' + s["intro"] + '</p>' + inner + '</section>')
    compare = ('<section class="eco-section" id="compare"><div class="eco-section-head">'
               '<span class="si">📊</span><h2>横向对比总表</h2></div>' + d["compare"] + '</section>')
    conclusion = ('<section class="eco-section" id="conclusion"><div class="eco-section-head">'
                  '<span class="si">✅</span><h2>结论与建议</h2></div>'
                  '<div class="eco-conclusion">' + d["conclusion"] + '</div></section>')
    cta = ('<div class="eco-cta"><h3>看完想试试？+ 老田的一线经验</h3>'
           '<a href="index.html">回到首页</a><a class="ghost" href="community.html">和我交流</a></div>')
    hero = ('<section class="eco-hero"><span class="eco-badge" style="background:' + color + '1a;color:' + color + '">'
            + ico + ' ' + title + '</span><h1>' + title + '</h1><p>' + tagline + '</p></section>')
    body = hero + '<div class="eco-layout">' + toc + '<div class="eco-main">' + main + compare + conclusion + cta + '</div></div>'
    html = wrap_page(title, body, active="AI生态专栏")
    with open(d["fname"], "w", encoding="utf-8") as f:
        f.write(html)
    print("生成:", d["fname"])

if __name__ == "__main__":
    _idx_path, _idx_n = _build_search_index()
    print("搜索索引:", _idx_path, "(" + str(_idx_n) + " 条)")
    build_index()
    build_reader("WB手册", "WorkBuddy 使用手册", MANUAL_WB, "manual-wb.html", C_WB, topbar_active="笔记类别")
    build_reader("WB案例", "WorkBuddy 案例", CASES_WB, "cases-wb.html", C_WB, topbar_active="笔记类别")
    build_doc("进阶篇","进阶篇","从案例到系统，构建你的工作流",ADVANCED,"advanced.html",C_WB, topbar_active="笔记类别")
    build_doc("岗位与行业落地","岗位与行业落地","按岗位 / 行业视角组织实战内容",INDUSTRY,"industry.html",C_INDUSTRY, topbar_active="笔记类别")
    build_skills()
    build_community()
    build_ecosystem_page("ai-tools")
    build_ecosystem_page("llm-compare")
    build_ecosystem_page("ai-industry")
    build_ecosystem_page("ai-agent-cases")
    print("全部页面生成完成。")
