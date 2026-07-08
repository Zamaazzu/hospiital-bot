# test_direct.py
import pymysql

try:
    connection = pymysql.connect(
        host='hayabusa.proxy.rlwy.net',
        port=50082,
        user='root',
        password='ZEGttbmtOYiXmGtYNdPeWAyIBlLfMOwF',  # replace this
        database='railway',
        connect_timeout=10
    )
    print("✓ Connection successful")
    connection.close()
except Exception as e:
    print(f"✗ Connection failed: {e}")