import json
from datetime import datetime
stock = {}
my_report={}
try:
   with open('daily_report.json','rt') as report_file:
        my_report = json.load(report_file)
except FileNotFoundError:
   my_report={}
today = datetime.now().strftime("%Y-%m-%d")

if today not in my_report:
   my_report[today] = {
      'sales':{},
      'sales summary' :{}
   }
else:
   pass
try:
    with open('inventory.json','rt') as inventory_file:
        stock = json.load(inventory_file)
except FileNotFoundError:
   stock= {'Inventory': {}}
   

def add_items():
    item_found = False
    print("1.Existing item")
    print("2.New item")
    try:
        option = int(input("Pick an option: "))
       
    
        if option == 1:

            item_name = input("Enter the item name: ")
           
            
            for id,info in stock['Inventory'].items():
             if info['name'] == item_name:
                item_found = True
                item_quantity = int(input ("Enter quantity: "))
                info['quantity'] += item_quantity
                
                print(f"{item_name} updated")
                break
            if not item_found:
             print("Item does not exist")
            
        elif option == 2:
         item_name = input("Enter the item name: ")
        
        
         for id,info in stock['Inventory'].items():
            if info['name'] == item_name:
                print("Item already exist.....")
                item_found = True
                break
            
         if not item_found :
                item_quantity = int(input ("Enter quantity: "))
                item_price = float(input("Enter price per item: "))
                new_item_key = f"item{len(stock['Inventory']) + 1}"
                stock['Inventory'][new_item_key] = {'name':item_name, 'quantity':item_quantity, 'price':item_price }
                    
                print(f"{item_name} added")
    except ValueError:
     print("Enter appropriate value")
    with open('inventory.json','wt') as inventory_file:
      json.dump(stock,inventory_file)

def make_sale():
   
   item_name = input("Enter item name: ")
   for id, info in stock['Inventory'].items():
        if info['name'].strip().lower() == item_name.strip().lower():
           item_quantity = int(input("Enter amount you want to sell: "))
           if info['quantity'] >= item_quantity:
              selling_price = float(input("Enter the selling price per item: "))
              info['quantity']-=item_quantity
              cost_price = info['price']
              revenue = selling_price * item_quantity
              profit = (revenue) - (item_quantity * cost_price)
              print(f"{item_name} successfully sold and the quantity has been updated")
              print(f"New quantity: {info['quantity']}")
              item_id = f"item{len(my_report[today]['sales']) + 1}"
              my_report[today]['sales'][item_id]= {'name' : item_name,'quantity sold' : item_quantity,'selling price per item' : selling_price,'cost price per item ' : cost_price,'profit' :profit, "revenue":revenue}
              break
           else:
              print(f"You dont have enough {item_name} in stock")
              print(f"You currently have {info['quantity']} {item_name} in stock")
              break
   else:
        print("Item unavailable in stock")
   with open('daily_report.json', 'wt') as report_file:
      json.dump(my_report, report_file)
   with open('inventory.json', 'wt') as inventory_file:
    json.dump(stock, inventory_file)

def tracker():
  total_revenue = 0
  total_profit = 0
  total_loss = 0
  for id, info in my_report[today]['sales'].items():
     total_revenue+=info['revenue']
     if info['profit'] < 0 :
        total_loss+=info['profit']
     else:
      total_profit+=info['profit']

  print(f"{today} Profit/Loss Summary")
  print(f"Total Revenue: {total_revenue}")
  print(f"Total Loss: {total_loss}")
  print(f"Total Profit: {total_profit}")
 
  my_report[today]['sales summary'] = {'total revenue': total_revenue, 'total_profit': total_profit, 'total_loss':total_loss}
  with open('daily_report.json', 'wt') as report_file:
    json.dump(my_report, report_file)


def view_items():
   print('STOCK')
   print(f"{'Item':<20}{'Quantity':<15}{'Price':<10}")
   for id,info in stock['Inventory'].items():
        name = info['name']
        quantity = info['quantity']
        price = info['price']
        print(f"{name:<20}{quantity:<15}{price:<10}")


def edit_item():
  item_name = input("Enter the name of the item you would like to edit: ")
  for id,info in stock['Inventory'].items():
     if info['name'].strip().lower() == item_name.strip().lower():
        while True:
            print("1.Edit name")
            print("2.Edit quantity")
            print("3.Edit Price")
            print("4.Exit")
            option = int(input("What would you like to edit: "))
        
            if option == 1:
             new_name = input ("Enter new name: ")
             info['name'] = new_name
             print("Done.")
            elif option == 2:
             new_quantity = float(input ("Enter new quantity: "))
             info['quantity'] = new_quantity
             print("Done.")
            elif option == 3:
             new_price = float(input ("Enter new price: "))
             info['price'] = new_price
             print("Done.")
            elif option == 4:
             break
            else:
             print("Please enter appropriate option")
            break
  else:
     print("Item doesnt exist in stock ")
  with open('inventory.json', 'wt') as inventory_file:
    json.dump(stock, inventory_file)

while True:
   print("1.ADD ITEM TO STOCK")
   print("2.MAKE SALES")
   print("3.TRACK PROFIT/LOSS")
   print("4.VIEW ITEMS IN STOCK")
   print("5.EDIT ITEM IN STOCK")
   print("6.EXIT")
   option=int(input("Enter the appropriate option to carry out one of the commands: "))

   if option == 1:
      add_items()
   elif option == 2:
      make_sale()
   elif option == 3:
      tracker()
   elif option == 4:
      view_items()
   elif option == 5:
      edit_item()
   elif option == 6:
      break


     






