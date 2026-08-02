#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build.py —— 老田手动改完 WB手册 后的「一键重建」入口

用法（在 site/ 目录下）：
    python build.py
等价于：
    python build_md.py      # 把 content/manual/*.md 渲染成 wb_manual.json
    python build_site.py    # 用 wb_manual.json 重建所有 HTML 页面

说明：
- content/manual/*.md 是「内容源头」，归老田手动编辑；改完跑本脚本即生效。
- build_site.py（框架/模板/导航/样式）仍归 YOYO 维护，老田无需碰。
- 本脚本只重建本地文件；发布到公网需另行 git push（见末尾提示）。
"""
import os
import sys
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
# 本机 venv（已装 markdown 库），用于 MD→JSON 步骤
VENV_PY = r"C:/Users/田伟/.workbuddy/binaries/python/envs/default/Scripts/python.exe"


def run(cmd):
    print(">>", " ".join(cmd))
    subprocess.run(cmd, cwd=HERE, check=True)


def main():
    # 1) MD -> JSON（需要 markdown 库，优先用 venv）
    if os.path.exists(VENV_PY):
        run([VENV_PY, "build_md.py"])
    else:
        try:
            import markdown  # noqa
        except ImportError:
            print("缺少依赖：请先运行  pip install markdown  后再执行。")
            sys.exit(1)
        run([sys.executable, "build_md.py"])

    # 2) JSON -> HTML（纯标准库，任意 python 均可）
    run([sys.executable, "build_site.py"])

    print("\n✅ 全部页面已在本机重建完成。")
    print("📤 发布到公网（GitHub Pages）请执行：")
    print("   git add . && git commit -m \"更新 WB手册\" && git push")


if __name__ == "__main__":
    main()
