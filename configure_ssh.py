import time
from devices import DEVICES_LIST
from netmiko import ConnectHandler

# Commande RSA standard compatible avec toutes les versions Cisco IOS/IOS-XE
ssh_config_commands = [
    "ip domain name cisco.local",
    "crypto key generate rsa modulus 1024",
    "line vty 0 4",
    "transport input ssh",
    "login local",
]


def enable_ssh_on_devices():
  for dev in DEVICES_LIST:
    dev_name = dev.get("name", dev["host"])
    print(f"\n{'='*50}")
    print(f"Activation du SSH sur : {dev_name} ({dev['host']})")
    print(f"{'='*50}")

    temp_params = {
        "device_type": "cisco_ios_telnet",
        "host": dev["host"],
        "username": dev["username"],
        "password": dev["password"],
        "secret": "cisco",
    }

    try:
      with ConnectHandler(**temp_params) as net_connect:
        print("Connexion Telnet réussie.")
        net_connect.enable()
        print("Mode privilégié activé.")

        output = net_connect.send_config_set(ssh_config_commands)
        print(output)
        print(f"-> SSH configuré avec succès sur {dev_name} !")

      # Pause de 2 secondes pour éviter de saturer les ports des équipements
      time.sleep(2)

    except Exception as e:
      print(f"Erreur lors de la configuration de {dev_name} : {e}")


if __name__ == "__main__":
  enable_ssh_on_devices()
