import logging
import os
import socket
import subprocess
import sys
import time
import traceback

import build123d
import ocp_vscode
from watchfiles import watch, PythonFilter

from logconfig import setup_logging

VIEWER_PORT = 3939
VIEWER_SETTLE = 3.0      # let a freshly-launched viewer's browser page connect before first render

if len(sys.argv) < 2:
    sys.exit("usage: python watch.py <model.py>")

target = sys.argv[1]
watch_dir = os.path.dirname(os.path.abspath(target))
data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

sys.path.insert(0, watch_dir)
setup_logging()      # entry point owns logging config; models just getLogger() + log
log = logging.getLogger("watch")


def viewer_running():
    with socket.socket() as s:
        s.settimeout(0.3)
        return s.connect_ex(("127.0.0.1", VIEWER_PORT)) == 0


def start_viewer():
    if viewer_running():
        log.info(f"reusing ocp_vscode viewer already on port {VIEWER_PORT}")
        return None            # not ours to manage
    log.info(f"starting ocp_vscode viewer on port {VIEWER_PORT} ...")
    proc = subprocess.Popen(
        [sys.executable, "-m", "ocp_vscode"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    for _ in range(100):
        if viewer_running():
            log.info(f"ocp_vscode viewer ready — open http://localhost:{VIEWER_PORT}")
            return proc
        time.sleep(0.1)
    log.warning(f"ocp_vscode viewer didn't come up on port {VIEWER_PORT}")
    return proc


def stop_viewer(proc):
    if proc is None:
        return
    log.info("shutting down ocp_vscode viewer")
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()


def purge_local_modules():
    for name, mod in list(sys.modules.items()):
        path = getattr(mod, "__file__", None) or ""
        if path.startswith(watch_dir):
            del sys.modules[name]


def run():
    purge_local_modules()
    try:
        script = compile(open(target).read(), target, "exec")
        exec(script, {"__name__": "__main__"})
    except Exception:
        traceback.print_exc()


log.info(f"watching {watch_dir}  (Ctrl-C to stop)")
viewer = start_viewer()
if viewer is not None:
    time.sleep(VIEWER_SETTLE)
try:
    run()                                             # initial render
    for _changes in watch(
            watch_dir, data_dir,
            watch_filter=PythonFilter(extra_extensions=('.yaml',))):
        run()
except KeyboardInterrupt:
    pass
finally:
    stop_viewer(viewer)
    log.info("watcher stopped")
