---
id: chapter-4
num: "04"
title: 第 4 章 快速完成第一个 WorkBuddy 任务
cat: WB手册
---

## 快速创建一个 WorkBuddy 任务

1. 点击“新建任务”；

![](images/001_image_C4q3bdNKso.BFqhj4mo.webp)

2. 选择或创建独立工作目录；

<div class="callout key">

<em>PS：WorkBuddy 采用文件夹级授权与高危拦截，首次操作请先在演练目录进行、留意授权范围，处理真实业务数据前谨慎确认</em>

</div>

![](images/002_image_GeeybIFZLo.BbWWIc4r.webp)

3. 判断应该使用模式，默认为Craft，还可以设置成Ask或Plan；

![](images/003_image_DZ55bxbCvo.DB9eN3-N.webp)

4. 选择模型，可以指定你想使用的模型，不同模型积分消耗不同。

![](images/004_image_JiigbkdTKo.DjMprcaA.webp)

5. 输入任务说明，“帮我分析一下《电商销售数据.xlsx》数据，生成一份汇报 PPT。”

![](images/005_image_ReDxbwNkYo.ltGwJePP.webp)

6. 如有必要，指定 Skill、专家、连接器或资料库，这里暂时忽略

![](images/006_image_INLGb7TDQo.CUdzVfVD.webp)

7. 发送后观察计划、工具调用和文件变更；

![](images/007_image_BD1FbDdcEo.C22GlpxL.webp)

8. 在结果区预览产物并验收。

文件可以本地打开、上传云端、或分享，注意分享前先确认产物不含敏感或涉密信息，按公司规范选择共享范围。

![](images/008_image_TzOAb2lxIo.B-jIFKL3.webp)

## 如何写一个任务说明

| 要素 | 要回答的问题 |
| --- | --- |
| 目标 | 最终要解决什么问题 |
| 输入 | 使用哪些文件、目录或链接 |
| 动作 | 需要分析、整理、转换还是生成 |
| 约束 | 哪些不能改，采用什么规范 |
| 输出 | 交付什么文件，放到哪里 |
| 验收 | 用什么标准判断合格 |

### 入门任务 A：整理文件

<div class="language-text vp-adaptive-theme"><span class="lang">text</span><pre class="shiki shiki-themes github-light github-dark vp-code"><code><span class="line"><span>目标：整理 input 目录中的练习文件，便于按类型查找。</span></span>
<span class="line"><span>输入：仅处理当前工作区的 input 目录。</span></span>
<span class="line"><span>动作：识别文件类型，提出分类和重命名方案。</span></span>
<span class="line"><span>约束：不删除、不覆盖原文件；重名时保留两份并标记序号。</span></span>
<span class="line"><span>输出：先生成 inventory.xlsx 和 proposed-actions.md。</span></span>
<span class="line"><span>验收：清单文件数与 input 实际文件数一致，所有动作可追溯。</span></span>
<span class="line"><span>在我确认 proposed-actions.md 前，不移动文件。</span></span></code></pre></div>

### 入门任务 B：生成会议纪要

<div class="language-text vp-adaptive-theme"><span class="lang">text</span><pre class="shiki shiki-themes github-light github-dark vp-code"><code><span class="line"><span>请把 input/meeting.txt 整理为结构化会议纪要。</span></span>
<span class="line"><span>必须包含：会议结论、待办事项、负责人、截止日期、待确认问题。</span></span>
<span class="line"><span>不能从原文确认的负责人或日期写“待确认”，不要自行补全。</span></span>
<span class="line"><span>输出 output/会议纪要.md 和 output/待办清单.xlsx。</span></span>
<span class="line"><span>验收：每一项结论可以在原文找到依据；待办不遗漏负责人和时间状态。</span></span></code></pre></div>

### 入门任务 C：Word 转 PPT

<div class="language-text vp-adaptive-theme"><span class="lang">text</span><pre class="shiki shiki-themes github-light github-dark vp-code"><code><span class="line"><span>把 input/项目汇报.docx 转成 10 页以内的内部汇报 PPT。</span></span>
<span class="line"><span>受众：部门负责人；汇报时长：8 分钟。</span></span>
<span class="line"><span>保持原文事实和数字，不新增未经证实的数据。</span></span>
<span class="line"><span>结构：背景、现状、问题、方案、计划、需要决策。</span></span>
<span class="line"><span>使用 reference/brand-guide.pdf 中的颜色与字体规范。</span></span>
<span class="line"><span>输出 output/项目汇报_v1.pptx，同时提供逐页内容清单。</span></span>
<span class="line"><span>验收：每页只有一个核心观点，数字与原文一致，正文在投影状态可读。</span></span></code></pre></div>
