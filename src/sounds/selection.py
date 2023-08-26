#uses openai to generate keywords and select best sound id from sound descriptions

import os
import openai
import re
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator

openai.api_key= os.getenv('OPENAI_API_KEY')

#langchain uses openai to read sounds.txt and responds with sound_id for a sound that fits to the prompt
def select_title(prompt):
    question = f"Provide a single valid sound id from the freesound data that best matches the following description: {prompt}."
    loader = TextLoader("SoundFiles/sounds.txt")
    index = VectorstoreIndexCreator().from_loaders([loader])
    response= index.query(question, llm= OpenAI())
    
    # Fallback in case model responds with "I don't know" or responds in a complete sentence with sound id
    if "I don't know" in response or len(response) > 6:
        # Extract sound id using regex if sound id is present
        pattern= r'\d{6}'
        match = re.search(pattern, response)
        if match:
            response = match.group()
        else:
            # Otherwise return first sound id from sounds.txt
            response= extract_first_id('SoundFiles/sounds.txt')  
    
    return response

# use openai ChatCompletion to extract 3 keywords from a prompt 
def generate_keywords(prompt):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": "You are an assistant that will respond with only 3 keywords that best descibe the situation. Do not repeat any keywords."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=20,
        temperature=0.1,
        stop=None 
    )
    keywords = response.choices[0].message.content.replace(",", "")
    return keywords
  
# Extract first id from file_path
def extract_first_id(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()[2:]

    for line in lines:
        line = line.strip()
        if line.startswith("id: "):
            id_str = line[4:].strip()
            return id_str
