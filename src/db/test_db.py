from database import get_db_engine

def test_connection():
    engine = get_db_engine()
    print(engine.connect())

if __name__ == "__main__":
    test_connection()