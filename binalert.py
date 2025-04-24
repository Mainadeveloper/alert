#!/usr/bin/env python3
# coding: utf-8

# In[39]:


import smtplib
import joblib
import requests
import time
import pandas as pd
from email.message import EmailMessage
import random

# Load model and features
import smtplib
import joblib
import requests
import time
import pandas as pd
from email.message import EmailMessage
import random

def run_alert():
    # Load model and features
    try:
        model = joblib.load("rf_model.pkl")
        feature_columns = joblib.load("feature_columns.pkl")
        month_mapping = joblib.load("month_mapping.pkl")
        event_type_mapping = joblib.load("event_type_mapping.pkl")
        print("Model, feature columns, and mappings loaded successfully!")
    except Exception as e:
        return f"Error loading model or files: {e}"

    # ThingsSpeak config
    THINGSPEAK_WRITE_API_KEY = "2E1NW7LV3SGFIBPU"
    CHANNEL_ID = "2907621"
    THINGSPEAK_READ_API_KEY = "QCKQ0U2RWLTYZ2H9"
    fetch_url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={THINGSPEAK_READ_API_KEY}&results=1"

    # Email config
    sender_email = "maina17fay@gmail.com"
    sender_password = "dcrx ewuy tfbl qyyj"
    receiver_email = "ifrahfarah48@gmail.com"

    # Fetch data
    time.sleep(10)
    try:
        fetch_response = requests.get(fetch_url)
        if fetch_response.status_code == 200:
            feed = fetch_response.json()['feeds'][0]
            bin_level = feed['field1']
            real_waste_weight = feed['field2']
        else:
            return "Failed to fetch data from ThingSpeak."
    except Exception as e:
        return f"Error fetching ThingSpeak data: {e}"

    # Recommendation logic
    def generate_recommendation(waste_weight):
        try:
            weight = float(waste_weight)
        except:
            return "No actionable recommendation due to invalid waste weight."

        if weight < 2:
            return "Minimal food waste today. Great job!"
        elif weight < 5:
            return random.choice([
                "Consider reducing supper portions.",
                "Repurpose leftovers for next day.",
                "Ask students about unpopular meals."
            ])
        elif weight < 10:
            return random.choice([
                "Partner with farmers for food scrap use.",
                "Match preparation with trends.",
                "Educate students on waste reduction."
            ])
        else:
            return random.choice([
                "Compost excess food or donate to shelters.",
                "Redesign menu to reduce waste.",
                "Use smart food ordering systems."
            ])

    try:
        bin_level_float = float(bin_level)
        if bin_level_float in [10.0, 0.0]:
            advice = generate_recommendation(real_waste_weight)

            msg = EmailMessage()
            msg['Subject'] = "Smart Waste Monitoring Alert"
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg.set_content(f"""
Dear Restaurant Owner,

Waste Bin Alert!

Bin Level: {bin_level} cm
Waste Weight: {real_waste_weight} kg

Recommended Action:
{advice}

Time: {time.strftime('%Y-%m-%d %H:%M:%S')}

Smart Waste Monitoring System
""")
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, sender_password)
                server.send_message(msg)
            return "Email alert sent successfully!"
        else:
            return f"No alert sent. Bin level is {bin_level} cm."
    except Exception as e:
        return f"Error sending email or processing data: {e}"

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




