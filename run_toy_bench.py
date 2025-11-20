#!/usr/bin/env python3
"""
Opt-in runner that executes the toy tabular bench under a Phoenix span.
"""
from __future__ import annotations

import argparse
import json

from code import PhoenixTracerManager, _phoenix_settings, load_config
from toy_bench.toy_tabular.toy_agent import run_toy_tabular


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the toy tabular bench with Phoenix tracing.")
    parser.add_argument("--config", default="config.json", help="Path to the main project config.")
    parser.add_argument("--num-steps", type=int, help="Override number of tuning steps (default=3).")
    args = parser.parse_args()

    cfg = load_config(args.config)
    default_steps = int(cfg.get("toy_bench", {}).get("num_steps", 3))
    num_steps = args.num_steps or default_steps

    tracer = PhoenixTracerManager(_phoenix_settings(cfg))
    span_cm = tracer.span(
        "toybench.toy_tabular_run",
        {
            "benchmark": "toy_bench",
            "task_name": "toy_tabular",
            "num_steps": num_steps,
        },
    )
    try:
        with span_cm as span:
            results = run_toy_tabular(num_steps=num_steps, tracer=tracer)
            if span:
                tracer.set_attributes(
                    span,
                    {
                        "final_accuracy": results["final_accuracy"],
                        "final_C": results["final_config"]["C"],
                        "final_max_iter": results["final_config"]["max_iter"],
                    },
                )
    finally:
        tracer.shutdown()

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()


