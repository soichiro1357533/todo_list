# タスク削除機能のルーティングを管理するモジュール
# 指定されたタスクの削除機能を提供

from flask import Blueprint, redirect, url_for
from db import get_db_connection

# Blueprintの作成
# URLプレフィックス'/delete'を指定
bp = Blueprint('delete', __name__, url_prefix='/delete')

@bp.route('/<int:task_id>')
def delete(task_id):
    """
    タスクを削除する関数
    
    機能：
    - 指定されたIDのタスクをデータベースから削除
    - 削除後は一覧画面にリダイレクト
    
    パラメータ：
        task_id: 削除対象のタスクID
    
    注意：
    - 削除操作は取り消し不可
    - 完了済みタスクも削除可能
    """
    conn = get_db_connection()
    # 指定されたIDのタスクを削除
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    # 一覧画面にリダイレクト
    return redirect(url_for('main.index'))
