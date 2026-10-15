---
id: riscv-environment
title: RISC-V 开发环境搭建
description: 记录 RISC-V 工具链准备、源码编译与 QEMU 运行步骤。
status: Done
created: '2025-04-18'
updated: '2025-04-18'
tags:
  - 项目实践
aliases: []
---

# RISC-V 开发环境搭建 {#risc-v}

## 配置编译环境

下载交叉编译工具链

执行命令
```bash
git clone https://github.com/riscv/riscv-gnu-toolchain
```
等待克隆完成

依赖安装
```bash
sudo apt-get install autoconf automake autotools-dev curl python3 python3-pip python3-tomli libmpc-dev libmpfr-dev libgmp-dev gawk build-essential bison flex texinfo gperf libtool patchutils bc zlib1g-dev libexpat-dev ninja-build git cmake libglib2.0-dev libslirp-dev
```

执行配置命令, 其中 `--prefix=xxx` 路径需要自己确认
./configure --prefix=/home/os/local/riscv64 --enable-multilib
```bash
#全量编译
./configure --prefix=/home/os/local/riscv64 --enable-multilib
```
等待检查完成，执行编译命令 `make`


## 获取源码

通过 git 下载 `freeRTOS` 的源码

```bash
git clone https://github.com/FreeRTOS/FreeRTOS.git --recurse-submodules
```

等待源码下载完成

## 编译

打开目录 `FreeRTOS/FreeRTOS/Demo/RISC-V-Qemu-virt_GCC`，本文使用 qemu 版本做编译

执行 `make` 如果上述所有过程都没有出错，则可以成功编译该版本，输出如下
```bash
riscv64-unknown-elf-gcc -nostartfiles -Tfake_rom.lds -march=rv32imac -mabi=ilp32 -mcmodel=medany -Xlinker --gc-sections -Xlinker --defsym=__stack_size=300 -Xlinker -Map=build/RTOSDemo.map build/main.o build/main_blinky.o build/riscv-virt.o build/ns16550.o build//home/os/workspace/Edge/FreeRTOS/FreeRTOS/Demo/Common/Minimal/EventGroupsDemo.o build//home/os/workspace/Edge/FreeRTOS/FreeRTOS/Demo/Common/Minimal/TaskNotify.o build//home/os/workspace/Edge/FreeRTOS/FreeRTOS/Demo/Common/Minimal/TimerDemo.o build//home/os/workspace/Edge/FreeRTOS/FreeRTOS/Demo/Common/Minimal/blocktim.o build//home/os/workspace/Edge/FreeRTOS/FreeRTOS/Demo/Common/Minimal/dynamic.o build//home/os/workspace/Edge/FreeRTOS/FreeRTOS/Demo/Common/Minimal/recmutex.o build//home/os/workspace/Edge/FreeRTOS/FreeRTOS/Source/event_groups.o build//home/os/workspace/Edge/FreeRTOS/FreeRTOS/Source/list.o build//home/os/workspace/Edge/FreeRTOS/FreeRTOS/Source/queue.o build//home/os/workspace/Edge/FreeRTOS/FreeRTOS/Source/stream_buffer.o build//home/os/workspace/Edge/FreeRTOS/FreeRTOS/Source/tasks.o build//home/os/workspace/Edge/FreeRTOS/FreeRTOS/Source/timers.o build//home/os/workspace/Edge/FreeRTOS/FreeRTOS/Source/portable/MemMang/heap_4.o build//home/os/workspace/Edge/FreeRTOS/FreeRTOS/Source/portable/GCC/RISC-V/port.o build/start.o build/vector.o build//home/os/workspace/Edge/FreeRTOS/FreeRTOS/Source/portable/GCC/RISC-V/portASM.o -o build/RTOSDemo.axf
```

## qemu 虚拟机运行镜像

执行命令
```bash
qemu-system-riscv32 -nographic -machine virt -net none \
  -chardev stdio,id=con,mux=on -serial chardev:con \
  -mon chardev=con,mode=readline -bios none \
  -smp 4 -kernel ./build/RTOSDemo.axf
```

可以看到如下输出
```bash
Hello FreeRTOS!
0: Tx: Transfer1
0: Rx: Blink1
0: Tx: Transfer2
0: Rx: Blink2
0: Tx: Transfer1
0: Rx: Blink1
0: Tx: Transfer2
0: Rx: Blink2
0: Tx: Transfer1
0: Rx: Blink1
0: Tx: Transfer2
```
