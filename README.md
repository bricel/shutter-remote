I'll show you how to make your Python Flask server run automatically at startup on your Raspberry Pi Zero W running Ubuntu. There are several ways to do this, but the most reliable method for systemd-based systems like Ubuntu is using a systemd service.

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
User=admin
WorkingDirectory=/home/admin/motor_control
ExecStart=/home/admin/motor_control/venv/bin/python /home/admin/motor_control/app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Make sure to:
- Change `admin` to your actual username if different
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

Now your motor control web server will automatically start whenever your Raspberry Pi boots, and it will restart automatically if it crashes for any reason.
