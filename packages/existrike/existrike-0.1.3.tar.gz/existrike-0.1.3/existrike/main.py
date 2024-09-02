#!/usr/bin/env python3
import os
import getpass
import time
from colorama import init, Fore, Style
from .utils.secure_account_manager import SecureAccountManager
from .utils.exploit_manager import ExploitManager

# Inicialize o colorama
init(autoreset=True)

def main():
    account_manager = SecureAccountManager()
    exploit_manager = ExploitManager()

    while True:
        try:
            action = input("Enter action (login, create, exit, help): ").strip()

            if action == "login":
                username = input("Enter username: ").strip()
                password = getpass.getpass("Enter password: ").strip()
                if account_manager.login(username, password):
                    print(f"Welcome {username}")
                    logged_in_menu(account_manager, exploit_manager)
                else:
                    print("Invalid credentials")

            elif action == "create":
                username = input("Enter name: ").strip()
                password = getpass.getpass("Enter password: ").strip()
                uid = account_manager.create_account(username, password)
                print(f"Account created for {username} with UID: {uid}")

            elif action == "exit":
                print("Exiting...")
                break

            elif action == "help":
                print("""
                Available commands:
                - login: Log into your account.
                - create: Create a new account.
                - exit: Exit the application.
                - help: Show this help message.
                """)

            else:
                print("Invalid action. Please try again.")

        except Exception as e:
            print(f"An error occurred: {e}")

def logged_in_menu(account_manager, exploit_manager):
    os.system("clear")
    print("""\033[1;31m
███████████████████████████
███████▀▀▀░░░░░░░▀▀▀███████
████▀░░░░░░░░░░░░░░░░░▀████
███│░░░░░░░░░░░░░░░░░░░│███
██▌│░░░░░░░░░░░░░░░░░░░│▐██
██░└┐░░░░░░░░░░░░░░░░░┌┘░██
██░░└┐░░░░░░░░░░░░░░░┌┘░░██
██░░┌┘▄▄▄▄▄░░░░░▄▄▄▄▄└┐░░██
██▌░│██████▌░░░▐██████│░▐██
███░│▐███▀▀░░▄░░▀▀███▌│░███
██▀─┘░░░░░░░▐█▌░░░░░░░└─▀██
██▄░░░▄▄▄▓░░▀█▀░░▓▄▄▄░░░▄██
████▄─┘██▌░░░░░░░▐██└─▄████
█████░░▐█─┬┬┬┬┬┬┬─█▌░░█████
████▌░░░▀┬┼┼┼┼┼┼┼┬▀░░░▐████
█████▄░░░└┴┴┴┴┴┴┴┘░░░▄█████
███████▄░░░░░░░░░░░▄███████
██████████▄▄▄▄▄▄▄██████████
███████████████████████████
    \033[0m """)
    name = "𝐁𝐲 𝐑𝐀𝐃𝐍𝐄𝐓𝟔𝟒"
    for char in name:
      print(char, end='', flush=True)
      time.sleep(0.1)
    exploits_count = exploit_manager.count_files(exploit_manager.exploits_dir)
    scans_count = exploit_manager.count_files(exploit_manager.scans_dir)
    auxiliaries_count = exploit_manager.count_files(exploit_manager.auxiliaries_dir)
    print(f"\n{Style.BRIGHT}{Fore.GREEN}Exploits: {exploits_count}{Style.RESET_ALL}")
    print(f"{Style.BRIGHT}{Fore.BLUE}Scans: {scans_count}{Style.RESET_ALL}")
    print(f"{Style.BRIGHT}{Fore.YELLOW}Auxiliaries: {auxiliaries_count}{Style.RESET_ALL}\n")

    prompt = "\033[1;31m╰──root@expiravitpmc─➤\033[0m "
    current_module_prompt = ""

    while True:
        try:
            action_line = input(prompt).strip()
            if not action_line:
                continue

            parts = action_line.split()
            action = parts[0].lower()
            args = parts[1:]

            if action == "profile":
                profile = account_manager.get_profile(account_manager.get_current_user()['uid'])
                if profile:
                    print(f"Profile for {profile['Name']} (UID: {profile['UID']})")
                    print(f"Balance: {profile['Balance']}")
                    print(f"Paid Exploits: {profile['Paid Exploits']}")
                    print(f"VIP Level: {profile['VIP Level']}")
                    print(f"Attacks Used: {profile['Attacks Used']}")
                    print(f"VIP Expiry: {profile['VIP Expiry']}")
                else:
                    print("Failed to retrieve profile information.")

            elif action == "search" and len(args) >= 1:
                keyword = ' '.join(args)
                results = exploit_manager.search_modules(keyword)
                if results:
                    print("Found modules:")
                    for result in results:
                        highlighted_path = highlight_keyword(result, keyword)
                        print(highlighted_path)
                else:
                    print("No modules found.")

            elif action == "use" and len(args) >= 1:
                module_path = ' '.join(args)
                exploit_manager.use_module(module_path)
                current_module_prompt = f"\033[1;31m╰──{module_path}─➤\033[0m "
                prompt = current_module_prompt

            elif action == "set" and len(args) >= 2:
                key, value = args[0], ' '.join(args[1:])
                exploit_manager.set_option(key, value)

            elif action == "run":
                exploit_manager.run_module()

            elif action == "info":
                exploit_manager.info_module()

            elif action == "set_vip" and len(args) >= 1:
                vip_level = args[0]
                account_manager.set_vip(account_manager.get_current_user()['uid'], vip_level)

            elif action == "exploits":
                exploit_manager.list_modules("exploits")

            elif action == "scans":
                exploit_manager.list_modules("scans")

            elif action == "auxiliaries":
                exploit_manager.list_modules("auxiliaries")

            elif action == "logout":
                account_manager.logout()
                print("Logging out...")
                break

            elif action == "help":
                if current_module_prompt:
                    print(f"""
                    Available commands for current module:
                    - info: Get information about the current module.
                    - run: Execute the current module.
                    - back: Return to the main menu.
                    """)
                else:
                    print("""
                    Available commands:
                    - profile: View your profile information.
                    - search <keyword>: Search for modules.
                    - use <module_path>: Use a specific module.
                    - set <key> <value>: Set an option for the current module.
                    - run: Execute the current module.
                    - info: Get information about the current module.
                    - set_vip <level>: Set your VIP level.
                    - exploits: List all exploit modules.
                    - scans: List all scan modules.
                    - auxiliaries: List all auxiliary modules.
                    - logout: Log out of your account.
                    - help: Show this help message.
                    """)

            elif action == "back":
                current_module_prompt = ""
                prompt = "\033[1;31m╰──root@expiravitpmc─➤\033[0m "

            else:
                print("Invalid action or missing arguments. Please try again.")

        except Exception as e:
            print(f"An error occurred: {e}")

def highlight_keyword(text, keyword):
    start_tag = '\033[42m'  # ANSI escape code for green background
    end_tag = '\033[0m'     # ANSI reset code
    parts = text.split(keyword)
    highlighted_text = f"{start_tag}{keyword}{end_tag}".join(parts)
    return highlighted_text

if __name__ == "__main__":
    main()
