import streamlit as st
import plotly.express as px
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Income Tax Calculator", page_icon="💰", layout="centered"
)

# Custom CSS for better UI
st.markdown(
    """
    <style>
        body { background-color: #f4f4f4; }
        .stButton > button { background-color: #D7AB6CFF; color: white; font-size: 16px; }
        .stMetric { text-align: center; }
        .dataframe td { text-align: center; }
        .dataframe th { text-align: center; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title with styled header
st.markdown(
    """
    <h1 style='text-align: center; color: #4CAF50;'>Income Tax Calculator (New Regime)</h1>
    """,
    unsafe_allow_html=True,
)

# User Input for Income
st.markdown("### Enter Your Income")
income = st.number_input(
    "Income (₹)", min_value=0, value=2500000, step=100000, format="%d"
)

# Category Selection
st.markdown("### Select Your Category")
category = st.radio("Category", ["Salaried", "Others"], horizontal=True)

# Exemption based on category
exemption = 1275000 if category == "Salaried" else 1200000


# Tax Calculation Function
def calculate_tax(income, exemption):
    if income <= exemption:
        return 0

    diff = income - exemption
    tax = 0

    if income <= 400000:
        return 0
    elif income <= 800000:
        tax = (income - 400000) * 5 / 100
    elif income <= 1200000:
        tax = (income - 800000) * 10 / 100 + 20000
    elif income <= 1600000:
        tax = (income - 1200000) * 15 / 100 + 60000
    elif income <= 2000000:
        tax = (income - 1600000) * 20 / 100 + 100000
    elif income <= 2400000:
        tax = (income - 2000000) * 25 / 100 + 140000
    else:
        tax = (income - 2400000) * 30 / 100 + 180000

    return min(tax, diff)


# Compute tax and results
tax = calculate_tax(income, exemption)
disposable_income = income - tax
effective_tax_rate = (tax / income) * 100 if income > 0 else 0

# Display Results
st.markdown("### Tax Summary")
col1, col2, col3 = st.columns(3)
col1.metric("💵 Total Tax", f"₹{tax:,.0f}")
col2.metric("🏦 Disposable Income", f"₹{disposable_income:,.0f}")
col3.metric("📊 Effective Rate", f"{effective_tax_rate:.2f}%")

# Tax Breakdown Pie Chart
tax_data = {
    "Category": ["Tax Paid", "Remaining Income"],
    "Amount": [tax, disposable_income],
}
fig = px.pie(
    tax_data,
    names="Category",
    values="Amount",
    title="Tax Distribution",
    color_discrete_sequence=["#FF5733", "#4CAF50"],
    hole=0.4,
)
st.plotly_chart(fig)

# Additional Insights
st.markdown("### Additional Insights")
st.markdown(
    f"- 💡 Your effective tax rate is **{effective_tax_rate:.2f}%** of your total income.\n"
    "- 📈 Higher income results in higher tax slabs; consider tax planning strategies.\n"
    "- 🏠 Investing in tax-saving options like NPS, PPF, and ELSS can help reduce taxable income.\n"
)

# Tax Saving Insight
max_tax_saving = min(150000, income * 0.3)  # Maximum tax saving considering 30% bracket
st.markdown(
    f"- 🎯 If you invest **₹1,50,000** in NPS/ELSS, you can save up to **₹{max_tax_saving:,.0f}** in taxes!"
)

# Tax Slabs Table at the Bottom
st.markdown("### Applicable Tax Slabs")
    
    # Define slab ranges and rates
slab_ranges = [
        (0, 400000),
        (400001, 800000),
        (800001, 1200000),
        (1200001, 1600000),
        (1600001, 2000000),
        (2000001, 2400000),
        (2400001, float('inf'))
    ]

    # Determine applicable slabs
applicable_indices = []
for i, (lower, upper) in enumerate(slab_ranges):
        if lower <= income <= upper:
            applicable_indices = list(range(i + 1))
            break

    # Create dataframe
slab_df = pd.DataFrame({
        "Income Slab (₹)": [
            "0 - 4,00,000",
            "4L - 8L",
            "8L - 12L",
            "12L - 16L",
            "16L - 20L",
            "20L - 24L",
            "24L+"
        ],
        "Tax Rate (%)": [0, 5, 10, 15, 20, 25, 30],
        "Taxable Amount (₹)": [0, "20,000", "40,000", "60,000", "80,000", "1,00,000", "-"],
        "Cumulative Tax (₹)": [0, "20,000", "60,000", "1,00,000", "1,40,000", "1,80,000", "-"]
    })

    # Apply highlighting
def highlight_slabs(row):
        if row.name in applicable_indices:
            return ['background-color: #EC1313FF' for _ in row]
        return [''] * len(row)

styled_df = slab_df.style.apply(highlight_slabs, axis=1)
st.dataframe(styled_df, use_container_width=True, hide_index=True)