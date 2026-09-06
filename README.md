# Service & Host Reliability Monitor

A Python-based SRE monitoring tool that continuously checks Linux host health and service availability, detects failures, retries transient failures, logs incidents, and reports recovery.

## Features

- CPU, memory, and disk monitoring
- Process health monitoring
- TCP connectivity checks
- HTTP health checks
- HTTP latency monitoring
- Configurable thresholds and targets
- Retry and timeout handling
- State-based alerts and recovery detection
- Structured monitoring results
- Graceful shutdown
- Automated tests with pytest
- Intentional failure simulation and incident documentation

## Architecture

```text
                 ┌──────────────────────┐
                 │   Reliability        │
                 │      Monitor         │
                 │     monitor.py       │
                 └──────────┬───────────┘
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
        Linux Host       TCP Check     HTTP Check
        ├─ CPU           Port 8000     /health
        ├─ Memory                       └─ Latency
        ├─ Disk
        └─ Process
                            │
                            ▼
                    Logs + Alerts

## Technologies

- Python
- Linux
- Bash
- TCP/IP
- HTTP
- psutil
- pytest
- JSON configuration
- Python logging

## Project Structure

```text
sre-reliability-monitor/
├── src/
│   ├── monitor.py
│   └── server.py
├── tests/
│   └── test_monitor.py
├── logs/
│   └── monitor.log
├── config.json
├── INCIDENTS.md
├── .gitignore
└── README.md

## Configuration

The monitor is configured through `config.json`.

It controls:

- CPU, memory, disk, and latency thresholds
- TCP host and port
- HTTP health-check URL
- Retry attempts and delay
- Connection timeout
- Monitoring interval

## Running the Project

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Start the test HTTP service:

```bash
python src/server.py
```

In another terminal, activate the environment and start the monitor:

```bash
source .venv/bin/activate
python src/monitor.py
```

The monitor runs continuously until stopped with `Ctrl+C`.

## Testing

Run the automated test suite:

```bash
pytest
```

The test suite validates:

- CPU monitoring
- Memory monitoring
- Disk monitoring
- Process monitoring
- TCP connectivity
- HTTP health checks

## Failure Scenarios

### 1. Service Unavailable

The HTTP server was stopped.

```text
TCP → DOWN
HTTP → DOWN
Connection refused
```

The monitor retried the connection and generated an alert.

### 2. HTTP Endpoint Failure

The monitored endpoint was changed to an invalid path.

```text
TCP → UP
HTTP → DOWN
HTTP 404
```

This demonstrated that network connectivity can remain healthy while an application endpoint fails.

### 3. High Latency

An artificial 2-second delay was introduced while the configured threshold was 1 second.

```text
TCP → UP
HTTP → UP
Latency → ~2 seconds
WARNING → High latency
```

This demonstrated that a service can be available but still degraded.

See `INCIDENTS.md` for the incident-testing record.

## SRE Concepts Demonstrated

- Monitoring
- Health checks
- Timeouts
- Retries
- Alerting
- Recovery detection
- Structured logging
- Failure detection
- Incident investigation
- Performance degradation detection
- Automated testing

## Future Improvements

- Prometheus metrics
- Grafana dashboards
- Alertmanager integration
- Containerization
- Kubernetes deployment
- Cloud deployment
