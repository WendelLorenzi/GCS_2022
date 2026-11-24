"""Entry point.

    python -m gcs                      # graphical GCS (PySide6)
    python -m gcs --out D:/voos        # choose where flight CSVs are written
    python -m gcs monitor --help       # headless console monitor

GCS_MQTT_* variables are read from the environment or from ./.env.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from gcs.config import Config, load_dotenv


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    load_dotenv()
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
    if argv and argv[0] == "monitor":
        from gcs.cli_monitor import main as monitor_main

        monitor_main(argv[1:])
        return 0

    cfg = Config.from_env()
    ap = argparse.ArgumentParser(prog="gcs", description="LtSat Ground Control Station")
    ap.add_argument("--out", type=Path, default=cfg.output_dir, help="flight CSV folder")
    args = ap.parse_args(argv)
    cfg.output_dir = args.out

    from gcs.ui.app import run  # Qt is imported only for the GUI

    return run(cfg, sys.argv[:1])


if __name__ == "__main__":
    sys.exit(main())
