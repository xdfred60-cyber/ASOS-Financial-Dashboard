# ASOS Financial Analysis Dashboard

## Project Overview
An interactive Streamlit dashboard analysing ASOS plc's FY2024–FY2025 financial performance. It calculates core financial ratios from reported figures, produces an illustrative DCF valuation, and generates AI commentary based on the calculated results.

## Features
- Revenue, profit and revenue growth analysis (FY2024 vs FY2025)
- Key ratios: operating margin, net margin, ROE, current ratio, debt-to-equity
- Illustrative DCF valuation (WACC, 5-year FCF forecast, terminal value, enterprise/equity value) with user-adjustable assumptions
- AI-generated commentary interpreting the calculated figures
- Interactive Streamlit dashboard with charts and an assumptions/data-sources section

## Technologies
- Python, Pandas
- Streamlit
- [Anthropic Claude API — confirm once you answer above]

## Methodology
Company financial data (revenue, profit, balance sheet items) is taken directly from ASOS plc's FY2024 and FY2025 Annual Report and Accounts. Python and Pandas calculate the core ratios using standard formulas. A separate DCF section applies WACC and discounted-cash-flow methodology, using user-adjustable assumptions (cost of equity, cost of debt, terminal growth rate) rather than figures derived from ASOS's actual market data — this is disclosed in the app.

## AI Component
The AI interprets the ratios and figures already calculated by Python — it does not perform the underlying calculations itself. This reduces the risk of the AI inventing or miscalculating financial data. The prompt restricts the AI to only the figures provided, and this was tested by supplying incomplete data and confirming the AI did not invent the missing ratios.

## Limitations
- Two years of reported data only
- DCF assumptions (cost of equity, cost of debt, terminal growth) are illustrative and user-set, not derived from ASOS's actual beta or market data
- Net debt is simplified as total reported debt (not adjusted for cash)
- AI commentary is generated interpretation based on calculated figures, not independently verified financial advice
- Not intended as investment advice

## Future Improvements
- Derive cost of equity via CAPM using ASOS's actual beta
- More companies / peer comparison
- Automated historical data pulls
