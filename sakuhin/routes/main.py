# メイン機能のルーティングを管理するモジュール
# タスクの一覧表示と新規タスクの追加機能を提供

from flask import Blueprint, render_template, request, redirect, url_for
from db import init_db, get_db_connection

# Blueprintの作成
# url_prefixは指定しない（ルートURLにマッピング）
bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    """
    タスクの一覧表示と新規タスクの追加を行う関数
    
    機能：
    - GET: タスク一覧を表示（完了済み/未完了のフィルタリング対応）
    - POST: フォームから送信されたデータで新しいタスクを追加
    
    パラメータ：
    - show_completed: URLクエリパラメータ（'true'/'false'）
        - true: 完了済みタスクのみ表示
        - false: 未完了タスクのみ表示（デフォルト）
    - category: URLクエリパラメータ（'仕事'/'プライベート'/'all'）
        - 特定のカテゴリのタスクのみ表示
        - 'all': すべてのカテゴリを表示（デフォルト）
    """
    # データベースの初期化（テーブルが存在しない場合は作成）
    init_db()
    
    if request.method == 'POST':
        # フォームからデータを取得
        content = request.form['content']
        priority = request.form['priority']
        deadline = request.form['deadline']
        category = request.form['category']
        
        # タスク内容が入力されている場合のみデータベースに保存
        if content:
            conn = get_db_connection()
            conn.execute('INSERT INTO tasks (content, priority, deadline, category) VALUES (?, ?, ?, ?)',
                         (content, priority, deadline, category))
            conn.commit()
            conn.close()
        return redirect(url_for('main.index'))

    # フィルター設定を取得
    show_completed = request.args.get('show_completed', 'false') == 'true'
    selected_category = request.args.get('category', 'all')
    
    # データベースからタスクを取得
    conn = get_db_connection()
    
    # 基本のSQLクエリを構築
    query = 'SELECT * FROM tasks WHERE completed = ?'
    params = [1 if show_completed else 0]
    
    # カテゴリフィルターを適用
    if selected_category != 'all':
        query += ' AND category = ?'
        params.append(selected_category)
    
    # クエリを実行（新しい順）
    query += ' ORDER BY id DESC'
    tasks = conn.execute(query, params).fetchall()
    
    # カテゴリごとのタスク数を取得
    category_counts = conn.execute('''
        SELECT category, COUNT(*) as count 
        FROM tasks 
        WHERE completed = ? 
        GROUP BY category
    ''', [1 if show_completed else 0]).fetchall()
    
    conn.close()
    
    # テンプレートにデータを渡して表示
    return render_template('index.html', 
                         tasks=tasks, 
                         show_completed=show_completed,
                         selected_category=selected_category,
                         category_counts=category_counts)

@bp.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_complete(task_id):
    """
    タスクの完了状態を切り替える関数
    
    機能：
    - チェックボックスの状態変更に応じてタスクの完了状態を反転
    - 未完了(0) → 完了(1)、完了(1) → 未完了(0)
    
    パラメータ：
        task_id: 切り替えるタスクのID
    """
    conn = get_db_connection()
    # 完了状態を反転（0→1、1→0）
    conn.execute('UPDATE tasks SET completed = CASE completed WHEN 0 THEN 1 ELSE 0 END WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('main.index'))