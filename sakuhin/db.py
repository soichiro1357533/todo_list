# データベース関連の処理を行うモジュール
# SQLiteデータベースの初期化と接続管理を担当

import sqlite3

def init_db():
    """
    データベースの初期化を行う関数
    - データベースファイルが存在しない場合は新規作成
    - tasksテーブルが存在しない場合は新規作成
    - テーブル構造：
        - id: タスクの一意の識別子（自動採番）
        - content: タスクの内容
        - priority: 優先度（低・普・高）
        - deadline: 期日
        - category: カテゴリ（仕事・プライベート）
        - completed: 完了状態（0: 未完了、1: 完了）
    """
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            priority TEXT NOT NULL,
            deadline TEXT,
            category TEXT,
            completed INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def get_db_connection():
    """
    データベースへの接続を取得する関数
    
    Returns:
        sqlite3.Connection: データベース接続オブジェクト
        - row_factoryをsqlite3.Rowに設定することで、
          カラム名でデータにアクセス可能
    """
    conn = sqlite3.connect('todo.db')
    conn.row_factory = sqlite3.Row
    return conn
