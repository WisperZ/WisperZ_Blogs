---
id: openvela-setup
title: OpenVela 环境与源码
description: 记录 OpenVela 开发依赖、源码同步与环境准备。
status: Todo
created: '2024-12-12'
updated: '2024-12-12'
tags:
  - 嵌入式开发
  - OpenVela
  - 操作系统
aliases: []
---

# OpenVela 环境与源码 {#_1}

## OpenVela 开发环境部署及源码下载

### 开发环境
操作系统使用 `Ubuntu 22.04.3 LTS WSL`
### 安装必备的软件包
使用 Ubuntu 22.04 版本编译 openvela。运行以下命令，在 Ubuntu 22.04 版本上安装必备的软件包：
```shell
sudo apt install \
bison flex gettext texinfo libncurses5-dev libncursesw5-dev xxd \
git gperf automake libtool build-essential gperf genromfs \
libgmp-dev libmpc-dev libmpfr-dev libisl-dev binutils-dev libelf-dev \
libexpat1-dev gcc-multilib g++-multilib picocom u-boot-tools util-linux \
dfu-util libx11-dev libxext-dev net-tools pkgconf unionfs-fuse zlib1g-dev \
libusb-1.0-0-dev libv4l-dev libuv1-dev npm nodejs nasm yasm libdivsufsort-dev \
libc++-dev libc++abi-dev libprotobuf-dev protobuf-compiler protobuf-c-compiler mtools
```
### 安装 Repo
运行以下命令安装 Repo 启动器:
```shell
curl https://storage.googleapis.com/git-repo-downloads/repo > repo
chmod +x repo
sudo mv repo /usr/local/bin/
```
Repo 启动器会提供一个 Python 脚本，该脚本可以初始化检出，并可以下载完整的 Repo 工具。

### 安装 KConfig frontend
openvela 配置系统使用 [KConfig](https://gitee.com/link?target=https%3A%2F%2Fwww.kernel.org%2Fdoc%2FDocumentation%2Fkbuild%2Fkconfig-language.txt) ，作为 kconfig-frontends 软件包的一部分，KConfig 通过一系列基于交互式菜单的前端对系统进行配置。使用软件包还是从源码构建取决于当前的操作系统，源码地址位于 [NuttX tools repository](https://gitee.com/link?target=https%3A%2F%2Fbitbucket.org%2Fnuttx%2Ftools%2Fsrc%2Fmaster%2Fkconfig-frontends%2F)。
```shell
sudo apt install kconfig-frontends
```
### 安装 Python
```shell
sudo apt install python3 python3-pip python-is-python3
```
### 安装 Python 包

```
sudo pip3 install kconfiglib pyelftools cxxfilt
```

## 下载 openvela 源码
openvela 源码位于由 [GitHub](https://gitee.com/link?target=https%3A%2F%2Fgithub.com%2Fopen-Vela) 或 [Gitee](https://gitee.com/open-vela) 托管的 Git 仓库中。

### 初始化 Repo 客户端

1. 创建并导航到工作目录：
    
    ```shell
    mkdir vela-opensource
    cd vela-opensource
    ```
    
2. 初始化用于操作源码的工作目录:
    
    - Github（需注册公钥，请参考[Github文档](https://gitee.com/link?target=https%3A%2F%2Fdocs.github.com%2Fen%2Fauthentication%2Fconnecting-to-github-with-ssh%2Fadding-a-new-ssh-key-to-your-github-account)）： 
        ```shell
        # Install Git LFS (Large File Storage) for managing large files
        sudo apt install git-lfs
        git lfs install
        git lfs --version
        
        repo init --partial-clone -u git@github.com:open-vela/manifests.git -b dev -m openvela.xml --git-lfs
        ```
    - Gitee（需注册公钥，请参考[码云文档](https://gitee.com/help/articles/4191)）：
        ```shell
        # Install Git LFS (Large File Storage) for managing large files
        sudo apt install git-lfs
        git lfs install
        git lfs --version
        
        repo init --partial-clone -u git@gitee.com:open-vela/manifests.git -b dev -m openvela.xml --git-lfs
        ```
        

### 下载 openvela 源码

运行如下命令下载 openvela 源码树至工作目录：

```
repo sync -c -j$(nproc)
```
