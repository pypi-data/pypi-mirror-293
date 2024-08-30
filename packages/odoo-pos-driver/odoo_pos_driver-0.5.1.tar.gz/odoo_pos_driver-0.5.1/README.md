# Odoo POS Driver

## Installation (to run manually)

* install the latest released version:

```shell
pipx install odoo-pos-driver
```

_or_

* Install the latest version:

```shell
pipx install git+https://gitlab.com/grap-rhone-alpes/odoo-pos-driver.git
```

Note: use ``--python python3.9`` (or higher) option, if your default python environment is under python 3.9 version.

## Installation (as a service)

This will create a service (via systemd) that will execute odoo-pos-driver in the background and launches at startup.

```shell
wget https://gitlab.com/grap-rhone-alpes/odoo-pos-driver/-/raw/main/install_debian.sh
# Optional adapt the installation script before execution:
# - add python specific version in pipx installation
# - add specific argument in the call of odoo-pos-driver in the .service file
sudo sh install_debian.sh
```

Once installed, you can run the following system command.

```shell
# Get status of the service
sudo systemctl status odoo-pos-driver.service

# Follow the logs of the service
sudo journalctl -fu odoo-pos-driver.service
```

## Odoo modules

- Odoo / point_of_sale
- OCA / pos_payment_terminal

# Credits

* Icon created by AbtoCreative (Flaticon):
  - Application icon: https://www.flaticon.com/fr/icones-gratuites/hub-usb

* Icon created by ToZ Icon (Flaticon):
  - Credit Card Payment Terminal: https://www.flaticon.com/fr/icone-gratuite/terminal-de-paiement_6137350

* Icon created by Iconic Panda (Flaticon):
  - LCD Customer Display: https://www.flaticon.com/fr/icone-gratuite/lcd_9622586

* Icon created by Icongeek26 (Flaticon):
  - Thermal Receipt Printer: https://www.flaticon.com/fr/icone-gratuite/facture_1649343
