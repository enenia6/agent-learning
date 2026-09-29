# ============================================================
# minimal_agent.py —— 你手写的最小 Agent Loop（150行版）
# 这是你自己理解 Agent 怎么跑起来的版本，后面读框架源码就靠它对照
# ============================================================

from openai import OpenAI
import json
from datetime import datetime

# ---------- 1. 配置模型（阿里云百炼） ----------
client = OpenAI(
    api_key="sk-ws-H.PHMHLYH.agcf.MEQCICqe4G5VNbb-Ian4mHpwfiW64_iRZAll2AYxQ8TaHUGpAiAKHITC2ogqYuEb-i1T5TIeluDCVcPnIOIIMiKKJm0jeg",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
MODEL = "qwen-plus"


# ---------- 2. 定义工具 ----------
def calculate(expression: str) -> str:
    """计算一个数学表达式"""
    return str(eval(expression))


def get_current_time() -> str:
    """获取当前时间"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_weather(city: str) -> str:
    """查询某个城市的天气（假数据）"""
    fake_db = {
        "北京": "晴，26度，西北风2级",
        "上海": "多云，28度",
        "广州": "雷阵雨，31度",
    }
    return fake_db.get(city, f"{city} 今天晴，25度（假数据）")


TOOLS = {
    "calculate": calculate,
    "get_current_time": get_current_time,
    "get_weather": get_weather,
}

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "计算一个数学表达式",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "要计算的数学表达式，例如 2+3*5"}
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前时间",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询某个城市的天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "要查询天气的城市名，例如 北京、上海"}
                },
                "required": ["city"],
            },
        },
    },
]


# ---------- 3. Agent Loop 本体 ----------
def run_agent(user_message: str, max_turns: int = 10):
    messages = [
        {"role": "system", "content": "你是一个会用工具的助手。需要计算或查时间时就调用工具，不要自己瞎猜。"},
        {"role": "user", "content": user_message},
    ]

    for turn in range(max_turns):
        print(f"\n===== 第 {turn + 1} 次调用模型 =====")

        resp = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOL_SCHEMAS,
        )
        msg = resp.choices[0].message
        messages.append(msg.model_dump(exclude_none=True))

        if not msg.tool_calls:
            print(f"\n[最终答案] {msg.content}")
            return msg.content

        for tc in msg.tool_calls:
            name = tc.function.name
            args = json.loads(tc.function.arguments)
            print(f"  → 模型要调工具: {name}({args})")
            try:
                result = TOOLS[name](**args)
            except Exception as e:
                result = f"工具调用失败: {type(e).__name__}: {e}"
            print(f"  ← 工具返回: {result}")
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": result,
            })

    print("\n[警告] 达到最大轮次还没结束，强制退出")


if __name__ == "__main__":
    run_agent("现在几点？北京天气怎么样？顺便算一下 100*100")
