---
id: windows-terminal
title: Windows 终端美化
description: 记录 Windows Terminal、字体、Starship 与 PowerShell 配置。
status: Todo
created: null
updated: null
tags:
  - 开发工具
aliases: []
---

# Windows 终端美化 {#windows}

### 1. 装软件 & 装字体

1. **下载终端：** 去系统自带的“微软商店”搜索下载 `Windows Terminal`。
    
2. **下载内核：** 打开终端，复制运行：`winget install Microsoft.PowerShell`。
    
3. **安装字体：** * 点此下载：[JetBrainsMono Nerd Font 压缩包](https://github.com/ryanoasis/nerd-fonts/releases/latest/download/JetBrainsMono.zip)
    
    - 解压，全选里面的 `.ttf` 文件，**右键 -> 安装**。
        

### 2. 改 UI 设置 (必须重启终端并选黑色的 PowerShell 7)

1. 按 `Ctrl + ,` 打开设置。
    
2. **默认配置文件：** 改为黑底白字的 `PowerShell`。
    
3. **外观设置：** * 字体选：**`JetBrainsMono NFP`** (极其重要！没有 NFP 后缀会乱码)。
    
    - 背景图：上传二次元雨夜图，调低不透明度。保存。
        

### 3. 装引擎 & 插件

在终端**依次复制运行**以下 3 行代码（如遇提示全选 Y）：

PowerShell

```
winget install --id Starship.Starship
Install-Module -Name Terminal-Icons -Scope CurrentUser -Force
Install-Module -Name PSReadLine -Scope CurrentUser -Force
```

### 4. 写死配置文件 ($PROFILE)

1. 运行：`notepad $PROFILE` (弹窗点“是”)。
    
2. **清空里面所有内容，把下面这段完整复制进去，然后保存关闭：**
    

PowerShell

```shell
# 1. 自动化函数区

function rl { Write-Host "🔄 重载..." -ForegroundColor Cyan; . $PROFILE }

# 2. 插件与引擎启动区
Invoke-Expression (&starship init powershell)
Import-Module -Name Terminal-Icons
Set-PSReadLineOption -PredictionSource History
```

### 5. 套用“马卡龙连体箭头”主题

终端里依次运行下面 2 行代码：

PowerShell

```
mkdir -Force $HOME\.config
starship preset pastel-powerline -o "$HOME\.config\starship.toml"
```

### 6. 彻底重启

关掉终端，重新打开。

**全套雨夜马卡龙色命令行 + 自动化快捷键，瞬间点亮！** 搞定收工！
