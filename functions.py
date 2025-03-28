# Author: Uvindu Perera
# Date: 10/12/2024
# Student ID: 20231320 w2119992

# Task A: Input Validation

def validate_date_input():
    """
    Prompts the user to input a valid date in the format DD/MM/YYYY.
    Validates the day, month, and year range and returns the file path
    and the formatted date string.
    """
    # Define the date components for user prompts
    dateList = ["DD", "MM", "YYYY"]

    # Keep prompting the user until valid input is provided
    while True:
        try:
            # Get the day and validate its range
            date = input(f"Please enter the day of the survey in the format {dateList[0]}:")
            if int(date) < 1 or int(date) > 31:
                print("Out of range - values must be in the range 1 and 31.")
                continue
            else:
                date = str(date)  # Convert to string for formatting

                # Validate the month
                while True:
                    try:
                        month = str(input(f"Please enter the month of the survey in the format {dateList[1]}:"))
                        if int(month) < 1 or int(month) > 12:
                            print("Out of range - values must be in the range 1 to 12.")
                            continue
                        else:
                            month = str(month)

                            # Validate the year
                            while True:
                                try:
                                    year = int(input(f"Please enter the year of the survey in the format {dateList[2]}:"))
                                    if year < 2000 or year > 2024:
                                        print("Invalid year. Must be between 2000 and 2024.")
                                        continue
                                    else:
                                        year = str(year)
                                        # Combine date components into a single string
                                        new_date = date + '/' + month + '/' + year

                                except ValueError:
                                    print("Integer required for the year.")
                                    continue
                                else:
                                    # Return the input date  
                                
                                    return  new_date

                    except ValueError:
                        print("Integer required for the month.")
                        continue

        except ValueError:
            print("Integer required for the day.")

def passing_file_path(date):
    #Passing the file_path ccording to user given date
    if date == '15/06/2024' or date=="15/6/2024":
        file_path = "traffic_data15062024.csv"
        return file_path
    elif date == '16/06/2024'or date=="16/6/2024":
        file_path = "traffic_data16062024.csv"
        return file_path  
    elif date == '21/06/2024'or date=="21/6/2024":
        file_path = "traffic_data21062024.csv"
        return file_path
    else:
        print("Date not found in records.")
        #validate__input()
    
    


# Task B: Process CSV Data
def process_csv_data(file_path):
    """
    Reads traffic data from a CSV file, filters it based on the date,
    and calculates various statistics about the vehicles and conditions.
    """
    # Initialize a dictionary to store traffic data 
    data = {
        "file_path":file_path,
        "vehicles": 0,
        "trucks": 0,
        "truckPercentage": 0,
        "electricVehicles": 0,
        "twoWheeled": 0,
        "buss": 0,
        "didntTurn": 0,
        "bicycles": 0,
        "aboveSpeedLimit": 0,
        "average_bikesPerHour": 0,
        "vehiclesInElm": 0,
        "scooters": 0,
        "scooterPercentage": 0,
        "vehiclesInHan": 0,
        "hourRangeInHan": [],
        "hourRangeInElm": [],
        "total_hours_in_han": [],
        "total_hours_in_elm": [],
        "max_num_of_vehicles_in_han": 0,
        "rain": 0
    }
    if file_path == "traffic_data15062024.csv":
        date = '15/06/2024'
             
    elif file_path == "traffic_data16062024.csv":
        date = '16/06/2024'
            
    elif file_path == "traffic_data21062024.csv":
        date = '21/06/2024'
            

    import csv

    # Open the CSV file
    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)

        # Process each row in the CSV file
        for line in csv_reader:
            if line["Date"] == date:
                data["vehicles"] += 1  # Count all vehicles

                # Increment specific counters based on conditions
                if line["VehicleType"] == "Truck":
                    data['trucks'] += 1
                    
                if line["elctricHybrid"] == "True":
                    data['electricVehicles'] += 1
                    
                if line["VehicleType"] in ["Motorcycle", "Bicycle", "Scooter"]:
                    data['twoWheeled'] += 1
                    
                if line["VehicleType"] == "Buss" and line["JunctionName"] == "Elm Avenue/Rabbit Road" and \
                        line["travel_Direction_out"] == "N":
                    data['buss'] += 1
                    
                if line["travel_Direction_in"] == line["travel_Direction_out"]:
                    data['didntTurn'] += 1
                    
                if line["VehicleType"] == "Bicycle":
                    data['bicycles'] += 1
                    data['average_bikesPerHour'] = round(data['bicycles'] / 24)
                    
                if int(line["JunctionSpeedLimit"]) < int(line["VehicleSpeed"]):
                    data['aboveSpeedLimit'] += 1
                    
                if line["JunctionName"] == "Elm Avenue/Rabbit Road":
                    data['vehiclesInElm'] += 1
                    data['hourRangeInElm'].append(int(line['timeOfDay'][:2]))
                    if line["VehicleType"] == "Scooter":
                        data['scooters'] += 1
                        
                if line["JunctionName"] == "Hanley Highway/Westway":
                    data['vehiclesInHan'] += 1
                    data['hourRangeInHan'].append(int(line['timeOfDay'][:2]))
                    
                if line['Weather_Conditions'] in ['Rain', 'Light Rain']:
                    data['rain'] += 1

        # Calculate additional statistics
        data['rain'] = round(data['rain'] /60)
        """To get the number of vehicles in an hour in Hanley Highway/Westway
        and Elm Avenue/Rabbit Road""" 
        for i in range(24):
            c = data['hourRangeInHan'].count(i)
            data['total_hours_in_han'].append(c)
            
            elm=data['hourRangeInElm'].count(i)
            data["total_hours_in_elm"].append(elm)
            
        data["max_num_of_vehicles_in_han"] = max(data['total_hours_in_han'])
        data['busiest_hour'] = data['total_hours_in_han'].index(data["max_num_of_vehicles_in_han"])
        data['scooterPercentage'] = round((data['scooters'] / data['vehiclesInElm']) * 100)
        data['truckPercentage'] = round((data['trucks'] / data['vehicles']) * 100)

        return data



def display_outcomes(outcome):
    """
    Collects data by calling input validation and processing functions,
    then displays the summarized outcomes.
    """
    stars = '***************************'
    output = f"""{stars}
data file selected is {outcome['file_path']}
{stars}
The total number of vehicles recorded for this date is {outcome['vehicles']} 
The total number of trucks recorded for this date is {outcome['trucks']} 
The total number of electric vehicles for this date is {outcome['electricVehicles']} 
The total number of two-wheeled vehicles for this date is {outcome['twoWheeled']} 
The total number of Busses leaving Elm Avenue/Rabbit Road heading North is {outcome['buss']} 
The total number of Vehicles through both junctions not turning left or right is {outcome['didntTurn']}  
The percentage of total vehicles recorded that are trucks for this date is {outcome['truckPercentage']}% 
The average number of Bikes per hour for this date is {outcome["average_bikesPerHour"]}

The total number of Vehicles recorded as over the speed limit for this date is {outcome['aboveSpeedLimit']}  
The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcome['vehiclesInElm']} 
The total number of vehicles recorded through Hanley Highway/Westway junction is {outcome['vehiclesInHan']} 
{outcome['scooterPercentage']}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters. 

The highest number of vehicles in an hour on Hanley Highway/Westway is {outcome['max_num_of_vehicles_in_han']} 
The most vehicles through Hanley Highway/Westway were recorded between {outcome['busiest_hour']}:00 and {outcome['busiest_hour'] + 1}:00  
The number of hours of rain for this date is {outcome['rain']} 
"""
    print(output)
    return output


# Task C: Saving the outcome to a text file
def save_results_to_file(outcomes, file_name="results.txt"):
    #Saves the summarized outcomes to a text file.
    try:
        with open(file_name, 'a+') as file:
            file.write('\n')
            file.write(outcomes)
    except FileNotFoundError:
        with open(file_name, "w+") as file:
            file.write(outcomes)




