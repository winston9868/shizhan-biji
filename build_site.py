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

# ---------- WorkBuddy 使用手册（复刻自「小饭的 AI 实战笔记」使用手册，共 10 章） ----------
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
    # 使用手册（WB手册 1-10 章）
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
    # 案例篇（WB案例）
    ("案例篇","01","第 1 章 从整理桌面文件这些小事做起","桌面发票扫描与台账生成","cases-wb.html#chapter-1"),
    ("案例篇","02","第 2 章 办公三件套：Word、Excel、PPT","三件套联动实战","cases-wb.html#chapter-2"),
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
        ("📘","WB手册","从 0 到 1，用好 WorkBuddy","📝 10 篇文章","manual-wb.html",C_WB),
        ("📂","WB案例","真实任务的完整复现","📝 2 篇文章","cases-wb.html",C_WB),
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
    # 1) WB 手册 10 章（从 wb_manual.json）
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
