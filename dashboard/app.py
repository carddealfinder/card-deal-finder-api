"""
dashboard/app.py
------------------
Interactive command-line dashboard for Card Deal Finder.

Features:
- Search for a card
- Pull aggregated pricing
- Score the deal (deal score, market value, risk)
- Display results in a styled ASCII dashboard
"""

import os
import sys
import time

# Import your aggregator and scorers
from pricing.aggregator import aggregate_card_prices
from pricing.scorers import score_card


LINE = "─" * 60


def clear_screen():
    """Clear terminal for a clean UI."""
    os.system("cls" if os.name == "nt" else "clear")


def print_header():
    print("\n" + LINE)
    print(" 🔍  CARD DEAL FINDER — COMMAND DASHBOARD ".center(60))
    print(LINE + "\n")


def format_price(value):
    return f"${value:.2f}" if value is not None else "N/A"


def show_results(query, aggregated, scored):
    clear_screen()
    print_header()

    print(f"Search Query: {query}\n")
    print(LINE)

    # Marketplace Prices
    print("📊 Marketplace Pricing")
    print(LINE)
    print(f"• eBay Avg:      {format_price(aggregated.get('ebay_avg'))}")
    print(f"• COMC Avg:      {format_price(aggregated.get('comc_avg'))}")
    print(f"• StockX Avg:    {format_price(aggregated.get('stockx_avg'))}")
    print(f"• Goldin Avg:    {format_price(aggregated.get('goldin_avg'))}")
    print(f"• Best Price:    {format_price(aggregated.get('best_price'))}")
    print(LINE)

    # Scoring Summary
    print("📈 Deal Scoring")
    print(LINE)
    print(f"• Market Value:        {format_price(scored['market_value'])}")
    print(f"• Deal Score:          {scored['deal_score']} / 100")
    print(f"• % Under Market:      {scored['percent_under_market']}%")
    print(f"• Risk Score:          {scored['risk_score']} / 100")
    print(f"• Trend Score:         {scored['trend_score']} / 100")
    print(LINE)

    # Recommendation
    print("📝 Recommendation")
    print(LINE)
    print(f"{scored['recommendation']}\n")
    print(LINE)

    input("\nPress ENTER to return to search...")


def main():
    clear_screen()
    print_header()

    print("Type a card to search (ex: '2020 Prizm Herbert Silver PSA 10')")
    print("Type 'exit' to quit.\n")

    while True:
        query = input("🔎 Enter card search: ").strip()

        if not query:
            continue
        if query.lower() == "exit":
            print("\nGoodbye! 👋")
            time.sleep(0.5)
            sys.exit()

        clear_screen()
        print_header()
        print(f"Searching for: {query}...\n")
        time.sleep(0.3)

        # Step 1: Aggregate marketplace data
        aggregated = aggregate_card_prices(query)

        # Step 2: Score the deal
        scored = score_card(aggregated)

        # Step 3: Display results
        show_results(query, aggregated, scored)


if __name__ == "__main__":
    main()
