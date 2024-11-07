import concurrent.futures
import subprocess

# Function to ping a host
def ping_host(host):
    result = subprocess.run(['ping', '-c', '3', host], stdout=subprocess.PIPE)
    return f"{host} is reachable" if result.returncode == 0 else f"{host} is unreachable"

# List of hosts to check
hosts = ["google.com", "github.com", "localhost"]

# Run checks in parallel
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(ping_host, hosts)

for result in results:
    print(result)
