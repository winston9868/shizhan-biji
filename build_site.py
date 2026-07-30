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

# 顶部导航栏目（name, href, icon, 产品色, 产品分组）
SECTIONS = [
    ("首页",   "index.html",              "🏠", "",         ""),
    ("笔记",   "index.html#notebooks",    "📝", "#10B981",  ""),
    ("进阶篇", "advanced.html",           "🚀", "#10B981", "WorkBuddy"),
    ("岗位与行业落地", "industry.html",   "🎯", "#0EA5E9", ""),
    ("Skills", "skills.html",             "🧩", "#A855F7", ""),
    ("交流",   "community.html",          "💬", "#64748B", ""),
]

# 产品色板
C_WECOM = "#07C160"   # 企业微信绿
C_WB    = "#10B981"   # WorkBuddy 翡翠绿
C_WECOM_SOFT = "rgba(7,192,96,.12)"
C_WB_SOFT    = "rgba(16,185,129,.12)"
C_INDUSTRY   = "#0EA5E9"  # 岗位与行业落地（天蓝）

# 笔记类别（首页卡片与下拉菜单共用）
NOTEBOOK_SECTIONS = [
    ("企微手册", "manual-wecom.html", "📘", C_WECOM, "企业微信账号、客户联系与协作"),
    ("企微案例", "cases-wecom.html",  "📂", C_WECOM, "真实企微场景的落地打法"),
    ("WB手册",  "manual-wb.html",    "📘", C_WB,    "从 0 到 1，把 WorkBuddy 用起来"),
    ("WB案例",  "cases-wb.html",     "📂", C_WB,    "真实任务的完整复现"),
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
  --sidebar-w:240px; --toc-w:210px; --reading-w:760px; --topbar-h:56px;
  --font-serif:Georgia,'Noto Serif SC','Songti SC',serif;
  --font-sans:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;
  --font-mono:'JetBrains Mono','Fira Code',Consolas,monospace;
  --radius-sm:8px; --radius-md:12px; --radius-lg:16px; --radius-xl:20px;
}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--text-primary);font-family:var(--font-sans);
  font-size:14px;line-height:1.85;-webkit-font-smoothing:antialiased}
a{color:var(--c-teal);text-decoration:none;transition:color .2s}
a:hover{color:#047857}
img{max-width:100%;height:auto}

/* ===== Top Nav ===== */
.topbar{position:fixed;top:0;left:0;right:0;height:var(--topbar-h);
  background:rgba(255,255,255,.85);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);
  border-bottom:1px solid var(--border);z-index:100;display:flex;align-items:center;padding:0 24px}
.topbar-inner{max-width:1320px;margin:0 auto;width:100%;display:flex;align-items:center;
  justify-content:space-between;gap:16px}
.blog-logo{display:flex;align-items:center;gap:8px;font-family:var(--font-serif);font-size:16px;
  font-weight:500;color:var(--text-primary);text-decoration:none;white-space:nowrap}
.blog-logo:hover{color:var(--c-teal)}
.blog-logo-icon{width:30px;height:30px;background:linear-gradient(135deg,#4DEE9E,#D6E807);
  border-radius:var(--radius-sm);display:flex;align-items:center;justify-content:center;
  color:#fff;font-size:12px;font-weight:700;letter-spacing:.5px;font-family:var(--font-sans);
  box-shadow:0 2px 8px rgba(16,185,129,.3)}
.topbar-nav{display:flex;align-items:center;gap:2px;flex-wrap:wrap;justify-content:flex-end}
.topbar-nav a{padding:6px 11px;border-radius:var(--radius-xl);font-size:13px;
  color:var(--text-secondary);text-decoration:none;transition:all .2s;display:inline-flex;align-items:center}
.topbar-nav a:hover{background:var(--bg-soft);color:var(--text-primary)}
.topbar-nav a.active{background:var(--accent-soft);color:var(--accent);font-weight:600}
.nav-dot{width:7px;height:7px;border-radius:50%;display:inline-block;margin-right:6px;flex-shrink:0}
.topbar-nav a .nav-ico{margin-right:4px}
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

/* ===== Hero (home) ===== */
.hero{margin-top:var(--topbar-h);padding:72px 24px 56px;
  background:var(--bg-hero);border-bottom:1px solid var(--border);text-align:center}
.hero-name{font-family:var(--font-serif);font-size:40px;font-weight:700;letter-spacing:.5px;
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
.card{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius-lg);
  padding:24px;box-shadow:var(--shadow-sm);transition:all .25s;position:relative;overflow:hidden}
.card:hover{transform:translateY(-4px);box-shadow:var(--shadow-hover);
  border-color:var(--border-hover)}
.card-ico{width:46px;height:46px;border-radius:var(--radius-md);display:flex;align-items:center;
  justify-content:center;font-size:22px;margin-bottom:14px}
.card h3{font-size:17px;font-weight:600;margin-bottom:8px}
.card p{color:var(--text-secondary);font-size:13.5px;line-height:1.8}
.card .meta{margin-top:14px;font-size:12px;color:var(--text-tertiary)}
.card .arrow{position:absolute;right:20px;bottom:18px;font-size:18px;color:var(--text-tertiary);
  transition:transform .25s,color .25s}
.card:hover .arrow{transform:translateX(4px);color:var(--c-teal)}

/* ===== Filter pills (home articles) ===== */
.filter-pills{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:24px}
.filter-pill{padding:7px 18px;border:1px solid var(--border);border-radius:var(--radius-xl);
  background:var(--bg-card);color:var(--text-secondary);font-size:13px;cursor:pointer;transition:all .2s}
.filter-pill:hover{border-color:var(--border-hover);color:var(--c-teal)}
.filter-pill.active{background:linear-gradient(120deg,#10B981,#84CC16);color:#fff;border-color:transparent;font-weight:600}

/* ===== Article list ===== */
.article-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:16px}
.article-card{display:flex;gap:14px;background:var(--bg-card);border:1px solid var(--border);
  border-radius:var(--radius-md);padding:18px;box-shadow:var(--shadow-sm);transition:all .22s}
.article-card:hover{transform:translateY(-3px);box-shadow:var(--shadow-md);border-color:var(--border-hover)}
.article-badge{flex-shrink:0;width:54px;height:54px;border-radius:var(--radius-sm);
  display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff;font-weight:600}
.article-badge .ch{font-size:11px;opacity:.85}
.article-badge .num{font-size:18px;line-height:1}
.article-card .body h4{font-size:15px;font-weight:600;margin-bottom:5px}
.article-card .body p{font-size:12.5px;color:var(--text-secondary);line-height:1.7;
  display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.article-card .tag{display:inline-block;margin-top:8px;font-size:11px;padding:2px 10px;
  border-radius:var(--radius-xl);background:var(--bg-soft);color:var(--text-tertiary)}

/* ===== Doc layout (manual/cases/advanced) ===== */
.layout{max-width:1280px;margin:0 auto;padding:calc(var(--topbar-h) + 28px) 24px 80px;
  display:grid;grid-template-columns:var(--sidebar-w) minmax(0,1fr) var(--toc-w);gap:34px}
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
.sidebar-part.expanded .sidebar-chapters,.sidebar-part.active .sidebar-chapters{max-height:1000px}
.sidebar-chapter{display:block;padding:6px 10px 6px 27px;font-size:13px;color:var(--text-secondary);
  border-radius:var(--radius-sm);transition:all .18s;border-left:2px solid transparent}
.sidebar-chapter:hover{background:var(--bg-soft);color:var(--text-primary)}
.sidebar-chapter.active{color:var(--accent);border-left-color:var(--accent);background:var(--accent-soft);font-weight:500}

.reading-section{min-width:0}
.reading-page{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius-lg);
  padding:36px 44px;box-shadow:var(--shadow-sm)}
.reading-page>.page-title{font-family:var(--font-serif);font-size:28px;font-weight:700;margin-bottom:6px}
.reading-page>.page-sub{color:var(--text-tertiary);font-size:13.5px;margin-bottom:28px;
  padding-bottom:20px;border-bottom:1px solid var(--border)}
.chapter{scroll-margin-top:calc(var(--topbar-h) + 24px);margin-bottom:42px}
.chapter-header{display:flex;align-items:center;gap:12px;margin-bottom:14px}
.chapter-badge{font-size:12px;font-weight:600;padding:3px 11px;border-radius:var(--radius-xl);
  background:var(--accent-soft);color:var(--accent);white-space:nowrap}
.chapter-title{font-size:20px;font-weight:700}
.chapter-body{color:var(--text-primary);font-size:14.5px;line-height:1.95}
.chapter-body h3{font-size:16px;font-weight:600;margin:22px 0 10px}
.chapter-body p{margin:12px 0;color:var(--text-secondary)}
.chapter-body ul,.chapter-body ol{margin:12px 0;padding-left:22px;color:var(--text-secondary)}
.chapter-body li{margin:6px 0}
.chapter-body strong{color:var(--text-primary)}
.chapter-body :not(pre) > code{font-family:var(--font-mono);font-size:13px;background:var(--bg-soft);
  padding:2px 6px;border-radius:5px;color:#047857}
.callout{margin:16px 0;padding:14px 16px;border-radius:var(--radius-md);font-size:13.5px;line-height:1.8;
  border-left:4px solid var(--c-teal);background:rgba(16,185,129,.07)}
.callout.warn{border-left-color:var(--c-coral);background:rgba(245,158,11,.08)}
.callout.info{border-left-color:var(--c-blue);background:rgba(6,182,212,.08)}
.callout .ttl{font-weight:600;display:block;margin-bottom:4px}
pre{margin:16px 0;background:#1E293B;color:#E2E8F0;border:1px solid var(--border);border-radius:var(--radius-md);padding:16px 18px;
  overflow-x:auto;font-size:13px;line-height:1.7}
pre code{font-family:var(--font-mono);color:inherit;background:none;padding:0}
table{width:100%;border-collapse:collapse;margin:18px 0;font-size:13.5px}
th,td{border:1px solid var(--border);padding:10px 12px;text-align:left}
th{background:var(--bg-soft);font-weight:600;color:var(--text-primary)}
td{color:var(--text-secondary)}
.chapter-body h2{font-size:18px;font-weight:700;margin:26px 0 12px;padding-bottom:8px;
  border-bottom:1px solid var(--border);color:var(--text-primary)}
.chapter-body img{max-width:100%;height:auto;display:block;margin:16px auto;
  border-radius:var(--radius-md);border:1px solid var(--border);background:var(--bg-soft)}
.chapter-body figure{margin:16px 0;padding:12px 14px;border:1px solid var(--border);
  border-radius:var(--radius-md);background:var(--bg-soft)}
.chapter-body figure pre{margin:0}
.img-missing{margin:16px auto;padding:18px;text-align:center;font-size:13px;color:var(--text-tertiary);
  border:1px dashed var(--border);border-radius:var(--radius-md);background:var(--bg-soft)}


/* ===== TOC (right) ===== */
.toc{position:sticky;top:calc(var(--topbar-h) + 24px);align-self:start;font-size:13px}
.toc-title{font-size:12px;font-weight:600;color:var(--text-tertiary);text-transform:uppercase;
  letter-spacing:1px;margin-bottom:12px}
.toc-heading{display:block;padding:5px 0 5px 12px;border-left:2px solid var(--border);
  color:var(--text-secondary);transition:all .18s;cursor:pointer}
.toc-heading:hover{color:var(--text-primary)}
.toc-heading.active{color:var(--accent);border-left-color:var(--accent);font-weight:500}
.toc-heading.level-3{padding-left:26px;font-size:12.5px;color:var(--text-tertiary)}
.toc-progress{margin-top:22px;padding-top:16px;border-top:1px solid var(--border)}
.toc-progress-bar{height:5px;background:var(--bg-soft);border-radius:4px;overflow:hidden}
.toc-progress-fill{height:100%;width:0;background:var(--accent-grad);transition:width .15s}
.toc-progress-label{font-size:11px;color:var(--text-tertiary);margin-top:6px}
.toc-back-top{margin-top:16px;font-size:12px;color:var(--text-tertiary);cursor:pointer;display:inline-block}
.toc-back-top:hover{color:var(--accent)}

/* ===== Skills page ===== */
.skill-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:20px}
.skill-card{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius-lg);
  padding:22px;box-shadow:var(--shadow-sm);transition:all .25s;display:flex;flex-direction:column}
.skill-card:hover{transform:translateY(-4px);box-shadow:var(--shadow-lg);border-color:var(--border-hover)}
.skill-top{display:flex;align-items:center;gap:12px;margin-bottom:12px}
.skill-ava{width:44px;height:44px;border-radius:var(--radius-md);display:flex;align-items:center;
  justify-content:center;font-size:22px;background:linear-gradient(135deg,#4DEE9E,#D6E807);color:#fff;flex-shrink:0}
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
.profile .ava{width:84px;height:84px;border-radius:50%;background:linear-gradient(135deg,#4DEE9E,#D6E807);
  display:flex;align-items:center;justify-content:center;color:#fff;font-size:30px;font-weight:600;flex-shrink:0}
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
.skills-hero h1{font-family:var(--font-serif);font-size:40px;font-weight:700;
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
  justify-content:center;font-size:26px;background:linear-gradient(135deg,#4DEE9E,#D6E807);color:#fff;flex-shrink:0}
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
  justify-content:center;font-size:32px;background:linear-gradient(135deg,#4DEE9E,#D6E807);color:#fff;flex-shrink:0}
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

/* ===== Responsive ===== */
@media(max-width:1100px){.layout{grid-template-columns:var(--sidebar-w) minmax(0,1fr)}
  .toc{display:none}}
@media(max-width:768px){.topbar-nav{display:none}.menu-btn{display:block}
  .layout{grid-template-columns:1fr;padding-left:16px;padding-right:16px}
  .sidebar{position:static;max-height:none;display:none}
  .sidebar.open{display:block}
  .reading-page{padding:24px 18px}
  .hero-name{font-size:30px}.section{padding:40px 16px}}
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
// 阅读进度 + TOC 高亮（仅文档页）
(function(){
  var fill=document.getElementById('tocFill');
  var sec=document.querySelector('.reading-section');
  var headings=Array.prototype.slice.call(document.querySelectorAll('.toc-heading'));
  var chapters=Array.prototype.slice.call(document.querySelectorAll('.chapter'));
  if(!sec) return;
  function onScroll(){
    var h=sec.scrollHeight-window.innerHeight;
    var p=h>0?Math.min(100,Math.max(0,window.scrollY/h*100)):0;
    if(fill) fill.style.width=p+'%';
  }
  window.addEventListener('scroll',onScroll,{passive:true}); onScroll();
  if('IntersectionObserver' in window && chapters.length){
    var obs=new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if(e.isIntersecting){
          var id=e.target.id;
          headings.forEach(function(h){h.classList.toggle('active',h.getAttribute('href')==='#'+id);});
          document.querySelectorAll('.sidebar-chapter').forEach(function(c){
            c.classList.toggle('active',c.getAttribute('href')==='#'+id);});
        }
      });
    },{rootMargin:'-20% 0px -70% 0px'});
    chapters.forEach(function(c){if(c.id) obs.observe(c);});
  }
})();
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
"""

# ============================ 公共片段 ============================
def hex_rgba(h, a):
    h = h.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return 'rgba(%d,%d,%d,%.2f)' % (r, g, b, a)

def topbar(active):
    navs = ""
    for (name, href, ico, color, grp) in SECTIONS:
        dot = '<span class="nav-dot" style="background:%s"></span>' % color if color else ''
        cls = "active" if name == active else ""
        navs += ('<a class="' + cls + '" href="' + href + '">' + dot +
                 '<span class="nav-ico">' + ico + '</span>' + name + '</a>')
    return ('<header class="topbar"><div class="topbar-inner">'
            '<a class="blog-logo" href="index.html">'
            '<span class="blog-logo-icon">TW</span>老田的 AI 实战笔记</a>'
            '<button class="menu-btn" onclick="toggleMenu()">☰</button>'
            '<nav class="topbar-nav">' + navs + '</nav></div></header>')

def footer():
    links = ('<a href="index.html">首页</a>'
             '<a href="manual-wecom.html">企微手册</a><a href="manual-wb.html">WB手册</a>'
             '<a href="cases-wecom.html">企微案例</a><a href="cases-wb.html">WB案例</a>'
             '<a href="advanced.html">进阶篇</a>'
             '<a href="industry.html">岗位与行业落地</a>'
             '<a href="skills.html">Skills</a><a href="community.html">交流</a>')
    return ('<footer class="footer"><div class="footer-inner">'
            '<span>© ' + str(__import__('datetime').datetime.now().year) + ' ' + AUTHOR + ' · ' + CITY + ' · 用 WorkBuddy 沉淀</span>'
            '<div class="links">' + links + '</div></div></footer>'
            '<button id="backTop" onclick="goTop()" title="回到顶部">↑</button>')

def article_wrap(product, num, title, desc, href, color, tag):
    return ('<div class="article-card-wrap" data-part="' + product + '">'
            '<a class="article-card" href="' + href + '">'
            '<div class="article-badge" style="background:' + color + '">'
            '<span class="ch">CH</span><span class="num">' + num + '</span></div>'
            '<div class="body"><h4>' + title + '</h4><p>' + desc + '</p>'
            '<span class="tag">' + tag + '</span></div></a></div>')

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
        elif t == 'code': out += '<pre><code>' + c + '</code></pre>'
        elif t == 'table': out += c
    return out

# ---------- WorkBuddy 使用手册（复刻自「小饭的 AI 实战笔记」使用手册，共 11 章） ----------
def _load_manual_wb():
    _p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wb_manual.json")
    with open(_p, encoding="utf-8") as _f:
        return json.load(_f)["chapters"]
MANUAL_WB = _load_manual_wb()

# ---------- 企业微信使用手册（占位，待补充） ----------
MANUAL_WECOM = [
 ("chapter-w1","01","企业微信产品概览", "企微手册",
  ch_body("企业微信是腾讯面向企业的即时通讯与办公平台，是老田服务客户的主阵地之一。本手册将逐步补充账号体系、通讯录、客户联系等实战内容。",
   [('callout-info','本手册建设中，内容随项目推进持续补充。优先沉淀：客户联系、社群运营、微盘与文档协作三类高频场景。')])),
 ("chapter-w2","02","客户联系与社群运营", "企微手册",
  ch_body("通过「客户联系」添加外部客户、打标签、建客户群，实现精细化运营与转化跟踪。",
   [('h3','落地要点'),
    ('ul',['外部客户加好友与标签分层','客户群公告、群发与 SOP 节奏','从聊天记录提炼需求与痛点']),
    ('callout-warn','客户信息属敏感数据，处理前确认授权范围，勿外泄。')])),
 ("chapter-w3","03","微盘与文档协作", "企微手册",
  ch_body("企业微信微盘与在线文档支持团队知识沉淀与多人协作，是交付物归档与共享的常用载体。",
   [('callout','交付物建议本地 + 乐享知识库双备份，命名结构两端保持一致。')])),
]

# ---------- WorkBuddy 案例 ----------
CASES_WB = [
 ("chapter-11","01","月度工作汇报自动生成", "WB案例",
  ch_body("月底最头疼的事之一：把零散工作汇总成结构化的月报。用 WorkBuddy + 模板，半小时变三分钟。",
   [('h3','做法'),
    ('ul',['维护一份每日日报（YYYY-MM/YYYY-MM-DD.md）','月底运行生成脚本，聚合成月报','自动推送企微群 + 邮件']),
    ('callout','老田已落地：自动化 ID automation-1782695947091，每月最后一天 18:00 触发。')])),
 ("chapter-13","03","培训方案一键成文", "WB案例",
  ch_body("面向企业微信 / WorkBuddy 的客户培训，方案有稳定结构。用公文标准排版 Skill 直接出 Word。",
   [('h3','结构'),
    ('ul',['培训背景与目标','课程大纲与课时','实操演练设计','考核与后续']),
    ('callout-info','排版遵循：大标题方正小标宋、一级标题黑体、正文仿宋、1.5 倍行距（见 tianwei-word-formatter）。')])),
 ("chapter-15","05","销售数据透视分析", "WB案例",
  ch_body("拿到一张杂乱的销售明细，让它快速产出透视表、趋势与异常项。",
   [('h3','产出'),
    ('ul',['按区域 / 产品 / 月份的透视','同比环比趋势','异常值提示']),
    ('callout','图表需内嵌，避免依赖外部 CDN（老田本机访问 jsdelivr 不通）。')])),
]

# ---------- 企业微信案例 ----------
CASES_WECOM = [
 ("chapter-12","02","客户跟进纪要整理", "企微案例",
  ch_body("拜访 / 通话后，把零散记录整理成统一格式的跟进纪要，方便后续转化跟踪。",
   [('h3','要点'),
    ('ul',['从聊天记录 / 录音提取关键承诺与待办','统一输出『需求-痛点-下一步』结构','沉淀进客户档案']),
    ('callout-warn','客户信息属于敏感数据，处理前确认授权范围，勿外泄。')])),
 ("chapter-14","04","企业微信消息汇总", "企微案例",
  ch_body("把分散在多群、多人的关键信息聚合成每日摘要，减少信息噪音。",
   [('h3','适用'),
    ('ul',['重点项目群进展','待办与风险','客户反馈汇总'])])),
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
 ("企业微信","01","客户跟进纪要整理","聊天记录转结构化纪要","cases-wecom.html#chapter-12",C_WECOM,"企微案例"),
 ("企业微信","02","企业微信消息汇总","多群信息聚合每日摘要","cases-wecom.html#chapter-14",C_WECOM,"企微案例"),
 ("WorkBuddy","01","初识 WorkBuddy","从回答到交付的 AI 工作台","manual-wb.html#chapter-1",C_WB,"WB手册"),
 ("WorkBuddy","02","下载、安装、登录与更新","多端安装与常见问题","manual-wb.html#chapter-2",C_WB,"WB手册"),
 ("WorkBuddy","03","主界面、任务与工作区","三区域/三模式/模型选择","manual-wb.html#chapter-3",C_WB,"WB手册"),
 ("WorkBuddy","04","快速完成第一个任务","任务说明怎么写","manual-wb.html#chapter-4",C_WB,"WB手册"),
 ("WorkBuddy","05","加载一个真正用得上的 Skill","Skill 原理与使用","manual-wb.html#chapter-5",C_WB,"WB手册"),
 ("WorkBuddy","06","专家和专家团","召唤/创建专家与专家团","manual-wb.html#chapter-6",C_WB,"WB手册"),
 ("WorkBuddy","07","使用连接器","MCP 与连接器加载","manual-wb.html#chapter-7",C_WB,"WB手册"),
 ("WorkBuddy","08","接入小程序与 IM 助理","微信/飞书/钉钉接入","manual-wb.html#chapter-8",C_WB,"WB手册"),
 ("WorkBuddy","09","如何接入外部 API","开放能力扩展","manual-wb.html#chapter-9",C_WB,"WB手册"),
 ("WorkBuddy","10","自动化任务","从想法到定时任务","manual-wb.html#chapter-10",C_WB,"WB手册"),
 ("WorkBuddy","11","办公三件套：Word、Excel、PPT","三件套联动实战","manual-wb.html#chapter-11",C_WB,"WB手册"),
 ("WorkBuddy","01","月度工作汇报自动生成","日报聚合月报并自动推送","cases-wb.html#chapter-11",C_WB,"WB案例"),
 ("WorkBuddy","05","销售数据透视分析","明细表出透视与趋势","cases-wb.html#chapter-15",C_WB,"WB案例"),
 ("WorkBuddy","03","培训方案一键成文","公文标准排版出 Word","cases-wb.html#chapter-13",C_WB,"WB案例"),
 ("WorkBuddy","01","把 SOP 沉淀为 Skill","把反复干的活固化成技能","advanced.html#chapter-22",C_WB,"进阶篇"),
 ("WorkBuddy","03","自动化可靠性实践","失败通知而非静默","advanced.html#chapter-24",C_WB,"进阶篇"),
]

SKILL_CATEGORIES = ["全部", "公文排版", "写作润色", "内容生产", "数据分析", "自动化", "企业微信", "销售获客", "效率工具", "邮箱通知"]

SKILLS = [
{
  "id":"tianwei-word-formatter",
  "ico":"📄",
  "title":"公文标准排版 v1.3",
  "desc":"所有 Word 文档统一采用公文标准 + 1.5 倍行距：大标题方正小标宋、一级标题黑体、正文仿宋。",
  "category":"公文排版",
  "status":"已落地",
  "hot":True,
  "overview":"将 Markdown 或纯文本内容按 GB/T 9704 路线一键排版为 Word：大标题方正小标宋简体二号、一级标题黑体三号、二级标题楷体_GB2312、正文仿宋_GB2312四号，1.5 倍行距，页边距上37mm/下35mm/左28mm/右26mm。",
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
  "category":"写作润色",
  "status":"已落地",
  "hot":False,
  "overview":"把通用 AI 输出转换成老田的口吻：日常闲聊、工作讨论、正式交付、散文四档语域自动切换；内置 11 维风格量化、去 AI 味规则、五步写作框架与平台适配（公众号/小红书/知乎/头条）。",
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
  "overview":"基于固定格式的日报（YYYY-MM/YYYY-MM-DD.md），月底自动汇总工作事项、产出成果与下月计划，生成公文标准排版月报，并推送到企业微信群与 QQ 邮箱。",
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
  "example":"运行月报自动化，生成本月工作月报并推送到「销售团队」企微群和 986898476@qq.com。",
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
  "overview":"通过 wecomcli-doc 连接器操作企业微信在线文档：按 docid 或文档 URL 读取 Markdown 内容、覆写正文、新建空白文档。适合把本地报告同步到团队知识库。",
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
  "category":"邮箱通知",
  "status":"已落地",
  "hot":False,
  "overview":"通过 qq-mail 连接器收发 QQ 邮件。发送遵循老田规范：先 GetMe 取 alias_id、分两步走（Phase 1 拿 confirmation_token，Phase 2 发送）、正文控制在 500 字以内、to 字段只传 email。",
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
  "overview":"通过 wecomcli-msg 连接器拉取企业微信会话与消息记录，支持文本/图片/文件/语音/视频类型；也可向指定会话发送文本消息，常用于自动化简报推送。",
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
  "overview":"面向销售/商务岗的日报→月报全自动化管线：口语输入自动转结构化日报（销售专属字段：电话/微信/拜访/商机/成交），月底从当月所有日报自动汇总月报，公文标准排版出 Word，QQ 邮箱附件 + 企微群 webhook 双通道推送。区分事实/推断/待补充，标注不确定性。",
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
  "overview":"内容生产三技能流水线：选题虾负责从口水稿/热点/主题挖掘选题并入选题库；文案虾负责大纲→初稿→Humanizer 去 AI 味润色→多平台改写（公众号/小红书/知乎/头条）；审核虾做 6 维度质量门禁（标题吸引力/小标题简洁性/数据准确性/逻辑/表达/废话清除），P0=0 且 P1≤2 才放行归档。",
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
  "overview":"pandas 跑完全部统计（groupby 排名、月份环比 pct_change、品类×月份透视找持续下滑），生成单文件 HTML：KPI 卡片 + 柱状图 + 双轴折线 + 饼图 + 下滑预警表 + 可执行建议。Chart.js 内嵌不依赖 CDN，离线可打开；数字全部来自脚本输出，禁止心算。",
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
  "overview":"通过企微群 webhook 推送报表与文件的标准做法：markdown 消息群内直接渲染关键数据；文件推送两步走——先 upload_media 取 media_id（3 天有效）再发 file 消息。关键坑：Git Bash 下 curl -F 上传返回空响应，必须用 Python urllib 原生 multipart 上传。",
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
  "overview":"解决企微群 image 消息内链接不可点的问题：Pillow 自动把 Markdown 简报渲染成深色竖版长图（编号徽章、来源标签），先发图片消息保证视觉冲击，再补一条 markdown 链接汇总消息保证每条资讯可点击跳转原文。",
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
  "category":"效率工具",
  "status":"已落地",
  "hot":False,
  "overview":"对话中流露保存/记忆/提醒意图即自动触发：内容写入个人写作系统 Markdown 库，自动判断类型并记录标题、类型标签、创建时间、来源对话摘要与正文；含链接时额外抓取摘要一并保存，存好后一句话告知。",
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
  "overview":"针对企微好友多但转化低的 B 端销售场景：按行业设计激活钩子资料（Word/PDF 指南）、分层触达话术和 Excel 测试追踪表。核心原则：价值先行、分层触达、先选 50~100 人小步测试、数据驱动迭代（发送/回复/意向/成交全程记录）。",
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
  "overview":"WorkBuddy 产品多渠道营销文案定制技能：围绕降本增效与开箱即用两大核心卖点，按渠道人群定制三版输出——公众号长文版面向企业决策者、小红书种草版面向职场人士、朋友圈短文案做极简传播。",
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
  "category":"效率工具",
  "status":"已落地",
  "hot":False,
  "overview":"安装 SkillHub / GitHub / 社区来源技能的标准流程：强制「先安全审计、后安装」硬顺序，静态审查 SKILL.md 及配套脚本是否含 curl|bash、os.system、凭证外送、未锁版本依赖等风险，确认安全后再落地到技能目录，Python 依赖进虚拟环境并锁版本。",
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
  "category":"效率工具",
  "status":"已落地",
  "hot":False,
  "overview":"把散乱命名的文件统一为「日期_主题_类型.扩展名」格式：执行前先输出改名预览清单，自动处理重名冲突，改名前做安全备份，小批量执行随时可回退，不碰目标目录以外的文件。",
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
  "overview":"腾讯云官方品牌视觉（腾云驾雾风格）的图像提示词生成器：先分析文章/内容，生成 5 个封面选题供挑选，选定后输出可直接投喂图像模型的高质量提示词。覆盖公众号封面、活动物料、朋友圈海报、产品图、信息图等场景。",
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
}
]

# ============================ 页面构建 ============================
def doc_sidebar(active_name):
    # 分区 part：笔记（4 项）+ 进阶篇 + 岗位与行业落地 + Skills / 交流
    parts = [
        ("企微手册", MANUAL_WECOM, C_WECOM, "manual-wecom.html"),
        ("企微案例", CASES_WECOM, C_WECOM, "cases-wecom.html"),
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
    items = ""
    for c in chs:
        items += '<a class="toc-heading" href="#' + c[0] + '">' + c[2] + '</a>'
    return ('<aside class="toc"><div class="toc-title">本页目录</div>' + items +
            '<div class="toc-progress"><div class="toc-progress-bar"><div class="toc-progress-fill" id="tocFill"></div></div>'
            '<div class="toc-progress-label">阅读进度</div>'
            '<span class="toc-back-top" onclick="goTop()">↑ 回到顶部</span></div></aside>')

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

def build_doc(active_name, title, sub, chs, fname, pcolor):
    accent = ('<style>:root{--accent:' + pcolor + ';--accent-soft:' + hex_rgba(pcolor, .12) +
              ';--accent-grad:' + pcolor + '}</style>')
    html = ('<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<meta name="description" content="' + SITE_DESC + '">'
            '<title>' + title + ' · ' + SITE_TITLE + '</title><style>' + CSS + '</style>' + accent + '</head>'
            '<body>' + topbar(active_name) +
            '<div class="layout">' + doc_sidebar(active_name) +
            '<main class="reading-section">' + reading_page(title, sub, chs) + '</main>' +
            doc_toc(chs) + '</div>' + footer() +
            '<script>' + JS + '</script></body></html>')
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(html)
    print("生成:", fname)

def build_index():
    # Hero
    hero = ('<section class="hero"><div class="hero-name">老田的 AI 实战笔记</div>'
            '<p class="hero-tagline">腾讯产品商务顾问的一线实战沉淀 —— 关于 WorkBuddy 与企业微信的'
            '使用手册、真实案例、进阶心法与可复用 Skill。边用边记，持续更新。</p>'
            '<div class="hero-tags">'
            '<span class="hero-tag wecom">企业微信</span>'
            '<span class="hero-tag teal">WorkBuddy</span>'
            '<span class="hero-tag coral">实战案例</span>'
            '<span class="hero-tag purple">Skill 沉淀</span></div></section>')
    # 板块卡片（笔记类别）：WB 在前，企微在后
    cards = [
        ("📘","WB手册","从 0 到 1，把 WorkBuddy 用起来","11 章：初识/安装/界面/Skill/专家/连接器/小程序/API/自动化/办公三件套","manual-wb.html",C_WB),
        ("📂","WB案例","真实任务的完整复现","月报/透视/培训方案","cases-wb.html",C_WB),
        ("🚀","进阶篇","从案例到系统，构建你的工作流","4 篇：Skill/多Agent/可靠性/双备份","advanced.html",C_WB),
        ("🎯","岗位与行业落地","按岗位 / 行业视角组织实战内容","销售/外贸/零售/制造 · 建设中","industry.html",C_INDUSTRY),
        ("📘","企微手册","企业微信账号、客户联系与协作","建设中 · 概览/客户联系/微盘文档","manual-wecom.html",C_WECOM),
        ("📂","企微案例","真实企微场景的落地打法","客户纪要 · 消息汇总","cases-wecom.html",C_WECOM),
    ]
    card_html = '<div class="cards">'
    for ico, name, desc, meta, href, color in cards:
        card_html += ('<a class="card" href="' + href + '">'
                      '<div class="card-ico" style="background:' + color + '22;color:' + color + '">' + ico + '</div>'
                      '<h3>' + name + '</h3><p>' + desc + '</p>'
                      '<div class="meta">' + meta + '</div><span class="arrow">→</span></a>')
    card_html += '</div>'
    # 最新文章 + 产品筛选
    pills = ('<div class="filter-pills">'
             '<span class="filter-pill active" data-part="" onclick="filterArticles(\'\')">全部</span>'
             '<span class="filter-pill" data-part="企业微信" onclick="filterArticles(\'企业微信\')">企业微信</span>'
             '<span class="filter-pill" data-part="WorkBuddy" onclick="filterArticles(\'WorkBuddy\')">WorkBuddy</span>'
             '</div>')
    wraps = "".join(article_wrap(p[0],p[1],p[2],p[3],p[4],p[5],p[6]) for p in HOME_ARTICLES)
    list_html = '<div class="article-list">' + wraps + '</div>'
    body = ('<div>' + hero +
            '<section class="section" id="notebooks"><div class="section-head"><h2><span class="bar"></span>笔记类别</h2>'
            '<p>手册、案例、进阶、岗位与行业落地，按类别快速进入，内容持续补充中</p></div>' + card_html + '</section>'
            '<section class="section" style="padding-top:0"><div class="section-head"><h2><span class="bar"></span>最新文章</h2>'
            '<p>点击产品快速筛选</p></div>' + pills + list_html + '</section></div>')
    html = wrap_page("首页", body)
    with open("index.html","w",encoding="utf-8") as f: f.write(html)
    print("生成: index.html")

def build_skills():
    # Hero
    hero = ('<section class="skills-hero"><h1>WorkBuddy Skills</h1>'
            '<p>' + str(len(SKILLS)) + ' 个已落地 / 运行中的实战技能，覆盖公文排版、写作与内容生产、数据分析、自动化、企业微信、销售获客、效率工具等场景。'
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
            modal + details)
    html = wrap_page("Skills", body, active="Skills")
    with open("skills.html","w",encoding="utf-8") as f: f.write(html)
    print("生成: skills.html")

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
if __name__ == "__main__":
    build_index()
    build_doc("企微手册","企业微信使用手册","账号体系、客户联系与协作实战",MANUAL_WECOM,"manual-wecom.html",C_WECOM)
    build_doc("WB手册","WorkBuddy 使用手册","从 0 到 1，把 WorkBuddy 用起来",MANUAL_WB,"manual-wb.html",C_WB)
    build_doc("企微案例","企业微信案例","真实企微场景的落地打法",CASES_WECOM,"cases-wecom.html",C_WECOM)
    build_doc("WB案例","WorkBuddy 案例","真实任务的完整复现",CASES_WB,"cases-wb.html",C_WB)
    build_doc("进阶篇","进阶篇","从案例到系统，构建你的工作流",ADVANCED,"advanced.html",C_WB)
    build_doc("岗位与行业落地","岗位与行业落地","按岗位 / 行业视角组织实战内容",INDUSTRY,"industry.html",C_INDUSTRY)
    build_skills()
    build_community()
    print("全部页面生成完成。")
