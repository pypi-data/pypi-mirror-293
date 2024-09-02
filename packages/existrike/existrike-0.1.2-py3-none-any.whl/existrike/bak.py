#!/usr/bin/env python3
import os
import subprocess
from threading import Thread

class ExploitManager:
    def __init__(self, exploits_dir='exploits', scans_dir='scans', auxiliaries_dir='auxiliaries'):
        self.exploits_dir = exploits_dir
        self.scans_dir = scans_dir
        self.auxiliaries_dir = auxiliaries_dir
        self.configurations = {}
        self.module_path = None
        self.module_type = None
        self.module_name = None

    def count_files(self, directory):
        return len([d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))])

    def search_modules(self, keyword):
        results = []
        base_dirs = {'exploits': self.exploits_dir, 'scans': self.scans_dir, 'auxiliaries': self.auxiliaries_dir}

        for module_type, base_dir in base_dirs.items():
            for root, dirs, _ in os.walk(base_dir):
                for dir_name in dirs:
                    module_path = os.path.join(root, dir_name)
                    config_path = os.path.join(module_path, 'config.cfg')
                    run_script_path = os.path.join(module_path, 'run.sh')
                    if keyword.lower() in module_path.lower() and os.path.isfile(config_path) and os.path.isfile(run_script_path):
                        full_module_path = os.path.join(module_type, os.path.relpath(module_path, base_dir))
                        results.append(full_module_path)

        return results

    def use_module(self, module_path):
        full_path = os.path.join(module_path)
        if os.path.isdir(full_path):
            self.module_path = full_path
            self.module_type, self.module_name = os.path.split(module_path)
            return True  # Indicate successful module selection
        else:
            print("Invalid module path.")
            return False

    def set_option(self, key, value):
        if self.module_path:
            self.configurations[key.lower()] = value
        else:
            print("No module selected.")

    def info_module(self):
        if self.module_path:
            config_path = os.path.join(self.module_path, 'config.cfg')
            if os.path.isfile(config_path):
                with open(config_path, 'r') as f:
                    requirements = f.read().splitlines()
                print(f"Module requirements: {', '.join(requirements)}")
                for req in requirements:
                    status = self.configurations.get(req.lower(), 'Not set')
                    print(f"{req}: {status}")
            else:
                print("Configuration file not found in the module directory.")
        else:
            print("No module selected.")

    def run_module(self):
        if self.module_path:
            config_path = os.path.join(self.module_path, 'config.cfg')
            run_script_path = os.path.join(self.module_path, 'run.sh')

            if os.path.isfile(config_path) and os.path.isfile(run_script_path):
                with open(config_path, 'r') as f:
                    requirements = f.read().splitlines()

                missing_configs = [req for req in requirements if req.lower() not in self.configurations]
                if missing_configs:
                    print(f"Missing configurations: {', '.join(missing_configs)}")
                    return

                command = ['bash', run_script_path] + [self.configurations.get(req.lower(), '') for req in requirements]
                print(f"Executing: {' '.join(command)}")

                # Execute the command and capture output in real-time using subprocess.Popen
                try:
                    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                    # Read stdout and stderr line by line in separate threads
                    def read_output(stream):
                        for line in stream:
                            line = line.strip()
                            if line:  # Print only non-empty lines
                                print(line)

                    stdout_thread = Thread(target=read_output, args=(process.stdout,))
                    stderr_thread = Thread(target=read_output, args=(process.stderr,))
                    stdout_thread.start()
                    stderr_thread.start()
                    stdout_thread.join()
                    stderr_thread.join()

                    # Wait for the process to complete
                    process.wait()

                except Exception as e:
                    print(f"An error occurred while executing the script: {e}")
            else:
                print("Configuration file or run script not found in the module directory.")
        else:
            print("No module selected.")

    def list_modules(self, module_type):
        base_dir = getattr(self, f"{module_type}_dir")
        print(f"Listing {module_type}:")
        for root, dirs, _ in os.walk(base_dir):
            for dir_name in dirs:
                module_path = os.path.join(root, dir_name)
                config_path = os.path.join(module_path, 'config.cfg')
                if os.path.isfile(config_path):
                    full_module_path = os.path.relpath(module_path, base_dir)
                    print(os.path.join(module_type, full_module_path))

    def help_module(self):
        if self.module_path:
            print(f"\nCommands available in module '{self.module_name}':")
            print("info - Display module information")
            print("run - Execute the module")
            print("back - Return to main menu")
            print("help - Display this help message")
        else:
            print("No module selected.")

    def back_to_menu(self):
        self.module_path = None
        self.module_type = None
        self.module_name = None

if __name__ == "__main__":
    manager = ExploitManager()

    while True:
        try:
            prompt = f"╰──{'/'.join(filter(None, [manager.module_type, manager.module_name]))}─➤ " if manager.module_path else "╰──root@expiravitpmc─➤ "
            cmd = input(prompt).strip()
            
            if cmd.startswith("search "):
                keyword = cmd.split(" ", 1)[1]
                results = manager.search_modules(keyword)
                if results:
                    print("Found modules:")
                    for result in results:
                        highlighted_path = highlight_keyword(result, keyword)
                        print(highlighted_path)
                else:
                    print("No modules found.")
                    
            elif cmd.startswith("use "):
                module_path = cmd.split(" ", 1)[1]
                if manager.use_module(module_path):
                    print(f"Module '{manager.module_name}' selected.")
                    prompt = f"╰──{'/'.join(filter(None, [manager.module_type, manager.module_name]))}─➤ "
                else:
                    prompt = "╰──root@expiravitpmc─➤ "
                
            elif cmd.startswith("set "):
                parts = cmd.split(" ", 2)
                if len(parts) == 3:
                    key, value = parts[1], parts[2]
                    manager.set_option(key, value)
                else:
                    print("Invalid set command format.")
                    
            elif cmd == "info":
                manager.info_module()
                
            elif cmd == "run":
                manager.run_module()
                
            elif cmd == "exploits":
                manager.list_modules("exploits")
                
            elif cmd == "scans":
                manager.list_modules("scans")
                
            elif cmd == "auxiliaries":
                manager.list_modules("auxiliaries")
                
            elif cmd == "help":
                manager.help_module()
                
            elif cmd == "back":
                manager.back_to_menu()
                prompt = "╰──root@expiravitpmc─➤ "
                
            elif cmd == "exit":
                break
                
            else:
                print("Unknown command.")
                
        except Exception as e:
            print(f"An error occurred: {e}")
