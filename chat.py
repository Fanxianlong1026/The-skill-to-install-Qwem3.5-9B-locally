"""
Qwen3.5 GGUF 本地聊天脚本
依赖: pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu124
硬件: RTX 5060 Laptop 8GB 显存 / 16GB 内存
"""

from llama_cpp import Llama

# ============ 配置区 ============
MODEL_PATH = r"D:\NewCode\Qwen\models\Qwen3.5-9B-Q4_K_S.gguf"  # 改成你下载的文件路径
N_GPU_LAYERS = -1      # -1=尽量全放GPU; 若OOM改成具体数字如 24
N_CTX = 8192           # 上下文长度; 显存紧就改 4096
SYSTEM_PROMPT = "你是一个有用的中文助手，回答简洁准确。"
# ================================


def load_model():
    print("正在加载模型，请稍候...")
    llm = Llama(
        model_path=MODEL_PATH,
        n_gpu_layers=N_GPU_LAYERS,
        n_ctx=N_CTX,
        n_batch=256,
        verbose=False,  # 改 True 可看到 "offloaded XX/XX layers to GPU" 等加载日志
    )
    print("模型加载完成！输入内容开始对话（输入 exit / quit 退出，clear 清空历史）\n")
    return llm


def main():
    llm = load_model()
    history = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        try:
            user_input = input("你: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见！")
            break

        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            print("再见！")
            break
        if user_input.lower() == "clear":
            history = [{"role": "system", "content": SYSTEM_PROMPT}]
            print("（已清空对话历史）\n")
            continue

        history.append({"role": "user", "content": user_input})

        # 流式输出（打字机效果）
        print("助手: ", end="", flush=True)
        reply = ""
        stream = llm.create_chat_completion(
            messages=history,
            temperature=0.7,
            max_tokens=1024,
            stream=True,
        )
        for chunk in stream:
            delta = chunk["choices"][0]["delta"]
            if "content" in delta:
                piece = delta["content"]
                print(piece, end="", flush=True)
                reply += piece
        print("\n")

        history.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
