from devices import DEVICES_LIST
from netmiko import ConnectHandler


def analyze_interfaces(output_ip_brief):
  up_interfaces = []
  down_interfaces = []
  fast_count = 0
  giga_count = 0

  for line in output_ip_brief.splitlines():
    # Comptage des types d'interfaces
    if "FastEthernet" in line or "Fa" in line:
      fast_count += 1
    elif "GigabitEthernet" in line or "Gi" in line or "Ethernet" in line:
      giga_count += 1

    # Filtrage Up / Down
    if " up " in line and not line.startswith("Interface"):
      up_interfaces.append(line)
    elif " down " in line or "administratively down" in line:
      down_interfaces.append(line)

  return up_interfaces, down_interfaces, fast_count, giga_count


def run_tp():
  for dev in DEVICES_LIST:
    dev_name = dev.get("name", dev["host"])
    print(f"\n{'='*60}")
    print(f"Traitement de l'équipement : {dev_name} ({dev['host']})")
    print(f"{'='*60}")

    try:
      # On retire la clé 'name' avant de l'envoyer à Netmiko
      netmiko_params = {
          k: v for k, v in dev.items() if k in ["device_type", "host", "username", "password"]
      }

      with ConnectHandler(**netmiko_params) as net_connect:
        print("Connexion réussie !\n")

        # 1. Informations système (Nom, OS, Version)
        print("--- 1. INFORMATIONS SYSTÈME ---")
        version_output = net_connect.send_command("show version")
        for line in version_output.splitlines():
          if "Cisco IOS Software" in line or "Uptime is" in line:
            print(line)

        # 2, 3 & 4. Analyse des interfaces
        print("\n--- 2, 3 & 4. GESTION DES INTERFACES ---")
        ip_brief = net_connect.send_command("show ip interface brief")
        up_ifs, down_ifs, fa_cnt, gi_cnt = analyze_interfaces(ip_brief)

        print(f"-> Interfaces UP : {len(up_ifs)}")
        for ui in up_ifs:
          print(f"   [UP] {ui}")

        print(f"-> Interfaces DOWN : {len(down_ifs)}")
        for di in down_ifs:
          print(f"   [DOWN] {di}")

        # 5. Table de routage
        print("\n--- 5. TABLE DE ROUTAGE (show ip route) ---")
        print(net_connect.send_command("show ip route"))

    except Exception as e:
      print(f"Erreur de connexion vers {dev_name} : {e}")


if __name__ == "__main__":
  run_tp()
