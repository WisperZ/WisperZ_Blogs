---
id: wsl-cubic
title: WSL2 安装 Cubic
description: 记录 Cubic 安装和图形环境依赖的排障方法。
status: Todo
created: null
updated: null
tags:
  - Linux与云计算
aliases: []
---

# WSL2 安装 Cubic {#wsl2cubic}

安装命令如下：
```shell
    $ sudo apt-add-repository universe
    $ sudo apt-add-repository ppa:cubic-wizard/release
    $ sudo apt update
    $ sudo apt install --no-install-recommends cubic
```
执行cubic报错
```shell
Settings schema 'org.gnome.desktop.interface' is not installed
```
执行
```shell
sudo apt install gedit
```
