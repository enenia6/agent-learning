import asyncio
from datetime import datetime
from openai import AsyncOpenAI
from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel

# ---------- 配置百炼 ----------
client = AsyncOpenAI(
    api_key="sk-ws-H.PHMHLYH.agcf.MEQCICqe4G5VNbb-Ian4mHpwfiW64_iRZAll2AYxQ8TaHUGpAiAKHITC2ogqYuEb-i1T5TIeluDCVcPnIOIIMiKKJm0jeg",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
model = OpenAIChatCompletionsModel(model="qwen-plus", openai_client=client)


# ---------- 定义工具：一个 @function_tool 装饰器就够了 ----------
@function_tool
def calculate(expression: str) -> str:
    """计算一个数学表达式，比如 calculate('2+3*5')"""
    return str(eval(expression))


@function_tool
def get_current_time() -> str:
    """获取当前时间"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@function_tool
def get_weather(city: str) -> str:
    """查询某个城市的天气"""
    return f"{city}：晴，26度"
@function_tool
def read_file(filename: str) -> str:
    """读取本地文本文件的内容"""
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


# ---------- 定义 Agent ----------
agent = Agent(
    name="助手",
    instructions="你是一个会用工具的助手。需要计算或查时间时就调用工具，不要自己瞎猜。",
    tools=[calculate, get_current_time, get_weather, read_file],

    model=model,
)


async def main():
    result = await Runner.run(agent, "帮我读一下 note.txt 里写了什么")

    print("\n[最终答案]", result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
