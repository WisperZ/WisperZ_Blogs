---
id: openstack-kolla-zed
title: Kolla-Ansible 部署 OpenStack Zed
description: 记录 Ubuntu 22.04 上 Kolla-Ansible Zed 单机部署与排障。
status: Todo
created: null
updated: null
tags:
  - Linux与云计算
aliases: []
---

# Kolla-Ansible 部署 OpenStack Zed {#ubuntu2204openstack-zed-all-in-one}

## 安装OpenStack
### 基础工具安装
```shell
# 安装python工具等
apt install git python3-dev libffi-dev gcc libssl-dev -y
```
### 安装并创建虚拟环境
虚拟环境路径可自定义，本文以"/opt/openstack/venv"为例。
```shell
# 安装虚拟环境包
apt install python3-venv -y
# 创建虚拟环境
python3 -m venv /opt/openstack/venv
```
### 进入虚拟环境
```shell
source /opt/openstack/venv/bin/activate
```
注：后续操作都在虚拟环境下进行，如果要退出虚拟环境请使用一下命令
```shell
deactivate
```
### 升级pip并配置国内源
```shell
# pip3临时使用清华源更新pip
pip3 install -U pip -i https://pypi.tuna.tsinghua.edu.cn/simple
# pip设置清华源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```
### 安装ansible
```shell
pip install 'ansible>=4,<6'
```
### 安装对应openstack版本的kolla-ansible
```shell
pip install git+https://opendev.org/openstack/kolla-ansible@stable/zed
```
### 创建配置文件目录并附加权限
```shell
sudo mkdir -p /etc/kolla
sudo chown $USER:$USER /etc/kolla
```
### 复制配置文件
```shell
# 复制配置文件到配置文件目录
cp -r /opt/openstack/venv/share/kolla-ansible/etc_examples/kolla/* /etc/kolla
```
### 复制依赖文件到当前目录
```shell
cp /opt/openstack/venv/share/kolla-ansible/ansible/inventory/all-in-one .
```
### 安装ansible依赖
```shell
kolla-ansible install-deps
```
### 生成密码到/etc/kolla/passwords.yml文件中
注：要配置的密码有很多，可以手动编辑文件进行配置，也可以执行下面命令自动生成。
```shell
kolla-genpwd
```
### 修改/etc/kolla/passwords.yml中登录密码
找到文件中key控制台登录密码的key：keystone_admin_password
或者直接使用命令替换
**注意：这里自定义密码前需要有个空格**
```shell
sed -i 's/^keystone_admin_password.*/keystone_admin_password: REPLACE_WITH_YOUR_SECRET/' /etc/kolla/passwords.yml
```
### 修改/etc/kolla/globals.yml文件,配置并开启服务
```yaml
# 基础配置:
kolla_base_distro:          						# 系统配置，修改为ubuntu即可
openstack_release:          						# openstack版本，本文使用的zed
kolla_internal_vip_address: 						# 用来访问web控制台,
																				# 如果enable_haproxy为no则配置一个单独的IP,
																				# 否则使用network_interface网卡分配的IP
network_interface: "enp3s0"    					# 这里需要改为自己的网卡否则会报错
neutron_external_interface: 						# 外部网卡名称，本文是ens37
# 服务组件配置:
enable_haproxy: "no" 										#高可用，如果为yes则kolla_internal_vip_address可以使用独立IP
enable_cinder: "yes" 										#块存储
enable_cinder_backup: "no"
enable_cinder_backend_lvm: "yes" 				#使用逻辑存储
enable_neutron_provider_networks: "yes" # 启用外部网络
nova_compute_virt_type: "qemu" 					# 虚拟化类型(物理机用kvm,VMWare使用qemu)
nova_console: "spice"
```
### cinder存储配置
```yaml
# a.查看存储节点的盘:
ansible -i all-in-one "storage*" -a "lsblk"
# b.格式化并且创建分区组
mkfs.ext4   /dev/sdb
pvcreate    /dev/sdb
vgcreate  cinder-volumes  /dev/sdb
```
### 预配置
```yaml
# 基础环境安装，比如docker等
kolla-ansible -i ./all-in-one bootstrap-servers
```
### 环境检测
```yaml
kolla-ansible -i ./all-in-one prechecks
```
注意：如果检测在Checking docker SDK报错找不到docker模块的话，修改all-in-one文件内容如下。
```yaml
[deployment]
localhost       ansible_connection=local  ansible_python_interpreter="{{ ansible_playbook_python }}"
```
我执行的结果如下
```yaml
Bootstrapping servers : ansible-playbook -e @/etc/kolla/globals.yml  -e @/etc/kolla/passwords.yml -e CONFIG_DIR=/etc/kolla  -e kolla_action=bootstrap-servers /opt/openstack/venv/share/kolla-ansible/ansible/kolla-host.yml  --inventory ./all-in-one
[WARNING]: Invalid characters were found in group names but not replaced, use -vvvv to see details

PLAY [Gather facts for all hosts] **********************************************************************************************************************************************************************************************************

TASK [Gather facts] ************************************************************************************************************************************************************************************************************************
ok: [localhost]

TASK [Group hosts to determine when using --limit] *****************************************************************************************************************************************************************************************
ok: [localhost]
[WARNING]: Could not match supplied host pattern, ignoring: all_using_limit_True

PLAY [Gather facts for all hosts (if using --limit)] ***************************************************************************************************************************************************************************************
skipping: no hosts matched

PLAY [Apply role baremetal] ****************************************************************************************************************************************************************************************************************

TASK [openstack.kolla.baremetal : Ensure localhost in /etc/hosts] **************************************************************************************************************************************************************************
ok: [localhost]

TASK [openstack.kolla.baremetal : Ensure hostname does not point to 127.0.1.1 in /etc/hosts] ***********************************************************************************************************************************************
ok: [localhost]

TASK [openstack.kolla.baremetal : Generate /etc/hosts for all of the nodes] ****************************************************************************************************************************************************************
changed: [localhost]

TASK [openstack.kolla.baremetal : Ensure unprivileged users can use ping] ******************************************************************************************************************************************************************
skipping: [localhost]

TASK [openstack.kolla.baremetal : Ensure /etc/cloud/cloud.cfg exists] **********************************************************************************************************************************************************************
ok: [localhost]

TASK [openstack.kolla.baremetal : Disable cloud-init manage_etc_hosts] *********************************************************************************************************************************************************************
skipping: [localhost]

TASK [openstack.kolla.baremetal : Set firewall default policy] *****************************************************************************************************************************************************************************
ok: [localhost]

TASK [openstack.kolla.baremetal : Check if firewalld is installed] *************************************************************************************************************************************************************************
skipping: [localhost]

TASK [openstack.kolla.baremetal : Disable firewalld] ***************************************************************************************************************************************************************************************
skipping: [localhost] => (item=firewalld)

TASK [openstack.kolla.packages : Install packages] *****************************************************************************************************************************************************************************************
ok: [localhost]

TASK [openstack.kolla.packages : Remove packages] ******************************************************************************************************************************************************************************************
ok: [localhost]

TASK [openstack.kolla.docker : Fail if docker_custom_option is defined] ********************************************************************************************************************************************************************
skipping: [localhost]

TASK [openstack.kolla.docker : include_tasks] **********************************************************************************************************************************************************************************************
included: /root/.ansible/collections/ansible_collections/openstack/kolla/roles/docker/tasks/repo-Debian.yml for localhost

TASK [openstack.kolla.docker : Install CA certificates and gnupg packages] *****************************************************************************************************************************************************************
ok: [localhost]

TASK [openstack.kolla.docker : Ensure apt sources list directory exists] *******************************************************************************************************************************************************************
ok: [localhost]

TASK [openstack.kolla.docker : Install docker apt gpg key] *********************************************************************************************************************************************************************************
ok: [localhost]

TASK [openstack.kolla.docker : Install docker apt pin] *************************************************************************************************************************************************************************************
skipping: [localhost]

TASK [openstack.kolla.docker : Enable docker apt repository] *******************************************************************************************************************************************************************************
ok: [localhost]

TASK [openstack.kolla.docker : Check which containers are running] *************************************************************************************************************************************************************************
ok: [localhost]

TASK [openstack.kolla.docker : Check if docker systemd unit exists] ************************************************************************************************************************************************************************
ok: [localhost]

TASK [openstack.kolla.docker : Mask the docker systemd unit on Debian/Ubuntu] **************************************************************************************************************************************************************
skipping: [localhost]

TASK [openstack.kolla.docker : Install packages] *******************************************************************************************************************************************************************************************
ok: [localhost]

TASK [openstack.kolla.docker : Start docker] ***********************************************************************************************************************************************************************************************
skipping: [localhost]

TASK [openstack.kolla.docker : Wait for Docker to start] ***********************************************************************************************************************************************************************************
skipping: [localhost]

TASK [openstack.kolla.docker : Ensure containers are running after Docker upgrade] *********************************************************************************************************************************************************
skipping: [localhost]

TASK [openstack.kolla.docker : Ensure docker config directory exists] **********************************************************************************************************************************************************************
ok: [localhost]

TASK [openstack.kolla.docker : Write docker config] ****************************************************************************************************************************************************************************************
changed: [localhost]

TASK [openstack.kolla.docker : Remove old docker options file] *****************************************************************************************************************************************************************************
ok: [localhost]

TASK [openstack.kolla.docker : Ensure docker service directory exists] *********************************************************************************************************************************************************************
skipping: [localhost]

TASK [openstack.kolla.docker : Configure docker service] ***********************************************************************************************************************************************************************************
skipping: [localhost]

TASK [openstack.kolla.docker : Ensure the path for CA file for private registry exists] ****************************************************************************************************************************************************
skipping: [localhost]

TASK [openstack.kolla.docker : Ensure the CA file for private registry exists] *************************************************************************************************************************************************************
skipping: [localhost]

TASK [openstack.kolla.docker : Flush handlers] *********************************************************************************************************************************************************************************************

RUNNING HANDLER [openstack.kolla.docker : Restart docker] **********************************************************************************************************************************************************************************
changed: [localhost]

TASK [openstack.kolla.docker : Start and enable docker] ************************************************************************************************************************************************************************************
changed: [localhost]

TASK [openstack.kolla.docker : include_tasks] **********************************************************************************************************************************************************************************************
skipping: [localhost]

TASK [openstack.kolla.kolla_user : Ensure groups are present] ******************************************************************************************************************************************************************************
skipping: [localhost] => (item=docker)
skipping: [localhost] => (item=sudo)
skipping: [localhost] => (item=kolla)

TASK [openstack.kolla.kolla_user : Create kolla user] **************************************************************************************************************************************************************************************
skipping: [localhost]

TASK [openstack.kolla.kolla_user : Add public key to kolla user authorized keys] ***********************************************************************************************************************************************************
skipping: [localhost]

TASK [openstack.kolla.kolla_user : Grant kolla user passwordless sudo] *********************************************************************************************************************************************************************
skipping: [localhost]

TASK [openstack.kolla.docker_sdk : Install packages] ***************************************************************************************************************************************************************************************
ok: [localhost]

TASK [openstack.kolla.docker_sdk : Install latest pip in the virtualenv] *******************************************************************************************************************************************************************
skipping: [localhost]

TASK [openstack.kolla.docker_sdk : Install docker SDK for python] **************************************************************************************************************************************************************************
changed: [localhost]

TASK [openstack.kolla.baremetal : Ensure node_config_directory directory exists] ***********************************************************************************************************************************************************
ok: [localhost]

TASK [openstack.kolla.apparmor_libvirt : include_tasks] ************************************************************************************************************************************************************************************
included: /root/.ansible/collections/ansible_collections/openstack/kolla/roles/apparmor_libvirt/tasks/remove-profile.yml for localhost

TASK [openstack.kolla.apparmor_libvirt : Get stat of libvirtd apparmor profile] ************************************************************************************************************************************************************
ok: [localhost]

TASK [openstack.kolla.apparmor_libvirt : Get stat of libvirtd apparmor disable profile] ****************************************************************************************************************************************************
ok: [localhost]

TASK [openstack.kolla.apparmor_libvirt : Remove apparmor profile for libvirt] **************************************************************************************************************************************************************
changed: [localhost]

TASK [openstack.kolla.baremetal : Change state of selinux] *********************************************************************************************************************************************************************************
skipping: [localhost]

TASK [openstack.kolla.baremetal : Set https proxy for git] *********************************************************************************************************************************************************************************
skipping: [localhost]

TASK [openstack.kolla.baremetal : Set http proxy for git] **********************************************************************************************************************************************************************************
skipping: [localhost]

TASK [openstack.kolla.baremetal : include_tasks] *******************************************************************************************************************************************************************************************
skipping: [localhost]

PLAY RECAP *********************************************************************************************************************************************************************************************************************************
localhost                  : ok=29   changed=6    unreachable=0    failed=0    skipped=24   rescued=0    ignored=0
```
遇到问题
```yaml
TASK [nova-cell : Checking that host libvirt is not running] *******************************************************************************************************************************************************************************
fatal: [localhost]: FAILED! => {"changed": false, "failed_when_result": true, "stat": {"atime": 1704351170.0131385, "attr_flags": "", "attributes": [], "block_size": 4096, "blocks": 0, "charset": "binary", "ctime": 1704350627.6463745, "dev": 24, "device_type": 0, "executable": false, "exists": true, "gid": 146, "gr_name": "libvirt", "inode": 4890, "isblk": false, "ischr": false, "isdir": false, "isfifo": false, "isgid": false, "islnk": false, "isreg": false, "issock": true, "isuid": false, "mimetype": "inode/socket", "mode": "0660", "mtime": 1704350627.6023772, "nlink": 1, "path": "/var/run/libvirt/libvirt-sock", "pw_name": "root", "readable": true, "rgrp": true, "roth": false, "rusr": true, "size": 0, "uid": 0, "version": null, "wgrp": true, "woth": false, "writeable": true, "wusr": true, "xgrp": false, "xoth": false, "xusr": false}}
```
手动删除文件`/var/run/libvirt/libvirt-sock`
### 开始部署
```yaml
kolla-ansible -i ./all-in-one deploy
```
#### 错误与解决

1. ModuleNotFoundError: No module named 'docker'
```yaml
An exception occurred during task execution. To see the full traceback, use -vvv. The error was: ModuleNotFoundError: No module named 'docker'
```
安装Docker Python模块：需要安装Python的docker模块。可以使用以下命令来安装：
```yaml
sudo pip install docker
```

2. mariadb : Wait for MariaDB service to be ready through VIP
```yaml
TASK [mariadb : Wait for MariaDB service to be ready through VIP] **************************************************************************************************************************************************************************
FAILED - RETRYING: [localhost]: Wait for MariaDB service to be ready through VIP (6 retries left).
FAILED - RETRYING: [localhost]: Wait for MariaDB service to be ready through VIP (5 retries left).
FAILED - RETRYING: [localhost]: Wait for MariaDB service to be ready through VIP (4 retries left).
FAILED - RETRYING: [localhost]: Wait for MariaDB service to be ready through VIP (3 retries left).
FAILED - RETRYING: [localhost]: Wait for MariaDB service to be ready through VIP (2 retries left).
FAILED - RETRYING: [localhost]: Wait for MariaDB service to be ready through VIP (1 retries left).
fatal: [localhost]: FAILED! => {"attempts": 6, "changed": false, "cmd": ["docker", "exec", "mariadb", "mysql", "-h", "-P", "3306", "-u", "root", "-pd12d7VGpKKanU7vsBXODTVhJQPUYnBMYFQUadQ6I", "-e", "show databases;"], "delta": "0:00:00.114604", "end": "2024-01-05 15:12:40.839061", "msg": "non-zero return code", "rc": 1, "start": "2024-01-05 15:12:40.724457", "stderr": "ERROR 2005 (HY000): Unknown server host '-P' (-2)", "stderr_lines": ["ERROR 2005 (HY000): Unknown server host '-P' (-2)"], "stdout": "", "stdout_lines": []}
```
修改配置文件`/etc/kolla/globals.yml`中的`kolla_internal_vip_address`如下，其中`x.x.x.x`为你自己的ip
```bash
kolla_internal_vip_address: "x.x.x.x"
```

3. openvswitch : Ensuring OVS bridge is properly setup
```bash
TASK [openvswitch : Ensuring OVS bridge is properly setup] *********************************************************************************************************************************************************************************
failed: [localhost] (item=['br-ex', 'eth1']) => {"ansible_loop_var": "item", "changed": false, "cmd": ["docker", "exec", "openvswitch_db", "/usr/local/bin/kolla_ensure_openvswitch_configured", "br-ex", "eth1"], "delta": "0:00:00.083234", "end": "2024-01-05 15:30:55.677928", "item": ["br-ex", "eth1"], "msg": "non-zero return code", "rc": 1, "start": "2024-01-05 15:30:55.594694", "stderr": "Device \"eth1\" does not exist.", "stderr_lines": ["Device \"eth1\" does not exist."], "stdout": "", "stdout_lines": []}
```
修改配置文件`/etc/kolla/globals.yml`中的`neutron_external_interface`为你自己的网卡名称

4. RUNNING HANDLER [nova-cell : Create libvirt SASL user]
```bash
RUNNING HANDLER [nova-cell : Create libvirt SASL user] *************************************************************************************************************************************************************************************
fatal: [localhost]: FAILED! => {"censored": "the output has been hidden due to the fact that 'no_log: true' was specified for this result", "changed": true}
```
修改文件`/opt/openstack/venv/share/kolla-ansible/ansible/roles/nova-cell/defaults/main.yml`，将`libvirt_enable_sasl`设置为false
```bash
# Whether to enable libvirt SASL authentication.
libvirt_enable_sasl: false
```

5. RUNNING HANDLER [openvswitch : Waiting for openvswitch_db service to be ready]
```bash
RUNNING HANDLER [openvswitch : Waiting for openvswitch_db service to be ready] *************************************************************************************************************************************************************
FAILED - RETRYING: [localhost]: Waiting for openvswitch_db service to be ready (30 retries left).
FAILED - RETRYING: [localhost]: Waiting for openvswitch_db service to be ready (29 retries left).
FAILED - RETRYING: [localhost]: Waiting for openvswitch_db service to be ready (28 retries left).
FAILED - RETRYING: [localhost]: Waiting for openvswitch_db service to be ready (27 retries left).
FAILED - RETRYING: [localhost]: Waiting for openvswitch_db service to be ready (26 retries left).
FAILED - RETRYING: [localhost]: Waiting for openvswitch_db service to be ready (25 retries left).
FAILED - RETRYING: [localhost]: Waiting for openvswitch_db service to be ready (24 retries left).
FAILED - RETRYING: [localhost]: Waiting for openvswitch_db service to be ready (23 retries left).
FAILED - RETRYING: [localhost]: Waiting for openvswitch_db service to be ready (22 retries left).
FAILED - RETRYING: [localhost]: Waiting for openvswitch_db service to be ready (21 retries left).
FAILED - RETRYING: [localhost]: Waiting for openvswitch_db service to be ready (20 retries left).
FAILED - RETRYING: [localhost]: Waiting for openvswitch_db service to be ready (19 retries left).
FAILED - RETRYING: [localhost]: Waiting for openvswitch_db service to be ready (18 retries left).
FAILED - RETRYING: [localhost]: Waiting for openvswitch_db service to be ready (17 retries left).
FAILED - RETRYING: [localhost]: Waiting for openvswitch_db service to be ready (16 retries left).
FAILED - RETRYING: [localhost]: Waiting for openvswitch_db service to be ready (15 retries left).
FAILED - RETRYING: [localhost]: Waiting for openvswitch_db service to be ready (14 retries left).
FAILED - RETRYING: [localhost]: Waiting for openvswitch_db service to be ready (13 retries left).
FAILED - RETRYING: [localhost]: Waiting for openvswitch_db service to be ready (12 retries left).
FAILED - RETRYING: [localhost]: Waiting for openvswitch_db service to be ready (11 retries left).
FAILED - RETRYING: [localhost]: Waiting for openvswitch_db service to be ready (10 retries left).
FAILED - RETRYING: [localhost]: Waiting for openvswitch_db service to be ready (9 retries left).
FAILED - RETRYING: [localhost]: Waiting for openvswitch_db service to be ready (8 retries left).
FAILED - RETRYING: [localhost]: Waiting for openvswitch_db service to be ready (7 retries left).
FAILED - RETRYING: [localhost]: Waiting for openvswitch_db service to be ready (6 retries left).
FAILED - RETRYING: [localhost]: Waiting for openvswitch_db service to be ready (5 retries left).
FAILED - RETRYING: [localhost]: Waiting for openvswitch_db service to be ready (4 retries left).
FAILED - RETRYING: [localhost]: Waiting for openvswitch_db service to be ready (3 retries left).
FAILED - RETRYING: [localhost]: Waiting for openvswitch_db service to be ready (2 retries left).
FAILED - RETRYING: [localhost]: Waiting for openvswitch_db service to be ready (1 retries left).
fatal: [localhost]: FAILED! => {"attempts": 30, "changed": false, "cmd": ["docker", "exec", "openvswitch_db", "ovs-vsctl", "--no-wait", "show"], "delta": "0:00:00.015240", "end": "2024-01-05 16:44:46.206933", "msg": "non-zero return code", "rc": 1, "start": "2024-01-05 16:44:46.191693", "stderr": "Error response from daemon: Container f2bdf7eaa98e670f388261c63d8a97dee9890928d61c973a315b42fe31fd8ed8 is restarting, wait until the container is running", "stderr_lines": ["Error response from daemon: Container f2bdf7eaa98e670f388261c63d8a97dee9890928d61c973a315b42fe31fd8ed8 is restarting, wait until the container is running"], "stdout": "", "stdout_lines": []}
```
RG HANDLER [nova-cell : Create libvirt SASL user]
