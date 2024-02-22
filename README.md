# Server and Client app for controlling our Courtroom AV installs

## Server

Server accepts commands from the client and sends them to the appropriate devices. Only works with specific devices.

## Client

Ultra simple client meant to run on amazon fire 8" tablets in lockdown mode (Fully Kiosk Browser). It's a simple web app that sends commands to the server.

## setup

Server runs on a raspberry pi. Its a simple Flask application. Runs as a service using systemd.

Create the service file at /etc/systemd/system/avcontrol.service

```
[Unit]
Description=AV Control
After=network.target

[Service]
User=pi
WorkingDirectory=/path/to/your/flask/app
ExecStart=/path/to/your/venv/bin/flask run /path/to/your/flask/app/app.py --host=0.0.0.0 --port=5000
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:

```
sudo systemctl daemon-reload
sudo systemctl enable yourapp.service
sudo systemctl start yourapp.service
```

Check status with:

```
sudo systemctl status yourapp.service
```

Configure the tablet to point to the server @ port 5000.

Set up a WLAN in the courtroom and hardwire the pi to the switcher and projector. The tablet joins the WLAN wirelessly.
