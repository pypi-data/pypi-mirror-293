import requests
import re
import argparse
import json
import csv
import logging

# Configuração do Logger
logging.basicConfig(filename='fuzzer.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def fuzz(url, wordlist, method='GET', headers=None, params=None, data=None, json_data=None, regex=None, ssl_verify=True, check_status=False):
    with open(wordlist, 'r') as wl:
        words = wl.read().splitlines()

    results = []

    for word in words:
        fuzzed_url = url.replace('FUZZ', word)
        try:
            if method.upper() == 'GET':
                response = requests.get(fuzzed_url, headers=headers, params=params, verify=ssl_verify)
            elif method.upper() == 'POST':
                response = requests.post(fuzzed_url, headers=headers, data=data, json=json_data, verify=ssl_verify)
            elif method.upper() == 'PUT':
                response = requests.put(fuzzed_url, headers=headers, data=data, json=json_data, verify=ssl_verify)
            elif method.upper() == 'DELETE':
                response = requests.delete(fuzzed_url, headers=headers, verify=ssl_verify)
            else:
                print(f"HTTP method {method} not supported.")
                continue

            if check_status and response.status_code != 200:
                continue

            if regex:
                matches = re.findall(regex, response.text)
                if matches:
                    result = {'url': fuzzed_url, 'matches': matches}
                    results.append(result)
                    logging.info(f"URL: {fuzzed_url} - Matches: {matches}")
            else:
                if response.status_code == 200:
                    result = {'url': fuzzed_url, 'status_code': response.status_code}
                    results.append(result)
                    logging.info(f"URL: {fuzzed_url} - Status Code: {response.status_code}")

        except requests.RequestException as e:
            logging.error(f"Error with URL {fuzzed_url}: {e}")

    return results

def save_results(results, output_format):
    if output_format == 'json':
        with open('fuzz_results.json', 'w') as json_file:
            json.dump(results, json_file, indent=4)
    elif output_format == 'csv':
        with open('fuzz_results.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=['url', 'matches'])
            writer.writeheader()
            for result in results:
                writer.writerow(result)
    else:
        for result in results:
            print(result)

def print_results(results):
    for result in results:
        url = f"\033[92m{result['url']}\033[0m"
        if 'matches' in result:
            matches = ', '.join(result['matches'])
            matches_colored = f"\033[93m{matches}\033[0m"
            print(f"URL: {url} - Matches: {matches_colored}")
        elif 'status_code' in result:
            status_code = result['status_code']
            print(f"URL: {url} - Status Code: {status_code}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Advanced Fuzzer with Regex Support')
    parser.add_argument('-u', '--url', type=str, required=True, help='URL with FUZZ keyword where fuzzing will be performed')
    parser.add_argument('-w', '--wordlist', type=str, required=True, help='Wordlist for fuzzing')
    parser.add_argument('-m', '--method', type=str, default='GET', help='HTTP method to use (GET, POST, PUT, DELETE)')
    parser.add_argument('-H', '--headers', type=str, help='Headers for the request')
    parser.add_argument('-p', '--params', type=str, help='Query parameters for the request')
    parser.add_argument('-d', '--data', type=str, help='Form data for POST/PUT requests')
    parser.add_argument('-j', '--json_data', type=str, help='JSON data for POST/PUT requests')
    parser.add_argument('-r', '--regex', type=str, help='Regex pattern to match in the response')
    parser.add_argument('-s', '--ssl_verify', type=bool, default=True, help='Whether to verify SSL certificates')
    parser.add_argument('-o', '--output', type=str, help='Output format (json, csv)')
    parser.add_argument('-c', '--check_status', action='store_true', help='Check only URLs with status code 200')

    args = parser.parse_args()

    headers = None
    if args.headers:
        headers = {k.strip(): v.strip() for k, v in [h.split(':') for h in args.headers.split(',')]}

    params = None
    if args.params:
        params = {k.strip(): v.strip() for k, v in [p.split('=') for p in args.params.split('&')]}

    json_data = None
    if args.json_data:
        json_data = json.loads(args.json_data)

    results = fuzz(args.url, args.wordlist, method=args.method, headers=headers, params=params, data=args.data, json_data=json_data, regex=args.regex, ssl_verify=args.ssl_verify, check_status=args.check_status)

    if args.output:
        save_results(results, args.output)
    else:
        print_results(results)
