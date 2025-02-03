import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="New Tax Regime Calculator India",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Modern Dark Theme CSS
st.markdown(
    """
    <style>
        /* Main theme colors */
        :root {
            --primary-color: #FF9933;
            --secondary-color: #138808;
            --background-dark: #1E1E1E;
            --card-bg: #2D2D2D;
            --text-color: #E0E0E0;
        }
        
        /* Global styles */
        .stApp {
            background-color: var(--background-dark);
            color: var(--text-color);
        }
        
        /* Custom card container */
        .custom-card {
            background-color: var(--card-bg);
            padding: 2rem;
            border-radius: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin: 1rem 0;
        }
        
        /* Input fields */
        .stNumberInput input {
            background-color: #363636;
            color: white;
            border: 1px solid #4A4A4A;
            border-radius: 8px;
            font-size: 1.1rem;
        }
        
        /* Radio buttons */
        .stRadio label {
            color: var(--text-color) !important;
            font-size: 1.1rem;
        }
        
        /* Metrics */
        .metric-card {
            background-color: var(--card-bg);
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid var(--primary-color);
            margin: 0.5rem 0;
        }
        
        /* Headers and text */
        h1, h2, h3 {
            color: var(--primary-color) !important;
            font-weight: 600;
        }
        
        /* Table styling */
        .dataframe {
            background-color: var(--card-bg) !important;
        }
        
        .dataframe th {
            background-color: var(--primary-color) !important;
            color: white !important;
        }
    </style>
""",
    unsafe_allow_html=True,
)


def format_currency(amount):
    """Format amount in Indian currency format"""
    return f"₹{amount:,.2f}"


def calculate_tax_breakdown(income, category):
    """Calculate tax breakdown with updated slabs and exemptions"""
    # Set basic Rebate based on category
    basic_exemption = 1275000 if category == "Salaried" else 1200000

    # Define tax slabs
    slabs = [
        (0, 400000, 0),
        (400000, 800000, 0.05),
        (800000, 1200000, 0.10),
        (1200000, 1600000, 0.15),
        (1600000, 2000000, 0.20),
        (2000000, 2400000, 0.25),
        (2400000, float("inf"), 0.30),
    ]

    # If income is below Rebate limit, return 0 tax
    if income <= basic_exemption:
        return 0, []

    breakdown = []
    total_tax = 0
    remaining_income = income
    diff=income-basic_exemption

    # Calculate tax for each applicable slab
    for lower, upper, rate in slabs:
        if remaining_income <= 0:
            break

        slab_income = min(remaining_income, upper - lower)
        if slab_income > 0:
            slab_tax = slab_income * rate
            total_tax += slab_tax
            breakdown.append(
                {
                    "slab": f"₹{lower:,} - {'∞' if upper == float('inf') else f'₹{upper:,}'}",
                    "rate": f"{rate*100}%",
                    "taxable_amount": slab_income,
                    "tax": slab_tax,
                }
            )
            remaining_income -= slab_income

    return min(total_tax,diff), breakdown


# Main application layout
st.markdown(
    """
    <div style='text-align: center; padding: 2rem 0;'>
        <h1>🇮🇳 Indian Income Tax Calculator</h1>
        <div class='banner'>
            <h3 style='color: white !important;'>New Tax Regime FY 2025-26 (AY 2025-26)</h3>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Create two columns for layout
col1, col2 = st.columns([1, 2])

# Input section
with col1:
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.subheader("📊 Income Details")

    income = st.number_input(
        "Annual Income (₹)",
        min_value=0,
        value=1200000,
        step=10000,
        format="%d",
        help="Enter your total annual income before any deductions",
    )

    category = st.radio(
        "Employment Category",
        ["Salaried", "Others"],
        horizontal=True,
        help="Salaried individuals get tax Rebate up to ₹12.75 Lakhs",
    )

    exemption_limit = "₹12.75 Lakhs" if category == "Salaried" else "₹12 Lakhs"
    st.markdown(
        f"""
        <div style='background-color: #363636; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem;'>
            <p style='margin: 0;'>✨ Tax Rebate up to {exemption_limit}</p>
            <p style='margin: 5px 0 0 0; font-size: 0.9em; color: #888;'>New Tax Regime benefit for FY 2025-26</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

# Calculate tax details
tax, tax_breakdown = calculate_tax_breakdown(income, category)
health_education_cess = tax * 0.04
total_tax = tax + health_education_cess
disposable_income = income - total_tax
effective_tax_rate = (total_tax / income) * 100 if income > 0 else 0

# Results section
with col2:
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.subheader("💰 Tax Calculation Results")

    # Display key metrics
    metrics_col1, metrics_col2 = st.columns(2)

    with metrics_col1:
        st.metric("Total Tax Payable", format_currency(total_tax))
        st.metric("Basic Tax", format_currency(tax))
        st.metric(
            "Health & Education Cess (4%)", format_currency(health_education_cess)
        )

    with metrics_col2:
        st.metric("Disposable Income", format_currency(disposable_income))
        st.metric("Effective Tax Rate", f"{effective_tax_rate:.2f}%")

    # Display tax breakdown
    if tax_breakdown:
        st.subheader("📊 Tax Breakdown")
        df = pd.DataFrame(tax_breakdown)
        st.table(df)

    st.markdown("</div>", unsafe_allow_html=True)

# Important notes section
st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
st.subheader("📝 Important Notes")
st.markdown(
    """
- New Tax Regime Benefits for FY 2025-26:
  - Income up to ₹12 Lakhs is completely tax-free for all taxpayers
  - Salaried individuals get Rebate up to ₹12.75 Lakhs
- Tax Slabs (applicable above Rebate limit):
  - Up to ₹4,00,000: No tax (0%)
  - ₹4,00,001 to ₹8,00,000: 5%
  - ₹8,00,001 to ₹12,00,000: 10%
  - ₹12,00,001 to ₹16,00,000: 15%
  - ₹16,00,001 to ₹20,00,000: 20%
  - ₹20,00,001 to ₹24,00,000: 25%
  - Above ₹24,00,000: 30%
- 4% Health and Education Cess is applicable on the calculated tax
- No other deductions or exemptions are available under the new tax regime
- For accurate tax planning, please consult a tax professional
"""
)
st.markdown("</div>", unsafe_allow_html=True)
