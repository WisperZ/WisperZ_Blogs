---
id: rk3588-isulad
title: RK3588 固件与 iSulad
description: 记录 RK3588 固件、虚拟化镜像与 iSulad 容器环境部署。
status: Todo
created: null
updated: null
tags:
  - 项目实践
aliases: []
---

# RK3588 固件与 iSulad {#isula}

本手册整合了固件烧录、Hypervisor 镜像部署以及 iSulad 容器引擎的编译与运行全过程。

------

## 一、 硬件开发环境准备

在部署任何软件环境前，必须确保开发板固件为最新版本。

### 1.1 硬件环境

本次演示基于 **讯为 (Topeet) RK3588 开发板** 进行部署与验证。

购买链接：https://e.tb.cn/h.iTSbGR9Rdk33o3U?tk=eH4QUBKg8MD tG-#22>lD

| **项目**            | **规格参数**     | **备注**                           |
| ------------------- | ---------------- | ---------------------------------- |
| **核心板型号**      | Rockchip RK3588  | 八核 (4×Cortex-A76 + 4×Cortex-A55) |
| **运行内存 (RAM)**  | 16GB LPDDR4x     |                                    |
| **存储容量 (eMMC)** | 64GB             |                                    |
| **操作系统**        | Ubuntu 20.04 LTS |                                    |

### 1.2 驱动与工具安装

- **驱动程序**：前往 [Firefly 官网](https://www.t-firefly.com/doc/download/164.html) 下载并安装《RK 驱动助手》。
- **烧录工具**：下载并解压《RKDevTool 烧写工具》。

### 1.3 更新固件 (Loader 模式)

1. 使用 Type-C 线连接开发板与 PC。
2. 打开 `RKDevTool.exe`。
3. **进入下载模式**：长按开发板 **音量+** 键，同时重启上电，直到工具显示“发现一个 LOADER 设备”。
4. 在“升级固件”选项卡中点击“固件”，选择解压得到的 `update.img`。
5. 点击“升级”等待烧录完成。



------

## 二、 虚拟化环境部署 (Hypervisor+RTOS)

## 2.1 串口与网络配置

- **物理连接**：连接 RS232 串口线（波特率 115200）、type-c和网线。
- **进入 U-Boot**：开发板重启时迅速按 <kbd>Ctrl + C</kbd>。
- **网络环境**：确保开发板 IP 与 PC（TFTP 服务器）在同一网段。

## 2.2 镜像烧录与启动

1. 在 PC 上启动 `tftpd64.exe`，设置目录为镜像所在路径。

2. 在 U-Boot 命令行执行以下组合指令`tftp 0xe0000000 kernel.bin;tftp 0xe0a00000 rootserver.bin;tftp 0xe2a00000 system_init.bin;tftp 0xe6000000 guestos.bin;go 0xe0000000`下载并启动：

   ```shell
   tftp 0xe0000000 kernel.bin; 
   tftp 0xe0a00000 rootserver.bin; 
   tftp 0xe2a00000 system_init.bin; 
   tftp 0xe6000000 guestos.bin; 
   go 0xe0000000
   ```
   
3. **启动 Ubuntu**：在 ROTS中命令行执行：

   ```
   vm_create_run ubuntu
   ```

4. 通过adb连接到ubuntu确定设备的ip地址

    ```shell
    adb shell
    ```

5. 通过ssh服务连接到ubuntu中

    ```shell
    ssh topeet@x.x.x.x
    ```

​	用户名：`REPLACE_WITH_YOUR_VALUE`

​	密码：`REPLACE_WITH_YOUR_VALUE`

------

## 三、 iSulad 容器引擎部署

## 3.1 基础环境优化

**1. 软件源更新（国内镜像）**

修改 `/etc/apt/sources.list`，使用清华大学开源镜像站以加速下载。

```ini
# 示例：Ubuntu 20.04 (Focal)
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ focal main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ focal-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ focal-backports main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ focal-security main restricted universe multiverse

deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ focal main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ focal-updates main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ focal-backports main restricted universe multiverse
deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ focal-security main restricted universe multiverse
```

更新命令`sudo apt update && sudo apt upgrade -y`

**2. 检查内核支持**

确认内核是否支持 OverlayFS（iSulad 默认存储驱动）：

```shell
cat /proc/filesystems | grep overlay
# 输出 "nodev overlay" 即为正常
```

## 3.2 源码编译安装

针对 RK3588 内存压力，建议先开启 **Swap 交换区** 防止编译被杀：

```shell
sudo dd if=/dev/zero of=/swapfile bs=1M count=4096
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

**执行安装脚本：**

```shell
git clone https://gitee.com/openeuler/iSulad.git
cd iSulad/docs/build_docs/guide/script
sudo chmod +x ./install_iSulad_on_Ubuntu_20_04_LTS.sh
sudo ./install_iSulad_on_Ubuntu_20_04_LTS.sh
```

------

## 四、 iSulad 排障与调优

## 4.1 编译常见问题：Meson 版本过低

若系统自带 Meson 低于 0.61，需手动升级：

```shell
sudo apt remove --purge meson -y
sudo pip3 install --upgrade meson ninja
sudo ln -sf $(which meson) /usr/bin/meson
# 清理旧缓存
rm -rf /tmp/build_isulad/lxc/lxc-5.0.2/build
```

## 4.2 运行环境修复

**1. 缺失动态库修复**

```shell
echo "/usr/local/lib" | sudo tee /etc/ld.so.conf.d/isulad.conf
sudo ldconfig
```

**2. 语言包配置 (Locale)**

防止 iSulad 初始化环境失败：

```shell
sudo apt install -y locales
sudo locale-gen en_US.UTF-8
sudo update-locale LANG=en_US.UTF-8
export LANG=en_US.UTF-8
```

**3. 路径对齐（关键）**

```shell
sudo mkdir -p /etc/isulad /var/lib/isulad
sudo cp -r /usr/local/etc/isulad/* /etc/isulad/
sudo ln -sf /etc/isulad /etc/default/isulad
```

------

## 五、 服务管理与实战

## 5.1 Systemd 服务配置

创建 `/etc/systemd/system/isulad.service`：

```ini
[Unit]
Description=iSulad Application Container Engine
After=network.target

[Service]
ExecStart=/usr/local/bin/isulad -l INFO
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

**启动命令：**

```shell
sudo systemctl daemon-reload
sudo systemctl enable --now isulad
sudo systemctl start isulad
```

查看近50条日志：

```shell
# 查看最近 50 行日志
sudo journalctl -u isulad -n 50 --no-pager
```

## 5.2 常用操作指令

- **版本检查**：`isula version`

- **拉取镜像**（推荐使用加速器）：

  `sudo isula pull docker.m.daocloud.io/library/busybox:latest`

- **运行容器**：

  - 启动busybox
  
    `sudo isula run -it --rm docker.m.daocloud.io/library/busybox:latest sh`
  
  - 启动ubuntu
  
    `sudo isula run -it --rm docker.m.daocloud.io/library/ubuntu:latest bash`
  

------

## 六、 彻底卸载清理

若需重新安装，请执行：

```shell
# 1. 停止服务
sudo systemctl stop isulad
sudo systemctl disable isulad
sudo killall -9 isulad 2>/dev/null

# 2. 移除系统服务定义
sudo rm -f /etc/systemd/system/isulad.service
sudo systemctl daemon-reload

# 3. 移除二进制文件与配置
sudo rm -f /usr/local/bin/isula*
sudo rm -rf /etc/isulad /etc/default/isulad /usr/local/etc/isulad

# 4. 抹除所有镜像与容器数据 (慎用)
sudo rm -rf /var/lib/isulad /var/run/isulad /var/run/isulad.sock
```

------

Last Updated: 2026-03-19
Device: iTOP-RK3588
