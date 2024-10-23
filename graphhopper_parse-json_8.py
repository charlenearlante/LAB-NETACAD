import requests
import urllib.parse
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

route_url = "https://graphhopper.com/api/1/route?"
key = "780c5c3a-6226-4b9e-9732-b74fe8a71920"

def geocoding(location, key):
    while location == "":
        location = input(Fore.YELLOW + "Enter the location again: ")
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code

    print(Fore.CYAN + "Geocoding API URL for " + location + ":\n" + url)
    
    if json_status == 200 and len(json_data["hits"]) != 0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]
        country = json_data["hits"][0].get("country", "")
        state = json_data["hits"][0].get("state", "")
        
        new_loc = name
        if state:
            new_loc += f", {state}"
        if country:
            new_loc += f", {country}"
        
        print(Fore.CYAN + "Geocoding API URL for " + new_loc + f" (Location Type: {value})\n" + url)
    else:
        lat = "null"
        lng = "null"
        new_loc = location
        if json_status == 200:
            print(Fore.RED + f"Geocode API status: {json_status}\nError message: {json_data.get('message', 'No hits found')}")

    return json_status, lat, lng, new_loc

while True:
    print(Fore.YELLOW + "\n+++++++++++++++++++++++++++++++++++++++++++++")
    print(Fore.GREEN + "Vehicle profiles available on Graphhopper:")
    print(Fore.YELLOW + "+++++++++++++++++++++++++++++++++++++++++++++")
    print(Fore.GREEN + "car, bike, foot")
    print(Fore.YELLOW + "+++++++++++++++++++++++++++++++++++++++++++++")
    profile = ["car", "bike", "foot"]
    vehicle = input(Fore.YELLOW + "Enter a vehicle profile from the list above (or 'quit' to exit): ")
    
    if vehicle in ["quit", "q"]:
        break
    elif vehicle not in profile:
        vehicle = "car"
        print(Fore.RED + "No valid vehicle profile was entered. Using the car profile.")

    loc1 = input(Fore.YELLOW + "Starting Location: ")
    if loc1 in ["quit", "q"]:
        break
    orig = geocoding(loc1, key)
    
    loc2 = input(Fore.YELLOW + "Destination: ")
    if loc2 in ["quit", "q"]:
        break
    dest = geocoding(loc2, key)

    # After entering the destination, calculate and print route info
    print(Fore.CYAN + "=================================================")
    if orig[0] == 200 and dest[0] == 200:
        op = f"&point={orig[1]}%2C{orig[2]}"
        dp = f"&point={dest[1]}%2C{dest[2]}"
        paths_url = route_url + urllib.parse.urlencode({"key": key, "vehicle": vehicle}) + op + dp
        paths_status = requests.get(paths_url).status_code
        paths_data = requests.get(paths_url).json()
        print(Fore.CYAN + f"Routing API Status: {paths_status}\nRouting API URL:\n" + paths_url)

    print(Fore.CYAN + "=================================================")
    print(Fore.GREEN + f"Directions from {orig[3]} to {dest[3]} by {vehicle}")
    print(Fore.CYAN + "=================================================")

    if paths_status == 200:
        miles = paths_data["paths"][0]["distance"] / 1000 / 1.61
        km = paths_data["paths"][0]["distance"] / 1000
        sec = int(paths_data["paths"][0]["time"] / 1000 % 60)
        min = int(paths_data["paths"][0]["time"] / 1000 / 60 % 60)
        hr = int(paths_data["paths"][0]["time"] / 1000 / 60 / 60)
        
        print(Fore.YELLOW + f"Distance Traveled: {miles:.1f} miles / {km:.1f} km")
        print(Fore.YELLOW + f"Trip Duration: {hr:02d}:{min:02d}:{sec:02d}")
        print(Fore.CYAN + "=================================================")
        
        # Loop through instructions and print each with a separator
        for each in paths_data["paths"][0]["instructions"]:
            path = each["text"]
            distance_km = each["distance"] / 1000
            distance_miles = distance_km / 1.61
            print(Fore.GREEN + f"{path} ( {distance_km:.1f} km / {distance_miles:.1f} miles )")
            print(Fore.CYAN + "=================================================")

        print(Fore.CYAN + "=============================================")
    else:
        print(Fore.RED + f"Error message: {paths_data.get('message', 'Unknown error')}")
        print(Fore.RED + "*************************************************")

    # Ask user if they want to continue or quit
    continue_choice = input(Fore.YELLOW + "Would you like to enter a new route? (y/n): ")
    if continue_choice.lower() not in ['y', 'yes']:
        break
