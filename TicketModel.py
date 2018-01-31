import  pyodbc
import pyodbc
cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};Server=DESKTOP-EOH37VD;Database=BusTicket;Trusted_Connection=yes;")
cursor = cnxn.cursor()

def ViewCustomerInfo():
    cursor.execute("select * from dbo.Customer;")
    for i in cursor:
        print('Customer = %r' % (i,))


def viewTicketInformation():
    cursor.execute("select * from dbo.Ticket;")
    for i in cursor:
        print('Tickets = %r' % (i,))

def BusInformation():
    cursor.execute("select * from dbo.BUS;")
    for row in cursor:
        print('row = %r' % (row,))

def ViewCityInformation():
    cursor.execute("select * from dbo.City;")
    for item in cursor:
        print('Items = %r' %  (item,) )


def ViewState():
    cursor.execute("select * from dbo.State;")
    for item in cursor:
        print('State = %r' % (item,))

def DeleteTicket():
    print("You are on the delete ticket Menu")
    ticket = input("Please input the ticket number you want to delete")
    cursor.execute("delete from dbo.Ticket   where TicketNo = '{0}';".format(ticket))
    cnxn.commit()

def DeleteCustomer():
    print("You are on the delete Customer Menu")
    customer = input("Please input the Customer Number you want to delete")
    cursor.execute("delete from dbo.Customer where CustomerID = '{0}'".format(customer))
    cnxn.commit()
def viewIndividualCustomer():
    x = input("Input the customer ID to look up detail of that customer")
    individualCustomerSQL = "select * from Customer where CustomerID = '{ID}';".format(ID = x)
    cursor.execute(individualCustomerSQL)
    for item in cursor:
        print('Customer = %s' % (item,))

def CreateCustomer():
    print("Now you are creating a customer")
    cusID = input("Enter an id for Customer ID :")
    fname = input("Enter the first Name: ")
    lname= input("Enter Last Name :" )
    phNo = input("Enter Phone Number :")
    email = input("Enter an Email Address :")

    createcustomerSql = "insert into dbo.Customer values ('{0}', '{1}' ,'{2}','{3}','{4}' );"\
        .format(cusID,fname,lname,phNo,email)
    cursor.execute(createcustomerSql)
    cnxn.commit()


def UpdateCustomerInfo():
    print("You are now on the update for customer inromation: ")
    print("Do you want to update all the attributes of a customer ? (Y/N)")
    choice = input()
    if(choice == 'y'):
        FirstName = input("Input your First Name ")
        LastName = input("Input your Last name")
        PhNum = input("Enter 10 digit phone Number")
        email = input("input your Email")
        Customerid = input("Input the customer ID")

        sql_statement = "update Customer set Fname='{first_name}',Lname = '{Last_name}',PhoneNumber ='{phoneNo}' \
                        ,Email ='{email}' where CustomerID ='{ID}';".format\
                        (first_name=FirstName,Last_name =LastName ,phoneNo = PhNum, email = email, ID = Customerid)
        cursor.execute(sql_statement)
        #cursor.execute("update Customer set Fname = '+FirstName+', Lname = '+LastName'+,PhoneNumber = '+phNum+', Email = '+email+' where CustomerID = '+Customerid+';")
        cnxn.commit()
    else:
        print("You can choose what you want to update")
        print("First we will display the customer info. input the customer id to view customer info")

        viewIndividualCustomer()

        print("What field you want to update:1= first name, 2 = lastname, 3 = phoneNo, 4 = Email")
        fieldChoice= input()

        if(fieldChoice == '1'):
            print("you are changing First name")
            name = input("Please input the new name")
            id = input("Insert Customer ID to update ")
            firstNameSql = "update Customer set Fname = '{firstname}' where CustomerID = '{ID}';"\
            .format(firstname = name,ID = id)
            cursor.execute(firstNameSql)
            cnxn.commit()
            viewIndividualCustomer() #show detail after changing by calling the function
        elif(fieldChoice == '2'):
            print("You are changing Last Name")
            last = input("Enter the last name : ")
            id = input("Insert Customer ID to update ")
            LastNameSql = "update Customer set Lname = '{Lastname}' where CustomerID = '{ID}';" \
                .format(Lastname=last, ID=id)
            cursor.execute(LastNameSql)
            cnxn.commit()
            viewIndividualCustomer()  # show detail after changing by calling the function
        elif(fieldChoice == '3'):
            print("You are changing Phone Number")
            Phone = input("Enter the Phone Number : ")
            id = input("Insert Customer ID to update ")
            PhoneNoSQL = "update Customer set PhoneNumber = '{PhNo}' where CustomerID = '{ID}';" \
                .format(PhNo=Phone, ID=id)
            cursor.execute(PhoneNoSQL)
            cnxn.commit()
            viewIndividualCustomer()  # show detail after changing by calling the function
        elif(fieldChoice == '4'):
            print("You are changing Email Address")
            email = input("Enter the Email Address : ")
            id = input("Insert Customer ID to update ")
            EmailSql = "update Customer set Email = '{Email}' where CustomerID = '{ID}';" \
                .format(Email=email, ID=id)
            cursor.execute(EmailSql)
            cnxn.commit()
            viewIndividualCustomer()  # show detail after changing by calling the function

def BuyTicket():
    print("welcome to Ticket Purchasing. Before purchasing create a customer to buy ticket")
    print("If you already have customer ID then use that ID instead")

    cusID = input("Enter your Customer ID")
    #now check the valid customer id
    # cusIDSQL = "select CustomerID from Custome;"
    # id = cursor.execute(cusIDSQL)

    ticketNum = input("Enter Ticket Number ")
    busNum = input("Enter Bus Number")

    date = input("Enter the Date You want to travel")
    seat = input("Input the seat No")
    capacity = GetBusCapacity(busNum)
    if(capacity > 0):
        ticketSql = "insert into dbo.Ticket values( '{0}', '{1}', '{2}', '{3}', '{4}');"\
                    .format(ticketNum,busNum,cusID,date,seat)
        cursor.execute(ticketSql)
        cnxn.commit()
    else:
        print("The Bus Capacity is Full. Please Try another Bus")

def GetBusCapacity(busid):
    updateCapaSql = " select count (*) from dbo.Ticket where BusNo= '{0}';".format(busid)
    current_tickets = cursor.execute(updateCapaSql)

    current_tickets = list(current_tickets)[0][0]

    remainingCapicity = "select Buscapacity from BUS where BusNo = '{0}';".format(busid)
    BusCapacity = cursor.execute(remainingCapicity)
    BusCapacity = list(BusCapacity)[0][0]

    return  BusCapacity - current_tickets


def UpDateBusCapacity(busid):
    bus_capacity = GetBusCapacity(busid)
    print(bus_capacity)
    #cnxn.commit()

def TicketViewWithJoin():
    view = "select TicketNo, BusNo, c.CustomerID,c.Fname, c.Lname, c.PhoneNumber, Date , SeatNo\
            from Customer as c, Ticket t\
            where c.CustomerID = t.CustomerID;"
    cursor.execute(view)
    for item in cursor:
        print('Ticket = %r' %(item,))

def BusTableWithCityName():
    BusSql = " select b.BusNo,b.Buscapacity,b.DepartureCity, DC.CityName, b.ArrivalCity, AC.CityName,b.TIME\
            from BUS b , City as DC,\
            City as AC \
            where b.DepartureCity = DC.CityID and \
            b.ArrivalCity = AC.CityID;"
    cursor.execute(BusSql)
    for item in cursor:
        print('BusInfo = %r' % (item,))

def NumberOfTicketIssued():
    TiketIsSQL = "select count(*) from Ticket;"
    cursor.execute(TiketIsSQL)
    for count in cursor:
        print(count[0])


def NumOfCustomer():
    cusNumSql = "select count(*) from Customer;"
    cursor.execute(cusNumSql)
    for count in cursor:
        print(count[0])

def main():


    while(True):
        print("Main Menu")
        print("1 for view table")
        print ("2 for update Customer information")
        print ("3 for delete information")
        print ("4 for inser information like create customer and Bus Ticket")
        print("5 To view Ticket and Bus Table using Join")
        print("6 to view Number Of Customer In the Database")
        print("7 to view Number Of Ticket Issued")
        number = input("Please input what you want to do? : ")
        if(number == '1'):
            print("Welcome to view table menu")
            print("1 for to view the customer information table")
            print("2 for to view the Ticket information Table")
            print("3 for to view Bus information Table")
            print("4 for to view City Information Table")
            print("5 for to view State Table")
            info = input("Please input the number for your choice :")
            if(info == '1'):
                ViewCustomerInfo()
            elif(info == '2'):
                viewTicketInformation()
            elif(info == '3'):
                BusInformation()
            elif(info == '4'):
                ViewCityInformation()
            elif(info == '5'):
                ViewState()

        elif(number == '2'):
            UpdateCustomerInfo()

        elif(number == '3'):
            print("You are on the Delete menu. You can only delete customer and Ticket")
            print("1 to delete Ticket")
            print("2 to delete Customer")
            num = input(" Please input your choice to perform Delete Opeartion :")
            if(num == '1'):
                DeleteTicket()
            elif(num == '2'):
                DeleteCustomer()
        elif(number == '4'):

            print ("1 for Customer create")
            print ("2 for Ticket")
            choose = input("Which field you want to insert or create:")
            if(choose == '1' ):
                CreateCustomer()
            elif(choose == '2'):
                BuyTicket()

        elif (number == '5'):
            print("This section prints the table with the name instead of the foreign key")
            print("1 for Ticket")
            print("2 for Bus")
            viewChoice = input("Please input your choice to perform :")
            if(viewChoice == '1'):
                TicketViewWithJoin()
            elif(viewChoice == '2'):
                BusTableWithCityName()

        elif (number == '6'):
            NumOfCustomer()
        elif (number == '7'):
            NumberOfTicketIssued()


        user_session_end = input("Do you want to contine ? ")

        if user_session_end == "N":
            break

if __name__ == '__main__':
    main()
