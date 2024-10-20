import sqlite3
from contextlib import contextmanager

class Database:
    def __init__(self):
        self.conn = None

    @contextmanager
    def get_connection(self):
        if self.conn is None:
            self.conn = sqlite3.connect(':memory:', check_same_thread=False)
            self.init_db()
        try:
            yield self.conn
        finally:
            pass

    @contextmanager
    def get_cursor(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                yield cursor
            finally:
                cursor.close()

    def init_db(self):
        with self.get_cursor() as cursor:
            # 観光地テーブルの作成
            cursor.execute('''
            CREATE TABLE attractions (
                id INTEGER PRIMARY KEY,
                name TEXT,
                city_id INTEGER,
                type TEXT,
                admission_fee INTEGER
            )
            ''')

            # 都市テーブルの作成
            cursor.execute('''
            CREATE TABLE cities (
                id INTEGER PRIMARY KEY,
                name TEXT,
                prefecture TEXT
            )
            ''')

            # 観光地データの挿入
            attractions = [
                (1, '東京スカイツリー', 1, 'タワー', 2100),
                (2, '浅草寺', 1, '寺院', 0),
                (3, '大阪城', 2, '城', 600),
                (4, '道頓堀', 2, '繁華街', 0),
                (5, '金閣寺', 3, '寺院', 400),
                (6, '伏見稲荷大社', 3, '神社', 0),
                (7, '横浜中華街', 4, '繁華街', 0),
                (8, '箱根温泉', 5, '温泉', 500),
                (9, '富士山', 6, '山', 1000),
                (10, '札幌時計台', 7, '歴史的建造物', 200)
            ]
            cursor.executemany('INSERT INTO attractions VALUES (?,?,?,?,?)', attractions)

            # 都市データの挿入
            cities = [
                (1, '東京', '東京都'),
                (2, '大阪', '大阪府'),
                (3, '京都', '京都府'),  
                (4, '横浜', '神奈川県'),
                (5, '箱根', '神奈川県'),
                (6, '富士宮', '静岡県'),
                (7, '札幌', '北海道')
            ]
            cursor.executemany('INSERT INTO cities VALUES (?,?,?)', cities)

            # レビューテーブルの作成
            cursor.execute('''
            CREATE TABLE reviews (
                id INTEGER PRIMARY KEY,
                attraction_id INTEGER,
                rating INTEGER,
                comment TEXT,
                review_date DATE,
                FOREIGN KEY (attraction_id) REFERENCES attractions (id)
            )
            ''')

            # レビューデータの挿入
            reviews = [
                (1, 1, 5, '景色が素晴らしい！', '2023-05-01'),
                (2, 1, 4, '混んでいたが、価値がある', '2023-05-02'),
                (3, 2, 5, '歴史を感じる素晴らしい寺院', '2023-05-03'),
                (4, 3, 4, '大阪の象徴、素晴らしい', '2023-05-04'),
                (5, 4, 3, '賑やかで面白い', '2023-05-05'),
                (6, 5, 5, '美しい金閣寺、必見', '2023-05-06'),
                (7, 6, 4, '鳥居の並びが印象的', '2023-05-07'),
                (8, 7, 4, '美味しい中華料理がたくさん', '2023-05-08'),
                (9, 8, 5, 'リラックスできる温泉', '2023-05-09'),
                (10, 9, 5, '日本の象徴、絶景', '2023-05-10'),
                (11, 10, 3, '歴史的な建物だが、期待ほどではない', '2023-05-11')
            ]
            cursor.executemany('INSERT INTO reviews VALUES (?,?,?,?,?)', reviews)

            self.conn.commit()