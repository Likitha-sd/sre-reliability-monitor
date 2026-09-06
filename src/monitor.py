import psutil
import logging
import socket
import urllib.request
import time
from urllib.error import HTTPError, URLError
import json

with open("config.json", "r") as file:
    config = json.load(file)

tcp_previous_state = None

tcp_previous_state = None
http_previous_state = None

TCP_RETRIES = config["retry"]["attempts"]
RETRY_DELAY = config["retry"]["delay"]
RETRY_TIMEOUT = config["retry"]["timeout"]

logging.basicConfig(
    filename="logs/monitor.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def alert(message):
    print(f"ALERT: {message}")
    logging.error(f"ALERT: {message}")

def check_cpu():
    cpu = psutil.cpu_percent(interval=1)

    if cpu >= config["thresholds"]["cpu"]:
        status = "WARNING"
        print(f"WARNING: High CPU usage: {cpu}%")
        logging.warning(f"High CPU usage: {cpu}%")
    else:
        status = "OK"
        print(f"OK: CPU usage: {cpu}%")
        logging.info(f"OK: CPU usage: {cpu}%")

    return {
        "check": "cpu",
        "status": status,
        "value": cpu
    }

def check_memory():
    memory = psutil.virtual_memory().percent

    if memory >= config["thresholds"]["memory"]:
        status = "WARNING"
        print(f"WARNING: High memory usage: {memory}%")
        logging.warning(f"High memory usage: {memory}%")
    else:
        status = "OK"
        print(f"OK: Memory usage: {memory}%")
        logging.info(f"OK: Memory usage: {memory}%")

    return {
        "check": "memory",
        "status": status,
        "value": memory
    }

def check_disk():
    disk = psutil.disk_usage("/").percent

    if disk >= config["thresholds"]["disk"]:
        status = "WARNING"
        print(f"WARNING: High disk usage: {disk}%")
        logging.warning(f"High disk usage: {disk}%")
    else:
        status = "OK"
        print(f"OK: Disk usage: {disk}%")
        logging.info(f"OK: Disk usage: {disk}%")

    return {
        "check": "disk",
        "status": status,
        "value": disk
    }

def check_process(process_name):
    for process in psutil.process_iter(["name"]):
        if process.info["name"] == process_name:
            print(f"OK: Process {process_name} is running")
            logging.info(f"Process {process_name} is running")

            return {
                "check": "process",
                "status": "OK",
                "process": process_name
            }

    message = f"Process {process_name} is not running"
    print(f"WARNING: {message}")
    logging.warning(message)

    return {
        "status": "WARNING",
        "process": process_name
    }


def check_tcp(host, port):
    global tcp_previous_state

    last_error = None

    for attempt in range(1, TCP_RETRIES + 1):
        try:
            with socket.create_connection((host, port), timeout=RETRY_TIMEOUT):
                current_state = "UP"

                if tcp_previous_state == "DOWN":
                    print(f"RECOVERY: TCP connection to {host}:{port} is back")
                    logging.info(f"RECOVERY: TCP connection to {host}:{port} is back")
                else:
                    print(f"OK: TCP connection to {host}:{port}")

                tcp_previous_state = current_state

                return {
                    "check": "tcp",
                    "status": "UP",
                    "host": host,
                    "port": port
                }

        except (socket.timeout, OSError) as error:
            last_error = error

            if attempt < TCP_RETRIES:
                print(f"TCP attempt {attempt} failed, retrying...")
                time.sleep(RETRY_DELAY)

    message = (
        f"Cannot connect to {host}:{port} "
        f"after {TCP_RETRIES} attempts - {last_error}"
    )

    if tcp_previous_state != "DOWN":
        alert(message)

    tcp_previous_state = "DOWN"

    return {
        "check": "tcp",
        "status": "DOWN",
        "host": host,
        "port": port,
        "error": str(last_error)
    }


import urllib.request
import time
def check_http(url):
    global http_previous_state

    last_error = None

    for attempt in range(1, TCP_RETRIES + 1):
        try:
            start = time.time()

            with urllib.request.urlopen(url, timeout=RETRY_TIMEOUT) as response:
                latency = time.time() - start

                if response.status == 200:
                    if http_previous_state == "DOWN":
                        print(f"RECOVERY: HTTP service {url} is back")
                        logging.info(f"RECOVERY: HTTP service {url} is back")
                    elif latency >= config["thresholds"]["latency"]:
                        print(f"WARNING: High latency: {latency:.3f}s")
                        logging.warning(
                            f"High HTTP latency: {latency:.3f}s"
                        )
                    else:
                        print(
                            f"OK: HTTP health check {url}, "
                            f"latency={latency:.3f}s"
                        )

                    http_previous_state = "UP"

                    return {
                        "check": "http",
                        "status": "UP",
                        "url": url,
                        "latency": latency
                    }

        except (HTTPError, URLError) as error:
            last_error = error

            if attempt < TCP_RETRIES:
                print(f"HTTP attempt {attempt} failed, retrying...")
                time.sleep(RETRY_DELAY)

    message = (
        f"HTTP request failed after "
        f"{TCP_RETRIES} attempts - {last_error}"
    )

    if http_previous_state != "DOWN":
        alert(message)

    http_previous_state = "DOWN"

    return {
        "check": "http",
        "status": "DOWN",
        "url": url,
        "error": str(last_error)
    }

def main():
    try:
        while True:
            print("\n--- Monitoring cycle ---")

            results = []

            results.append(check_cpu())
            results.append(check_memory())
            results.append(check_disk())
            results.append(check_process("bash"))

            results.append(
                check_tcp(
                    config["tcp"]["host"],
                    config["tcp"]["port"]
                )
            )

            results.append(
                check_http(
                    config["http"]["url"]
                )
            )

            print("\nCycle summary:")

            for result in results:
                print(result)

            time.sleep(config["monitor"]["interval"])

    except KeyboardInterrupt:
        print("\nMonitoring stopped safely.")
        logging.info("Monitoring stopped by user.")


if __name__ == "__main__":
    main()


