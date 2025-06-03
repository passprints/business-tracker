import streamlit as st
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

# Load cleaned data
@st.cache_data
def load_data():
    income = pd.read_excel("SUMMARY REPORT.xlsx", sheet_name="RECEIVE", skiprows=3)
    income = income[['DATE', 'CUSTOMER', 'QTY', 'AMOUNT', 'TOTAL', 'STATUS']]
    income = income.dropna(subset=['DATE'])
    income['DATE'] = pd.to_datetime(income['DATE'])

    expense = pd.read_excel("SUMMARY REPORT.xlsx", sheet_name="EXPENSES", skiprows=2)
    expense = expense[['DATE', 'SUPPLIER NAME', 'ITEM', 'TOTAL AMOUNT']]
    expense = expense.dropna(subset=['DATE'])
    expense['DATE'] = pd.to_datetime(expense['DATE'])
    return income, expense

income_df, expense_df = load_data()

st.set_page_config(page_title="Business Tracker", layout="centered")
st.title("📊 Business Income & Expense Tracker")

menu = st.sidebar.radio("Menu", ["Dashboard", "Add Entry", "View Data"])

if menu == "Dashboard":
    st.subheader("📈 Monthly Overview")
    col1, col2 = st.columns(2)

    col1.metric("Total Income", f"₱{income_df['TOTAL'].sum():,.2f}")
    col2.metric("Total Expenses", f"₱{expense_df['TOTAL AMOUNT'].sum():,.2f}")

    # Monthly summary chart
    income_monthly = income_df.groupby(income_df['DATE'].dt.to_period("M")).sum(numeric_only=True)
    expense_monthly = expense_df.groupby(expense_df['DATE'].dt.to_period("M")).sum(numeric_only=True)
    summary = pd.DataFrame({
        'Income': income_monthly['TOTAL'],
        'Expenses': expense_monthly['TOTAL AMOUNT']
    }).fillna(0)

    st.bar_chart(summary)

elif menu == "Add Entry":
    st.subheader("➕ Add New Entry")
    entry_type = st.selectbox("Entry Type", ["Income", "Expense"])

    if entry_type == "Income":
        with st.form("income_form"):
            date = st.date_input("Date", value=dt.date.today())
            customer = st.text_input("Customer")
            qty = st.number_input("Quantity", min_value=0.0)
            amount = st.number_input("Amount per Unit", min_value=0.0)
            total = qty * amount
            st.write(f"Total: ₱{total:,.2f}")
            status = st.selectbox("Status", ["pd", "unpaid"])
            submitted = st.form_submit_button("Save Income")
            if submitted:
                st.success("Income entry saved (in this demo, not persisted)")

    else:
        with st.form("expense_form"):
            date = st.date_input("Date", value=dt.date.today())
            supplier = st.text_input("Supplier Name")
            item = st.text_input("Item Description")
            amount = st.number_input("Total Amount", min_value=0.0)
            submitted = st.form_submit_button("Save Expense")
            if submitted:
                st.success("Expense entry saved (in this demo, not persisted)")

elif menu == "View Data":
    st.subheader("📄 Income Records")
    st.dataframe(income_df)

    st.subheader("📄 Expense Records")
    st.dataframe(expense_df)

    st.download_button("Download Income CSV", income_df.to_csv(index=False), file_name="income.csv")
    st.download_button("Download Expense CSV", expense_df.to_csv(index=False), file_name="expenses.csv")
