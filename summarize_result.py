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
    tasks = [
        "humaneval",
        "mbpp",
    ]

    model_result = [model_name]
    for task in sorted(tasks):
        task_path = os.path.join(model_path, f"{task}.json")
        base_result, plus_result, time_taken = get_task_result(task_path)
        model_result.extend([f"{base_result*100:.1f}", f"{plus_result*100:.1f}", f"{time_taken}s"])

    return model_result


def main(args):
    table = [
        ["Score: Pass@1", "HumanEval", "", "", "MBPP", "", ""],
        ["Model", "Base", "Plus", "Time Taken", "Base", "Plus", "Time Taken"],
    ]
    
    models = os.listdir(args.result_dir)
    for model in models:
        model_path = os.path.join(args.result_dir, model)
        model_result = get_model_result(model_path)
        table.append(model_result)
    
    print(tabulate(table, headers="firstrow", tablefmt="github"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--result_dir", type=str, default="result")
    args = parser.parse_args()

    main(args)
