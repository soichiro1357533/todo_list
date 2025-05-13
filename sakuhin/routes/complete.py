# タスク完了機能のルーティングを管理するモジュール
# タスクの完了状態を切り替える機能を提供

from flask import Blueprint, redirect, url_for
from db import get_db_connection

# Blueprintの作成
# URLプレフィックス'/complete'を指定
bp = Blueprint('complete', __name__, url_prefix='/complete')

@bp.route('/<int:task_id>')
def complete(task_id):
    """
    タスクの完了状態を切り替える関数
    
    機能：
    - 指定されたIDのタスクの完了状態を反転
    - 未完了(0) → 完了(1)、完了(1) → 未完了(0)
    - 状態変更後は一覧画面にリダイレクト
    
    パラメータ：
        task_id: 完了状態を切り替えるタスクのID
    
    注意：
    - この機能はmain.pyのtoggle_completeと重複
    - 将来的な機能拡張のために別ルートとして実装
    """
    conn = get_db_connection()
    # 完了状態を反転（0→1、1→0）
    conn.execute('UPDATE tasks SET completed = CASE completed WHEN 0 THEN 1 ELSE 0 END WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    # 一覧画面にリダイレクト
    return redirect(url_for('main.index'))
