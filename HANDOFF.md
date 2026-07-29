# 续接说明 ·「老田的 AI 实战笔记」静态知识库

> 用途：上下文已满、重新开会话时使用。本文件自包含，新会话直接读它即可无缝接续。
> 更新时间：2026-07-29 21:41

---

## 一、项目目标（一句话）

对标 `fanxion98.github.io/workbuddy-bluebook`（小饭的 AI 实战笔记），做一个**个人沉淀 + 分享**用的静态网站。
老田身份：腾讯产品商务顾问（企业微信 + WorkBuddy 双产品线）。

---

## 二、当前进度

### ✅ 已完成
1. **分析原站**：纯静态单文件 HTML（CSS/JS 全内联、零依赖、零框架），首页(Hero+分类筛选卡) + 内层三栏文档(左目录树/中正文/右TOC进度条)。
2. **6 页站点初版**：单文件自包含、青绿+天蓝主题。
3. **配色改为 ima 风**：抓 ima favicon SVG 取真实品牌色（薄荷绿 `#4DEE9E` + 柠檬黄绿 `#D6E807`）；主色改翡翠绿、Hero 用薄荷→柠檬渐变，旧青蓝 `#14B8A6/#38BDF8` 等**零残留**。
4. **Logo 改为 TW**：左上角「田」→「TW」（无衬线、12px、加粗）。
5. **按产品分区重构（6 页 → 8 页）**：使用手册 + 案例篇拆成「企业微信 / WorkBuddy」两套；进阶篇/Skills/交流保持 WB 不分区；视觉双色标（企微绿 `#07C160` / WB 翡翠绿 `#10B981`）；案例内部不细分。
6. **导航与首页改为「笔记」类别（2026-07-29）**：
   - 顶部导航把「企微手册 / 企微案例 / WB手册 / WB案例」合并为「笔记」入口，点击跳转首页 `#notebooks` 锚点；
   - 首页「按产品分区浏览」改为「笔记类别」，6 张卡片顺序调整为 WB 在前、企微在后：WB手册 / WB案例 / 进阶篇 / 岗位与行业落地 / 企微手册 / 企微案例；
   - 新增「岗位与行业落地」页面（天蓝 `#0EA5E9`），占位章节：销售/外贸/零售/制造。
7. **Skills 页面重构为分类筛选 + 详情弹窗（2026-07-29）**：
   - 顶部 Hero + 分类标签（全部 / 公文排版 / 写作润色 / 自动化 / 企业微信 / 邮箱通知）；
   - 技能卡片网格，带「热门」标签与分类标签；
   - 点击卡片弹出详情面板，含：技能概述、部署方法、使用步骤、示例指令、应用场景；
   - 支持 URL hash 直接访问：`skills.html#skill-<id>`。
8. **部署到公网（GitHub Pages）准备就绪**：
   - 站点代码已推送至 `github.com/winston9868/shizhan-biji`（public 仓库），全部 9 页 + wechat-qr.png 入库；
   - 本机已生成 ed25519 SSH 密钥，remote 改为 SSH 方式，公钥已加入 GitHub，**`git push` 免密通道已验证可用**；
   - GitHub Pages 待老田在仓库 Settings → Pages 开启（Source 选 `main` 分支 /(root)），约 1-2 分钟出公网链接。

### ⏳ 待办（老田可选方向）
- A. 把**示例占位内容**替换成老田真实实战内容（企微手册目前是 3 个"建设中"占位章，未瞎编）。
- B. **开启 GitHub Pages**：进仓库 Settings → Pages → Source 选 `main` /(root) → Save，等待 1-2 分钟，链接即 `https://winston9868.github.io/shizhan-biji/`。
- C. 微调（如某个栏目色太跳、培训方案案例的归属、Hero 标语）。

---

## 三、文件清单（绝对路径）

| 文件 | 作用 |
|---|---|
| `E:\workbuddy\实战笔记\site\build_site.py` | **唯一改动入口**。所有内容/配色/结构集中在此，改完重跑即重建全部页面 |
| `E:\workbuddy\实战笔记\site\patch_colors.py` | 一次性配色补丁脚本（已用，正常不需再跑） |
| `E:\workbuddy\实战笔记\site\README.md` | 本地预览 + GitHub Pages 部署说明 |
| `E:\workbuddy\实战笔记\site\index.html` | 首页（按产品分区浏览 + 产品筛选） |
| `E:\workbuddy\实战笔记\site\manual-wecom.html` | 企业微信使用手册（企微绿主色） |
| `E:\workbuddy\实战笔记\site\manual-wb.html` | WorkBuddy 使用手册（WB 翡翠绿主色） |
| `E:\workbuddy\实战笔记\site\cases-wecom.html` | 企业微信案例（客户纪要、消息汇总） |
| `E:\workbuddy\实战笔记\site\cases-wb.html` | WorkBuddy 案例（月报、销售透视、培训方案） |
| `E:\workbuddy\实战笔记\site\advanced.html` | 进阶篇（不分区，WB 翡翠绿） |
| `E:\workbuddy\实战笔记\site\industry.html` | 岗位与行业落地（天蓝 `#0EA5E9`） |
| `E:\workbuddy\实战笔记\site\skills.html` | Skills 专栏（6 技能卡） |
| `E:\workbuddy\实战笔记\site\community.html` | 交流（关于我 + 电话/企业邮箱/企业微信二维码） |

> ⚠️ 旧文件 `manual.html` / `cases.html` 已删除，避免死链。

---

## 四、关键技术约定（改之前必看，防踩坑）

1. **只改 `build_site.py`，不要手改 html**。改完运行：
   ```
   C:/Users/田伟/.workbuddy/binaries/python/versions/3.13.12/python.exe build_site.py
   ```
   会重新生成全部 8 个 html。

2. **章节数据格式**（文档页章节列表）：
   ```python
   (id, num, title, badge, body_html)   # 五元素，缺一不可
   # c[0]=锚点id  c[1]=序号(如"01")  c[2]=标题  c[3]=徽标文字(如"WB手册")  c[4]=正文html
   ```
   正文 html 用 `ch_body(intro, blocks)` 生成，`blocks` 元素为 `('p'|'h3'|'ul'|'callout'|'callout-warn'|'callout-info'|'code'|'table', 内容)`。

3. **数据区变量名**（加内容只看这些）：
   `MANUAL_WB, MANUAL_WECOM, CASES_WB, CASES_WECOM, ADVANCED`（章节列表）
   `SKILLS`（技能卡）、`HOME_ARTICLES`（首页最新文章）、`SECTIONS`（8 项导航 `(name, href, ico, color, grp)`）

4. **主循环坑（已修，但别复发）**：`build_doc(active, title, sub, chs, fname, pcolor)` 第 4 参必须传**变量**（如 `MANUAL_WECOM`），**不能加引号**变成字符串——否则会被当字符序列遍历，`c[3]` 越界报错。

5. **主题色切换机制**：`build_doc` 注入 `<style>:root{--accent:主色}</style>` 覆盖默认，所以企微页绿、WB 页翡翠绿。新增分区页时把对应色值作为第 6 参传入即可（企微 `#07C160`、WB `#10B981`）。

---

## 五、配色方案（当前生效）

| 角色 | 色值 | 说明 |
|---|---|---|
| 品牌渐变（Logo/Hero） | 薄荷绿 `#4DEE9E` → 柠檬黄绿 `#D6E807` | 来自 ima favicon，站点品牌色 |
| 企业微信主色 | `#07C160` | 企微页强调色、导航色点 |
| WorkBuddy 主色 | `#10B981` | WB 页强调色、导航色点 |
| 站点主文字 | `#292524` | 浅色主题 |
| 背景 | `#FAFAF9` 卡片白 | 浅色主题 |
| 警示 callout | 琥珀 `#F59E0B` | — |

---

## 六、重新开会话时的接档提示（直接复制给新会话）

> "继续 `E:\workbuddy\实战笔记\site\` 的「老田的 AI 实战笔记」站点任务。先读 `site/HANDOFF.md` 了解全貌，再读 `site/build_site.py` 看当前代码。当前已完成：导航「笔记」跳转首页笔记类别、首页 6 张笔记类别卡（WB 在前企微在后）、新增「岗位与行业落地」页面、Skills 页面重构为分类筛选+详情弹窗（支持 URL hash 直达），ima 薄荷绿配色 + 三色标，Logo 为 TW。下一步待老田拍板：填充真实内容（尤其岗位与行业落地与 Skill 详情） / 部署公网 / 微调视觉。改动只通过 `build_site.py`，改完重跑生成。"

---

## 七、已验证状态（2026-07-29 20:16 最后生成）
- 本地 http.server 下 9 页均返回 200
- 企微页含 `--accent:#07C160`、WB 页含 `#10B981`、岗位与行业落地页含 `#0EA5E9`
- 导航「笔记」跳转首页 `#notebooks`；首页「笔记类别」6 张卡顺序为 WB 在前、企微在后
- Skills 页分类筛选、卡片网格、详情弹窗、URL hash 访问均正常
- 旧青蓝配色零残留

---

## 八、部署与持续更新（GitHub Pages + SSH 免密）

### 公网链接（Pages 开启后）
- 首页：`https://winston9868.github.io/shizhan-biji/`
- 各页：`https://winston9868.github.io/shizhan-biji/manual-wecom.html` 等

### SSH 免密 push 配置（已就绪）
- 本机密钥：`~/.ssh/id_ed25519`（私钥，空密码）+ `id_ed25519.pub`（公钥已加入 GitHub）
- remote：`git@github.com:winston9868/shizhan-biji.git`（SSH 方式）
- 验证：`ssh -T git@github.com` 返回 `Hi winston9868! You've successfully authenticated` 即通

### 以后更新站点的标准流程
1. 只改 `build_site.py`
2. 运行生成脚本（见第四节第 1 条）
3. 提交并推送：
   ```
   git add -A
   git commit -m "更新：xxx"
   git push        # 走 SSH，免密
   ```
4. GitHub Pages 自动重新构建（通常 1 分钟内生效）

### 开启 Pages（一次性，需老田网页操作）
仓库 → Settings → Pages → Build and deployment → Source 选 **Deploy from a branch** → Branch 选 **main** / **/(root)** → Save。

### 备选：CloudStudio 一键部署
若不想走 GitHub，可改走 CloudStudio 部署（个人免费额度），生成公网链接 `https://xxx.cloudstudio.dev/`，无需 GitHub 凭据。
