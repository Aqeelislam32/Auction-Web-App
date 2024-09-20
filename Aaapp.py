 import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
from datetime import datetime
import os
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import io
import random 
import string
 
# Define file paths for storing user data
USER_DATA_FILE = "user_data.pkl"
USER_DATA_FILE = 'user_data.csv'
PRODUCT_DATA_FILE = "product_data.csv"
EXPENSE_DATA_FILE = "expense_data.csv"
INVENTORY_DATA_FILE = "inventory_data.csv"
CUSTOMER_DATA_FILE = "customer_data.csv"

# Function to load data from a file
def load_data(file_path, default_data):
    if os.path.exists(file_path):
       with open(file_path, "rb") as file:
            return pickle.load(file)
    else:
        return default_data

# Function to save data to a file
def save_data(file_path, data):
    with open(file_path, "wb") as file:
        pickle.dump(data, file) 
# User Database
if 'user_data' not in st.session_state:
    st.session_state.user_data = pd.DataFrame(columns=['First Name', 'Last Name', 'Email', 'Phone Number', 'Password'])



 


# Initialize or load sample data
if 'product_data' not in st.session_state:
    st.session_state.product_data = pd.DataFrame({
        'Auction Branch': np.random.choice(['Branch A', 'Branch B', 'Branch C'], 100),
        'Product': np.random.choice(['Product A', 'Product B', 'Product C'], 100),
        'Quantity': np.random.randint(1, 10, 100),
        'Purchase Date': pd.date_range(start='2024-01-01', periods=100, freq='D'),
        'Price': np.random.uniform(1000, 10000, 100),  # Prices in PKR
        'Payment Method': np.random.choice(['Credit', 'Cash', 'Online'], 100)
    })
    st.session_state.product_data['Total'] = st.session_state.product_data['Quantity'] * st.session_state.product_data['Price']
    st.session_state.product_data = load_data(PRODUCT_DATA_FILE, st.session_state.product_data)

if 'expense_data' not in st.session_state:
    st.session_state.expense_data = pd.DataFrame({
        'Date': pd.date_range(start='2024-01-01', periods=100, freq='D'),
        'Category': np.random.choice(['Rent', 'Electricity Bill', 'Water Bill', 'Gas Bill', 'Inventory', 'Misc'], 100),
        'Amount': np.random.uniform(500, 5000, 100)  # Amounts in PKR
    }) 
    st.session_state.expense_data = load_data(EXPENSE_DATA_FILE,st.session_state.expense_data)
#
if 'inventory_data' not in st.session_state:
    st.session_state.inventory_data = pd.DataFrame({
        'Product': ['Product A', 'Product B', 'Product C'],
        'Stock': [100, 150, 80],
        'Restock Date': pd.to_datetime(['2024-02-01', '2024-02-15', '2024-03-01'])
    })
    st.session_state.inventory_data = load_data(INVENTORY_DATA_FILE,st.session_state.inventory_data)

if 'customer_data' not in st.session_state:
    st.session_state.customer_data = pd.DataFrame({
        'Customer Name': np.random.choice(['Customer A', 'Customer B', 'Customer C'], 100),
        'Contact Number': np.random.choice(['03001234567', '03101234567', '03201234567'], 100),
        'Sale Product Name': np.random.choice(['Product A', 'Product B', 'Product C'], 100),
        'Quantity': np.random.randint(1, 10, 100),
        'Shop Name': np.random.choice(['Shop A', 'Shop B', 'Shop C'], 100),
        'Purchase Date': pd.date_range(start='2024-01-01', periods=100, freq='D'),
        'Payment Method': np.random.choice(['Credit', 'Cash', 'Online'], 100)
    })
    st.session_state.customer_data = load_data(CUSTOMER_DATA_FILE, st.session_state.customer_data)

# Function to save all session data
def save_all_data():
    save_data(PRODUCT_DATA_FILE, st.session_state.product_data)
    save_data(EXPENSE_DATA_FILE, st.session_state.expense_data)
    save_data(INVENTORY_DATA_FILE, st.session_state.inventory_data)
    save_data(CUSTOMER_DATA_FILE, st.session_state.customer_data)

# Sign-up form
def sign_up():
    st.title("Welcome To Auction Web App")
    st.header("Sign Up")
    with st.form("signup_form"):
        email = st.text_input("Email")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        phone = st.text_input("Phone Number")
        password = st.text_input("Password", type="password")
        password_confirm = st.text_input("Confirm Password", type="password")

        col1, col2 = st.columns([1, 1])
        with col1:
            sign_up_button = st.form_submit_button("Sign Up")
        with col2:
            login_button = st.form_submit_button("Login")

        if sign_up_button:
            if not email or not first_name or not last_name or not phone or not password or not password_confirm:
     if st.button("Calculate Budget"):
        # Check if necessary data is available
        if 'customer_data' in st.session_state and 'expense_data' in st.session_state:
            # Calculate total sales and expenses
            total_sales = st.session_state.customer_data['Total'].sum()
            total_expenses = st.session_state.expense_data['Amount'].sum()
            
            # Set budget based on total sales
            yearly_budget = total_sales * 0.2  # Assuming budget is 20% of total sales
            monthly_budget = yearly_budget / 12    # Monthly budget is yearly budget divided by 12
            
            st.session_state.budget = {'Monthly': monthly_budget, 'Yearly': yearly_budget}
            st.success(f"Calculated Monthly Budget: PKR {monthly_budget:,.2f}")
            st.success(f"Calculated Yearly Budget: PKR {yearly_budget:,.2f}")
            
            # Plot Pie Chart
            fig, ax = plt.subplots()
            labels = ['Total Sales', 'Total Expenses', 'Yearly Budget']
            sizes = [total_sales, total_expenses, yearly_budget]
            colors = ['#ff9999','#66b3ff','#99ff99']
            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            
            st.subheader("Pie Chart")
            st.pyplot(fig)

            # Plot Bar Plot
            fig, ax = plt.subplots()
            categories = ['Total Sales', 'Total Expenses', 'Yearly Budget']
            values = [total_sales, total_expenses, yearly_budget]
            sns.barplot(x=categories, y=values, ax=ax, palette='viridis')
            ax.set_ylabel('Amount (PKR)')
            ax.set_title('Budget and Expense Breakdown')
            
            st.subheader("Bar Plot")
            st.pyplot(fig)
            
            # Prepare data for download
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            
            st.subheader("Download Charts")
            st.download_button(
                label="Download Pie and Bar Charts",
                data=buf,
                file_name="charts.png",
                mime="image/png"
            )
        else:
            st.error("Required data is missing.")
    
    # Forecasting Section
     st.subheader("Forecasting")
     if st.button("Generate Forecast"):
        if 'customer_data' in st.session_state:
            total_sales = st.session_state.customer_data['Total'].sum()
            future_sales_prediction = total_sales * 1.1  # Assuming a 10% increase
            
            st.write(f"**Total Sales:** PKR {total_sales:,.2f}")
            st.write(f"**Future Sales Prediction:** PKR {future_sales_prediction:,.2f}")
        
        # Calculate and display budget differences
        if 'budget' in st.session_state:
            monthly_budget = st.session_state.budget.get('Monthly', 0)
            yearly_budget = st.session_state.budget.get('Yearly', 0)
            monthly_expenses = st.session_state.expense_data['Amount'].sum() / 12
            yearly_expenses = st.session_state.expense_data['Amount'].sum()

            budget_difference_monthly = monthly_budget - monthly_expenses
            budget_difference_yearly = yearly_budget - yearly_expenses

            st.write(f"**Monthly Budget Difference:** PKR {budget_difference_monthly:,.2f}")
            st.write(f"**Yearly Budget Difference:** PKR {budget_difference_yearly:,.2f}")a
