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

    # Collect high quality sounds (there are ~15 results per page and only high rated sounds are selected)
    # Loop terminates after 5th page is read, limits the number of api calls in loop (max 4 api calls to next_page() inside loop)
    page= 1
    while results_pager and len(hi_quality_sounds) < 30: 
        for sound in results_pager:
            if sound.num_ratings >= 3 and sound.avg_rating >= 4:
                hi_quality_sounds.append({"id": sound.id, "name": sound.name, "description": sound.description, "tags": sound.tags, "rating": sound.avg_rating})
        if page >= 5:
                break
        try:       
            results_pager= results_pager.next_page()
            page+= 1
        except Exception as e:
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
