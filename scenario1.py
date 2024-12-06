import pandas as pd
import os

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
parcel_dict = df.to_dict('records')
destinations = df["Destination"].unique()

def truck_loading(parcel_data, size_col, destination_col, distance_col):
    #Assume that parcel_data is a dictionary extracted from a Dataframe with size column, destination column and distance column
    
    #Create bins for each destination
    bins = {}
    for destination in destinations:
        bins[destination] = []
    
    #Group parcels by destination
    for parcel in parcel_data:
        destination = parcel[destination_col]
        bins[destination].append(parcel)
    
    #Sort parcels in bins
    sorted_bins = {}
    #Transfer sizes into numbers for easier sorting later 
    for parcel in parcel_data:
        size = parcel[size_col]
        if size == "Small":
            parcel[size_col] = 1
        elif size == "Medium":
            parcel[size_col] = 2
        elif size == "Large":
            parcel[size_col] = 3
        elif size == "Oversize":
            parcel[size_col] = 4
        else:
            print("Please input parcel's size")
    #Sort parcels by size (descending)
    for destination in destinations:
        sorted_bins[destination] = sorted(bins[destination], key=lambda parcel: parcel[size_col], reverse=True)
    #Sort each bin by destination (closest to furtherst)
    destination_distance = dict(zip(df[destination_col], df[distance_col]))
    sorted_destinations = sorted(sorted_bins.keys(), key=lambda destination: destination_distance.get(destination, float('inf')))
    loading_order = {destination: sorted_bins[destination] for destination in sorted_destinations}

    return loading_order

def export_loading_order(loading_order, output_dir="GoodsLoadingPlan"):
    #All information of the plan stored in one txt file
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    filename = f"{output_dir}/GoodsLoadingPlan.txt"
    
    with open(filename, 'w') as file:
        file.write("=" * 20 + "GOODS LOADING PLAN" + "=" * 20 + "\n")
        file.write("Workers are advised to strictly follow this plan to optimize the goods loading process (which comes first, gets stacked first)\n")
        file.write("=" * 40 + "\n")
        
        for destination, parcels in loading_order.items():
            file.write(f"Destination: {destination}\n")
            file.write("="*40 + "\n")
            
            for parcel in parcels:
                file.write(f"Parcel ID: {parcel['Parcel ID']}\n")
                file.write(f"Recipient: {parcel['Recipient']}\n")
                file.write(f"Weight (kg): {parcel['Weight (kg)']}\n")
                file.write(f"Size: {['Small', 'Medium', 'Large', 'Oversize'][parcel['Size'] - 1]}\n")
                file.write(f"Rate per km (VND): {parcel['Rate per km (VND)']}\n")
                file.write(f"Distance (km): {parcel['Distance (km)']}\n")
                file.write("=" * 40 + "\n")


def cash_invoice(df, parcel_id_col, distance_col, destination_col, recipient_col, weight_col, rate_col, date_col):
    #Take necessary inputs
    cash_invoice_data = [
        {
            "Parcel ID": p,
            "Distance (km)": d,
            "Recipient": r,
            "Weight (kg)": w,
            "Rate per km (VND)": rate,
            "Destination": des,
            "Date": ord_date
        }
        for p, d, r, w, rate, des, ord_date in zip(df[parcel_id_col],
                                                   df[distance_col], 
                                                   df[recipient_col], 
                                                   df[weight_col], 
                                                   df[rate_col], 
                                                   df[destination_col], 
                                                   df[date_col])
    ]

    cash_invoice_final = {}

    #Update the cash_invoice_final with the inputs
    for data in cash_invoice_data:
        try:
            p = data['Parcel ID']
            d = int(data['Distance (km)'])  
            r = data['Recipient']
            w = int(data['Weight (kg)'])
            rate = int(data['Rate per km (VND)'])
            destination = data['Destination']
            ord_date = data['Date']

            #Calculate total money 
            total = d * w * rate

            #Update to the dictionary
            cash_invoice_final[r] = {
                "Parcel ID": p,
                "Total": total,
                "Destination": destination,
                "Date": ord_date
            }
            
        except ValueError as e:
            print(f"Skipping invalid data: {data} - Error: {e}")

    return cash_invoice_final

    
def export_cash_invoices(invoice_data, output_dir = "Cash invoices"):
    os.makedirs(output_dir, exist_ok=True)

    #Each customer get their own invoices
    for recipient, data in invoice_data.items():
        filename = f"{output_dir}/{recipient.replace(' ', '_')}_CashInvoice.txt"

        with open(filename, 'w') as file:
            file.write("Cash Invoice\n")
            file.write("="*40 + "\n")
            file.write(f"Recipient: {recipient}\n")
            file.write(f"Parcel ID: {data['Parcel ID']}\n")
            file.write(f"Date ordered: {data['Date']}\n")
            file.write(f"Shipping from: Hanoi to {data['Destination']}\n")
            file.write(f"Total: {data['Total']:,.0f} VND\n")
            file.write("="*40 + "\n")

loading_order=truck_loading(parcel_dict, 
              size_col="Size", 
              destination_col="Destination", 
              distance_col="Distance (km)"
              )

cash_invoice_final=cash_invoice(df, 
             parcel_id_col="Parcel ID", 
             distance_col="Distance (km)", 
             recipient_col="Recipient", 
             weight_col="Weight (kg)", 
             rate_col="Rate per km (VND)", 
             destination_col="Destination",
             date_col="Date"
             )

#User inputs for loading plan
user_choice1 = input("Do you want to export Goods Loading Plan? (y/n): ")
user_choice1 = user_choice1.lower()
if user_choice1 in ['y', 'yes']:
    export_folder1 = input("Enter your folder's name: ")
    export_loading_order(loading_order, export_folder1)
    print(f"Your plan is ready at {export_folder1}")

#Usr inputs for cash invoice
user_choice2 = input("Do you want to export cash invoices? (y/n): ")
user_choice2 = user_choice2.lower()
if user_choice2 in ['y', 'yes']:
    export_folder2 = input("Enter your folder's name: ")
    export_cash_invoices(cash_invoice_final, export_folder2)
    print(f"Your plan is ready at {export_folder2}")