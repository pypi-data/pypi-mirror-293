import os
import platform

import psutil
from flask import render_template, send_from_directory
from flask_babel import gettext as _
from loguru import logger

from .. import __version__
from ..app import app
from ..interface import interface


@app.route("/")
@app.route("/home.html")
@logger.catch
def home():
    return render_template("home.html.jinja", interface=interface)


@app.route("/favicon.ico")
@logger.catch
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static", "favicon"),
        "favicon.png",
        mimetype="image/png",
    )


@app.route("/usb_devices.html", methods=["GET"])
@logger.catch
def usb_devices():
    logger.trace("usb_devices()")
    return render_template("usb_devices.html.jinja", interface=interface)


@app.route("/system.html")
@logger.catch
def system():
    logger.trace("system()")
    system_info = [
        (_("Odoo PoS Drivers"), __version__),
        (_("Operating System"), platform.system()),
        (_("Kernel Release"), platform.release()),
        (_("Operating System Version"), platform.version()),
        (_("Architecture"), " / ".join(platform.architecture())),
        (_("Processors Type"), platform.processor()),
        (
            _("Processors Quantity"),
            f"{psutil.cpu_count(logical=False)} / {psutil.cpu_count()}",
        ),
        (
            _("Processors Frequency"),
            f"{(psutil.cpu_freq().current / 1024):.1f} Ghz",
        ),
        (
            _("Processors Load"),
            f"{(psutil.getloadavg()[0] / psutil.cpu_count() * 100):.2f} %",
        ),
        (
            _("Total Memory"),
            f"{(psutil.virtual_memory().total / (pow(1024, 3))):.2f} Gb",
        ),
        (_("Memory Usage"), f"{(psutil.virtual_memory().percent):.2f} %"),
        (_("Python Version"), platform.python_version()),
    ]
    return render_template("system.html.jinja", system_info=system_info)


@app.route("/errored_tasks.html/<string:device_type>")
@logger.catch
def errored_tasks(device_type):
    logger.trace("errored_tasks()")
    if device_type not in interface.device_types:
        raise Exception(f"{device_type} is not a valid device type.")
    device = interface.get_device(device_type)
    return render_template("errored_tasks.html.jinja", device=device)
