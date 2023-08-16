parsed_data = json.loads(json_string)

print(parsed_data['acts'][0]['name']) 
print(parsed_data['acts'][0]['parts'][0]['sequences'][0]['description'])  



