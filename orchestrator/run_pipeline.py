"""Simple orchestration entrypoint for learning multi-agent flows."""

from datetime import datetime


def run_ingestion_agent() -> None:
    print("[ingestion-agent] syncing 13F and institution snapshots...")


def run_market_agent() -> None:
    print("[market-agent] syncing Nasdaq company fundamentals...")


def run_valuation_agent() -> None:
    print("[valuation-agent] recalculating score cache...")


def main() -> None:
    print(f"Pipeline start: {datetime.utcnow().isoformat()}Z")
    run_ingestion_agent()
    run_market_agent()
    run_valuation_agent()
    print("Pipeline complete")


if __name__ == "__main__":
    main()
