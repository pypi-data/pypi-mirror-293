import sys

import click
import importlib_resources
from click_loglevel import LogLevel
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from loguru import logger

import odoo_pos_driver

from .app import app
from .interface import interface


@click.command()
@click.option(
    "-a",
    "--address",
    type=click.STRING,
    default="0.0.0.0",
    show_default=True,
    help="Address on which the web service will be exposed",
)
@click.option(
    "-p",
    "--port",
    type=click.INT,
    default=8069,
    show_default=True,
    help="Port on which the web service will be exposed",
)
@click.option(
    "--secure/--unsecure",
    default=True,
    show_default=True,
    help="Option 'secure' exposes web service on https."
    " Option 'unsecure' exposes web service on http.",
)
@click.option(
    "-r",
    "--refresh-devices-delay",
    type=click.INT,
    default=1,
    show_default=True,
    help="Interval in seconds between two device refreshes",
)
@click.option(
    "-l",
    "--log-level",
    type=LogLevel(extra=["TRACE", "SUCCESS"]),
    default="INFO",
    show_default=True,
)
@click.version_option(version=odoo_pos_driver.__version__)
def main(log_level, address, port, refresh_devices_delay, secure):
    kwargs = {"handler_class": WebSocketHandler}

    # Log Configuration
    logger.remove()
    logger.add(sys.stderr, level=log_level)

    # Update Interface settings
    interface.refresh_devices_delay = refresh_devices_delay
    interface.refresh_usb_devices()
    interface.start()

    # Handle HTTPS, if required
    if secure:
        cert_folder = (
            importlib_resources.files("odoo_pos_driver") / "default_cert"
        )
        server_key_path = cert_folder / "server.key"
        server_cert_path = cert_folder / "server.crt"
        kwargs.update(
            {"keyfile": server_key_path, "certfile": server_cert_path}
        )
    http_server = pywsgi.WSGIServer((address, port), app, **kwargs)
    prefix = secure and "https" or "http"
    logger.success(
        f"Serving odoo-pos-driver (version: {odoo_pos_driver.__version__})"
        f" on {prefix}://{address}:{port} ..."
    )
    http_server.serve_forever()
