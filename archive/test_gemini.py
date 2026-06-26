import google.generativeai as genai
import os

with open('gmni.env', 'r') as f:
    for line in f:
        if line.strip().startswith('api_key='):
            key = line.strip().split('=', 1)[1].strip('"\'')
            os.environ['GEMINI_API_KEY'] = key

genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel('gemini-2.5-flash')

try:
    response = model.generate_content('Hello')
    print('SUCCESS:', response.text)
except Exception as e:
    print('ERROR:', e)
