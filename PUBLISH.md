# 发布指南 · 把仓库推到 GitHub 并开启 Pages

## ✅ 已完成（2026-11-10）

| 项目 | 值 |
|---|---|
| GitHub 账号 | **xiaobaigyt**（注意：不是从 noreply 邮箱推测的 `yb2460`） |
| 仓库 | https://github.com/xiaobaigyt/aimei-checklist （Public） |
| 在线版 | **https://xiaobaigyt.github.io/aimei-checklist/** （Pages 状态 `built`，HTTP 200 已验证） |
| 分支 | `main`，remote `origin` |

---

以下保留为「下次从头发布」的通用步骤。本次实际踩的坑见文末。

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
> 在线玩：https://xiaobaigyt.github.io/aimei-checklist/

---

## 本机环境诊断（2026-11-10，实际踩坑记录）

本次发布真正卡住的不是项目，是**代理 + HTTP/2 + 证书吊销检查**三件事叠在一起。

### 1. 代理软件必须真的在监听

系统 WinINET 记着 `127.0.0.1:7897`，但代理软件没开时端口不监听 → `github.com:443` 直连必超时，`winget install GitHub.cli` 卡死在下载。
**判定方法**：`Get-NetTCPConnection -LocalPort 7897 -State Listen`，没输出就是没开。

### 2. 它是 HTTP CONNECT 代理，不是纯 SOCKS5

`curl -x http://127.0.0.1:7897 https://github.com` 能拿 200；
`--socks5-hostname` 也能通但慢。**给 git 用 `http.proxy=http://127.0.0.1:7897` 即可。**

### 3. 必须强制 HTTP/1.1（最关键）

git 默认 ALPN 会协商 `h2`，经这个代理时 TLS 握手后立刻 `SSL routines::unexpected eof while reading`。

```powershell
git config --local http.proxy   http://127.0.0.1:7897
git config --local http.version HTTP/1.1     # 少了这句必失败
```

Go 程序（gh）不吃 git 的配置，要单独设环境变量：

```powershell
$env:GODEBUG = 'http2client=0'
$env:HTTPS_PROXY = 'http://127.0.0.1:7897'
$env:HTTP_PROXY  = 'http://127.0.0.1:7897'
```

### 4. Windows schannel 的证书吊销检查

curl 有时报 `CRYPT_E_REVOCATION_OFFLINE`——代理下查不到 CRL/OCSP 就拒绝握手。
命令行加 `--ssl-no-revoke`；Python 用 `ssl.CERT_NONE` 自建 context。

### 5. 代理整体不稳，重试是常态

`api.github.com` / Pages 站点会间歇性 SSL EOF。本次 Pages 的 POST 是**第 4 次重试**才成功。
写脚本务必带 3–5 次重试 + 退避，不要一次失败就下结论。

### 6. 认证的坑

- gh 2.103 已**移除 `--device` 标志**；`gh auth login` 默认是浏览器流程，非交互 shell 里弹不出来。
- 设备流能出码（`gh auth login --clipboard` 会打印一次性码），但 gh 把码输出到终端容易被缓冲；用 `cmd /c` 直接跑才看得到。
- 用户授权后 gh 写凭据，`gh auth status` 一度报 `keyring token invalid`，但 `gh auth token` 能取到可用的 `gho_` token。
- **最稳的推送方式**：token 内嵌 URL，绕开 GCM：

```powershell
$tok = (& 'C:\Program Files\GitHub CLI\gh.exe' auth token).Trim()
git -c credential.helper= -c http.proxy=http://127.0.0.1:7897 -c http.version=HTTP/1.1 `
    push "https://xiaobaigyt:$tok@github.com/xiaobaigyt/aimei-checklist.git" main
```

> ⚠️ 这条命令 git 会把含 token 的 URL 回显、并可能写进 `branch.main.remote`。
> 用完立刻清：`git config --unset branch.main.remote` / `branch.main.merge`，再手工指回 `origin`。
> 本次已清理干净，`git config --local --list` 无 token 残留。

### 7. 账号名别靠猜

`git config user.email` 是 `yb2460@users.noreply.github.com`，但设备流实际登录的是 **`xiaobaigyt`**。
以 `gh auth login` 成功后打印的 `Logged in as ...` 为准。

---

## 关于商用授权

README 里写了：题目是 **CC BY-NC-SA**，别人可以转载、改编、做非商业版本，但接广告、卖课、付费小程序需要先开 issue 授权。你自己当然不受这个限制——你是著作权人，可以任意处置。

如果要改成更宽松（比如允许商用），把 `LICENSE-CONTENT.md` 和 README 里对应段落换掉即可，改完重新提交。