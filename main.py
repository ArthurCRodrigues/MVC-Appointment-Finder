import argparse
from searcher import continuous_search

if __name__ == "__main__":
    # Step 1: Create an argument parser
    parser = argparse.ArgumentParser(description="CLI for continuous appointment search")
    parser.add_argument(
        "--days", type=int, required=True, help="Number of days to search for available appointments"
    )
    parser.add_argument(
        "--interval", type=int, default=10, help="Time in seconds between each check (default: 10 seconds)"
    )

    # Step 2: Parse command-line arguments
    args = parser.parse_args()

    # Step 3: Validate the --days and --interval arguments
    if args.days <= 0:
        print("Error: The value for --days must be greater than 0.")
    elif args.interval <= 0:
        print("Error: The value for --interval must be greater than 0.")
    else:
        # Step 4: Call continuous_search with the specified number of days and interval
        continuous_search(days=args.days, check_interval=args.interval)
