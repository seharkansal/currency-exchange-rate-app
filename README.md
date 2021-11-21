# currency exchange rate app
**1. summary**
A currency exchange rate app where a user can ask for 3 things:
1. user can fetch exchange rate of a country by giving date, base and of country he wants the exchange rate of
2. user can ask for a graph between 2 dates and exchange rate wrt to those dates of a country 
3. user can ask for average between 2 dates and their respective exchange rates of a country

**2. Author**
Sehar Kansal

**3.Technologies Used**
1. python
2. sqllite
3. API

**4.learning**
1. graph plotting using matplotlib
2. date manipulation: manipulating the date entered by user to correct format and asking the user to enter a particular format of date only
3. input validation: validating base country and country according to data in database
4. how to make an API call
5. sqllite
6. caching: if some data asked by user is already in db then fetching is faster or else first make an API call, store in db and then fetch to user

**5. challenges**
1. check if data is present in db or not
2. input validation
3. graph plotting: ploting a line graph between a date range and their corroesponding exchange rates

**6.future scope**
1. date limit i.e. till which date data is present
2. country limit i.e. if data is present for that country 

**7. refrences**
1. https://python.gotrained.com/python-json-api-tutorial/
2. https://www.tutorialspoint.com/sqlite/sqlite_python.htm
3. https://exchangerate.host/#/

**8. instructions**
To run the app:

~~~
python3 exchange_rate.py
~~~
