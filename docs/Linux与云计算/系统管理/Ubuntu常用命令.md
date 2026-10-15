---
id: ubuntu-commands
title: Ubuntu 常用命令
description: 汇总 Ubuntu 服务、防火墙与磁盘管理中的常用命令。
status: Todo
created: null
updated: null
tags:
  - Linux与云计算
aliases: []
---

# Ubuntu 常用命令 {#ubuntu}

## 查看服务状态
```shell
sudo systemctl status apache2.service
```
## 防火墙相关
### 查看防火墙状态
```shell
sudo ufw status
# Status: inactive 关闭状态
# Status: active 开启状态
```
## 磁盘管理
首先查看Linux磁盘空间的具体使用情况, 确定空间不够用的磁盘所对应的mounted on目录
```bash
df -h
```
进入磁盘目录之后，使用如下命令逐级分析占用最大的目录，直到找到可以清理的文件和目录进入磁盘目录之后，使用如下命令逐级分析占用最大的目录，直到找到可以清理的文件和目录
```bash
du -h --max-depth=1
```
