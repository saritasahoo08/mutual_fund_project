"""
run_pipeline.py

Master script for the Bluestock Mutual Fund Capstone Project.

This script runs the full data pipeline in order:
    1. Clean the raw data (data_cleaning.py)
    2. Build the SQLite database (create_database.py)

Run this file from the project's main folder like this:
    python run_pipeline.py

Each step prints its own progress. If a step fails, the pipeline
stops and shows which step caused the problem.
"""

import subprocess
import sys
import time


def run_step(step_name, script_path):
    """
    Run one script as a separate step in the pipeline.

    step_name: a short label printed to the screen (e.g. "Data Cleaning")
    script_path: the path to the .py file to run (e.g. "data_cleaning.py")

    Returns True if the script finished without errors, False otherwise.
    """
    print("\n" + "=" * 60)
    print(f"STEP: {step_name}")
    print("=" * 60)

    start_time = time.time()

    # run the script and wait for it to finish
    result = subprocess.run([sys.executable, script_path])

    elapsed = round(time.time() - start_time, 1)

    if result.returncode == 0:
        print(f"\n{step_name} finished successfully in {elapsed} seconds.")
        return True
    else:
        print(f"\n{step_name} FAILED after {elapsed} seconds.")
        return False


def main():
    """
    Run every step of the pipeline in order.
    Stops immediately if any step fails.
    """
    print("BLUESTOCK MUTUAL FUND CAPSTONE - FULL PIPELINE")
    print("Starting pipeline run...")

    steps = [
        ("Data Cleaning", "data_cleaning.py"),
        ("Database Creation", "create_database.py"),
    ]

    for step_name, script_path in steps:
        success = run_step(step_name, script_path)
        if not success:
            print(f"\nPipeline stopped because '{step_name}' failed.")
            print("Fix the error above and run this script again.")
            sys.exit(1)

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE")
    print("=" * 60)
    print("All cleaned data and the SQLite database are ready.")
    print("Database location: data/db/bluestock_mf.db")


if __name__ == "__main__":
    main()