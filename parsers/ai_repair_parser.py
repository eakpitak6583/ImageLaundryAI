import json
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# -----------------------------
# โหลด .env จากโฟลเดอร์หลักของโปรเจกต์
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# -----------------------------
# OpenAI Client
# -----------------------------
client = OpenAI()

# -----------------------------
# Prompt
# -----------------------------
SYSTEM_PROMPT = """
คุณเป็น AI สำหรับวิเคราะห์ใบงานซ่อมเครื่องซักผ้าอุตสาหกรรม

อ่านข้อความใบงานซ่อม 1 งาน

ให้คืนค่าเป็น JSON เท่านั้น

Schema

{
  "job_no":"",
  "machine_model":"",
  "complaint":"",
  "detail":"",
  "repair_action":"",
  "result":"",
  "sap_no":"",
  "serial_no":""
}

กฎ

- machine_model เช่น DI225, DP250, IM1200X3300X2
- ถ้าไม่มีข้อมูลให้คืน ""
- ห้ามอธิบาย
- ตอบเป็น JSON อย่างเดียว
"""

# -----------------------------
# Parse Repair Job
# -----------------------------
def parse_job(text: str):

    response = client.responses.create(
        model="gpt-5.5",
        input=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": text,
            },
        ],
    )

    return json.loads(response.output_text)