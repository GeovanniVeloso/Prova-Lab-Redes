#!/usr/bin/python3
# scripVPn.py

import sys
import os
import subprocess

nomeCliente = sys.argv[1]
password = sys.argv[2]

try:
    subprocess.run(
        ["/usr/share/easy-rsa/easyrsa", "gen-req", nomeCliente, "nopass"], check=True
    )
except:
    print("Erro ao executar o gen-req")

try:
    subprocess.run(
        ["/usr/share/easy-rsa/easyrsa", "sign-req", "client", nomeCliente],
        input=f"yes\n{password}",
        text=True,
        check=True,
    )
except:
    print("Erro ao executar o sign-req")

try:
    subprocess.run(
        ["mkdir", os.path.join("/etc/openvpn/clientes/", nomeCliente)], check=True
    )
except:
    print("Erro ao executar o mkdir")

try:
    subprocess.run(
        [
            "cp",
            "/usr/share/easy-rsa/pki/ca.crt",
            os.path.join("/etc/openvpn/cliente/", nomeCliente),
        ],
        check=True,
    )
except:
    print("Erro ao executar o cp ca.crt")

try:
    subprocess.run(
        [
            "cp",
            os.path.join("/usr/share/easy-rsa/pki/issued/", nomeCliente, ".crt"),
            os.path.join("/etc/openvpn/clientes/", nomeCliente, "/"),
        ],
        check=True,
    )
except:
    print("Erro ao executar o cp cliente.crt")

try:
    subprocess.run(
        [
            "cp",
            os.path.join("/usr/share/easy-rsa/pki/private/", nomeCliente, ".key"),
            os.path.join("/etc/openvpn/clientes/", nomeCliente, "/"),
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
            os.path.join("/etc/openvpn/clientes/", nomeCliente, "/"),
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
            os.path.join("/etc/openvpn/clientes/", nomeCliente),
            "/home/clientes/",
        ],
        check=True,
    )
except:
    print("Erro ao executar o cp -r")

# Criando o certificado - cd /usr/share/easy-rsa/ | sudo ./easyrsa gen-req nomeCliente nopass

# Criando o certificado P2 - cd /usr/share/easy-rsa/ | sudo ./easyrsa sign-req client nomeCliente

# Criando o certificado por cliente - sudo mkdir /etc/openvpn/client/nomeCliente -> OK
# sudo cp /usr/share/easy-rsa/pki/ca.crt /etc/openvpn/client/nomeCliente -> OK
# sudo cp /usr/share/easy-rsa/pki/issued/nomeCliente.crt /etc/openvpn/client/nomeCliente/ -> OK
# sudo cp /usr/share/easy-rsa/pki/private/nomeCliente.key /etc/openvpn/client/nomeCliente/ -> Ok
# sudo cp /usr/share/easy-rsa/pki/dh.pem /etc/openvpn/client/nomeCliente/ -> Ok
# sudo cp -r /etc/openvpn/client/nomeCliente /home/clientes/

# Criando o arquivo ovpn - sudo nano /etc/openvpn/client/nomeCliente/nomeCliente.ovpn

# client
# dev tun
# proto udp

# remote ip server 1194

# ca ca.crt
# cert nomeCliente.key
# key nomeCliente.key

# tls-client
# resolv-retry infinite
# nobind
# persist-key
# persist-tun

# Movendo os arquivos para o cliente - cp /etc/openvpn/client/nomeCliente/nomeCliente.ovpn /home/clientes/nomeCliente/
# Dando permissão - sudo chown -R usuario:usuario /home/clientes/nomeCliente

try:
    subprocess.run(
        [
            "cp",
            os.path.join(
                "/etc/openvpn/client/", nomeCliente, "/", nomeCliente, ".ovpn"
            ),
            os.path.join("/etc/openvpn/clientes/", nomeCliente),
        ],
        check=True,
    )
except:
    print("Erro ao executar o cp cliente.ovpn")

try:
    subprocess.run(
        ["chown", "-R", "usuario:usuario /home/clientes/", nomeCliente], check=True
    )
except:
    print("Erro ao executar o chown")
