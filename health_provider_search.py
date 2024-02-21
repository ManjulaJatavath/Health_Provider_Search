import requests
import json
import csv
import zipfile

#  URL for the API
api_url = "https://intake.steerhealth.io/api/doctor-search"

# Set the desired page size for the results
page_size = 648

# Payload for the API request
payload_api = json.dumps({
    "name": "",
    "title": "MD",
    "phone": "",
    "location": "",
    "education": "",
    "expertise": "Heart Health",
    "speciality": "",
    "organizationId": "aa1f8845b2eb62a957004eb491bb8ba70a",
    "size": page_size,
    "page": 0
})

# Headers for API request
headers = {
    'Content-Type': 'application/json'
}

# Make the API request and get the response
print("Making API request...")
response_api = requests.post(api_url, headers = headers, data=payload_api)
#print(response_api)
# Parse the API response as JSON
api_data = json.loads(response_api.text)

# List to store dictionaries of providers
providers_list = []

# Loop through all items in the API response
print("Processing providers...")
for item in api_data.get('items', []):
    provider_details = {}

    # Name section
    provider_details["Name"] = f"{item.get('firstName')} {item.get('lastName')}"

    # Title section
    titles = item.get('specialty', [])
    provider_details["Speciality"] = titles[0] if titles else ''

    # Extract gender information
    gender_code = item.get('gender', '')
    provider_details["Gender"] = 'Male' if gender_code == 'M' else 'Female'

    # Expertise information
    provider_details["Expertise"] = titles[1] if len(titles) > 1 else ''

    # Phone information
    addresses = item.get('addresses', [])
    provider_details["Phone"] = addresses[0].get('phoneNumber', '') if addresses else ''

    # Address information
    address_info = addresses[0] if addresses else {}
    
    # Separate 'Location' and 'Education' into separate columns
    provider_details["Education"] = address_info.get('name', '')
    provider_details["Location"] = address_info.get('address', '')

    # Append the provider information to the main list
    providers_list.append(provider_details)

# Save the provider list to a CSV file
csv_filename = "all_providers.csv"
keys = providers_list[0].keys()
with open(csv_filename, "w") as file:
    csvwriter = csv.DictWriter(file, keys)
    csvwriter.writeheader()
    csvwriter.writerows(providers_list)

# the provider list to JSON
json_filename = "all_providers.json"
with open(json_filename, "w") as json_file:
    json.dump(providers_list, json_file, indent=4)

# Zip  files
zip_filename = "output_files.zip"
with zipfile.ZipFile(zip_filename, 'w') as zip_file:
    zip_file.write(csv_filename)
    zip_file.write(json_filename)

print(f"Files saved and zipped to {zip_filename}")
print("Done")





