import json

# List to hold the transformed dictionaries
transformed_list = []


# Function to check if the item is a string that looks like an OpenAIObject JSON
def is_openaiobject_json_string(item):
    return isinstance(item, str) and item.startswith('<OpenAIObject at') and 'JSON: ' in item


# Function to extract and parse the JSON content from the string
def extract_json_from_string(item):
    json_str = item.split('JSON: ')[1]
    return json.loads(json_str)


# Iterate over the input list and transform it
def transform_msg_json(input_list):
    for item in input_list:
        if is_openaiobject_json_string(item):
            # Extract and parse the JSON content
            dict_item = extract_json_from_string(item)
            transformed_list.append(dict_item)
        else:
            # The item is already a dictionary, so just append it
            transformed_list.append(item)
    return transformed_list
