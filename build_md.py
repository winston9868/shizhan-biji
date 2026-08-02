#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_md.py —— 把 content/manual/*.md 渲染成 site/wb_manual.json

老田手动编辑流程（改完长文后发布）：
  1) 编辑 content/manual/chapter-N.md   （用任意编辑器写 Markdown）
  2) 运行：python build_md.py           （重新生成 wb_manual.json）
  3) 运行：python build_site.py         （重建所有 HTML 页面）
  4) git add . && git commit -m "更新手册" && git push

框架/模板（build_site.py、导航、样式、卡片）仍归 YOYO 维护；
长文内容（content/manual/*.md）归老田，改了不会被覆盖。

依赖：pip install markdown
"""
import os
import re
import json
import markdown

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(HERE, "content", "manual")
OUT_JSON = os.path.join(HERE, "wb_manual.json")

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)


def parse_front(text):
    m = FM_RE.match(text)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, m.group(2)


def render():
    if not os.path.isdir(CONTENT_DIR):
        raise SystemExit("找不到内容目录: " + CONTENT_DIR)
    chapters = []
    for fn in sorted(os.listdir(CONTENT_DIR)):
        if not fn.endswith(".md") or fn.startswith("_"):
            continue
        with open(os.path.join(CONTENT_DIR, fn), encoding="utf-8") as f:
            raw = f.read()
        meta, body = parse_front(raw)
        md = markdown.Markdown(extensions=["extra", "attr_list", "tables", "fenced_code"])
        html = md.convert(body)
        chapters.append({
            "id": meta.get("id", fn[:-3]),
            "num": meta.get("num", "01"),
            "title": meta.get("title", ""),
            "cat": meta.get("cat", "WB手册"),
            "html": html,
        })
    chapters.sort(key=lambda c: int(re.sub(r"\D", "", c["num"]) or 0))
    return [[c["id"], c["num"], c["title"], c["cat"], c["html"]] for c in chapters]


def main():
    chs = render()
    if os.path.exists(OUT_JSON):
        with open(OUT_JSON, encoding="utf-8") as f:
            old = f.read()
        with open(OUT_JSON + ".bak", "w", encoding="utf-8") as f:
            f.write(old)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump({"chapters": chs}, f, ensure_ascii=False, indent=1)
    print("已生成", OUT_JSON, "（共", len(chs), "章）｜原文件已备份为 wb_manual.json.bak")


if __name__ == "__main__":
    main()
