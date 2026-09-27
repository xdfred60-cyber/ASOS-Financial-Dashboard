import streamlit as st
import pandas as pd

st.title("ASOS Financial Analysis Dashboard")

st.write(
    "An interactive financial analysis tool analysing ASOS plc's "
    "FY2024 and FY2025 financial performance using Python, Pandas "
    "and Streamlit."
)

# ASOS financial data
asos_data = {
    "year": [2024, 2025],
    "revenue": [2906.5, 2478.0],
    "operating_profit": [-331.9, -212.3],
    "net_income": [-379.4, -298.4],
    "current_assets": [1146.4, 1122.9],
    "current_liabilities": [714.0, 689.0],
    "debt": [688.1, 668.8],
    "equity": [521.3, 212.4]
}

asos_df = pd.DataFrame(asos_data)
st.subheader("ASOS Financial Data")
st.dataframe(asos_df)

def revenue_growth(current_revenue, previous_revenue):
    if previous_revenue == 0:
        return None
    
    return (current_revenue - previous_revenue) / previous_revenue


def operating_margin(operating_profit, revenue):
    if revenue == 0:
        return None
    
    return operating_profit / revenue


def net_margin(net_income, revenue):
    if revenue == 0:
        return None
    
    return net_income / revenue


def roe(net_income, equity):
    if equity == 0:
        return None
    
    return net_income / equity


def current_ratio(current_assets, current_liabilities):
    if current_liabilities == 0:
        return None
    
    return current_assets / current_liabilities


def debt_to_equity(debt, equity):
    if equity == 0:
        return None
    
    return debt / equity

revenue_growth_2025 = revenue_growth(
    asos_df["revenue"].iloc[1],
    asos_df["revenue"].iloc[0]
)

operating_margin_2025 = operating_margin(
    asos_df["operating_profit"].iloc[1],
    asos_df["revenue"].iloc[1]
)

net_margin_2025 = net_margin(
    asos_df["net_income"].iloc[1],
    asos_df["revenue"].iloc[1]
)

roe_2025 = roe(
    asos_df["net_income"].iloc[1],
    asos_df["equity"].iloc[1]
)

current_ratio_2025 = current_ratio(
    asos_df["current_assets"].iloc[1],
    asos_df["current_liabilities"].iloc[1]
)

debt_to_equity_2025 = debt_to_equity(
    asos_df["debt"].iloc[1],
    asos_df["equity"].iloc[1]
)
ai_prompt = f"""
Analyse ASOS plc's FY2025 financial performance using ONLY the
following calculated figures:

Revenue growth: {revenue_growth_2025:.1%}
Operating margin: {operating_margin_2025:.2%}
Net margin: {net_margin_2025:.2%}
ROE: {roe_2025:.2%}
Current ratio: {current_ratio_2025:.2f}
Debt-to-equity: {debt_to_equity_2025:.2%}

Provide:

1. Financial overview
2. Key strengths
3. Key risks
4. Areas that require further investigation

Do not invent additional financial figures.
Do not provide investment advice.
Clearly distinguish between the financial figures and your interpretation.
"""
st.subheader("FY2025 Key Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Revenue Growth", f"{revenue_growth_2025:.1%}")

with col2:
    st.metric("Operating Margin", f"{operating_margin_2025:.2%}")

with col3:
    st.metric("Net Margin", f"{net_margin_2025:.2%}")

col4, col5, col6 = st.columns(3)

with col4:
    st.metric("ROE", f"{roe_2025:.2%}")

with col5:
    st.metric("Current Ratio", f"{current_ratio_2025:.2f}")

with col6:
    st.metric("Debt-to-Equity", f"{debt_to_equity_2025:.2%}")
st.subheader("Year-on-Year Financial Changes")

revenue_change = (
    (asos_df["revenue"].iloc[1] - asos_df["revenue"].iloc[0])
    / asos_df["revenue"].iloc[0]
)

operating_loss_change = (
    (asos_df["operating_profit"].iloc[1] - asos_df["operating_profit"].iloc[0])
    / abs(asos_df["operating_profit"].iloc[0])
)

net_income_change = (
    (asos_df["net_income"].iloc[1] - asos_df["net_income"].iloc[0])
    / abs(asos_df["net_income"].iloc[0])
)

change_data = {
    "Metric": [
        "Revenue",
        "Operating Loss",
        "Net Loss"
    ],
    "FY2025 Change": [
        f"{revenue_change:.1%}",
        f"{operating_loss_change:.1%}",
        f"{net_income_change:.1%}"
    ]
}

change_df = pd.DataFrame(change_data)

st.dataframe(change_df)
st.subheader("WACC Calculation")

# Assumptions
cost_of_equity = st.slider(
    "Cost of Equity",
    min_value=0,
    max_value=20,
    value=10,
    step=1,
    format="%d%%"
) / 100

cost_of_debt = st.slider(
    "Cost of Debt",
    min_value=0,
    max_value=15,
    value=6,
    step=1,
    format="%d%%"
) / 100

tax_rate = st.slider(
    "Tax Rate",
    min_value=0,
    max_value=40,
    value=25,
    step=1,
    format="%d%%"
) / 100
st.subheader("DCF Valuation")

# DCF assumptions
starting_fcf = st.number_input(
    "Starting Free Cash Flow (£m)",
    value=100.0,
    step=10.0
)

growth_rate = st.slider(
    "FCF Growth Rate",
    min_value=-10,
    max_value=20,
    value=5,
    step=1,
    format="%d%%"
) / 100

terminal_growth = st.slider(
    "Terminal Growth Rate",
    min_value=0.0,
    max_value=5.0,
    value=2.0,
    step=0.5,
    format="%.1f%%"
) / 100

# Forecast free cash flow for 5 years
fcf_forecast = []

for year in range(1, 6):
    fcf = starting_fcf * (1 + growth_rate) ** year
    fcf_forecast.append(fcf)

fcf_df = pd.DataFrame({
    "Year": ["1", "2", "3", "4", "5"],
    "Forecast FCF (£m)": fcf_forecast
})

st.write("5-Year Free Cash Flow Forecast")

st.dataframe(fcf_df, hide_index=True)
debt = asos_df["debt"].iloc[1]
equity = asos_df["equity"].iloc[1]

total_capital = debt + equity

equity_weight = equity / total_capital
debt_weight = debt / total_capital

wacc = (
    equity_weight * cost_of_equity
    + debt_weight * cost_of_debt * (1 - tax_rate)
)

st.metric("Estimated WACC", f"{wacc:.2%}")
# Discount each year's FCF back to present value
present_values = []

for year in range(1, 6):
    present_value = fcf_forecast[year - 1] / (1 + wacc) ** year
    present_values.append(present_value)

fcf_df["Present Value (£m)"] = present_values

st.write("Discounted Free Cash Flow")

st.dataframe(fcf_df, hide_index=True)
# Calculate terminal value
st.write("Terminal Value")

if wacc <= terminal_growth:
    st.error(
        "WACC must be greater than the Terminal Growth Rate "
        "for the DCF calculation to be valid."
    )
else:
    terminal_fcf = fcf_forecast[-1] * (1 + terminal_growth)

    terminal_value = (
        terminal_fcf / (wacc - terminal_growth)
    )

    st.metric(
        "Terminal Value (£m)",
        f"£{terminal_value:,.2f}m"
    )
        # Calculate present value of terminal value
    terminal_value_pv = (
        terminal_value / (1 + wacc) ** 5
    )

    # Calculate enterprise value
    enterprise_value = (
        sum(present_values) + terminal_value_pv
    )

    st.metric(
        "Enterprise Value (£m)",
        f"£{enterprise_value:,.2f}m"
    )
    st.write("DCF Valuation Breakdown")

    dcf_breakdown = {
        "Component": [
            "PV of Forecast FCFs",
            "PV of Terminal Value",
            "Enterprise Value"
        ],
        "Value (£m)": [
            sum(present_values),
            terminal_value_pv,
            enterprise_value
        ]
    }

    dcf_breakdown_df = pd.DataFrame(dcf_breakdown)

    st.dataframe(
        dcf_breakdown_df,
        hide_index=True
    )
        # Calculate equity value
    net_debt = debt

    equity_value = enterprise_value - net_debt

    st.metric(
        "Estimated Equity Value (£m)",
        f"£{equity_value:,.2f}m"
    )
    st.write("Enterprise Value Sensitivity")

    sensitivity_data = []

    for wacc_scenario in [wacc - 0.01, wacc, wacc + 0.01]:
        row = []

        for growth_scenario in [
            terminal_growth - 0.005,
            terminal_growth,
            terminal_growth + 0.005
        ]:
            if wacc_scenario <= growth_scenario:
                value = None
            else:
                terminal_fcf_scenario = (
                    fcf_forecast[-1] * (1 + growth_scenario)
                )

                terminal_value_scenario = (
                    terminal_fcf_scenario
                    / (wacc_scenario - growth_scenario)
                )

                terminal_value_pv_scenario = (
                    terminal_value_scenario
                    / (1 + wacc_scenario) ** 5
                )

                value = (
                    sum(
                        fcf_forecast[i] / (1 + wacc_scenario) ** (i + 1)
                        for i in range(5)
                    )
                    + terminal_value_pv_scenario
                )

            row.append(value)

        sensitivity_data.append(row)

    sensitivity_df = pd.DataFrame(
        sensitivity_data,
        index=[
            f"{(wacc - 0.01):.1%}",
            f"{wacc:.1%}",
            f"{(wacc + 0.01):.1%}"
        ],
        columns=[
            f"{(terminal_growth - 0.005):.1%}",
            f"{terminal_growth:.1%}",
            f"{(terminal_growth + 0.005):.1%}"
        ]
    )

    sensitivity_df.index.name = "WACC"
    sensitivity_df.columns.name = "Terminal Growth"

    st.dataframe(
        sensitivity_df.style.format("£{:,.2f}m")
    )
st.subheader("Net Income Trend")

chart_data = asos_df.copy()
chart_data["year"] = chart_data["year"].astype(str)

st.line_chart(
    chart_data.set_index("year")["net_income"],
    height=400
)
st.subheader("Revenue Trend")

revenue_chart_data = asos_df.copy()
revenue_chart_data["year"] = revenue_chart_data["year"].astype(str)

st.bar_chart(
    revenue_chart_data.set_index("year")["revenue"]
)
st.subheader("Key Financial Ratios")

ratios_data = {
    "Metric": [
        "Revenue Growth",
        "Operating Margin",
        "Net Margin",
        "ROE",
        "Current Ratio",
        "Debt-to-Equity"
    ],
    
    "FY2025": [
        f"{revenue_growth_2025:.1%}",
        f"{operating_margin_2025:.2%}",
        f"{net_margin_2025:.2%}",
        f"{roe_2025:.2%}",
        f"{current_ratio_2025:.2f}",
        f"{debt_to_equity_2025:.2%}"
    ]
}

ratios_df = pd.DataFrame(ratios_data)

st.dataframe(ratios_df)
st.subheader("Assumptions & Data Sources")

st.write("""
Data Source: ASOS plc FY2024 and FY2025 financial reports.

Calculations: Financial ratios are calculated using standard
financial formulas from the reported financial statement data.

AI Commentary: The AI will receive the calculated financial
figures and provide interpretation. It will not perform the
underlying financial calculations.

Limitation: This dashboard is an educational financial analysis
project and does not provide investment advice.
""")
st.subheader("AI Financial Commentary")

st.markdown("### Financial Overview")

st.write(
    "ASOS experienced a decline in revenue in FY2025, while its "
    "operating and net margins remained negative. However, the "
    "net loss was smaller than in FY2024."
)

st.markdown("### Key Risks")

st.write(
    "The negative operating margin and net margin indicate that "
    "ASOS remained loss-making. The high debt-to-equity ratio also "
    "shows that debt is significant relative to reported equity."
)

st.markdown("### Areas to Investigate")

st.write(
    "Further analysis could examine the reasons behind the decline "
    "in revenue, the drivers of operating losses, and changes in "
    "ASOS's debt and equity position."
)
st.subheader("AI Analysis Prompt")

st.code(ai_prompt, language="text")

st.download_button(
    label="Download AI Prompt",
    data=ai_prompt,
    file_name="asos_ai_prompt.txt",
    mime="text/plain"
)