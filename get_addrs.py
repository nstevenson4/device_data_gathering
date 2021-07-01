from netmiko import ConnectHandler
import time
from getpass import getpass
import concurrent.futures

device_list = input('Enter name of device list file: ').strip()
output_file = 'juniper_ip_list.txt'
start_time = time.perf_counter()
login = input('Username: ')
password = getpass('Password: ')

def get_net_devices():
    with open(device_list) as devices:
        addresses = devices.read().splitlines()
    return addresses

def get_device_data(address):
    junos_device_info = {
        'ip': address,
        #'port': 22,
        'username': login,
        'password': password,
        'device_type': 'juniper',
        'verbose': True
    }
    print(f'Connecting to host {address}...')
    ssh_connection = ConnectHandler(**junos_device_info)
    border = "-----------------------------"
    host_name = ssh_connection.send_command("show configuration system host-name | display set | trim 21")
    spacer = "--"
    output = ssh_connection.send_command('show configuration interfaces | match address | trim 20')
    #version = ssh_connection.send_command('show version')
    
    with open(output_file, 'a+') as data_file:
       #time.sleep(1)
       data_file.write(border + "\n" + host_name + "" + spacer + "\n" + output + "" + border + "\n")
       #time.sleep(1)

    print(border + "\n" + host_name + "" + spacer + "\n" + output + "" + border + "\n")
    ssh_connection.disconnect()
    return

def main():
   with concurrent.futures.ThreadPoolExecutor() as exe:
      ip_addresses = get_net_devices()
      results = exe.map(get_device_data, ip_addresses)
      print(results)

   finish_time = time.perf_counter()
   print(f'The script finished executing in {round(start_time - finish_time,2)} seconds.')

   exit_script = input("Close Window or Type 'y' and press 'Enter' to exit: ")
   exit_script = exit_script.lower()
   
   if exit_script == 'y':
       exit()

if __name__ == '__main__':
   main()