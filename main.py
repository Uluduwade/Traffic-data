# Author: Uvindu Perera
# Date: 10/12/2024
# Student ID: 20231320 w2119992

#importing functions and libraries
import tkinter as tk
import csv

current_data=None
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
                                    year = int(
                                        input(f"Please enter the year of the survey in the format {dateList[2]}:"))
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

                                    return new_date

                    except ValueError:
                        print("Integer required for the month.")
                        continue

        except ValueError:
            print("Integer required for the day.")


def passing_file_path(date):
    # Passing the file_path according to user given date
    if date == '15/06/2024' or date == "15/6/2024":
        file_path = "traffic_data15062024.csv"
        return file_path
    elif date == '16/06/2024' or date == "16/6/2024":
        file_path = "traffic_data16062024.csv"
        return file_path
    elif date == '21/06/2024' or date == "21/6/2024":
        file_path = "traffic_data21062024.csv"
        return file_path
    else:
        print("Date not found in records.")
        loop()


# Task B: Process CSV Data
def process_csv_data(file_path):
    """
    Reads traffic data from a CSV file, filters it based on the date,
    and calculates various statistics about the vehicles and conditions.
    """
    date=None
    # Initialize a dictionary to store traffic data 
    data = {
        "file_path": file_path,
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

    # Open the CSV file
    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)

        # Process each row in the CSV file
        for line in csv_reader:
            if line["Date"] == date:
                data["vehicles"] += 1  # Count all vehicles

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
        data['rain'] = round(data['rain'] / 60)
        """To get the number of vehicles in an hour in Hanley Highway/Westway
        and Elm Avenue/Rabbit Road"""
        for i in range(24):
            c = data['hourRangeInHan'].count(i)
            data['total_hours_in_han'].append(c)

            elm = data['hourRangeInElm'].count(i)
            data["total_hours_in_elm"].append(elm)

        data["max_num_of_vehicles_in_han"] = max(data['total_hours_in_han'])
        data['busiest_hour'] = data['total_hours_in_han'].index(data["max_num_of_vehicles_in_han"])
        data['scooterPercentage'] = round((data['scooters'] / data['vehiclesInElm']) * 100)
        data['truckPercentage'] = round((data['trucks'] / data['vehicles']) * 100)


        return data

def histogram(data, date):
    traffic_data = {
        "Elm Avenue/Rabbit Road": data["total_hours_in_elm"],
        "Hanley Highway/Westway": data["total_hours_in_han"]
    }
    current_data = traffic_data
    if current_data:
        app = HistogramApp(traffic_data, date, ask_for_another_date)
        app.run()

def ask_for_another_date():
    while True:
        user_input = input("Do you want to select another data file for a different date? Y/N > ").strip().lower()
        if user_input == 'n':
            print("End....")
            exit()
        elif user_input == 'y':
            execute()  # Call execute again to start the process for a new date
            break
        else:
            print("Invalid input. Please enter 'Y' or 'N'.")

def clear_previous_data(self):
    current_data = None


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
    # Saves the summarized outcomes to a text file.
    try:
        with open(file_name, 'a+') as file:
            file.write('\n')
            file.write(outcomes)
    except FileNotFoundError:
        with open(file_name, "w+") as file:
            file.write(outcomes)



#import functions as fun
# Task D : drawing the histogram
class HistogramApp:
    def __init__(self, traffic_data, date,close_callback):
        """
        Initializes the histogram application with the traffic data and selected date.
        """
        self.traffic_data = traffic_data
        self.date = date
        self.close_callback = close_callback
        self.root = tk.Tk()
        self.root.title(f"Histogram of Vehicle Frequency per Hour ({self.date})")
        self.root.geometry("900x600")
        self.canvas = tk.Canvas(self.root, bg="white", width=900, height=600)
        self.canvas.pack()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_window(self):
        """
        Sets up the Tkinter window and canvas for the histogram.
        """
        self.canvas.create_text(
            255, 20, text=f"Histogram of Vehicle Frequency per Hour ({self.date})", font=("Arial", 14,"bold","underline")
        )
        self.canvas.create_line(60, 550, 760, 550, width=2)
        self.canvas.create_text(350, 585, text="Hours 00:00 to 24:00", anchor="w", font=("Arial", 12,"bold"))

    def draw_histogram(self):
        """
        Draws the histogram with axes, labels, and bars.
        """
        max_count = max(
            max(self.traffic_data["Elm Avenue/Rabbit Road"]),
            max(self.traffic_data["Hanley Highway/Westway"])
        )
        hours = [i  for i in range (24)]
        bar_width = 10
        x = 65
        colors = {"Elm Avenue/Rabbit Road": "blue", "Hanley Highway/Westway": "red"}

        for hour in hours:
            x_base = 60 + hour * 30

            for i, junction in enumerate(self.traffic_data):
                count = self.traffic_data[junction][hour]
                bar_height = (count / max_count) * 400  # Scale to fit the canvas
                x1 = x_base + i * bar_width
                y1 = 550 - bar_height
                x2 = x1 + bar_width
                y2 = 550
                self.canvas.create_text(x1 + 5, y1 - 5, text=count, font=("Arial", 7), fill=colors[junction])
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=colors[junction], outline="black")

        for hour in range(24):
            self.canvas.create_text(x, 556, text=hour)
            x += 30

    def add_legend(self):
        """
        Adds a legend to the histogram to indicate which bar corresponds to which junction.
        """
        legend_x = 50
        legend_y = 50
        colors = {"Elm Avenue/Rabbit Road": "blue", "Hanley Highway/Westway": "red"}
        for i, (junction, color) in enumerate(colors.items()):
            self.canvas.create_rectangle(legend_x, legend_y + i * 20, legend_x + 10, legend_y + 10 + i * 20, fill=color)
            self.canvas.create_text(legend_x + 20, legend_y + 5 + i * 20, text=junction, anchor="w", font=("Arial", 10))

    def on_close(self):

        self.root.destroy()  # Close the window
        self.close_callback()
    def run(self):
        """
        Runs the Tkinter main loop to display the histogram.
        """
        self.setup_window()
        self.draw_histogram()
        self.add_legend()
        self.root.mainloop()

def execute():
    date = validate_date_input()
    file_path = passing_file_path(date)
    csv_file = process_csv_data(file_path)
    output = display_outcomes(csv_file)
    save_results_to_file(output, file_name="results.txt")
    histogram(csv_file, date)

def loop():
    execute()
loop()

# class MultiCSVProcessor:
#     def __init__(self):
#         """
#         Initializes the application for processing multiple CSV files.
#         """
#         self.current_data = None
#
#     def load_csv_file(self, file_path, date):
#         """
#         Loads a CSV file and processes its data.
#         """
#         try:
#             csv_file = process_csv_data(file_path)
#             output=display_outcomes(csv_file)
#             save_results_to_file(output, file_name="results.txt")
#             traffic_data = {
#                 "Elm Avenue/Rabbit Road": csv_file["total_hours_in_elm"],
#                 "Hanley Highway/Westway": csv_file["total_hours_in_han"]
#             }
#             self.current_data = traffic_data
#         except FileNotFoundError:
#             print(f"Error: File {file_path} not found.")
#         except KeyError:
#             print("Error: CSV file format is incorrect.")
#         else:
#             if self.current_data:
#                 app = HistogramApp(self.current_data, date)
#                 app.run()
#
#     def clear_previous_data(self):
#         """
#         Clears data from the previous run to process a new dataset.
#         """
#         self.current_data = None
#
#     def handle_user_interaction(self):
#         """
#         Handles user input for processing multiple files.
#         """
#         while True:
#             date = validate_date_input()
#             file_path = passing_file_path(date)
#             if file_path:
#                 self.clear_previous_data()
#                 self.load_csv_file(file_path, date)
#             user_input=input("Do you want to select another data file for a different date? Y/N > ").strip().lower()
#             if user_input == 'n':
#                 print("End....")
#                 break
#             elif user_input != 'y':
#                 print("Invalid input. Please enter 'Y' or 'N'.")
#
#
#     def process_files(self):
#         """
#         Main loop for handling multiple CSV files until the user decides to quit.
#         """
#         self.handle_user_interaction()
#
#
#
#
#
# # Calling
# processor = MultiCSVProcessor()
# processor.process_files()
