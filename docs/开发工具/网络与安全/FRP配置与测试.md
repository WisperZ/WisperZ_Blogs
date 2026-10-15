---
id: frp-setup
title: FRP 配置与测试
description: 记录 FRP 服务端、客户端、systemd 与 TCP 测试流程。
status: Todo
created: null
updated: null
tags:
  - 开发工具
aliases: []
---

# FRP 配置与测试 {#frp}

## 1. 获取 FRP 文件

当前 frp 文件存放在内网服务器路径（文件浏览器访问）：

```
\\192.0.2.10\itx_share\04_软件工具\Frp
```

或通过浏览器访问：

[点击此处访问共享目录](http://192.0.2.10:1024/#/itx_share/04_软件工具/Frp)

文件说明：

- `frp_0.58.0_linux_amd64.tar.gz`：frp 主程序文件
- `server_test.py`：测试脚本

------

## 2. 解压

在目标目录执行：

```
tar -xvf frp_0.58.0_linux_amd64.tar.gz
```

解压后文件结构示例：

```
├── frpc         # 客户端程序
├── frpc.toml    # 客户端配置文件
├── frps         # 服务端程序
├── frps.toml    # 服务端配置文件
└── LICENSE
```

------

## 3. 服务端配置（frps）

### 3.1 编辑 frps. toml

服务器地址：`192.0.2.10`
 管理面板： [FRP 管理页面](http://192.0.2.10:7500/)
 默认账号/密码：

`REPLACE_WITH_YOUR_VALUE`
```text
user: admin
pwd: admin
```

示例配置（`frps.toml`）：

```
bindPort = 7000

transport.tls.force = true

auth.method = "token"
auth.token = "REPLACE_WITH_YOUR_SECRET"

webServer.addr = "0.0.0.0"
webServer.port = 7500
webServer.user = "admin"
webServer.password = "REPLACE_WITH_YOUR_SECRET"

log.to = "frpc.log"
```

------

### 3.2 创建系统服务（frps）

创建服务文件：

```
sudo vim /etc/systemd/system/frps.service
```

写入（按实际路径调整）：

```
[Unit]
Description = frp server
After = network.target syslog.target
Wants = network.target

[Service]
Type = simple
ExecStart = /root/frps/frp_0.58.0_linux_amd64/frps -c /root/frps/frp_0.58.0_linux_amd64/frps.toml

[Install]
```

------

### 3.3 启动与验证（服务端）

1. 重新加载 systemd 配置：

```
sudo systemctl daemon-reload
```

1. 启动服务：

```
sudo systemctl start frps.service
```

1. 查看服务状态：

```
sudo systemctl status frps.service
```

1. 开机自启（可选）：

```
sudo systemctl enable frps.service
```

验证：

```
systemctl is-enabled frps.service
```

------

## 4. 客户端配置（frpc）

### 4.1 编辑 frpc. toml

示例配置（`frpc.toml`）：

```
serverAddr = "192.0.2.10"
serverPort = 7000

user = "AI"
auth.method = "token"
auth.token = "REPLACE_WITH_YOUR_SECRET"

log.to = "/opt/frp/frpc.log"
log.level = "info"
log.maxDays = 7

[[proxies]]
name = "AI_poxy"
type = "tcp"
localIP = "127.0.0.1"
localPort = 6000
remotePort = 6000

[[proxies]]
name = "GasMeter"
type = "tcp"
localIP = "127.0.0.1"
localPort = 6001
remotePort = 6001

[[proxies]]
name = "CinosWaterMeter"
type = "tcp"
localIP = "127.0.0.1"
localPort = 8001
remotePort = 8001

[[proxies]]
name = "CinosGasMeter"
type = "tcp"
localIP = "127.0.0.1"
localPort = 8000
remotePort = 8000
```

------

### 4.2 创建系统服务（frpc）

创建服务文件：

```
sudo vim /etc/systemd/system/frpc.service
```

写入（按实际路径调整）：

```
[Unit]
Description = frp client
After = network.target syslog.target
Wants = network.target

[Service]
Type = simple
ExecStart = /mnt/cinos/Yuh/frp/frp_0.58.0_linux_amd64/frpc -c /mnt/cinos/Yuh/frp/frp_0.58.0_linux_amd64/frpc.toml

[Install]
WantedBy = multi-user.target
```

------

### 4.3 启动与验证（客户端）

与服务端同样的命令：

```
sudo systemctl daemon-reload
sudo systemctl start frpc.service
sudo systemctl status frpc.service
sudo systemctl enable frpc.service
systemctl is-enabled frpc.service
```

------

## 5.测试
当启动了上述的 `frpc.service` 和 `frps.service` 服务，可以通过简单的 tcp 服务器程序来验证
拷贝 `server_test.py` 文件到你的服务器上
将以下两句修改为你对应的端口 
server_socket.bind (('0.0.0.0', 6001))
print ("TCP server listening on port 6001...", flush=True)
```py
import socket

def tcp_server():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('0.0.0.0', 6001))
        server_socket.listen(5)
        print("TCP server listening on port 6001...", flush=True)
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connected to {client_address}", flush=True)
            try:
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        print(f"Client {client_address} disconnected", flush=True)
                        break
                    # Convert data to hex string
                    hex_data = ' '.join(f'{byte:02X}' for byte in data)
                    print(f"Received data from {client_address} (hex): {hex_data}", flush=True)
            except Exception as e:
                print(f"Error handling client {client_address}: {e}", flush=True)
            finally:
                client_socket.close()
                print(f"Closed connection to {client_address}", flush=True)
    except Exception as e:
        print(f"Server error: {e}", flush=True)
    finally:
        server_socket.close()
        print("Server socket closed", flush=True)

if __name__ == "__main__":
    tcp_server()
```

运行服务
```bash
python server_test.py
```

在另外的电脑，这里推荐 window 设备使用 NetAssist 软件建立 tcp 链接来进行测试，如果一切顺利的话可以在终端中看到来自 NetAssist 的 tcp 消息

```bash
(base) aiserver@aiserver:~/frp$ python server_test.py
TCP server listening on port 8100...
Connected to ('127.0.0.1', 41686)
Received data from ('127.0.0.1', 41686) (hex): 57 65 6C 63 6F 6D 65 20 74 6F 20 4E 65 74 41 73 73 69 73 74
Received data from ('127.0.0.1', 41686) (hex): 57 65 6C 63 6F 6D 65 20 74 6F 20 4E 65 74 41 73 73 69 73 74
Received data from ('127.0.0.1', 41686) (hex): 57 65 6C 63 6F 6D 65 20 74 6F 20 4E 65 74 41 73 73 69 73 74
Received data from ('127.0.0.1', 41686) (hex): 57 65 6C 63 6F 6D 65 20 74 6F 20 4E 65 74 41 73 73 69 73 74
Client ('127.0.0.1', 41686) disconnected
```

## 6.说明与注意事项

- 上文的所有路径请按你系统上的真实路径调整。
- `auth.token` 必须在 frps 与 frpc 上保持一致。
- 需要在云服务器提供上的 `控制台` 的 ` 安全策略 ` 中开放你所需的端口
    - 7000：当前配置的 frps 的端口
    - 7500：当前配置的 frp 的管理页面端口
    - 你在 frpc.toml 配置的 `remotePort` 端口
