import paho.mqtt.client as mqtt
import pytest

from gcs.config import Config, MqttConfig, load_dotenv
from gcs.mqtt import MqttPublisher
from gcs.protocol.telemetry import parse_line

C1 = "1038,10:00:00.00,1,C,F,N,100.0,25.0,7.50,10:00:00,37.1966,-80.5786,710.0,8,ASCENT,CXON"


# -- config -------------------------------------------------------------------------------
def test_mqtt_config_defaults():
    cfg = MqttConfig.from_env({})
    assert (cfg.host, cfg.port, cfg.topic, cfg.username, cfg.password) == (
        "", 1883, "teams/1038", "", ""
    )
    assert not cfg.configured


def test_mqtt_config_from_env_and_password_hidden():
    env = {
        "GCS_MQTT_HOST": " broker.example ",
        "GCS_MQTT_PORT": "8883",
        "GCS_MQTT_TOPIC": "teams/9999",
        "GCS_MQTT_USER": "ltsat",
        "GCS_MQTT_PASSWORD": "s3cret",
    }
    cfg = Config.from_env(env).mqtt
    assert (cfg.host, cfg.port, cfg.topic, cfg.username, cfg.password) == (
        "broker.example", 8883, "teams/9999", "ltsat", "s3cret"
    )
    assert "s3cret" not in repr(cfg)


def test_mqtt_config_bad_port():
    with pytest.raises(ValueError, match="GCS_MQTT_PORT"):
        MqttConfig.from_env({"GCS_MQTT_PORT": "abc"})


def test_load_dotenv(tmp_path):
    f = tmp_path / ".env"
    f.write_text(
        "# comment\n\nGCS_MQTT_HOST=broker.local\nexport GCS_MQTT_USER='team'\n"
        'GCS_MQTT_PASSWORD="a b=c"\nGCS_MQTT_TOPIC=from_file\ngarbage line\n'
    )
    env = {"GCS_MQTT_TOPIC": "from_shell"}
    assert load_dotenv(f, env)
    assert env == {
        "GCS_MQTT_HOST": "broker.local",
        "GCS_MQTT_USER": "team",
        "GCS_MQTT_PASSWORD": "a b=c",
        "GCS_MQTT_TOPIC": "from_shell",  # shell wins
    }
    assert not load_dotenv(tmp_path / "missing.env", env)


# -- publisher ----------------------------------------------------------------------------
class FakeInfo:
    def __init__(self, rc):
        self.rc = rc


class FakeClient:
    def __init__(self, client_id):
        self.client_id = client_id
        self.calls = []
        self.messages = []
        self.publish_rc = mqtt.MQTT_ERR_SUCCESS

    def username_pw_set(self, user, password):
        self.calls.append(("auth", user, password))

    def reconnect_delay_set(self, **kw):
        pass

    def connect_async(self, host, port, keepalive):
        self.calls.append(("connect", host, port))

    def loop_start(self):
        self.calls.append("loop_start")

    def loop_stop(self):
        self.calls.append("loop_stop")

    def disconnect(self):
        self.calls.append("disconnect")

    def publish(self, topic, payload, qos=0):
        self.messages.append((topic, payload))
        return FakeInfo(self.publish_rc)


def make(cfg=None):
    clients = []

    def factory(client_id):
        clients.append(FakeClient(client_id))
        return clients[-1]

    cfg = cfg or MqttConfig(host="broker.local", username="team", password="pw")
    return MqttPublisher(cfg, client_factory=factory), clients


def connect(pub, clients, rc=0):
    pub._on_connect(clients[-1], None, {}, rc, None)


def test_enable_requires_host():
    pub, clients = make(MqttConfig())
    assert not pub.enable()
    assert "GCS_MQTT_HOST" in pub.last_error and not clients


def test_publishes_raw_line_to_topic_when_connected():
    pub, clients = make()
    packet = parse_line(C1)
    pub.on_packet(packet)  # disabled: ignored silently
    assert pub.enable()
    c = clients[0]
    assert ("auth", "team", "pw") in c.calls and ("connect", "broker.local", 1883) in c.calls
    pub.on_packet(packet)  # enabled but not connected yet
    assert pub.dropped == 1 and c.messages == []
    connect(pub, clients)
    pub.on_packet(packet)
    assert c.messages == [("teams/1038", C1)]
    assert pub.published == 1


def test_counts_publish_failures_and_disconnects():
    pub, clients = make()
    pub.enable()
    connect(pub, clients)
    clients[0].publish_rc = mqtt.MQTT_ERR_NO_CONN
    pub.on_packet(parse_line(C1))
    assert pub.dropped == 1
    pub._on_disconnect(clients[0], None, {}, 7, None)
    assert not pub.connected


def test_refused_connection_sets_error():
    pub, clients = make()
    pub.enable()
    connect(pub, clients, rc=5)
    assert not pub.connected and "refused" in pub.last_error


def test_disable_and_session_end():
    pub, clients = make()
    pub.enable()
    connect(pub, clients)
    pub.close_session()  # session end must not disconnect
    assert pub.enabled and "disconnect" not in clients[0].calls
    pub.disable()
    assert not pub.enabled and not pub.connected
    assert clients[0].calls[-2:] == ["disconnect", "loop_stop"]
    pub.on_packet(parse_line(C1))
    assert len(clients[0].messages) == 0
    assert pub.enable() and len(clients) == 2  # fresh client on re-enable
