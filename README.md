# swarm-text-to-sql-app

## 概要
Swarmを使用して自然言語クエリをSQLクエリに変換し、データベースから結果を取得するアプリケーションです。

![image](/doc/image.png)

## 使用方法
1. このリポジトリをクローンします。
2. 必要なパッケージをインストールします。
```bash
pip install -r requirements.txt
```
3. アプリケーションを起動します。
```bash
export OPENAI_API_KEY=<your-openai-api-key>
uvicorn app:app --reload
```