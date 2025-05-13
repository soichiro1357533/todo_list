# タスク編集機能のルーティングを管理するモジュール
# 既存タスクの内容、優先度、期日、カテゴリの編集機能を提供

from flask import Blueprint, render_template, request, redirect, url_for
from db import get_db_connection

# Blueprintの作成
# URLプレフィックス'/edit'を指定
bp = Blueprint('edit', __name__, url_prefix='/edit')

@bp.route('/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    """
    タスクの編集機能を提供する関数
    
    機能：
    - GET: 編集フォームを表示（現在のタスク情報を初期値として設定）
    - POST: フォームから送信されたデータでタスクを更新
    
    パラメータ：
        task_id: 編集対象のタスクID
    
    処理の流れ：
    1. POSTリクエストの場合：
       - フォームから送信されたデータを取得
       - データベースの該当タスクを更新（内容、優先度、期日、カテゴリ）
       - 一覧画面にリダイレクト
    2. GETリクエストの場合：
       - データベースから該当タスクの情報を取得
       - 編集フォームを表示
    """
    conn = get_db_connection()
    if request.method == 'POST':
        # フォームから送信されたデータを取得
        content = request.form['content']
        priority = request.form['priority']
        deadline = request.form['deadline']
        category = request.form['category']  # カテゴリを取得
        
        # データベースの該当タスクを更新（カテゴリを含む）
        conn.execute('''
            UPDATE tasks 
            SET content = ?, priority = ?, deadline = ?, category = ? 
            WHERE id = ?
        ''', (content, priority, deadline, category, task_id))
        conn.commit()
        conn.close()
        return redirect(url_for('main.index'))
    
    # 編集対象のタスク情報を取得
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    conn.close()
    # 編集フォームを表示
    return render_template('edit.html', task=task)
