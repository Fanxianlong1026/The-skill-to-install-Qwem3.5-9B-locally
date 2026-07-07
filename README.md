# The-skill-to-install-Qwem3.5-9B-locally
how to install Qwem3.5-9B locally?Here is!

# 首先下载llama_cpp_python-0.3.29-py3-none-win_amd64.whl 安装包和 Qwen3.5-9B-Q4_K_S.gguf 模型文件

我们将采用**虚拟环境**来隔离部署，这样既能保证环境干净，又方便后续管理。

---

## 前期准备

建议把这两个文件放到同一个好找的文件夹里（例如在 D 盘新建一个 `Qwen_Local` 文件夹）：

* `D:\Qwen_Local\llama_cpp_python-0.3.29-py3-none-win_amd64.whl`
* `D:\Qwen_Local\Qwen3.5-9B-Q4_K_S.gguf`

---

## 第一步：创建并激活 Python 虚拟环境

1. 在电脑左下角搜索框输入 `cmd` 或 `PowerShell`，并**以管理员身份运行**。
2. 切换到你的工作目录：
```bash
cd /d D:\Qwen_Local

```


3. 创建一个名为 `venv` 的虚拟环境：
```bash
python -m venv venv

```


4. 激活这个虚拟环境：
* 如果你使用的是 **CMD**，运行：
```bash
.\venv\Scripts\activate.bat

```


* 如果你使用的是 **PowerShell**，运行：
```bash
.\venv\Scripts\Activate.ps1

```




*(激活成功后，你的终端命令行开头会出现 `(venv)` 字样)*

---

## 第二步：安装本地离线 Wheel 包

在激活的虚拟环境中，直接通过 `pip` 安装你准备好的 `.whl` 文件。

1. 先顺手更新一下 pip（防止旧版本报错）：
```bash
python -m pip install --upgrade pip

```


2. 安装本地的 `llama_cpp_python` 包：
```bash
pip install llama_cpp_python-0.3.29-py3-none-win_amd64.whl

```


3. *(选填)* 如果你后续想用精美的 Web 界面（如 Cherry Studio、AnythingLLM）连接它，建议把服务器依赖也装上：
```bash
pip install "llama-cpp-python[server]"

```



---

## 第三步：编写聊天运行脚本

在 `D:\Qwen_Local` 目录下新建一个文本文件，重命名为 `chat.py`（注意后缀是 `.py` 而不是 `.txt`）。用记事本或其他代码编辑器打开它，粘贴以下代码：

```python
from llama_cpp import Llama

# 1. 初始化 Qwen3.5 模型
# Qwen3.5 理论上支持超长上下文，但在本地普通电脑上，建议先从 2048 或 4096 开始，防止内存/显存爆掉。
print("正在加载 Qwen3.5-9B 模型，请稍候...")
llm = Llama(
    model_path="Qwen3.5-9B-Q4_K_S.gguf",
    n_ctx=4096,         # 上下文窗口大小
    n_threads=6,        # 线程数，建议设置为你 CPU 物理核心数或核心数减 2
    n_gpu_layers=0      # 如果你的 whl 包含显卡加速且你有独立显卡，可以改写为 20~35 将层卸载到显卡；纯 CPU 填 0
)

# 2. 简单的对话循环
print("\n【模型加载成功！】输入 'exit' 或 'quit' 退出对话。\n")
while True:
    user_input = input("用户: ")
    if user_input.lower() in ['exit', 'quit']:
        print("再见！")
        break
    if not user_input.strip():
        continue
        
    # 使用 Qwen3.5 标准 Chat 格式进行流式输出
    response = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": "你是一个乐于助人的智能助手。"},
            {"role": "user", "content": user_input}
        ],
        stream=True  # 开启打字机流式效果
    )
    
    print("Qwen3.5: ", end="", flush=True)
    for chunk in response:
        delta = chunk['choices'][0]['delta']
        if 'content' in delta:
            print(delta['content'], end="", flush=True)
    print("\n" + "-"*40)

```

---

## 第四步：启动大模型对话

回到刚刚激活了虚拟环境的终端，输入以下命令运行脚本：

```bash
python chat.py

```

稍等片刻，看到系统提示 `【模型加载成功！】` 后，你就可以直接在命令行里向 Qwen3.5-9B 提问了。

---

## 💡 进阶玩法：发布为 OpenAI 兼容的 API 服务

如果你不想用黑乎乎的终端聊天，更倾向于使用现成的 UI 前端（例如第三方软件 AnythingLLM、Cherry Studio，或者浏览器插件 Page Assist），你可以直接用 `llama_cpp` 把它变成一个本地服务器。

在激活环境的终端里直接运行这行命令：

```bash
python -m llama_cpp.server --model Qwen3.5-9B-Q4_K_S.gguf --n_ctx 4096 --host 127.0.0.1 --port 8000

```

运行后，服务器会保持在后台。此时你可以在任何第三方软件中配置：

* **API 接口类型:** OpenAI
* **API 基地址 (Base URL):** `http://127.0.0.1:8000/v1`
* **API 密钥 (API Key):** 随便填（如 `sk-123456`）
* **模型名称 (Model):** `Qwen3.5-9B-Q4_K_S.gguf`

### 💡 性能优化小贴士：

1. **吐字速度慢？** `Q4_K_S` 是 4-bit 量化版，9B 模型大约需要 6-7GB 的空闲运行内存（RAM）。如果回答极慢，请检查任务管理器中内存是不是已经吃满了。
2. **CPU 线程调优：** 脚本中设置的 `n_threads=6`。如果你的 CPU 是 8 核的，设为 6 会留出一点系统余量；如果觉得慢，可以尝试直接改为 `8`。
3. **显卡加速说明：** 如果你下载的 `py3-none-win_amd64.whl` 包名字里没有带 `cuda` 或 `clblast` 字样，它默认是纯 CPU 解码。如果后面有了独立显卡，可以考虑重新装一个带 CUDA 支持的 whl 包，然后将代码里的 `n_gpu_layers` 调大，速度会有质的飞跃。
