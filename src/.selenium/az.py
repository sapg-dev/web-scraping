import json

# Function to add an initial empty apartment object to JSON data


# Function to add an initial empty apartment object to a JSON file
def add_empty_apartment_to_file(file_path):
    try:
        # Read existing JSON data from the file
        with open(file_path, 'r') as file:
            data_dict = json.load(file)

        # Add an empty apartment object
        data_dict["apartment"] = {}

        # Write the updated data back to the file
        with open(file_path, 'w') as file:
            json.dump(data_dict, file, indent=4)

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")

# Example usage
# Provide the path to your JSON file
json_file_path = 'path/to/your/json_file.json'

# Add an empty apartment object to the JSON file
add_empty_apartment_to_file(json_file_path)

add_empty_apartment_to_file('estate.json')