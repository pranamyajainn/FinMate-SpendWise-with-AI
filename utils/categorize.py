

def categorize_expense(expense_amount):
    """
    Categorize expense based on predefined thresholds.
    Returns the category as a string.
    """
    if expense_amount < 100:
        return "Low Expense"
    elif 100 <= expense_amount < 500:
        return "Medium Expense"
    elif 500 <= expense_amount < 1000:
        return "High Expense"
    else:
        return "Very High Expense"