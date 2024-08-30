from flask import jsonify, request
from loguru import logger

from ..app import app


@app.route(
    "/hw_proxy/payment_terminal_transaction_start", methods=["POST", "PUT"]
)
@logger.catch
def payment_terminal_transaction_start():
    logger.trace("payment_terminal_transaction_start()")
    data = request.json["params"]["payment_info"]
    logger.warning(
        "TODO: payment_terminal::payment_terminal_transaction_start"
    )
    logger.info(f"data: {data}")
    return jsonify(jsonrpc="2.0", result=True)
