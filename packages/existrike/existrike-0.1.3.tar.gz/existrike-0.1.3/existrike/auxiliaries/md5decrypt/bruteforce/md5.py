import hashlib
import argparse
import sys
import time

# ANSI Colors for messages
class Colors:
    INFO = '\033[94m'  # Light blue
    SUCCESS = '\033[92m'  # Light green
    ERROR = '\033[91m'  # Red
    BOLD = '\033[1m'  # Bold
    YELLOW = '\033[93m'  # Yellow
    RESET = '\033[0m'  # Reset color

def md5_hash(password):
    """Generates the MD5 hash of a password."""
    return hashlib.md5(password.encode()).hexdigest()

def brute_force_md5(hash_to_crack, wordlist_file):
    """Performs a brute force attack to find the password corresponding to the MD5 hash."""
    attempts = 0
    start_time = time.time()

    try:
        with open(wordlist_file, 'r') as file:
            for line in file:
                attempts += 1
                password = line.strip()
                if md5_hash(password) == hash_to_crack:
                    end_time = time.time()
                    return password, attempts, end_time - start_time
    except FileNotFoundError:
        print(f"{Colors.ERROR}[ERROR] File {wordlist_file} not found.{Colors.RESET}")
        return None, attempts, 0

    return None, attempts, time.time() - start_time

def main():
    parser = argparse.ArgumentParser(description="Brute force attack on MD5 hashes using a wordlist.")
    parser.add_argument('-i', '--hash', required=True, help="MD5 hash to be cracked.")
    parser.add_argument('-w', '--wordlist', required=True, help="Path to the wordlist.")

    args = parser.parse_args()

    print(f"{Colors.INFO}[INFO] Starting brute force attack for MD5 hash {args.hash}.{Colors.RESET}")

    cracked_password, attempts, elapsed_time = brute_force_md5(args.hash, args.wordlist)
    
    if cracked_password:
        print(f"{Colors.SUCCESS}[SUCCESS] Password found: {cracked_password}.{Colors.RESET}")
    else:
        print(f"{Colors.ERROR}[ERROR] Password not found in the wordlist.{Colors.RESET}")

    # Report in yellow and bold
    print(f"{Colors.YELLOW}{Colors.BOLD}[INFO] Total attempts: {attempts}.{Colors.RESET}")
    print(f"{Colors.YELLOW}{Colors.BOLD}[INFO] Time taken: {elapsed_time:.2f} seconds.{Colors.RESET}")
    print(f"\n{Colors.YELLOW}                  𝔹𝕪 ℝ𝔸𝔻ℕ𝔼𝕋𝟞𝟜{Colors.RESET}")
if __name__ == "__main__":
    main()
