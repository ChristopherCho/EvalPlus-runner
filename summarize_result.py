import os
import re
import json
import argparse

from glob import glob
from tabulate import tabulate


def get_task_result(task_path):
    with open(task_path, "r") as f:
        result = json.load(f)

    return result["scores"]["base"]["pass@1"], result["scores"]["plus"]["pass@1"], result["time_taken"]


def get_model_result(model_path):
    model_name = os.path.basename(model_path)
    print(f"# {model_name}")

    result_table = [["Task", "Base (pass@1)", "Plus (pass@1)", "Time taken (s)"]]
    
    task_paths = glob(os.path.join(model_path, "*.json"))
    for task_path in sorted(task_paths):
        task = os.path.basename(task_path).split(".")[0]
        base_result, plus_result, time_taken = get_task_result(task_path)
        result_table.append([task, f"{base_result*100:.2f}", f"{plus_result*100:.2f}", time_taken])
    
    print(tabulate(result_table, headers="firstrow", tablefmt="github"))
    print()


def main(args):
    models = os.listdir(args.result_dir)
    for model in models:
        model_path = os.path.join(args.result_dir, model)
        get_model_result(model_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--result_dir", type=str, default="result")
    args = parser.parse_args()

    main(args)
