from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    set_tracing_disabled,
)
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

# -----------------------------------------
# Setup
# -----------------------------------------
load_dotenv()
set_tracing_disabled(True)

# Gemini (OpenAI-Compatible) Client
client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Model (Gemini)
model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",     # Model name you are using
    openai_client=client
)

# -----------------------------------------
# MAIN AI AGENT (Project-Specific)
# -----------------------------------------
main_agent = Agent(
    name="TextbookAssistant",
    instructions="""
You are the official assistant for the Physical AI & Humanoid Robotics textbook.
You must answer questions ONLY based on the provided context. Do not use any external knowledge.
If the provided context does not contain the answer to the question, explicitly state that the information is not available in the provided context.

Your expertise covers:
- robotics concepts,
- humanoid control systems,
- ROS 2 fundamentals,
- simulation environments,
- Python explanations when needed.

Keep answers clear and helpful, and always cite the source of your information from the provided context.
""",
    model=model
)

# -----------------------------------------
# TEST RUN
# -----------------------------------------
if __name__ == "__main__":
    result = Runner.run_sync(
        main_agent,
        ""
    )
    print("\nFINAL OUTPUT:\n")
    print(result.final_output)
