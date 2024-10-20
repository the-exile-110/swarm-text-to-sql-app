from swarm import Swarm, Agent
from utils import clean_sql_query, format_results, execute_sql

client = Swarm()

agent = Agent(
    name="SQLAgent",
    instructions="""
    あなたは日本語の自然言語クエリをSQLクエリに変換できるAIアシスタントです。
    データベースには3つのテーブルがあります:
    1. 'attractions'テーブル以下の列を含む:id, name, city_id, type, admission_fee
    2. 'cities'テーブル、以下の列を含む:id, name, prefecture
    3. 'reviews'テーブル、以下の列を含む:id, attraction_id, rating, comment, review_date
    SQLクエリのみを返し、他のテキストや説明を含めないでください。複雑なクエリをサポートし、複数テーブルの結合、比較、ソート、集計関数を含みます。
    """
)

explanation_agent = Agent(
    name="ExplanationAgent",
    instructions="""
    あなたはSQL専門家のAIアシスタントです。与えられたSQLクエリを非技術者にも分かりやすく説明することが任務です。
    クエリの目的、関連するテーブル、使用される操作（結合、フィルタリング、ソートなど）、期待される結果を含む、簡潔かつ包括的な説明をMarkdown形式で提供してください。
    説明のみを返し、他の内容は含めないでください。
    """
)

def explain_query(sql_query: str) -> str:
    """AIを使用してSQLクエリの説明を生成する"""
    response = client.run(
        agent=explanation_agent,
        messages=[{"role": "user", "content": f"以下のSQLクエリを説明してください：\n\n{sql_query}"}],
    )
    print(response.messages[-1]["content"])
    return response.messages[-1]["content"]

def process_query(natural_language_query: str, cursor) -> dict:
    """自然言語クエリを処理し、SQLに変換し、実行して結果を返す"""
    # Swarmを使用して自然言語をSQLに変換
    response = client.run(
        messages=[{"role": "user", "content": natural_language_query}],
        agent=agent,
    )
    sql_query = clean_sql_query(response.messages[-1]["content"])
    
    # SQLクエリを実行
    results, description = execute_sql(sql_query, cursor)
    
    # クエリの説明を取得
    explanation = explain_query(sql_query)
    
    # 結果をフォーマット
    formatted_results = format_results(results, description)
    
    return {
        "sql_query": sql_query,
        "explanation": explanation,
        "results": formatted_results
    }