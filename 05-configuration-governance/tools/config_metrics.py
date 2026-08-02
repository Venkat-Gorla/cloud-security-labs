"""
uv run tools/config_metrics.py
"""

import boto3


def print_config_metrics(metrics) -> None:
    for metric in sorted(metrics, key=lambda m: m["MetricName"]):
        print(metric["MetricName"])

        if metric["Dimensions"]:
            for dimension in metric["Dimensions"]:
                print(
                    f"    {dimension['Name']} = "
                    f"{dimension.get('Value', '*')}"
                )

        print()

    # unique_metric_names = {
    #     metric["MetricName"]
    #     for metric in metrics
    # }

    # print("\nPrinting Config metric names:")
    # print("=============================")
    # for name in sorted(unique_metric_names):
    #     print(name)


def main() -> None:
    client = boto3.client("cloudwatch")
    paginator = client.get_paginator("list_metrics")

    metrics = []

    for page in paginator.paginate(Namespace="AWS/Config"):
        metrics.extend(page["Metrics"])

    print(f"Metrics Found : {len(metrics)}\n")
    print_config_metrics(metrics)


if __name__ == "__main__":
    main()
