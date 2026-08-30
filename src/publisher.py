import socket
import json
import select
import psycopg2
import psycopg2.extensions

HOST = '127.0.0.1'
PORT = 5005

DB_CONFIG = {
    "dbname": "postgres",
    "user": "user",
    "password": "1234",
    "host": "127.0.0.1",
    "port": 5432
}

def send_to_broker(s, table, operation, data):
    payload = json.dumps(data)
    
    # 1. Request Message
    request = f"PUBLISH {table} {operation}\r\n\r\n{payload}"
    print("="*50)
    print(f"[PUBLISHER] Sending Request Protocol:\n{request.strip()}")
    print("-" * 50)
    
    s.sendall(request.encode('utf-8'))
    
    # 2. Status Response from Server
    response = s.recv(1024).decode('utf-8').strip()
    print(f"[PUBLISHER] Received Status Response:\n{response}")
    print("="*50 + "\n")

def start_pg_publisher():
    broker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    broker_socket.connect((HOST, PORT))
    print(f"[PUBLISHER] Connected to Server at {HOST}:{PORT}")

    conn = psycopg2.connect(**DB_CONFIG)
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    cursor.execute("LISTEN cdc_channel;")
    print("[PUBLISHER] Listening for PostgreSQL changes on 'cdc_channel'...\n")

    try:
        while True:
            if select.select([conn], [], [], 5) == ([], [], []):
                pass
            else:
                conn.poll()
                while conn.notifies:
                    notify = conn.notifies.pop(0)
                    event = json.loads(notify.payload)
                    send_to_broker(broker_socket, event['table'], event['operation'], event['data'])
    except KeyboardInterrupt:
        print("\n[PUBLISHER] Stopping.")
    finally:
        cursor.close()
        conn.close()
        broker_socket.close()

if __name__ == "__main__":
    start_pg_publisher()
