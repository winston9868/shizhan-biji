---
id: chapter-5
num: "05"
title: 第 5 章 WorkBuddy加载一个真正用得上的 Skill
cat: WB手册
---

## Skill 是什么

WorkBuddy 本身负责理解任务和组织执行；Skill 则是一组可复用的说明、脚本、参考资料和资源，告诉 Agent 某类任务应该怎样做、调用什么工具、交付什么格式。

Anthropic 在 2025 年 10 月正式推出 Agent Skills，2025 年 12 月将其发布为开放标准。

一个最标准的 Skill，大概长这样：

<div class="language-Plain vp-adaptive-theme"><span class="lang">Plain</span><pre class="shiki shiki-themes github-light github-dark vp-code"><code><span class="line"><span>my-skill/</span></span>
<span class="line"><span>├── SKILL.md</span></span>
<span class="line"><span>├── scripts/</span></span>
<span class="line"><span>│   └── check.py</span></span>
<span class="line"><span>├── references/</span></span>
<span class="line"><span>│   └── guide.md</span></span>
<span class="line"><span>└── assets/</span></span>
<span class="line"><span>    └── template.pptx</span></span></code></pre></div>

其中只有 <code>SKILL.md</code> 是必须的。

<div class="language-Markdown vp-adaptive-theme"><span class="lang">Markdown</span><pre class="shiki shiki-themes github-light github-dark vp-code"><code><span class="line"><span style="--shiki-light:#005CC5;--shiki-light-font-weight:bold;--shiki-dark:#79B8FF;--shiki-dark-font-weight:bold;">---</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">name: tech-article-writing</span></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">description: 用于撰写 AI 产品、模型评测和科技行业相关文章</span></span>
<span class="line"><span style="--shiki-light:#005CC5;--shiki-light-font-weight:bold;--shiki-dark:#79B8FF;--shiki-dark-font-weight:bold;">---</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;">收到写作任务后：</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-light:#E36209;--shiki-dark:#FFAB70;">1.</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> 先确认文章核心角度</span></span>
<span class="line"><span style="--shiki-light:#E36209;--shiki-dark:#FFAB70;">2.</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> 查找一手资料</span></span>
<span class="line"><span style="--shiki-light:#E36209;--shiki-dark:#FFAB70;">3.</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> 对核心事实交叉验证</span></span>
<span class="line"><span style="--shiki-light:#E36209;--shiki-dark:#FFAB70;">4.</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> 根据用户写作风格完成初稿</span></span>
<span class="line"><span style="--shiki-light:#E36209;--shiki-dark:#FFAB70;">5.</span><span style="--shiki-light:#24292E;--shiki-dark:#E1E4E8;"> 检查禁用句式和 AI 味表达</span></span></code></pre></div>

还可以带上：

<div class="language-Plain vp-adaptive-theme"><span class="lang">Plain</span><pre class="shiki shiki-themes github-light github-dark vp-code"><code><span class="line"><span>references/style.md</span></span></code></pre></div>

## Skill 是怎么工作的

Skill 最关键的设计，其实不是 SKILL.md，而是 Progressive Disclosure，渐进式披露。

假设你的 Agent 装了 100 个 Skill。

它不会一上来把 100 个 Skill 的完整内容全部塞进上下文。这样不仅浪费 Token，还会让模型被大量无关指令干扰。

标准做法分三层。

第一层，Agent 启动时只看所有 Skill 的名称和 description。

比如：

<div class="language-Plain vp-adaptive-theme"><span class="lang">Plain</span><pre class="shiki shiki-themes github-light github-dark vp-code"><code><span class="line"><span>pptx</span></span>
<span class="line"><span>处理 PowerPoint 创建、编辑、读取任务</span></span>
<span class="line"><span></span></span>
<span class="line"><span>pdf</span></span>
<span class="line"><span>处理 PDF 提取、合并、编辑、填写任务</span></span>
<span class="line"><span></span></span>
<span class="line"><span>tech-article-writing</span></span>
<span class="line"><span>撰写 AI 和科技行业文章</span></span></code></pre></div>

第二层，当用户说：

<div class="language-Plain vp-adaptive-theme"><span class="lang">Plain</span><pre class="shiki shiki-themes github-light github-dark vp-code"><code><span class="line"><span>帮我写一篇 WorkBuddy 的公众号文章</span></span></code></pre></div>

Agent 根据 description 判断 <code>tech-article-writing</code> 可能相关，这时才加载完整的 <code>SKILL.md</code>。

第三层，执行过程中发现需要模仿你的写作风格，才继续读取：

<div class="language-Plain vp-adaptive-theme"><span class="lang">Plain</span><pre class="shiki shiki-themes github-light github-dark vp-code"><code><span class="line"><span>references/style.md</span></span></code></pre></div>

需要检查 AI 味，才执行：

<div class="language-Plain vp-adaptive-theme"><span class="lang">Plain</span><pre class="shiki shiki-themes github-light github-dark vp-code"><code><span class="line"><span>scripts/check-ai-phrases.py</span></span></code></pre></div>

标准规范建议，所有 Skill 启动时只加载数十至上百Token的元数据，Skill 激活后再加载完整说明，其他资料和脚本继续按需读取。OpenAI Codex 也采用类似机制，先向模型暴露 Skill 的名称、描述和路径，再在模型决定使用时读取完整内容。

所以 Skill 解决了一个长期困扰 Agent 的问题：

<strong>怎么给 Agent 很多知识和工作方法，又不把所有东西永远塞在 Prompt 里。</strong>

## Skill 跟 Prompt 到底有什么区别

这是最核心的问题。

| 维度 | Prompt | Skill |
| --- | --- | --- |
| 核心作用 | 描述当前任务 | 定义一类任务怎么做 |
| 生命周期 | 通常针对一次请求 | 长期复用 |
| 触发方式 | 用户主动输入 | Agent 自动选择或用户显式调用 |
| 载体 | 主要是文本 | 文件夹 |
| 内容 | 指令、上下文、示例 | 指令、脚本、资料、模板、资源 |
| 上下文占用 | 通常直接进入上下文 | 按需加载 |
| 复用 | 经常复制粘贴 | 原生可复用 |
| 分享 | Prompt 文本 | 完整能力包 |
| 执行 | 本身只是指令 | 可以调用附带脚本和工具 |
| 模型参数 | 不改变 | 同样不改变 |

最简单的理解是：

<div class="language-Plain vp-adaptive-theme"><span class="lang">Plain</span><pre class="shiki shiki-themes github-light github-dark vp-code"><code><span class="line"><span>Prompt = 任务</span></span>
<span class="line"><span>Skill = 做法</span></span></code></pre></div>

## Skill 有哪些作用

\*\*第一个作用，是给模型补充程序性知识。\*\*大模型往往知道大量知识，但未必知道你的事情具体应该怎么做，比如它知道 SQL，但它不知道你公司的：

<div class="language-Plain vp-adaptive-theme"><span class="lang">Plain</span><pre class="shiki shiki-themes github-light github-dark vp-code"><code><span class="line"><span>canonical user_id 在哪张表</span></span>
<span class="line"><span>subscriptions 表是 append-only</span></span>
<span class="line"><span>查询退款时必须排除某个状态</span></span>
<span class="line"><span>Grafana 对应 dashboard ID 是多少</span></span></code></pre></div>

这些知识非常适合做 Skill，Anthropic 在内部使用了数百个 Skill，最终发现主要集中在 API 和内部库使用、产品验证、数据分析、业务流程自动化、代码脚手架、代码审查、CI/CD、故障 Runbook 和基础设施运维九类场景。

\*\*第二个作用，是固定复杂工作流，\*\*比如做一次行业调研。

普通 Prompt 可能是：

<div class="language-Plain vp-adaptive-theme"><span class="lang">Plain</span><pre class="shiki shiki-themes github-light github-dark vp-code"><code><span class="line"><span>详细调研一下 WorkBuddy</span></span></code></pre></div>

模型每一次都会重新思考：

<div class="language-Plain vp-adaptive-theme"><span class="lang">Plain</span><pre class="shiki shiki-themes github-light github-dark vp-code"><code><span class="line"><span>去哪里找资料</span></span>
<span class="line"><span>先查什么</span></span>
<span class="line"><span>怎么验证</span></span>
<span class="line"><span>跟谁对比</span></span>
<span class="line"><span>输出什么结构</span></span></code></pre></div>

Skill 可以把流程固定下来：

<div class="language-Plain vp-adaptive-theme"><span class="lang">Plain</span><pre class="shiki shiki-themes github-light github-dark vp-code"><code><span class="line"><span>1. 官方网站</span></span>
<span class="line"><span>2. 官方公众号和发布会</span></span>
<span class="line"><span>3. 产品文档</span></span>
<span class="line"><span>4. 实际产品测试</span></span>
<span class="line"><span>5. 同类产品对比</span></span>
<span class="line"><span>6. 核心观点提炼</span></span>
<span class="line"><span>7. 事实核验</span></span></code></pre></div>

这种能力称为 Encoded Preference Skill。模型本来能完成每一个单独步骤，但 Skill 把这些步骤按照团队或个人的工作方式组织起来。

另一类是 Capability Uplift Skill，给模型补充它原本做不好或不稳定的能力，例如复杂文档、PDF 和 PPT 处理。

<strong>第三个作用，是减少重复 Prompt。</strong>

你现在跟 AI 合作，其实有大量内容是在重复说，比如你经常告诉我：

<div class="language-Plain vp-adaptive-theme"><span class="lang">Plain</span><pre class="shiki shiki-themes github-light github-dark vp-code"><code><span class="line"><span>不要写得太 AI</span></span>
<span class="line"><span>长短句结合</span></span>
<span class="line"><span>不要过度点列</span></span>
<span class="line"><span>要有自己的判断</span></span>
<span class="line"><span>技术内容要克制</span></span>
<span class="line"><span>不要编造例子</span></span></code></pre></div>

这些其实已经天然适合做成一个 <code>writing-style</code> Skill。

以后你的 Prompt 只需要：

<div class="language-Plain vp-adaptive-theme"><span class="lang">Plain</span><pre class="shiki shiki-themes github-light github-dark vp-code"><code><span class="line"><span>写一篇 WorkBuddy 文章</span></span></code></pre></div>

写作习惯、资料标准、禁用表达、文章流程，都由 Skill 提供。

<strong>第四个作用，是把个人经验和组织经验资产化。</strong>

传统 Prompt 最大的问题是容易散落在：

<div class="language-Plain vp-adaptive-theme"><span class="lang">Plain</span><pre class="shiki shiki-themes github-light github-dark vp-code"><code><span class="line"><span>聊天记录</span></span>
<span class="line"><span>飞书文档</span></span>
<span class="line"><span>Notion</span></span>
<span class="line"><span>个人脑子里</span></span></code></pre></div>

Skill 是文件，所以它可以：

<div class="language-Plain vp-adaptive-theme"><span class="lang">Plain</span><pre class="shiki shiki-themes github-light github-dark vp-code"><code><span class="line"><span>Git 管理</span></span>
<span class="line"><span>版本回滚</span></span>
<span class="line"><span>团队共享</span></span>
<span class="line"><span>A/B 测试</span></span>
<span class="line"><span>自动评测</span></span>
<span class="line"><span>持续更新</span></span></code></pre></div>

这件事情很关键。

## WorkBuddy里找到合适的Skill

打开左侧“专家·技能·连接器”，可以从技能市场搜索，也可以用“查找技能”描述需求。

![](images/001_image_TdcLblfvIo.JAXghKd8.webp)

也可以在SkillHub技能市场里找到合适的Skill

![](images/002_image_V3E5bsVZGo.CNcIiHwr.webp)

除了从推荐列表里直接安装，还可以<strong>导入自己下载的技能</strong>。

比如你在网上看到一个好用的技能包，下载下来是一个 zip 压缩文件，操作流程是这样的：点击"上传技能"，把 zip 文件加载即可

![](images/003_image_Oag3bNQHOo.b-8ptr40.webp)

![](images/004_image_GgOebNBh3o.CPUvV_oi.webp)

## 使用Skill解决一个任务

比如，你让AI写了一篇文章，需要去除AI味，你可以找到“文章去AI味工具 ”Skill，安装之后，使用时，直接 “/” 可以换出。

![](images/005_20260708200848_NN3hbPsKAo.B8peHH8Y.webp)

你只需要引用Skill内容，把文章给到即可，

![](images/006_image_Xom2btXVZo.Cxu6iZ-s.webp)

WorkBuddy 会先加载skill的内容，

![](images/007_image_AmOVb1oGEo.D502lg6P.webp)

根据skill中的规则，来执行，比如要去除不是而是、双引号等内容，

![](images/008_image_FbpQbmSswo.nrN9jN1J.webp)

修改之后，可以得到结果，确实去除了AI味。

![](images/009_image_RhBKbRhgIo.BFK_niy2.webp)

## Skill的关闭和卸载

从全部技能中，点击我安装的

![](images/010_image_NGsdbBcjso.CTQ38jHp.webp)

按钮关闭（则关闭该Skill）

![](images/011_image_DABBb41fGo.IjaR-w9T.webp)

点击“···”，可以选择删除或编辑该Skill

![](images/012_image_Uya3bNC9io.7Wlm0KE8.webp)
