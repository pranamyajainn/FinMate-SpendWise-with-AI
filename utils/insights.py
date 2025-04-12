import pandas as pd

# Function to calculate the total spending for today
def calculate_total_spending(expenses, date):
    today_expenses = [exp for exp in expenses if exp["Date"] == date]
    total_spent_today = sum(exp["Amount"] for exp in today_expenses)
    return total_spent_today

# Function to provide feedback based on daily limit
def daily_limit_feedback(expenses, date, daily_limit):
    total_spent_today = calculate_total_spending(expenses, date)
    
    if total_spent_today <= daily_limit:
        return f"✅ You're within your daily budget of ₹{daily_limit}. Great job!"
    else:
        overspent = total_spent_today - daily_limit
        return f"⚠️ You've spent ₹{total_spent_today}, which is ₹{overspent} over your daily limit of ₹{daily_limit}."

# Function to calculate the average daily spending
def average_daily_spending(expenses):
    df = pd.DataFrame(expenses)
    total_spent = df["Amount"].sum()
    unique_days = len(df["Date"].unique())
    return total_spent / unique_days if unique_days > 0 else 0

# Function to generate insights (categorize spending)
def generate_financial_insight(expenses, daily_limit):
    total_spent_today = calculate_total_spending(expenses, pd.to_datetime("today").strftime("%Y-%m-%d"))
    daily_feedback = daily_limit_feedback(expenses, pd.to_datetime("today").strftime("%Y-%m-%d"), daily_limit)
    avg_spent = average_daily_spending(expenses)
    
    insights = {
        "daily_feedback": daily_feedback,
        "average_spent_per_day": avg_spent
    }
    
    return insights