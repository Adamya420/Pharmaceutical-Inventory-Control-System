'''----------------------------------------------------------------------------------------------------------------------
                                                    Medicine Shop                                                       
------------------------------------------------------------------------------------------------------------------------'''




# module for mysql connectivity
import mysql.connector

# module for creating table
from prettytable import PrettyTable

#connection with mysql
mydb = mysql.connector.connect(host = "localhost", user = "root", passwd = "mysql", database = "medicineshop1")
mycursor = mydb.cursor()

# main menu
def menu():
    choice = input('''Enter 1 to add medicine in the store.
Enter 2 to display the medicine details.
Enter 3 to remove a medicine form the store.
Enter 4 to display the stock of a medicine.
Enter 5 to buy a medicine.
Enter 6 to sell a medicine.
Enter 7 to Exit.
Enter your choice: ''')
    return(choice)


# prints line
def line():
    print("*"*100)

#calculates total amt to be paid
def bill(newstock, id):
    #query for price of 1 med
    sql = "select price from medicines where id = %s"
    mycursor.execute(sql,(id,))
    price = mycursor.fetchall()
    #price will return tuple in list i.e [(x,)]
    #accessing zeroth pos of tuple at zeroth pos of list price
    print(f"Total amount payable is: {newstock*price[0][0]}")

# creating tables
def table(res):
    myTable = PrettyTable(["Medicine id", "Medicine Name", "Price", "Pharma company Name", "Total No of Medicines"])
    for i in res:    
        #if medicines are in database
        if i != 0:
            myTable.add_row(i)
        #if no medicines in database
        else:
            print("No medicines in database")
    print(myTable)

# adding meds into database
def addmedicine():
    #empty list
    info = []
    #med id
    id = int(input("Enter medicine Id : "))
    info.append(id)
    #med name
    name = input("Enter medicine Name: ") 
    info.append(name)
    #med price
    price = float(input("Enter medicine Price : ")) 
    info.append(price)
    #pharma name
    pharma_company = input("Enter Pharma company Name : ")
    info.append(pharma_company)
    #meds in stock
    stock = int(input("Enter Total medicines in Stock: ")) 
    info.append(stock)
    cust = (info)
    #insertion in database
    sql = "Insert into medicines(id,name,price,pharma_company,stock) values(%s,%s,%s,%s,%s)"
    mycursor.execute(sql,cust)
    print("Record Inserted\n")
    mydb.commit()

# searching meds
def search():
    print("Select the search criteria : ") 
    print("1. Medicine Id")
    print("2. Medicine Name") 
    print("3. Pharma company Name")
    print("4. View All")
    ch = input("Enter the choice : ")
    #function for user choice
    def choice():
        if ch == '1':
            #search by med id
            id = int(input("Enter medicine Id : "))
            sql = "select * from medicines where id = %s"
            mycursor.execute(sql,(id,))
        elif ch == '2':
            #search by med name
            name = input("Enter Medicine Name : ")
            sql = "select * from medicines where name = %s"
            mycursor.execute(sql,(name,))
        elif ch == '3':
            #search by pharma name
            pharma = input("Enter pharma company name : ")
            sql = "select * from medicines where pharma_company = %s"
            mycursor.execute(sql,(pharma,))
        elif ch == '4':
            #view all
            sql = "select * from medicines"
            mycursor.execute(sql)
        else:
            #goto choice
            print("Invalid option")
            print("choose a valid option")
            choice()
    choice()
    #fetches the data according to the user choice
    res = mycursor.fetchall()
    #creates table
    table(res)

# delete meds
def delMedicine():
    id = int(input("Enter Medicine Id to delete medicine from Database :"))
    #query for fetching medicine id
    query = "select id from medicines"
    mycursor.execute(query)
    stock = mycursor.fetchall()
    #checking availability of medicines
    if (id,) in stock:
        #if available
        sql = "delete from medicines where id = %s"
        mycursor.execute(sql,(id,))
        print("Medicine records deleted\n")
        mydb.commit()
    else:
        #if not available
        print("No medicine with this id present in database")

#display medicines
def display():
    sql = "select * from medicines"
    mycursor.execute(sql)
    res = mycursor.fetchall()
    table(res)

#purchasing meds for stock
def purchase():
    #no of meds to purchase
    newstock = int(input("Enter No. of Mediciness to Purchase for Stock : "))
    #med id
    id = int(input("Enter Medicine Id : "))
    cust = (newstock,id)
    #query for fetching medicine id
    query = "select id from medicines"
    mycursor.execute(query)
    stock = mycursor.fetchall()
    #checking availability of medicines
    if (id,) in stock:
        #if available
        sql = "Update medicines set stock = stock+%s where id = %s"
        mycursor.execute(sql,cust)
        mydb.commit()
        print(f"{newstock} medicines are added now in Database")
        #bill calculates total amt
        bill(newstock, id)
    else:
        #if not available
        print("No medicine with this id present in database")

#sell medicines from stock
def sell():
    newstock = int(input("Enter No. of medicines to sell : "))
    id = int(input("Enter Medicine Id : ")) 
    cust = (newstock,id)
    #query for fetching stock of medicines
    query = "select stock from medicines where id = %s"
    mycursor.execute(query,(id,))
    stock = mycursor.fetchall()
    #checking availability of medicines
    if stock[0][0] >= newstock:
        #if available
        sql = "Update medicines set stock = stock-%s where id = %s"
        mycursor.execute(sql,cust)
        mydb.commit()
        print(f"{newstock} medicines are deleted from Database")
        #bill
        bill(newstock, id)
    else:
        #if not available
        print("Not enough medicines in stock")
        if stock[0][0] == 0:
            #if medicines completely out of stocks
            print( "Medicines out of stock")
        else:
            #if some medicines are left
            print(f"Only {stock[0][0]} medicines in stock")


#hedder format
line()
print("\t\t\tMedical store")
line()

#main operations
while(True):
    choice = menu()
    if choice == '1':
        addmedicine()
    elif choice == '2':
        search()
    elif choice == '3':
        delMedicine()
    elif choice == '4':
        display()
    elif choice == '5':
        purchase()
    elif choice == '6':
        sell()
    elif choice == '7':
        break
    else:
        print("Select a valid option!!")


#                                                            END OF PROJECT ;)
#                                                            Created by Adamya