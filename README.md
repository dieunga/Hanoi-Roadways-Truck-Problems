# Hanoi-Roadways-Truck-Problems

## Overview
### Milestone 1: Truck Loading Problem
**Problem:**
The company faces inefficiencies in loading parcels onto trucks, as goods are loaded randomly. This causes significant delays when drivers search for packages at delivery destinations, leading to driver frustration, poor delivery performance, and a declining reputation for the company.

**Goal:** 
Develop an efficient system to address the unregulated truck loading process. This solution will optimize the loading order of parcels to ensure drivers can quickly and easily locate goods for delivery, reducing delays, improving overall delivery efficiency, and enhancing customer satisfaction. The solution will also help restore the company's reputation and streamline operations.

**Input:**
It is expected that the user will provide the program a CSV file or an Excel file, other file types won't work. See sample_input_data.xlsx for best example.

**Output:**
- Text file of optimized loading plan (ordered list of parcels).
- Cash invoice for each customer will be exported as seperated text files for easy management.

### Milestone 2: Dynamic Truck Route Allocation
**Problem:**
Drivers frequently travel to cities where there are no parcels to deliver, causing frustration and wasting time and resources. This inefficiency stems from the lack of a customized route planning system, as the current process relies on simple, static routing methods.

**Goal:** 
Create a dynamic route planning system to prevent drivers from traveling to cities without parcels for delivery. This solution will customize delivery routes based on the current trip's requirements, reducing unnecessary travel, saving time and resources, and boosting driver satisfaction. It will also provide a backup system using grid coordinates to ensure operations run smoothly in case of IT failures.

**Input:**
It is expected that the user will provide the program a CSV file or an Excel file, other file types won't work. See sample_input_data.xlsx for best example.

**Output:**
- Route plan
- Backup map with coordinates of cities

## Solution 
### Features 
- **Route Optimization:** Implements algorithms like the nearest neighbor and other heuristic approaches to find the most efficient delivery routes.
- **Greedy Algorithms:** Uses greedy methods for solving route planning problems efficiently.
- **Scalability:** Designed to handle large datasets representing real-world road networks.
- **Extensibility:** Modular codebase that allows for easy customization and expansion.

## Prereuisites 
Before running the program, enseure you have the following installed:
- Python 3.8 or higher
- Required Python libraries (listed in ``requirements.txt``)

## Installation 
1. Clone the repository
```
git clone https://github.com/dieunga/Hanoi-Roadways-Truck-Problems.git
```

2. Navigate to the project directory
```
cd Hanoi-Roadways-Truck-Problems
```

3. Install the required dependencies
```
pip install -r requirements.txt
```

## Usage 
1. Prepare your data
   - Make sure your data is stored in CSV/Excel file and has the required attributes to have the best results

2. Run the file
   - Solution for Milestone 1 is stored in ``scenario1.py``
   - Solution for Milestone 2 is stored in ``scenario2.py``
   - Then run the program
     ```
     python scenario.py
     ```
3. View your results in the customize folders/files (Only the route plan will be displayed in your terminal)
