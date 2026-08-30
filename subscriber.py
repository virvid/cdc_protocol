import socket
import json
import os
import uuid

HOST = '127.0.0.1'
PORT = 5005

os.makedirs("data_lake", exist_ok=True)


def start_subscriber():
    table_name = input("Enter table to subscribe (e.g., users_table, orders_table): ").strip()
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        
        # 1. Request Messsage
        request = f"SUBSCRIBE {table_name}\r\n\r\n"
        print("\n[SUBSCRIBER] Sending Request Protocol:")
        print(request.strip())
        s.sendall(request.encode('utf-8'))
        
        # 2. Status Response
        status_resp = s.recv(1024).decode('utf-8')
        print("-" * 50)
        print(f"[SUBSCRIBER] Received Status Response:\n{status_resp.strip()}")
        print("=" * 50)
        print(f"\n[SUBSCRIBER] Waiting for real-time events on '{table_name}'...\n")
        
        client_id = str(uuid.uuid4())[:6] # random number
        file_path = f"data_lake/{table_name}_{client_id}_cdc.jsonl"

        with open(file_path, "a", encoding="utf-8") as f:
            while True:
                data = s.recv(4096)
                if not data:
                    break
                    
                raw_message = data.decode('utf-8').strip()
                parts = raw_message.split('\r\n\r\n')
                header = parts[0]
                payload_str = parts[1] if len(parts) > 1 else "{}"
                
                # 3. Event Message
                print(">>> [SUBSCRIBER] Event Message Received:")
                print(f"Header:  {header}")
                
                if payload_str:
                    parsed_json = json.loads(payload_str)
                    print(f"Payload: {json.dumps(parsed_json, indent=2)}")
                print("-" * 50)
                
                # save
                header_parts = header.split(" ")
                if len(header_parts) > 2:
                    record = {"operation": header_parts[2], "data": parsed_json}
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")
                    f.flush()

if __name__ == "__main__":
    start_subscriber()
