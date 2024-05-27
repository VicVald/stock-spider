from time import sleep
from functions import date, end, counters, get_price, conversor, date_day
import csv
import sys
import os
import concurrent.futures

#To not initialize when market is closed
if end():
    print("Market is closed.")
    sys.exit(0)

#List of values
list1 = ["BTC", "ETH", "ADA", "BNB", "USDT", "XRP"]
list2 = ['MGLU3', 'HAPV3', 'PETR4', 'B3SA3', 'USIM5', 'CIEL3']

#Reset the file and put the head file
with open("crypto.csv", "w") as acoes_table:
    acoes_table.write("Data, ")
    for acronym in list1:
        acoes_table.write(f"{acronym}, ")
    acoes_table.write("\n")
    acoes_table.close()

with open("ações.csv", "w") as acoes_table:
    acoes_table.write("Data, ")
    for acronym in list2:
        acoes_table.write(f"{acronym}, ")
    acoes_table.write("\n")
    acoes_table.close()

#Rows
while not end():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        act = executor.map(lambda acronym: get_price(f'https://www.google.com/finance/quote/{acronym}-USD?hl=pt'), list1)
        with open("crypto.csv", "a") as acoes_table:
            acoes_table.write(f"{date()}, ")
            i = 0
            wait_list = []
            for value in act:
                if value == "Error":
                    print(f"{acronym} error!\nTrying again!!")
                    i=0
                    break

                elif not value == "Error":
                    value = value.replace(".", "").replace(",", ".")
                    value = float(value) * conversor(0)
                    wait_list.append(value)

                    i += 1
                    if i % len(list1) == 0:
                        for item in wait_list:
                            acoes_table.write(f"{item}, ")

            acoes_table.write("\n")
            acoes_table.close()

        with concurrent.futures.ThreadPoolExecutor() as executor2:
            act = executor2.map(lambda acronym: get_price(f'https://www.google.com/finance/quote/{acronym}:BVMF?hl=pt'), list2)
            with open("ações.csv", "a") as acoes_table:
                acoes_table.write(f"{date()}, ")
                for value in act:
                    i = 0
                    wait_list = []
                    if value == "Error":
                        print(f"{acronym} error!\nTrying again!!")
                        i=0
                        break
                    else:
                        i += 1
                        if i % len(list2) == 0:
                            for item in wait_list:
                                acoes_table.write(f"{item}, ")
                    acoes_table.write(f"{value}, ")
                acoes_table.write("\n")
            sleep(2)
    

        
for acronym in list1:
    directory = os.path.dirname(f"{acronym}.csv")

    if directory or not os.path.exists(directory):
        os.makedirs(directory)
        with open(f"{acronym}.csv", "a") as final_counters:
            csv_reader = csv.reader(final_counters)
            final_counters.write("Data, Data_Max, Max, Data_Min, Min, Last\n")
            final_counters.write(f"{date_day()}")
            for counter in counters('crypto.csv', list1.index(acronym)+1):
                final_counters.write(f"{counter}, ")
            final_counters.write("\n")
            #dia, data max, max, data min, min, last
            final_counters.close()
    else:
        with open(f"{acronym}.csv", "a") as final_counters:
            csv_reader = csv.reader(final_counters)
            final_counters.write(f"{date_day()}")
            for counter in counters('crypto.csv', list1.index(acronym)+1):
                final_counters.write(f"{counter}, ")
            final_counters.write("\n")
            #dia, data max, max, data min, min, last
            final_counters.close()

for acronym in list2:
    directory = os.path.dirname(f"{acronym}.csv")

    if directory or not os.path.exists(directory):
        os.makedirs(directory)
        with open(f"{acronym}.csv", "a") as final_counters:
            final_counters.write("Data, Data_Max, Max, Data_Min, Min, Last\n")
            csv_reader = csv.reader(final_counters)
            final_counters.write(f"{date_day()}")
            for counter in counters('crypto.csv', list2.index(acronym)+1):
                final_counters.write(f"{counter}, ")
            final_counters.write("\n")
            final_counters.close()
    else:
        with open(f"{acronym}.csv", "a") as final_counters:
            csv_reader = csv.reader(final_counters)
            final_counters.write(f"{date_day()}")
            for counter in counters('crypto.csv', list2.index(acronym)+1):
                final_counters.write(f"{counter}, ")
            final_counters.write("\n")
            final_counters.close()