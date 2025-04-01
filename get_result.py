import os
import re
import json
import argparse


def main(args):
    logfile_path = os.path.join(args.logging_dir, args.task + ".log")
    with open(logfile_path, "r") as f:
        content = f.read()

    base_score_pattern = rf"{args.task}\s\((.*)\)\s+pass@1:\s+(.*)"
    match = re.search(base_score_pattern, content)
    if match is None:
        raise ValueError(f"No match found for {args.task} (base tests)")
    base_score = float(match.group(2))

    plus_score_pattern = rf"{args.task}\+\s\((.*)\)\s+pass@1:\s+(.*)"
    match = re.search(plus_score_pattern, content)
    if match is None:
        raise ValueError(f"No match found for {args.task} (base + extra tests)")
    plus_score = float(match.group(2))
    
    time_consumption_pattern = r"Time taken: (\d+) seconds"
    match = re.search(time_consumption_pattern, content)
    if match is None:
        raise ValueError(f"No match found for {args.task} (time consumption)")
    time_consumption = int(match.group(1))
    
    output_file_path = os.path.join(args.output_dir, args.task + ".json")
    with open(output_file_path, "w") as f:
        json.dump({"time_taken": time_consumption, "scores": {"base": {"pass@1": base_score}, "plus": {"pass@1": plus_score}}}, f, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", type=str, required=True)
    parser.add_argument("--logging_dir", type=str, required=True)
    parser.add_argument("--output_dir", type=str, required=True)
    args = parser.parse_args()

    main(args)
