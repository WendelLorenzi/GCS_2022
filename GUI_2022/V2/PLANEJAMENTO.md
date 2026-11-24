# Planejamento da reestruturação — LtSat GCS V2

Contexto completo do projeto: [context.md](context.md).

## 1. Diagnóstico do código atual

| Área | Problema | Impacto |
|------|----------|---------|
| Arquitetura | Import circular `main.py` ↔ `tela.py`; lógica, UI e I/O misturados | App não inicia |
| Serial | Porta aberta no import do módulo; `flushInput()` antes de cada `readline()` | Perda de pacotes; efeitos colaterais ao importar |
| Protocolo | Formato posicional próprio de 19 campos, tipos `c`/`t` minúsculos; pacote `t` regrava campos do container | Diverge do formato oficial exigido pelos juízes |
| Dados | ~20 CSVs intermediários gravados/relidos a cada 8–10 s; `unifyData` nunca salva nada | Lento, frágil, CSV final nunca é gerado |
| Bugs pontuais | Campos trocados (GPS altura → arquivo de longitude, `MAG_P` = acelerômetro, `GPS_LATITUDE` = altitude); precedência de `&`; `Process` nunca iniciado; métodos sem `self` | Dados errados entregues |
| Portabilidade | Caminhos absolutos `/home/wendel/...`, `/dev/ttyACM0`, baud 9600 fixos | Só roda em uma máquina Linux |
| UI | `command=f()` em vez de `command=f`; Tk em thread secundária; gráficos comentados | Botões não funcionam; sem visualização |
| Funcionalidades | Sem envio de comandos, sem modo simulação, sem MQTT | Requisitos do PDR não atendidos |
| Qualidade | `except:` vazio, `print` como log, zero testes, `requirements.txt` com lixo | Falhas silenciosas |

Conclusão: não há o que aproveitar além do layout visual da tela e dos cabeçalhos CSV.
Reescrever do zero em `V2/`.

## 2. Objetivos da V2

1. Seguir o protocolo oficial da competição (seção 3 do `context.md`) como fonte única.
2. Nunca perder um pacote: leitura contínua, gravação imediata em CSV.
3. Rodar em Windows e Linux sem editar código (config por arquivo/CLI).
4. Testável sem hardware: fonte de dados fake e replay de CSV.
5. Camadas separadas para que a UI possa ser trocada sem tocar no resto.

## 3. Decisões

| # | Decisão | Escolha | Motivo |
|---|---------|---------|--------|
| D1 | Toolkit de UI | **PySide6 + pyqtgraph** (decidido) | pyqtgraph redesenha 8 gráficos a 10 Hz sem engasgar; matplotlib no Tk fica pesado. Diverge do PDR (Tkinter) — citar a mudança no CDR |
| D6 | Teste sem hardware | Simulador `FakeCanSat` (in-process, TCP ou porta serial) | Exercita o caminho serial real (`socket://`) sem drivers de porta virtual |
| D2 | Pandas | Removido | Só precisamos de append de linhas; `csv` da stdlib basta |
| D3 | Concorrência | 1 thread leitora + `queue.Queue` + timer na UI | Simples, sem `multiprocessing` |
| D4 | Formato de entrada | Linhas ASCII oficiais (C/T), repassadas pela LaunchPad | A GCS grava exatamente o que o CanSat envia |
| D5 | Empacotamento | `pyproject.toml` + layout `src/` | `pip install -e .` e `python -m gcs` em qualquer SO |

## 4. Fases

Status: ☐ a fazer · ◐ em andamento · ☑ feito

### Fase 0 — Base ☑
- ☑ Estrutura de pastas e `pyproject.toml`
- ☑ `context.md` para agentes de IA
- ☑ `protocol/telemetry.py`: dataclasses `ContainerPacket` / `PayloadPacket`, `parse_line()`
- ☑ `protocol/commands.py`: montadores `cx()`, `st()`, `sim()`, `simp()`
- ☑ Testes do protocolo

### Fase 1 — Fontes de dados (transport) ☑
- ☑ `LineSource` base + eventos `LineReceived` / `SourceStatus` + `LineAssembler` (framing)
- ☑ `SerialLineSource` (pyserial `serial_for_url`, thread daemon, reconexão automática, `send()` thread-safe)
- ☑ `ReplayLineSource` (CSVs C+T mesclados por PACKET_COUNT, ritmo do MISSION_TIME, `speed`)
- ☑ `FakeCanSat` + `FakeLineSource`: máquina de estados do FSW, C a 1 Hz, T a 4 Hz após
  liberação, responde a CX/ST/SIM/SIMP (substitui `tst_Groud_Station.ino`)
- ☑ `tools/fake_cansat.py`: expõe o simulador via `--tcp`, `--port` ou `--stdout`
- ☑ `list_serial_ports()`
- ☑ `python -m gcs`: monitor de console provisório (`--port`, `--fake`, `--replay`, `--cx-on`)
- ☑ Testes (loopback `loop://`, reconexão, replay, voo completo do fake, modo simulação)
  e teste ponta a ponta manual: fake via TCP → monitor, voo completo sem erros
- Pendente para validar com hardware: baud real da LaunchPad e terminador de linha do firmware

### Fase 2 — Núcleo (core) ☑
- ☑ `TelemetryStore`: últimos N pacotes por tipo (`deque`), último C/T, `LinkStats`
  (recebidos C/T, inválidos, perdidos por lacuna no PACKET_COUNT, resets), `series()` para
  gráficos (x = s desde o 1º pacote, trata virada da meia-noite; ausente = NaN), `version`
- ☑ `MissionController`: `start_session(factory)` / `stop_session()` (para a fonte, **drena a
  fila** e fecha sinks), `poll()` limitado chamado da thread principal, `send_command()`,
  `set_telemetry()`, `set_time()`; protocolo `PacketSink` (`open_session` / `on_packet` /
  `close_session`) para CSV e MQTT; sink com erro não derruba a recepção
- ☑ `SimulationRunner`: perfil `CMD,$,SIMP,<Pa>` ou números; exige ENABLE→ACTIVATE e perfil;
  1 SIMP/s sem rajadas após travamentos; reenvia em falha; `confirmed` quando a telemetria
  volta com MODE=S; `halt()` ao encerrar sessão
- ☑ `tools/sim_profile_example.txt` (perfil de teste, não oficial)
- ☑ Monitor de console usa o controller (`--sim PERFIL`)
- ☑ Testes (19 novos) + voo simulado completo com o fake: 379 pacotes, 0 inválidos, 0 perdidos

### Fase 3 — Persistência ☑
- ☑ `CsvFlightWriter` (`PacketSink`): `Flight_1038_C.csv` / `Flight_1038_T.csv` com cabeçalho
  oficial, grava `packet.raw` exatamente como recebido, flush por linha
- ☑ Pasta por sessão `flights/<YYYYmmdd_HHMMSS>/` (sufixo `_2`, `_3`... se repetir); nunca sobrescreve
- ☑ `copy_to(destino)` para levar os arquivos ao pendrive dos juízes (recusa sobrescrever sem `overwrite=True`)
- ☑ Monitor de console grava por padrão (`--out`, `--no-record`); replay não grava
- ☑ Testes: cabeçalho igual ao modelo da competição (`GUI_2022/datasets`), não sobrescrita,
  cópia, ida e volta voo fake → CSV → replay; teste manual com processo morto no meio do voo
  (dados íntegros até o último pacote)
- Decisão: sem `fsync` por linha (flush basta para travamento do programa; queda de energia
  do laptop é mitigada pela bateria). Reavaliar se necessário

### Fase 4 — MQTT ☑
- ☑ `MqttPublisher` (`PacketSink`): paho-mqtt v2, thread de rede própria (`loop_start`),
  reconexão automática, publish não bloqueante da linha bruta (QoS 0), liga/desliga em runtime
  independente da sessão, contadores `published` / `dropped`, `connected`, `last_error`
- ☑ Configuração por variáveis de ambiente (`GCS_MQTT_HOST/PORT/TOPIC/USER/PASSWORD`),
  tópico padrão `teams/1038`, porta padrão 1883; senha nunca aparece em `repr`/log
- ☑ `.env` opcional (`load_dotenv`, sem dependência extra; shell tem prioridade),
  `.env.example` versionado, `.env` no `.gitignore`
- ☑ Monitor de console: `--mqtt`
- ☑ Testes com cliente falso (9) + teste manual com broker local (amqtt, só no venv de teste):
  40/40 mensagens recebidas em `teams/1038`, idênticas à telemetria
- Pendente: validar usuário/senha contra o broker real da competição (o broker local de
  teste aceitava conexão anônima)

### Fase 5 — Interface ☑ (PySide6 + pyqtgraph)
- ☑ Janela no layout do PDR (slide 143): controles à esquerda, 8 gráficos 4×2, terminal embaixo; tema escuro
- ☑ Fonte de dados: Serial (porta + ↻ + baud, aceita `socket://`), Replay de CSV (velocidade), CanSat simulado (aceleração);
  "Gravar CSV" desliga sozinho no replay
- ☑ START / STOP and Save / Copiar CSVs para pendrive; pasta da sessão exibida (caminho completo no tooltip)
- ☑ Indicadores: conexão, Mission Time, GPS Time, Packets Received (C/T), inválidos/perdidos,
  estados C/T, modo, payload liberado, satélites, pointing error, CMD_ECHO, último comando
- ☑ Comandos: CX ON/OFF, ST (campo hh:mm:ss, "UTC agora", "GPS")
- ☑ Simulação: carregar perfil, SIMULATION ENABLE → ACTIVATE → SIM DISABLE, progresso e confirmação MODE=S
- ☑ MQTT ENABLE/DISABLE com destino, conexão, enviados e descartados
- ☑ Botões habilitados conforme o estado (sem comando sem link, sem ACTIVATE antes de ENABLE...)
- ☑ Fechar a janela com sessão ativa pede confirmação e faz STOP and Save
- ☑ Terminal colorido por nível, alimentado pelo `logging` de todas as threads
- ☑ Gráficos redesenham no máx. 5×/s e só quando chega dado novo; janela de 1200 pacotes por tipo
- ☑ `python -m gcs` / `ltsat-gcs` abre a UI; monitor de console virou `python -m gcs monitor ...`
- ☑ Teste de fumaça da UI sem tela (`offscreen`) clicando nos botões reais + revisão visual por captura de tela
- Diferença em relação ao PDR: SIMULATION ENABLE/ACTIVATE são enviados **depois** do START
  (precisam do link aberto para chegar ao CanSat). Citar no CDR

### Fase 6 — Integração e ensaio ☐
- ☐ Teste ponta a ponta com `fake_cansat.py`
- ☐ Teste com LaunchPad + XBee reais
- ☐ Ensaio do modo simulação com perfil oficial
- ☐ Teste de 2 h contínuas (memória estável, nenhum pacote perdido)
- ☐ Checklist de dia de voo (README de operação)

## 5. Critérios de pronto

- `pytest` verde; `ruff check` limpo.
- Replay de um voo gravado (interface: fonte "Replay de CSV") mostra todos os gráficos sem hardware.
- Contador da GCS bate com `PACKET_COUNT` do CanSat (diferença = perda real de rádio).
- CSVs gerados abrem com os cabeçalhos oficiais e um pacote por linha.
- Roda em Windows e Linux com o mesmo código.

## 6. Próximo passo

**Fase 6** — integração com o hardware real (LaunchPad + XBee), ensaio do modo simulação
com o perfil oficial, teste de 2 h contínuas e checklist do dia de voo.
