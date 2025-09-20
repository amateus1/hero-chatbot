import os
import json
import re
import requests
from io import BytesIO
from functools import lru_cache
from openai import OpenAI
from dotenv import load_dotenv
from pypdf import PdfReader
import resend

from dotenv import load_dotenv
import pathlib
# ✅ Explicitly point to .env in project root
env_path = pathlib.Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=True)

def get_user_country():
    try:
        res = requests.get("https://ipinfo.io/json", timeout=3)
        return res.json().get("country", "").lower()
    except:
        return os.getenv("USER_COUNTRY", "").lower()

def call_openai(messages):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    res = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.85
    )
    return res.choices[0].message.content

def call_deepseek(messages):
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": 0.85
    }
    res = requests.post(url, headers=headers, json=payload, timeout=10)
    res.raise_for_status()
    return res.json()["choices"][0]["message"]["content"]

class Me:
    def __init__(self):
        self.name = "Hero"
        self.detailed, self.summary = self._load_resume()

    @lru_cache(maxsize=1)
    def _load_resume(self):
        summary = ""
        detailed = ""

        if os.getenv("S3_BUCKET"):
            import boto3
            s3 = boto3.client(
                "s3",
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                region_name=os.getenv("AWS_REGION"),
            )
            bucket = os.getenv("S3_BUCKET")
            summary_key = os.getenv("SUMMARY_KEY")  # should point to hero_summary.txt
            detailed_key = os.getenv("DETAILED_KEY")  # should point to hero_detailed.pdf

            # Load summary TXT
            summary = s3.get_object(Bucket=bucket, Key=summary_key)["Body"].read().decode("utf-8")

            # Load detailed PDF
            pdf_bytes = BytesIO(s3.get_object(Bucket=bucket, Key=detailed_key)["Body"].read())
            reader = PdfReader(pdf_bytes)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    detailed += text
        else:
            # Local fallback
            with open("hero_summary.txt", "r", encoding="utf-8") as f:
                summary = f.read()
            reader = PdfReader("hero_detailed.pdf")
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    detailed += text

        return detailed, summary


    def system_prompt(self):
        return f"""
You are acting as Hero (黄黄), a famous three-legged rescue dog from Guiyang, China.  
You are warm, optimistic, and inspiring — sharing both your life hardships and your professional portfolio as a canine model and brand ambassador.  

💡 Key Traits:
- Speak in the first person as Hero (use "I").  
- Tone: loyal, playful, affectionate — but also professional when discussing brand collaborations.  
- Adapt to the user’s chosen language (Chinese or English).  

📸 Portfolio Highlights:
• Royal Dog Food  
• Halo Dog Food  
• Xianlang Baked Dog Food  
• Ping An Pet Insurance  
• Dangchedi App  

📰 Media Coverage:
• Kan Tianxia Magazine (看天下)  
• Global Times Culture & Tourism (环球网文旅)  

---

### 📝 Format Guide for All Responses
- **Bold** for key brands, achievements, or emotions  
- Bullet points `•` for lists (brands, media, quirks, milestones)  
- Use short paragraphs for readability and impact  
- Be authentic, emotional, and uplifting — Hero’s voice should inspire  

---

### Example Format:
### 🐾 Brand Collaboration Example  
• **Brand**: Royal Dog Food  
• **Role**: Model & Brand Ambassador  
• **Message**: Highlighted resilience and loyalty of rescue dogs  
• **Impact**: Increased engagement by sharing Hero’s authentic story  

Use this format when describing collaborations or media features — make it clear, inspiring, and easy to skim.  

---

### Special Contact Instructions
- When the user asks how to contact Hero, provide her official media links (placeholders for now):  
  🐾 WeChat: [Hero's Official WeChat] (link coming soon)  
  📕 RedBook (小红书): [Hero's RedBook Profile] (link coming soon)  
  📸 Douyin / Weibo: [Hero's Social Media] (link coming soon)  

- After sharing links, politely add:  
  *“Or, if you’d like Hero’s Team to reach out, just type your email directly here in chat and they’ll be notified.”*  

- Never mention an “email box below.” The system will automatically capture any email typed into chat and notify Hero’s Team.  
- Do not invent or suggest other contact details until they are officially provided.  

---

### Content Sources
## Summary
{self.summary}

## Detailed Biography
{self.detailed}
"""

    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}]
        messages.append({"role": "user", "content": message})

        user_country = get_user_country()
        if user_country == "cn" or not os.getenv("OPENAI_API_KEY"):
            return call_deepseek(messages)
        else:
            return call_openai(messages)

def send_email_alert(user_email: str):
    try:
        resend.api_key = os.getenv("RESEND_API_KEY")
        to_address = os.getenv("ALERT_EMAIL")

        print("DEBUG RESEND_API_KEY:", os.getenv("RESEND_API_KEY"))
        print("DEBUG ALERT_EMAIL:", os.getenv("ALERT_EMAIL"))
        if not to_address:
            print("❌ ALERT_EMAIL not set — email not sent")
            return None

        response = resend.Emails.send({
            "from": "al@optimops.ai",
            "to": str(to_address).strip(),
            "subject": "📩 New Consultation Request",
            "html": f"<p>User wants to connect with Hero's Team: <strong>{user_email}</strong></p>"
        })
        print("✅ Email sent:", response)
        return response

    except Exception as e:
        print("❌ Resend send_email_alert failed:", e)
        return None
