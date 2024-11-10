import random
import string
import requests
import os
import time
from pystyle import Colors, Colorate

def generate_device_id():
    characters = string.ascii_lowercase + string.digits
    parts = ["".join(random.choices(characters, k=8)), 
             "".join(random.choices(characters, k=4)), 
             "".join(random.choices(characters, k=4)), 
             "".join(random.choices(characters, k=4)), 
             "".join(random.choices(characters, k=12))]
    return "-".join(parts)

def get_random_user_agent():
    with open('user-agents.txt', 'r') as file:
        user_agents = file.readlines()
    return random.choice(user_agents).strip()

def send_message():
    os.system('clear')
    
    ascii_art = Colorate.Horizontal(Colors.red_to_purple, """
  █████▒██▓    ▄▄▄        ██████  ██░ ██  ██▓███   ██▓ ███▄    █   ▄████ 
▓██   ▒▓██▒   ▒████▄    ▒██    ▒ ▓██░ ██▒▓██░  ██▒▓██▒ ██ ▀█   █  ██▒ ▀█▒
▒████ ░▒██░   ▒██  ▀█▄  ░ ▓██▄   ▒██▀▀██░▓██░ ██▓▒▒██▒▓██  ▀█ ██▒▒██░▄▄▄░
░▓█▒  ░▒██░   ░██▄▄▄▄██   ▒   ██▒░▓█ ░██ ▒██▄█▓▒ ▒░██░▓██▒  ▐▌██▒░▓█  ██▓
░▒█░   ░██████▒▓█   ▓██▒▒██████▒▒░▓█▒░██▓▒██▒ ░  ░░██░▒██░   ▓██░░▒▓███▀▒
 ▒ ░   ░ ▒░▓  ░▒▒   ▓▒█░▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒▒▓▒░ ░  ░░▓  ░ ▒░   ▒ ▒  ░▒   ▒ 
 ░     ░ ░ ▒  ░ ▒   ▒▒ ░░ ░▒  ░ ░ ▒ ░▒░ ░░▒ ░      ▒ ░░ ░░   ░ ░░  ░   ░ 
 ░ ░     ░ ░    ░   ░  ░      ░   ░  ░░ ░░░        ░           ░       ░ 
    """)
    
    print(ascii_art)

    ngl_username = input(Colors.blue + "Username: " + Colors.reset)
    message = input(Colors.green + "Message: " + Colors.reset)
    count = int(input(Colors.red + "Count: " + Colors.reset))
    delay = float(input(Colors.purple + "Delay (enter 0 for fastest): " + Colors.reset))

    success_count = 0
    consecutive_failures = 0

    for i in range(count):
        headers = {
            'Host': 'ngl.link',
            'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'accept': '*/*',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'x-requested-with': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'user-agent': get_random_user_agent(),
            'sec-ch-ua-platform': '"Windows"',
            'origin': 'https://ngl.link',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': f'https://ngl.link/{ngl_username}',
            'accept-language': 'en-US,en;q=0.9'
        }

        data = {
            'username': ngl_username,
            'question': message,
            'deviceId': generate_device_id(),
            'gameSlug': '',
            'referrer': ''
        }

        try:
            response = requests.post('https://ngl.link/api/submit', headers=headers, data=data)
            if response.status_code == 200:
                success_count += 1
                consecutive_failures = 0
                print(Colors.green + f"Message {success_count} sent successfully." + Colors.reset)
            else:
                consecutive_failures += 1
                print(Colors.red + f"Failed to send message {i + 1}, status code: {response.status_code}" + Colors.reset)

            if consecutive_failures >= 4:
                print(Colors.yellow + "Changing User-Agent and Device ID." + Colors.reset)
                consecutive_failures = 0

            time.sleep(delay)

        except requests.exceptions.RequestException as e:
            print(Colors.red + "Request error:", e + Colors.reset)

    print(Colors.cyan + f"\nTotal messages sent successfully: {success_count}" + Colors.reset)

if __name__ == "__main__":
    send_message()