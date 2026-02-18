from netmiko import ConnectHandler
import getpass

# 1. Get Credentials
username = input("Enter SSH Username: ")
password = getpass.getpass("Enter SSH Password: ")

# 2. Read Device List
with open('devices.txt') as f:
    devices_list = f.read().splitlines()

# 3. Define Configuration to Push
config_commands = [
    'interface Loopback100',
    'description Configured_via_Linux_Python',
    'ip address 10.10.10.1 255.255.255.0',
    'no shutdown'
]

# 4. Loop Through Each Device
for ip in devices_list:
    print(f"\n--- Connecting to {ip} ---")
    
    device_params = {
        'device_type': 'cisco_ios',
        'host': ip,
        'username': username,
        'password': password,
    }

    try:
        net_connect = ConnectHandler(**device_params)
        net_connect.enable()
        
        # Send Config
        output = net_connect.send_config_set(config_commands)
        print(output)
        
        # Verify
        print(f"Verifying {ip}...")
        check = net_connect.send_command('show ip int brief | include Loopback')
        print(check)
        
        net_connect.disconnect()
        print(f"✅ Finished {ip}")

    except Exception as e:
        print(f"❌ Failed to connect to {ip}: {e}")
