import asyncio
from openai import AsyncOpenAI
from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel
from agents.memory.sqlite_session import SQLiteSession

client = AsyncOpenAI(
    api_key="sk-ws-H.PHMHLYH.agcf.MEQCICqe4G5VNbb-Ian4mHpwfiW64_iRZAll2AYxQ8TaHUGpAiAKHITC2ogqYuEb-i1T5TIeluDCVcPnIOIIMiKKJm0jeg",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
model = OpenAIChatCompletionsModel(model="qwen-plus", openai_client=client)


@function_tool
def read_file(filename: str) -> str:
    """读取本地文本文件的内容。比如用户问某个文件里写了什么，就用这个工具。"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"错误：找不到文件 {filename}"
    except Exception as e:
        return f"读取文件失败: {e}"


agent = Agent(
    name="文档助手",
    instructions="你是一个能读本地文件的助手。用户问文件内容时，先用 read_file 工具读出来，再回答。",
    tools=[read_file],
    model=model,
)


async def main():
    session = SQLiteSession("file_agent.db")

    # 第一轮：让它读文件
    r1 = await Runner.run(agent, "帮我读一下 note.txt 里写了什么", session=session)
    print("我问: 帮我读一下 note.txt 里写了什么")
    print("Agent答:", r1.final_output, "\n")

    # 第二轮：基于刚才读的内容追问
    r2 = await Runner.run(agent, "刚才那个文件里提到的重点是什么？用一句话总结", session=session)
    print("我问: 刚才那个文件里提到的重点是什么？")
    print("Agent答:", r2.final_output)


if __name__ == "__main__":
    asyncio.run(main())
