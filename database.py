from sqlite3 import connect, Row

DATABASE = "ssd_api.db"

def get_db_connection():
    conn = connect(DATABASE)
    conn.row_factory = Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email    TEXT NOT NULL
        )
        """
    )

    cursor.execute("INSERT OR IGNORE INTO users (username, email) VALUES ('Eldar', 'e.mametov@innopolis.university')")
    cursor.execute("INSERT OR IGNORE INTO users (username, email) VALUES ('Artem', 'a.bulgakov@innopolis.university')")
    cursor.execute("INSERT OR IGNORE INTO users (username, email) VALUES ('Aleksandr', 'a.ryabov@innopolis.university')")
    cursor.execute("INSERT OR IGNORE INTO users (username, email) VALUES ('Ruslan', 'r.belkov@innopolis.university')")
    cursor.execute("INSERT OR IGNORE INTO users (username, email) VALUES ('Mikhail', 'm.voronin@innopolis.university')")
    conn.commit()
    conn.close()