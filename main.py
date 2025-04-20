import csv
from dateutil import parser
import matplotlib.pyplot as plt
import numpy as np

# Function to load data from CSV file
def load_data_from_csv(filename="covid_data.csv"):
    data = []
    try:
        with open(filename, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print(f"{filename} not found! Starting with an empty dataset.")
    return data

# Function to save data to CSV file
def save_data_to_csv(data, filename="covid_data.csv"):
    fieldnames = ['City', 'Date', 'Cases', 'Recovered', 'Deaths']
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

# Function to add daily data and save it
def add_daily_data(city, date_str, cases, recovered, deaths, data):
    # Smart date parsing
    date = parser.parse(date_str).date()
    
    # Add the new data
    data.append({
        "City": city,
        "Date": str(date),
        "Cases": cases,
        "Recovered": recovered,
        "Deaths": deaths
    })
    
    # Save to CSV
    save_data_to_csv(data)

    print(f"Data for {city} on {date} added successfully!")
    
# Function to display all data
def display_all_data(data):
    if data:
        for entry in data:
            print(f"City: {entry['City']}, Date: {entry['Date']}, Cases: {entry['Cases']}, Recovered: {entry['Recovered']}, Deaths: {entry['Deaths']}")
    else:
        print("No data available.")

# Function to categorize risk zones
def analyze_risk_zones(data):
    risk_zones = {}
    for entry in data:
        city = entry['City']
        cases = int(entry['Cases'])

        # Categorize based on the number of cases
        if city not in risk_zones:
            if cases > 1000:
                risk_zones[city] = 'High'
            elif cases > 500:
                risk_zones[city] = 'Medium'
            else:
                risk_zones[city] = 'Low'
    
    return risk_zones

# Function to generate trend visualization
def generate_trend(data):
    cities = list(set([entry['City'] for entry in data]))
    for city in cities:
        city_data = [entry for entry in data if entry['City'] == city]
        dates = [entry['Date'] for entry in city_data]
        cases = [int(entry['Cases']) for entry in city_data]

        plt.plot(dates, cases, label=city)

    plt.xlabel('Date')
    plt.ylabel('Number of Cases')
    plt.title('COVID Trend per City')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Function to predict hotspots
def predict_hotspot(data):
    city_cases = {}
    for entry in data:
        city = entry['City']
        cases = int(entry['Cases'])

        if city not in city_cases:
            city_cases[city] = 0
        city_cases[city] += cases

    # Sort cities based on total cases and predict hotspot
    sorted_cities = sorted(city_cases.items(), key=lambda x: x[1], reverse=True)
    print(f"Predicted hotspot: {sorted_cities[0][0]} with {sorted_cities[0][1]} total cases.")

# Main function to run the program
def main():
    # Load existing data from CSV
    data = load_data_from_csv()

    while True:
        print("\nCOVID Data Management System")
        print("1. Add Daily Data")
        print("2. View All Data")
        print("3. Analyze Risk Zones")
        print("4. Generate Trend Visualization")
        print("5. Predict Hotspot")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            city = input("Enter the city: ")
            date = input("Enter date (YYYY-MM-DD): ")
            cases = int(input("Enter the number of cases: "))
            recovered = int(input("Enter the number of recovered: "))
            deaths = int(input("Enter the number of deaths: "))
            add_daily_data(city, date, cases, recovered, deaths, data)
        
        elif choice == '2':
            display_all_data(data)
        
        elif choice == '3':
            risk_zones = analyze_risk_zones(data)
            print("\nRisk Zones:")
            for city, zone in risk_zones.items():
                print(f"{city}: {zone}")
        
        elif choice == '4':
            generate_trend(data)
        
        elif choice == '5':
            predict_hotspot(data)
        
        elif choice == '6':
            print("Exiting the program...")
            break
        
        else:
            print("Invalid choice! Please try again.")

# Run the program
if __name__ == "__main__":
    main()
