# 仓库搭建与推送手册

> 面向：马子尊（项目负责人）及全体成员
> 目标：把本地已就绪的仓库推到 GitHub，并把 5 个人的分支、Issue、PR 流程跑起来
> 预计耗时：负责人 15 分钟，每位成员 5 分钟

---

## 〇、当前本地状态（已完成，无需重做）

本地仓库位于 `two-complement-simulator/`，已经完成：

| 项 | 状态 |
| :--- | :--- |
| `git init` | ✅ 已完成，主分支名 `main` |
| 首次提交 | ✅ 2 个提交（初始化 + .gitattributes） |
| 成员分支 | ✅ 7 条分支已建好，均指向 `main` 最新提交 |
| `.gitignore` / `.gitattributes` | ✅ 已配置（含 PNG 二进制保护、换行符统一） |
| 远程仓库 | ❌ **尚未配置**（本手册要做的部分） |

当前分支：

```text
* main
  chore/scaffold          马子尊：仓库初始化与规范
  feat/engine             马子尊：编排层与入口
  feature/core-logic      成员B：核心算法
  feature/ui-layout       成员C：界面布局
  feature/canvas-render   成员D：Canvas 渲染
  docs/feature-proposal   成员E：设计文档
  test/qa-suite           成员E：测试
```

---

## 一、前置：配置 Git 身份

**注意**：本机此前没有配置全局 `user.name` / `user.email`。仓库内已临时设置为 `马子尊 / 2610250212@users.noreply.github.com`，**请改成你自己的真实信息**，否则 GitHub 上提交不会关联到你的头像。

```bash
# 全局配置（推荐，一次配好所有仓库）
git config --global user.name "你的名字"
git config --global user.email "你的GitHub邮箱或用户名@users.noreply.github.com"

# 让 git 正确显示中文文件名（Windows 必配）
git config --global core.quotepath false

# 检查
git config --global --list
```

> 邮箱建议用 GitHub 提供的 noreply 地址：GitHub → Settings → Emails → *Keep my email addresses private*，页面会给出 `12345678+username@users.noreply.github.com` 这种格式。用它既保护隐私，也能正确关联提交。

---

## 二、在 GitHub 上创建空仓库

1. 打开 <https://github.com/new>
2. 填写：

   | 字段 | 值 |
   | :--- | :--- |
   | Repository name | `twos-complement-simulator` |
   | Description | 补码加减法运算模拟器 · 求补过程与溢出判定可视化（计算机基础课程大作业） |
   | Visibility | **Public**（推荐，便于教师查看；Private 需主动给教师加权限） |
   | Initialize this repository with | **全部不勾选**（README / .gitignore / License 都不要勾） |

3. 点 **Create repository**。

> ⚠️ **关键**：不要勾选 "Add a README file"。本地已有内容，勾了会产生一个无关的初始提交，推送时必然冲突。

---

## 三、关联远程并推送 main

```bash
cd two-complement-simulator

# 关联远程（把 <用户名> 换成你的 GitHub 用户名）
git remote add origin https://github.com/<用户名>/twos-complement-simulator.git

# 确认
git remote -v

# 首次推送
git push -u origin main
```

### 认证说明（2021 年后 GitHub 已不支持密码）

推送时会要求输入用户名和密码，**密码处必须填 Personal Access Token**：

1. 打开 <https://github.com/settings/tokens> → *Generate new token (classic)*
2. Note 填 `twos-complement-simulator`，Expiration 选 90 天
3. 勾选 **`repo`** 权限（整块勾上）
4. 生成后**立刻复制**（只显示一次），在终端粘贴到密码位置
5. Git for Windows 自带 Credential Manager，会记住凭据，**只需一次**

> 也可以改用 SSH：`git remote set-url origin git@github.com:<用户名>/twos-complement-simulator.git`，需先在 GitHub 添加本机公钥（`ssh-keygen -t ed25519` 后把 `~/.ssh/id_ed25519.pub` 内容贴到 Settings → SSH keys）。

---

## 四、推送 7 条分支

```bash
# 一次推送全部分支（本地分支名 -> 同名远程分支）
git push origin --all

# 验证
git branch -r
```

期望看到：

```text
origin/main
origin/chore/scaffold
origin/feat/engine
origin/feature/canvas-render
origin/feature/core-logic
origin/feature/ui-layout
origin/docs/feature-proposal
origin/test/qa-suite
```

> **为什么先建分支再推**：让每位成员进仓库就能 `git switch feature/xxx` 直接开工，不用自己想分支名；同时教师打开仓库首页就能看到分工结构，协作流程这一项直接得分。

---

## 五、配置仓库（负责人 5 分钟）

### 5.1 邀请成员

Settings → **Collaborators** → *Add people* → 输入 4 位成员的 GitHub 用户名 → 角色选 **Write**。
成员会收到邮件邀请，**必须点接受**，否则无法推送。

### 5.2 保护 main 分支

Settings → **Branches** → *Add branch protection rule*：

| 选项 | 值 |
| :--- | :--- |
| Branch name pattern | `main` |
| Require a pull request before merging | ✅ |
| Require approvals | ✅ 1 |
| Do not allow bypassing the above settings | ✅（可选，严格模式） |

> **免费版限制**：Private 仓库可能提示需要升级到 Pro 才能用分支保护。遇到这种情况有两个选择：① 把仓库改为 Public；② 放弃强制保护，改用团队纪律（"谁直推 main 谁请奶茶"），并在 README 里写明"main 不接受直接 push"。

### 5.3 建标签与里程碑

Issues → Labels → *New label*，依次建：

| 标签 | 颜色 | 说明 |
| :--- | :--- | :--- |
| `core` | `#2E7D32` | 核心算法 |
| `ui` | `#1565C0` | 界面交互 |
| `render` | `#6A1B9A` | Canvas 渲染 |
| `docs` | `#546E7A` | 文档 |
| `test` | `#EF6C00` | 测试 |
| `blocked` | `#C62828` | 被阻塞 |

Issues → Milestones → *New milestone*：`M1 文档`、`M2 算法`、`M3 界面`、`M4 交付`。

### 5.4 建看板

Projects → *New project* → Board 视图 → 列：`Todo` / `Doing` / `Review` / `Done`。
把 [`Team_Task_Allocation.md`](Team_Task_Allocation.md) 第 5.3 节的 20 个 Issue 一次性建进去（可以批量粘贴标题）。

---

## 六、每位成员的开工流程

```bash
# 1. 克隆（只需一次）
git clone https://github.com/<用户名>/twos-complement-simulator.git
cd twos-complement-simulator

# 2. 确认身份
git config user.name && git config user.email

# 3. 切到自己的分支
git switch feature/core-logic      # 换成自己的分支名

# 4. 每天开工前同步主干
git pull --rebase origin main
```

### 提交与推送

```bash
git status                          # 看改了什么
git add src/core/negate.py          # 只加自己的文件
git commit -m "feat(core): 实现求补算法并返回逐步 trace"
git push                            # 首次可能需要 -u origin feature/core-logic
```

### 提 PR

1. 推送后终端会给出一个 `Create a pull request` 链接，点它；
2. 标题同 commit 规范，描述里写 `Closes #6`（对应 Issue 号）；
3. 勾选自测清单，界面类改动**必须附截图**；
4. 点 **Create pull request**，然后在群里 @ 负责人来 Review。

---

## 七、冲突演练（作业硬性要求，务必留档）

> 目的：真实触发一次 `<<<<<<< HEAD` 并解决，截图存档。
> 冲突点：`src/ui/app.py` 的 `_init_window()`。

### 7.1 制造冲突

**成员C（feature/ui-layout）**

```bash
git switch feature/ui-layout
git pull --rebase origin main
# 编辑 src/ui/app.py，把窗口尺寸改为 1280x800：
#   self.root.geometry("1280x800")
git add src/ui/app.py
git commit -m "feat(ui): 主窗口尺寸调整为 1280x800"
git push
```

→ 在 GitHub 上给这条分支开 PR，负责人合并进 `main`。

**成员D（feature/canvas-render）**

```bash
git switch feature/canvas-render
git pull --rebase origin main
# 编辑同一函数，追加画布参数：
#   self.canvas_w, self.canvas_h = 700, 420
git add src/ui/app.py
git commit -m "feat(render): 新增画布尺寸参数"
git push
```

**关键一步**：成员C 的 PR 先合并后，成员D 再拉取主干，冲突才会真正发生：

```bash
git fetch origin
git merge origin/main
```

预期输出：

```text
Auto-merging src/ui/app.py
CONFLICT (content): Merge conflict in src/ui/app.py
Automatic merge failed; fix conflicts and then commit the result.
```

### 7.2 解决冲突

打开 `src/ui/app.py`，会看到：

```text
<<<<<<< HEAD
        self.root.geometry("1280x800")
=======
        self.root.geometry("1280x800")
        self.canvas_w, self.canvas_h = 700, 420
>>>>>>> origin/main
```

协商结论：**两个都保留**（新尺寸 + 新参数）。改完删掉三行冲突标记：

```python
        self.root.geometry("1280x800")
        self.canvas_w, self.canvas_h = 700, 420
```

```bash
git add src/ui/app.py
git commit -m "fix(ui): 解决 main 与 feature/canvas-render 在窗口初始化参数上的冲突"
git push
```

### 7.3 留档（评分要用）

| 材料 | 存放位置 |
| :--- | :--- |
| 冲突标记截图（含 VS Code 高亮） | `docs/images/conflict-marker.png` |
| 解决后 `git log --graph --oneline --all` 截图 | `docs/images/conflict-graph.png` |
| 冲突说明文字 | 本文件第 7 节 + README 第五节 |

```bash
git log --graph --oneline --all | Out-String | Set-Content docs/images/git-graph.txt
```

---

## 八、常见问题

| 现象 | 原因 | 解决 |
| :--- | :--- | :--- |
| `Support for password authentication was removed` | 用了账号密码而不是 Token | 生成 PAT，密码处填 Token |
| `remote: Permission to xxx denied to yyy` | 未接受协作者邀请，或 Token 无 `repo` 权限 | 检查邮件邀请；重新生成带 `repo` 的 Token |
| `Updates were rejected because the remote contains work...` | 远程有你本地没有的提交（通常是建仓时勾了 README） | `git pull --rebase origin main` 后再推；或 `git push --force-with-lease`（**仅限自己的分支**） |
| `fatal: refusing to merge unrelated histories` | 本地与远程各自独立初始化 | `git pull origin main --allow-unrelated-histories` |
| 中文文件名显示成 `\346\226\207...` | Git 默认转义非 ASCII | `git config --global core.quotepath false` |
| 每次提交都提示 `LF will be replaced by CRLF` | 换行符配置 | 已通过 `.gitattributes` 统一，若仍提示可忽略，或设 `git config core.autocrlf false` |
| 提交后 GitHub 上不显示自己的头像 | `user.email` 与账号邮箱不匹配 | 改成 GitHub 的 noreply 邮箱后 `git commit --amend --reset-author` |
| `error: src refspec main does not match any` | 本地还没有提交 | 先 `git add -A && git commit -m "..."` |
| 大文件推送失败（>100MB） | 误提交了 exe / 视频 | 从历史中移除，或改用 Git LFS；本仓库已在 `.gitignore` 排除 exe |
| 分支保护后自己推不上去 | 规则生效 | 走 PR 流程合并，这正是规则的目的 |

---

## 九、交作业前检查清单

- [ ] 仓库 Public（或已给教师加 Collaborator 权限）
- [ ] `main` 上有 **≥ 5 个已合并的 PR**，每个都有 Review 记录
- [ ] 5 位成员各自分支上有 **≥ 8 次有意义的提交**，提交信息符合 `type(scope): 描述`
- [ ] 7 条分支在远程可见，命名与分工表一致
- [ ] 有一次完整的冲突解决记录（截图 + 说明 + 合并提交）
- [ ] `README.md` 含安装运行、截图、贡献者、开源协议
- [ ] `Project_Requirements_and_Design.md` 含多级标题、表格、图片、代码块
- [ ] `AI_Prompts_Log.md` 含 15 条记录（5 人 × 3 条），且至少 3 条记录了 AI 出错与修正
- [ ] `python main.py` 在干净环境可运行（无第三方依赖）
- [ ] `pytest tests/ -v` 全绿
- [ ] Issue 与 Milestone 状态已更新为 Done

---

## 十、附：改用 Gitee 的等价操作

作业允许使用 Gitee。如果 GitHub 访问不稳定：

```bash
# 1. 在 https://gitee.com/projects/new 创建空仓库（同样不勾选初始化）
# 2. 改远程地址
git remote set-url origin https://gitee.com/<用户名>/twos-complement-simulator.git
# 3. 推送
git push -u origin main
git push origin --all
```

其余流程（协作者邀请、分支保护、PR、Issue）与 GitHub 基本一致，界面名称略有差异：Gitee 的 PR 叫 **Pull Request** / **合并请求**，分支保护在 *管理 → 保护分支设置*。

---

<div align="center">

**遇到本手册没覆盖的问题，先在群里贴报错原文再讨论——不要自己猜着改。**

</div>
