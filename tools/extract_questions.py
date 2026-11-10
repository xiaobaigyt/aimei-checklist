#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 index.html 导出 40 题到 questions.json。

改了 index.html 里的 QUESTIONS 数组之后，跑一次这个脚本同步数据镜像：

    python tools/extract_questions.py

只依赖标准库。
"""
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(ROOT, "index.html")
OUT = os.path.join(ROOT, "questions.json")


def main():
    with io.open(HTML, "r", encoding="utf-8") as f:
        html = f.read()

    m = re.search(r"var QUESTIONS = \[(.*?)\n  \];", html, re.S)
    if not m:
        sys.exit("没在 index.html 里找到 QUESTIONS 数组")

    questions = re.findall(r'"([^"]*)"', m.group(1))
    if not questions:
        sys.exit("QUESTIONS 数组是空的")

    levels = []
    for v, label in ((1, "这就是暧昧"), (2, "有点上头，但不算"), (3, "纯友谊，没问题")):
        levels.append({"value": v, "label": label})

    types = []
    for avg, name in re.findall(r'if\(avg < ([\d.]+)\).*?name:"([^"]+)"', html):
        types.append({"avg_lt": float(avg), "name": name})
    types.append({"avg_lt": None, "name": "纯友谊信徒型"})

    data = json.loads(io.open(OUT, "r", encoding="utf-8").read()) if os.path.exists(OUT) else {}
    data.update({
        "title": data.get("title", "这算暧昧吗？判定表"),
        "description": data.get("description", "40 个场景，测你和 TA 之间那段还没名字的关系。"),
        "license": "CC BY-NC-SA 4.0",
        "note": "本文件由 index.html 导出，是数据镜像；以 index.html 里的 QUESTIONS 数组为准。",
        "levels": levels,
        "questions": questions,
        "types": types,
    })

    with io.open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("导出 %d 题 -> %s" % (len(questions), os.path.relpath(OUT, ROOT)))


if __name__ == "__main__":
    main()