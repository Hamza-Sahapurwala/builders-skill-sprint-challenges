"""
Challenge 4: The Full Agent — Tools + Memory + Streaming
Combine everything into one powerful agent.
Model: Amazon Nova Pro via Bedrock

Instructions:
  1. Fill in ALL the TODO sections
  2. Run: python starter.py
  3. Have a full conversation using all tools!
"""

import os
os.environ["BYPASS_TOOL_CONSENT"] = "true"

from datetime import date, datetime

MODEL = "us.amazon.nova-pro-v1:0"


# ============================================================
# TODO 1: Import everything you need
# ============================================================
# Hint: You need Agent, tool from strands
#       calculator, mem0_memory from strands_tools

# Your imports here
from strands import Agent, tool
from strands_tools import mem0_memory
from strands_tools import calculator
import requests


# ============================================================
# TODO 2: Create a streaming callback handler
# ============================================================
# This function gets called for every chunk of text the agent generates
# Hint:
# def stream_callback(**kwargs):
#     if "data" in kwargs:
#         print(kwargs["data"], end="", flush=True)
#     elif "current_tool_use" in kwargs and kwargs["current_tool_use"].get("name"):
#         print(f"\n🔧 Using tool: {kwargs['current_tool_use']['name']}")

# Your callback here

def stream_callback(**kwargs):
    if "data" in kwargs:
        print(kwargs["data"], end="", flush=True)
    elif "current_tool_use" in kwargs and kwargs["current_tool_use"].get("name"):
        print(f"\n🔧 Using tool: {kwargs['current_tool_use']['name']}")


# ============================================================
# TODO 3: Create custom tools — weather and age_calculator
# ============================================================
# Reuse your code from Challenge 2!

# Your tools here

@tool
def weather(city: str) -> str:
    """Get the current weather for a city.
    Args:
        city: The name of the city.
    """
    # TODO: Implement this function
    try:
        res =  requests.get(f"https://wttr.in/{city}?format=j1")
        return res.json()
    except:
        return f"The weather in {city} is sunny, 28°C"
    
@tool
def age_calculator(birth_date: str) -> str:
    """Calculate age from a birth date.
    Args:
        birth_date: Date of birth in YYYY-MM-DD format.
    Returns:
        A string representing the exact age in years, months, and days.
    """
    # Parse the birth date string into a date object
    try:
        birth = datetime.strptime(birth_date, "%Y-%m-%d").date()
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD."
        
    today = date.today()
    
    # Check if the birth date is in the future
    if birth > today:
        return "Birth date cannot be in the future."
    
    # 1. Calculate initial differences
    years = today.year - birth.year
    months = today.month - birth.month
    days = today.day - birth.day
    
    # 2. Adjust for negative days (day of the month hasn't been reached yet)
    if days < 0:
        months -= 1
        # Find the last day of the previous month
        # We handle January rolling back to December by shifting the year
        prev_month_year = today.year if today.month > 1 else today.year - 1
        prev_month = today.month - 1 if today.month > 1 else 12
        
        # Total days in that previous month = (current month's 1st day) - (1 day)
        last_day_prev_month = (date(today.year, today.month, 1) - date(prev_month_year, prev_month, 1)).days
        
        # If it rolls over into a different year/month structure entirely, standard timedelta math works:
        days += (date(today.year, today.month, 1) - date(prev_month_year, prev_month, 1)).days

    # 3. Adjust for negative months (birthday month hasn't been reached yet)
    if months < 0:
        years -= 1
        months += 12
        
    return f"{years} years, {months} months, and {days} days"


# ============================================================
# TODO 4: Create the full agent with ALL tools + memory + streaming
# ============================================================
# Hint: Agent(
#     model=MODEL,
#     tools=[calculator, weather, age_calculator, mem0_memory],
#     callback_handler=stream_callback,
#     system_prompt="..."
# )

agent = Agent(model=MODEL, tools=[calculator, weather, age_calculator, mem0_memory], callback_handler=stream_callback, system_prompt="You are a smart Assistant. You must store and remember user preferences when asked")  # Replace this line


# ============================================================
# TODO 5: Interactive chat loop
# ============================================================

print("🤖 Full Agent Ready! Type 'quit' to exit.")
print("Try: 'What's the weather in Delhi and how old is someone born 2000-01-01?'")
print("Try: 'Remember my name is [name]' then 'What's my name?'\n")

while True:
    try:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("Bye! 👋")
            break

        print("\nAgent: ", end="")
        # TODO: Call the agent with user_input
        response = agent(user_input)
        print("\n")

    except KeyboardInterrupt:
        print("\nBye! 👋")
        break

print("\n✅ Challenge 4 complete! 🏆")
