'''
A currency exchange rate app where user can ask for 3 things:
1. user asks for the exchange rate of a country wrt to a base country and a date
2. user can give a range of dates and ask for a graph between exchange rates of a country wrt to a base btw those dates
3. user can ask for average of exchange rates between a range of dates for a country wrt to its base
'''
import sqlite3 
import datetime
import sqlite3.dbapi2 as Cursor
import requests
import json
import matplotlib.pyplot as plt
from datetime import timedelta

conn = sqlite3.connect('FINAL.db')
cur=conn.cursor()

def api_call(date1,base):
    '''
    A function which makes a call to the API for data not present in database
    input: date and base country
    output: exchange rate wrt that date and base
    '''
    url ='https://api.exchangerate.host/'+date1+"?base="+base

    response = requests.get(url)
    data = response.text
   #loads is  used to parse a valid JSON string and convert it into a Python Dictionary.
    parsed = json.loads(data)
    rates = parsed["rates"]
    result=rates[country]
    return result

def write_data_to_db(date1,base,rate):
    '''
    a function which writes data to database after API call 
    input: date and country 
    output: exchange rate wrt date and base
    '''
   
    primary_key=country+"_"+str(date1)
    command1 = "INSERT INTO Currency_exchange (primary_key,DATE,COUNTRY,BASE,RATE) VALUES ('{}','{}','{}','{}',{})".format(primary_key,date1,country,base,rate)
    cur.execute(command1)
    conn.commit()
  

def user_fetch(date,base,country):
    '''
   function that gives exchange rate of a country by asking user: 
   input/params: 
        date: sring, required
                %Y-%m-%d
        base: string,required
                from country
        country: string, required
                to country
   output/returns:return exchange rate of user specified input
    '''
    command='''SELECT COUNT(primary_key) FROM currency_exchange WHERE currency_exchange.primary_key="'''+country+'''_'''+date+'''"'''
    
    cur.execute(command)
    new_list=cur.fetchone()

    if new_list[0]==1:
        print ("yes")
        result=conn.execute('''SELECT RATE FROM currency_exchange WHERE currency_exchange.primary_key="'''+country+'''_'''+date+'''"''' )
        
        for row in result:
            print("rate for",country,"is",row[0])
        conn.commit()
        return row[0]

    else:
        rate=api_call(date,base)
        write_data_to_db(date,base,rate)
        return rate
        

def get_date_list(start_dt,end_dt):
    '''
    A function that gives all the dates between given 2 dates
    input: start date and end date
    output: date list with all the dates within those dates
    '''
    date_list=[]

    def daterange(date1, date2):
        for n in range(int ((date2 - date1).days)+1):
            yield date1 + timedelta(n)

    for dt in daterange(start_dt, end_dt):
        date_list.append(dt.strftime("%Y-%m-%d"))
    print("dates between",start_dt,"and",end_dt,"are",date_list)
    return date_list

def get_value_list(base,country):
    '''
    a function that gives list of values for list of dates
    input: base and country of which values are needed
    output: list of values 
    '''
    values=[]
    pk_list=[]
    command2='''SELECT primary_key FROM currency_exchange'''
    result=cur.execute(command2)
    for row in result:
        pk_list.append(row[0])

    date_list=get_date_list(start_dt,end_dt)

    for i in date_list:
        
        pk=country+'_'+i
        if pk in pk_list:
            print("yes")
            
            result=conn.execute('''SELECT RATE FROM currency_exchange WHERE currency_exchange.primary_key="'''+country+'''_'''+i+'''"''' )
        
            for row in result:
               values.append(row[0])
            
            conn.commit()
               
        else: 
            rate=api_call(i,base)
            write_data_to_db(i,base,rate)
            
            values.append(rate)
            
    print(values)
    return values

def graph_plot(start_dt,end_dt,base,country):
    '''
   function plots a graph according to input prvodided by user i.e.
   input: start date,end date, base country and country to
   output:displays a graph
  '''
    
    plt.style.use('seaborn')
    value_list=get_value_list(base,country)
    date_list=get_date_list(start_dt,end_dt)
    plt.plot(date_list, value_list)
    plt.xlabel('dates')
    plt.ylabel('exchange rates')
    plt.show()

def avg_rate(base,country):
    '''
    function to display average of currency rates of a country on a range of dates provided by user
    input:start date, end date, base country, country to
    output:average of currency rates between those dates
    '''
    value_list=get_value_list(base,country)
    average=sum(value_list)/len(value_list)
    return average


if __name__ == "__main__":

   while True:
        print("""
        ====== currency exhcange rate app =======
        1. Enter date, base country and country you want to see exhnge rate of
        2. enter a start and end date to see exchange rate of an country during that dates through a graph
        3. see average exchange rates of a country between 2 dates
        4. Exit
        """)
        
        choice = input("Enter choice: ")
        
        try:
            choice = int(choice)
        except ValueError:
            print("That's not an int!")
            continue
        
        if choice == 1:
            while True:
                
                    date_country=input("enter date:")
                    format = "%Y-%m-%d"

                    try:
                        datetime.datetime.strptime(date_country, format)
                        print("This is the correct date string format.")
                        break
                    except ValueError:
                        print("This is the incorrect date string format. It should be YYYY-MM-DD")
                        continue
            while True:

                    base=input("enter base:")
                    country_list=[]
                    command2='''SELECT COUNTRY FROM currency_exchange'''
                    result=cur.execute(command2)
                    for row in result:
                        country_list.append(row[0])
                    
                    if len(base)==3 and base.isupper() and base in country_list:
                           
                        print("yes")
                        break
                    else:
                        print("invalid")
                        continue

            while True:

                    country=input("enter base:")
                    country_list=[]
                    command2='''SELECT COUNTRY FROM currency_exchange'''
                    result=cur.execute(command2)
                    for row in result:
                        country_list.append(row[0])
                    
                    if len(country)==3 and country.isupper() and country in country_list:
                        
                        print("yes")
                        break
                    else:
                        print("invalid")
                        continue
            print("exchange rate of",country,"is:",user_fetch(date_country,base,country))
        
        elif choice == 2:
           while True:

            try:
              date_entry = input('Enter a start date in YYYY-MM-DD format:')
              year, month, day = map(int, date_entry.split('-'))
              start_dt = datetime.date(year, month, day)
              break
            except:
               print("invalid date")
               continue

           while True:

            try:
              date_entry = input('Enter a end date in YYYY-MM-DD format:')
              year, month, day = map(int, date_entry.split('-'))
              end_dt = datetime.date(year, month, day)
              break
            except:
               print("invalid date")
               continue
               
           while True:
                base=input("enter base:")
                country_list=[]
                command2='''SELECT COUNTRY FROM currency_exchange'''
                result=cur.execute(command2)
                for row in result:
                    country_list.append(row[0])
                    
                if len(base)==3 and base.isupper() and base in country_list:
                     
                    print("yes")
                    break
                else:
                    print("invalid")
                    continue

           while True:

                    country=input("enter country:")
                    country_list=[]
                    command2='''SELECT COUNTRY FROM currency_exchange'''
                    result=cur.execute(command2)
                    for row in result:
                        country_list.append(row[0])
                    
                    if len(country)==3 and country.isupper() and country in country_list:
                           
                        print("yes")
                        break
                    else:
                        print("invalid")
                        continue
           graph_plot(start_dt,end_dt,base,country)

        elif choice == 3:
            while True:
                try:
                    date_entry = input('Enter a start date in YYYY-MM-DD format:')
                    year, month, day = map(int, date_entry.split('-'))
                    start_dt = datetime.date(year, month, day)
                except ValueError:
                    print("invalid date")
                    continue
                
                try:
                    date_entry = input('Enter a end date in YYYY-MM-DD format:')
                    year, month, day = map(int, date_entry.split('-'))
                    end_dt = datetime.date(year, month, day)
                except ValueError:
                    print("invalid date")
                    continue

                base=input("enter base:")
                country_list=[]
                command2='''SELECT COUNTRY FROM currency_exchange'''
                result=cur.execute(command2)
                for row in result:
                        country_list.append(row[0])
                            
                if len(base)==3 and base.isupper() and base in country_list:
                                
                        print("yes")
                        break
                else:
                        print("invalid")
                        continue

            while True:

                    country=input("enter country:")
                    country_list=[]
                    command2='''SELECT COUNTRY FROM currency_exchange'''
                    result=cur.execute(command2)
                    for row in result:
                        country_list.append(row[0])
                    
                    if len(country)==3 and country.isupper() and country in country_list:
                           
                        print("yes")
                        break
                    else:
                        print("invalid")
                        continue
            print("average btw dates:",avg_rate(base,country))

        elif choice == 4:
            break
        else:
            print("Invalid input. Please enter number between 1-4 ")        
        print("Thank you for using the currency exchange rate app")

