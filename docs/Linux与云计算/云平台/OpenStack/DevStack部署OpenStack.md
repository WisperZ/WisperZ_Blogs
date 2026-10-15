---
id: openstack-devstack
title: DevStack 部署 OpenStack
description: 记录 DevStack 单机实验环境的配置与排障过程。
status: Todo
created: null
updated: null
tags:
  - Linux与云计算
aliases: []
---

# DevStack 部署 OpenStack {#openstack}

OpenStack 是利用虚拟资源池构建和管理私有云和公共云的平台。那些包含 OpenStack 平台的各个工具（称作“项目”）负责处理计算、网络、存储、身份和镜像服务等核心云计算服务。还可将十余个可选项目捆绑到一起，创建与众不同的可部署云。
## 开始部署
部署的脚本要求是拥有 root 权限的非 root 用户。
添加stack用户并添加root权限
```shell
sudo useradd -s /bin/bash -d /opt/stack -m stack
echo "stack ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/stack
```
克隆并打开devstack
```shell
sudo su - stack
cd /opt/stack
git clone https://git.openstack.org/openstack-dev/devstack
cd devstack
```
如果上面 clone 太慢或者 clone 不下来的话可以试试 github 的源。
```shell
git clone https://github.com/openstack-dev/devstack.git
```

然后就是添加配置了，如果不懂推荐直接使用官方页面介绍的。或者使用以下命令
```shell
cp samples/local.conf ./
vim local.conf
```
修改基础配置
```shell
# [[local|localrc]]
# ADMIN_PASSWORD=REPLACE_WITH_YOUR_SECRET
# DATABASE_PASSWORD=$ADMIN_PASSWORD
# RABBIT_PASSWORD=$ADMIN_PASSWORD
# SERVICE_PASSWORD=$ADMIN_PASSWORD

# #HOST_IP=192.0.2.10
# #SERVICE_HOST=$HOST_IP

# # Enable logging
# LOGFILE=$DEST/logs/stack.sh.log
# VERBOSE=True
# LOG_COLOR=True
# SCREEN_LOGDIR=$DEST/logs/screen

# # Pre-requisite
# ENABLED_SERVICES=placement-api,rabbit,mysql,key
# # Nova
# #ENABLED_SERVICES+=,n-api,n-crt,n-obj,n-cpu,n-cond,n-sch,n-novnc,n-cauth

# # Glance
# #ENABLED_SERVICES+=,g-api,g-reg

# # Neutron
# #ENABLED_SERVICES+=,q-svc,q-dhcp,q-meta,neutron

# # Cinder
# #ENABLED_SERVICES+=,c-api,c-vol,c-sch

# # Horizon
# ENABLED_SERVICES+=,horizon


# Sample ``local.conf`` for user-configurable variables in ``stack.sh``

# NOTE: Copy this file to the root DevStack directory for it to work properly.

# ``local.conf`` is a user-maintained settings file that is sourced from ``stackrc``.
# This gives it the ability to override any variables set in ``stackrc``.
# Also, most of the settings in ``stack.sh`` are written to only be set if no
# value has already been set; this lets ``local.conf`` effectively override the
# default values.

# This is a collection of some of the settings we have found to be useful
# in our DevStack development environments. Additional settings are described
# in https://docs.openstack.org/devstack/latest/configuration.html#local-conf
# These should be considered as samples and are unsupported DevStack code.

# The ``localrc`` section replaces the old ``localrc`` configuration file.
# Note that if ``localrc`` is present it will be used in favor of this section.
[[local|localrc]]

# Minimal Contents
# ----------------

# While ``stack.sh`` is happy to run without ``localrc``, devlife is better when
# there are a few minimal variables set:

# If the ``*_PASSWORD`` variables are not set here you will be prompted to enter
# values for them by ``stack.sh``and they will be added to ``local.conf``.
ADMIN_PASSWORD=REPLACE_WITH_YOUR_SECRET
DATABASE_PASSWORD=$ADMIN_PASSWORD
RABBIT_PASSWORD=$ADMIN_PASSWORD
SERVICE_PASSWORD=$ADMIN_PASSWORD

# ``HOST_IP`` and ``HOST_IPV6`` should be set manually for best results if
# the NIC configuration of the host is unusual, i.e. ``eth1`` has the default
# route but ``eth0`` is the public interface.  They are auto-detected in
# ``stack.sh`` but often is indeterminate on later runs due to the IP moving
# from an Ethernet interface to a bridge on the host. Setting it here also
# makes it available for ``openrc`` to include when setting ``OS_AUTH_URL``.
# Neither is set by default.
#HOST_IP=w.x.y.z
#HOST_IPV6=2001:db8::7


# Logging
# -------

# By default ``stack.sh`` output only goes to the terminal where it runs.  It can
# be configured to additionally log to a file by setting ``LOGFILE`` to the full
# path of the destination log file.  A timestamp will be appended to the given name.
LOGFILE=$DEST/logs/stack.sh.log

# Old log files are automatically removed after 2 days to keep things neat.  Change
# the number of days by setting ``LOGDAYS``.
LOGDAYS=2

# Nova logs will be colorized if ``SYSLOG`` is not set; turn this off by setting
# ``LOG_COLOR`` false.
#LOG_COLOR=False


# Using milestone-proposed branches
# ---------------------------------

# Uncomment these to grab the milestone-proposed branches from the
# repos:
#CINDER_BRANCH=milestone-proposed
#GLANCE_BRANCH=milestone-proposed
#HORIZON_BRANCH=milestone-proposed
#KEYSTONE_BRANCH=milestone-proposed
#KEYSTONECLIENT_BRANCH=milestone-proposed
#NOVA_BRANCH=milestone-proposed
#NOVACLIENT_BRANCH=milestone-proposed
#NEUTRON_BRANCH=milestone-proposed
#SWIFT_BRANCH=milestone-proposed

# Using git versions of clients
# -----------------------------
# By default clients are installed from pip.  See LIBS_FROM_GIT in
# stackrc for details on getting clients from specific branches or
# revisions.  e.g.
# LIBS_FROM_GIT="python-ironicclient"
# IRONICCLIENT_BRANCH=refs/changes/44/2.../1

# Swift
# -----

# Swift is now used as the back-end for the S3-like object store. Setting the
# hash value is required and you will be prompted for it if Swift is enabled
# so just set it to something already:
SWIFT_HASH=66a3d6b56c1f479c8b4e70ab5c2000f5

# For development purposes the default of 3 replicas is usually not required.
# Set this to 1 to save some resources:
SWIFT_REPLICAS=1

# The data for Swift is stored by default in (``$DEST/data/swift``),
# or (``$DATA_DIR/swift``) if ``DATA_DIR`` has been set, and can be
# moved by setting ``SWIFT_DATA_DIR``. The directory will be created
# if it does not exist.
SWIFT_DATA_DIR=$DEST/data
```
修改 pip 源
```shell
mkdir ~/.pip
vim ~/.pip/pip.conf

填入：
[global]
trusted-host=mirrors.aliyun.com
index-url=http://mirrors.aliyun.com/pypi/simple
```
修改软件源为国内源，根据自己的系统版本修改
```shell
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
sudo vim /etc/apt/sources.list

填入：
# deb cdrom:[Ubuntu 16.04 LTS _Xenial Xerus_ - Release amd64 (20160420.1)]/ xenial main restricted
deb-src http://archive.ubuntu.com/ubuntu xenial main restricted #Added by software-properties
deb http://mirrors.aliyun.com/ubuntu/ xenial main restricted
deb-src http://mirrors.aliyun.com/ubuntu/ xenial main restricted multiverse universe #Added by software-properties
deb http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted multiverse universe #Added by software-properties
deb http://mirrors.aliyun.com/ubuntu/ xenial universe
deb http://mirrors.aliyun.com/ubuntu/ xenial-updates universe
deb http://mirrors.aliyun.com/ubuntu/ xenial multiverse
deb http://mirrors.aliyun.com/ubuntu/ xenial-updates multiverse
deb http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse #Added by software-properties
deb http://archive.canonical.com/ubuntu xenial partner
deb-src http://archive.canonical.com/ubuntu xenial partner
deb http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted multiverse universe #Added by software-properties
deb http://mirrors.aliyun.com/ubuntu/ xenial-security universe
deb http://mirrors.aliyun.com/ubuntu/ xenial-security multiverse
```
下载需要的压缩包，并传到服务器上
```shell
https://github.com/etcd-io/etcd/releases/download/v3.4.27/etcd-v3.4.27-linux-amd64.tar.gz
```
拷贝到文件夹`/opt/stack/devstack/files/`下
执行部署
```shell
FORCE=yes ./stack.sh
```
## 遇到的问题

1. [ERROR] /opt/stack/devstack/lib/neutron_plugins/ovn_agent:352 The q-agt/neutron-agt service must be disabled with OVN.
```shell
./stack.sh:972:stack_install_service
/opt/stack/devstack/lib/stack:32:install_neutron
/opt/stack/devstack/lib/neutron:551:install_ovn
/opt/stack/devstack/lib/neutron_plugins/ovn_agent:367:ovn_sanity_check
/opt/stack/devstack/lib/neutron_plugins/ovn_agent:352:die
[ERROR] /opt/stack/devstack/lib/neutron_plugins/ovn_agent:352 The q-agt/neutron-agt service must be disabled with OVN.
Error on exit
```
**解决方法**
删除配置中的`q-agt`，重新执行安装。

2. [ERROR] /opt/stack/devstack/lib/neutron_plugins/ovn_agent:354 The q-l3/neutron-l3 service must be disabled with OVN.
```shell
/opt/stack/devstack/lib/stack:32:install_neutron
/opt/stack/devstack/lib/neutron:551:install_ovn
/opt/stack/devstack/lib/neutron_plugins/ovn_agent:367:ovn_sanity_check
/opt/stack/devstack/lib/neutron_plugins/ovn_agent:354:die
[ERROR] /opt/stack/devstack/lib/neutron_plugins/ovn_agent:354 The q-l3/neutron-l3 service must be disabled with OVN.
Error on exit
```
**解决方法**
删除配置中的`q-l3`，重新执行安装。

3. 遇到错误`Didn't find service registered by hostname after 60 seconds`
```shell
+functions:wait_for_compute:465            echo 'Didn'\''t find service registered by hostname after 60 seconds'
Didn't find service registered by hostname after 60 seconds
+functions:wait_for_compute:466            openstack --os-cloud devstack-admin --os-region RegionOne compute service list
```
	执行如下命令，其中iot换成自己主机的名字
```shell
openstack --os-cloud devstack-admin --os-region RegionOne compute service list --host iot --service nova-compute -c ID -f value
```

4. 错误`g-api did not start`
```shell
[Call Trace]
./stack.sh:1377:start_glance
/opt/stack/devstack/lib/glance:632:die
[ERROR] /opt/stack/devstack/lib/glance:632 g-api did not start
exit_trap: cleaning up child processes
Error on exit
```

5. 执行脚本的时候卡住

执行`./stack.sh`时卡在
```shell
+functions:wait_for_compute:465            echo 'Didn'\''t find service registered by hostname after 60 seconds'
Didn't find service registered by hostname after 60 seconds
+functions:wait_for_compute:466            openstack --os-cloud devstack-admin --os-region RegionOne compute service list
```
