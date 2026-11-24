# Contexto do projeto — LtSat GCS V2

> Arquivo de contexto para agentes de IA. Leia antes de alterar qualquer coisa em `V2/`.
> Plano de execução e status: [PLANEJAMENTO.md](PLANEJAMENTO.md).

## 1. O que é

**GCS (Ground Control Station)** da equipe **LtSat (Team #1038)** — UTFPR, Brasil — para a
**CanSat Competition 2022** (EUA). É o software que roda no laptop da estação em solo e:

1. Recebe telemetria do CanSat via porta serial (USB).
2. Mostra os dados em tempo real (gráficos + indicadores).
3. Salva a telemetria em CSV no formato exigido pelos juízes.
4. Envia comandos ao CanSat (telemetria on/off, ajuste de hora, modo simulação).
5. Executa o **modo simulação** (envia pressões de um CSV a 1 Hz).
6. Publica a telemetria em um broker **MQTT**.

`V2/` é uma reescrita do zero. O código antigo (`GUI_2022/main.py`, `tela.py`, `src/`) é
**apenas referência** — não importe nada dele e não o modifique.

## 2. A missão (resumo do PDR)

- CanSat = **Container** + **Tethered Payload** (presa por cabo de 10 m).
- Lançado por foguete a 670–725 m. Desce a 15 m/s (paraquedas 1). A **400 m** abre o
  paraquedas 2 (5 m/s). A **300 m** o payload é liberado e desce 10 m em 20 s por uma
  polia com motor, mantendo uma câmera apontada para o **Sul, 45° para baixo**.
- Bonus objective: **não** será tentado.

### Cadeia de comunicação

```
Payload (MSP432 + XBee SX) ──RF 4 Hz──► Container (MSP432 + XBee SX)
Container ──RF──► XBee SX + antena AP3900 ──UART──► MSP432 LaunchPad ──USB serial──► Laptop (GCS)
```

- Rádio: XBee SX 900 MHz, **NETID 1038**, modo burst (sem broadcast).
- O **container** transmite sua telemetria a **1 Hz** e **retransmite** a do payload
  (que chega a 4 Hz). Ou seja, a GCS recebe dois tipos de pacote intercalados na mesma serial.
- A LaunchPad é só uma ponte UART↔USB: a GCS deve receber **as linhas ASCII exatamente
  no formato da competição** (seção 3). O formato posicional antigo de 19 campos (README
  raiz) está **descontinuado**.

## 3. Protocolo — fonte única da verdade

Implementado em [`src/gcs/protocol/`](src/gcs/protocol/). Se o formato mudar, mude **lá** e
nos testes; nenhum outro módulo deve conhecer índices de campos.

Pacotes: ASCII, campos separados por vírgula, uma linha por pacote, `TEAM_ID = 1038`.

### 3.1 Container — `PACKET_TYPE = C` (16 campos)

| # | Campo | Tipo | Observação |
|---|-------|------|------------|
| 0 | TEAM_ID | int | 1038 |
| 1 | MISSION_TIME | str | UTC `hh:mm:ss.ss` |
| 2 | PACKET_COUNT | int | cumulativo C+T, sobrevive a reset |
| 3 | PACKET_TYPE | str | `C` |
| 4 | MODE | str | `F` voo / `S` simulação |
| 5 | TP_RELEASED | str | `N` / `R` |
| 6 | ALTITUDE | float | m, relativo à base de lançamento, res. 0.1 |
| 7 | TEMP | float | °C, res. 0.1 |
| 8 | VOLTAGE | float | V, res. 0.01 |
| 9 | GPS_TIME | str | UTC `hh:mm:ss` |
| 10 | GPS_LATITUDE | float | graus decimais, res. 0.0001 |
| 11 | GPS_LONGITUDE | float | graus decimais, res. 0.0001 |
| 12 | GPS_ALTITUDE | float | m acima do nível do mar, res. 0.1 |
| 13 | GPS_SATS | int | |
| 14 | SOFTWARE_STATE | str | ex.: `LAUNCH_WAIT`, `ASCENT`, `ROCKET_SEPARATION`, `PC2_RELEASE`, `TP_RELEASE`, `LANDED` |
| 15 | CMD_ECHO | str | último comando recebido, sem vírgulas (ex.: `CXON`) |

### 3.2 Tethered Payload — `PACKET_TYPE = T` (18 campos)

| # | Campo | Tipo | Observação |
|---|-------|------|------------|
| 0–3 | TEAM_ID, MISSION_TIME, PACKET_COUNT, PACKET_TYPE | | igual ao container, tipo `T` |
| 4 | TP_ALTITUDE | float | m |
| 5 | TP_TEMP | float | °C |
| 6 | TP_VOLTAGE | float | V |
| 7–9 | GYRO_R, GYRO_P, GYRO_Y | float | °/s |
| 10–12 | ACCEL_R, ACCEL_P, ACCEL_Y | float | |
| 13–15 | MAG_R, MAG_P, MAG_Y | float | gauss |
| 16 | POINTING_ERROR | float | graus, 0 = Sul |
| 17 | TP_SOFTWARE_STATE | str | ex.: `STANDBY`, `RELEASED`, `ACQUIRING_TARGET`, `TARGET_POINTING` |

> O PDR (slide 100) lista `ACCEL_P` duas vezes por erro de digitação; o correto é
> `ACCEL_R, ACCEL_P, ACCEL_Y` (confirmado pelos cabeçalhos em `GUI_2022/datasets/`).

Pacote `X` (custom) é opcional e hoje não é usado: a GCS deve registrá-lo no log e ignorar.

### 3.3 Comandos GCS → CanSat

Formato: `CMD,1038,<NOME>,<DADO>` + `\n`.

| Nome | Dado | Exemplo | Efeito |
|------|------|---------|--------|
| CX | `ON` / `OFF` | `CMD,1038,CX,ON` | liga/desliga telemetria do container |
| ST | `hh:mm:ss` ou `GPS` | `CMD,1038,ST,13:35:59` | ajusta hora da missão (UTC) |
| SIM | `ENABLE` / `ACTIVATE` / `DISABLE` | `CMD,1038,SIM,ENABLE` | modo simulação |
| SIMP | pressão em Pa (int) | `CMD,1038,SIMP,101325` | pressão simulada |

> `ST,GPS` vem do Mission Guide 2022 (não aparece no PDR) — confirmar antes de usar em voo.

### 3.4 Modo simulação

- Ativa só com **ENABLE seguido de ACTIVATE**. `DISABLE` desliga.
- Com ele ativo, a GCS lê o perfil de pressão fornecido pela competição e envia um
  `SIMP` por segundo (1 Hz). O CanSat usa essa pressão no lugar do barômetro para calcular
  a altitude; os demais sensores continuam reais.
- Arquivo de perfil (formato do Mission Guide, confirmar): linhas `CMD,$,SIMP,<Pa>`, onde
  `$` é substituído pelo TEAM_ID; linhas iniciadas por `#` e linhas vazias são ignoradas.

## 4. Requisitos da GCS (PDR slides 139–144)

- **CSV de saída**: `Flight_1038_C.csv` (pacotes C) e `Flight_1038_T.csv` (pacotes T), com
  cabeçalho igual às tabelas acima. Gravar **linha a linha, conforme chega** (flush), para
  não perder dados em travamento. Entregues aos juízes via pendrive.
- **Tela** deve conter: START, STOP and Save, SIMULATION ENABLE, SIMULATION ACTIVATE,
  MQTT ENABLE/DISABLE, Mission Time, GPS Time, Packets Received, terminal de log e
  8 gráficos: temperatura (C×T), altitude (C×T), tensão (C×T), GPS lat/lon do container,
  altitude GPS, giroscópio RPY, acelerômetro RPY, magnetômetro RPY. Ver o mock em
  PDR slide 143 / `README.md` raiz.
- **MQTT**: paho-mqtt, publica cada linha recebida, sem alteração. Tópico **`teams/1038`**
  (o PDR dizia `topic/1038`; a equipe decidiu por `teams/1038`). Broker, porta, tópico,
  usuário e senha vêm de variáveis de ambiente — ver seção 5, camada mqtt.
- Laptop roda em bateria por > 2 h; sem atualizações automáticas durante o voo.
- Deve rodar em **Windows e Linux** (o código antigo só rodava na máquina de um membro).

## 5. Arquitetura V2

```
V2/
├── context.md            ← este arquivo
├── PLANEJAMENTO.md       ← fases, tarefas e status
├── pyproject.toml
├── src/gcs/
│   ├── __main__.py       ← `python -m gcs` (composition root)
│   ├── config.py         ← porta, baud, team id, caminhos, MQTT (sem caminho absoluto fixo)
│   ├── protocol/         ← parsing de telemetria + montagem de comandos (puro, sem I/O)
│   ├── transport/        ← fontes de linhas: serial real, replay de CSV, simulador fake
│   ├── core/             ← TelemetryStore, MissionController, SimulationRunner
│   ├── persistence/      ← escrita dos CSV de voo
│   ├── mqtt/             ← publisher MQTT
│   └── ui/               ← PySide6 + pyqtgraph (única camada que importa Qt)
├── tests/
└── tools/                ← fake_cansat.py (substitui o .ino de teste), scripts utilitários
```

### Camada transport (pronta)

- Toda fonte herda `LineSource` (`transport/base.py`): `start()`, `stop()`, `running`,
  `can_send`, `send(line)`. Roda numa thread daemon e coloca na `queue.Queue` apenas
  `LineReceived(text, source, timestamp)` e `SourceStatus(state, source, message)`.
  `STOPPED` é sempre o último evento.
- `SerialLineSource`: porta via `serial.serial_for_url` (`COM5`, `/dev/ttyACM0`,
  `socket://localhost:7777`, `loop://`). Reconecta sozinha; `send()` lança
  `ConnectionError` se desconectada.
- `ReplayLineSource`: reproduz CSVs gravados; `send()` lança `CommandNotSupported`.
- `FakeLineSource` / `FakeCanSat`: simulador que obedece aos comandos. Sem telemetria até
  receber `CX,ON` (igual ao FSW). `tools/fake_cansat.py --tcp 7777` expõe por TCP.
- Monitor de console (sem janela): `python -m gcs monitor --fake --cx-on` (ver `cli_monitor.py`).

### Camada core (pronta)

- `MissionController` é o único ponto de contato da UI com o resto:
  - `start_session(lambda q: SerialLineSource(q, porta))` → START; `stop_session()` → STOP and Save.
  - `poll()` a cada ~100 ms na thread principal (QTimer). É ele que avança a simulação.
  - `send_command(linha) -> bool`, `set_telemetry(on)`, `set_time("hh:mm:ss"|"GPS")`.
  - `simulation` (`SimulationRunner`): `load_file()`, `enable()`, `activate()`, `disable()`,
    `state`, `progress`, `confirmed`.
  - `source_state` / `source_message` para o indicador de conexão.
- `TelemetryStore` (`controller.store`): `last_container`, `last_payload`, `stats`
  (`received`, `invalid`, `lost`...), `series("C"|"T", campo)` e `version` (redesenhar só
  quando mudar).
- Novos consumidores de pacotes (CSV, MQTT) implementam `PacketSink` e são passados em
  `MissionController(store, sinks=[...])`. Exceção num sink é logada e ignorada.

### Camada persistence (pronta)

- `CsvFlightWriter(output_dir)` é um `PacketSink`. Cada sessão cria
  `output_dir/<YYYYmmdd_HHMMSS>/Flight_1038_C.csv` e `Flight_1038_T.csv` (nomes oficiais),
  grava `packet.raw` + flush por linha. `paths` / `session_dir` apontam a última sessão.
- `copy_to(pasta)` (após STOP) copia os dois CSVs para o pendrive — usar no botão "Save" da UI.
- Não reformatar valores ao gravar: o CSV deve conter exatamente o que o CanSat transmitiu.

### Camada mqtt (pronta)

- Configuração **somente** por variáveis de ambiente (nunca no código nem em arquivo versionado):

  | Variável | Padrão | |
  |----------|--------|--|
  | `GCS_MQTT_HOST` | — | obrigatória para ligar o MQTT |
  | `GCS_MQTT_PORT` | `1883` | |
  | `GCS_MQTT_TOPIC` | `teams/1038` | |
  | `GCS_MQTT_USER` | — | opcional |
  | `GCS_MQTT_PASSWORD` | — | opcional; nunca logar |

  `Config.from_env()` lê; `load_dotenv()` carrega um `.env` local (ignorado pelo git; modelo
  em `.env.example`). Variáveis do shell têm prioridade sobre o `.env`.
- `MqttPublisher(cfg.mqtt)` é um `PacketSink`. `enable()` / `disable()` = botões MQTT ENABLE /
  DISABLE; independe de START/STOP. `enable()` retorna False e preenche `last_error` se
  `GCS_MQTT_HOST` estiver vazio. Para a UI: `enabled`, `connected`, `published`, `dropped`.
- Pacotes recebidos com o broker fora do ar são descartados (contados em `dropped`), nunca
  enfileirados — o CSV local é o registro oficial.

### Camada ui (pronta)

- `ui/app.py`: `build_window(cfg)` monta tudo (store, `CsvFlightWriter`, `MqttPublisher`,
  `MissionController`, janela); `run(cfg)` cria o `QApplication` e abre a janela.
- `ui/main_window.py`: `MainWindow` **não tem lógica de missão** — só chama controller/writer/
  publisher. Um `QTimer` (`cfg.ui_refresh_ms`) faz `controller.poll()`, drena o terminal,
  redesenha gráficos (máx. 5×/s, só se `store.version` mudou) e atualiza indicadores e o
  estado habilitado dos botões em `_refresh()`.
- `ui/plots.py`: os 8 gráficos são declarados em `PLOTS` (lista de `PlotSpec`/`Curve` com
  tipo de pacote + campo). Para adicionar/alterar um gráfico, edite só essa lista.
  O gráfico GPS (lon × lat) é especial: só pontos, sem `clipToView` (x não é monótono).
- `ui/log_console.py`: `QueueLogHandler` no logger raiz (qualquer thread) → `LogConsole`.
- Diálogos (`QMessageBox`, `QFileDialog`) só em ações do operador, nunca no timer.
- Teste: `tests/test_ui.py` roda com `QT_QPA_PLATFORM=offscreen`. Para capturar a tela sem
  monitor no Windows, defina também `QT_QPA_FONTDIR=C:/Windows/Fonts` (senão o texto vira quadrados).
- Fluxo do operador: escolher fonte → START → CX ON → (simulação: carregar perfil →
  ENABLE → ACTIVATE) → STOP and Save → Copiar CSVs para pendrive.

### Regras de dependência

```
ui ──► core ──► protocol
        │ ──► transport, persistence, mqtt ──► protocol
```

- `protocol` não importa nada do projeto e não faz I/O.
- `core` não importa `ui`. Nenhuma camada além de `ui` importa Tk/Qt/matplotlib.
- Só `__main__.py` instancia e conecta as peças (injeção de dependência manual).

### Fluxo de dados (threads)

```
[thread leitora serial] --linha--> queue.Queue --> [thread principal / UI]
                                                     ├─ parse (protocol)
                                                     ├─ TelemetryStore (deque limitado p/ gráficos)
                                                     ├─ CsvFlightWriter (append + flush)
                                                     └─ MqttPublisher (não bloqueante)
UI drena a fila a cada ~100 ms via QTimer; nunca bloqueia esperando a serial.
```

- Qt **só** é tocado na thread principal (nada de sinais Qt nas threads de transport;
  a ponte é a `queue.Queue`).
- A thread serial só lê linhas e enfileira; não faz parsing nem I/O de disco.
- Linha inválida → registra no terminal/log e segue. Nunca derruba a aplicação.

## 6. Convenções

- Python **≥ 3.10**, type hints em tudo, `dataclasses` (frozen) para pacotes.
- Código e identificadores em **inglês**; UI, logs e docs podem ser em português.
- Nomes de campos de telemetria = nomes da competição (`GPS_LATITUDE` → `gps_latitude`).
- `logging` da stdlib, nunca `print`. Nunca `except:` vazio.
- Sem caminhos absolutos; caminhos via `config.py` / `pathlib`.
- Testes com `pytest` em `tests/`; todo parser e montador de comando tem teste.
- Formatação/lint: `ruff`.
- Credenciais e endereços externos só por variáveis de ambiente `GCS_*` (ou `.env` local).
- Ambiente: `python -m venv .venv` e `.venv\Scripts\pip install -e ".[dev]"` dentro de `V2/`
  (venv em caminho curto: o PySide6 falha com caminhos longos no Windows sem Long Paths).
- Rodar: `python -m gcs` (interface), `python -m gcs monitor --help` (console), `pytest`.

## 7. Armadilhas conhecidas do código antigo (não repetir)

- Import circular `main.py` ↔ `tela.py`; `command=Main.setStart()` chamava a função na
  construção do botão em vez de passar a referência.
- `src/serialCom/index.py` abria a porta serial **no import** (`SerialC().Captura(...)` no fim do arquivo).
- Pipeline de ~20 CSVs intermediários (um por sensor) gravados e relidos a cada 8–10 s.
- Bugs de copiar/colar: GPS altura gravado no arquivo de longitude, `MAG_P` recebendo
  acelerômetro, `GPS_LATITUDE` recebendo altitude, `clear()` esquecendo listas.
- `len(x) > 1 & stop != True` (precedência de `&`), `flushInput()` antes de `readline()`
  (descartava dados), listas como argumento default mutável, `except:` engolindo erros.
- Tkinter criado fora da thread principal; `Process` criado e nunca iniciado.
- Baud/porta fixos (`/dev/ttyACM0`, 9600); `requirements.txt` com pacotes inúteis (`tk==0.1.0`, opencv).

## 8. Referências

- PDR da equipe (CanSat 2022 PDR, Team #1038 — LtSat), seções CDH (slides 85–102) e GCS (137–144).
- CanSat Mission Guide 2022: https://www.cansatcompetition.com/docs/CanSat_Mission_Guide_2022.pdf
- Cabeçalhos oficiais dos CSV: `GUI_2022/datasets/flight_1038_C.csv` e `flight_1038_T.csv`.
