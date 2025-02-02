import streamlit as st
import plotly.express as px
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Income Tax Calculator", page_icon="💰", layout="centered"
)

# Custom CSS for better UI
st.markdown(
    """
    <style>
        body { background-color: #f9f9f9; }
        .stButton>button { background-color: #4CAF50; color: white; font-size: 16px; border-radius: 8px; }
        .stMetric { text-align: center; }
        .stRadio label { font-size: 16px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title
st.markdown(
    """<h1 style='text-align: center; color: #4CAF50;'>💰 Income Tax Calculator</h1>""",
    unsafe_allow_html=True,
)

# User Input
st.subheader("Enter Your Income")
income = st.number_input(
    "Income (₹)", min_value=0, value=2500000, step=100000, format="%d"
)

# Category Selection
st.subheader("Select Your Category")
category = st.radio("", ["Salaried", "Others"], horizontal=True)
exemption = 1275000 if category == "Salaried" else 1200000


# Tax Calculation Function
def calculate_tax(income, exemption):
    if income <= exemption:
        return 0

    slabs = [
        (400000, 0.05),
        (800000, 0.10),
        (1200000, 0.15),
        (1600000, 0.20),
        (2000000, 0.25),
        (2400000, 0.30),
    ]
    taxable_income = income - exemption
    tax, prev_limit = 0, exemption

    for limit, rate in slabs:
        if income > limit:
            tax += (min(income, limit) - prev_limit) * rate
            prev_limit = limit
    if income > 2400000:
        tax += (income - 2400000) * 0.30

    return tax


# Compute tax and results
tax = calculate_tax(income, exemption)
disposable_income = income - tax
effective_tax_rate = (tax / income) * 100 if income > 0 else 0

# Display Results
st.subheader("Tax Summary")
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
st.plotly_chart(fig, use_container_width=True)

# Additional Insights
st.subheader("💡 Additional Insights")
st.markdown(
    f"- Your effective tax rate is **{effective_tax_rate:.2f}%** of your total income."
)
st.markdown("- Consider tax-saving investments like NPS, PPF, and ELSS.")
st.markdown("- Higher income moves you into higher tax brackets; plan accordingly.")

# Tax Saving Suggestion
max_tax_saving = min(150000, income * 0.3)
st.success(
    f"🎯 Investing ₹1,50,000 in tax-saving instruments could save up to ₹{max_tax_saving:,.0f} in taxes!"
)

# Tax Slabs Table
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
            return ['background-color: #2863B0FF' for _ in row]
        return [''] * len(row)

styled_df = slab_df.style.apply(highlight_slabs, axis=1)
st.dataframe(styled_df, use_container_width=True, hide_index=True)