import time
from threading import Thread

import usb
from loguru import logger

from . import devices


class Interface(Thread):
    device_types = ["display", "printer", "payment", "scale"]

    def __init__(self, refresh_devices_delay=1):
        Thread.__init__(self)
        self.usb_devices = []
        self.refresh_devices_delay = refresh_devices_delay
        self.usb_device_display = devices.DeviceDisplay(
            self, delay=1, max_queue_size=10
        )
        self.usb_device_display.start()

        self.usb_device_printer = devices.DevicePrinter(
            self, delay=1, max_queue_size=3
        )
        self.usb_device_printer.start()

        self.usb_device_payment = devices.DevicePayment(self)
        self.usb_device_payment.start()

        self.usb_device_scale = devices.DeviceScale(self)
        self.usb_device_scale.start()

    def get_device(self, device_type):
        return getattr(self, f"usb_device_{device_type}")

    def device_display_task_display_lines(self, lines):
        self.usb_device_display.add_task(lines)

    def device_printer_task_print(self, receipt):
        self.usb_device_printer.add_task(("print", receipt))

    def device_printer_task_open_cashbox(self):
        self.usb_device_printer.add_task(("open_cashbox", False))

    @logger.catch
    def refresh_usb_devices(self):
        logger.info(
            "Refreshing USB Devices List ..."
            f"(Next refresh in {self.refresh_devices_delay} second(s).)"
        )
        new_devices = [device for device in usb.core.find(find_all=True)]

        # Detect new devices
        for device in new_devices:
            if device not in self.usb_devices:
                self._hook_usb_device_new(device)

        # Handle device removal
        for device in self.usb_devices:
            if device not in new_devices:
                self._hook_usb_device_removed(device)

    def run(self):
        while True:
            time.sleep(self.refresh_devices_delay)
            self.refresh_usb_devices()

    def _hook_usb_device_new(self, device):
        """Handle here things to be done, when a new device is detected"""
        (device_type, extra_info) = devices.get_device_type(
            device.idVendor, device.idProduct
        )
        logger.log(
            device_type and "INFO" or "DEBUG",
            f"Found new USB device."
            f" Type '{device_type or 'Unknown'}'."
            f" Code: {self.get_device_id_vendor_id_product(device)} ;"
            f" Name: {self.get_device_product(device)}",
        )
        if device_type:
            getattr(self, f"usb_device_{device_type}").set_usb_device(
                device, extra_info
            )
        self.usb_devices.append(device)

    def _hook_usb_device_removed(self, device):
        """Handle here cleanup to be done, when a removal of
        device is detected"""
        (device_type, _extra_info) = devices.get_device_type(
            device.idVendor, device.idProduct
        )
        logger.info(
            f"Removing USB device."
            f" Code: {self.get_device_id_vendor_id_product(device)} ;"
            f" Name: {self.get_device_product(device)}"
        )
        if device_type:
            getattr(self, f"usb_device_{device_type}").remove_usb_device()
        self.usb_devices.remove(device)

    @classmethod
    def get_device_id_vendor_id_product(cls, device):
        return (
            "{0:04x}".format(device.idVendor)
            + ":"
            + "{0:04x}".format(device.idProduct)
        )

    @classmethod
    def get_device_manufacturer(cls, device):
        try:
            return device.manufacturer
        except ValueError:
            return ""

    @classmethod
    def get_device_serial_number(cls, device):
        try:
            return device.serial_number and device.serial_number or ""
        except ValueError:
            return ""

    @classmethod
    def get_device_product(cls, device):
        try:
            return device.product
        except ValueError:
            return ""

    @classmethod
    def get_device_type(cls, device):
        try:
            (device_type, _extra_info) = devices.get_device_type(
                device.idVendor, device.idProduct
            )
            return device_type
        except ValueError:
            return False


interface = Interface()
