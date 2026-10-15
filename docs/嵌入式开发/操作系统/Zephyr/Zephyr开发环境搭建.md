---
id: zephyr-setup
title: Zephyr 开发环境搭建
description: 记录 Windows 环境中的 Zephyr 工具链、West 与编译流程。
status: Todo
created: null
updated: null
tags:
  - 嵌入式开发
aliases: []
---

# Zephyr 开发环境搭建 {#_1}

本指南严格遵循 Zephyr 官方 v3.x+ 手册流程，并针对中国网络环境进行了镜像源适配，解决 GitHub 访问超时问题。

---

## 1. 系统预准备 (Pre-requisites)

### 1.1 开启长路径支持 (必做)
Zephyr 的编译路径通常很深，Windows 默认限制会导致编译失败。
1. 按 `Win + R`，输入 `regedit`。
2. 导航至：`HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem`。
3. 找到 `LongPathsEnabled`，将其值修改为 `1`。

### 1.2 安装 Chocolatey 包管理器
以 **管理员权限** 打开 PowerShell，运行以下命令安装 Chocolatey：

    Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

---

## 2. 安装核心依赖工具 (Step 1: Install Dependencies)

通过 Chocolatey 自动安装 Git, Python, CMake 和 Ninja。请在管理员 PowerShell 中运行：

    choco install cmake --installargs 'ADD_CMAKE_TO_PATH=System'
    choco install git python ninja

---

## 3. 初始化 Zephyr 工作空间 (Step 2: Get Zephyr)

**注意**：此步骤已替换为 **Gitee 镜像源**，解决国内 `west init` 访问 GitHub 443 端口超时的问题。

### 3.1 安装 West 管理工具

    pip3 install west

### 3.2 初始化仓库 (使用镜像)
请选择一个非系统盘目录（如 `D:\`），避免权限问题。

    # 创建目录并进入
    mkdir D:\zephyrproject
    cd D:\zephyrproject

    # 使用 Gitee 镜像源初始化 manifest
    west init -m https://gitee.com/mirrors/zephyr.git

### 3.3 修改配置并同步 (关键步骤)
防止 update 时子模块去拉取 GitHub。

    # 1. 将子项目下载源强制指向国内镜像
    west config manifest.remotes.zephyr.url https://gitee.com/mirrors/zephyr.git

    # 2. 执行同步（下载 HAL 库、驱动、协议栈等，耗时较长）
    west update

---

## 4. 安装 Python 依赖 (Step 3: Python Requirements)

安装 Zephyr 编译脚本所需的 Python 库：

    west zephyr-export
    pip3 install -r D:\zephyrproject\zephyr\scripts\requirements.txt

---

## 5. 安装 Zephyr SDK (Step 4: Install SDK)

SDK 包含编译器（GCC）和调试工具，需单独安装。

1. **下载**: 访问 [Zephyr SDK Releases](https://github.com/zephyrproject-rtos/sdk-ng/releases) 下载最新版 `zephyr-sdk-x.x.x_windows-x86_64.7z` (约 1GB)。
2. **解压**: 建议解压至 `C:\zephyr-sdk` (路径不要包含空格或中文)。
3. **注册**: 进入解压后的目录，右键以 PowerShell 运行 `./setup.ps1`。
   * 提示安装驱动时选择 `Y`。
   * 提示注册环境变量时选择 `Y`。

---

## 6. VS Code 深度集成 (推荐)

使用官方插件将 VS Code 变为全功能 IDE。

1. 在 VS Code 扩展市场搜索并安装：**nRF Connect for VS Code Extension Pack**。
2. 安装完成后，点击左侧出现的 **"n"** 图标。
3. 在 **Manage SDKs** 区域，点击 **Add SDK**。
4. 选择 **"Select an existing SDK"**，路径指向你的 `D:\zephyrproject`。
   * 插件会自动检测 Toolchain (C:\zephyr-sdk) 和 CMake。

---

## 7. 编译验证 (Step 5: Build Blinky)

验证环境是否正常，以 **Raspberry Pi Pico** 为例。

### 命令行方式：

    cd D:\zephyrproject\zephyr

    # 针对 Pico 编译点灯程序
    west build -p always -b rpi_pico samples/basic/blinky

    # 产物路径: build/zephyr/zephyr.uf2 (直接拖入 Pico 磁盘即可)

### VS Code 方式：
1. 点击 "n" 图标 -> **Create a new application** -> **Copy a sample**。
2. 搜索 `blinky` 并创建。
3. 在 **Build Configuration** 中选择 Board: `rpi_pico`。
4. 点击 **Build**。

---

## 8. 针对 GD32VW553 (RISC-V) 的开发者建议

由于 GD32VW553 是较新的 RISC-V 芯片，Zephyr 官方支持可能还在完善中。

1. **检查 RISC-V 工具链**: 确保在 SDK 安装阶段通过了 RISC-V 编译器的检查。
2. **DeviceTree**: 该芯片的定义通常位于 `zephyr/boards/gigadevice/` 或 `zephyr/dts/riscv/gigadevice`。
3. **Overlay 技巧**: 如果板载 LED 引脚与默认不同，请在项目根目录创建 `boards/gd32vw553.overlay` 文件重定义引脚：

    /* boards/gd32vw553.overlay 示例 */
    / {
        aliases {
            led0 = &my_led;
        };
    };
    
    &gpioa {
        status = "okay";
        /* 假设 LED 接在 PA1 */
        my_led: led_pa1 {
            gpios = <&gpioa 1 GPIO_ACTIVE_HIGH>;
        };
    };
