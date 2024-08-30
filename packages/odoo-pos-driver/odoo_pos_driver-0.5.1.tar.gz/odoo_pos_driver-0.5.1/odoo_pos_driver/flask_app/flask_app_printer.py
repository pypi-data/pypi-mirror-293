from flask import jsonify, request
from loguru import logger

from ..app import app
from ..interface import interface


@app.route("/hw_proxy/default_printer_action", methods=["POST", "PUT"])
@logger.catch
def default_printer_action():
    logger.trace("default_printer_action()")
    data = request.json["params"]["data"]
    action = data["action"]

    if action == "print_receipt":
        receipt = data["receipt"]
        interface.device_printer_task_print(receipt)

    elif action == "cashbox":
        interface.device_printer_task_open_cashbox()

    return jsonify(jsonrpc="2.0", result=True)
