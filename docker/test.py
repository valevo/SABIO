import requests
import json

import argparse

parser = argparse.ArgumentParser(
                    prog='SABIO Flask app test',
                    description='Automates checking whether the app loads correctly and all defined routes run without errors.',
                    epilog='Gunicorn is set to run at 0.0.0.0, default port is 8080 (but can be passed as argument to the ./start.sh script).')

parser.add_argument('-o', '--host', default="0.0.0.0", type=str)
parser.add_argument('-p', '--port', default="8080", type=str)
parser.add_argument('-a', '--app_running', action='store_true')
parser.add_argument('-v', '--verbose',action='store_true')

args = parser.parse_args()

prefix="http://"
host = args.host
port = f"{args.port}"

if not args.app_running:
    import subprocess
    subprocess.call(['sh', './start.sh', '&'])


# testing all routes routes defined in ./src/app.py
res = requests.get(f"{prefix}{host}:{port}/examples")

print(f"/examples: {res.status_code}")
if args.verbose:
    print(f'{res.headers["Content-Type"]=}')
    print(f'{json.loads(res.text)}')



print()
res = requests.get(f"{prefix}{host}:{port}/datasets")

print(f"/datasets: {res.status_code}")
if args.verbose:
    print(f'{res.headers["Content-Type"]=}')
    print(f'{json.loads(res.text)}')



print()
res = requests.get(f"{prefix}{host}:{port}/engines")

print(f"/engines: {res.status_code}")
if args.verbose:
    print(f'{res.headers["Content-Type"]=}')
    print(f'{json.loads(res.text)}')



print()
res = requests.get(f"{prefix}{host}:{port}/datasets")

print(f"/datasets: {res.status_code}")
if args.verbose:
    print(f'{res.headers["Content-Type"]=}')
    print(f'{json.loads(res.text)}')




print()
res = requests.get(f"{prefix}{host}:{port}/datasets/NMvW_v0/autocomplete", 
			params=dict(param="Geography", keyword=""))

print(f"/datasets/NMvW_v0/autocomplete: {res.status_code}")
if args.verbose:
    print(f'{res.headers["Content-Type"]=}')
    print(f'{json.loads(res.text)}')



print()
res = requests.get(f"{prefix}{host}:{port}/engines/TypicalityEnginev0/html")

print(f"/engines/TypicalityEngine_v0/html: {res.status_code}")
if args.verbose:
    print(f'{res.headers["Content-Type"]=}')
    print(f'{res.text}')



print()
res = requests.get(f"{prefix}{host}:{port}/objects/NMvW_v0/details/847658")

print(f"/objects/NMvW_v0/details/847658: {res.status_code}")
if args.verbose:
    print(f'{res.headers["Content-Type"]=}')
    print(f'{json.loads(res.text)}')




