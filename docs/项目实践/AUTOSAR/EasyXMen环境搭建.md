---
id: autosar-easyxmen
title: EasyXMen 环境搭建
description: 记录普华小满 EasyXMen、NXP MCAL 与工具安装和示例编译。
status: Done
created: 2025-02-24 10:53
updated: 2025-04-18 19:00
tags:
  - 项目实践
  - AUTOSAR
  - 小满
aliases: []
---

# EasyXMen 环境搭建 {#_1}

## 1.软件包下载

### 1.1 AUTOSAR BSW 软件安装

AUTOSAR BSW基础软件这里使用开源免费的普华基础软件“[小满EasyXMen](https://atomgit.com/easyxmen/XMen)”，文档可以参考[普华小满文档](https://easyxmen.atomgit.net/docs/sub/%E5%B7%A5%E7%A8%8B%E8%AF%B4%E6%98%8E/%E5%B0%8F%E6%BB%A1S32K148%E7%A4%BA%E4%BE%8B%E5%B7%A5%E7%A8%8B%E8%AF%B4%E6%98%8E.html#)，需要在[开源小满的网站](https://easyxmen.atomgit.com/) 申请工具授权码。

### 1.2 Mcal 驱动包下载

1. 获取 MCAL 安装包和 IDE 补丁包。打开[网址](https://www.nxp.com.cn/document/guide/getting-started-with-the-real-time-drivers-rtd:GS-AUTOMOTIVE-RTD?section=design-resources)
    ![生成license](../../_resources/autosar-easyxmen/Mcal驱动包下载-18.png)
    ![生成license](../../_resources/autosar-easyxmen/Mcal驱动包下载-19.png)
    ![生成license](../../_resources/autosar-easyxmen/Mcal驱动包下载-20.png)
    ![生成license](../../_resources/autosar-easyxmen/Mcal驱动包下载-21.png)
### 1.3 EB Tresos 工具下载
下载 EB 工具
![下载 EB 工具](../../_resources/autosar-easyxmen/Mcal驱动包下载-08.png)
保存激活码，下载所有文件
![保存激活码](../../_resources/autosar-easyxmen/Mcal驱动包下载-09.png)

### 1.4 S32 Design Studio 工具下载
1. S32 Design Studio for S32 Platform工具下载，打开[网站](https://www.nxp.com/design/design-center/software/development-software/s32-design-studio-ide:S32-DESIGN-STUDIO)
    选择 S32 Design Studio for S32 Platform v3.5
    ![ARM工具下载](../../_resources/autosar-easyxmen/Mcal驱动包下载-10.png)
    
2. 下载S32 Design Studio v3.5 Windows installer
    ![下载 EB 工具](../../_resources/autosar-easyxmen/Mcal驱动包下载-17.png)
3. 生成 Licencse
    ![生成licencse](../../_resources/autosar-easyxmen/Mcal驱动包下载-14-1.png)
    > 配图涉及设备、账号或软件授权信息，公开版已省略。
### 1.5 普华 AUTOSAR 工具下载
1. 在[普华官网](https://easyxmen.atomgit.com/)，申请之后，会在邮箱中提供下载地址
    ![工具链申请](../../_resources/autosar-easyxmen/Mcal驱动包下载-16.png)

## 2.软件安装

### 2.1 EB Tresos软件安装
1. 点击EB下载的工具，setup.exe

    ![EB Tresos 安装](../../_resources/autosar-easyxmen/软件安装-00.png)
    如果出现报错，找不到安装包
    如下所示
    ![报错](../../_resources/autosar-easyxmen/软件安装-01.jpeg)
    需要将下载下来的部分压缩包解压并添加后缀，和网页上的文件对应
    ![软件安装](../../_resources/autosar-easyxmen/软件安装-02.png)
2. 选择安装路径，我这里选的是默认，再点击 Install，等待安装结束后点击 Exit
    ![软件安装](../../_resources/autosar-easyxmen/软件安装-03.png)
3. 安装安装 EB tresos 许可证，双击打开 EB_Client_License_Administrator_1_4_0_Setup.exe
    ![软件安装](../../_resources/autosar-easyxmen/软件安装-04.png)
4. 选择安装目录，我这里选的是 D:\EB\EB_Client_License_Administrator，尽量不要安装到C盘，文件夹  
   名不要出现空格
    ![软件安装](../../_resources/autosar-easyxmen/软件安装-05.png)
5. 一直默认点 Next 后 Install 安装，直到安装完成
6. 双击打开这个程序：D:\EB\EB_Client_License_Administrator\bin\ClientLicenseAdministrator.exe
    ![软件安装](../../_resources/autosar-easyxmen/软件安装-06.png)
7. 输入激活码，激活
    ![软件安装](../../_resources/autosar-easyxmen/软件安装-07.png)

### 2.2 Mcal 安装
1. 双击 SW32K1_S32M24x_RTD_R21-11_2.0.0_QLP1_D2408.exe 运行安装包
2. 点击 Next，选择 I accept …，再点击 Next
3. 选择之前下载好的 license.dat 文件，然后点击 Next
    ![软件安装](../../_resources/autosar-easyxmen/软件安装-08.png)
4. 默认勾选，点击 Next
    ![软件安装](../../_resources/autosar-easyxmen/软件安装-09.png)
5. 选择安装路径，点击 Next
    ![软件安装](../../_resources/autosar-easyxmen/软件安装-10.png)
    这里我选择的路径是 D:\NXP\AUTOSAR\S 32 K 14 X_MCAL 4_3_RTM_HF 3_1_0_1
6. 设置之前安装的EB路径，如我之前装的是 D:\EB\tresos\，然后点击 Install，直到安装成功
    ![软件安装](../../_resources/autosar-easyxmen/软件安装-11.png)
7. 安装完成，点击tresos Studio
    ![软件安装](../../_resources/autosar-easyxmen/软件安装-12.png)

### 2.3 安装s32ds3.5
1. 双击运行S32DS_ARM_Win32_v2.2.exe
    ![软件安装](../../_resources/autosar-easyxmen/软件安装-13.png)
2. 进入进入安装准备界面
    ![软件安装](../../_resources/autosar-easyxmen/软件安装-14.png)
3. 当安装准备完成之后，会弹出安装向导，点击 Next
    ![软件安装](../../_resources/autosar-easyxmen/软件安装-15.png)
4. 将安装协议拉到底部，勾选同意，然后点击 Next
    ![软件安装](../../_resources/autosar-easyxmen/软件安装-17.png)
6. 选择安装目录，点击 Next
    ![软件安装](../../_resources/autosar-easyxmen/软件安装-18.png)
7. 创建桌面快捷方式
    ![软件安装](../../_resources/autosar-easyxmen/软件安装-19.png)
8. 点击 Install，进入安装流程
    ![软件安装](../../_resources/autosar-easyxmen/软件安装-20.png)
9. 几秒钟之后会弹出激活界面，输入之前保存的激活码，点击 OK。激活码是之前在下载 **S32 Design Studio for ARM 工具下载**的时候保存的
    > 配图涉及设备、账号或软件授权信息，公开版已省略。
10. 然后会弹出安装pe环境，一样的，设置好安装地址跟着装就行。
    ![软件安装](../../_resources/autosar-easyxmen/软件安装-22.png)
11. 点击安装界面的 Done 即完成安装
    ![软件安装](../../_resources/autosar-easyxmen/软件安装-23.png)
### 2.4 普华AutoSAR基础软件安装
1. 点击安装包，可以参考下方文档
    ![软件安装](../../_resources/autosar-easyxmen/软件安装-24.png)
2. 一路Next进行安装
    ![软件安装](../../_resources/autosar-easyxmen/软件安装-25.png)
3. 安装完成，使用邮件中的激活码
    ![软件安装](../../_resources/autosar-easyxmen/软件安装-26.png)
4. 下面是软件打开视图，可以在里面进行AutoSAR配置
    ![软件安装](../../_resources/autosar-easyxmen/软件安装-27.png)
### 2.5 安装 GCC10.2
1. 打开软件 S 32 DS, 创建工作区（**注意不要有中文路径**）
    ![编译 demo](../../_resources/autosar-easyxmen/编译demo-01.png)
2. 安装一个 GCC 10.2
    ![编译 demo](../../_resources/autosar-easyxmen/编译demo-02.png)

### 2.6 安装 S32DS 补丁
1. 安装 S32DS 补丁
    ![编译 demo](../../_resources/autosar-easyxmen/编译demo-03.png)
2. 选择安装新软件之后
    ![编译 demo](../../_resources/autosar-easyxmen/编译demo-05.png)
3. 将下载好的 S32D 补丁包拖入
    ![编译 demo](../../_resources/autosar-easyxmen/编译demo-04.png)
4. 勾选所有选项
    ![](../../_resources/autosar-easyxmen/img-01.png)
    ![](../../_resources/autosar-easyxmen/img-00.png)
    ![](../../_resources/autosar-easyxmen/img-02.png)
    ![](../../_resources/autosar-easyxmen/img-03.png)
    注：如果在这个过程中有时候会报错，很有可能是网络原因，nxp服务器不稳定造成的，重复该操作即可。
    ![](../../_resources/autosar-easyxmen/img-04.png)
## 3. 示例编译
1. 将demo文件提出，因为小满示例工程文件夹原来的压缩包带有中文，所以要把demo文件夹提出来，让路径**不带中文**。
    ![编译 demo](../../_resources/autosar-easyxmen/编译demo-00.png)
2. 工程导入
    ![](../../_resources/autosar-easyxmen/img-05.png)
    ![](../../_resources/autosar-easyxmen/img-06.png)
3. 点击编译会报警告
    ![](../../_resources/autosar-easyxmen/img-07.png)
    找到s32ds的安装路径，然后找到GCC10.2的执行文件，复制路径。
    ![](../../_resources/autosar-easyxmen/img-08.png)
    然后点击菜单栏 project->properties, 双击 PATH
    ![](../../_resources/autosar-easyxmen/img-09.png)
    将复制好的路径添加进环境变量，加路径之前要加个;号。
    ![](../../_resources/autosar-easyxmen/img-10.png)
    再执行编译即成功
    ![](../../_resources/autosar-easyxmen/img-11.png)
