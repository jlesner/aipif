import json

# List of tuples containing the emoji-decorated strings and hex strings
data = [
    ("🌟🍀🦄🍍🚀🎸", "097a99d0"),
    ("🎈🌵🦉🍉🚁🎻", "0caf2351"),
    ("🌕🍒🦎🍓🚂🎷", "0f3f26b6"),
    ("🎉🌻🦖🍏🚜🎺", "1306e381"),
    ("🌈🍋🦚🍇🚓🎶", "172f3386"),
    ("🎊🌼🦜🍔🚕🎵", "1843526c"),
    ("🌙🍎🦢🍩🚢🎤", "185f8db3"),
    ("🎋🍉🦋🍖🚤🎼", "1ad999b6"),
    ("🌠🍓🦗🍜🚘🎧", "1ef4bdbb"),
    ("🎍🍑🦘🍛🚖🎸", "22eb2a07"),
    ("🌌🍅🦙🍝🚍🎻", "27131044"),
    ("🎎🍈🦡🍞🚔🎷", "27378438"),
    ("🌑🍇🦒🍟🚐🎺", "2b5ea0b4"),
    ("🎏🍊🦓🍠🚑🎶", "34862083"),
    ("🌔🍎🦂🍡🚎🎵", "3afc8665"),
    ("🎐🍋🦔🍢🚛🎤", "40265b0e"),
    ("🌖🍌🦕🍣🚚🎼", "47b9da95"),
    ("🎒🍍🦏🍤🚜🎧", "4991422f"),
    ("🌓🍏🦜🍥🚝🎸", "4c5347f0"),
    ("🎑🍐🦑🍦🚞🎻", "4f99c6a8")
]

# Convert the list of tuples into a dictionary
data_dict = {key: value for key, value in data}

# Serialize the dictionary as a JSON string
json_str = json.dumps(data_dict, ensure_ascii=False, indent=4)

print(json_str)
