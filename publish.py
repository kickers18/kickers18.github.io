#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
个人主页一键发布脚本

用法：
    python publish.py                      # 自动提交信息（时间戳）
    python publish.py "新增 2 篇论文"        # 自定义提交信息
    python publish.py --dry-run            # 只看要提交什么，不推送

说明：
    1. 发布前自动把 index.html 备份到 .backups/（保留最近 30 份）
    2. 提交并推送到 origin/gh-pages
    3. GitHub Pages 通常 30 秒 ~ 2 分钟生效
"""

import os
import re
import subprocess
import sys
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
BACKUP_DIR = os.path.join(ROOT, ".backups")
BACKUP_KEEP = 30


def run(cmd, check=True, capture=True):
    """执行命令，返回 (returncode, stdout)"""
    p = subprocess.run(
        cmd, cwd=ROOT, shell=True,
        capture_output=capture, text=True, encoding="utf-8", errors="replace",
    )
    if check and p.returncode != 0:
        print(p.stdout or "", p.stderr or "")
        sys.exit(p.returncode)
    return p.returncode, (p.stdout or "").strip()


def backup():
    """备份 index.html"""
    src = os.path.join(ROOT, "index.html")
    if not os.path.exists(src):
        return None
    os.makedirs(BACKUP_DIR, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dst = os.path.join(BACKUP_DIR, f"{stamp}_index.html")
    with open(src, "rb") as f:
        data = f.read()
    with open(dst, "wb") as f:
        f.write(data)
    # 只保留最近 N 份
    files = sorted(f for f in os.listdir(BACKUP_DIR) if f.endswith("_index.html"))
    for old in files[:-BACKUP_KEEP]:
        try:
            os.remove(os.path.join(BACKUP_DIR, old))
        except OSError:
            pass
    return dst


def quick_check():
    """发布前的轻量自检：标签配对 + 常见残缺模式"""
    src = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    problems = []

    # 1. 属性值引号后紧跟非空白/非 > 字符（常见于漏写 '>'，如 rel="noopener"GB/T...）
    for i, line in enumerate(src.split("\n"), 1):
        for m in re.finditer(r'="[^"]*"[^\s>/]', line):
            if "<a" in line[: m.start()] and "</a>" in line[m.end():]:
                problems.append(
                    f"行 {i}: 标签疑似缺 '>' → ...{line.strip()[:90]}"
                )

    # 2. 一行里 <a 出现但没有 </a>
    for i, line in enumerate(src.split("\n"), 1):
        n_open = len(re.findall(r"<a\b", line))
        n_close = line.count("</a>")
        if n_open and n_close < n_open:
            problems.append(f"行 {i}: <a> 未闭合（开 {n_open} / 闭 {n_close}）→ {line.strip()[:80]}")

    # 3. 空徽章
    for i, line in enumerate(src.split("\n"), 1):
        if re.search(r'<span class="pub-badge">\s*</span>', line):
            problems.append(f"行 {i}: 空徽章 <span class=\"pub-badge\"></span>")

    return problems


def main():
    args = [a for a in sys.argv[1:]]
    dry = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]
    msg = " ".join(args).strip() or f"更新主页 {datetime.now().strftime('%Y-%m-%d %H:%M')}"

    os.chdir(ROOT)

    # 0. 自检
    problems = quick_check()
    if problems:
        print("[自检] 发现以下可疑问题（不阻断发布，建议修完再发）：")
        for p in problems:
            print("   ! " + p)
        print()
    else:
        print("[自检] HTML 结构无明显问题")

    # 1. 是否有改动
    _, status = run("git status --porcelain")
    if not status:
        print("[提示] 没有需要提交的改动")
        return 0

    print("[变更]")
    for line in status.split("\n"):
        print("   " + line)
    print()

    if dry:
        print(f"[dry-run] 提交信息预览：{msg}")
        return 0

    # 2. 备份
    dst = backup()
    if dst:
        print(f"[备份] {os.path.relpath(dst, ROOT)}")

    # 3. 提交推送
    run("git add -A")
    run(f'git commit -m "{msg}"')
    print("[推送] 正在推送到 origin/gh-pages ...")
    code, out = run("git push origin gh-pages", check=False)
    if code != 0:
        print("[失败] push 被拒绝或未认证：")
        print(out)
        print("\n若提示认证失败：本机还没有 GitHub 凭据，"
              "请执行一次 `ssh -T git@github.com` 确认 SSH 可用，或重新配置 PAT。")
        return code

    print("[成功] 已推送")
    print("[生效] https://kickers18.github.io 约 30 秒 ~ 2 分钟后更新")
    return 0


if __name__ == "__main__":
    sys.exit(main())
