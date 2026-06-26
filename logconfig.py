"""Logging setup for the dev entry points (watch.py).

Kept at the root, out of `src/`, on purpose: configuring logging is an app/dev
concern, and a library must never ship it. The model code under `src/` stays a
clean library — it only does `getLogger(__name__)`; this owns the handlers and
levels. If `src/` ever graduates into an installable library, the config stays
here and doesn't tag along.

Grows into `logging.config.dictConfig` here if it ever needs per-logger handlers.
"""
import logging
import os


def setup_logging():
    # partomatic configures its own logger at import time (ignoring a later
    # setLevel), so mute it via its env knob — must be set before anything
    # imports partomatic.
    os.environ.setdefault("PARTOMATIC_LOG_LEVEL", "WARNING")

    logging.basicConfig(
        level=logging.INFO,                # our model code logs at INFO
        format="[%(asctime)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    for noisy in ("build123d", "watchfiles", "ocp_vscode", "ocp_tessellate"):
        logging.getLogger(noisy).setLevel(logging.WARNING)
