import pyodbc

def test_connection():
    try:
        ip_server = "192.168.56.1"
        username = "user1"
        password = "1"
        connection_query = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={ip_server},1433;"
            f"Database=FOTA;"
            f"UID={username};"
            f"PWD={password};"
            "Trusted_Connection=no"
        )
        conn = pyodbc.connect(connection_query)
        print("Kết nối thành công!")
    except pyodbc.Error as e:
        print("Lỗi kết nối cơ sở dữ liệu:", e)

test_connection()