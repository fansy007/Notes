# Mac 远程调用 Windows QMT（xtquant）配置文档

> 建立时间：2026-03-17
> 目的：在 Mac（爱因斯坦 AI）上通过 SSH 远程调用 Windows QMT 数据，实现股票五维评分自动化

---

## 环境信息

| 项目 | 内容 |
|------|------|
| Mac 用户 | hg26502 |
| Windows IP | 192.168.7.102（局域网，同一 WiFi）|
| Windows 用户 | qjgeng |
| Windows Python | C:\Python311\python.exe（3.11.0）|
| QMT 安装目录 | E:\qmt |
| xtquant 目录 | E:\xtquant |
| 评分脚本 | E:\scripts\wdpf_score.py |

---

## 一、Windows 开启 SSH 服务

### 安装 OpenSSH Server

以管理员身份运行 PowerShell：

```powershell
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'
```

> ⚠️ 安装后需要**重启 Windows** 才能生效

### 验证服务状态

```powershell
Get-Service -Name *ssh*
```

---

## 二、Mac 配置免密 SSH 登录

### Mac 公钥位置

```
~/.ssh/id_rsa.pub
```

### Windows 管理员账户公钥配置

管理员账户（Administrator/qjgeng）的公钥**不能**放在用户目录，必须放在系统目录：

```powershell
# 以管理员身份运行 PowerShell
New-Item -ItemType Directory -Force -Path "C:\ProgramData\ssh"

Set-Content -Path "C:\ProgramData\ssh\administrators_authorized_keys" -Value "你的Mac公钥内容"

# 设置权限（关键步骤，缺少会导致公钥不生效）
icacls "C:\ProgramData\ssh\administrators_authorized_keys" /inheritance:r /grant "SYSTEM:(F)" /grant "BUILTIN\Administrators:(F)"
```

> ⚠️ 普通用户公钥放 `~/.ssh/authorized_keys`，管理员必须放 `C:\ProgramData\ssh\administrators_authorized_keys`

### 测试连接

在 Mac 终端运行：

```bash
ssh qjgeng@192.168.7.102 "echo 连接成功"
```

---

## 三、xtquant 环境说明

### 目录结构

```
E:\xtquant\
├── xtdata.py          # 行情数据接口
├── xttrader.py        # 交易接口
├── datacenter.cp311-win_amd64.pyd   # Python 3.11 扩展
├── xtpythonclient.cp311-win_amd64.pyd
└── __init__.py
```

### 使用方式

xtquant **不需要 pip install**，直接把 `E:\` 加入 sys.path 即可：

```python
import sys
sys.path.insert(0, 'E:\\')
import xtquant.xtdata as xtdata
xtdata.connect()  # 需要 QMT 客户端在后台运行
```

### 重要限制

> ⚠️ **xtquant 必须在 QMT 客户端登录运行的情况下才能连接**
> 每次使用前确认 QMT 已启动并登录

---

## 四、常用数据接口

### ⚠️ 重要：必须先下载历史数据到本地缓存

xtquant 的 `get_market_data()` 和 `get_financial_data()` **只读取本地缓存**，不会自动联网拉取。
如果本地没有缓存，返回的数据会是空的或不完整。

**行情数据和财务数据都需要单独下载：**

```python
import time

# 1. 下载日线行情
stocks = ['300017.SZ','002335.SZ','300442.SZ','002518.SZ','300113.SZ','000905.SH']
xtdata.download_history_data2(
    stocks, period='1d',
    start_time='20230101',
    incrementally=True   # 增量更新，只下载缺失部分
)
time.sleep(5)

# 2. 下载财务数据（耗时较长，建议在Windows本地直接运行，不要通过SSH）
xtdata.download_financial_data(
    stocks,
    table_list=['Income'],   # Income=利润表，Balance=资产负债表
    start_time='20230101',
    incrementally=True
)
time.sleep(10)  # 财务数据下载较慢，等待时间要长一些
```

> ⚠️ **财务数据下载耗时较长，通过 SSH 远程执行会超时断开**
> 建议在 Windows 本地直接运行下载脚本：`C:\Python311\python.exe E:\scripts\download_data.py`
> 下载完成后，再通过 SSH 调用评分脚本读取数据

### 行情数据读取

```python
# 获取日线数据（必须先 download，否则数据为空）
data = xtdata.get_market_data(
    ['close', 'high', 'low', 'open', 'volume'],
    ['300113.SZ'],
    period='1d',
    start_time='20230101',
    end_time='20260317'
)

# 取数据（注意：用 .loc 而不是 []）
closes = data['close'].loc['300113.SZ']
```

### 股票代码格式

| 市场 | 格式 | 示例 |
|------|------|------|
| 深交所 | XXXXXX.SZ | 300113.SZ |
| 上交所 | XXXXXX.SH | 600000.SH |
| 中证500指数 | 000905.SH | 000905.SH |
| 创业板指 | 399006.SZ | 399006.SZ |

> ⚠️ 399905.SZ（中证500深交所版）在 QMT 里无数据，用 000905.SH

### 财务数据

```python
fin = xtdata.get_financial_data(
    ['300113.SZ'],
    table_list=['Income', 'Balance'],
    start_time='20230101'
)

# 取利润表
income = fin['300113.SZ']['Income']

# 关键字段
# operating_revenue  营业收入
# net_profit_incl_min_int_inc  净利润
# s_fa_eps_basic  基本每股收益
```

---

## 五、从 Mac 远程执行脚本

### 整体架构

```
Mac（爱因斯坦 AI / QClaw）
    │
    │  SSH 免密登录（局域网 192.168.7.102）
    │
    ▼
Windows（qjgeng@192.168.7.102）
    │
    │  C:\Python311\python.exe 执行脚本
    │
    ▼
E:\scripts\wdpf_score.py
    │
    │  import sys; sys.path.insert(0, 'E:\\')
    │  import xtquant.xtdata as xtdata
    │
    ▼
E:\xtquant（xtquant 库）
    │
    │  xtdata.connect() 连接本地 QMT 进程
    │
    ▼
E:\qmt（QMT 客户端，必须登录运行）
    │
    └── 返回行情/财务数据 → 计算评分 → Server酱 → 微信推送
```

### 关键技术点：xtquant 如何被调用

xtquant 不是通过 pip 安装的标准包，而是放在 `E:\xtquant\` 目录下的本地库。
调用方式是在脚本开头手动把 `E:\` 加入 Python 的模块搜索路径：

```python
import sys
sys.path.insert(0, 'E:\\')   # 让 Python 能找到 E:\xtquant\
import xtquant.xtdata as xtdata
xtdata.connect()              # 连接本机运行中的 QMT 进程（走 127.0.0.1:58610）
```

`xtdata.connect()` 本质上是连接 QMT 客户端在本地开启的数据服务（端口 58610），
所以脚本必须在 **Windows 本机**运行，不能在 Mac 上直接 import xtquant。

### Mac 触发的完整流程

```
1. Mac 上（爱因斯坦）发起 SSH 命令
   ↓
   ssh qjgeng@192.168.7.102 "C:\Python311\python.exe E:\scripts\wdpf_score.py"

2. SSH 连接到 Windows（免密，用公钥认证）
   ↓
3. Windows 上启动 Python 3.11 进程执行脚本
   ↓
4. 脚本把 E:\ 加入 sys.path，import xtquant
   ↓
5. xtdata.connect() 连接本地 QMT 数据服务（127.0.0.1:58610）
   ↓
6. 调用 xtdata.get_market_data() / get_financial_data() 拉取数据
   ↓
7. 计算五维评分
   ↓
8. 通过 Server酱 API 推送结果到微信
   ↓
9. SSH 命令返回，Mac 收到执行结果
```

### Mac 上的调用方式

**直接执行（手动触发）：**
```bash
ssh qjgeng@192.168.7.102 "C:\Python311\python.exe E:\scripts\wdpf_score.py"
```

**通过 QClaw 定时任务自动触发（每日15:35）：**
```
cron job → agentTurn → 爱因斯坦执行 exec(ssh ...) → Windows 跑脚本 → 微信推送
```

**在 Mac Python 脚本中调用：**
```python
import subprocess
result = subprocess.run(
    ['ssh', 'qjgeng@192.168.7.102',
     r'C:\Python311\python.exe E:\scripts\wdpf_score.py'],
    capture_output=True, text=True, timeout=60
)
print(result.stdout)
```

### 注意事项

1. **编码问题**：Windows 终端默认 GBK，脚本中避免使用 emoji（⚠️✅等），改用文字 [警][好]
2. **路径分隔符**：SSH 命令中 Windows 路径用 `\`，在 bash 字符串中需转义为 `\\`
3. **QMT 必须开启**：每次运行前确认 QMT 已登录，否则 xtdata.connect() 报错
4. **xtquant 只能本地调用**：不能从 Mac 直接 import，必须通过 SSH 在 Windows 上执行

---

## 六、已部署的脚本

### 五维买入评估脚本

- **位置**：`E:\scripts\wdpf_score.py`
- **功能**：计算5只股票的五维评分 + CS500环境分，推送到微信
- **运行方式**：
  ```bash
  # Mac 上远程触发
  ssh qjgeng@192.168.7.102 "C:\Python311\python.exe E:\scripts\wdpf_score.py"
  ```

### 评估的股票列表

| 代码 | 名称 |
|------|------|
| 300017.SZ | 网宿科技 |
| 002335.SZ | 科华数据 |
| 300442.SZ | 润泽科技 |
| 002518.SZ | 科士达 |
| 300113.SZ | 顺网科技 |

---

## 七、待解决问题

- [ ] 科华数据（002335）、科士达（002518）财务数据越界，需排查
- [ ] 换手率数据：QMT 个股行情接口无 `turnoverRate` 字段，目前用成交量替代
- [ ] Windows IP 可能变化（DHCP），如变化需更新 SSH 配置

---

## 八、故障排查

| 问题 | 原因 | 解决 |
|------|------|------|
| SSH Permission denied | 公钥未生效 | 检查 `C:\ProgramData\ssh\administrators_authorized_keys` 权限 |
| xtquant 连接失败 | QMT 未启动 | 打开 QMT 客户端并登录 |
| KeyError: '000905.SH' | 用了 `[]` 取数据 | 改用 `.loc['000905.SH']` |
| UnicodeEncodeError | Windows GBK 不支持 emoji | 脚本中用文字替代 emoji |

---

**关联文档**：[[顺网科技五维买入评估系统.md]]、[[cs500_daily_score.py]]
**作者**：haining 与 AI助手爱因斯坦
