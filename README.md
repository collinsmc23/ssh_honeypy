# 🍯 SSH_HONEYPY
A basic python SSH honeypot to capture IP Adresses, usernames, passwords, and commands.

# Install

**1) Clone repository.**
`git clone https://github.com/collinsmc23/ssh_honeypy.git`

**2) Permissions.**
Move into `ssh_honeypy` folder.

Ensure `main.py` has proper permisions. (`chmod 755 main.py`)

**3) Keygen.**

An RSA key must be generated for the SSH server host key. The SSH host key provides proper identification for the SSH server. Ensure the key is titled `server.key` and resides in the same relative directory to the main program.

`ssh-keygen -t rsa -b 2048 -f server.key`

# Usage

SSH_HONEYPY requires a bind IP address (`-a`) and network port to listen on (`-p`). Use `0.0.0.0` to listen on all network interfaces. 

```
-a / --address: Bind address.
-p / --port: Port.
```

Example: `python3 main.py -a 0.0.0.0 -p 22`

💡 If SSH_HONEYPY is set up to listen on a privileged port (22), the program must be run with `sudo` or root privileges. No other services should be using the specified port. 

If port 22 is being used as the listener, the default SSH port must be changed. Refer to Hostinger's "(How to Change the SSH Port)[https://www.hostinger.com/tutorials/how-to-change-ssh-port-vps]" guide.

**Optional Arguments**

A username (`-u`) and password (`-w`) can be specified to authenticate the SSH server. The default configuration will accept all usernames and passwords.

```
-u / --username: Username.
-w / --password: Password.
```

Example: `python3 main.py -a 0.0.0.0 -p 22 -u admin -p admin`

# Logging Files

SSH_HONEYPY has two loggers configured. Loggers will route to either `cmd_audits.log` or `creds_audits.log` log files for information capture.

`cmd_audits.log`: Captures IP address, username, password, and all commands supplied.

`creds_audits.log`: Captures IP address, username, and password, comma seperated. Used to see how many hosts attempt to connect to SSH_HONEYPY.

# Video Overview

[![YouTube Video](https://img.youtube.com/vi/tyKyLhcKgNo/0.jpg)](https://youtu.be/tyKyLhcKgNo)

# Future Features

- Systemd support to run Python script in background.
- Docker support for host-based isolation and code deployment.
- Write additional support for common protocols, Telnet, HTTP(S) web server, SMTP...
- Create a basic overview Dashboard. 
- ~~Add SSH Banner Tarpit to trap SSH sessions~~ ✅ (`-t, --tarpit`)

# Helpful Resources

Resources and guides used while developing project.

- https://securehoney.net/blog/how-to-build-an-ssh-honeypot-in-python-and-docker-part-1.html 
- https://medium.com/@abdulsamie488/deceptive-defense-building-a-python-honeypot-to-thwart-cyber-attackers-2a9d2ced2760
- https://gist.github.com/cschwede/3e2c025408ab4af531651098331cce45
- https://www.hostinger.com/tutorials/how-to-change-ssh-port-vps