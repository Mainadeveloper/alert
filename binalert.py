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
model = joblib.load("rf_model.pkl")
feature_columns = joblib.load("feature_columns.pkl")

# Load mappings
month_mapping = joblib.load("month_mapping.pkl")
event_type_mapping = joblib.load("event_type_mapping.pkl")

print("Model, feature columns, and mappings loaded successfully!")

# ThingsSpeak config
THINGSPEAK_WRITE_API_KEY = "2E1NW7LV3SGFIBPU"
THINGSPEAK_URL = "https://api.thingspeak.com/update"
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
        print("Could not fetch bin level/waste weight.")
        bin_level = "N/A"
        real_waste_weight = "N/A"
except Exception as e:
    print(f"Error fetching real-time data: {e}")
    bin_level = "N/A"
    real_waste_weight = "N/A"

# Recommendation logic
def generate_recommendation(waste_weight):
    try:
        weight = float(waste_weight)
    except:
        return "No actionable recommendation due to missing or invalid waste weight."

    if weight < 2:
        return "Great job! Minimal food waste today. Continue with your current food planning approach."
    elif weight < 5:
        return random.choice([
            "Consider slightly reducing portion sizes for supper.",
            "Repurpose leftovers for staff meals or the next day's menu.",
            "Conduct a brief survey to identify unpopular menu items."
        ])
    elif weight < 10:
        return random.choice([
            "Consider partnering with local farmers to convert food scraps into animal feed.",
            "Explore ways to better match food preparation with actual demand trends.",
            "Launch a small awareness campaign for students on mindful consumption."
        ])
    else:
        return random.choice([
            "High waste detected! Consider composting or turning excess into organic manure for campus gardens.",
            "Explore food donation programs with local shelters or needy communities.",
            "Use this data to redesign the menu and reduce surplus production.",
            "Introduce a smart food ordering system to avoid overproduction."
        ])

# Send alert only when bin is 10cm or 0cm
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

 Waste Bin Alert

The bin is currently at {bin_level} cm.
Actual Waste: {real_waste_weight} kg

Recommended Action:
{advice}

Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}

Regards,
Smart Waste Monitoring System
""")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print("Email alert sent successfully!")
    else:
        print(f"No alert sent. Bin level is {bin_level} cm.")
except Exception as e:
    print(f"Error processing bin level or sending email: {e}")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




