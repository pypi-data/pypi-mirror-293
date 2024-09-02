import argparse
import aiohttp
import asyncio
import time

# Sequências ANSI para cores
ansi_reset = "\033[0m"
ansi_green = "\033[92m"
ansi_red = "\033[91m"

async def fetch(session, url, result_file):
    try:
        async with session.get(url) as response:
            status_code = response.status
            if status_code == 200:
                print(f"[{ansi_green}200{ansi_reset}] {url}")
                if result_file:
                    result_file.write(f"[200] {url}\n")
    except aiohttp.ClientError:
        pass  # Ignora erros de conexão

async def scan_subdomains(base_domain, wordlist_lines, result_file, max_threads):
    connector = aiohttp.TCPConnector(limit_per_host=max_threads)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        for line in wordlist_lines:
            subdomain = line.strip()
            target_url = f'https://{subdomain}.{base_domain}'
            task = asyncio.create_task(fetch(session, target_url, result_file))
            tasks.append(task)
            # Limitar o número de tarefas em execução simultaneamente
            if len(tasks) >= max_threads:
                await asyncio.gather(*tasks)
                tasks = []
        if tasks:
            await asyncio.gather(*tasks)

def main():
    parser = argparse.ArgumentParser(description='Simple Subdomain Scanner')

    parser.add_argument('-d', '--domain', required=True, help='Base domain (e.g., example.com)')
    parser.add_argument('-w', '--wordlist', required=True, help='Wordlist file with subdomains')
    parser.add_argument('-s', '--save', help='Save accessible subdomains to a file (e.g., resultado.txt)')
    parser.add_argument('-c', '--code200', action='store_true', help='Show only subdomains returning code 200')
    parser.add_argument('-t', '--threads', type=int, default=100, help='Number of concurrent threads (default: 100)')

    args = parser.parse_args()

    # Banner em vermelho
    banner = (
        f"{ansi_red}        .     .                     \n"
        f"        |     |               o     \n"
        f",-. . . |-. ,-| ,-. ;-.-. ,-: . ;-. \n"
        f"`-. | | | | | | | | | | | | | | | | \n"
        f"`-' `-` `-' `-' `-' ' ' ' `-` ' ' ' \n"
        f"       𝗕𝘆 𝗥𝗔𝗗𝗡𝗘𝗧𝟲𝟰        \n"
        f"                                    {ansi_reset}\n"
    )

    print(banner)

    with open(args.wordlist, 'r') as wordlist:
        wordlist_lines = wordlist.readlines()

    if args.save:
        result_file = open(args.save, 'w')
    else:
        result_file = None

    start_time = time.time()  # Registra o tempo de início

    asyncio.run(scan_subdomains(args.domain, wordlist_lines, result_file, args.threads))

    if result_file:
        result_file.close()

    end_time = time.time()  # Registra o tempo de término
    execution_time = end_time - start_time
    print(f'Tempo de execução: {execution_time:.2f} segundos')

if __name__ == '__main__':
    main()
