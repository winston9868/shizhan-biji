# -*- coding: utf-8 -*-
"""把站点配色从青蓝改为 ima 薄荷绿+柠檬黄绿风。"""
import io, sys
path = r"E:\workbuddy\实战笔记\site\build_site.py"
with io.open(path, "r", encoding="utf-8") as f:
    s = f.read()

def apply(pairs):
    global s
    for a, b in pairs:
        n = s.count(a)
        s = s.replace(a, b)
        print(f"  {a!r} -> {b!r}  (x{n})")

print("== 1. 注入 --color-primary-50 ==")
apply([("  --c-purple:#F472B6;", "  --c-purple:#F472B6;\n  --color-primary-50:rgba(16,185,129,.12);")])

print("== 2. 渐变整体串（先换，避免被下方散色替换破坏）==")
apply([
 ("linear-gradient(135deg,#14B8A6,#38BDF8)", "linear-gradient(135deg,#4DEE9E,#D6E807)"),
 ("linear-gradient(120deg,#14B8A6,#38BDF8)", "linear-gradient(120deg,#10B981,#84CC16)"),
 ("linear-gradient(90deg,#14B8A6,#38BDF8)",  "linear-gradient(90deg,#10B981,#84CC16)"),
 ("linear-gradient(120deg,#0F766E,#0EA5E9,#7C3AED)", "linear-gradient(120deg,#047857,#10B981,#84CC16)"),
 ("linear-gradient(180deg,#14B8A6,#38BDF8)", "linear-gradient(180deg,#4DEE9E,#D6E807)"),
])

print("== 3. 散落主色 hex ==")
apply([
 ("#14B8A6", "#10B981"),
 ("#38BDF8", "#06B6D4"),
 ("#FB923C", "#F59E0B"),
 ("#F472B6", "#A855F7"),
 ("#0F766E", "#047857"),
])

print("== 4. rgba 色调 ==")
apply([
 ("rgba(20,184,166,.12)", "rgba(16,185,129,.12)"),
 ("rgba(20,184,166,.08)", "rgba(16,185,129,.08)"),
 ("rgba(20,184,166,.07)", "rgba(16,185,129,.07)"),
 ("rgba(56,189,248,.14)", "rgba(6,182,212,.14)"),
 ("rgba(56,189,248,.3)",  "rgba(16,185,129,.3)"),
 ("rgba(56,189,248,.08)", "rgba(6,182,212,.08)"),
 ("rgba(251,146,60,.14)", "rgba(245,158,11,.14)"),
 ("rgba(251,146,60,.08)", "rgba(245,158,11,.08)"),
 ("rgba(244,114,182,.14)","rgba(168,85,247,.14)"),
])

print("== 5. hero-tag 文字色 ==")
apply([
 ("#0369A1", "#0E7490"),
 ("#C2410C", "#B45309"),
 ("#A21CAF", "#7E22CE"),
])

print("== 6. 数据内联色（带引号）==")
apply([
 ('"#14B8A6"', '"#10B981"'),
 ('"#38BDF8"', '"#06B6D4"'),
 ('"#FB923C"', '"#84CC16"'),
 ('"#F472B6"', '"#A855F7"'),
 ('"#A8A29E"', '"#64748B"'),
])

with io.open(path, "w", encoding="utf-8") as f:
    f.write(s)
print("== 完成，已写回 build_site.py ==")
