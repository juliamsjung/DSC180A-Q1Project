from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict


class ToyTabularEnv:
    """Minimal environment wrapper around the toy tabular workspace."""

    def __init__(self, workspace: Path | None = None):
        self.workspace = workspace or Path(__file__).resolve().parent / "workspace"
        self.config_path = self.workspace / "config.json"
        self.results_path = self.workspace / "results.json"
        self.train_script = self.workspace / "train.py"
        self.workspace.mkdir(parents=True, exist_ok=True)

    def read_config(self) -> Dict[str, Any]:
        return json.loads(self.config_path.read_text())

    def write_config(self, cfg: Dict[str, Any]) -> None:
        self.config_path.write_text(json.dumps(cfg, indent=2))

    def run_train(self) -> Dict[str, Any]:
        subprocess.run(
            [sys.executable, str(self.train_script)],
            cwd=self.workspace,
            check=True,
        )
        return json.loads(self.results_path.read_text())


