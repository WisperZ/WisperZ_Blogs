---
id: wsl-setup
title: WSL 备份与配置
description: 记录 WSL 导出恢复、Ubuntu、终端与开发环境配置。
status: Todo
created: null
updated: null
tags:
  - Linux与云计算
aliases: []
---

# WSL 备份与配置 {#wsl}

## WSL 备份和恢复
备份WSL
```shell
 wsl --export Ubuntu-22.04 E://WSL//ubuntu-22.04.tar
```
恢复
```shell
wsl --import  Ubuntu-22.04 E:\WSL\Ubuntu-22.04\ E:\WSL\ubuntu-22.04.tar
```
设置默认登录用户
```shell
 ubuntu2204.exe config --default-user yuh
```
## Ubuntu配置
阿里源
```shell
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ jammy-proposed main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ jammy-backports main restricted universe multiverse
```
中文环境
安装中文包
```shell
sudo apt install language-pack-zh-hans
```
首先运行如下命令配置 locale 
```shell
sudo vi /etc/locale.gen
```
找到 ***zh_CN.UTF-8 UTF-8*** 并取消注释，然后保存并退出。
```shell
locale.gen...
# zh_CN.GBK GBK
zh_CN.UTF-8 UTF-8
# zh_HK BIG5-HKSCS
 
此处省略200行 ...
```
 运行命令 **sudo locale-gen** 进行编译
```shell
$ sudo locale-gen
Generating locales (this might take a while)...
  en_US.UTF-8... done
  zh_CN.UTF-8... done
  zh_SG.UTF-8... done
Generation complete.
```
设置默认语言是中文
编辑文件 /etc/default/locale
```shell
sudo vi /etc/default/locale
```
将文件内容更改如下，重启 [wsl](https://so.csdn.net/so/search?q=wsl&spm=1001.2101.3001.7020) 生效。
```shell
LANG=zh_CN.UTF-8
LANGUAGE="zh_CN:zh:en_US:en"
```
## zsh
安装zsh
```shell
sudo apt install zsh
chsh -s /bin/zsh #将zsh设置成默认shell（不设置的话启动zsh只有直接zsh命令即可）
```
安装oh-my-zsh
```shell
sh -c "$(curl -fsSL https://gitee.com/shmhlsy/oh-my-zsh-install.sh/raw/master/install.sh)"
```
安装插件
```shell
#zsh-autosuggestions 命令行命令键入时的历史命令建议
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
#zsh-syntax-highlighting 命令行语法高亮插件
git clone https://gitee.com/Annihilater/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```

## 工作环境
```shell
sudo apt-get install make libncurses5-dev  bison flex
```
