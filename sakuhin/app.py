# Flaskアプリケーションのメインファイル
# アプリケーションの初期化とBlueprintの登録を行う

from flask import Flask
from routes import main, edit, complete, delete

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)

# 各機能のBlueprintを登録
app.register_blueprint(main.bp)      # メイン機能（一覧表示・タスク追加）
app.register_blueprint(edit.bp)      # タスク編集機能
app.register_blueprint(complete.bp)  # タスク完了機能
app.register_blueprint(delete.bp)    # タスク削除機能

# アプリケーションの実行
if __name__ == '__main__':
    # デバッグモードを有効にして開発サーバーを起動
    app.run(debug=True)
