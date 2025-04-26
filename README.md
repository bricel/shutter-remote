# ssh into your Raspberry Pie

```angular2html
ssh admin@192.168.1.50
```

password: `admin`


Here's how to set it up:

### 1. Create a systemd service file

```bash
sudo nano /etc/systemd/system/motor-control.service
```

### 2. Add the following content to the file

```
[Unit]
Description=Motor Control Web Server
After=network.target

[Service]
User=root
WorkingDirectory=/home/admin/shutter-control
ExecStart=/home/admin/shutter-control/venv/bin/python /home/admin/shutter-control/app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Make sure to:
- Change `root` to your actual username if different
- Check that the paths match your actual setup
- If you're not using a virtual environment, change the ExecStart line to use the system Python: `ExecStart=/usr/bin/python3 /home/admin/motor_control/app.py`

### 3. Save and exit the editor (Ctrl+O, Enter, Ctrl+X)

### 4. Enable and start the service

```bash

sudo systemctl enable motor-control.service
sudo systemctl start motor-control.service
```

### 5. Check the status to make sure it's running

```bash
sudo systemctl status motor-control.service
```

You should see "active (running)" in the output.

### Troubleshooting

If the service doesn't start properly:

1. Check logs for errors:
```bash
sudo journalctl -u motor-control.service
or
sudo journalctl -u motor-control.service -f


```

2. Make sure your Python script has the necessary permissions:
```bash
chmod +x /home/admin/motor_control/app.py
```

3. If running without sudo causes GPIO permission issues, you might need to modify the service file:
```
[Service]
User=root
...
```


Reload the systemd manager configuration and restart the service if you make any changes to the service file:
```
sudo systemctl daemon-reload
sudo systemctl restart motor-control.service
```