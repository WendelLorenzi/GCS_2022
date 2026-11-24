"""Runtime configuration. No hard-coded absolute paths, machine-specific ports or secrets.

MQTT settings come from environment variables (optionally loaded from a ``.env`` file):

    GCS_MQTT_HOST       broker address (required to enable MQTT)
    GCS_MQTT_PORT       default 1883
    GCS_MQTT_TOPIC      default teams/1038
    GCS_MQTT_USER       optional
    GCS_MQTT_PASSWORD   optional
"""

from __future__ import annotations

import logging
import os
from collections.abc import Mapping, MutableMapping
from dataclasses import dataclass, field
from pathlib import Path

from gcs.protocol.telemetry import TEAM_ID

log = logging.getLogger(__name__)

ENV_PREFIX = "GCS_"


@dataclass
class MqttConfig:
    host: str = ""
    port: int = 1883
    topic: str = f"teams/{TEAM_ID}"
    username: str = ""
    password: str = field(default="", repr=False)  # never printed/logged

    @property
    def configured(self) -> bool:
        return bool(self.host)

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> MqttConfig:
        env = os.environ if env is None else env
        default = cls()
        port_text = env.get("GCS_MQTT_PORT", "").strip()
        try:
            port = int(port_text) if port_text else default.port
        except ValueError as exc:
            raise ValueError(f"GCS_MQTT_PORT must be an integer, got {port_text!r}") from exc
        return cls(
            host=env.get("GCS_MQTT_HOST", "").strip(),
            port=port,
            topic=env.get("GCS_MQTT_TOPIC", "").strip() or default.topic,
            username=env.get("GCS_MQTT_USER", "").strip(),
            password=env.get("GCS_MQTT_PASSWORD", ""),
        )


@dataclass
class Config:
    team_id: int = TEAM_ID
    serial_port: str | None = None  # None = ask the user / pick from list_ports
    baudrate: int = 9600  # must match the LaunchPad firmware
    output_dir: Path = field(default_factory=lambda: Path.cwd() / "flights")
    mqtt: MqttConfig = field(default_factory=MqttConfig)
    plot_window: int = 1200  # packets kept per type for plotting (C: 20 min, T: 5 min)
    ui_refresh_ms: int = 100
    sim_period: float = 1.0  # SIMP rate required by the competition (1 Hz)

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> Config:
        return cls(mqtt=MqttConfig.from_env(env))


def load_dotenv(path: str | Path = ".env", env: MutableMapping[str, str] | None = None) -> bool:
    """Minimal ``.env`` loader: ``KEY=VALUE`` lines, ``#`` comments, optional quotes.

    Variables already set in the environment win (so the shell can override the file).
    Returns False if the file does not exist.
    """
    env = os.environ if env is None else env
    path = Path(path)
    if not path.is_file():
        return False
    for n, raw in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        line = line.removeprefix("export ")
        key, sep, value = line.partition("=")
        key, value = key.strip(), value.strip()
        if not sep or not key:
            log.warning("%s:%d ignored (expected KEY=VALUE)", path, n)
            continue
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        env.setdefault(key, value)
    return True
