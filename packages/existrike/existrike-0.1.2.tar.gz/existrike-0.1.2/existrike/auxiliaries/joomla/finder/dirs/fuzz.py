import argparse
import requests
from colorama import Fore, Style
import time

def scan_url(url, wordlist_file, save_file, show_only_200):
    start_time = time.time()  # Registra o tempo de início

    with open(wordlist_file, 'r') as wordlist:
        if save_file:
            result_file = open(save_file, 'w')
        else:
            result_file = None

        for line in wordlist:
            word = line.strip()
            target_url = 'https://' + url + '/' + word
            response = requests.get(target_url)
            status_code = response.status_code
            if status_code == 200:
                print(f'{Fore.GREEN}{status_code}: {target_url}{Style.RESET_ALL}')
                if result_file:
                    result_file.write(f'{status_code}: {target_url}\n')
            elif not show_only_200:
                print(f'{Fore.RED}{status_code}: {target_url}{Style.RESET_ALL}')

        if result_file:
            result_file.close()

    end_time = time.time()  # Registra o tempo de término
    execution_time = end_time - start_time
    print(f'Tempo de execução: {execution_time:.2f} segundos')

def main():
    parser = argparse.ArgumentParser(description='Simple URL Scanner')

    parser.add_argument('-u', '--url', required=True, help='Target URL')
    parser.add_argument('-w', '--wordlist', required=True, help='Wordlist file')
    parser.add_argument('-s', '--save', help='Save accessible URLs to a file (e.g., resultado.txt)')
    parser.add_argument('-c', '--code200', action='store_true', help='Show only URLs returning code 200')

    # Adicionando mensagem de ajuda personalizada
    examples = "Exemplos de comando:\n" \
               "python fuzz.py -u https://example.com -w wordlist.txt\n" \
               "python fuzz.py -u https://example.com -w wordlist.txt -s resultado.txt"
    parser.epilog = examples

    args = parser.parse_args()

    scan_url(args.url, args.wordlist, args.save, args.code200)

if __name__ == '__main__':
    main()
