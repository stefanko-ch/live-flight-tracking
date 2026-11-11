"""The whole thing with one command – no notebook needed:

    uv run start.py              # live Switzerland from OpenSky + map in the browser + all analyses
    uv run start.py --no-browser # the same, without opening the browser

What it does: reads .env, starts the map app (app/app.py) – it collects Switzerland live from OpenSky into
flights.duckdb and runs all analyses in the background – and opens http://127.0.0.1:<port> in your browser.
Stop with Ctrl+C. Leave it running for a few hours: notebooks 07–20 analyse what it collected.

Optional, only with the R2 settings of your own S3-compatible archive in .env (same layout as notebook 04):
    uv run start.py --hours 6    # first load the last 6 h from the archive (default 24)
    uv run start.py --no-world   # do not mirror the world feed from the archive
"""
import argparse
import os
import runpy
import socket
import sys
import threading
import time
import webbrowser
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import flightlab as fl  # noqa: E402


def free_port(start=8050):
    for port in range(start, start + 20):
        with socket.socket() as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
    raise SystemExit("no free port between 8050 and 8069")


def main():
    ap = argparse.ArgumentParser(description="Start the map app: live Switzerland from OpenSky, all analyses, "
                                             "optional backfill from your own S3-compatible archive.")
    ap.add_argument("--hours", type=float, default=24,
                    help="hours of history from the archive (only with R2 settings in .env, default 24)")
    ap.add_argument("--no-world", action="store_true",
                    help="do not mirror the world feed from the archive (only relevant with R2 settings)")
    ap.add_argument("--no-browser", action="store_true", help="do not open the browser")
    args = ap.parse_args()

    env = fl.load_env()
    has_r2 = fl.has_r2(env)
    if not has_r2:
        print("No R2 settings in .env – collecting Switzerland live from OpenSky (no archive backfill, no world "
              "feed). That is the normal setup.")
    os.environ.setdefault("BACKFILL_HOURS", str(args.hours if has_r2 else 0))   # done by the app's collector thread
    if args.no_world:
        os.environ["R2_REGIONS"] = ""            # wins over R2_REGIONS in .env (the app only fills unset variables)
    elif has_r2:
        os.environ.setdefault("R2_REGIONS", "world")
    os.environ.setdefault("PYTHONUNBUFFERED", "1")
    port = int(os.environ.setdefault("PORT", str(free_port())))

    if not args.no_browser:
        def _open():
            time.sleep(8)                                    # the app needs a few seconds to start
            webbrowser.open(f"http://127.0.0.1:{port}")
        threading.Thread(target=_open, daemon=True).start()

    print(f"Starting the map on http://127.0.0.1:{port} – history: {os.environ['BACKFILL_HOURS']} h, "
          f"world feed: {'on' if os.environ.get('R2_REGIONS') else 'off'}. Ctrl+C stops it.")
    sys.path.insert(0, str(HERE / "app"))
    os.chdir(HERE / "app")
    runpy.run_path(str(HERE / "app" / "app.py"), run_name="__main__")


if __name__ == "__main__":
    main()
