---
id: riscv-linker-startup
title: RISC-V 链接与启动脚本分析
description: 结合 RISC-V 示例分析链接文件、内存布局与启动代码。
status: InProgress
created: 2025-04-18 17:28
updated: 2025-04-18 18:20
tags:
  - 嵌入式开发
  - RISC-V
  - 嵌入式操作系统
aliases: []
---

# RISC-V 链接与启动脚本分析 {#risc-v}

## 链接脚本

```LinkerScript
OUTPUT_ARCH( "riscv" )        # 指定目标架构为 RISC-V。
                              # 告诉链接器生成 RISC-V 格式的 ELF 文件（例如，32 位或 64 位，取决于工具链配置）。
ENTRY( _start )               # 定义程序的入口点为 _start。

# 内存区域定义
MEMORY
{
    /* Fake ROM area */
    rom (rxa) : ORIGIN = 0x80000000, LENGTH = 512K # 只读存储器 属性rxa 可读（r）、可执行（x）、可分配（a）
    ram (wxa) : ORIGIN = 0x80080000, LENGTH = 512K # 随机访问存储器 属性wxa 可写（w）、可执行（x）、可分配（a
}

SECTIONS
{
    # .init段，通常存放初始化代码（如_start）
    .init :
    {
        _text = .;                    # 定义符号 _text，表示 .init 段的起始地址
        KEEP (*(SORT_NONE(.init)))    # 将所有 .init 段的内容（来自目标文件）放入这里
                                      # KEEP 确保即使没有引用，这些内容也不会被垃圾回收
                                      # SORT_NONE 表示不按名称排序（保持输入顺序）
    } >rom AT>rom                     # >rom：运行时地址（VMA, Virtual Memory Address）在 rom 区域（0x80000000 起）
                                      # AT>rom：加载地址（LMA, Load Memory Address）也在 rom 区域
                                      # 因为 VMA 和 LMA 相同，表明 .init 段直接在 ROM 中运行，无需复制
    
    # .text段，定义代码段，存放程序的可执行指令
    .text :
    {
        *(.text.unlikely .text.unlikely.*)   # .text.unlikely：存放标记为“不太可能执行”的代码（编译器优化）
        *(.text.startup .text.startup.*)     # .text.startup：存放启动相关代码。
        *(.text .text.*)                     # .text：普通代码段。
        *(.gnu.linkonce.t.*)                 # .gnu.linkonce.t.*：GNU 链接器生成的特殊代码段（用于去重）
    } >rom AT>rom                            # >rom AT>rom：代码段的运行时和加载地址都在 ROM 中
    
    # .fini段，，通常存放程序退出时的清理代码（嵌入式系统中很少使用）
    .fini :
    {
        KEEP (*(SORT_NONE(.fini)))
        _etext = .;                          # 定义符号 _etext，表示代码段的结束地址。
    } >rom AT>rom

    # .rodata相关段
    .rodata.align ALIGN(4):                  # 确保 .rodata 段 4 字节对齐
    {
        _rodata = .;                         # 定义符号 _rodata，表示只读数据段的起始地址
    } >rom AT>rom

    .rodata.start :
    {
        _rodata_lma = LOADADDR(.rodata.start);    # 定义符号 _rodata_lma，表示 .rodata 段的加载地址
    } >rom AT>rom
    
    # .rodata段，存放只读数据（.rdata、.rodata 等），例如字符串常量、const 变量
    .rodata :
    {
        *(.rdata)                # TODO
        *(.rodata .rodata.*)     # TODO
        *(.gnu.linkonce.r.*)     # TODO

        . = ALIGN(4);            # 确保数据 4 字节对齐
        _erodata = .;            # 定义符号 _erodata，表示只读数据段的结束地址
    } >rom AT>rom

    # .data相关段
    .data.align :
    {
        . = ALIGN(4);            # 确保 .data 段 4 字节对齐
        _data = .;               # 定义符号 _data，表示数据段的起始地址（RAM 中）
    } >ram AT>rom

    .data.start :
    {
        _data_lma = LOADADDR(.data.start);  # 定义符号 _data_lma，表示数据段的加载地址（ROM 中）
    } >ram AT>rom

    # .data段，存放初始化数据（.data）、小型数据（.sdata）、只读小型数据（.srodata）等
    .data :
    {
        *(.data .data.*)
        *(.gnu.linkonce.d.*)
        . = ALIGN(8);
        PROVIDE( __global_pointer$ = . + 0x800 );  # 定义全局指针符号 __global_pointer$，指向 .sdata 段的中间位置（偏移 0x800）
                                                   # 在启动代码中，la gp, __global_pointer$ 使用这个符号初始化 gp 寄存器
        *(.sdata .sdata.*)
        *(.sdata2 .sdata2.*)
        *(.gnu.linkonce.s.*)
        . = ALIGN(8);                              # 确保对齐（RISC-V 要求严格对齐）
        *(.srodata.cst16)
        *(.srodata.cst8)
        *(.srodata.cst4)
        *(.srodata.cst2)
        *(.srodata .srodata.*)

        . = ALIGN(4);
        _edata = .;
    } >ram AT>rom

    # .tdata段，存放线程局部存储（TLS）的初始化数据
    .tdata : {
        *(.tdata .tdata.*)
    } >rom AT>rom

    # .tbss段，存放线程局部存储的未初始化数据（BSS 类型的 TLS 变量），NOLOAD 表示此段不占用加载空间（仅在运行时分配）
    .tbss (NOLOAD) : {
        *(.tbss .tbss.* .gnu.linkonce.tb.*)
        *(.tcommon)
        PROVIDE( __tbss_end = . );            # PROVIDE 符号：定义一系列与 TLS 相关的符号（如 __tdata_source、 __tbss_size），供运行时库或 FreeRTOS 使用
                                              # 这些符号描述了 TLS 数据的大小、位置和对齐要求
        PROVIDE( __tls_end = . );
    } >rom AT>rom
    PROVIDE( __tdata_source = LOADADDR(.tdata) );
    PROVIDE( __tdata_source_end = LOADADDR(.tdata) + SIZEOF(.tdata) );
    PROVIDE( __tdata_size = SIZEOF(.tdata) );
    PROVIDE( __tbss_offset = ADDR(.tbss) - ADDR(.tdata) );
    PROVIDE( __tbss_start = ADDR(.tbss) );
    PROVIDE( __tbss_size = SIZEOF(.tbss) );
    PROVIDE( __tls_size = __tls_end - ADDR(.tdata) );
    PROVIDE( __tls_align = MAX(ALIGNOF(.tdata), ALIGNOF(.tbss)) );

    # .bss相关段
    .bss.align :
    {
        . = ALIGN(4);                        # 确保 .bss 段 4 字节对齐
        _bss = .;                            # 定义符号 _bss，表示 BSS 段的起始地址
    } >ram AT>rom

    .bss.start :
    {
        _bss_lma = LOADADDR(.bss.start);     # 定义符号 _bss_lma，表示 BSS 段的加载地址（实际无加载数据）
    } >ram AT>rom

    # .bss段，存放未初始化数据（.bss）、小型未初始化数据（.sbss）和公共符号（COMMON）
    .bss :
    {
        *(.sbss*)%%  %%
        *(.gnu.linkonce.sb.*)
        *(.bss .bss.*)
        *(.gnu.linkonce.b.*)
        *(COMMON)

        . = ALIGN(4);
        _ebss = .;                           # 定义符号 _ebss，表示 BSS 段的结束地址
    } >ram AT>rom

    . = ALIGN(8);                            # 确保当前地址 8 字节对齐
    _end = .;                                # 定义符号 _end，表示程序数据段的结束地址

    # .stack段，定义栈区域
    .stack :
    {
        . = ALIGN(16);                       # 确保栈 16 字节对齐（RISC-V 要求栈对齐）
        . += __stack_size;                   # 分配栈空间，__stack_size 是一个外部定义的符号（可能在 Makefile 或代码中定义）
        _stack_top = .;                      # 定义符号 _stack_top，表示栈顶地址
    } >ram AT>ram
}

```
## 启动文件
\_start.S
```Arm
/*
 * FreeRTOS V202212.00
 * Copyright (C) 2020 Amazon.com, Inc. or its affiliates.  All Rights Reserved.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of
 * this software and associated documentation files (the "Software"), to deal in
 * the Software without restriction, including without limitation the rights to
 * use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 * the Software, and to permit persons to whom the Software is furnished to do so,
 * subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 * FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 * COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 * IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 *
 * https://www.FreeRTOS.org
 * https://www.github.com/FreeRTOS
 *
 */

#include "riscv-virt.h"

    .section .init                # 将 _start 放入 .init 段，通常是固件或内核的初始化代码段，链接器会将其放置在程序的起始位置
    .globl _start                 # 声明 _start 为全局符号，链接器会将其作为程序入口点
    .type _start,@function        # 指定 _start 是一个函数符号，用于调试和链接
_start:
    .cfi_startproc                # 用于生成调用栈信息（CFI，Call Frame Information），调试器使用
    .cfi_undefined ra             # ra（返回地址寄存器）被标记为未定义，因为 _start 是入口点，没有调用者
.option push
.option norelax                   # 禁用链接器优化（如指令替换），确保 la 指令按预期加载地址
                                  # RISC-V 的链接器有时会优化伪指令（例如将 la 替换为 lui/addi），可能导致问题
    la  gp, __global_pointer$     # 加载全局指针（gp）的地址。__global_pointer$ 是链接器脚本定义的符号
                                  # 通常指向全局数据的中间位置，用于优化数据访问（GP-Relative 寻址）
.option pop                       # push/pop 成对出现 保存和恢复编译选项，确保 norelax 只影响当前代码块

    // Continue primary hart
    csrr a0, mhartid              # 读取 mhartid 寄存器（机器 Hart ID），每个硬件线程（Hart）有唯一 ID
                                  # 用于多核系统中区分主核和从核
    li   a1, PRIM_HART            # 加载主 Hart 的 ID（PRIM_HART，通常为 0，在 riscv-virt.h 中定义）
    bne  a0, a1, secondary        # 如果当前 Hart ID 不等于主 Hart ID，跳转到 secondary 标签，执行从核逻辑

    // Primary hart
    la sp, _stack_top             # 为主 Hart 设置栈指针（sp）
                                  # _stack_top 是链接器脚本定义的符号，通常指向栈顶（高地址）
                                  # RISC-V 的栈向下增长（从高地址到低地址）

    // Load data section
    la a0, _data_lma              # 数据段的加载地址（Flash 中的位置）
    la a1, _data                  # 数据段的起始地址（RAM 中的位置）
    la a2, _edata                 # 数据段的结束地址（RAM 中的位置）
    bgeu a1, a2, 2f               # 如果 _data >= _edata，即数据段为空，跳转到标签 2，跳过复制
1:
    LOAD t0, (a0)                 # 从 Flash（a0 指向 _data_lma）加载数据到寄存器 t0  
    STOR t0, (a1)                 # 将数据存储到 RAM（a1 指向 _data）
    addi a0, a0, REGSIZE          # 地址递增，REGSIZE 是寄存器大小->
    addi a1, a1, REGSIZE          # （RISC-V 32 位为 4 字节，64 位为 8 字节，在 riscv-virt.h 中定义）
    bltu a1, a2, 1b               # 如果 a1 < a2，继续循环（跳转到标签 1）
2:

    // Clear bss section
    la a0, _bss                   # BSS 段的起始地址
    la a1, _ebss                  # BSS 段的结束地址
    bgeu a0, a1, 2f               # 如果 _bss >= _ebss，即 BSS 段为空，跳转到标签 2，跳过清零
1:
    STOR zero, (a0)               # 将地址 a0 处的值清零
    addi a0, a0, REGSIZE          # 地址递增
    bltu a0, a1, 1b               # 如果 a0 < a1，继续循环
2:

    // argc, argv, envp is 0
    li  a0, 0                     # 设置 main 函数的参数为 0（argc、argv、envp），因为嵌入式系统中通常没有命令行参数
    li  a1, 0 
    li  a2, 0
    jal main                      # 跳转到 main 函数（C 语言入口），jal 会将返回地址存储到 ra 寄存器
1:
    wfi
    j 1b

secondary:
    // TODO: Multicore is not supported
    wfi                           # 从核进入等待中断状态
    j secondary                   # 无限循环，表明当前代码不支持多核运行
    .cfi_endproc                  # 结束调用栈信息生成，与 .cfi_startproc 配对

```


## 参考
- 开发环境搭建参考 [RISC-V开发环境搭建](../../项目实践/RISC-V/RISC-V开发环境搭建.md)
- 链接文件段划分参考[链接脚本](../构建与链接/段与内存布局.md)
