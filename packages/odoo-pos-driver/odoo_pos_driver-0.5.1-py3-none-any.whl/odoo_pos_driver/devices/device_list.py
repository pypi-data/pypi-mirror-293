_DISPLAY_DEVICES = {
    (0x0416, 0xF012): {"name": "Aures - OCD 300"},
}

_PRINTER_DEVICES = {
    (0x04B8, 0x0202): {"name": "Epson - TM-T70 / TM-T88III / TM-T88IV "},
    (0x04B8, 0x0E03): {"name": "Epson - TM-T20"},
    (0x04B8, 0x0E15): {"name": "Epson - TM-T20II"},
    (0x04B8, 0x0E28): {"name": "Epson - TM-T20III"},
}

_PAYMENT_DEVICES = {
    (0x079B, 0x0028): {"name": "Ingenico - Move/5000"},
}


def get_device_type(vendor_code, product_code):
    """return the type of the device, depending on the
    vendor and product code;
    vendor_code: hexadecimal, example: 0x0416
    product_code: hexadecimal, example: 0xF012
    Return: value in ['display', 'printer', 'payment', 'scale', False]
    and extra data
    """
    vendor_product_code = (vendor_code, product_code)

    if vendor_product_code in _DISPLAY_DEVICES.keys():
        device_type = "display"
        extra_info = _DISPLAY_DEVICES.get(vendor_product_code)

    elif vendor_product_code in _PRINTER_DEVICES.keys():
        device_type = "printer"
        extra_info = _PRINTER_DEVICES.get(vendor_product_code)

    elif vendor_product_code in _PAYMENT_DEVICES.keys():
        device_type = "payment"
        extra_info = _PAYMENT_DEVICES.get(vendor_product_code)

    else:
        device_type = extra_info = False

    return (device_type, extra_info)
