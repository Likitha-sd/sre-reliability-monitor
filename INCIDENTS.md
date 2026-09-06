# Incident Testing

## Incident 1 — Service Unavailable

### Detection
TCP health check failed with:
`[Errno 111] Connection refused`

HTTP health check also failed.

### Diagnosis
The HTTP server was stopped, so nothing was listening on port 8000.

### Recovery
Restarted the HTTP server.

### Monitor Behavior
- Retried TCP connection 3 times
- Retried HTTP request 3 times
- Generated an alert
- Detected recovery when the service returned

---

## Incident 2 — HTTP Endpoint Failure

### Detection
TCP remained UP, but HTTP health check returned:
`HTTP Error 404: Not Found`

### Diagnosis
The server was reachable, but the requested `/health` endpoint was changed to an invalid path.

### Recovery
Restored the correct `/health` endpoint.

### Monitor Behavior
- TCP remained UP
- HTTP changed to DOWN
- Generated an HTTP alert
- Detected recovery after restoring the endpoint

---

## Incident 3 — High Latency

### Detection
HTTP request succeeded, but latency increased to approximately 2 seconds.

Configured latency threshold:
`1 second`

### Diagnosis
The health endpoint was intentionally delayed by 2 seconds.

### Recovery
Removed the artificial delay.

### Monitor Behavior
- TCP remained UP
- HTTP remained UP
- High latency generated a WARNING
