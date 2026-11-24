"""Publishes every received telemetry line to the competition MQTT broker.

``MqttPublisher`` is a PacketSink whose on/off state is independent of the session
(MQTT ENABLE / MQTT DISABLE buttons). paho runs its own network thread with automatic
reconnection; ``publish`` never blocks the main thread. Packets that arrive while the broker
is unreachable are counted as dropped, never queued without limit.
"""

from __future__ import annotations

import logging
import threading
import uuid
from collections.abc import Callable
from typing import Any

import paho.mqtt.client as mqtt

from gcs.config import MqttConfig
from gcs.protocol.telemetry import Packet

log = logging.getLogger(__name__)

ClientFactory = Callable[[str], Any]


def _default_client(client_id: str) -> mqtt.Client:
    return mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)


class MqttPublisher:
    def __init__(self, config: MqttConfig, client_factory: ClientFactory = _default_client) -> None:
        self.config = config
        self._factory = client_factory
        self._client: Any = None
        self._lock = threading.Lock()  # paho callbacks run on its network thread
        self.enabled = False
        self.connected = False
        self.last_error = ""
        self.published = 0
        self.dropped = 0

    # -- operator actions ------------------------------------------------------------------
    def enable(self) -> bool:
        if self.enabled:
            return True
        if not self.config.configured:
            self.last_error = "GCS_MQTT_HOST not set"
            log.warning("MQTT not enabled: %s", self.last_error)
            return False
        client = self._factory(f"ltsat-gcs-{uuid.uuid4().hex[:8]}")
        if self.config.username:
            client.username_pw_set(self.config.username, self.config.password or None)
        client.on_connect = self._on_connect
        client.on_disconnect = self._on_disconnect
        client.reconnect_delay_set(min_delay=1, max_delay=10)
        try:
            client.connect_async(self.config.host, self.config.port, keepalive=30)
            client.loop_start()
        except (OSError, ValueError) as exc:
            self.last_error = str(exc)
            log.error("MQTT start failed: %s", exc)
            return False
        self._client = client
        self.enabled = True
        log.info(
            "MQTT enabled: %s:%d topic %s", self.config.host, self.config.port, self.config.topic
        )
        return True

    def disable(self) -> None:
        client, self._client = self._client, None
        self.enabled = False
        with self._lock:
            self.connected = False
        if client is not None:
            try:
                client.disconnect()
                client.loop_stop()
            except OSError as exc:
                log.warning("MQTT disconnect error: %s", exc)
            log.info("MQTT disabled (published=%d, dropped=%d)", self.published, self.dropped)

    # -- PacketSink ------------------------------------------------------------------------
    def open_session(self) -> None:
        self.published = self.dropped = 0

    def on_packet(self, packet: Packet) -> None:
        client = self._client
        if client is None:
            return
        if not self.connected:
            self.dropped += 1
            return
        info = client.publish(self.config.topic, ",".join(packet.raw), qos=0)
        if info.rc == mqtt.MQTT_ERR_SUCCESS:
            self.published += 1
        else:
            self.dropped += 1

    def close_session(self) -> None:
        """MQTT stays as the operator left it; the session end does not disconnect."""

    # -- paho callbacks (network thread) ---------------------------------------------------
    def _on_connect(self, client, userdata, flags, reason_code, properties=None) -> None:
        # paho v2 passes a ReasonCode (has .is_failure); fall back to a plain int
        is_failure = getattr(reason_code, "is_failure", None)
        ok = (not is_failure) if is_failure is not None else reason_code == 0
        with self._lock:
            self.connected = ok
        if ok:
            self.last_error = ""
            log.info("MQTT connected to %s:%d", self.config.host, self.config.port)
        else:
            self.last_error = f"connection refused: {reason_code}"
            log.error("MQTT %s", self.last_error)

    def _on_disconnect(self, client, userdata, flags, reason_code, properties=None) -> None:
        with self._lock:
            self.connected = False
        if self.enabled:
            log.warning("MQTT disconnected (%s); retrying", reason_code)
