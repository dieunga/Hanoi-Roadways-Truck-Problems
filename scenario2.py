import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#User input (make sure it is a CSV file or an Excel file)
while True:
    path_file = input("Enter your file's path (CSV or EXCEL): ")
    if path_file.endswith('.csv'):
        df = pd.read_csv(path_file)
        print("Data received!")
        break 
    elif path_file.endswith('.xlsx'):
        df = pd.read_excel(path_file)
        print("Data received!")
        break
    else:
        print("Invalid file type. Please re-enter your file's path")

#Get necessary data
destinations = df["Destination"].unique().tolist()
coordinates_arr = np.array([
    [20.8443, 106.6883],  # Hải Phòng
    [16.0471, 108.2068],  # Đà Nẵng
    [12.2388, 109.1967],  # Nha Trang
    [11.9400, 108.4550],  # Đà Lạt
    [10.8231, 106.6297]   # TP.HCM
])

coordinates = {}
for city, coor in zip(destinations, coordinates_arr):
    coordinates[city] = [coor]
#Add the starting point's name and coordinates to the list
coordinates["Hanoi"] =  [[21.0285, 105.8542]]

#Sort cities to find to route plan
def route_plan(df, destination_col, distance_col):
    #df is a DataFrame, with Destination column (destination_col) and Distance column (distance_col)
    destinations_dict = dict(zip(df[destination_col], df[distance_col]))
    sorted_destinations = dict(sorted(destinations_dict.items(), key=lambda item: item[1]))

    route_plan = list(sorted_destinations.keys())
    # route_plan = ' -> '.join(route_plan)
    return route_plan, sorted_destinations


#Backup map
def backup_map(sorted_destination, start_destination, coordinates):
    #sorted_destination is dictionary, start_destination is the name of the starting city
    sorted_cities = [start_destination] + list(sorted_destination.keys())

    #Draw cities as dots 
    for city, coor in coordinates.items():
        y, x = coor[0]  
        if city == start_destination:
            plt.plot(x, y, label=city, ms=15, marker='o', color='y')  #Starting point is yellow
        else:
            plt.plot(x, y, label=city, ms=10, marker='o')  #The rest are randomly colored

        #Include city names and coordinates
        plt.text(x-0.2, y+1.5, city, fontsize=10)  
        plt.text(x-0.3, y+1, coor[0], fontsize=5)  

    #Draw line connect the cities as the route plan
    for i in range(len(sorted_cities)-1):
        starting_point = sorted_cities[i]
        ending_point = sorted_cities[i+1]

        start_y, start_x = coordinates[starting_point][0]
        end_y, end_x = coordinates[ending_point][0]

        plt.plot([start_x, end_x], [start_y, end_y], 'c--')

    plt.title('Backup Map')
    plt.xlabel('Longtitude')
    plt.ylabel('Langtitude')

    plt.xlim(105, 110)
    plt.ylim(5, 30)
    #The figure will pop up for the user to see
    plt.show()
    
route_plan_output, sorted_cities = route_plan(df, 'Destination', 'Distance (km)')
backup_map_output = backup_map(sorted_cities, 'Hanoi', coordinates)

#User inputs for route plan
user_choice1 = input("Do you want to export Route Plan? (y/n): ")
user_choice1 = user_choice1.lower()
if user_choice1 in ['y', 'yes']:
    print('='*20 + 'ROUTE PLAN' + '='*20)
    print(' - '.join(route_plan_output))

#User inputs for backup map
user_choice2 = input("Do you want to export Backup Map? (y/n): ")
user_choice2 = user_choice2.lower()
if user_choice2 in ['y', 'yes']:
    file_export = input("Type desired file name: ")
    plt.savefig(f"{file_export}.png")