---
id: git-reference
title: Git 速查
description: 保留分支重命名、用户配置和分支恢复的简短速查。
status: Todo
created: null
updated: null
tags:
  - 开发工具
aliases: []
---

# Git 速查 {#git}

完整操作整理见 [Git 常用操作](Git常用操作.md)。

## 1.分支重命名

**注：**想要修改分支名，我们需要将远端的分支拉下来，重新修改。

旧分支：oldBranch
新分支：newBranch
**步骤：**
1. 先拉一下仓库，保证最新。
```powershell
git pull
```

2. 先将本地分支重命名。
```powershell
git branch -m oldBranch newBranch
```

3. 删除远端分支（如果分支尚未传到远端，则可以跳过该步骤）
```powershell
git push --delete origin oldBranch
```

4. 将重命名之后的分支推送到远端
```powershell
git push origin newBranch
```

5. 把修改后的本地分支和远程分支关联
```powershell
git branch --set-upstream-to=origin/newBranch
```
## 2.一些常用的配置
#### 中文乱码
```powershell
git config --global core.quotepath false
```
#### 配置用户名和邮箱
```powershell
git config --global user.name "Your Name"
git config --global user.email "user@example.com"
```
## 3.恢复git被删除的本地分支
1. 查看操作记录
```powershell
git reflog show --date=iso
```
2. 找到对应分支最后一个提交记录，复制第一个7位的字符串
3. 恢复分支
```powershell
git checkout -b xxxx 1234567
```
