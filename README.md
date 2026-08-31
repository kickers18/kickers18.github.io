# kickers18.github.io

任文奇个人学术主页 · https://kickers18.github.io

## 目录说明

| 文件 | 说明 |
|---|---|
| `index.html` | 主页面（单文件 SPA：全部 CSS/JS 内嵌） |
| `my_photo.jpg` | 头像 |
| `publish.py` | 一键发布脚本（自检 → 备份 → 提交 → 推送） |
| `.nojekyll` | 禁用 GitHub Pages 的 Jekyll 处理 |
| `.backups/` | publish.py 自动生成的 index.html 快照（不入库） |

已删除：`index.md`（旧版，含明文邮箱）、`index2.html` / `index2.md`（废弃副本）、`_config.yml`（Jekyll 主题配置，随 .nojekyll 一并废弃）。

## 对话式更新工作流（与 WorkBuddy 配合）

1. **改内容**：直接告诉 WorkBuddy 要改什么（加论文、改获奖、换链接……），由 WorkBuddy 修改本地 `index.html`。
   - 本地工作副本：`C:\Users\renwenqi\WorkBuddy\AI Coding\homepage`
   - 分支：`gh-pages`
2. **发布**：WorkBuddy 执行
   ```
   python publish.py "提交说明"
   ```
   脚本会自动：HTML 结构自检 → 备份 index.html → git 提交 → 推送。
3. **生效**：GitHub Pages 约 30 秒 ~ 2 分钟后线上可见。

## publish.py 自检项

- `<a>` 标签缺 `>` / 未闭合（历史上出过 2 处，导致标准列表渲染错乱）
- 空徽章 `<span class="pub-badge"></span>`
- 发布前自动备份（保留最近 30 份），回滚直接从 `.backups/` 取

## SSH 推送

- 密钥：`~/.ssh/id_ed25519_github`（对应公钥需添加到 GitHub → Settings → SSH keys）
- 远程：`git@github.com:kickers18/kickers18.github.io.git`

## 2026-08-31 改版记录

- 修复：2 处破损 `<a>` 标签（GB/T 42382.2、大模型第4部分标准）、2 处空徽章、专利悬浮提示专利号错误
- 修复：KBS 论文链接（原 sciencedirect 反爬页，且 2026-08-03 曾误替换为他人论文 DOI；正确 DOI 10.1016/j.knosys.2026.116267 已验证）
- 修复：SIGNet（easychair 登录页）、Sensors（期刊主页）、FAME（会议主页）等占位链接
- 21 条专利链接：CNIPA 检索首页 → Google Patents 搜索直达
- 新增：Google Scholar / GitHub 入口、邮箱 mailto 可点击（源码仍反爬）、深色模式、BibTeX 一键复制（27 条）、打印样式（Ctrl+P 得 CV）、JSON-LD 结构化数据、og:image、favicon、页脚"最后更新"
- 无障碍：导航 role=tab / aria-selected / 键盘 ←→ 切换

## 推送认证（2026-08-31 实测）

本机网络环境 SSH（22/443）到 GitHub 均被连接重置，不可用；HTTPS 正常。
采用方案：HTTPS + Windows 凭据管理器（GCM）。
- 方式 A：用户在本机终端（非 WorkBuddy Bash）进入本目录执行一次 `git push`，浏览器 OAuth 授权一次后凭据长期缓存。
- 方式 B：用户提供 fine-grained PAT（仅本仓库 Contents 读写），由助手写入 GCM。
