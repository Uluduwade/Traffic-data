# Traffic Data Analysis Project

## Overview
This project analyzes traffic data, processes vehicle records, and generates insights such as traffic volume, nighttime vehicle count, and histogram visualization. It supports multiple CSV files and saves results for future reference.

## Features
- **Input Validation**: Ensures correct date format and valid range.
- **Nighttime Traffic Count**: Counts vehicles between 8 PM and 6 AM.
- **Result Storage**: Saves analyzed data to a text file.
- **Histogram Visualization**: Displays traffic volume with an average line.
- **Multi-Date Support**: Allows users to process multiple dates.

## Technologies Used
- Python
- Pandas (for data processing)
- Tkinter (for GUI visualization)
- Matplotlib (for histogram plotting)

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/traffic-data-analysis.git
   ```
2. Navigate to the project folder:
   ```sh
   cd traffic-data-analysis
   ```
3. Install dependencies:
   ```sh
   pip install pandas matplotlib tk
   ```

## Usage
1. **Run the program:**
   ```sh
   python main.py
   ```
2. **Enter the date** (DD/MM/YYYY) for which you want to analyze data.
3. **View insights** such as total vehicles, nighttime traffic, and histogram.
4. **Save results** to `results.txt` for future reference.

## Example Code Snippets
### Input Validation
```python
def validate_date():
    day = input("Enter the day (DD): ")
    if not day.isdigit() or not (1 <= int(day) <= 31):
        print("Error: Invalid day.")
        return False
    
    month = input("Enter the month (MM): ")
    if not month.isdigit() or not (1 <= int(month) <= 12):
        print("Error: Invalid month.")
        return False
    
    year = input("Enter the year (YYYY): ")
    if not year.isdigit() or not (2000 <= int(year) <= 2024):
        print("Error: Invalid year.")
        return False
    
    return f"{day}/{month}/{year}"
```

### Counting Nighttime Vehicles
```python
def count_nighttime_vehicles(dataset):
    return sum(1 for row in dataset if 20 <= int(row['timeOfDay'].split(':')[0]) or int(row['timeOfDay'].split(':')[0]) < 6)
```

### Saving Results
```python
def save_results(results, selected_date):
    with open("results.txt", "a") as file:
        file.write(f"Results for {selected_date}:\n")
        for result in results:
            file.write(f"{result}\n")
        file.write("\n")
```

## Contributing
Feel free to fork this repository and submit pull requests for improvements.

## License
This project is licensed under the MIT License.

