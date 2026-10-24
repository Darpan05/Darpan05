# My Pi Dashboard 🍓

A small browser dashboard for your **Raspberry Pi 3**. See CPU temperature, uptime, memory usage, and disk usage. Readings update every three seconds.

No wiring, sensors, Python packages, accounts, or API keys are needed. Works on Raspberry Pi OS Lite or Desktop with Python 3.7 or newer. Missing system readings display as unavailable.

## Run on your Pi

1. Connect the Pi to your home network and open its terminal (or connect with SSH).
2. Get this project onto the Pi. If you have pushed it to GitHub:

   ```bash
   git clone https://github.com/Darpan05/Darpan05.git
   cd Darpan05
   ```

   Otherwise, copy `app.py` and `index.html` together into a folder on the Pi, then open that folder in the terminal.

3. Start the dashboard:

   ```bash
   python3 app.py --host 0.0.0.0
   ```

4. In another terminal, run `hostname -I` to find your Pi's home-network IP address. On a phone or computer on the same network, open `http://YOUR_PI_IP:8000` in a modern browser.

Keep the terminal running. Press **Ctrl+C** to stop. Run the command again after rebooting. To choose another port, add `--port 8080`.

The dashboard is read-only and has no login. Use it on a trusted home network; do not forward its port to the internet. The default command `python3 app.py` accepts connections only from the Pi itself.

## Check it works

With the server running, from a second terminal on the Pi:

```bash
curl --fail http://127.0.0.1:8000/api/stats
```

You should receive JSON with your hostname and system readings. The page should show the same readings and update its timestamp automatically. If another device cannot connect, check that both devices use the same network, you used `--host 0.0.0.0`, and your firewall allows the selected port.

## How it works

`app.py` serves the page and a read-only `/api/stats` endpoint using Python's standard library. Linux system files supply temperature, uptime, and memory readings; Python supplies disk usage. `index.html` displays the readings without external libraries or external requests.

Ideas to try next: add a high-temperature color indicator, show free disk space, or add a light/dark theme.
