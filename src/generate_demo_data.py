from pathlib import Path
import argparse
import numpy as np
import pandas as pd


def generate(months=24, seed=42):
    rng = np.random.default_rng(seed)
    dates = pd.date_range('2024-01-01', periods=months, freq='MS')
    revenue = rng.normal(250000, 30000, months).round(2)
    taxes = (revenue * 0.10).round(2)
    costs = (revenue * rng.normal(0.48, 0.03, months)).round(2)
    expenses = rng.normal(70000, 7000, months).round(2)
    net_revenue = revenue - taxes
    gross_profit = net_revenue - costs
    ebitda = gross_profit - expenses
    cash_flow = ebitda - rng.normal(15000, 5000, months).round(2)
    return pd.DataFrame({
        'month': dates.strftime('%Y-%m'),
        'gross_revenue': revenue,
        'taxes': taxes,
        'net_revenue': net_revenue,
        'costs': costs,
        'expenses': expenses,
        'gross_profit': gross_profit,
        'ebitda': ebitda,
        'cash_flow': cash_flow,
    })


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--months', type=int, default=24)
    parser.add_argument('--output', default='data/demo_financials.csv')
    args = parser.parse_args()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    generate(args.months).to_csv(out, index=False)
    print(out)


if __name__ == '__main__':
    main()
