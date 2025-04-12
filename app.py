import os
import sys
from datetime import datetime, date
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.categorize import categorize_expense
from llama_index.llms.groq import Groq
from datetime import datetime, timedelta
import random



from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file
groq_api_key = os.getenv('GROQ_API_KEY')
# Set page configuration
st.set_page_config(page_title="FinMate — SpendWise with AI", layout="wide")

# Function to apply custom CSS
def apply_custom_css():
    with open('style.css', 'r') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Apply custom CSS
apply_custom_css()

# Initialize session state variables if not present
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
if "global_daily_limit" not in st.session_state:
    st.session_state.global_daily_limit = 100
if "expenses" not in st.session_state:
    st.session_state.expenses = []
if "goals" not in st.session_state:
    st.session_state.goals = []
if "daily_expenses" not in st.session_state:
    st.session_state.daily_expenses = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_chat_date" not in st.session_state:
    st.session_state.last_chat_date = None

# XP rewards configuration
XP_REWARDS = {
    "add_expense": 10,
    "set_goal": 25,
    "complete_goal": 100,
    "track_streak": 15,
    "under_budget": 20,
    "complete_challenge": 50,
    "first_chat": 20,
    "daily_login": 10,
    "budget_setup": 30,
    "streak_milestone": 50
}

# Function to add XP and check for level up
def add_xp(amount):
    st.session_state.xp += amount
    if st.session_state.xp >= st.session_state.level * 100:
        level_up()

def level_up():
    st.session_state.level += 1
    st.balloons()
    st.success(f"🎉 Level Up! You're now level {st.session_state.level}!")
    if st.session_state.level == 5:
        st.session_state.badges.append("Financial Novice 🌟")
    elif st.session_state.level == 10:
        st.session_state.badges.append("Money Master 💰")
    elif st.session_state.level == 20:
        st.session_state.badges.append("Budget Guru 🏆")

# Tab Mapping and Title
tab_mapping = {"Dashboard": 0, "Track Expenses": 1, "Set Goals": 2, "Insights": 3}
st.title("FinMate — SpendWise with AI 💼✨")
st.markdown("#### Smart budgeting. Real savings. Built with AI.")

# Top Navigation Tabs
tabs = st.tabs(["Dashboard", "Track Expenses", "Set Goals", "Insights"])
active_tab_index = tab_mapping.get(st.session_state.active_tab, 0)



# Initialize chat state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# DASHBOARD TAB
with tabs[0]:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🎮 Level", f"{st.session_state.level}")
    with col2:
        next_level_xp = st.session_state.level * 100
        st.metric("⭐ XP", f"{st.session_state.xp}/{next_level_xp}")
    with col3:
        st.metric("🔥 Streak", f"{st.session_state.streaks['current']} days")
    
    xp_progress = st.session_state.xp / next_level_xp
    st.progress(xp_progress)
    st.caption(f"XP needed for Level {st.session_state.level + 1}: {next_level_xp - st.session_state.xp}")
    st.subheader("📊 Dashboard Overview")
    
    st.markdown("### 💼 Monthly Income & Plans")
    salary = st.number_input("Enter your total monthly salary (₹):", min_value=0, value=30000, step=500)
    planned_savings = st.number_input("Enter your planned savings (₹):", min_value=0, value=10000, step=500)
    total_expenses = st.number_input("Enter your expected monthly expenses (₹):", min_value=0, value=15000, step=500)
    
    unspent = salary - (planned_savings + total_expenses)
    if unspent < 0:
        st.error("⚠️ Your planned savings and expenses exceed your salary!")
        unspent = 0
    
    st.metric("Planned Savings", f"₹{planned_savings}")
    st.metric("Expected Expenses", f"₹{total_expenses}")
    st.metric("Unallocated Amount", f"₹{unspent}")
    
    st.markdown("### 🏦 Savings Progress")
    current_savings = 0  # Placeholder for dynamic update
    progress_val = min(current_savings / planned_savings, 1.0) if planned_savings > 0 else 0
    st.progress(progress_val)
    st.caption(f"₹{current_savings} / ₹{planned_savings} saved")
    
    st.markdown("### 📉 Salary Distribution Breakdown")
    labels = ['Expenses', 'Planned Savings', 'Unspent']
    sizes = [total_expenses, planned_savings, unspent]
    colors = ['#FF6F61', '#6EC1E4', '#9CCC65']
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    ax1.axis('equal')
    st.pyplot(fig1)
    
   
    recent_transactions = {
        'Date': ['2025-04-10', '2025-04-09', '2025-04-08'],
        'Category': ['Groceries', 'Shopping', 'Bills'],
        'Amount (₹)': [1200, 2000, 1500]
    }
    df_recent = pd.DataFrame(recent_transactions)
    st.markdown("### 📝 Recent Transactions")
    st.dataframe(df_recent)
    
    st.markdown("### 💡 Financial Tips")
    st.info("Consider reducing your 'Dining Out' expenses to save ₹2000 this month!")
    # Add this after the Monthly Income & Plans section
st.markdown("### 🏦 Bank Accounts")

# Initialize bank accounts in session state if not present
if "bank_accounts" not in st.session_state:
    st.session_state.bank_accounts = [
        {
            "name": "Primary Savings",
            "account_number": "**** **** 1234",
            "balance": 45000,
            "type": "Savings",
            "bank": "State Bank of India"
        },
        {
            "name": "Salary Account",
            "account_number": "**** **** 5678",
            "balance": 28500,
            "type": "Current",
            "bank": "HDFC Bank"
        }
    ]

# Display bank accounts
for account in st.session_state.bank_accounts:
    with st.expander(f"💳 {account['name']} - {account['bank']}", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Account Type:** {account['type']}")
            st.markdown(f"**Account Number:** {account['account_number']}")
        with col2:
            st.metric(
                "Current Balance",
                f"₹{account['balance']:,.2f}",
                delta="↑ ₹1,200 this month"
            )

# TRACK EXPENSES TAB
with tabs[1]:
    st.subheader("💸 Track Your Expenses")
    with st.form("expense_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            expense_date = st.date_input("Date")
        with col2:
            amount = st.number_input("Amount (₹)", min_value=0.0, step=10.0)
        notes = st.text_input("Notes (optional)")
        form_submitted = st.form_submit_button("➕ Add Expense")
        if form_submitted:
            category_result = categorize_expense(amount)
            st.session_state.expenses.append({
                "Date": expense_date.strftime("%Y-%m-%d"),
                "Category": category_result,
                "Amount (₹)": amount,
                "Notes": notes
            })
            st.success(f"Expense for ₹{amount} categorized as: {category_result} added successfully!")
            add_xp(XP_REWARDS["add_expense"])
            # Bonus XP if under the global daily limit (if applicable)
            if amount <= st.session_state.global_daily_limit:
                add_xp(XP_REWARDS["under_budget"])
                st.success(f"🎯 Bonus XP earned for staying under budget! (+{XP_REWARDS['under_budget']} XP)")
    
    if st.session_state.expenses:
        st.markdown("### 📋 Expense History")
        df_exp = pd.DataFrame(st.session_state.expenses)
        st.dataframe(df_exp)
        
        st.markdown("### 📊 Category-wise Spending")
        category_totals = df_exp.groupby("Category")["Amount (₹)"].sum().reset_index()
        fig_exp, ax_exp = plt.subplots()
        ax_exp.bar(category_totals["Category"], category_totals["Amount (₹)"], color="#4CAF50")
        ax_exp.set_xlabel("Category")
        ax_exp.set_ylabel("Total Spent (₹)")
        ax_exp.set_title("Spending by Category")
        st.pyplot(fig_exp)
    else:
        st.info("No expenses added yet. Start tracking now!")

# SET GOALS TAB
with tabs[2]:
    st.subheader("🎯 Set Your Savings Goals")
    if len(st.session_state.goals) < 10:
        with st.form("add_goal_form", clear_on_submit=True):
            goal_name = st.text_input("Goal Name", value="My Goal")
            target_amount = st.number_input("Target Amount (₹)", min_value=100.0, step=100.0)
            deadline = st.date_input("Deadline")
            goal_submitted = st.form_submit_button("➕ Add Goal")
            if goal_submitted:
                st.session_state.goals.append({
                    "name": goal_name,
                    "target": target_amount,
                    "deadline": deadline,
                    "current": 0
                })
                st.success(f"Goal '{goal_name}' added!")
                add_xp(XP_REWARDS["set_goal"])
                st.session_state.challenges.append({
                    "type": "goal",
                    "name": f"Complete {goal_name}",
                    "target": target_amount,
                    "deadline": deadline,
                    "completed": False
                })
    if st.session_state.goals:
        st.markdown("### 📋 Your Goals")
        for goal in st.session_state.goals:
            with st.expander(f"🎯 {goal['name']} (Deadline: {goal['deadline']})"):
                st.markdown(f"**Target:** ₹{goal['target']}")
                current = goal.get("current", 0)
                progress = min(current / goal['target'], 1.0) if goal['target'] > 0 else 0
                st.progress(progress)
                st.caption(f"₹{current} / ₹{goal['target']} saved")
    else:
        st.info("No goals set yet. Add a goal to start tracking!")

# INSIGHTS TAB
with tabs[3]:
    st.subheader("💡 Smart Financial Insights")
    for challenge in st.session_state.challenges:
        if not challenge["completed"]:
            st.markdown(f"- **{challenge['name']}**")
            st.progress(challenge.get("progress", 0) / 100)
            if st.button(f"✅ Complete: {challenge['name']}", key=challenge['name']):
                challenge["completed"] = True
                add_xp(XP_REWARDS["complete_challenge"])
                st.balloons()
                st.success(f"🎉 Challenge completed! (+{XP_REWARDS['complete_challenge']} XP)")
        else:
            st.markdown(f"✔️ ~~{challenge['name']}~~")
    
    st.markdown("### 🛡 Set Your Daily Spending Shield")
    st.session_state.global_daily_limit = st.number_input(
        "Enter your Global Daily Spending Limit (₹)",
        value=st.session_state.global_daily_limit,
        min_value=100,
        step=50
    )
    st.info(f"💡 Your current daily limit is ₹{st.session_state.global_daily_limit}. Adjust it as needed!")
    
    st.markdown("### ➕ Add Your Daily Expense")
    insight_date = st.date_input("📅 Date", key="insight_date")
    category = st.selectbox(
        "📂 Category", 
        ["🛒 Groceries", "🍽 Dining Out", "🎮 Entertainment", "💡 Utilities", "🚗 Transport", "🛍 Shopping", "🌈 Others"], 
        key="insight_category"
    )
    insight_amount = st.number_input("💲 Amount (₹)", min_value=0, step=50, key="insight_amount")
    if st.button("➕ Add Expense", key="daily_expense"):
        st.session_state.daily_expenses.append({
            "Date": insight_date.strftime("%Y-%m-%d"),
            "Category": category,
            "Amount": insight_amount
        })
        st.success(f"🎉 Expense for {category} of ₹{insight_amount} added successfully!")
        
        today_expenses = [
            exp for exp in st.session_state.daily_expenses
            if exp["Date"] == insight_date.strftime("%Y-%m-%d")
        ]
        total_today = sum(exp["Amount"] for exp in today_expenses)
        if total_today <= st.session_state.global_daily_limit:
            st.success(f"✅ You're within your daily budget of ₹{st.session_state.global_daily_limit}. 🌟 Keep it up! 🎯")
        else:
            overspent = total_today - st.session_state.global_daily_limit
            st.warning(f"⚠️ You've spent ₹{total_today}, which is ₹{overspent} over your daily limit!")
    
    if st.session_state.daily_expenses:
        df_daily = pd.DataFrame(st.session_state.daily_expenses)
        st.markdown("### 📝 Tracked Expenses")
        st.dataframe(df_daily)
        
        st.markdown("### 📊 Spending Breakdown by Category")
        category_totals = df_daily.groupby("Category")["Amount"].sum().to_dict()
        fig_breakdown, ax_breakdown = plt.subplots()
        colors = sns.color_palette("pastel")
        wedges, texts, autotexts = ax_breakdown.pie(
            list(category_totals.values()),
            labels=list(category_totals.keys()),
            autopct='%1.1f%%',
            startangle=90,
            colors=colors
        )
        ax_breakdown.axis('equal')
        for text in autotexts:
            text.set_color('black')
        st.pyplot(fig_breakdown)
        
        st.markdown("### 🧠 Cumulative Insight")
        total_spent = df_daily["Amount"].sum()
        avg_daily = total_spent / df_daily["Date"].nunique()
        st.info(f"📅 Your average daily spend is ₹{avg_daily:.2f}. Aim to keep it under ₹{st.session_state.global_daily_limit} for a high score!")
        
        st.markdown("### 💬 FinMate's Daily Motivation")
        st.info("“Greatness is not in never falling, but in rising every time you fall. Keep mastering your finances!” — FinMate AI")
        
        st.markdown("### 🎮 XP Tracker")
        st.progress(st.session_state.xp / 1000)
        st.markdown(f"🌟 **XP:** {st.session_state.xp} / 1000")
        if st.session_state.xp >= 1000:
            st.success("🎉 You've leveled up! Keep unlocking new financial superpowers.")
    else:
        st.info("🌟 Start adding your expenses to unlock insights and level up your financial game!")

# XP reward constants
XP_REWARDS = {
    "track_streak": 10,
    "chat_interaction": 5,
    "complete_quiz": 20
}

def add_xp(amount):
    """Add XP and level up if threshold reached"""
    st.session_state.xp += amount
    level_threshold = st.session_state.level * 100
    
    if st.session_state.xp >= level_threshold:
        st.session_state.level += 1
        st.session_state.xp = st.session_state.xp - level_threshold
        st.balloons()
        st.success(f"🎉 Level Up! You're now level {st.session_state.level}!")

# Initialize OpenAI or similar fallback client
def get_fallback_response(query):
    """Enhanced rule-based fallback with detailed financial advice when API is unavailable"""
    query = query.lower()
    
    if "budget" in query:
        return """Creating a budget is the foundation of financial wellness. Here's a comprehensive approach:

1. **Track Your Income**: Document all sources of income, including salary, freelance work, investments, etc.

2. **List Fixed Expenses**: Identify recurring monthly costs like rent/mortgage, utilities, loan payments, and subscriptions.

3. **Record Variable Expenses**: Track costs that fluctuate monthly like groceries, entertainment, and dining out.

4. **Follow the 50/30/20 Rule**: Allocate 50% of income to needs, 30% to wants, and 20% to savings and debt repayment.

5. **Use Budgeting Tools**: Consider apps like Mint, YNAB, or spreadsheets to maintain your budget.

6. **Review Regularly**: Reassess your budget monthly and adjust as necessary.

7. **Set Specific Goals**: Define short-term and long-term financial objectives to stay motivated.

Remember, a budget isn't about restriction—it's about intentional spending that aligns with your priorities and goals."""

    elif "invest" in query or "investing" in query:
        return """Investing is crucial for building wealth and achieving financial independence. Here's a comprehensive guide:

1. **Define Your Goals**: Determine what you're investing for—retirement, home purchase, education, etc.—and your time horizon.

2. **Emergency Fund First**: Before investing, establish an emergency fund covering 3-6 months of expenses.

3. **Understand Risk Tolerance**: Assess how much volatility you can handle emotionally and financially.

4. **Diversification**: Spread investments across various asset classes to manage risk:
   - Stocks: Higher risk, potentially higher returns
   - Bonds: Lower risk, generally lower returns
   - Real Estate: Tangible assets with potential income
   - Cash/Equivalents: Safety and liquidity

5. **Low-Cost Index Funds**: For most beginners, index funds like S&P 500 ETFs offer diversification with lower fees than actively managed funds.

6. **Retirement Accounts**: Maximize tax-advantaged accounts like 401(k)s (especially if employer matching is available) and IRAs.

7. **Dollar-Cost Averaging**: Invest regularly regardless of market conditions to reduce timing risk.

8. **Rebalance Periodically**: Review your portfolio annually and realign with your target asset allocation.

9. **Long-Term Perspective**: Focus on long-term growth and ignore short-term market fluctuations.

The most important investment principles are starting early, staying consistent, keeping costs low, and maintaining a long-term perspective."""

    elif "debt" in query:
        return """Managing debt effectively is critical to financial health. Here's a comprehensive approach:

1. **Know What You Owe**: List all debts with their interest rates, minimum payments, and balances.

2. **Prioritization Methods**:
   - **Avalanche Method**: Pay minimum on all debts and put extra money toward highest-interest debt first (mathematically optimal)
   - **Snowball Method**: Pay off smallest balances first for psychological wins and momentum
   
3. **Consolidation Options**: Consider consolidating high-interest debts through personal loans or balance transfer cards if you qualify for lower rates.

4. **Student Loan Strategies**: 
   - Explore income-driven repayment plans
   - Check forgiveness program eligibility (PSLF, etc.)
   - Consider refinancing if you have good credit and stable income

5. **Mortgage Management**: 
   - Extra payments toward principal can save thousands in interest
   - Refinancing when rates drop significantly can be beneficial

6. **Avoid Taking On New Debt**: While paying off existing obligations, minimize new debt acquisition.

7. **Emergency Fund**: Maintain 3-6 months of expenses to avoid debt reliance during unexpected situations.

8. **Seek Professional Help**: Credit counseling services can provide structured plans for severe debt situations.

Remember that not all debt is bad—low-interest debt for appreciating assets (like education or housing) can be strategic. Focus on eliminating high-interest consumer debt first."""

    elif "save" in query or "saving" in query:
        return """Building a strong savings foundation is essential for financial security. Here's a comprehensive savings strategy:

1. **Emergency Fund**: Your first priority should be establishing a fund covering 3-6 months of essential expenses. Keep this in a high-yield savings account for easy access.

2. **Savings Hierarchy**:
   - First: Emergency fund
   - Second: Employer retirement match (free money)
   - Third: High-interest debt repayment
   - Fourth: Additional retirement savings
   - Fifth: Other financial goals (home, education, etc.)

3. **Automate Savings**: Set up automatic transfers on payday so money is saved before you can spend it.

4. **Savings Rates**: 
   - Beginners: Save at least 10% of gross income
   - Intermediate: Aim for 15-20%
   - Advanced: Try to reach 20-30% or more for early financial independence

5. **Separate Accounts for Different Goals**: Create dedicated accounts for specific purposes (vacation, home down payment, etc.) to prevent "borrowing" from yourself.

6. **Use Tax-Advantaged Accounts**:
   - 401(k)/403(b) for retirement
   - HSA for healthcare (triple tax advantage)
   - 529 plans for education

7. **Optimize Interest Rates**: Shop around for high-yield savings accounts, certificates of deposit (CDs), and money market accounts for better returns on cash reserves.

8. **Review and Adjust**: Reassess your savings strategy quarterly and after major life events.

Remember that consistency is more important than amount when starting—even small regular contributions compound significantly over time."""

    elif "credit score" in query or "credit report" in query:
        return """Your credit score significantly impacts your financial options. Here's a comprehensive guide to understanding and improving it:

1. **Credit Score Components**:
   - Payment History (35%): Make on-time payments consistently
   - Credit Utilization (30%): Keep balances below 30% of available credit
   - Length of Credit History (15%): Older accounts improve your score
   - Credit Mix (10%): Having various types of credit (revolving, installment)
   - New Credit (10%): Minimize hard inquiries

2. **Monitoring Your Credit**:
   - Get free annual reports from all three bureaus at annualcreditreport.com
   - Consider credit monitoring services or use free options from credit card issuers
   - Dispute inaccuracies promptly

3. **Improvement Strategies**:
   - Set up automatic payments to avoid missed due dates
   - Pay down revolving debt (especially credit cards)
   - Ask for credit limit increases (but don't use the additional credit)
   - Become an authorized user on a responsible person's credit card
   - Use secured credit cards if you're building credit from scratch

4. **Credit Utilization Tricks**:
   - Pay credit card balances before statement close date
   - Make multiple payments throughout the month
   - Keep older accounts open even if unused

5. **Protection Measures**:
   - Consider credit freezes to prevent unauthorized accounts
   - Use fraud alerts if you suspect identity theft
   - Review statements monthly for unauthorized charges

Most improvements take 3-6 months to reflect in your score, so be patient and consistent with good habits."""

    elif "retirement" in query or "retire" in query:
        return """Planning for retirement requires long-term strategy and consistent action. Here's a comprehensive approach:

1. **Determine Your Needs**:
   - Estimate expenses in retirement (typically 70-80% of pre-retirement income)
   - Consider healthcare costs, which increase with age
   - Factor in inflation (historically around 3% annually)

2. **Tax-Advantaged Accounts**:
   - **401(k)/403(b)**: Prioritize employer matching contributions
   - **Traditional IRA**: Tax-deductible contributions, taxed withdrawals
   - **Roth IRA**: After-tax contributions, tax-free withdrawals
   - **HSA**: Triple tax advantage for healthcare expenses

3. **Asset Allocation Strategy**:
   - More aggressive (stock-heavy) when young
   - Gradually increase bond/fixed income allocations as retirement approaches
   - Consider target-date funds for automatic rebalancing

4. **Contribution Guidelines**:
   - Minimum: Save 15% of gross income for retirement
   - Ideal: Maximize annual contributions to tax-advantaged accounts
   - Late start: Catch-up contributions after age 50

5. **Social Security Optimization**:
   - Check your estimated benefits at ssa.gov
   - Consider delaying benefits until age 70 for maximum monthly amount
   - Coordinate claiming strategies with spouse for household optimization

6. **Withdrawal Strategies**:
   - The 4% rule: Withdraw 4% of portfolio in first year, adjust for inflation after
   - Consider tax implications when withdrawing from different account types
   - Required Minimum Distributions (RMDs) begin at age 73

7. **Estate Planning**:
   - Create/update will and beneficiary designations
   - Consider trusts for complex situations
   - Prepare healthcare directives

The earlier you start, the more time compound growth can work in your favor. Even small increases in savings rate can significantly impact your retirement security."""

    else:
        return """Thank you for your financial question. While I don't have a specific detailed answer for this particular query, here are some fundamental financial principles that apply broadly:

1. **Build an Emergency Fund**: Save 3-6 months of expenses in a liquid account before focusing on other financial goals.

2. **Follow the 50/30/20 Budget Rule**: Allocate 50% of income to needs, 30% to wants, and 20% to savings and debt repayment.

3. **Eliminate High-Interest Debt**: Prioritize paying off credit cards and personal loans with double-digit interest rates.

4. **Invest Early and Regularly**: Take advantage of compound interest by investing consistently over time, regardless of market conditions.

5. **Maximize Tax-Advantaged Accounts**: Contribute to 401(k)s, IRAs, and HSAs to reduce tax burden and build wealth more efficiently.

6. **Ensure Proper Insurance Coverage**: Protect yourself with appropriate health, life, disability, auto, home/renters, and liability insurance.

7. **Focus on Increasing Income**: Develop skills and pursue opportunities that increase your earning potential over time.

8. **Estate Planning**: Create a will, designate beneficiaries, and prepare healthcare directives regardless of your age or wealth.

For more specific guidance on your question, consider consulting with a financial professional who can provide personalized advice based on your complete financial situation."""

# Now implement this improved fallback function in your chatbot code
# CHATBOT TAB
st.subheader("🤖 FinMate Bot")
st.info("Ask anything about your money!")

# Sidebar content
st.sidebar.markdown("### 🎮 Your Progress")
st.sidebar.metric("Current Level", f"{st.session_state.level} 🎮")
st.sidebar.metric("XP Progress", f"{st.session_state.xp}/{st.session_state.level * 100} ⭐")
st.sidebar.metric("Chat Streak", f"{st.session_state.streaks['current']} days 🔥")
st.sidebar.markdown("### 🏆 Your Badges")
if st.session_state.badges:
    for badge in st.session_state.badges:
        st.sidebar.markdown(f"- {badge}")
else:
    st.sidebar.info("Keep using FinMate to earn badges! 🎯")

# Initialize the chatbot with error handling
if "chatbot" not in st.session_state:
    try:
        # First try to use Groq if API key is available
        if "GROQ_API_KEY" in os.environ and os.environ["GROQ_API_KEY"].strip():
            st.session_state.chatbot = Groq(model="llama3-70b-8192", api_key=os.environ["GROQ_API_KEY"])
            st.session_state.using_fallback = False
        else:
            st.warning("⚠️ GROQ_API_KEY not found in environment variables. Using fallback responses.")
            st.session_state.using_fallback = True
    except Exception as e:
        st.warning(f"⚠️ Failed to initialize Groq model: {str(e)}. Using fallback responses.")
        st.session_state.using_fallback = True

# Chat interface
user_query = st.text_input("💬 You:", key="chat_input")

if st.button("📨 Send", key="send_chat") and user_query:
    # Track streak and add XP
    today = date.today()
    if st.session_state.last_chat_date != today:
        st.session_state.streaks["current"] += 1
        add_xp(XP_REWARDS["track_streak"])
        st.session_state.last_chat_date = today
        
        # Update longest streak if current exceeds it
        if st.session_state.streaks["current"] > st.session_state.streaks.get("longest", 0):
            st.session_state.streaks["longest"] = st.session_state.streaks["current"]
        
        # Award streak badges
        if st.session_state.streaks["current"] in [7, 30, 100]:
            new_badge = f"{st.session_state.streaks['current']}-Day Streak 🔥"
            if new_badge not in st.session_state.badges:
                st.session_state.badges.append(new_badge)
                st.balloons()
                st.success(f"🎉 New Badge Earned: {new_badge}")
    
    # Add XP for chatting
    add_xp(XP_REWARDS["chat_interaction"])
    
    # Add user message to chat history
    st.session_state.chat_history.append(("user", user_query))
    
    # Generate bot response
    expert_prompt = "You are a financial expert and you answer all queries about finances in atleast 500 words. "
    full_query = expert_prompt + user_query
    
    try:
        if st.session_state.get("using_fallback", False):
            bot_reply = get_fallback_response(user_query)
        else:
            # Simple direct approach using the Groq API
            try:
                response = st.session_state.chatbot.completion(
                    prompt=f"You are a financial expert. {user_query}",
                    model="llama3-70b-8192",
                    max_tokens=500
                )
                bot_reply = response.text.strip()
            except Exception as internal_e:
                
                bot_reply = get_fallback_response(user_query)
    except Exception as e:
        st.error(f"❌ Failed to generate response: {str(e)}")
        bot_reply = get_fallback_response(user_query)
    # Add bot response to chat history
    st.session_state.chat_history.append(("bot", bot_reply))

# Display chat history
for sender, msg in st.session_state.chat_history:
    if sender == "user":
        st.markdown(f"**🧑 You:** {msg}")
    else:
        st.markdown(f"**🤖 FinMate Bot:** {msg}")

# Add a clear chat button
if st.session_state.chat_history and st.button("🧹 Clear Chat"):
    st.session_state.chat_history = []
    st.experimental_rerun()

import datetime
import pandas as pd

def get_recent_transactions():
    """Generate sample recent transactions for demonstration"""
    return {
        'Date': [
            (datetime.datetime.now() - datetime.timedelta(days=i)).strftime('%Y-%m-%d') 
            for i in range(10)
        ],
        'Description': [
            'Grocery Store', 'Online Shopping', 'Restaurant', 
            'Gas Station', 'Utility Bill', 'Streaming Service',
            'Coffee Shop', 'Pharmacy', 'Bookstore', 'Electronics'
        ],
        'Amount': [
            -45.67, -89.32, -32.45, -38.20, -120.00, 
            -14.99, -5.75, -27.80, -19.95, -149.99
        ],
        'Category': [
            'Food', 'Shopping', 'Dining', 'Transport', 'Utilities',
            'Entertainment', 'Food', 'Health', 'Education', 'Shopping'
        ]
    }

# When calling the function
df_recent = pd.DataFrame(get_recent_transactions())
st.dataframe(
    df_recent.style.format({'Amount (₹)': '₹{:,.2f}'}),
    use_container_width=True
)

def generate_financial_tips():
    tips = [
        {
            "category": "Savings",
            "tip": "Try the 50/30/20 rule: 50% for needs, 30% for wants, and 20% for savings.",
            "impact": "Could save ₹5,000+ monthly"
        },
        {
            "category": "Investment",
            "tip": "Consider starting a SIP (Systematic Investment Plan) in mutual funds.",
            "impact": "Potential long-term growth"
        },
        {
            "category": "Spending",
            "tip": "Your dining out expenses are 25% higher than last month. Consider cooking more meals at home.",
            "impact": "Could save ₹2,000 monthly"
        },
        {
            "category": "Budget",
            "tip": "Create an emergency fund with 3-6 months of expenses.",
            "impact": "Financial security"
        }
    ]
    return random.sample(tips, 3)  # Return 3 random tips

# Replace the Financial Tips section with this code
st.markdown("### 💡 Financial Tips")
col1, col2, col3 = st.columns(3)
columns = [col1, col2, col3]

for tip, col in zip(generate_financial_tips(), columns):
    with col:
        st.info(
            f"**{tip['category']}**\n\n"
            f"{tip['tip']}\n\n"
            f"💫 *Impact: {tip['impact']}*"
        )
