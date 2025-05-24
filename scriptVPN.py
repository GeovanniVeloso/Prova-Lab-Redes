#!/usr/bin/python3
# scripVPn.py

import sys
import os
import subprocess
import zipfile

nomeCliente = sys.argv[1]
password = sys.argv[2]
destino = os.path.join("/etc/openvpn/client/", nomeCliente)
ipServidor = ""

try:
    result = subprocess.run(
        ["ip", "-4", "addr", "show", "enp0s3"],
        capture_output=True,
        text=True,
        check=True
    )
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith("inet "):
            ipServidor =  line.split()[1].split("/")[0]  # Pega só o IP
except subprocess.CalledProcessError:
    print("Erro ao obter IP da interface enp0s3")

try:
    subprocess.run(
        ["./easyrsa","--batch", "gen-req", nomeCliente, "nopass"], cwd="/usr/share/easy-rsa/", check=True
    )
except:
    print("Erro ao executar o gen-req")

#try:
#    subprocess.run(
#        ["./easyrsa","--batch", "sign-req", "client", nomeCliente],
#        input=f"\n{password}\n",
#        text=True,
#        check=True,
#        cwd="/usr/share/easy-rsa/"
#    )
#except:
#    print("Erro ao executar o sign-req")

env = os.environ.copy()
env["EASYRSA_PASSIN"] = f"pass:{password}"

try:
    subprocess.run(
        ["./easyrsa", "--batch", "sign-req", "client", nomeCliente],
        check=True,
        cwd="/usr/share/easy-rsa/",
        env=env
    )
except subprocess.CalledProcessError:
    print("Erro ao executar o sign-req")

try:
    subprocess.run(
        ["mkdir", os.path.join("/etc/openvpn/client/", nomeCliente)], check=True
    )
except:
    print("Erro ao executar o mkdir")

try:
    subprocess.run(
        [
            "cp",
            "/usr/share/easy-rsa/pki/ca.crt",
            os.path.join("/etc/openvpn/client/", nomeCliente),
        ],
        check=True,
    )
except:
    print("Erro ao executar o cp ca.crt")

try:
    subprocess.run(
        [
            "cp",
            os.path.join("/usr/share/easy-rsa/pki/issued/", f"{nomeCliente}.crt"),
            destino
        ],
        check=True,
    )
except:
    print("Erro ao executar o cp cliente.crt")

try:
    subprocess.run(
        [
            "cp",
            os.path.join("/usr/share/easy-rsa/pki/private/", f"{nomeCliente}.key"),
            destino,
        ],
        check=True,
    )
except:
    print("Erro ao executar o cliente.key")

try:
    subprocess.run(
        [
            "cp",
            os.path.join("/usr/share/easy-rsa/pki/dh.pem"),
            destino,
        ],
        check=True,
    )
except:
    print("Erro ao executar o cp dh.pem")

try:
    subprocess.run(
        [
            "cp",
            "-r",
            f"/etc/openvpn/client/{nomeCliente}",
            "/home/usuario/",
        ],
        check=True,
    )
except:
    print("Erro ao executar o cp -r")

ovpn_conteudo = f"""client
dev tun
proto udp

remote {ipServidor}

ca ca.crt
cert {nomeCliente}.crt
key {nomeCliente}.key

tls-client
resolv-retry infinite
nobind
persist-key
persist-tun
"""

try:
    with open(os.path.join(
                "/etc/openvpn/client/", nomeCliente,f"{nomeCliente}.ovpn"
            ), "w") as f:
        f.write(ovpn_conteudo)
except Exception as e:
    print("Erro ao criar o arquivo .ovpn")

try:
    subprocess.run(
        [
            "cp",
            os.path.join(
                "/etc/openvpn/client/", nomeCliente,f"{nomeCliente}.ovpn"
            ),
            os.path.join("/home/usuario/", nomeCliente),
        ],
        check=True,
    )
except:
    print("Erro ao executar o cp cliente.ovpn")

try:
    subprocess.run(
        ["chown", "-R", "usuario:usuario", f"/home/usuario/{nomeCliente}"], check=True
    )
except:
    print("Erro ao executar o chown")

destino = f"/home/usuario/{nomeCliente}.zip"
origem = f"/home/usuario/{nomeCliente}"

with zipfile.ZipFile(destino, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(origem):
            for file in files:
                caminho_completo = os.path.join(root, file)
                caminho_relativo = os.path.relpath(caminho_completo, origem)
                zipf.write(caminho_completo, caminho_relativo)