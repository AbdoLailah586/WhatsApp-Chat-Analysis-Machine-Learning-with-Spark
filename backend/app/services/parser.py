import re
import pandas as pd
from datetime import datetime
from typing import List, Dict

def parse_whatsapp(file_content: str) -> List[Dict]:
    pattern = re.compile(
        r"^\[?(?P<date>\d{1,4}[-./]\d{1,2}[-./]\d{1,4})[, ]\s*(?P<time>\d{1,2}:\d{2}(?::\d{2})?\s*(?:[aApP]\.?[mM]\.?)?)\]?\s*[-]?\s*(?P<sender>[^:]+):\s*(?P<message>.*)$",
        re.IGNORECASE,
    )
    messages = []
    current_msg = None

    for line in file_content.splitlines():
        match = pattern.match(line)
        if match:
            if current_msg:
                messages.append(current_msg)
            date_str = match.group("date")
            time_str = match.group("time")
            sender = match.group("sender").strip()
            text = match.group("message").strip()
            
            is_media = False
            if text == "<Media omitted>":
                is_media = True
                
            try:
                timestamp = pd.to_datetime(f"{date_str} {time_str}", dayfirst=False, errors='coerce')
                if pd.isna(timestamp):
                    timestamp = datetime.utcnow()
                else:
                    timestamp = timestamp.to_pydatetime()
            except:
                timestamp = datetime.utcnow()

            current_msg = {
                "timestamp": timestamp,
                "sender": sender,
                "content": text,
                "is_media": is_media
            }
        else:
            if current_msg:
                current_msg["content"] += "\n" + line.strip()

    if current_msg:
        messages.append(current_msg)

    return messages
