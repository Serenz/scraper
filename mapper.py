import re
import json

if __name__ == '__main__':
    with open('mercatino.txt', 'r') as f:
        content = f.read()
    result_dict = {}

    # Using regular expressions to extract data between <option></option> tags
    pattern = r'<option value="(\d+-[A-Z]{0,3})">([^<]+)<\/option>'
    matches = re.findall(pattern, content)

    # Populating the dictionary with extracted data
    for match in matches:
        value, text = match
        # result_dict[text] = int(value)  # Converting value to an integer
        result_dict[text] = value  # Converting value to an integer

    with open('zona.txt', 'w') as f:
        json.dump(result_dict, f, indent=4)  