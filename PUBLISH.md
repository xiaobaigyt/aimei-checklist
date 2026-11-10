# 发布指南 · 把仓库推到 GitHub 并开启 Pages

本地已经 `git init` + 首次提交完成（commit `3d263b5`），分支 `main`。

剩下三步：**建远程仓库 → 关联 → push → 开 Pages**。按你手头条件选一条路。

---

## 先确认两件事

1. GitHub 用户名（下面用 `<USER>` 代替）。
2. 仓库名，建议 `ambiguous-check` 或 `aimei-checklist`（纯英文、无空格，Pages 链接更干净）。

---

## 路径 A：你已在 GitHub 网页建好空仓库（最省事）

在 GitHub 点 **New repository**，填仓库名、选 **Public**、**不要**勾 "Initialize with README"（否则会和本地冲突），建好后复制仓库地址，然后：

```powershell
cd "E:\workbuddy完成版\2026-11-10-暧昧判定表-开源"
git remote add origin https://github.com/<USER>/<REPO>.git
git push -u origin main
```

第一次 push 会弹浏览器让你登录 GitHub（Git Credential Manager 已经配好），授权一次即可。

---

## 路径 B：装 GitHub CLI，一条龙（推荐给以后还要发项目的）

```powershell
winget install --id GitHub.cli
# 装完重开一个终端，然后：
gh auth login          # 选 GitHub.com → HTTPS → 浏览器登录
cd "E:\workbuddy完成版\2026-11-10-暧昧判定表-开源"
gh repo create <REPO> --public --source=. --remote=origin --push
```

`gh repo create` 会自动建仓库、加 remote、push 一条龙。

---

## 路径 C：只交付本地仓库，你自己手动推

把这个文件夹整包拷走，或自己 `git remote add` + `git push`。GitHub 也支持网页端直接拖拽上传文件，但这样会丢掉 commit 历史，不建议。

---

## 开启 GitHub Pages（push 完之后）

1. 打开 `https://github.com/<USER>/<REPO>/settings/pages`
2. **Source** 选 `Deploy from a branch`
3. **Branch** 选 `main` / `root`，保存
4. 等约 30 秒，访问 `https://<USER>.github.io/<REPO>/`

单文件应用不需要任何构建步骤。以后改了 `index.html`，`git add -A && git commit -m "..." && git push` 就自动更新。

---

## 推送前最后自检（已自动跑过，全过）

- [x] `index.html` 单文件、零依赖、无外链
- [x] 无本机绝对路径、无邮箱、无密钥、无 `file://` 引用
- [x] 40 题数据镜像 `questions.json` 与页面一致
- [x] 双许可证齐全：`LICENSE`(MIT) + `LICENSE-CONTENT.md`(CC BY-NC-SA)
- [x] README 截图用的是英文名 `docs/02-quiz.png` 等（避免 Windows/Git 编码坑）

---

## 发布文案（可选，用于仓库简介 / 视频简介）

> 40 个场景，测你和 TA 之间那段还没名字的关系。单文件、零依赖、可离线，代码 MIT / 题目 CC BY-NC-SA 4.0。
> 在线玩：<Pages 链接>

---

## 本机环境诊断（2026-11-10，重要）

试过装 GitHub CLI 走一条龙，**卡住了**，原因不在项目，在网络：

- 系统记着一个代理 `127.0.0.1:7897`（WinINET 设置），但**代理软件当时没开**，端口没监听。
- 结果：`api.github.com` 偶尔可达，`github.com` 超时；winget 要从 GitHub 下载 release，直接卡死在下载阶段，`gh.exe` 没落盘。
- git 自身**没有**配代理（`git config --global http.proxy` 为空），所以 `git push` 会走直连，在国内网络下大概率失败。

**推送前先做两件事：**

1. 打开你的代理软件（让 `127.0.0.1:7897` 真正监听起来）。
2. 给 git 配上代理（端口按你软件实际设置改）：

```powershell
git config --global http.proxy  http://127.0.0.1:7897
git config --global https.proxy http://127.0.0.1:7897
# 不用了就取消：
# git config --global --unset http.proxy
# git config --global --unset https.proxy
```

配好后重新 `git push -u origin main`。如果代理软件提供的是 SOCKS5，把 `http://` 换成 `socks5://`。

> 注：`winget install GitHub.cli` 在代理恢复后可以重试；但**其实不装 gh 也能推**，走上面的「路径 A」即可，更省事。

---

## 关于商用授权

README 里写了：题目是 **CC BY-NC-SA**，别人可以转载、改编、做非商业版本，但接广告、卖课、付费小程序需要先开 issue 授权。你自己当然不受这个限制——你是著作权人，可以任意处置。

如果要改成更宽松（比如允许商用），把 `LICENSE-CONTENT.md` 和 README 里对应段落换掉即可，改完重新提交。