import sqlite3
dbpath = './db/data.sqlite'
connection = sqlite3.connect(dbpath)
connection.isolation_level = None


class Database:
    def __init__(self):
        self.cursor = connection.cursor()

    def execute(self, sql):
        self.cursor.execute(sql)

    def setup(self):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS cmd_mute(user_id integer primary key)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS welcome_notice(guild_id integer primary key)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS msg_expand(guild_id integer primary key)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS '
                            'member_log(guild_id integer primary key, join_msg, left_msg, join_id, left_id)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS '
                            'tao_help(guild_id integer primary key, func, log_id, role_t, role_g, role_r, premium)')

    # コマンド制限
    def mute_user_set(self, user_id):
        self.setup()
        self.cursor.execute('INSERT INTO cmd_mute VALUES (?)', (user_id,))
        return True

    def mute_user_unset(self, user_id):
        self.setup()
        self.cursor.execute('DELETE FROM cmd_mute WHERE user_id = ?', (user_id,))
        return True

    def mute_user_get(self):
        self.setup()
        res = self.cursor.execute('SELECT user_id FROM cmd_mute')
        data = res.fetchall()
        return data

    # メンバー参加通知
    def welcome_notice_set(self, guild_id):
        self.setup()
        self.cursor.execute('INSERT INTO welcome_notice VALUES (?)', (guild_id,))
        return True

    def welcome_notice_unset(self, guild_id):
        self.setup()
        self.cursor.execute('DELETE FROM welcome_notice WHERE guild_id = ?', (guild_id,))
        return True

    def welcome_notice_get(self):
        self.setup()
        res = self.cursor.execute('SELECT guild_id FROM welcome_notice')
        data = res.fetchall()
        return data

    # メッセージURL展開
    def message_expand_set(self, guild_id):
        self.setup()
        self.cursor.execute('INSERT INTO msg_expand VALUES (?)', (guild_id,))
        return True

    def message_expand_unset(self, guild_id):
        self.setup()
        self.cursor.execute('DELETE FROM msg_expand WHERE guild_id = ?', (guild_id,))
        return True

    def message_expand_get(self):
        self.setup()
        res = self.cursor.execute('SELECT guild_id FROM msg_expand')
        data = res.fetchall()
        return data

    # ユーザー用ログ
    def member_log_set(self, guild_id, join_msg, left_msg, join_id, left_id):
        self.setup()
        self.cursor.execute('INSERT INTO member_log VALUES (?,?,?,?,?)',
                            (guild_id, join_msg, left_msg, join_id, left_id))
        return True

    def member_log_unset(self, guild_id):
        self.setup()
        self.cursor.execute('DELETE FROM member_log WHERE guild_id = ?', (guild_id,))
        return True

    def member_log_get(self, guild_id):
        self.setup()
        res = self.cursor.execute('SELECT * FROM member_log WHERE guild_id = ?', (guild_id,))
        data = res.fetchall()
        return data

    # TAOお助け機能
    def tao_help_set(self, guild_id, func, log_id, role_t):
        self.setup()
        self.cursor.execute('INSERT INTO tao_help VALUES (?,?,?,?)',
                            (guild_id, func, log_id, role_t))
        return True

    def tao_help_guild_get(self, guild_id):
        self.setup()
        res = self.cursor.execute('SELECT * FROM tao_help WHERE guild_id = ?', (guild_id,))
        data = res.fetchall()
        return data

    def tao_help_premium_set(self, guild_id, func, log_id, role_t, role_g, role_r, premium):
        self.setup()
        self.cursor.execute('INSERT INTO tao_help VALUES (?,?,?,?,?,?,?',
                            (guild_id, func, log_id, role_t, role_g, role_r, premium))
        return True

    def tao_help_del(self, guild_id):
        self.setup()
        self.cursor.execute('DELETE FROM tao_help WHERE guild_id = ?', (guild_id,))
        return True

    def tao_help_change(self, guild_id, func):
        self.setup()
        self.cursor.execute('UPDATE tao_help SET func = ? WHERE guild_id = ? ', (func, guild_id))
        return True

    def tao_help_get(self):
        self.setup()
        res = self.cursor.execute('SELECT guild_id FROM tao_help WHERE func = "on"')
        data = res.fetchall()
        return data

    def tao_help_premium_get(self):
        self.setup()
        res = self.cursor.execute('SELECT guild_id FROM tao_help WHERE premium = "on"')
        data = res.fetchall()
        return data
