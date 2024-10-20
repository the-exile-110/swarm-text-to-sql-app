
import re
from tabulate import tabulate
import sqlite3

def clean_sql_query(sql_query: str) -> str:
    """SQLクエリをクリーンアップし、可能なMarkdown形式と余分な空白を削除する"""
    cleaned = re.sub(r'```sql\s*|\s*```', '', sql_query).strip()
    return cleaned


def format_results(results, description) -> str:
    """クエリ結果をフォーマットし、コンテキストと単位を追加する"""
    if isinstance(results, str):
        return results
    
    if not results or not description:
        return "一致する結果が見つかりませんでした。"
    
    headers = [desc[0] for desc in description]
    
    # 入場料に単位を追加
    if 'admission_fee' in headers:
        fee_index = headers.index('admission_fee')
        results = [list(row) for row in results]
        for row in results:
            row[fee_index] = f"{row[fee_index]}円" if row[fee_index] > 0 else "無料"
    
    formatted_results = tabulate(results, headers=headers, tablefmt="grid")
    
    return formatted_results


def execute_sql(sql_query: str, cursor) -> tuple:
    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        return results, cursor.description
    except sqlite3.Error as e:
        return f"SQLエラー: {e}", None