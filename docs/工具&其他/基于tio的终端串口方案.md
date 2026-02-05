# 在 Windows Terminal 中使用 tio 作为串口工具

## 一、背景

在 Windows 上，常见串口工具多为 GUI（如 XCOM、MobaXterm、SecureCRT）。  
如果希望在 **终端环境中以类 Linux 方式使用串口**，可以选择开源工具 **tio**。

`tio` 是一个轻量级串口终端工具，原生支持 Linux/macOS。  
在 GitHub 上可以找到 Windows 版本的移植项目：

[https://github.com/konosubakonoakua/tio-win](https://github.com/konosubakonoakua/tio-win)

---

## 二、准备工作

### 1. 下载 tio（Windows 版）

从仓库 Release 页面下载编译好的可执行文件，解压后将目录加入 `PATH`，确保在 PowerShell 中可直接使用：

```powershell
tio --version
```

若能正确输出版本信息，说明安装成功。

---

## 三、启动脚本设计（串口选择器）

为了方便选择串口设备并自动记录日志，编写一个 PowerShell 启动脚本。

**文件名：`tio_start.ps1`**

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 | Out-Null

# 1. 显示串口设备列表
Write-Host "--- Available Serial Devices ---" -ForegroundColor Cyan
tio --list

# 2. 获取用户输入
Write-Host ""
Write-Host "TIP: If you see '/dev/ttyS22', it usually maps to COM23 (n+1)." -ForegroundColor Gray
$inputStr = (Read-Host "Enter COM number (e.g. 3) or full path (e.g. /dev/ttyS22)").Trim()

# 3. 处理输入
if ($inputStr -match '^\d+$') {
    $port = "COM$inputStr"
} elseif (-not $inputStr) {
    $port = "COM3"
} else {
    $port = $inputStr
}

# 4. 日志目录
$logDir = "D:\\log"
if (!(Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force
}

# 清理文件名非法字符
$cleanName = $port -replace '[\\/]', '_'
$fn = Join-Path $logDir "${cleanName}_$(Get-Date -f 'yyyyMMdd_HHmm').log"

# 5. 启动 tio
Write-Host "`n>> Target: $port" -ForegroundColor Green
Write-Host ">> Log   : $fn" -ForegroundColor Yellow
Write-Host ">> Press Ctrl+t then q to quit.`n" -ForegroundColor DarkGray

tio -t --timestamp-format iso8601 -L --log-file $fn $port
```

---

## 四、集成到 Windows Terminal

为了像“内置工具”一样使用 tio，可将其加入 Windows Terminal 的 profile 配置。

### 打开配置文件

Windows Terminal → 设置 → 左下角 **打开 JSON 文件**

### 在 `profiles.list` 中添加：

```json
{
  "name": "Tio 串口选择器 (脚本版)",
  "commandline": "powershell.exe -ExecutionPolicy Bypass -File \"D:\\\\Tools\\\\tio\\\\tio_start.ps1\"",
  "icon": "⚡",
  "font": {
    "face": "Cascadia Code"
  },
  "colorScheme": "One Half Dark",
  "useAcrylic": true,
  "acrylicOpacity": 0.7,
  "closeOnExit": "graceful"
}
```

> ⚠ 注意：JSON 中路径必须使用双反斜杠 `\\`，否则 Windows Terminal 会报错。

保存后重启 Windows Terminal，即可在新建标签页中看到该入口。

---

## 五、使用说明

1. 打开 Windows Terminal  
2. 新建标签页 → 选择：

```text
Tio 串口选择器 (脚本版)
```

3. 脚本会列出可用串口：

```text
tio --list
```

4. 输入：
- `3` → 使用 COM3  
- `/dev/ttyS22` → 使用该路径  

5. 自动生成日志文件，例如：

```text
D:\log\COM3_20260205_1030.log
```

退出方式：

```text
Ctrl + t 然后 q
```

---

## 六、补充说明

### 1. 关于 `/dev/ttySxx` 与 COM 端口

在 tio-win 的实现中：

```text
/dev/ttyS0  ≈ COM1
/dev/ttyS1  ≈ COM2
...
```

不同版本映射可能不同，因此建议：

👉 **优先使用 COMx 方式输入最稳妥**

---

### 2. 适合使用 tio 的场景

适合：

- 串口调试嵌入式设备  
- 长时间日志采集  
- 与 Linux 上 tio 使用体验保持一致  
- 自动记录日志文件  

不适合：

- 需要 XMODEM/YMODEM 传文件  
- 需要 GUI 配置复杂参数的场景  

---

## 七、总结

该方案实现了：

- 在 Windows Terminal 中原生使用串口  
- 类 Linux 风格操作体验  
- 自动生成带时间戳的日志文件  
- 避免 GUI 串口工具对编码和复制粘贴的限制  

适合：

> 习惯终端工作流、需要长时间串口日志采集的用户。
