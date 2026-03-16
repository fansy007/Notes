#mac #ai

## 📋 概述

本指南将帮助您在 MacBook Pro 上部署一个完全本地运行、数据私有的 AI 个人助理。该助理基于 **Qwen3.5**大语言模型和 **OpenClaw**代理框架，能够通过飞书等通讯工具接收指令，并在您的电脑上执行任务。

**最终成果**：一个能理解自然语言指令、操作您 Mac 电脑、拥有记忆能力的“数字员工”。

---

## 🖥️ 前置条件

1. **硬件**：Apple Silicon (M1/M2/M3/M4) 的 MacBook Pro，建议 **16GB 或以上内存**。
    
2. **系统**：macOS 12 (Monterey) 或更高版本。
    
3. **网络**：安装过程中需要下载软件和模型。
    
4. **终端基础**：需要熟悉基本的终端命令操作。
    
5. **安全意识**：OpenClaw 具有执行系统命令的权限，**建议首次在测试环境或非主力机上部署**。
    

---

## 🚀 安装流程

## 安装brew
/bin/zsh -c "$(curl -fsSL https://gitee.com/cunkai/HomebrewCN/raw/master/Homebrew.sh)"

### 步骤 1：安装 Ollama（本地模型引擎）

1. 访问 [Ollama 官网](https://ollama.com/)，下载 macOS 版本并安装。
    
2. 安装完成后，Ollama 服务会自动在后台启动。
    
3. **验证安装**：打开终端，运行 `ollama --version`，应显示版本号。


#### 给ollama配置代理
1. 打开或创建 Ollama 的配置文件：
    
    bash
    
    复制
    
    ```
    # 使用文本编辑器（如 nano 或 vim）打开配置文件
    nano ~/.ollama/config.json
    ```
    
2. 将以下内容写入文件并保存：
    
    json
    
    复制
    
    ```
    {
      "registry": {
        "mirrors": {
          "registry.ollama.ai": "https://ollama.modelscope.cn"
        }
      }
    }
    ```

#### 装glm后测试
```
curl -X POST http://localhost:11434/api/generate -H "Content-Type: application/json" -d '{
  "model": "glm-4.7-flash",
  "prompt": "你好，请证明API调用成功。",
  "stream": false
}'
```

    

### 步骤 2：下载 Qwen3.5 模型

1. 在终端中，运行以下命令下载推荐的 Qwen3.5 模型（根据您的内存选择）：
    
    ```
    # 方案A：极致轻量，适合后台常驻 (约1.3GB)
    ollama pull qwen3.5:2b
    
    # 方案B：平衡性能与资源，推荐大多数用户 (约2.5GB)
    ollama pull qwen3.5:4b
    
    # 方案C：能力更强，适合复杂任务 (约5GB)
    # ollama pull qwen3.5:9b
    ```
    
2. 等待下载完成。您可以通过 `ollama list`查看已下载的模型。
    

### 步骤 3：安装 OpenClaw（AI 代理框架）

**方案一：使用官方一键安装脚本（推荐）**

```
curl -fsSL https://openclaw.ai/install.sh | bash
```

脚本会自动安装 Node.js、Docker（用于安全沙箱）和 OpenClaw 本身。

**方案二：手动安装**

1. 安装 Homebrew（如果尚未安装）：
    
    ```
    /bin/bash -c "$(curl -fsSL https://gitee.com/cunkai/HomebrewCN/raw/master/Homebrew.sh)"
    ```
    
2. 安装 Node.js（版本 22 或更高）：
    
    ```
    brew install node@22
    ```
    
3. 安装 OpenClaw：
    
    ```
    npm install -g openclaw@latest
    ```
    

### 步骤 4：配置 OpenClaw 连接 Ollama (Qwen3.5)

这是最关键的一步，将 OpenClaw 的大脑设置为本地 Qwen3.5 模型。

1. **启动配置向导**：
    
    ```
    openclaw onboard --install-daemon
    ```
    
    或直接运行：
    
    ```
    openclaw onboard
    ```
    
2. 在交互式向导中，按以下提示配置：
    
    - **选择 AI 提供商**：选择 `Custom (OpenAI-compatible)`或类似选项。
        
    - **设置 API 地址**：输入 `http://localhost:11434/v1`（这是 Ollama 的本地 API 地址）。
        
    - **设置 API 密钥**：留空或任意填写（Ollama 默认无需密钥）。
        
    - **设置模型名称**：输入您下载的 Qwen3.5 模型名，例如 `qwen3.5:4b`。
        
    - **其他设置**：按需配置代理、超时等，或直接使用默认值。
        
    
3. **（可选）通过命令行直接配置**：
    
    如果您熟悉命令行，可以跳过向导，直接设置：
    
    ```
    openclaw config set llm.provider openai
    openclaw config set llm.openai.baseUrl http://localhost:11434/v1
    openclaw config set llm.openai.model qwen3.5:4b  # 替换为您的模型名
    ```
    

### 步骤 5：配置消息通道（以飞书为例）

OpenClaw 需要通过一个“通道”来接收您的指令。飞书是官方支持且配置简单的选择。

1. 在配置向导中，选择 **“Lark (Feishu)”**作为消息通道。
    
2. 按照屏幕提示，在飞书开放平台创建一个企业自建应用，获取 `App ID`和 `App Secret`。
    
3. 将这两个凭证填入 OpenClaw 的配置中。
    
4. 配置飞书应用的事件订阅和权限，并启用机器人。
    
5. 完成配置后，将机器人添加到您的飞书群或直接与它对话。
    

### 步骤 6：启动 OpenClaw 服务

1. 启动 OpenClaw 后台服务（如果安装脚本或向导未自动启动）：
    
    ```
    openclaw start
    ```
    
2. 检查服务状态：
    
    ```
    openclaw status
    ```
    
    应显示服务正在运行。
    

### 步骤 7：测试与使用

1. 在飞书中找到您配置的机器人，发送一条测试指令，例如：“你好，请告诉我当前时间。”
    
2. OpenClaw 会调用本地的 Qwen3.5 模型进行思考，并回复您。
    
3. 尝试更复杂的指令，例如：“帮我列出桌面上的所有文件。” 或 “今天的天气怎么样？”（需要安装相应技能）。
    

---

## ⚙️ 高级配置与技能管理

- **查看与安装技能**：运行 `openclaw skills`查看可用技能市场，使用 `openclaw skills install <技能名>`安装新技能（如 `weather`天气查询）。
    
- **修改配置**：配置文件通常位于 `~/.openclaw/config.json`，您可以直接编辑，或使用 `openclaw config`命令组进行修改。
    
- **查看日志**：运行 `openclaw logs`查看运行日志，便于调试。
    

---

## 🔧 常见问题 (FAQ)

1. **收不到飞书消息回复**：
    
    - 检查 OpenClaw 服务是否运行：`openclaw status`。
        
    - 检查飞书应用的“事件订阅”URL 是否正确配置为 OpenClaw 提供的地址。
        
    - 查看日志：`openclaw logs --tail=50`。
        
    
2. **Ollama 模型调用失败**：
    
    - 确认 Ollama 服务正在运行：`ollama serve`。
        
    - 测试 Ollama API：`curl http://localhost:11434/api/tags`，应返回模型列表。
        
    - 确认 OpenClaw 配置的模型名称与 `ollama list`中的完全一致。
        
    
3. **如何更新 OpenClaw 或模型**：
    
    - 更新 OpenClaw：`npm update -g openclaw`。
        
    - 更新 Ollama：重新下载安装包覆盖安装。
        
    - 更新模型：`ollama pull qwen3.5:4b`（会拉取最新版本）。
        
    
4. **如何卸载**：
    
    - 停止服务：`openclaw stop`。
        
    - 卸载 OpenClaw：`npm uninstall -g openclaw`。
        
    - 删除配置和数据目录：`rm -rf ~/.openclaw`。
        
    - 卸载 Ollama：从应用程序文件夹拖入废纸篓，并删除 `~/.ollama`。
        
    

---

## 📁 目录结构说明

安装完成后，主要目录如下：

```
~/.ollama/           # Ollama 模型存储目录
~/.openclaw/         # OpenClaw 配置、数据和日志目录
    ├── config.json  # 主配置文件
    ├── data/        # 数据库和记忆存储
    └── logs/        # 运行日志
```

**恭喜您！**现在您已经拥有了一个完全在本地运行、由最新 Qwen3.5 模型驱动的智能个人助理。它将在保护您隐私的前提下，帮助您处理各种电脑操作任务。