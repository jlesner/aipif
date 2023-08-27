#uses openai to generate keywords and select best sound id from sound descriptions

import os
import openai
import re
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator

openai.api_key= os.getenv('OPENAI_API_KEY')
temp_directory= os.getenv('TEMP_DIRECTORY')

def select_title(prompt):
    """ langchain uses openai to read sound data stored in `temp_directory` and recommend the sound id that best matches `prompt`.

    Args:
    -   `prompt`(string): prompt describing desired sound to be selected

    Returns:
        string: 6 digit response given by model, or first sound id from sound data (if model fails)
    """
    question = f"Provide a single valid sound id from the freesound data that best matches the following description: {prompt}."
    loader = TextLoader(f"{temp_directory}sound_data.txt")
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
            # Otherwise return first sound id from sound_data.txt
            response= extract_first_id(f'{temp_directory}sound_data.txt')  
    
    return response
 
def generate_keywords(prompt):
    """ use openai ChatCompletion to extract 3 keywords from `prompt`

    Args:
    -   `prompt`(string): text prompt describing a sound

    Returns:
        string: space separated collection of keywords describing `prompt`
    """
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
  
def extract_first_id(file_path):
    """ Extract first id from sound data in `file_path`

    Args:
    -   `file_path`(string): path to the file being read
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()[4:5]
    return lines[0].split(":")[1].strip().rstrip(',')

