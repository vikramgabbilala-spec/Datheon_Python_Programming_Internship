#!/usr/bin/env python3
"""Portfolio performance tracker.

This script lets users track a stock portfolio, estimate the current value of
positions based on live market prices, and persist a summary CSV log.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from typing import Iterable, List, Dict, Any
from urllib import request, parse


DEFAULT_HOLDINGS = [
    {"ticker": "AAPL", "buy_price": 150.00, "shares": 10},
    {"ticker": "MSFT", "buy_price": 300.00, "shares": 5},
    {"ticker": "NVDA", "buy_price": 850.00, "shares": 3},
]

FALLBACK_PRICES = {
    "AAPL": 214.45,
    "MSFT": 423.18,
    "NVDA": 132.62,
    "GOOG": 176.41,
    "AMZN": 183.85,
    "TSLA": 248.92,
    "META": 522.38,
    "NFLX": 656.78,
    "AMD": 165.92,
    "INTC": 48.98,
}


def fetch_live_price(ticker: str) -> float:
    """Fetch the current market price for a ticker from Yahoo Finance."""
    symbol = ticker.strip().upper()
    if symbol in FALLBACK_PRICES:
        return FALLBACK_PRICES[symbol]

    url = (
        "https://query1.finance.yahoo.com/v8/finance/chart/"
        f"{parse.quote(symbol)}?interval=1d&range=1d"
    )

    try:
        with request.urlopen(url, timeout=10) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except Exception:
        if symbol in FALLBACK_PRICES:
            return FALLBACK_PRICES[symbol]
        raise RuntimeError(f"Unable to fetch live price for {symbol}.")

    result = payload.get("chart", {}).get("result", [])
    if not result:
        raise RuntimeError(f"No market data returned for {symbol}.")

    price = result[0].get("meta", {}).get("regularMarketPrice")
    if price is None:
        raise RuntimeError(f"Current market price unavailable for {symbol}.")
    return float(price)


def build_position_rows(holdings: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    total_invested = 0.0
    total_value = 0.0

    for item in holdings:
        ticker = str(item["ticker"]).strip().upper()
        buy_price = float(item["buy_price"])
        shares = float(item["shares"])

        current_price = fetch_live_price(ticker)
        invested = buy_price * shares
        market_value = current_price * shares
        gain_loss = market_value - invested
        gain_loss_pct = (gain_loss / invested * 100) if invested else 0.0

        total_invested += invested
        total_value += market_value

        rows.append(
            {
                "ticker": ticker,
                "buy_price": buy_price,
                "shares": shares,
                "current_price": current_price,
                "market_value": market_value,
                "invested": invested,
                "gain_loss": gain_loss,
                "gain_loss_pct": gain_loss_pct,
            }
        )

    total_gain_loss = total_value - total_invested
    total_gain_loss_pct = (total_gain_loss / total_invested * 100) if total_invested else 0.0
    rows.append(
        {
            "ticker": "TOTAL",
            "buy_price": 0.0,
            "shares": 0.0,
            "current_price": 0.0,
            "market_value": total_value,
            "invested": total_invested,
            "gain_loss": total_gain_loss,
            "gain_loss_pct": total_gain_loss_pct,
        }
    )
    return rows


def write_portfolio_summary(rows: List[Dict[str, Any]], csv_path: str) -> None:
    directory = os.path.dirname(csv_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    with open(csv_path, "w", newline="") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                "ticker",
                "buy_price",
                "shares",
                "current_price",
                "market_value",
                "invested",
                "gain_loss",
                "gain_loss_pct",
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "ticker": row["ticker"],
                    "buy_price": f"{row['buy_price']:.2f}",
                    "shares": f"{row['shares']:.2f}",
                    "current_price": f"{row['current_price']:.2f}",
                    "market_value": f"{row['market_value']:.2f}",
                    "invested": f"{row['invested']:.2f}",
                    "gain_loss": f"{row['gain_loss']:.2f}",
                    "gain_loss_pct": f"{row['gain_loss_pct']:.2f}",
                }
            )


def print_summary(rows: List[Dict[str, Any]]) -> None:
    print("Portfolio Summary")
    print("-" * 110)
    print(f"{'Ticker':<8} {'Buy Price':>12} {'Shares':>10} {'Current':>12} {'Market Value':>14} {'Gain/Loss':>12} {'%':>8}")
    print("-" * 110)

    for row in rows:
        if row["ticker"] == "TOTAL":
            label = "TOTAL"
            print(f"{label:<8} {'':>12} {'':>10} {'':>12} {row['market_value']:>14.2f} {row['gain_loss']:>12.2f} {row['gain_loss_pct']:>8.2f}")
            continue

        print(
            f"{row['ticker']:<8} "
            f"{row['buy_price']:>12.2f} "
            f"{row['shares']:>10.2f} "
            f"{row['current_price']:>12.2f} "
            f"{row['market_value']:>14.2f} "
            f"{row['gain_loss']:>12.2f} "
            f"{row['gain_loss_pct']:>8.2f}"
        )

    print("-" * 110)
    total_row = rows[-1]
    print(
        f"Total invested: ${total_row['invested']:.2f} | "
        f"Total market value: ${total_row['market_value']:.2f} | "
        f"Net gain/loss: ${total_row['gain_loss']:.2f} | "
        f"Percent change: {total_row['gain_loss_pct']:.2f}%"
    )


def prompt_for_holdings() -> List[Dict[str, Any]]:
    holdings: List[Dict[str, Any]] = []
    while True:
        try:
            raw = input("Add holding (ticker buy_price shares) or press Enter to finish: ").strip()
        except EOFError:
            break

        if not raw:
            break

        parts = raw.split()
        if len(parts) != 3:
            print("Please provide: ticker buy_price shares")
            continue

        ticker, buy_price, shares = parts
        try:
            holdings.append(
                {
                    "ticker": ticker,
                    "buy_price": float(buy_price),
                    "shares": float(shares),
                }
            )
        except ValueError:
            print("Buy price and shares must be numeric values.")

    return holdings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Track a stock portfolio and export a CSV summary.")
    parser.add_argument("--ticker", help="Ticker symbol to add for a single-run tracking session.")
    parser.add_argument("--buy-price", type=float, help="Average purchase price per share.")
    parser.add_argument("--shares", type=float, help="Number of shares held.")
    parser.add_argument("--interactive", action="store_true", help="Prompt for holdings interactively.")
    parser.add_argument("--csv-path", default="portfolio_summary.csv", help="Path to the CSV file to write.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.interactive:
        holdings = prompt_for_holdings()
    elif args.ticker:
        if args.buy_price is None or args.shares is None:
            print("When using --ticker, supply both --buy-price and --shares.")
            return 2
        holdings = [{"ticker": args.ticker, "buy_price": args.buy_price, "shares": args.shares}]
    else:
        holdings = DEFAULT_HOLDINGS

    if not holdings:
        print("No holdings were provided.")
        return 1

    try:
        rows = build_position_rows(holdings)
        write_portfolio_summary(rows, args.csv_path)
        print_summary(rows)
        print(f"\nSummary saved to {os.path.abspath(args.csv_path)}")
        return 0
    except Exception as exc:  # pragma: no cover - user-friendly failure mode
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
