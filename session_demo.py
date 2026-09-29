import asyncio
from openai import AsyncOpenAI
from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel
from agents.memory.sqlite_session import SQLiteSession

client = AsyncOpenAI(
    api_key="sk-ws-H.PHMHLYH.agcf.MEQCICqe4G5VNbb-Ian4mHpwfiW64_iRZAll2AYxQ8TaHUGpAiAKHITC2ogqYuEb-i1T5TIeluDCVcPnIOIIMiKKJm0jeg",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
model = OpenAIChatCompletionsModel(model="qwen-plus", openai_client=client)

agent = Agent(
    name="助手",
    instructions="你是一个友好的助手，记住用户告诉你的信息。",
    model=model,
)


async def main():
    # Session 就是把"对话历史"存起来的地方（这里用 SQLite 存在本地文件）
    session = SQLiteSession("demo_session.db")

    # 第一轮：告诉它你叫什么
    r1 = await Runner.run(agent, "你好，我叫小明，今年22岁", session=session)
    print("第1轮我问: 你好，我叫小明，今年22岁")
    print("Agent答:", r1.final_output, "\n")

    # 第二轮：不重复自我介绍，看它记不记得
    r2 = await Runner.run(agent, "我叫什么名字？我今年多大？", session=session)
    print("第2轮我问: 我叫什么名字？我今年多大？")
    print("Agent答:", r2.final_output, "\n")

    # 第三轮：再问一个问题
    r3 = await Runner.run(agent, "那我名字里有几个字？", session=session)
    print("第3轮我问: 那我名字里有几个字？")
    print("Agent答:", r3.final_output)


if __name__ == "__main__":
    asyncio.run(main())
