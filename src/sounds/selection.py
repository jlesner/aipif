#uses openai to generate keywords and select best sound id from sound descriptions

import os
import openai
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.vectorstores import Chroma
import constants
import json

openai_key= constants.APIKEY_GPT
os.environ["OPENAI_API_KEY"] = openai_key
openai.api_key = openai_key

# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = False

#langchain uses openai to read sounds.txt and responds with sound_id for a sound that fits to the prompt
def select_title(prompt):
    query = f"Provide a valid sound ID from the freesound JSON data that best matches the following description: {prompt}. Avoid responding with phrases like 'I don't know' or any unrelated text."

    if PERSIST and os.path.exists("persist"):
        print("Reusing index...\n")
        vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
        index = VectorStoreIndexWrapper(vectorstore=vectorstore)
    else:
        loader = TextLoader("SoundFiles/sounds.txt")
        #loader = DirectoryLoader("data/")
        if PERSIST:
          index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory":"persist"}).from_loaders([loader])
        else:
          index = VectorstoreIndexCreator().from_loaders([loader])

    response= index.query(query, llm= OpenAI())
    
    # Fallback in case model responds with "I don't know"
    if "I don't know" in response:
        #return first sound id from sounds.txt
        response= str(extract_first_id('SoundFiles/sounds.txt'))
        
    return response
        
      

# use openai ChatCompletion to extract 3 keywords from a prompt 
def generate_keywords(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Choose the appropriate engine
        messages=[
            {"role": "system", "content": "You will respond only with 3 keywords that capture the sound effect described in the prompt. The output should be in the form: keyword1 keyword2 keyword3. Do not repeat any keywords."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=20,  # length of generated text
        temperature=0.1,  # creativity of the output
        stop=None 
    )
    
    keywords = response.choices[0].message.content.replace(",[]", "")
    return keywords
  
def extract_first_id(file_path):
    # Read the contents of sounds.txt, skipping the first line
    with open(file_path, 'r') as file:
        lines = file.readlines()[1:]

    # Combine remaining lines into a single string and parse as JSON
    file_contents = ''.join(lines)
    data = json.loads(file_contents)

    # Access the "id" field of the first dictionary
    id_of_first_sound = data[0]["id"]

    #return type: int
    return id_of_first_sound
    
