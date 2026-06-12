"""
Challenge 2: Adding Tools to Your Agent
Give your agent a calculator, weather tool, and age calculator.
Model: Amazon Nova Pro via Bedrock

Instructions:
  1. Fill in the TODO sections below
  2. Run: python starter.py
  3. Needs AWS credentials configured (aws configure)
"""

import os
os.environ["BYPASS_TOOL_CONSENT"] = "true"

from datetime import date, datetime
from strands import Agent, tool
from strands_tools import calculator
import requests

MODEL = "us.amazon.nova-pro-v1:0"


# ============================================================
# TODO 1: Create a custom weather tool
# ============================================================
# Hint: Use the @tool decorator
# The function should take a city name and return weather info
# Use wttr.in API: https://wttr.in/{city}?format=j1
# Or return dummy data: f"The weather in {city} is sunny, 28°C"

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


# ============================================================
# TODO 2: Create a custom age calculator tool
# ============================================================
# Hint: Use @tool decorator
# Take a birth_date string in YYYY-MM-DD format
# Calculate the age using datetime

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
# TODO 3: Create an agent with all tools
# ============================================================
# Hint: Agent(model=MODEL, tools=[calculator, weather, age_calculator], ...)

agent = Agent(model=MODEL, tools=[calculator, weather, age_calculator])  # Replace this line


# ============================================================
# TODO 4: Test the agent with different questions
# ============================================================

# Test math
print("🧮 Math test:")
response = agent("What is 42 * 17?")

# Test weather
print("\n🌤️ Weather test:")
response = agent("What's the weather in Chennai?")

# Test age
print("\n🎂 Age test:")
response = agent("How old is someone born on 2000-05-15?")


print("\n✅ Challenge 2 complete!")
