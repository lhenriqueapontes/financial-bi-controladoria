from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd


def load_financials(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def add_margins(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out['gross_margin_pct'] = (out['gross_profit'] / out['net_revenue'] * 100).round(2)
    out['ebitda_margin_pct'] = (out['ebitda'] / out['net_revenue'] * 100).round(2)
    out['cash_flow_margin_pct'] = (out['cash_flow'] / out['net_revenue'] * 100).round(2)
    return out


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    enriched = add_margins(df)
    data = {
        'total_gross_revenue': enriched['gross_revenue'].sum(),
        'total_net_revenue': enriched['net_revenue'].sum(),
        'total_ebitda': enriched['ebitda'].sum(),
        'total_cash_flow': enriched['cash_flow'].sum(),
        'avg_gross_margin_pct': enriched['gross_margin_pct'].mean(),
        'avg_ebitda_margin_pct': enriched['ebitda_margin_pct'].mean(),
    }
    return pd.DataFrame([data]).round(2)


def export(input_path: str, output_dir: str = 'reports') -> None:
    df = load_financials(input_path)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    add_margins(df).to_csv(out / 'financials_with_margins.csv', index=False)
    summarize(df).to_csv(out / 'financial_summary.csv', index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='data/demo_financials.csv')
    parser.add_argument('--output-dir', default='reports')
    args = parser.parse_args()
    export(args.input, args.output_dir)
    print(f'Reports saved to {args.output_dir}')


if __name__ == '__main__':
    main()
