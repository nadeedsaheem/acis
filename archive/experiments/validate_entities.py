import json
import os
import sys

def validate():
    output_file = "all_entities.json"
    summary_file = "parse_summary.json"
    failed_file = "failed_files.json"

    print("==================================================")
    print("VALIDATING PARSED DATASET")
    print("==================================================")

    # 1. Check all_entities.json
    if not os.path.exists(output_file):
        print(f"[ERROR] Final output file '{output_file}' not found.")
        sys.exit(1)

    print(f"Loading '{output_file}'...")
    try:
        with open(output_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"[SUCCESS] '{output_file}' is valid JSON.")
        print(f"[INFO] Loaded {len(data)} file records.")
    except Exception as e:
        print(f"[ERROR] Failed to load '{output_file}': {e}")
        sys.exit(1)

    # 2. Check parse_summary.json
    if not os.path.exists(summary_file):
        print(f"[ERROR] Summary file '{summary_file}' not found.")
    else:
        try:
            with open(summary_file, "r", encoding="utf-8") as f:
                summary = json.load(f)
            print(f"[SUCCESS] '{summary_file}' is valid JSON.")
            print("[INFO] Summary Statistics:")
            for k, v in summary.items():
                print(f"  - {k}: {v}")
        except Exception as e:
            print(f"[ERROR] Failed to load '{summary_file}': {e}")

    # 3. Check failed_files.json
    if not os.path.exists(failed_file):
        print(f"[ERROR] Failed files log '{failed_file}' not found.")
    else:
        try:
            with open(failed_file, "r", encoding="utf-8") as f:
                failed = json.load(f)
            print(f"[SUCCESS] '{failed_file}' is valid JSON.")
            print(f"[INFO] Failed files count: {len(failed)}")
        except Exception as e:
            print(f"[ERROR] Failed to load '{failed_file}': {e}")

    print("==================================================")

if __name__ == "__main__":
    validate()
