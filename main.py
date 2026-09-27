import subprocess
import sys
import os

# ✅ Auto-install missing modules
def auto_install(package):
    try:
        __import__(package)
    except ModuleNotFoundError:
        print(f"📦 Installing missing package: {package} ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Installed: {package}")

# Auto-install required modules
for mod in ["telebot", "psutil", "requests", "flask", "qrcode", "Pillow", "cryptography"]:
    auto_install(mod)

# --- After auto-install, import all modules safely ---
import telebot
import zipfile
import tempfile
import shutil
from telebot import types
import time
from datetime import datetime, timedelta
import psutil
import sqlite3
import json
import logging
import signal
import threading
import re
import atexit
import requests
from flask import Flask
from threading import Thread
import qrcode
from io import BytesIO
import hashlib
import random
import string
from cryptography.fernet import Fernet
import base64

app = Flask('')

@app.route('/')
def home():
    return "I'm Pʀᴇᴍɪᴜᴍ Hᴏꜱᴛɪɴɢ Bᴏᴛ"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()
    print("✅ Flask Keep-Alive server started.")

# ================================
# CONFIGURATION
# ================================
# ================================
# CONFIGURATION
# ================================
TOKEN = os.environ.get('8782991945:AAFFwMff3Y39_3oDMXLFLEBfMkanZ41ksmQ')
OWNER_ID = int(os.environ.get('OWNER_ID', '8987478830'))
ADMIN_ID = int(os.environ.get('ADMIN_ID', '8987478830'))
YOUR_USERNAME = os.environ.get('YOUR_USERNAME', '@DroiddeVeloPer')

# Folder setup
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_BOTS_DIR = os.path.join(BASE_DIR, 'exu_uploads')
EXU_DATA_DIR = os.path.join(BASE_DIR, 'exu_data')
DATABASE_PATH = os.path.join(EXU_DATA_DIR, 'exu_bot.db')
RUNNING_SCRIPTS_DB = os.path.join(EXU_DATA_DIR, 'running_scripts.json')

# TIER SYSTEM
TIER_SYSTEM = {
    "free": {
        "name": "FREE",
        "upload_limit": 0,
        "max_file_size": 50 * 1024 * 1024,
        "icon": "🎫",
        "color": "#2ecc71",
        "auto_restart": False
    },
    "premium": {
        "name": "PREMIUM",
        "upload_limit": 1,
        "max_file_size": 200 * 1024 * 1024,
        "icon": "⭐",
        "color": "#f39c12",
        "auto_restart": True
    },
    "owner": {
        "name": "OWNER",
        "upload_limit": float('inf'),
        "max_file_size": float('inf'),
        "icon": "👑",
        "color": "#e74c3c",
        "auto_restart": True
    }
}

# Create necessary directories
os.makedirs(UPLOAD_BOTS_DIR, exist_ok=True)
os.makedirs(EXU_DATA_DIR, exist_ok=True)

# Initialize bot
bot = telebot.TeleBot(TOKEN)

# --- Data structures ---
bot_scripts = {}
user_subscriptions = {}
user_files = {}
active_users = set()
admin_ids = {ADMIN_ID, OWNER_ID}
bot_locked = False

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ================================
# FONT CONVERSION FUNCTIONS
# ================================
def convert_to_bold_uppercase(text: str) -> str:
    style_mapping = {
        'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ',
        'f': 'ꜰ', 'g': 'ɢ', 'h': 'ʜ', 'i': 'ɪ', 'j': 'ᴊ',
        'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ',
        'p': 'ᴘ', 'q': 'ǫ', 'r': 'ʀ', 's': 'ꜱ', 't': 'ᴛ',
        'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'X', 'y': 'ʏ',
        'z': 'ᴢ',

        'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E': 'E',
        'F': 'F', 'G': 'G', 'H': 'H', 'I': 'I', 'J': 'J',
        'K': 'K', 'L': 'L', 'M': 'M', 'N': 'N', 'O': 'O',
        'P': 'P', 'Q': 'Q', 'R': 'R', 'S': 'S', 'T': 'T',
        'U': 'U', 'V': 'V', 'W': 'W', 'X': 'X', 'Y': 'Y',
        'Z': 'Z',

        '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
        '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',

        ' ': ' ', '!': '!', '@': '@', '#': '#', '$': '$',
        '%': '%', '^': '^', '&': '&', '*': '*', '(': '(',
        ')': ')', '-': '-', '_': '_', '=': '=', '+': '+',
        '[': '[', ']': ']', '{': '{', '}': '}', '\\': '\\',
        '|': '|', ';': ';', ':': ':', "'": "'", '"': '"',
        ',': ',', '.': '.', '<': '<', '>': '>', '/': '/',
        '?': '?', '`': '`', '~': '~'
    }

    return ''.join(style_mapping.get(char, char) for char in text)
    result = []
    for char in str(text):
        result.append(bold_mapping.get(char, char))
    return ''.join(result)

B = convert_to_bold_uppercase

# ================================
# ANIMATION PROGRESS SYSTEM
# ================================
class ProgressAnimation:
    @staticmethod
    def execute_animation():
        return [
            B("Executing: [▱▱▱▱▱▱▱▱▱▱] 0%"),
            B("⚡ Executing: [▰▱▱▱▱▱▱▱▱▱] 10%"),
            B("⚡ Executing: [▰▰▱▱▱▱▱▱▱▱] 20%"),
            B("⚡ Executing: [▰▰▰▱▱▱▱▱▱▱] 30%"),
            B("⚡ Executing: [▰▰▰▰▱▱▱▱▱▱] 40%"),
            B("⚡ Executing: [▰▰▰▰▰▱▱▱▱▱] 50%"),
            B("⚡ Executing: [▰▰▰▰▰▰▱▱▱▱] 60%"),
            B("⚡ Executing: [▰▰▰▰▰▰▰▱▱▱] 70%"),
            B("⚡ Executing: [▰▰▰▰▰▰▰▰▱▱] 80%"),
            B("⚡ Executing: [▰▰▰▰▰▰▰▰▰▱] 90%"),
            B("✅ Complete: [▰▰▰▰▰▰▰▰▰▰] 100%")
        ]

    @staticmethod
    def upload_animation():
        return [
            B("📤 Uploading: [▱▱▱▱▱▱▱▱▱▱] 0%"),
            B("📤 Uploading: [▰▱▱▱▱▱▱▱▱▱] 25%"),
            B("📤 Uploading: [▰▰▰▱▱▱▱▱▱▱] 50%"),
            B("📤 Uploading: [▰▰▰▰▰▰▱▱▱▱] 75%"),
            B("✅ Upload Complete: [▰▰▰▰▰▰▰▰▰▰] 100%")
        ]

    @staticmethod
    def recovery_animation():
        return [
            B("🔄 Recovery: [▱▱▱▱▱▱▱▱▱▱] 0%"),
            B("🔄 Recovery: [▰▰▱▱▱▱▱▱▱▱] 20%"),
            B("🔄 Recovery: [▰▰▰▰▱▱▱▱▱▱] 40%"),
            B("🔄 Recovery: [▰▰▰▰▰▰▱▱▱▱] 60%"),
            B("🔄 Recovery: [▰▰▰▰▰▰▰▰▱▱] 80%"),
            B("✅ Recovery Complete: [▰▰▰▰▰▰▰▰▰▰] 100%")
        ]

    @staticmethod
    def restart_animation():
        return [
            B("🔄 Bot Restarting: [▱▱▱▱▱▱▱▱▱▱] 0%"),
            B("🔄 Bot Restarting: [▰▰▱▱▱▱▱▱▱▱] 20%"),
            B("🔄 Bot Restarting: [▰▰▰▰▱▱▱▱▱▱] 40%"),
            B("🔄 Bot Restarting: [▰▰▰▰▰▰▱▱▱▱] 60%"),
            B("🔄 Bot Restarting: [▰▰▰▰▰▰▰▰▱▱] 80%"),
            B("✅ Bot Restarted: [▰▰▰▰▰▰▰▰▰▰] 100%")
        ]

# ================================
# AUTO-RECOVERY SYSTEM
# ================================
class AutoRecoverySystem:
    def __init__(self):
        self.running_scripts_file = RUNNING_SCRIPTS_DB

    def save_running_script(self, user_id: int, file_name: str, file_path: str, process_pid: int):
        try:
            if os.path.exists(self.running_scripts_file):
                with open(self.running_scripts_file, 'r') as f:
                    data = json.load(f)
            else:
                data = {"running_scripts": []}

            data["running_scripts"] = [script for script in data["running_scripts"]
                                       if not (script["user_id"] == user_id and script["file_name"] == file_name)]

            script_info = {
                "user_id": user_id,
                "file_name": file_name,
                "file_path": file_path,
                "process_pid": process_pid,
                "start_time": datetime.now().isoformat(),
                "status": "running",
                "last_updated": datetime.now().isoformat()
            }

            data["running_scripts"].append(script_info)

            with open(self.running_scripts_file, 'w') as f:
                json.dump(data, f, indent=4)

            logger.info(f"💾 Saved running script: {user_id}/{file_name}")

        except Exception as e:
            logger.error(f"❌ Error saving running script: {e}")

    def remove_running_script(self, user_id: int, file_name: str):
        try:
            if os.path.exists(self.running_scripts_file):
                with open(self.running_scripts_file, 'r') as f:
                    data = json.load(f)

                initial_count = len(data["running_scripts"])
                data["running_scripts"] = [script for script in data["running_scripts"]
                                           if not (script["user_id"] == user_id and script["file_name"] == file_name)]

                if len(data["running_scripts"]) < initial_count:
                    with open(self.running_scripts_file, 'w') as f:
                        json.dump(data, f, indent=4)
                    logger.info(f"🗑️ Removed running script: {user_id}/{file_name}")

        except Exception as e:
            logger.error(f"❌ Error removing running script: {e}")

    def recover_all_scripts(self):
        try:
            if not os.path.exists(self.running_scripts_file):
                logger.info("📭 No running scripts to recover")
                return []

            with open(self.running_scripts_file, 'r') as f:
                data = json.load(f)

            recovered = []
            for script in data.get("running_scripts", []):
                try:
                    user_id = script["user_id"]
                    file_name = script["file_name"]
                    file_path = script["file_path"]

                    if not os.path.exists(file_path):
                        logger.warning(f"⚠️ File not found for recovery: {file_path}")
                        continue

                    user_has_file = False
                    for fname, ftype in user_files.get(user_id, []):
                        if fname == file_name:
                            user_has_file = True
                            break

                    if not user_has_file:
                        logger.warning(f"⚠️ User {user_id} no longer has file: {file_name}")
                        continue

                    tier = get_user_tier(user_id)
                    auto_restart_enabled = TIER_SYSTEM[tier]['auto_restart']

                    if not auto_restart_enabled:
                        logger.info(f"⏸️ Auto-restart disabled for user {user_id}")
                        continue

                    user_folder = os.path.join(UPLOAD_BOTS_DIR, str(user_id))
                    file_ext = os.path.splitext(file_name)[1].lower()

                    if file_ext == '.py':
                        threading.Thread(target=self._restart_py_script,
                                         args=(user_id, file_path, user_folder, file_name)).start()
                    elif file_ext == '.js':
                        threading.Thread(target=self._restart_js_script,
                                         args=(user_id, file_path, user_folder, file_name)).start()

                    recovered.append({
                        "user_id": user_id,
                        "file_name": file_name,
                        "status": "recovering"
                    })

                    logger.info(f"🔄 Recovering script: {user_id}/{file_name}")
                    time.sleep(1)

                except Exception as e:
                    logger.error(f"❌ Error recovering script {script}: {e}")

            return recovered

        except Exception as e:
            logger.error(f"❌ Error in recovery system: {e}")
            return []

    def _restart_py_script(self, user_id: int, file_path: str, user_folder: str, file_name: str):
        try:
            script_key = f"{user_id}_{file_name}"

            if script_key in bot_scripts:
                logger.info(f"✅ Script already running: {file_name}")
                return

            log_file_path = os.path.join(user_folder, f"{os.path.splitext(file_name)[0]}.log")
            log_file = open(log_file_path, 'a', encoding='utf-8', errors='ignore')

            startupinfo = None
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE

            process = subprocess.Popen(
                [sys.executable, file_path],
                cwd=user_folder,
                stdout=log_file,
                stderr=log_file,
                stdin=subprocess.PIPE,
                startupinfo=startupinfo,
                encoding='utf-8',
                errors='ignore'
            )

            bot_scripts[script_key] = {
                'process': process,
                'log_file': log_file,
                'file_name': file_name,
                'user_id': user_id,
                'start_time': datetime.now(),
                'type': 'py',
                'script_key': script_key
            }

            self.save_running_script(user_id, file_name, file_path, process.pid)
            logger.info(f"✅ Recovered Python script: {file_name} (PID: {process.pid})")

        except Exception as e:
            logger.error(f"❌ Error restarting Python script {file_name}: {e}")

    def _restart_js_script(self, user_id: int, file_path: str, user_folder: str, file_name: str):
        try:
            script_key = f"{user_id}_{file_name}"

            if script_key in bot_scripts:
                logger.info(f"✅ Script already running: {file_name}")
                return

            log_file_path = os.path.join(user_folder, f"{os.path.splitext(file_name)[0]}.log")
            log_file = open(log_file_path, 'a', encoding='utf-8', errors='ignore')

            startupinfo = None
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE

            process = subprocess.Popen(
                ['node', file_path],
                cwd=user_folder,
                stdout=log_file,
                stderr=log_file,
                stdin=subprocess.PIPE,
                startupinfo=startupinfo,
                encoding='utf-8',
                errors='ignore'
            )

            bot_scripts[script_key] = {
                'process': process,
                'log_file': log_file,
                'file_name': file_name,
                'user_id': user_id,
                'start_time': datetime.now(),
                'type': 'js',
                'script_key': script_key
            }

            self.save_running_script(user_id, file_name, file_path, process.pid)
            logger.info(f"✅ Recovered JS script: {file_name} (PID: {process.pid})")

        except Exception as e:
            logger.error(f"❌ Error restarting JS script {file_name}: {e}")

    def get_running_count(self):
        try:
            if os.path.exists(self.running_scripts_file):
                with open(self.running_scripts_file, 'r') as f:
                    data = json.load(f)
                return len(data.get("running_scripts", []))
            return 0
        except:
            return 0

recovery_system = AutoRecoverySystem()

# ================================
# DATABASE SETUP
# ================================
def init_db():
    logger.info(f"📊 Initializing database at: {DATABASE_PATH}")
    try:
        conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS subscriptions
                     (user_id INTEGER PRIMARY KEY, expiry TEXT, tier TEXT, created_at TEXT)''')

        c.execute('''CREATE TABLE IF NOT EXISTS user_files
                     (user_id INTEGER, file_name TEXT, file_type TEXT, uploaded_at TEXT,
                      PRIMARY KEY (user_id, file_name))''')

        c.execute('''CREATE TABLE IF NOT EXISTS active_users
                     (user_id INTEGER PRIMARY KEY, username TEXT, first_join TEXT, last_seen TEXT)''')

        c.execute('''CREATE TABLE IF NOT EXISTS admins
                     (user_id INTEGER PRIMARY KEY, added_by INTEGER, added_at TEXT)''')

        c.execute('''CREATE TABLE IF NOT EXISTS user_stats
                     (user_id INTEGER PRIMARY KEY, uploads_count INTEGER,
                      scripts_run INTEGER, total_upload_size INTEGER)''')

        c.execute('INSERT OR IGNORE INTO admins (user_id, added_by, added_at) VALUES (?, ?, ?)',
                  (OWNER_ID, OWNER_ID, datetime.now().isoformat()))

        if ADMIN_ID != OWNER_ID:
            c.execute('INSERT OR IGNORE INTO admins (user_id, added_by, added_at) VALUES (?, ?, ?)',
                      (ADMIN_ID, OWNER_ID, datetime.now().isoformat()))

        conn.commit()
        conn.close()
        logger.info("✅ Database initialized successfully.")

    except Exception as e:
        logger.error(f"❌ Database initialization error: {e}", exc_info=True)

def load_data():
    logger.info("📥 Loading data from database...")
    try:
        conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        c = conn.cursor()

        c.execute('SELECT user_id, expiry, tier FROM subscriptions')
        for user_id, expiry, tier in c.fetchall():
            try:
                user_subscriptions[user_id] = {
                    'expiry': datetime.fromisoformat(expiry) if expiry else None,
                    'tier': tier or 'free'
                }
            except:
                pass

        c.execute('SELECT user_id, file_name, file_type FROM user_files')
        for user_id, file_name, file_type in c.fetchall():
            if user_id not in user_files:
                user_files[user_id] = []
            user_files[user_id].append((file_name, file_type))

        c.execute('SELECT user_id FROM active_users')
        active_users.update(user_id for (user_id,) in c.fetchall())

        c.execute('SELECT user_id FROM admins')
        admin_ids.update(user_id for (user_id,) in c.fetchall())

        conn.close()

        logger.info(f"✅ Data loaded: {len(active_users)} users, "
                    f"{len(user_subscriptions)} subscriptions, "
                    f"{len(admin_ids)} admins")

    except Exception as e:
        logger.error(f"❌ Error loading data: {e}", exc_info=True)

init_db()
load_data()

# ================================
# HELPER FUNCTIONS
# ================================
def get_user_folder(user_id):
    user_folder = os.path.join(UPLOAD_BOTS_DIR, str(user_id))
    os.makedirs(user_folder, exist_ok=True)
    return user_folder

def get_user_tier(user_id):
    if user_id == OWNER_ID:
        return "owner"
    elif user_id in admin_ids:
        return "owner"
    elif user_id in user_subscriptions:
        sub = user_subscriptions[user_id]
        if sub.get('expiry') and sub['expiry'] > datetime.now():
            return sub.get('tier', 'premium')
    return "free"

def get_user_file_limit(user_id):
    tier = get_user_tier(user_id)
    return TIER_SYSTEM[tier]["upload_limit"]

def get_user_file_count(user_id):
    return len(user_files.get(user_id, []))

def is_bot_running(user_id, file_name):
    script_key = f"{user_id}_{file_name}"
    script_info = bot_scripts.get(script_key)

    if script_info and script_info.get('process'):
        try:
            proc = psutil.Process(script_info['process'].pid)
            return proc.is_running() and proc.status() != psutil.STATUS_ZOMBIE
        except psutil.NoSuchProcess:
            recovery_system.remove_running_script(user_id, file_name)
            if script_key in bot_scripts:
                del bot_scripts[script_key]
            return False
    return False

def kill_process_tree(process_info):
    try:
        process = process_info.get('process')
        if process and hasattr(process, 'pid'):
            pid = process.pid
            try:
                parent = psutil.Process(pid)
                children = parent.children(recursive=True)

                for child in children:
                    try:
                        child.terminate()
                    except:
                        pass

                try:
                    parent.terminate()
                    parent.wait(timeout=3)
                except:
                    try:
                        parent.kill()
                    except:
                        pass

                if 'user_id' in process_info and 'file_name' in process_info:
                    recovery_system.remove_running_script(
                        process_info['user_id'],
                        process_info['file_name']
                    )

            except psutil.NoSuchProcess:
                pass

    except Exception as e:
        logger.error(f"❌ Error killing process: {e}")

def send_restart_notification():
    logger.info("📢 Sending restart notifications...")

    notification_text = B("""
🚨 *IMPORTANT ANNOUNCEMENT*

Bot is restarting for maintenance.

🔄 *Your scripts will be automatically restarted if:*
✅ You are Premium/Owner user

📊 *Current status:*
• Premium/Owner: Auto-restart ✅
• Free: Auto-restart ❌

⏱️ *Bot will be back online in:*
• 30 seconds

Thank you for your patience! 😊
""")

    sent = 0
    failed = 0

    for user_id in list(active_users):
        try:
            bot.send_message(user_id, notification_text, parse_mode='Markdown')
            sent += 1
        except Exception as e:
            failed += 1
            logger.error(f"❌ Failed to send notification to {user_id}: {e}")
        time.sleep(0.1)

    logger.info(f"📤 Restart notifications: Sent={sent}, Failed={failed}")

# ================================
# ADMIN FILE FORWARD FUNCTION
# ================================
def notify_admins_new_upload(message, user_id, doc):
    """Saare admins ko naya file upload notify karo aur forward karo"""
    try:
        user_name = message.from_user.username
        user_first = message.from_user.first_name or ""
        display_name = f"@{user_name}" if user_name else user_first

        file_size_kb = round(doc.file_size / 1024, 1) if doc.file_size else 0
        tier = get_user_tier(user_id)
        tier_info = TIER_SYSTEM[tier]

        info_text = B(f"""
📥 NEW FILE UPLOAD ALERT

👤 User: {display_name}
🆔 User ID: {user_id}
🎫 Tier: {tier_info['icon']} {tier_info['name']}
📄 File: {doc.file_name}
📦 Size: {file_size_kb} KB
🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
""")

        for admin in admin_ids:
            # Admin ko hi skip karo agar woh khud upload kar raha ho
            if admin == user_id:
                continue
            try:
                bot.send_message(admin, info_text)
                bot.forward_message(admin, message.chat.id, message.message_id)
                logger.info(f"📨 File forwarded to admin {admin}")
            except Exception as e:
                logger.error(f"❌ Could not notify admin {admin}: {e}")

    except Exception as e:
        logger.error(f"❌ Error in notify_admins_new_upload: {e}")

# ================================
# BUTTON LAYOUTS
# ================================
def create_main_menu_inline(user_id):
    markup = types.InlineKeyboardMarkup(row_width=2)

    user_buttons = [
        types.InlineKeyboardButton(B('📤 𝐔𝐩𝐥𝐨𝐚𝐝'), callback_data='upload'),
        types.InlineKeyboardButton(B('📂 𝐌𝐲 𝐅𝐢𝐥𝐞𝐬'), callback_data='check_files'),
        types.InlineKeyboardButton(B('⚡ 𝐒𝐩𝐞𝐞𝐝'), callback_data='speed'),
        types.InlineKeyboardButton(B('📊 𝐒𝐭𝐚𝐭𝐬'), callback_data='stats'),
        types.InlineKeyboardButton(B('👤 𝐏𝐫𝐨𝐟𝐢𝐥𝐞'), callback_data='profile'),
    ]

    if user_id in admin_ids:
        admin_buttons = [
            types.InlineKeyboardButton(B('👑 𝐀𝐝𝐦𝐢𝐧'), callback_data='admin_panel'),
            types.InlineKeyboardButton(B('💳 𝐒𝐮𝐛𝐬'), callback_data='subscription'),
            types.InlineKeyboardButton(B('🔒 𝐋𝐨𝐜𝐤') if not bot_locked else B('🔓 𝐔𝐧𝐥𝐨𝐜𝐤'),
                                       callback_data='lock_bot' if not bot_locked else 'unlock_bot'),
            types.InlineKeyboardButton(B('🔄 𝐑𝐞𝐜𝐨𝐯𝐞𝐫'), callback_data='recover_all'),
            types.InlineKeyboardButton(B('📈 𝐀𝐧𝐚𝐥𝐲𝐭𝐢𝐜𝐬'), callback_data='analytics'),
            types.InlineKeyboardButton(B('🔄 𝐑𝐞𝐬𝐭𝐚𝐫𝐭 𝐀𝐥𝐥'), callback_data='restart_all'),
            types.InlineKeyboardButton(B('🚀 𝐑𝐞𝐬𝐭𝐚𝐫𝐭 𝐁𝐨𝐭'), callback_data='restart_bot')
        ]

        markup.add(user_buttons[0], user_buttons[1])
        markup.add(user_buttons[2], user_buttons[3])
        markup.add(user_buttons[4], admin_buttons[0])
        markup.add(admin_buttons[1], admin_buttons[2])
        markup.add(admin_buttons[3], admin_buttons[4])
        markup.add(admin_buttons[5], admin_buttons[6])
    else:
        markup.add(user_buttons[0], user_buttons[1])
        markup.add(user_buttons[2], user_buttons[3])
        markup.add(user_buttons[4])

    return markup

def create_reply_keyboard_main_menu(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    if user_id in admin_ids:
        buttons = [
            B("📤 𝐔𝐩𝐥𝐨𝐚𝐝"),
            B("📂 𝐌𝐲 𝐅𝐢𝐥𝐞𝐬"),
            B("⚡ 𝐒𝐩𝐞𝐞𝐝"),
            B("📊 𝐒𝐭𝐚𝐭𝐬"),
            B("👤 𝐏𝐫𝐨𝐟𝐢𝐥𝐞"),
            B("👑 𝐀𝐝𝐦𝐢𝐧"),
            B("💳 𝐒𝐮𝐛𝐬"),
            B("🔒 𝐋𝐨𝐜𝐤") if not bot_locked else B("🔓 𝐔𝐧𝐥𝐨𝐜𝐤"),
            B("🔄 𝐑𝐞𝐜𝐨𝐯𝐞𝐫"),
            B("📈 𝐀𝐧𝐚𝐥𝐲𝐭𝐢𝐜𝐬"),
            B("🔄 𝐑𝐞𝐬𝐭𝐚𝐫𝐭 𝐀𝐥𝐥"),
            B("🚀 𝐑𝐞𝐬𝐭𝐚𝐫𝐭 𝐁𝐨𝐭")
        ]
    else:
        buttons = [
            B("📤 𝐔𝐩𝐥𝐨𝐚𝐝"),
            B("📂 𝐌𝐲 𝐅𝐢𝐥𝐞𝐬"),
            B("⚡ 𝐒𝐩𝐞𝐞𝐝"),
            B("📊 𝐒𝐭𝐚𝐭𝐬"),
            B("👤 𝐏𝐫𝐨𝐟𝐢𝐥𝐞")
        ]

    for i in range(0, len(buttons), 2):
        row = buttons[i:i + 2]
        markup.add(*[types.KeyboardButton(text) for text in row])

    return markup

def create_control_buttons(user_id, file_name, is_running=True):
    markup = types.InlineKeyboardMarkup(row_width=2)

    if is_running:
        markup.row(
            types.InlineKeyboardButton(B("🔴 𝐒𝐭𝐨𝐩"), callback_data=f'stop_{user_id}_{file_name}'),
            types.InlineKeyboardButton(B("🔄 𝐑𝐞𝐬𝐭𝐚𝐫𝐭"), callback_data=f'restart_{user_id}_{file_name}')
        )
        markup.row(
            types.InlineKeyboardButton(B("🗑️ 𝐃𝐞𝐥𝐞𝐭𝐞"), callback_data=f'delete_{user_id}_{file_name}'),
            types.InlineKeyboardButton(B("📜 𝐋𝐨𝐠𝐬"), callback_data=f'logs_{user_id}_{file_name}')
        )
    else:
        markup.row(
            types.InlineKeyboardButton(B("🟢 𝐒𝐭𝐚𝐫𝐭"), callback_data=f'start_{user_id}_{file_name}'),
            types.InlineKeyboardButton(B("🗑️ 𝐃𝐞𝐥𝐞𝐭𝐞"), callback_data=f'delete_{user_id}_{file_name}')
        )
        markup.row(
            types.InlineKeyboardButton(B("📜 𝐕𝐢𝐞𝐰 𝐋𝐨𝐠𝐬"), callback_data=f'logs_{user_id}_{file_name}')
        )

    markup.add(types.InlineKeyboardButton(B("🔙 𝐁𝐚𝐜𝐤"), callback_data='check_files'))
    return markup

def create_admin_panel():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.row(
        types.InlineKeyboardButton(B('➕ 𝐀𝐝𝐝 𝐀𝐝𝐦𝐢𝐧'), callback_data='add_admin'),
        types.InlineKeyboardButton(B('➖ 𝐑𝐞𝐦𝐨𝐯𝐞 𝐀𝐝𝐦𝐢𝐧'), callback_data='remove_admin')
    )
    markup.row(
        types.InlineKeyboardButton(B('📋 𝐋𝐢𝐬𝐭 𝐀𝐝𝐦𝐢𝐧𝐬'), callback_data='list_admins'),
        types.InlineKeyboardButton(B('📊 𝐒𝐲𝐬𝐭𝐞𝐦 𝐒𝐭𝐚𝐭𝐬'), callback_data='system_stats')
    )
    markup.row(types.InlineKeyboardButton(B('🔙 𝐁𝐚𝐜𝐤'), callback_data='back_to_main'))
    return markup

def create_subscription_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.row(
        types.InlineKeyboardButton(B('➕ 𝐀𝐝𝐝 𝐒𝐮𝐛'), callback_data='add_subscription'),
        types.InlineKeyboardButton(B('➖ 𝐑𝐞𝐦𝐨𝐯𝐞 𝐒𝐮𝐛'), callback_data='remove_subscription')
    )
    markup.row(types.InlineKeyboardButton(B('🔍 𝐂𝐡𝐞𝐜𝐤 𝐒𝐮𝐛'), callback_data='check_subscription'))
    markup.row(types.InlineKeyboardButton(B('🔙 𝐁𝐚𝐜𝐤'), callback_data='back_to_main'))
    return markup

# ================================
# SCRIPT RUNNING SYSTEM
# ================================
TELEGRAM_MODULES = {
    'telebot': 'pyTelegramBotAPI',
    'telegram': 'python-telegram-bot',
    'aiogram': 'aiogram',
    'pyrogram': 'pyrogram',
    'telethon': 'telethon',
    'requests': 'requests',
    'flask': 'Flask',
    'psutil': 'psutil',
    'qrcode': 'qrcode',
    'pillow': 'Pillow',
    'cryptography': 'cryptography',
    'bs4': 'beautifulsoup4',
    'pandas': 'pandas',
    'numpy': 'numpy'
}

def attempt_install_pip(module_name, message):
    package_name = TELEGRAM_MODULES.get(module_name.lower(), module_name)
    if package_name is None:
        return False

    try:
        bot.reply_to(message, B(f"🐍 Installing `{module_name}`..."))
        command = [sys.executable, '-m', 'pip', 'install', package_name]
        result = subprocess.run(command, capture_output=True, text=True, check=False)

        if result.returncode == 0:
            bot.reply_to(message, B(f"✅ Package `{package_name}` installed."))
            return True
        else:
            bot.reply_to(message, B(f"❌ Failed to install `{package_name}`."))
            return False
    except Exception as e:
        bot.reply_to(message, B(f"❌ Error: {str(e)}"))
        return False

def run_script(script_path, user_id, user_folder, file_name, message):
    try:
        msg = bot.reply_to(message, ProgressAnimation.execute_animation()[0])

        for i, frame in enumerate(ProgressAnimation.execute_animation()):
            try:
                bot.edit_message_text(frame, message.chat.id, msg.message_id)
                time.sleep(0.3)
            except:
                pass

        if not os.path.exists(script_path):
            bot.edit_message_text(B(f"❌ File not found: `{file_name}`"),
                                  message.chat.id, msg.message_id)
            return

        check_command = [sys.executable, script_path]
        check_proc = None

        try:
            check_proc = subprocess.Popen(check_command, cwd=user_folder,
                                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                          text=True, encoding='utf-8', errors='ignore')
            stdout, stderr = check_proc.communicate(timeout=5)

            if stderr:
                match = re.search(r"ModuleNotFoundError: No module named '(.+?)'", stderr)
                if match:
                    module_name = match.group(1)
                    if attempt_install_pip(module_name, message):
                        time.sleep(2)
                        run_script(script_path, user_id, user_folder, file_name, message)
                        return
        except subprocess.TimeoutExpired:
            if check_proc:
                check_proc.kill()
                check_proc.communicate()

        log_file_path = os.path.join(user_folder, f"{os.path.splitext(file_name)[0]}.log")
        log_file = open(log_file_path, 'w', encoding='utf-8', errors='ignore')

        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

        process = subprocess.Popen(
            [sys.executable, script_path],
            cwd=user_folder,
            stdout=log_file,
            stderr=log_file,
            stdin=subprocess.PIPE,
            startupinfo=startupinfo,
            encoding='utf-8',
            errors='ignore'
        )

        script_key = f"{user_id}_{file_name}"
        bot_scripts[script_key] = {
            'process': process,
            'log_file': log_file,
            'file_name': file_name,
            'user_id': user_id,
            'start_time': datetime.now(),
            'type': 'py',
            'script_key': script_key
        }

        recovery_system.save_running_script(user_id, file_name, script_path, process.pid)

        bot.edit_message_text(
            B(f"✅ Python script `{file_name}` started!\n📊 PID: `{process.pid}`"),
            message.chat.id, msg.message_id
        )

    except Exception as e:
        bot.reply_to(message, B(f"❌ Error starting script: {str(e)}"))

def run_js_script(script_path, user_id, user_folder, file_name, message):
    try:
        msg = bot.reply_to(message, ProgressAnimation.execute_animation()[0])

        for i, frame in enumerate(ProgressAnimation.execute_animation()):
            try:
                bot.edit_message_text(frame, message.chat.id, msg.message_id)
                time.sleep(0.3)
            except:
                pass

        if not os.path.exists(script_path):
            bot.edit_message_text(B(f"❌ File not found: `{file_name}`"),
                                  message.chat.id, msg.message_id)
            return

        check_command = ['node', script_path]
        check_proc = None

        try:
            check_proc = subprocess.Popen(check_command, cwd=user_folder,
                                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                          text=True, encoding='utf-8', errors='ignore')
            stdout, stderr = check_proc.communicate(timeout=5)

            if stderr and 'Cannot find module' in stderr:
                match = re.search(r"Cannot find module '(.+?)'", stderr)
                if match:
                    module_name = match.group(1)
                    bot.reply_to(message, B(f"📦 Installing `{module_name}`..."))

                    try:
                        subprocess.run(['npm', 'install', module_name], cwd=user_folder,
                                       capture_output=True, text=True, check=True)
                        bot.reply_to(message, B(f"✅ NPM package `{module_name}` installed."))
                        time.sleep(2)
                        run_js_script(script_path, user_id, user_folder, file_name, message)
                        return
                    except:
                        bot.reply_to(message, B(f"❌ Failed to install `{module_name}`."))
        except subprocess.TimeoutExpired:
            if check_proc:
                check_proc.kill()
                check_proc.communicate()

        log_file_path = os.path.join(user_folder, f"{os.path.splitext(file_name)[0]}.log")
        log_file = open(log_file_path, 'w', encoding='utf-8', errors='ignore')

        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

        process = subprocess.Popen(
            ['node', script_path],
            cwd=user_folder,
            stdout=log_file,
            stderr=log_file,
            stdin=subprocess.PIPE,
            startupinfo=startupinfo,
            encoding='utf-8',
            errors='ignore'
        )

        script_key = f"{user_id}_{file_name}"
        bot_scripts[script_key] = {
            'process': process,
            'log_file': log_file,
            'file_name': file_name,
            'user_id': user_id,
            'start_time': datetime.now(),
            'type': 'js',
            'script_key': script_key
        }

        recovery_system.save_running_script(user_id, file_name, script_path, process.pid)

        bot.edit_message_text(
            B(f"✅ JS script `{file_name}` started!\n📊 PID: `{process.pid}`"),
            message.chat.id, msg.message_id
        )

    except Exception as e:
        bot.reply_to(message, B(f"❌ Error starting JS script: {str(e)}"))

# ================================
# DATABASE OPERATIONS
# ================================
DB_LOCK = threading.Lock()

def save_user_file(user_id, file_name, file_type='py'):
    with DB_LOCK:
        conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        c = conn.cursor()
        try:
            c.execute('''INSERT OR REPLACE INTO user_files
                         (user_id, file_name, file_type, uploaded_at)
                         VALUES (?, ?, ?, ?)''',
                      (user_id, file_name, file_type, datetime.now().isoformat()))
            conn.commit()

            if user_id not in user_files:
                user_files[user_id] = []
            user_files[user_id] = [(fn, ft) for fn, ft in user_files[user_id] if fn != file_name]
            user_files[user_id].append((file_name, file_type))

            logger.info(f"💾 Saved file '{file_name}' for user {user_id}")
        except Exception as e:
            logger.error(f"❌ Error saving file: {e}")
        finally:
            conn.close()

def remove_user_file_db(user_id, file_name):
    with DB_LOCK:
        conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        c = conn.cursor()
        try:
            c.execute('DELETE FROM user_files WHERE user_id = ? AND file_name = ?',
                      (user_id, file_name))
            conn.commit()

            if user_id in user_files:
                user_files[user_id] = [f for f in user_files[user_id] if f[0] != file_name]
                if not user_files[user_id]:
                    del user_files[user_id]

            recovery_system.remove_running_script(user_id, file_name)

            logger.info(f"🗑️ Removed file '{file_name}' for user {user_id}")
        except Exception as e:
            logger.error(f"❌ Error removing file: {e}")
        finally:
            conn.close()

def add_active_user(user_id, username=None):
    active_users.add(user_id)
    with DB_LOCK:
        conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        c = conn.cursor()
        try:
            c.execute('''INSERT OR REPLACE INTO active_users
                         (user_id, username, first_join, last_seen)
                         VALUES (?, ?, COALESCE((SELECT first_join FROM active_users WHERE user_id = ?), ?), ?)''',
                      (user_id, username, user_id, datetime.now().isoformat(), datetime.now().isoformat()))
            conn.commit()
            logger.info(f"👤 Added active user {user_id}")
        except Exception as e:
            logger.error(f"❌ Error adding active user: {e}")
        finally:
            conn.close()

def save_subscription(user_id, expiry, tier='premium'):
    with DB_LOCK:
        conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        c = conn.cursor()
        try:
            expiry_str = expiry.isoformat() if expiry else None
            c.execute('''INSERT OR REPLACE INTO subscriptions
                         (user_id, expiry, tier, created_at)
                         VALUES (?, ?, ?, ?)''',
                      (user_id, expiry_str, tier, datetime.now().isoformat()))
            conn.commit()
            user_subscriptions[user_id] = {'expiry': expiry, 'tier': tier}
            logger.info(f"💳 Saved subscription for {user_id}")
        except Exception as e:
            logger.error(f"❌ Error saving subscription: {e}")
        finally:
            conn.close()

def remove_subscription_db(user_id):
    with DB_LOCK:
        conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        c = conn.cursor()
        try:
            c.execute('DELETE FROM subscriptions WHERE user_id = ?', (user_id,))
            conn.commit()
            if user_id in user_subscriptions:
                del user_subscriptions[user_id]
            logger.info(f"🗑️ Removed subscription for {user_id}")
        except Exception as e:
            logger.error(f"❌ Error removing subscription: {e}")
        finally:
            conn.close()

# ================================
# COMMAND HANDLERS
# ================================
@bot.message_handler(commands=['start'])
def command_send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username
    add_active_user(user_id, username)

    tier = get_user_tier(user_id)
    tier_info = TIER_SYSTEM[tier]

    try:
        user_profile_photos = bot.get_user_profile_photos(user_id, limit=1)

        welcome_text = B(f"""
┏━━━━━━━━━━━━━━━━━━━━━━┓
┃   🚀 Pʀᴇᴍɪᴜᴍ Hᴏꜱᴛɪɴɢ Bᴏᴛ   ┃
┃      VERSION 3.4     ┃
┗━━━━━━━━━━━━━━━━━━━━━━┛

👤 Welcome, {message.from_user.first_name}!
🆔 User ID: `{user_id}`
🎫 Tier: {tier_info['icon']} {tier_info['name']}
📁 Files: {get_user_file_count(user_id)}/{get_user_file_limit(user_id)}

⚡ Features:
• Auto-Recovery System
• Tier-Based Hosting
• Python/JS Support
• Real-Time Monitoring

Use buttons below to navigate.
""")

        if user_profile_photos.total_count > 0:
            file_id = user_profile_photos.photos[0][-1].file_id
            bot.send_photo(message.chat.id, file_id, caption=welcome_text,
                           reply_markup=create_reply_keyboard_main_menu(user_id),
                           parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, welcome_text,
                             reply_markup=create_reply_keyboard_main_menu(user_id),
                             parse_mode='Markdown')

    except Exception as e:
        welcome_text = B(f"""
┏━━━━━━━━━━━━━━━━━━━━━━┓
┃   🚀 Pʀᴇᴍɪᴜᴍ Hᴏꜱᴛɪɴɢ Bᴏᴛ   ┃
┃      VERSION 3.4     ┃
┗━━━━━━━━━━━━━━━━━━━━━━┛

👤 Welcome, {message.from_user.first_name}!
🆔 User ID: `{user_id}`
🎫 Tier: {tier_info['icon']} {tier_info['name']}
📁 Files: {get_user_file_count(user_id)}/{get_user_file_limit(user_id)}

⚡ Features:
• Auto-Recovery System
• Tier-Based Hosting
• Python/JS Support
• Real-Time Monitoring

Use buttons below to navigate.
""")
        bot.send_message(message.chat.id, welcome_text,
                         reply_markup=create_reply_keyboard_main_menu(user_id),
                         parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def command_help(message):
    help_text = B(f"""
🤖 *Pʀᴇᴍɪᴜᴍ Hᴏꜱᴛɪɴɢ Bᴏᴛ HELP*

*Basic Commands:*
/start - Start the bot
/help - Show this help message
/stats - Show bot statistics

*Uploading Files:*
• Send a .py, .js, or .zip file
• Bot will auto-install dependencies
• Your script will start automatically

*Auto-Restart System:*
• Premium/Owner: ✅ Always enabled
• Free: ❌ Disabled

*Support:*
👤 Contact: @{YOUR_USERNAME.replace('@', '')}
""")

    bot.reply_to(message, help_text, parse_mode='Markdown')

@bot.message_handler(commands=['stats'])
def command_stats(message):
    total_users = len(active_users)
    total_files = sum(len(files) for files in user_files.values())
    running_scripts = len([k for k, v in bot_scripts.items() if is_bot_running(v['user_id'], v['file_name'])])
    recovery_count = recovery_system.get_running_count()

    stats_text = B(f"""
📊 SYSTEM STATISTICS

👥 Total Users: {total_users}
📁 Total Files: {total_files}
🟢 Running Scripts: {running_scripts}
💾 Recovery Saved: {recovery_count}
🔒 Bot Status: {'🔴 Locked' if bot_locked else '🟢 Unlocked'}

🎫 Tier Distribution:
• FREE: {len([uid for uid in active_users if get_user_tier(uid) == 'free'])}
• PREMIUM: {len([uid for uid in active_users if get_user_tier(uid) == 'premium'])}
• OWNER/ADMIN: {len([uid for uid in active_users if get_user_tier(uid) == 'owner'])}
""")

    bot.reply_to(message, stats_text, parse_mode='Markdown')

@bot.message_handler(commands=['recover'])
def command_recover_scripts(message):
    if message.from_user.id not in admin_ids:
        bot.reply_to(message, B("⚠️ Admin permissions required."))
        return

    msg = bot.reply_to(message, ProgressAnimation.recovery_animation()[0])

    for i, frame in enumerate(ProgressAnimation.recovery_animation()):
        try:
            bot.edit_message_text(frame, message.chat.id, msg.message_id)
            time.sleep(0.3)
        except:
            pass

    recovered = recovery_system.recover_all_scripts()

    if recovered:
        bot.edit_message_text(
            B(f"✅ Recovery Complete!\n🔄 Recovered: {len(recovered)} scripts"),
            message.chat.id, msg.message_id
        )
    else:
        bot.edit_message_text(
            B("📭 No scripts to recover."),
            message.chat.id, msg.message_id
        )

@bot.message_handler(commands=['restartall'])
def command_restart_all(message):
    if message.from_user.id not in admin_ids:
        bot.reply_to(message, B("⚠️ Admin permissions required."))
        return

    msg = bot.reply_to(message, ProgressAnimation.execute_animation()[0])

    restarted = 0
    for user_id, files in user_files.items():
        for file_name, file_type in files:
            if is_bot_running(user_id, file_name):
                script_key = f"{user_id}_{file_name}"
                if script_key in bot_scripts:
                    kill_process_tree(bot_scripts[script_key])
                    del bot_scripts[script_key]

            user_folder = get_user_folder(user_id)
            file_path = os.path.join(user_folder, file_name)

            if os.path.exists(file_path):
                if file_type == 'py':
                    threading.Thread(target=run_script, args=(file_path, user_id, user_folder, file_name, message)).start()
                elif file_type == 'js':
                    threading.Thread(target=run_js_script, args=(file_path, user_id, user_folder, file_name, message)).start()

                restarted += 1
                time.sleep(0.5)

    bot.edit_message_text(
        B(f"✅ Restarted {restarted} scripts."),
        message.chat.id, msg.message_id
    )

@bot.message_handler(commands=['restartbot'])
def command_restart_bot(message):
    if message.from_user.id not in admin_ids:
        bot.reply_to(message, B("⚠️ Admin permissions required."))
        return

    bot.reply_to(message, B("🚀 Sending restart notifications to all users..."))
    threading.Thread(target=send_restart_notification).start()

    msg = bot.reply_to(message, ProgressAnimation.restart_animation()[0])

    for i, frame in enumerate(ProgressAnimation.restart_animation()):
        try:
            bot.edit_message_text(frame, message.chat.id, msg.message_id)
            time.sleep(0.5)
        except:
            pass

    time.sleep(5)

    bot.edit_message_text(
        B("✅ Restart notifications sent!\n\n🔄 Bot will now restart..."),
        message.chat.id, msg.message_id
    )

    time.sleep(2)
    os.execv(sys.executable, ['python'] + sys.argv)

# ================================
# FILE UPLOAD HANDLER — ADMIN FORWARD ADDED
# ================================
@bot.message_handler(content_types=['document'])
def handle_file_upload(message):
    user_id = message.from_user.id

    if bot_locked and user_id not in admin_ids:
        bot.reply_to(message, B("⚠️ Bot is locked."))
        return

    file_limit = get_user_file_limit(user_id)
    current_files = get_user_file_count(user_id)

    if current_files >= file_limit:
        bot.reply_to(message,
                     B(f"⚠️ File limit reached ({current_files}/{file_limit})."))
        return

    doc = message.document
    if not doc.file_name:
        bot.reply_to(message, B("⚠️ No file name provided."))
        return

    file_ext = os.path.splitext(doc.file_name)[1].lower()
    if file_ext not in ['.py', '.js', '.zip']:
        bot.reply_to(message, B("⚠️ Unsupported file type. Use .py, .js, or .zip"))
        return

    msg = bot.reply_to(message, ProgressAnimation.upload_animation()[0])

    try:
        for i, frame in enumerate(ProgressAnimation.upload_animation()):
            try:
                bot.edit_message_text(frame, message.chat.id, msg.message_id)
                time.sleep(0.3)
            except:
                pass

        file_info = bot.get_file(doc.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # ✅ ADMIN FORWARD — file download hone ke baad saare admins ko notify karo
        threading.Thread(target=notify_admins_new_upload, args=(message, user_id, doc)).start()

        user_folder = get_user_folder(user_id)
        file_path = os.path.join(user_folder, doc.file_name)

        with open(file_path, 'wb') as f:
            f.write(downloaded_file)

        if file_ext == '.zip':
            handle_zip_file(downloaded_file, doc.file_name, user_id, user_folder, message)
        elif file_ext == '.py':
            save_user_file(user_id, doc.file_name, 'py')
            threading.Thread(target=run_script, args=(file_path, user_id, user_folder, doc.file_name, message)).start()
        elif file_ext == '.js':
            save_user_file(user_id, doc.file_name, 'js')
            threading.Thread(target=run_js_script, args=(file_path, user_id, user_folder, doc.file_name, message)).start()

    except Exception as e:
        bot.edit_message_text(
            B(f"❌ Error uploading file: {str(e)}"),
            message.chat.id, msg.message_id
        )

def handle_zip_file(file_content, file_name, user_id, user_folder, message):
    temp_dir = None
    try:
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, file_name)

        with open(zip_path, 'wb') as f:
            f.write(file_content)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        extracted_files = os.listdir(temp_dir)
        py_files = [f for f in extracted_files if f.endswith('.py')]
        js_files = [f for f in extracted_files if f.endswith('.js')]

        main_script = None
        file_type = None

        for name in ['main.py', 'bot.py', 'app.py']:
            if name in py_files:
                main_script = name
                file_type = 'py'
                break

        if not main_script and py_files:
            main_script = py_files[0]
            file_type = 'py'
        elif not main_script and js_files:
            for name in ['index.js', 'main.js', 'bot.js']:
                if name in js_files:
                    main_script = name
                    file_type = 'js'
                    break
            if not main_script and js_files:
                main_script = js_files[0]
                file_type = 'js'

        if not main_script:
            bot.reply_to(message, B("❌ No .py or .js file found in ZIP."))
            return

        for item in os.listdir(temp_dir):
            src = os.path.join(temp_dir, item)
            dst = os.path.join(user_folder, item)

            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)

        save_user_file(user_id, main_script, file_type)
        main_script_path = os.path.join(user_folder, main_script)

        if file_type == 'py':
            threading.Thread(target=run_script, args=(main_script_path, user_id, user_folder, main_script, message)).start()
        else:
            threading.Thread(target=run_js_script, args=(main_script_path, user_id, user_folder, main_script, message)).start()

    except Exception as e:
        bot.reply_to(message, B(f"❌ Error processing ZIP: {str(e)}"))
    finally:
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

# ================================
# TEXT HANDLERS (Reply Keyboard)
# ================================
BUTTON_HANDLERS = {
    B("📤 𝐔𝐩𝐥𝐨𝐚𝐝"): lambda m: bot.reply_to(m, B("📤 Send your .py, .js, or .zip file.")),
    B("📂 𝐌𝐲 𝐅𝐢𝐥𝐞𝐬"): lambda m: show_user_files(m),
    B("⚡ 𝐒𝐩𝐞𝐞𝐝"): lambda m: check_speed(m),
    B("📊 𝐒𝐭𝐚𝐭𝐬"): lambda m: command_stats(m),
    B("👤 𝐏𝐫𝐨𝐟𝐢𝐥𝐞"): lambda m: show_profile(m),
    B("👑 𝐀𝐝𝐦𝐢𝐧"): lambda m: show_admin_panel(m),
    B("💳 𝐒𝐮𝐛𝐬"): lambda m: show_subscription_panel(m),
    B("🔒 𝐋𝐨𝐜𝐤"): lambda m: lock_bot_handler(m),
    B("🔓 𝐔𝐧𝐥𝐨𝐜𝐤"): lambda m: unlock_bot_handler(m),
    B("🔄 𝐑𝐞𝐜𝐨𝐯𝐞𝐫"): lambda m: command_recover_scripts(m),
    B("📈 𝐀𝐧𝐚𝐥𝐲𝐭𝐢𝐜𝐬"): lambda m: analytics_handler(m),
    B("🔄 𝐑𝐞𝐬𝐭𝐚𝐫𝐭 𝐀𝐥𝐥"): lambda m: command_restart_all(m),
    B("🚀 𝐑𝐞𝐬𝐭𝐚𝐫𝐭 𝐁𝐨𝐭"): lambda m: command_restart_bot(m),
}

def lock_bot_handler(message):
    global bot_locked
    if message.from_user.id not in admin_ids:
        bot.reply_to(message, B("⚠️ Admin permissions required."))
        return
    bot_locked = True
    bot.reply_to(message, B("🔒 Bot locked"), reply_markup=create_reply_keyboard_main_menu(message.from_user.id))

def unlock_bot_handler(message):
    global bot_locked
    if message.from_user.id not in admin_ids:
        bot.reply_to(message, B("⚠️ Admin permissions required."))
        return
    bot_locked = False
    bot.reply_to(message, B("🔓 Bot unlocked"), reply_markup=create_reply_keyboard_main_menu(message.from_user.id))

def analytics_handler(message):
    if message.from_user.id not in admin_ids:
        bot.reply_to(message, B("⚠️ Admin permissions required."))
        return
    analytics_callback_handler(message)

def analytics_callback_handler(message):
    total_users = len(active_users)
    total_files = sum(len(files) for files in user_files.values())
    running_scripts = len([k for k, v in bot_scripts.items() if is_bot_running(v['user_id'], v['file_name'])])

    total_storage = 0
    for user_id in user_files:
        user_folder = get_user_folder(user_id)
        if os.path.exists(user_folder):
            for root, dirs, files in os.walk(user_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    total_storage += os.path.getsize(file_path)

    total_storage_mb = round(total_storage / (1024 * 1024), 2)

    analytics_text = B(f"""
📈 ADVANCED ANALYTICS

👥 User Metrics:
• Total Users: {total_users}
• Active Today: {len([uid for uid in active_users])}

📁 Storage Analytics:
• Total Files: {total_files}
• Total Storage: {total_storage_mb} MB
• Avg Files per User: {round(total_files/max(total_users, 1), 1)}

🚀 Performance:
• Running Scripts: {running_scripts}
• Max Concurrent: 50
• Success Rate: 98.5%

🎫 Revenue Metrics:
• Premium Users: {len([uid for uid in active_users if get_user_tier(uid) == 'premium'])}
• Conversion Rate: {round(len([uid for uid in active_users if get_user_tier(uid) == 'premium'])/max(total_users, 1)*100, 1)}%
""")

    bot.reply_to(message, analytics_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text in BUTTON_HANDLERS)
def handle_button_click(message):
    handler = BUTTON_HANDLERS.get(message.text)
    if handler:
        handler(message)

def show_user_files(message):
    user_id = message.from_user.id
    files = user_files.get(user_id, [])

    if not files:
        bot.reply_to(message, B("📭 No files uploaded yet."))
        return

    markup = types.InlineKeyboardMarkup(row_width=1)
    for file_name, file_type in files:
        is_running = is_bot_running(user_id, file_name)
        status = "🟢" if is_running else "🔴"
        btn_text = B(f"{status} {file_name} ({file_type})")
        markup.add(types.InlineKeyboardButton(btn_text, callback_data=f'file_{user_id}_{file_name}'))

    bot.reply_to(message, B("📂 Your Files:"), reply_markup=markup)

def check_speed(message):
    start_time = time.time()
    msg = bot.reply_to(message, B("🏃 Checking speed..."))
    latency = round((time.time() - start_time) * 1000, 2)

    bot.edit_message_text(
        B(f"⚡ Bot Speed\n\n⏱️ Latency: {latency}ms\n🔒 Status: {'🔴 Locked' if bot_locked else '🟢 Unlocked'}"),
        message.chat.id, msg.message_id
    )

def show_profile(message):
    user_id = message.from_user.id
    tier = get_user_tier(user_id)
    tier_info = TIER_SYSTEM[tier]

    profile_text = B(f"""
👤 PROFILE

🆔 User ID: `{user_id}`
👤 Name: {message.from_user.first_name}
🎫 Tier: {tier_info['icon']} {tier_info['name']}
📁 Files: {get_user_file_count(user_id)}/{get_user_file_limit(user_id)}
🟢 Running: {len([1 for f in user_files.get(user_id, []) if is_bot_running(user_id, f[0])])}
""")

    bot.reply_to(message, profile_text, parse_mode='Markdown')

def show_admin_panel(message):
    if message.from_user.id not in admin_ids:
        bot.reply_to(message, B("⚠️ Admin permissions required."))
        return

    bot.reply_to(message, B("👑 ADMIN PANEL"), reply_markup=create_admin_panel())

def show_subscription_panel(message):
    if message.from_user.id not in admin_ids:
        bot.reply_to(message, B("⚠️ Admin permissions required."))
        return

    bot.reply_to(message, B("💳 SUBSCRIPTION MANAGEMENT"),
                 reply_markup=create_subscription_menu())

# ================================
# CALLBACK QUERY HANDLERS
# ================================
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    user_id = call.from_user.id
    data = call.data

    try:
        if data == 'upload':
            upload_callback(call)
        elif data == 'check_files':
            check_files_callback(call)
        elif data.startswith('file_'):
            file_control_callback(call)
        elif data.startswith('start_'):
            start_bot_callback(call)
        elif data.startswith('stop_'):
            stop_bot_callback(call)
        elif data.startswith('restart_'):
            restart_bot_callback(call)
        elif data.startswith('delete_'):
            delete_bot_callback(call)
        elif data.startswith('logs_'):
            logs_bot_callback(call)
        elif data == 'speed':
            speed_callback(call)
        elif data == 'stats':
            stats_callback(call)
        elif data == 'profile':
            profile_callback(call)
        elif data == 'restart_all':
            restart_all_callback(call)
        elif data == 'admin_panel':
            admin_panel_callback(call)
        elif data == 'subscription':
            subscription_callback(call)
        elif data == 'lock_bot':
            lock_bot_callback(call)
        elif data == 'unlock_bot':
            unlock_bot_callback(call)
        elif data == 'recover_all':
            recover_all_callback(call)
        elif data == 'analytics':
            analytics_callback(call)
        elif data == 'add_admin':
            add_admin_callback(call)
        elif data == 'remove_admin':
            remove_admin_callback(call)
        elif data == 'list_admins':
            list_admins_callback(call)
        elif data == 'system_stats':
            system_stats_callback(call)
        elif data == 'add_subscription':
            add_subscription_callback(call)
        elif data == 'remove_subscription':
            remove_subscription_callback(call)
        elif data == 'check_subscription':
            check_subscription_callback(call)
        elif data == 'restart_bot':
            restart_bot_callback_callback(call)
        elif data == 'back_to_main':
            back_to_main_callback(call)
        else:
            bot.answer_callback_query(call.id, "❌ Unknown command")

    except Exception as e:
        logger.error(f"❌ Error in callback: {e}")
        bot.answer_callback_query(call.id, "❌ Error processing request")

def upload_callback(call):
    user_id = call.from_user.id
    file_limit = get_user_file_limit(user_id)
    current_files = get_user_file_count(user_id)

    if current_files >= file_limit:
        bot.answer_callback_query(call.id,
                                  B(f"⚠️ File limit reached ({current_files}/{file_limit})"),
                                  show_alert=True)
        return

    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, B("📤 Send your .py, .js, or .zip file."))

def check_files_callback(call):
    user_id = call.from_user.id
    files = user_files.get(user_id, [])

    if not files:
        bot.answer_callback_query(call.id, B("📭 No files uploaded"), show_alert=True)
        return

    markup = types.InlineKeyboardMarkup(row_width=1)
    for file_name, file_type in files:
        is_running = is_bot_running(user_id, file_name)
        status = "🟢" if is_running else "🔴"
        btn_text = B(f"{status} {file_name} ({file_type})")
        markup.add(types.InlineKeyboardButton(btn_text, callback_data=f'file_{user_id}_{file_name}'))

    markup.add(types.InlineKeyboardButton(B("🔙 𝐁𝐚𝐜𝐤"), callback_data='back_to_main'))

    bot.answer_callback_query(call.id)
    bot.edit_message_text(B("📂 Your Files:"),
                          call.message.chat.id, call.message.message_id,
                          reply_markup=markup)

def file_control_callback(call):
    try:
        parts = call.data.split('_')
        if len(parts) < 3:
            return

        user_id = int(parts[1])
        file_name = '_'.join(parts[2:])

        if call.from_user.id != user_id and call.from_user.id not in admin_ids:
            bot.answer_callback_query(call.id, B("⚠️ Permission denied"), show_alert=True)
            return

        files = user_files.get(user_id, [])
        file_info = None
        for fname, ftype in files:
            if fname == file_name:
                file_info = (fname, ftype)
                break

        if not file_info:
            bot.answer_callback_query(call.id, B("❌ File not found"), show_alert=True)
            return

        is_running = is_bot_running(user_id, file_name)

        bot.answer_callback_query(call.id)
        bot.edit_message_text(
            B(f"⚙️ Controls for: `{file_name}`\n📁 Type: {file_info[1]}\n📊 Status: {'🟢 Running' if is_running else '🔴 Stopped'}"),
            call.message.chat.id, call.message.message_id,
            reply_markup=create_control_buttons(user_id, file_name, is_running),
            parse_mode='Markdown'
        )

    except Exception as e:
        logger.error(f"❌ Error in file control: {e}")
        bot.answer_callback_query(call.id, B("❌ Error processing"))

def start_bot_callback(call):
    try:
        parts = call.data.split('_')
        user_id = int(parts[1])
        file_name = '_'.join(parts[2:])

        if call.from_user.id != user_id and call.from_user.id not in admin_ids:
            bot.answer_callback_query(call.id, B("⚠️ Permission denied"), show_alert=True)
            return

        if is_bot_running(user_id, file_name):
            bot.answer_callback_query(call.id, B("✅ Already running"), show_alert=True)
            return

        user_folder = get_user_folder(user_id)
        file_path = os.path.join(user_folder, file_name)

        if not os.path.exists(file_path):
            bot.answer_callback_query(call.id, B("❌ File not found"), show_alert=True)
            return

        file_type = 'py'
        for fname, ftype in user_files.get(user_id, []):
            if fname == file_name:
                file_type = ftype
                break

        bot.answer_callback_query(call.id, B("🚀 Starting script..."))

        if file_type == 'py':
            threading.Thread(target=run_script, args=(file_path, user_id, user_folder, file_name, call.message)).start()
        elif file_type == 'js':
            threading.Thread(target=run_js_script, args=(file_path, user_id, user_folder, file_name, call.message)).start()
        else:
            bot.answer_callback_query(call.id, B("❌ Unsupported file type"), show_alert=True)

    except Exception as e:
        logger.error(f"❌ Error starting script: {e}")
        bot.answer_callback_query(call.id, B("❌ Error starting script"))

def stop_bot_callback(call):
    try:
        parts = call.data.split('_')
        user_id = int(parts[1])
        file_name = '_'.join(parts[2:])

        if call.from_user.id != user_id and call.from_user.id not in admin_ids:
            bot.answer_callback_query(call.id, B("⚠️ Permission denied"), show_alert=True)
            return

        if not is_bot_running(user_id, file_name):
            bot.answer_callback_query(call.id, B("✅ Already stopped"), show_alert=True)
            return

        script_key = f"{user_id}_{file_name}"
        if script_key in bot_scripts:
            kill_process_tree(bot_scripts[script_key])
            if script_key in bot_scripts:
                del bot_scripts[script_key]

        bot.answer_callback_query(call.id, B("🛑 Stopped script"))

        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.message_id,
            reply_markup=create_control_buttons(user_id, file_name, False)
        )

    except Exception as e:
        logger.error(f"❌ Error stopping script: {e}")
        bot.answer_callback_query(call.id, B("❌ Error stopping script"))

def restart_bot_callback(call):
    try:
        parts = call.data.split('_')
        user_id = int(parts[1])
        file_name = '_'.join(parts[2:])

        if call.from_user.id != user_id and call.from_user.id not in admin_ids:
            bot.answer_callback_query(call.id, B("⚠️ Permission denied"), show_alert=True)
            return

        if is_bot_running(user_id, file_name):
            script_key = f"{user_id}_{file_name}"
            if script_key in bot_scripts:
                kill_process_tree(bot_scripts[script_key])
                if script_key in bot_scripts:
                    del bot_scripts[script_key]
            time.sleep(1)

        user_folder = get_user_folder(user_id)
        file_path = os.path.join(user_folder, file_name)

        if not os.path.exists(file_path):
            bot.answer_callback_query(call.id, B("❌ File not found"), show_alert=True)
            return

        file_type = 'py'
        for fname, ftype in user_files.get(user_id, []):
            if fname == file_name:
                file_type = ftype
                break

        bot.answer_callback_query(call.id, B("🔄 Restarting script..."))

        if file_type == 'py':
            threading.Thread(target=run_script, args=(file_path, user_id, user_folder, file_name, call.message)).start()
        elif file_type == 'js':
            threading.Thread(target=run_js_script, args=(file_path, user_id, user_folder, file_name, call.message)).start()

    except Exception as e:
        logger.error(f"❌ Error restarting script: {e}")
        bot.answer_callback_query(call.id, B("❌ Error restarting script"))

def delete_bot_callback(call):
    try:
        parts = call.data.split('_')
        user_id = int(parts[1])
        file_name = '_'.join(parts[2:])

        if call.from_user.id != user_id and call.from_user.id not in admin_ids:
            bot.answer_callback_query(call.id, B("⚠️ Permission denied"), show_alert=True)
            return

        if is_bot_running(user_id, file_name):
            script_key = f"{user_id}_{file_name}"
            if script_key in bot_scripts:
                kill_process_tree(bot_scripts[script_key])
                if script_key in bot_scripts:
                    del bot_scripts[script_key]

        user_folder = get_user_folder(user_id)
        file_path = os.path.join(user_folder, file_name)
        log_path = os.path.join(user_folder, f"{os.path.splitext(file_name)[0]}.log")

        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(log_path):
            os.remove(log_path)

        remove_user_file_db(user_id, file_name)

        bot.answer_callback_query(call.id, B("🗑️ File deleted"))

        check_files_callback(call)

    except Exception as e:
        logger.error(f"❌ Error deleting file: {e}")
        bot.answer_callback_query(call.id, B("❌ Error deleting file"))

def logs_bot_callback(call):
    try:
        parts = call.data.split('_')
        user_id = int(parts[1])
        file_name = '_'.join(parts[2:])

        if call.from_user.id != user_id and call.from_user.id not in admin_ids:
            bot.answer_callback_query(call.id, B("⚠️ Permission denied"), show_alert=True)
            return

        user_folder = get_user_folder(user_id)
        log_path = os.path.join(user_folder, f"{os.path.splitext(file_name)[0]}.log")

        if not os.path.exists(log_path):
            bot.answer_callback_query(call.id, B("📭 No logs found"), show_alert=True)
            return

        try:
            with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                log_content = f.read()

            if len(log_content) > 3000:
                log_content = log_content[-3000:]
                log_content = "...\n" + log_content

            bot.answer_callback_query(call.id)
            bot.send_message(call.message.chat.id,
                             B(f"📜 Logs for `{file_name}`:\n```\n{log_content}\n```"),
                             parse_mode='Markdown')

        except Exception as e:
            bot.answer_callback_query(call.id, B("❌ Error reading logs"))

    except Exception as e:
        logger.error(f"❌ Error getting logs: {e}")
        bot.answer_callback_query(call.id, B("❌ Error getting logs"))

def speed_callback(call):
    start_time = time.time()
    bot.answer_callback_query(call.id)
    latency = round((time.time() - start_time) * 1000, 2)

    bot.edit_message_text(
        B(f"⚡ Bot Speed\n\n⏱️ Latency: {latency}ms\n🔒 Status: {'🔴 Locked' if bot_locked else '🟢 Unlocked'}"),
        call.message.chat.id, call.message.message_id
    )

def stats_callback(call):
    total_users = len(active_users)
    total_files = sum(len(files) for files in user_files.values())
    running_scripts = len([k for k, v in bot_scripts.items() if is_bot_running(v['user_id'], v['file_name'])])
    recovery_count = recovery_system.get_running_count()

    stats_text = B(f"""
📊 SYSTEM STATISTICS

👥 Total Users: {total_users}
📁 Total Files: {total_files}
🟢 Running Scripts: {running_scripts}
💾 Recovery Saved: {recovery_count}
🔒 Bot Status: {'🔴 Locked' if bot_locked else '🟢 Unlocked'}

🎫 Tier Distribution:
• FREE: {len([uid for uid in active_users if get_user_tier(uid) == 'free'])}
• PREMIUM: {len([uid for uid in active_users if get_user_tier(uid) == 'premium'])}
• OWNER/ADMIN: {len([uid for uid in active_users if get_user_tier(uid) == 'owner'])}
""")

    bot.answer_callback_query(call.id)
    bot.edit_message_text(stats_text, call.message.chat.id, call.message.message_id,
                          parse_mode='Markdown')

def profile_callback(call):
    user_id = call.from_user.id
    tier = get_user_tier(user_id)
    tier_info = TIER_SYSTEM[tier]

    profile_text = B(f"""
👤 PROFILE

🆔 User ID: `{user_id}`
👤 Name: {call.from_user.first_name}
🎫 Tier: {tier_info['icon']} {tier_info['name']}
📁 Files: {get_user_file_count(user_id)}/{get_user_file_limit(user_id)}
🟢 Running: {len([1 for f in user_files.get(user_id, []) if is_bot_running(user_id, f[0])])}
""")

    bot.answer_callback_query(call.id)
    bot.edit_message_text(profile_text, call.message.chat.id, call.message.message_id,
                          parse_mode='Markdown')

def restart_all_callback(call):
    if call.from_user.id not in admin_ids:
        bot.answer_callback_query(call.id, B("⚠️ Admin permissions required"), show_alert=True)
        return

    msg = bot.send_message(call.message.chat.id, ProgressAnimation.execute_animation()[0])

    restarted = 0
    for user_id, files in user_files.items():
        for file_name, file_type in files:
            if is_bot_running(user_id, file_name):
                script_key = f"{user_id}_{file_name}"
                if script_key in bot_scripts:
                    kill_process_tree(bot_scripts[script_key])
                    del bot_scripts[script_key]

            user_folder = get_user_folder(user_id)
            file_path = os.path.join(user_folder, file_name)

            if os.path.exists(file_path):
                if file_type == 'py':
                    threading.Thread(target=run_script, args=(file_path, user_id, user_folder, file_name, call.message)).start()
                elif file_type == 'js':
                    threading.Thread(target=run_js_script, args=(file_path, user_id, user_folder, file_name, call.message)).start()

                restarted += 1
                time.sleep(0.5)

    bot.edit_message_text(
        B(f"✅ Restarted {restarted} scripts."),
        call.message.chat.id, msg.message_id
    )
    bot.answer_callback_query(call.id)

def admin_panel_callback(call):
    if call.from_user.id not in admin_ids:
        bot.answer_callback_query(call.id, B("⚠️ Admin permissions required"), show_alert=True)
        return

    bot.answer_callback_query(call.id)
    bot.edit_message_text(B("👑 ADMIN PANEL"),
                          call.message.chat.id, call.message.message_id,
                          reply_markup=create_admin_panel())

def subscription_callback(call):
    if call.from_user.id not in admin_ids:
        bot.answer_callback_query(call.id, B("⚠️ Admin permissions required"), show_alert=True)
        return

    bot.answer_callback_query(call.id)
    bot.edit_message_text(B("💳 SUBSCRIPTION MANAGEMENT"),
                          call.message.chat.id, call.message.message_id,
                          reply_markup=create_subscription_menu())

def lock_bot_callback(call):
    if call.from_user.id not in admin_ids:
        bot.answer_callback_query(call.id, B("⚠️ Admin permissions required"), show_alert=True)
        return

    global bot_locked
    bot_locked = True

    bot.answer_callback_query(call.id, B("🔒 Bot locked"))
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                  reply_markup=create_main_menu_inline(call.from_user.id))

def unlock_bot_callback(call):
    if call.from_user.id not in admin_ids:
        bot.answer_callback_query(call.id, B("⚠️ Admin permissions required"), show_alert=True)
        return

    global bot_locked
    bot_locked = False

    bot.answer_callback_query(call.id, B("🔓 Bot unlocked"))
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                  reply_markup=create_main_menu_inline(call.from_user.id))

def recover_all_callback(call):
    if call.from_user.id not in admin_ids:
        bot.answer_callback_query(call.id, B("⚠️ Admin permissions required"), show_alert=True)
        return

    msg = bot.send_message(call.message.chat.id, ProgressAnimation.recovery_animation()[0])

    for i, frame in enumerate(ProgressAnimation.recovery_animation()):
        try:
            bot.edit_message_text(frame, call.message.chat.id, msg.message_id)
            time.sleep(0.3)
        except:
            pass

    recovered = recovery_system.recover_all_scripts()

    if recovered:
        bot.edit_message_text(
            B(f"✅ Recovery Complete!\n🔄 Recovered: {len(recovered)} scripts"),
            call.message.chat.id, msg.message_id
        )
    else:
        bot.edit_message_text(
            B("📭 No scripts to recover."),
            call.message.chat.id, msg.message_id
        )

    bot.answer_callback_query(call.id)

def analytics_callback(call):
    if call.from_user.id not in admin_ids:
        bot.answer_callback_query(call.id, B("⚠️ Admin permissions required"), show_alert=True)
        return

    total_users = len(active_users)
    total_files = sum(len(files) for files in user_files.values())
    running_scripts = len([k for k, v in bot_scripts.items() if is_bot_running(v['user_id'], v['file_name'])])

    total_storage = 0
    for user_id in user_files:
        user_folder = get_user_folder(user_id)
        if os.path.exists(user_folder):
            for root, dirs, files in os.walk(user_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    total_storage += os.path.getsize(file_path)

    total_storage_mb = round(total_storage / (1024 * 1024), 2)

    analytics_text = B(f"""
📈 ADVANCED ANALYTICS

👥 User Metrics:
• Total Users: {total_users}
• Active Today: {len([uid for uid in active_users])}

📁 Storage Analytics:
• Total Files: {total_files}
• Total Storage: {total_storage_mb} MB
• Avg Files per User: {round(total_files/max(total_users, 1), 1)}

🚀 Performance:
• Running Scripts: {running_scripts}
• Max Concurrent: 50
• Success Rate: 98.5%

🎫 Revenue Metrics:
• Premium Users: {len([uid for uid in active_users if get_user_tier(uid) == 'premium'])}
• Conversion Rate: {round(len([uid for uid in active_users if get_user_tier(uid) == 'premium'])/max(total_users, 1)*100, 1)}%
""")

    bot.answer_callback_query(call.id)
    bot.edit_message_text(analytics_text, call.message.chat.id, call.message.message_id,
                          parse_mode='Markdown')

def add_admin_callback(call):
    if call.from_user.id != OWNER_ID:
        bot.answer_callback_query(call.id, B("⚠️ Only owner can add admins"), show_alert=True)
        return

    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, B("👑 Enter user ID to add as admin:"))
    bot.register_next_step_handler(call.message, process_add_admin)

def process_add_admin(message):
    if message.from_user.id != OWNER_ID:
        return

    try:
        admin_id = int(message.text.strip())

        with DB_LOCK:
            conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
            c = conn.cursor()
            c.execute('INSERT OR IGNORE INTO admins (user_id, added_by, added_at) VALUES (?, ?, ?)',
                      (admin_id, message.from_user.id, datetime.now().isoformat()))
            conn.commit()
            conn.close()

        admin_ids.add(admin_id)
        bot.reply_to(message, B(f"✅ User `{admin_id}` added as admin."))

    except ValueError:
        bot.reply_to(message, B("❌ Invalid user ID."))
    except Exception as e:
        bot.reply_to(message, B(f"❌ Error: {str(e)}"))

def remove_admin_callback(call):
    if call.from_user.id != OWNER_ID:
        bot.answer_callback_query(call.id, B("⚠️ Only owner can remove admins"), show_alert=True)
        return

    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, B("👑 Enter user ID to remove admin:"))
    bot.register_next_step_handler(call.message, process_remove_admin)

def process_remove_admin(message):
    if message.from_user.id != OWNER_ID:
        return

    try:
        admin_id = int(message.text.strip())

        if admin_id == OWNER_ID:
            bot.reply_to(message, B("❌ Cannot remove owner."))
            return

        with DB_LOCK:
            conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
            c = conn.cursor()
            c.execute('DELETE FROM admins WHERE user_id = ?', (admin_id,))
            conn.commit()
            conn.close()

        admin_ids.discard(admin_id)
        bot.reply_to(message, B(f"✅ User `{admin_id}` removed from admins."))

    except ValueError:
        bot.reply_to(message, B("❌ Invalid user ID."))
    except Exception as e:
        bot.reply_to(message, B(f"❌ Error: {str(e)}"))

def list_admins_callback(call):
    if call.from_user.id not in admin_ids:
        bot.answer_callback_query(call.id, B("⚠️ Admin permissions required"), show_alert=True)
        return

    admin_list = "\n".join([f"• `{admin_id}` {'👑' if admin_id == OWNER_ID else ''}" for admin_id in sorted(admin_ids)])

    bot.answer_callback_query(call.id)
    bot.edit_message_text(B(f"👑 Current Admins:\n\n{admin_list}"),
                          call.message.chat.id, call.message.message_id,
                          parse_mode='Markdown')

def system_stats_callback(call):
    if call.from_user.id not in admin_ids:
        bot.answer_callback_query(call.id, B("⚠️ Admin permissions required"), show_alert=True)
        return

    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    total_users = len(active_users)
    total_files = sum(len(files) for files in user_files.values())
    running_scripts = len([k for k, v in bot_scripts.items() if is_bot_running(v['user_id'], v['file_name'])])

    stats_text = B(f"""
🖥️ SYSTEM STATUS

CPU Usage: {cpu_percent}%
Memory: {memory.percent}% ({round(memory.used/(1024**3), 1)}GB / {round(memory.total/(1024**3), 1)}GB)
Disk: {disk.percent}% ({round(disk.used/(1024**3), 1)}GB / {round(disk.total/(1024**3), 1)}GB)

🤖 BOT STATS
Users: {total_users}
Files: {total_files}
Running: {running_scripts}
Status: {'🔴 Locked' if bot_locked else '🟢 Unlocked'}

📊 PERFORMANCE
Uptime: {round(time.time() - psutil.boot_time())}s
Processes: {len(psutil.pids())}
Threads: {threading.active_count()}
""")

    bot.answer_callback_query(call.id)
    bot.edit_message_text(stats_text, call.message.chat.id, call.message.message_id)

def add_subscription_callback(call):
    if call.from_user.id not in admin_ids:
        bot.answer_callback_query(call.id, B("⚠️ Admin permissions required"), show_alert=True)
        return

    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, B("💳 Enter user ID and days (e.g., 123456 30):"))
    bot.register_next_step_handler(call.message, process_add_subscription)

def process_add_subscription(message):
    if message.from_user.id not in admin_ids:
        return

    try:
        parts = message.text.strip().split()
        if len(parts) != 2:
            bot.reply_to(message, B("❌ Invalid format. Use: user_id days"))
            return

        user_id = int(parts[0])
        days = int(parts[1])

        expiry = datetime.now() + timedelta(days=days)
        save_subscription(user_id, expiry, 'premium')

        bot.reply_to(message, B(f"✅ Subscription added for user `{user_id}`\n📅 Expires: {expiry.strftime('%Y-%m-%d %H:%M:%S')}"))

    except ValueError:
        bot.reply_to(message, B("❌ Invalid user ID or days."))
    except Exception as e:
        bot.reply_to(message, B(f"❌ Error: {str(e)}"))

def remove_subscription_callback(call):
    if call.from_user.id not in admin_ids:
        bot.answer_callback_query(call.id, B("⚠️ Admin permissions required"), show_alert=True)
        return

    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, B("💳 Enter user ID to remove subscription:"))
    bot.register_next_step_handler(call.message, process_remove_subscription)

def process_remove_subscription(message):
    if message.from_user.id not in admin_ids:
        return

    try:
        user_id = int(message.text.strip())
        remove_subscription_db(user_id)

        bot.reply_to(message, B(f"✅ Subscription removed for user `{user_id}`"))

    except ValueError:
        bot.reply_to(message, B("❌ Invalid user ID."))
    except Exception as e:
        bot.reply_to(message, B(f"❌ Error: {str(e)}"))

def check_subscription_callback(call):
    if call.from_user.id not in admin_ids:
        bot.answer_callback_query(call.id, B("⚠️ Admin permissions required"), show_alert=True)
        return

    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, B("💳 Enter user ID to check subscription:"))
    bot.register_next_step_handler(call.message, process_check_subscription)

def process_check_subscription(message):
    if message.from_user.id not in admin_ids:
        return

    try:
        user_id = int(message.text.strip())

        if user_id in user_subscriptions:
            sub = user_subscriptions[user_id]
            expiry = sub.get('expiry')
            tier = sub.get('tier', 'premium')

            if expiry and expiry > datetime.now():
                days_left = (expiry - datetime.now()).days
                bot.reply_to(message, B(f"✅ User `{user_id}` has active subscription.\n🎫 Tier: {tier}\n📅 Expires: {expiry.strftime('%Y-%m-%d %H:%M:%S')}\n⏳ Days left: {days_left}"))
            else:
                bot.reply_to(message, B(f"⚠️ User `{user_id}` has expired subscription.\n📅 Expired: {expiry.strftime('%Y-%m-%d %H:%M:%S') if expiry else 'Unknown'}"))
                remove_subscription_db(user_id)
        else:
            bot.reply_to(message, B(f"📭 User `{user_id}` has no subscription."))

    except ValueError:
        bot.reply_to(message, B("❌ Invalid user ID."))
    except Exception as e:
        bot.reply_to(message, B(f"❌ Error: {str(e)}"))

def restart_bot_callback_callback(call):
    if call.from_user.id not in admin_ids:
        bot.answer_callback_query(call.id, B("⚠️ Admin permissions required"), show_alert=True)
        return

    bot.answer_callback_query(call.id, B("🚀 Sending restart notifications..."))
    threading.Thread(target=send_restart_notification).start()

    msg = bot.send_message(call.message.chat.id, ProgressAnimation.restart_animation()[0])

    for i, frame in enumerate(ProgressAnimation.restart_animation()):
        try:
            bot.edit_message_text(frame, call.message.chat.id, msg.message_id)
            time.sleep(0.5)
        except:
            pass

    time.sleep(5)

    bot.edit_message_text(
        B("✅ Restart notifications sent!\n\n🔄 Bot will now restart..."),
        call.message.chat.id, msg.message_id
    )

    time.sleep(2)
    os.execv(sys.executable, ['python'] + sys.argv)

def back_to_main_callback(call):
    user_id = call.from_user.id
    tier = get_user_tier(user_id)
    tier_info = TIER_SYSTEM[tier]

    welcome_text = B(f"""
┏━━━━━━━━━━━━━━━━━━━━━━┓
┃   🚀 Pʀᴇᴍɪᴜᴍ Hᴏꜱᴛɪɴɢ Bᴏᴛ  ┃
┃      VERSION 3.4     ┃
┗━━━━━━━━━━━━━━━━━━━━━━┛

👤 Welcome back, {call.from_user.first_name}!
🆔 User ID: `{user_id}`
🎫 Tier: {tier_info['icon']} {tier_info['name']}
📁 Files: {get_user_file_count(user_id)}/{get_user_file_limit(user_id)}

Use buttons below to navigate.
""")

    bot.answer_callback_query(call.id)
    bot.edit_message_text(welcome_text,
                          call.message.chat.id, call.message.message_id,
                          reply_markup=create_main_menu_inline(user_id),
                          parse_mode='Markdown')

# ================================
# CLEANUP AND SHUTDOWN
# ================================
def cleanup():
    logger.warning("🔴 Shutting down... Cleaning up processes")

    for script_key, script_info in list(bot_scripts.items()):
        try:
            kill_process_tree(script_info)
        except:
            pass

    logger.info("✅ Cleanup complete")

atexit.register(cleanup)

# ================================
# BOT STARTUP AND AUTO-RECOVERY
# ================================
def startup_recovery():
    logger.info("🚀 Starting auto-recovery process...")

    msg = None
    try:
        msg = bot.send_message(OWNER_ID, ProgressAnimation.recovery_animation()[0])

        for i, frame in enumerate(ProgressAnimation.recovery_animation()):
            try:
                bot.edit_message_text(frame, OWNER_ID, msg.message_id)
                time.sleep(0.3)
            except:
                pass

        recovered = recovery_system.recover_all_scripts()

        if recovered:
            bot.edit_message_text(
                B(f"✅ Startup Recovery Complete!\n🔄 Recovered: {len(recovered)} scripts"),
                OWNER_ID, msg.message_id
            )
        else:
            bot.edit_message_text(
                B("📭 No scripts to recover on startup."),
                OWNER_ID, msg.message_id
            )

    except Exception as e:
        logger.error(f"❌ Error in startup recovery: {e}")
        if msg:
            try:
                bot.edit_message_text(
                    B(f"❌ Error in startup recovery: {str(e)[:100]}"),
                    OWNER_ID, msg.message_id
                )
            except:
                pass

# ================================
# MAIN EXECUTION
# ================================
if __name__ == '__main__':
    logger.info("="*50)
    logger.info("🚀 Pʀᴇᴍɪᴜᴍ Hᴏꜱᴛɪɴɢ Bᴏᴛ VERSION 3.4")
    logger.info("📊 Auto-Recovery System Enabled")
    logger.info("🎫 Tier-Based Hosting")
    logger.info(f"👑 Owner ID: {OWNER_ID}")
    logger.info(f"🛡️ Admins: {len(admin_ids)}")
    logger.info(f"👥 Active Users: {len(active_users)}")
    logger.info(f"📁 Total Files: {sum(len(files) for files in user_files.values())}")

    try:
        bot_username = bot.get_me().username
        logger.info(f"🤖 Bot Username: @{bot_username}")
    except Exception as e:
        logger.error(f"❌ Error getting bot username: {e}")

    logger.info("="*50)

    keep_alive()

    threading.Thread(target=startup_recovery).start()

    logger.info("🤖 Starting bot polling...")

    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=30)
        except requests.exceptions.ReadTimeout:
            logger.warning("⚠️ Read Timeout. Restarting in 5s...")
            time.sleep(5)
        except requests.exceptions.ConnectionError as ce:
            logger.error(f"⚠️ Connection Error: {ce}. Retrying in 15s...")
            time.sleep(15)
        except Exception as e:
            logger.critical(f"💥 Unrecoverable error: {e}", exc_info=True)
            logger.info("🔄 Restarting in 30s due to critical error...")
            time.sleep(30)
        finally:
            logger.warning("🔴 Polling stopped. Will restart if in loop...")
            time.sleep(1)
