import argparse
import subprocess
import platform
import ipaddress
import re


def ping(host, size):
    system = platform.system()
    if system == 'Darwin':
        cmd = f'ping {host} -c 1 -D -s {size} -W 2000'
    elif system == 'Windows':
        cmd = f'ping {host} -f -n 1 -l {size} -w 2000'
    else:
        cmd = f'ping {host} -M do -c 1 -s {size} -W 2'
    return subprocess.run(cmd, shell=True).returncode


parser = argparse.ArgumentParser()
parser.add_argument('--host', required=True)

args = parser.parse_args()
address = args.host

pattern = re.compile(
    r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
    r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
    r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\.'
    r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$'
)

if not pattern.match(address):
    try:
        ipaddress.ip_address(address)
    except ValueError:
        print("\nincorrect host\ncheck for errors")
        exit(0)

left = 0
right = 1500

while left + 1 < right:
    med = int((left + right) / 2)
    result = ping(address, med)
    if result == 0:
        left = med
    elif result == 1:
        right = med
    elif result == 68:
        print(f'\nunresolvable host')
        exit(0)
    else:
        print(f'\nerror {result}\nhost is not reachable'
              f'\ncheck if host is allowed to receive icmp')
        exit(0)

print(f'\nMTU for {address} is {left + 28}')
