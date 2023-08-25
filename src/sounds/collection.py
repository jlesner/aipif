#uses freesound api to collect sounds in sounds.txt and download sound previews to SoundFiles directory

import os
import freesound
    
freesound_client = freesound.FreesoundClient()
freesound_client.set_token(os.getenv('FREESOUND_API_KEY'))

# Collect sounds from a text based query to freesound and write results to sounds.txt file
def collect_sounds(prompt):
    hi_quality_sounds= []
    results_pager = freesound_client.text_search(
        query=prompt,
        filter="duration:[1.0 TO 8.0] license:\"Creative Commons 0\"",
        sort="score",
        fields="id,name,score,avg_rating,description,tags,num_ratings"
    )

    #collect at least 50 high quality sounds (actually closer to 60 bc there are ~15 results per page and only high rated sounds are selected)
    while results_pager and len(hi_quality_sounds) < 50: 
        for sound in results_pager:
            if sound.num_ratings >= 3 and sound.avg_rating >= 4:
                hi_quality_sounds.append({"id": sound.id, "name": sound.name, "description": sound.description, "tags": sound.tags, "rating": sound.avg_rating})
        try:        
            results_pager= results_pager.next_page()
        except Exception as e:
            #print(f"error: {e}")
            #print(f"len sounds: {len(hi_quality_sounds)}")
            pass
        
    # write sound titles with descriptions and tags into sounds.txt
    write_to_file(hi_quality_sounds, 'SoundFiles/sounds.txt')
        
# Download sound preview to SoundFiles directory
def preview_sound(sound_id):
    sound = freesound_client.get_sound(
        sound_id, fields="previews"
    )
    sound.retrieve_preview(directory="SoundFiles/", name=f"{sound_id}")

# Write sound_list to file_path
def write_to_file(sound_list, file_path):
    with open(file_path, 'w') as file:
        file.write("This data represents sounds from freesound and their descriptions.\n\n")
        for sound_obj in sound_list:
            file.write('{\n')
            for field, val in sound_obj.items():
                if field == 'tags':
                    file.write("tags: ")
                    delim= ""
                    for tag in val:
                        file.write(f"{delim}{tag} ")
                        delim= ", "
                    file.write("\n")
                elif field == 'description':
                    # don't include long descriptions
                    if not "\n" in val:
                        file.write(f"{field}: {val}\n")
                else:
                    file.write(f"{field}: {val}\n")
            file.write('}\n\n')

'''
import requests
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# Obtain an access token programmatically using the client credentials flow
def get_access_token():
    auth_url = 'https://freesound.org/apiv2/oauth2/authorize/'
    data = {
        'client_id': CLIENT_ID,
        'response_type': 'code'
    }
    response = requests.get(auth_url, data=data)
    print(f"response: {response}")
    print(f"response text: {response.text}\n")
    
    access_token = response.json().get('access_token')
    print(f"token: {access_token}")
    return access_token

# Download a sound using the obtained access token
def download_sound(sound_id, access_token):
    sound_url = f'https://freesound.org/apiv2/sounds/{sound_id}/download/'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(sound_url, headers=headers)

    if response.status_code == 200:
        # Extract the filename from the response headers
        filename = response.headers.get('content-disposition')
        if filename:
            filename = filename.split('filename=')[-1].strip('"')
        else:
            filename = 'sound'  # Default filename if content-disposition is not available

        # Determine the file extension based on the filename
        file_extension = os.path.splitext(filename)[1]

        # Save the downloaded content to a file
        with open(f'sound{file_extension}', 'wb') as f:
            f.write(response.content)
        print('Sound downloaded successfully!')
    else:
        print(response)
        print('Failed to download sound.')
'''