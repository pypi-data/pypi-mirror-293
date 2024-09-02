#!/usr/bin/env python3
import sqlite3
import hashlib
import uuid, os
from datetime import datetime, timedelta

class SecureAccountManager:
    def __init__(self, db_file=None, passphrase=None):
        # Define o caminho relativo se não for fornecido
        if db_file is None:
            base_dir = os.path.dirname(__file__)  # Diretório onde o script está
            db_file = os.path.join(base_dir, '..', 'accounts', 'accounts.db')
        
        self.db_file = os.path.abspath(db_file)  # Garante que o caminho seja absoluto
        self.passphrase = passphrase

        # Conecta ao banco de dados
        self.connection = sqlite3.connect(self.db_file)
        if self.passphrase:
            # Aplicar criptografia, se necessário (ajuste conforme a implementação do banco de dados)
            self.connection.execute(f"PRAGMA key = '{self.passphrase}'")
        
        self.current_user = None
        self.initialize_db()

    def initialize_db(self):
        with self.connection:
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    uid TEXT PRIMARY KEY,
                    name TEXT,
                    password TEXT,
                    balance REAL,
                    paid_exploits INTEGER,
                    vip_level TEXT,
                    attacks_used INTEGER,
                    last_attack_reset TEXT,
                    vip_expiry TEXT
                )
            ''')

    def create_account(self, name, password):
        uid = str(uuid.uuid4())
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        with self.connection:
            self.connection.execute('''
                INSERT INTO users (uid, name, password, balance, paid_exploits, vip_level, attacks_used, last_attack_reset, vip_expiry)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (uid, name, hashed_password, 0, 0, 'free', 0, datetime.utcnow().isoformat(), None))
        return uid

    def get_user_by_name(self, name):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE name = ?', (name,))
        row = cursor.fetchone()
        if row:
            return {
                "uid": row[0],
                "name": row[1],
                "password": row[2],
                "balance": row[3],
                "paid_exploits": row[4],
                "vip_level": row[5],
                "attacks_used": row[6],
                "last_attack_reset": row[7],
                "vip_expiry": row[8]
            }
        return None

    def get_user(self, uid):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE uid = ?', (uid,))
        row = cursor.fetchone()
        if row:
            return {
                "uid": row[0],
                "name": row[1],
                "password": row[2],
                "balance": row[3],
                "paid_exploits": row[4],
                "vip_level": row[5],
                "attacks_used": row[6],
                "last_attack_reset": row[7],
                "vip_expiry": row[8]
            }
        return None

    def update_account(self, user):
        with self.connection:
            self.connection.execute('''
                UPDATE users
                SET name = ?, password = ?, balance = ?, paid_exploits = ?, vip_level = ?, attacks_used = ?, last_attack_reset = ?, vip_expiry = ?
                WHERE uid = ?
            ''', (user['name'], user['password'], user['balance'], user['paid_exploits'], user['vip_level'], user['attacks_used'], user['last_attack_reset'], user['vip_expiry'], user['uid']))

    def reset_attacks(self):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM users')
            users = cursor.fetchall()
            for user in users:
                if datetime.fromisoformat(user[7]) < datetime.utcnow() - timedelta(hours=1):
                    self.connection.execute('''
                        UPDATE users
                        SET attacks_used = ?, last_attack_reset = ?
                        WHERE uid = ?
                    ''', (0, datetime.utcnow().isoformat(), user[0]))

    def get_profile(self, uid):
        user = self.get_user(uid)
        if user:
            return {
                "UID": user['uid'],
                "Name": user['name'],
                "Balance": user['balance'],
                "Paid Exploits": user['paid_exploits'],
                "VIP Level": user['vip_level'],
                "Attacks Used": user['attacks_used'],
                "VIP Expiry": user['vip_expiry']
            }
        return None

    def login(self, name, password):
        user = self.get_user_by_name(name)
        if user and user['password'] == hashlib.sha256(password.encode()).hexdigest():
            self.current_user = user
            return True
        return False

    def logout(self):
        self.current_user = None

    def get_current_user(self):
        return self.current_user

    def set_vip(self, uid, level, duration):
        user = self.get_user(uid)
        if user:
            vip_expiry = datetime.utcnow() + timedelta(days=duration)
            user['vip_level'] = level
            user['vip_expiry'] = vip_expiry.isoformat()
            self.update_account(user)
