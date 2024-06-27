import pandas as pd

df = pd.read_csv('mtsamples.csv')

import re

def clean_text(text):
    # Remove leading/trailing whitespace
    text = text.strip()
    
    # Remove leading punctuation
    text = re.sub(r'^[^\w\s]+', '', text)
    
    # Remove trailing punctuation
    text = re.sub(r'[^\w\s]+$', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def parse_text_to_dict(text):
    # Split the text into sections using uppercase words followed by a colon
    pattern = r'([A-Z\s]+:)'
    try:
        sections = re.split(pattern, text)
        
        # Initialize an empty dictionary
        result = {}
        
        # Iterate through the sections, skipping the first (empty) item
        for i in range(1, len(sections), 2):
            key = sections[i].strip().rstrip(':')
            value = sections[i+1].strip() if i+1 < len(sections) else ""
            value = clean_text(value)
            # Add to dictionary, handling duplicate keys by appending to a list
            if key in result:
                if isinstance(result[key], list):
                    result[key].append(value)
                else:
                    result[key] = [result[key], value]
            else:
                result[key] = value
    except:
        result = {}

    return result

# Apply the function to the 'transcription' column
df['transcription'] = df['transcription'].apply(parse_text_to_dict)
# get keys of all dictionaries in the transcription column
