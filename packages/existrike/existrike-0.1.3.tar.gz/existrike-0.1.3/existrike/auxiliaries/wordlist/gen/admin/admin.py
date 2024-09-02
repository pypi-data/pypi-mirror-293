import argparse
from colorama import Fore, Style, init

# Inicializa o colorama
init(autoreset=True)

def exibir_banner():
    banner = """
    .#####...#####....####...######..##..##.
    .##..##..##..##..##......##......###.##.
    .#####...##..##..##.###..####....##.###.
    .##..##..##..##..##..##..##......##..##.
    .##..##..#####....####...######..##..##.
    ........................................
             𝗕𝘆 𝗥𝗔𝗗𝗡𝗘𝗧𝟲𝟰
   """
    print(Fore.CYAN + banner)

def gerar_palavras_fixas():
    palavras_fixas = [
        "Admin", "admin", "P@ssw0rd", "admin@321", "Administrator",
        "admin@123", "admin@3214", "admin administrator", "adminpanel",
        "adm", "manage@123", "manage", "manager", "manage@321",
        "manage@3214", "manager@2023", "manage@2024", "manage@2022",
        "manage@2021", "123", "1234", "12345", "123456", "1234567",
        "12345678", "123456789"
    ]

    # Adicionar variações com primeira letra minúscula e maiúscula
    palavras_fixas_expandida = []
    for palavra in palavras_fixas:
        palavras_fixas_expandida.append(palavra.lower())
        palavras_fixas_expandida.append(palavra.capitalize())

    # Adicionar mais palavras comuns
    mais_palavras = [
        "password", "Password", "Passw0rd", "admin123", "Admin123",
        "root", "Root", "toor", "Toor", "guest", "Guest", "user", "User",
        "superuser", "Superuser", "adminadmin", "Adminadmin", "adminpass",
        "Adminpass", "rootpass", "Rootpass", "guestpass", "Guestpass"
    ]

    palavras_fixas_expandida.extend(mais_palavras)
    return palavras_fixas_expandida

def gerar_combinacoes_dinamicas(d):
    anos = [str(ano) for ano in range(2005, 2025)]
    sufixos = ["@421", "@123", "@1234", "@321", "@3214", "#421", "#123", "#1234", "#321", "#3214", "_421", "_123", "_1234", "_321", "_3214"]
    prefixes = ["!", "$", "%", "*"]
    suffixes = ["!"]
    palavras = [d.lower(), d.capitalize()]

    combinacoes = set()
    for palavra in palavras:
        combinacoes.add(palavra)
        for sufixo in sufixos:
            combinacoes.add(palavra + sufixo)
        for prefix in prefixes:
            combinacoes.add(prefix + palavra)
        for suffix in suffixes:
            combinacoes.add(palavra + suffix)
        for ano in anos:
            combinacoes.add(palavra + ano)
            combinacoes.add(palavra + "@" + ano)
            combinacoes.add(palavra + "#" + ano)
            combinacoes.add(palavra + "_" + ano)
        combinacoes.add(palavra + "painel")
        combinacoes.add(palavra + "admin")
        combinacoes.add(palavra + "@painel")
        combinacoes.add(palavra + "@admin")
        combinacoes.add(palavra + "#painel")
        combinacoes.add(palavra + "#admin")
        combinacoes.add(palavra + "_painel")
        combinacoes.add(palavra + "_admin")

    return combinacoes

def gerar_wordlist(dados, arquivo_saida, exibir=False):
    palavras_fixas = gerar_palavras_fixas()
    combinacoes_dinamicas = gerar_combinacoes_dinamicas(dados)

    wordlist = set(palavras_fixas) | combinacoes_dinamicas

    with open(arquivo_saida, 'w') as f:
        for palavra in sorted(wordlist):
            f.write(palavra + '\n')
            if exibir:
                print(Fore.GREEN + palavra)

if __name__ == "__main__":
    exibir_banner()

    parser = argparse.ArgumentParser(description="Gerador de Wordlist")
    parser.add_argument('-d', '--dados', required=True, help="Dados dinâmicos para gerar combinações")
    parser.add_argument('-o', '--output', default='wordlist.txt', help="Nome do arquivo de saída (padrão: wordlist.txt)")
    parser.add_argument('-i', '--invisivel', action='store_true', help="Salva a wordlist sem exibi-la na tela")
    args = parser.parse_args()

    print(Fore.YELLOW + f"generating wordlist to username: {args.dados}")
    print(Fore.YELLOW + f"saved on wordlist.txt")
    gerar_wordlist(args.dados, args.output, not args.invisivel)
    print(Fore.CYAN + "Wordlist as been generated!")
