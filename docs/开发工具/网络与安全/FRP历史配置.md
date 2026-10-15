---
id: frp-legacy
title: FRP 历史配置
description: 保留 FRP 较早的服务端与客户端配置示例。
status: Todo
created: null
updated: null
tags:
  - 开发工具
aliases: []
---

# FRP 历史配置 {#frp}

## 介绍

frp 是一款高性能的反向代理应用，专注于内网穿透。它支持多种协议，包括 TCP、UDP、HTTP、HTTPS 等，并且具备 P2P 通信功能。使用 frp，您可以安全、便捷地将内网服务暴露到公网，通过拥有公网 IP 的节点进行中转。
如下优点：

- 多种协议支持：客户端服务端通信支持 TCP、QUIC、KCP 和 Websocket 等多种协议。
- TCP 连接流式复用：在单个连接上承载多个请求，减少连接建立时间，降低请求延迟。
- 代理组间的负载均衡。
- 端口复用：多个服务可以通过同一个服务端端口暴露。
- P2P 通信：流量不必经过服务器中转，充分利用带宽资源。
- 客户端插件：提供多个原生支持的客户端插件，如静态文件查看、HTTPS/HTTP 协议转换、HTTP、SOCKS5 代理等，以便满足各种需求。
- 服务端插件系统：高度可扩展的服务端插件系统，便于根据自身需求进行功能扩展。
- 用户友好的 UI 页面：提供服务端和客户端的用户界面，使配置和监控变得更加方便。

## 软件下载

通过 Github 下载，通过[下载地址](https://github.com/fatedier/frp/releases)获取最新版本。
或者通过 wget 下载
```bash
wget https://github.com/fatedier/frp/releases/download/v0.61.2/frp_0.61.2_linux_amd64.tar.gz
```
下载完成之后解压文件

```bash
tar -xvf frp_0.61.2_linux_amd64.tar.gz
```

解压完成进入文件夹，可以看到以下文件
```
frp
├── frpc
├── frpc.toml
├── frps
├── frps.toml
└── LICENSE
```
文件介绍，后面需要按需改动配置。

- 服务端frps启动文件， frps.toml为配置文件，默认配置文件监听的端口为7000，不使用认证。
- 客户端frpc启动文件， frpc.toml为配置文件，默认配置文件转发端口为22，远程端口是6000。


## 服务端配置

服务端只需要留下 `frps` 和 `frps.toml` 文件。

编辑 `frps.toml` ，完整的配置文件选项可访问 [https://github.com/fatedier/frp/blob/dev/conf/frps_full_example.toml](https://link.zhihu.com/?target=https%3A//github.com/fatedier/frp/blob/dev/conf/frps_full_example.toml) 查看。

```toml
# 默认监听所以地址，如果你想使用特定的IP地址,请更改为你使用的IP地址并取消注释。
# bindAddr = x.x.x.x

# 默认使用7000作为服务端口，建议改成其他端口。
bindPort = 7100

# 用于客户端和服务器通信的身份验证令牌
auth.method = "token"
# 秘钥格式建议配置 用户+@+密码 的格式，方便区分用户，如下所示：
auth.token = "REPLACE_WITH_YOUR_SECRET"

# 允许的端口范围，不设置允许所以端口，笔者允许使用7101-7199端口和6001端口。
allowPorts = [
  { start = 7101, end = 7199 },
  { single = 6001 }
]

# 面板相关配置（可选），配置面板后可以查看代理使用的流量统计。
# webServer.addr = "x.x.x.x"
webServer.port = 7200
webServer.user = "admin"
webServer.password = "REPLACE_WITH_YOUR_SECRET"

# 最大连接池数量
transport.maxPoolCount = 5

# 指定日志文件存储级别和位置，最大存储日志为7天。
log.to = "/opt/frp/frps.log"
log.level = "info"
log.maxDays = 7
```
### 服务端 systemd 管理 frp

创建管理文件

```bash
sudo vim /etc/systemd/system/frps.service
```
写入内容

```text
[Unit]
Description = frp server
After = network.target syslog.target
Wants = network.target

[Service]
Type = simple
# 启动frps的命令，需修改为您的frps的安装路径
ExecStart = /opt/frp/frps -c /opt/frp/frps.toml

[Install]
WantedBy = multi-user.target
```

开机自器和启动服务。
```bash
sudo systemctl enable frps && sudo systemctl start frps
```

服务端状态检查

```bash
sudo systemctl status frps
```

正常情况应该输出如下状态
```bash
● frps.service - frp server
   Loaded: loaded (/etc/systemd/system/frps.service; disabled; vendor preset: disabled)
   Active: active (running) since Wed 2025-04-16 10:29:35 CST; 3h 18min ago
 Main PID: 24519 (frps)
   CGroup: /system.slice/frps.service
           └─24519 /root/frps/frp_0.58.0_linux_amd64/frps -c /root/frps/frp_0.58.0_linux_amd64/frps.toml
Apr 16 10:29:35 hecs-x-xlarge-4-linux-20200511143205 systemd[1]: Started frp server.
```

Active：active (running) 是正常状态

## 客户端配置

客户端只需要留下 `frpc` 和 `frpc.toml` 文件。

编辑 `frpc.toml` ，完整的配置文件选项可访问 [https://github.com/fatedier/frp/blob/dev/conf/frpc_full_example.toml](https://link.zhihu.com/?target=https%3A//github.com/fatedier/frp/blob/dev/conf/frpc_full_example.toml) 查看。

```toml
# 指定服务器地址与端口号。
serverAddr = "x.x.x.x"
serverPort = 7100
# 代理名称将会改为 {user}.{proxy}，建议配置，取服务器上的token中@前部分。
user = "user1"
auth.method = "token"
auth.token = "REPLACE_WITH_YOUR_SECRET"

# 面板相关配置（可选），配置面板后可以查看代理使用的流量统计。
# webServer.addr = "x.x.x.x"
webServer.port = 7200
webServer.user = "admin"
webServer.password = "REPLACE_WITH_YOUR_SECRET"

# 指定日志文件存储级别和位置，最大存储日志为7天。
log.to = "/opt/frp/frpc.log"
log.level = "info"
log.maxDays = 7

[[proxies]]
# name为应用名称，type为协议类型，localIP为内网服务的地址，localPort为内网服务的端口，remotePort为服务器上监听的端口，transport.bandwidthLimit为限速，服务端不限制使用端口，不建议使用1-1024端口。
name = "ssh"
type = "tcp"
localIP = "x.x.x.x"
localPort = 389
remotePort = 7101        #远端服务器如果有安全配置需要去对应的服务商开启端口访问权限
transport.bandwidthLimit = "1MB"
```

### 客户端 systemd 管理 frp

创建管理文件

```bash
sudo vim /etc/systemd/system/frpc.service
```

配置如下
```text
[Unit]
Description = frp server
After = network.target syslog.target
Wants = network.target

[Service]
Type = simple
# 启动frps的命令，需修改为您的frps的安装路径
ExecStart = /opt/frp/frps -c /opt/frp/frps.toml

[Install]
WantedBy = multi-user.target
```

开机自启&启动服务

```bash
sudo systemctl enable frpc && sudo systemctl start frpc
```

检查服务是否正常，使用如下命令查看，如果服务异不是active请检查日志。
```bash
sudo systemctl status frpc
```


使用如下命令查看日志文件，可用于排错和查看frp运行状态。
```bash
# 服务端
sudo cat /opt/frp/frps.log

# 客户端
sudo cat /opt/frp/frpc.log
```
