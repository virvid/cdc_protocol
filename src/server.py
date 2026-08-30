import socket
import threading

HOST = '127.0.0.1'
PORT = 5005
PROTOCOL = "CDCP/1.0"

subscriptions = {}
subscriptions_lock = threading.Lock()

def handle_client(conn, addr):
    print(f"\n[SERVER] New connection from {addr}")
    with conn:
        while True:
            try:
                data = conn.recv(4096)
                if not data:
                    break
                
                raw_message = data.decode('utf-8')
                parts = raw_message.split('\r\n\r\n')
                headers = parts[0].split(' ')
                command = headers[0]
                
                print(f"[SERVER] Received Request: {parts[0]}")
                
                if command == "SUBSCRIBE":
                    table_name = headers[1]
                    with subscriptions_lock:
                        if table_name not in subscriptions:
                            subscriptions[table_name] = []
                        subscriptions[table_name].append(conn)
                    
                    response = f"{PROTOCOL} 200 SUBSCRIBED\r\n\r\n"
                    print(f"[SERVER] Sending Status Response: {PROTOCOL} 200 SUBSCRIBED")
                    conn.sendall(response.encode('utf-8'))
                    
                elif command == "PUBLISH":
                    table_name = headers[1]
                    operation = headers[2]
                    payload = parts[1] if len(parts) > 1 else ""
                    
                    # 1. w/ Publisher
                    response = f"{PROTOCOL} 201 PUBLISHED\r\n\r\n"
                    print(f"[SERVER] Sending Status Response: {PROTOCOL} 201 PUBLISHED")
                    conn.sendall(response.encode('utf-8'))
                    
                    # 2. w/ Subscriber
                    event_msg = f"EVENT {table_name} {operation}\r\n\r\n{payload}"
                    with subscriptions_lock:
                        if table_name in subscriptions:
                            for sub_conn in list(subscriptions[table_name]):
                                try:
                                    sub_conn.sendall(event_msg.encode('utf-8'))
                                except:
                                    subscriptions[table_name].remove(sub_conn)

                else:
                    response = f"{PROTOCOL} 400 BAD_REQUEST\r\n\r\n"
                    print(f"[SERVER] Sending Error Response: {PROTOCOL} 400 BAD_REQUEST")
                    conn.sendall(response.encode('utf-8'))
                    
            except ConnectionResetError:
                break
    print(f"\n[SERVER] Connection closed: {addr}")

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[SERVER] CDC Broker listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    start_server()
