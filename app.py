import socket
import requests
import re
from flask import Flask, current_app, jsonify, send_from_directory

# Kramer switcher URL
KRAMER_HOST_URL = "http://192.168.0.39/aj.shtml?a=SCAFUN&i=0&f=0&v="

# IP address of the Sony projector
PROJECTOR_IP = "192.168.0.46"

# PORT of the Sony projector
PROJECTOR_PORT = 53595

commands = {
    "POWER_STATUS": "power_status ?\r\n",
    "POWER_ON": 'power "on"\r\n',
    "POWER_OFF": 'power "off"\r\n',
    "BLANK_ON": 'blank "on"\r\n',
    "BLANK_OFF": 'blank "off"\r\n',
    # Add other commands here...
}


class ProjectorController:
    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((ip, port))
            self.sock.recv(1024)
        except Exception as e:
            raise e

    def send_command(self, command):
        full_command = f"{command}"
        self.sock.sendall(full_command.encode())
        response = self.sock.recv(1024)
        return response.decode()

    def close(self):
        self.sock.close()


def switchKramerInput(input):
    url = KRAMER_HOST_URL + str(input)
    print("Sending command to switcher: " + url)
    if input >= 0 and input < 6:
        requests.get(url)


def sendProjectorCommand(command):
    p = ProjectorController(PROJECTOR_IP, PROJECTOR_PORT)
    print('Sending to projector: "' + command.strip() + '"')
    try:
        res = p.send_command(command)
    except Exception as e:
        raise e

    print("Projector response:" + res.strip())
    p.close()


app = Flask(__name__)


# Path for our main Svelte page
@app.route("/")
def base():
    return send_from_directory("client/public", "index.html")


# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory("client/public", path)


@app.route("/c/<command>")
def handle_command(command):
    try:
        match = re.match(r"v(\d+)", command)
        if match:
            num = int(match.group(1))
            if num >= 1 and num <= 6:
                switchKramerInput(num - 1)
            else:
                print("Invalid input number")
        elif command == "blankon":
            sendProjectorCommand(commands["BLANK_ON"])
        elif command == "blankoff":
            sendProjectorCommand(commands["BLANK_OFF"])
        elif command == "poweron":
            sendProjectorCommand(commands["POWER_ON"])
        elif command == "poweroff":
            sendProjectorCommand(commands["POWER_OFF"])
        else:
            print("Unknown command: " + command)
            return jsonify({"status": "error: unknown command"})
    except Exception as e:
        print("Error: " + str(e))
        return jsonify({"status": "error: " + str(e)})
    return jsonify({"command": command, "status": "ok"})
