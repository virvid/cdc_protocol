# Real-time CDC Broker System 
ส่งงาน **Project 1: Socket Programming** ของรายวิชา **01418351 Computer Communications and Cloud Computing Principles**  
**ผู้จัดทำ:** นายวีรวิชญ์ นิธิศไพศาลกุล รหัสนิสิต 6710451313 หมู่ 200

## Documents
- [Report (PDF)](docs/project1_report.pdf)
- [Presentation (PDF)](docs/project1_presentation.pdf)

## Source Code & How to run
- โค้ดทั้งหมดอยู่ในโฟลเดอร์ `src/`

**การติดตั้ง Dependencies:**  
โปรเจกต์นี้ใช้ไลบรารีภายนอกคือ `psycopg2` สำหรับเชื่อมต่อ PostgreSQL โดยจัดการแพ็กเกจผ่าน `uv`

1. สร้าง Virtual Environment:
   `uv venv`
2. เปิดใช้งาน Virtual Environment:   
สำหรับ macOS / Linux: `source .venv/bin/activate`   
สำหรับ Windows (Command Prompt หรือ PowerShell): `.venv\Scripts\activate`
3. ติดตั้งไลบรารี:
   `uv pip install psycopg2-binary`

**วิธีรันโปรแกรม:**
1. รัน Server: `python src/server.py`
2. รัน Subscriber: `python src/subscriber.py`
3. รัน Publisher: `python src/publisher.py`

## VDO Link
https://youtu.be/Cq2Sjd9Q9dA