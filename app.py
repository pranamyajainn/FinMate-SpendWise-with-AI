import streamlit as st
from utils import categorize, insights, chatbot  # placeholder for later
import streamlit as st
from utils.categorize import categorize_expense
#from utils.insights import generate_financial_insight
#from utils.chatbot import get_chatbot_response


# Now you can set the page configuration
st.set_page_config(page_title="FinMate — SpendWise with AI", layout="wide")
# Function to apply custom CSS
def apply_custom_css():
    with open('style.css', 'r') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Apply custom CSS before setting the page configuration
apply_custom_css()

# Initialize default badges if not present
if "default_badges" not in st.session_state:
    st.session_state.default_badges = {
        "welcome": "Welcome to FinMate! 👋",
        "first_expense": "First Expense Tracked 📝",
        "first_goal": "Goal Setter 🎯",
        "budget_master": "Budget Master 💰",
        "saving_star": "Saving Star ⭐",
        "streak_starter": "7-Day Streak 🔥",
        "streak_master": "30-Day Streak 🔥",
        "streak_legend": "100-Day Streak 🌟"
    }

# Initialize gamification state
if "xp" not in st.session_state:
    st.session_state.xp = 0
if "level" not in st.session_state:
    st.session_state.level = 1
if "badges" not in st.session_state:
    st.session_state.badges = []
if "streaks" not in st.session_state:
    st.session_state.streaks = {"current": 0, "best": 0}
if "challenges" not in st.session_state:
    st.session_state.challenges = []
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Dashboard"

# XP rewards configuration
XP_REWARDS = {
    "add_expense": 10,
    "set_goal": 25,
    "complete_goal": 100,
    "track_streak": 15,
    "under_budget": 20,
    "complete_challenge": 50,
    "first_chat": 20,      # First time using chatbot
    "daily_login": 10,     # Logging in daily
    "budget_setup": 30,    # Setting up initial budget
    "streak_milestone": 50
}

# Tab Mapping
tab_mapping = {"Dashboard": 0, "Track Expenses": 1, "Set Goals": 2, "Insights": 3, "Chatbot": 4}

# App Title
st.title("FinMate — SpendWise with AI 💼✨")
st.markdown("#### Smart budgeting. Real savings. Built with AI.")

# 🔝 Top Navigation Tabs
tab = st.tabs(["Dashboard", "Track Expenses", "Set Goals", "Insights", "Chatbot"])

# Navigate to the selected active tab
active_tab_index = tab_mapping[st.session_state.active_tab]
current_tab = tab[active_tab_index]


def add_xp(amount):
    """Add XP and check for level up"""
    st.session_state.xp += amount
    if st.session_state.xp >= st.session_state.level * 100:
        level_up()

def level_up():
    """Handle level up logic"""
    st.session_state.level += 1
    st.balloons()
    st.success(f"🎉 Level Up! You're now level {st.session_state.level}!")
    
    # Add level-specific rewards
    if st.session_state.level == 5:
        st.session_state.badges.append("Financial Novice 🌟")
    elif st.session_state.level == 10:
        st.session_state.badges.append("Money Master 💰")
    elif st.session_state.level == 20:
        st.session_state.badges.append("Budget Guru 🏆")

# Each tab content
with tab[0]:  # Dashboard
    # Add level and XP display at the top
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🎮 Level", f"{st.session_state.level}")
    with col2:
        next_level_xp = st.session_state.level * 100
        st.metric("⭐ XP", f"{st.session_state.xp}/{next_level_xp}")
    with col3:
        st.metric("🔥 Streak", f"{st.session_state.streaks['current']} days")
    
    # Add XP progress bar
    xp_progress = st.session_state.xp / next_level_xp
    st.progress(xp_progress)
    st.caption(f"XP needed for Level {st.session_state.level + 1}: {next_level_xp - st.session_state.xp}")
    st.subheader("📊 Dashboard Overview")

    # 🔹 User Inputs
    st.markdown("### 💼 Monthly Income & Plans")
    salary = st.number_input("Enter your total monthly salary (₹):", min_value=0, value=30000, step=500)
    planned_savings = st.number_input("Enter your planned savings (₹):", min_value=0, value=10000, step=500)
    total_expenses = st.number_input("Enter your expected monthly expenses (₹):", min_value=0, value=15000, step=500)

    # 🔹 Calculate Unspent Amount
    unspent = salary - (planned_savings + total_expenses)
    if unspent < 0:
        st.error("⚠️ Your planned savings and expenses exceed your salary!")
        unspent = 0

    # 🔹 Metrics
    st.metric("Planned Savings", f"₹{planned_savings}")
    st.metric("Expected Expenses", f"₹{total_expenses}")
    st.metric("Unallocated Amount", f"₹{unspent}")

    # 🔹 Savings Progress Bar
    st.markdown("### 🏦 Savings Progress")
    current_savings = 0  # You can update this dynamically later
    st.progress(min(current_savings / planned_savings, 1.0))
    st.caption(f"₹{current_savings} / ₹{planned_savings} saved")

    # 🔹 Pie Chart - Salary Breakdown
    st.markdown("### 📉 Salary Distribution Breakdown")
    import matplotlib.pyplot as plt

    labels = ['Expenses', 'Planned Savings', 'Unspent']
    sizes = [total_expenses, planned_savings, unspent]
    colors = ['#FF6F61', '#6EC1E4', '#9CCC65']

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    ax1.axis('equal')
    st.pyplot(fig1)

    # 🔹 Quick Links to other sections
    st.markdown("### 🔗 Quick Links")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Track Expenses"):
            st.session_state.active_tab = "Track Expenses"
            st.rerun()  # Updated from st.experimental_rerun()
    with col2:
        if st.button("Set Goals"):
            st.session_state.active_tab = "Set Goals"
            st.rerun()  # Updated from st.experimental_rerun()
    with col3:
        if st.button("Insights"):
            st.session_state.active_tab = "Insights"
            st.rerun()  # Updated from st.experimental_rerun()
        # 🔹 Recent Transactions
    import pandas as pd
    recent_transactions = {
        'Date': ['2025-04-10', '2025-04-09', '2025-04-08'],
        'Category': ['Groceries', 'Shopping', 'Bills'],
        'Amount (₹)': [1200, 2000, 1500]
    }
    df = pd.DataFrame(recent_transactions)
    st.markdown("### 📝 Recent Transactions")
    st.dataframe(df)

    # 🔹 Personalized Recommendations
    st.markdown("### 💡 Financial Tips")
    st.info("Consider reducing your 'Dining Out' expenses to save ₹2000 this month!")
with tab[1]:  # Track Expenses
    st.subheader("💸 Track Your Expenses")

    # Initialize session state for storing expenses
    if "expenses" not in st.session_state:
        st.session_state.expenses = []

    # Expense Input Form
    with st.form("expense_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            expense_date = st.date_input("Date")
        with col2:
            amount = st.number_input("Amount (₹)", min_value=0.0, step=10.0)
            notes = st.text_input("Notes (optional)")

        submitted = st.form_submit_button("➕ Add Expense")
        if submitted:
            # Categorize the expense based on its amount
            category_result = categorize_expense(amount)
            
            # Append the expense to the session state with the auto-categorized category
            st.session_state.expenses.append({
                "Date": expense_date.strftime("%Y-%m-%d"),
                "Category": category_result,  # Use the categorized result
                "Amount (₹)": amount,
                "Notes": notes
            })
            st.success(f"Expense for ₹{amount} categorized as: {category_result} added successfully!")

    # Display Stored Expenses
    if st.session_state.expenses:
        st.markdown("### 📋 Expense History")
        import pandas as pd
        df = pd.DataFrame(st.session_state.expenses)
        st.dataframe(df)

        # Category-wise Total
        st.markdown("### 📊 Category-wise Spending")
        category_totals = df.groupby("Category")["Amount (₹)"].sum().reset_index()

        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        ax.bar(category_totals["Category"], category_totals["Amount (₹)"], color="#4CAF50")
        ax.set_xlabel("Category")
        ax.set_ylabel("Total Spent (₹)")
        ax.set_title("Spending by Category")
        st.pyplot(fig)
    else:
        st.info("No expenses added yet. Start tracking now!")

    if submitted:
        # Add XP reward for tracking expense
        st.session_state.xp += XP_REWARDS["add_expense"]
        if st.session_state.xp >= st.session_state.level * 100:
            st.session_state.level += 1
            st.balloons()
            st.success(f"🎉 Level Up! You're now level {st.session_state.level}!")
        
        # Check if under budget
        if amount <= st.session_state.global_daily_limit:
            st.session_state.xp += XP_REWARDS["under_budget"]
            st.success(f"🎯 Bonus XP earned for staying under budget! (+{XP_REWARDS['under_budget']} XP)")
with tab[2]:  # Set Goals
    st.subheader("🎯 Set Your Savings Goals")

    # Initialize goals list
    if "goals" not in st.session_state:
        st.session_state.goals = []

    # Add New Goal Form (only visible if under 10 goals)
    if len(st.session_state.goals) < 10:
        with st.form("add_goal_form", clear_on_submit=True):
            goal_name = st.text_input("Goal Name", value="My Goal")
            target_amount = st.number_input("Target Amount (₹)", min_value=100.0, step=100.0)
            deadline = st.date_input("Deadline")
            submitted = st.form_submit_button("➕ Add Goal")

            if submitted:
                st.session_state.goals.append({
                    "name": goal_name,
                    "target": target_amount,
                    "deadline": deadline,
                    "current": 0  # Placeholder for now
                })
                st.success(f"Goal '{goal_name}' added!")

    # Display All Goals
    if st.session_state.goals:
        st.markdown("### 📋 Your Goals")
        for i, goal in enumerate(st.session_state.goals):
            with st.expander(f"🎯 {goal['name']} (Deadline: {goal['deadline']})"):
                st.markdown(f"**Target:** ₹{goal['target']}")
                current = goal.get("current", 0)
                progress = min(current / goal['target'], 1.0)
                st.progress(progress)
                st.caption(f"₹{current} / ₹{goal['target']} saved")
    else:
        st.info("No goals set yet. Add a goal to start tracking!")
    if submitted:
        # Add XP reward for setting a goal
        st.session_state.xp += XP_REWARDS["set_goal"]
        st.success(f"🎯 Goal added! (+{XP_REWARDS['set_goal']} XP)")
        
        # Add challenge
        st.session_state.challenges.append({
            "type": "goal",
            "name": f"Complete {goal_name}",
            "target": target_amount,
            "deadline": deadline,
            "completed": False
        })
with tab[3]:  # Insights
    st.subheader("💡 Smart Financial Insights")
    st.sidebar.markdown("### 🎯 Active Challenges")
    
    # Highlight active challenges with progress bar
    for challenge in st.session_state.challenges:
        if not challenge["completed"]:
            st.sidebar.markdown(f"- **{challenge['name']}**")
            st.sidebar.progress(challenge.get("progress", 0) / 100)
            if st.sidebar.button(f"✅ Complete: {challenge['name']}"):
                challenge["completed"] = True
                st.session_state.xp += XP_REWARDS["complete_challenge"]
                st.balloons()
                st.success(f"🎉 Challenge completed! (+{XP_REWARDS['complete_challenge']} XP)")
        else:
            st.sidebar.markdown(f"✔️ ~~{challenge['name']}~~")

    # Global daily limit setup with dynamic updates
    st.markdown("### 🛡 Set Your Daily Spending Shield")
    st.session_state.global_daily_limit = st.number_input(
        "Enter your Global Daily Spending Limit (₹)",
        value=st.session_state.get("global_daily_limit", 100),  # Default to 100 if not set
        min_value=100,
        step=50
    )
    st.info(f"💡 Your current daily limit is ₹{st.session_state.global_daily_limit}. Adjust it to match your goals!")

    # Daily expense data store
    if "daily_expenses" not in st.session_state:
        st.session_state.daily_expenses = []

    # Add today's expense with emoji categories
    st.markdown("### ➕ Add Your Daily Expense")
    expense_date = st.date_input("📅 Date", key="insight_date")
    category = st.selectbox(
        "📂 Category", 
        ["🛒 Groceries", "🍽 Dining Out", "🎮 Entertainment", "💡 Utilities", "🚗 Transport", "🛍 Shopping", "🌈 Others"], 
        key="insight_category"
    )
    amount = st.number_input("💲 Amount (₹)", min_value=0, step=50, key="insight_amount")

    if st.button("➕ Add Expense"):
        st.session_state.daily_expenses.append({
            "Date": expense_date.strftime("%Y-%m-%d"),
            "Category": category,
            "Amount": amount
        })
        st.success(f"🎉 Expense for {category} of ₹{amount} added successfully!")

        # AI-powered feedback with emoji reactions
        st.markdown("### 🧠 AI Insight for This Entry")
        today_expenses = [
            exp for exp in st.session_state.daily_expenses
            if exp["Date"] == expense_date.strftime("%Y-%m-%d")
        ]
        total_today = sum(exp["Amount"] for exp in today_expenses)

        if total_today <= st.session_state.global_daily_limit:
            st.success(f"✅ You're within your daily budget of ₹{st.session_state.global_daily_limit}. 🌟 Keep it up! 🎯")
        else:
            overspent = total_today - st.session_state.global_daily_limit
            st.warning(f"⚠️ You've spent ₹{total_today}, which is ₹{overspent} over your daily limit of ₹{st.session_state.global_daily_limit}. 🛑 Consider cutting back tomorrow!")

    # Show Tracked Expenses
    if st.session_state.daily_expenses:
        import pandas as pd
        df = pd.DataFrame(st.session_state.daily_expenses)

        st.markdown("### 📝 Tracked Expenses")
        st.dataframe(df)

        # Spending Breakdown Chart with animations
        st.markdown("### 📊 Spending Breakdown by Category")
        import matplotlib.pyplot as plt
        import seaborn as sns
        
        category_totals = df.groupby("Category")["Amount"].sum().to_dict()
        fig, ax = plt.subplots()
        colors = sns.color_palette("pastel")
        wedges, texts, autotexts = ax.pie(
            category_totals.values(), 
            labels=category_totals.keys(), 
            autopct='%1.1f%%', 
            startangle=90, 
            colors=colors
        )
        ax.axis('equal')
        for text in autotexts:
            text.set_color('black')
        st.pyplot(fig)

        # General AI Insight with fun wording
        st.markdown("### 🧠 Cumulative Insight")
        total_spent = df["Amount"].sum()
        avg_daily = total_spent / df["Date"].nunique()
        st.info(f"📅 Your average daily spend is ₹{avg_daily:.2f}. Aim to keep it under ₹{st.session_state.global_daily_limit} for a high score! 🏆")

        # Personalized motivational quote
        st.markdown("### 💬 FinMate's Daily Motivation")
        st.info("“Greatness is not in never falling, but in rising every time you fall. Keep mastering your finances!” — FinMate AI")
        
        # Gamified XP Tracker
        st.markdown("### 🎮 XP Tracker")
        st.progress(st.session_state.xp / 1000)
        st.markdown(f"🌟 **XP:** {st.session_state.xp} / 1000")
        if st.session_state.xp >= 1000:
            st.success("🎉 You've leveled up! Keep unlocking new financial superpowers.")
    else:
        st.info("🌟 Start adding your expenses to unlock insights and level up your financial game!")

import os
from transformers import pipeline
import datetime
import streamlit as st

# Set the GROQ API Key as an environment variable
os.environ["GROQ_API_KEY"] = "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"

# Chatbot
st.sidebar.markdown("### 🎮 Your Progress")
st.sidebar.metric("Current Level", f"{st.session_state.level} 🎮")
st.sidebar.metric("XP Progress", f"{st.session_state.xp}/{st.session_state.level * 100} ⭐")
st.sidebar.metric("Chat Streak", f"{st.session_state.streaks['current']} days 🔥")

# Display badges
st.sidebar.markdown("### 🏆 Your Badges")
if st.session_state.badges:
    for badge in st.session_state.badges:
        st.sidebar.markdown(f"- {badge}")
else:
    st.sidebar.info("Keep using FinMate to earn badges! 🎯")

st.subheader("🤖 FinMate Bot")
st.info("Ask anything about your money!")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "last_chat_date" not in st.session_state:
    st.session_state.last_chat_date = None

# Load model once and reuse
if "chatbot" not in st.session_state:
    try:
        st.session_state.chatbot = pipeline("text-generation", model="gpt2")
    except Exception as e:
        st.error("❌ Failed to load model. Make sure 'transformers' and 'torch' are installed.")
        st.stop()

user_query = st.text_input("💬 You:", key="chat_input")

if st.button("📨 Send") and user_query:
    # Check for daily streak
    today = datetime.date.today()
    if st.session_state.last_chat_date != today:
        st.session_state.streaks["current"] += 1
        add_xp(XP_REWARDS["track_streak"])
        st.session_state.last_chat_date = today
        
        # Check for streak badges
        if st.session_state.streaks["current"] in [7, 30, 100]:
            new_badge = f"{st.session_state.streaks['current']}-Day Streak 🔥"
            if new_badge not in st.session_state.badges:
                st.session_state.badges.append(new_badge)
                st.balloons()
                st.success(f"🎉 New Badge Earned: {new_badge}")

    st.session_state.chat_history.append(("user", user_query))
    
    # Prepend the financial expert prompt to the user query
    expert_prompt = "You are a financial expert and you answer all queries about finances. "
    full_query = expert_prompt + user_query
    
    try:
        response = st.session_state.chatbot(full_query, max_length=100, do_sample=True)[0]['generated_text']
        # Remove the expert prompt from the generated text if present.
        bot_reply = response[len(full_query):].strip()
    except Exception as e:
        bot_reply = "❌ Failed to generate response."

    st.session_state.chat_history.append(("bot", bot_reply))

for sender, msg in st.session_state.chat_history:
    if sender == "user":
        st.markdown(f"**🧑 You:** {msg}")
    else:
        st.markdown(f"**🤖 FinMate Bot:** {msg}")