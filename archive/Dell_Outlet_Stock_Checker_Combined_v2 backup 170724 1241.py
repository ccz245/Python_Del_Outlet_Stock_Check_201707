#!python3

# coding: utf-8

# # Objective

# __Purpose__:
# - check dell outlet stock website
# - filter for 15inch screen, i7 7..H. Processor, 3840x2160 screen, (scratch and dent?), outlet price < 1200
# - send result to personal email

# Dell outlet URL<br>
# 
# Active filters:
# - XPS 15 9560
# - i7
# - 3840x2160

# In[2]:

outletURLPage1 = "http://outlet.euro.dell.com/Online/InventorySearch.aspx?c=uk&cs=ukdfh1&l=en&s=dfh&brandid=7&sign=PXhcOSHtr1T4IOw%2fPR7UdQQtu8ahqH%2bNHH7w97RBh24Yb9ytkYEwHZxQv9U80NfLyDpcxEbPA%2bQ4gJotV48WzamWydAzuCBajsdD24yQdkrRWEd0Afm6GvzpUjsdxJe3QVbHjM%2fDzGzVL5PmDUJ26kUrHxrxG3PaSE97ZZ1TESjW%2fExCZjGJtWMImzIJrfMgNSuVc8hA0%2b%2fw3ZVBonDQsW6XaFlvfbawyudtMeLZ6g8MZVlfcCzO%2bND3DYnPDPILCHs12ssROc%2fPc%2fFW24ZEamIN1MGhMTYJ6NXA1WEem161c0A6aF98wKHdZxTp3kbE46wKm%2bthFJnCMcpbz5%2btWYu7up1Ky6JGB4%2bIlqaJ%2bVUfh6UK5i9aPXMIHNXULO7xCYvu69R7sdQ%3d"
outletURLPage2 = "http://outlet.euro.dell.com/Online/InventorySearch.aspx?c=uk&cs=ukdfh1&l=en&s=dfh&brandid=7&sign=PXhcOSHtr1T4IOw%2fPR7UdUbIb1XeAVkg7mqbVtWGF38z5d%2frJiiyf6HqilpYOtgwhuGdJHhtznNyEPM%2bNJySPYY%2bdIYXEh8VwZMPo2V%2bTwZZTv6FkWzNiUiC9qe9eWdtHTNW7E7GxowZnLxEzF2LyabINL9vicwkY9uENvNNsp1X4NuXUtHmKM%2bjQ5Jh3Ya7ENnWnbqbf8wwrf1kE5FD4D8iff70kzAkWbVq72DAntplNqL4A9auTP3GV%2bTR6QZRbEG6%2bz%2bryyovBb2YVzKlVzmhkxaxFd64%2bPFNhXnAb%2fgMXH1O6LsCgWF56qvfA67UgZKsXi2JnRmz8Gzz34i6HwF5b4OOsDmsxVVz4StwovV16QDmkEeK1t9btUtq1aiq"


# __References__:
# - Coursera: Python for Everyone Series: Using Python to Access Web Data
#     - https://www.coursera.org/learn/python-network-data/home/welcome
#     - https://www.py4e.com/html3/12-network
#     
# 

#run_interval = 120
#output_path = "D:\\01 Google Drive\\10. Coding\\201707 Dell Outlet Stock Check with Python\\results\\"

# output path for surface book
#output_path = "C:\\Users\\charl\\Google Drive\\10. Coding\\201707 Dell Outlet Stock Check with Python\\results\\"

import sys
import os

'''=============================== scan dell outlet, save results to file ========================='''

def scan(output_path):
    from datetime import datetime

    run_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    # absolute path for output (doesn't work across machines)
    #output_file = output_path + str(run_time) + ".txt"

    # output path for
    output_file = output_path + str(run_time) + ".txt"


    # relative path
    #import os
    #dir = os.path.dirname(__file__)
    #output_path = os.path.join(dir, '/results/')
    #output_file = output_path + str(run_time) + ".txt"

    # a+ will append after creating file (if doesn't exist)
    output = open(output_file, "a+")


    # ### get html string back from dell outlet website

    # reading html using decode then print one line at a time (more human readable)

    # In[4]:

    from urllib.request import urlopen
    from datetime import datetime

    # html is a HTTPResponse object
    html1 = urlopen(outletURLPage1)
    html2 = urlopen(outletURLPage2)

    # create a list of offered products
    results_string = []

    # convert html object into string using decode() then print each line
    for line in html1:
        #print(line.decode().strip())
        results_string.append(line.decode().strip())

    for line in html2:
        #print(line.decode().strip())
        results_string.append(line.decode().strip())



    # ### Parsing html string using regex

    # In[5]:

    from re import search

    # list to store all the offers, each offer's details are stored as a dictionary within the master list
    offers = []
    # index counter for the offers list
    j = -1
    # offer class
    class Offer():
        def __init__(self, condition):
            self.condition = condition


    for i in range(len(results_string)):
        if search(r'<div class="fl-item-condition">.*?</div>',results_string[i]):
            condition = search(r'<div class="fl-item-condition">(.*?)</div>',results_string[i]).group(1)
            if condition == "":
                condition = "Scratch and Dent"
            # create a new offer object to capture details of the new offer
            j += 1
            offers.append(Offer(condition))

        if search(r'<lft>Outlet Price</lft><rgt>.+?</rgt>',results_string[i]):
            price = search(r'<lft>Outlet Price</lft><rgt>£(.+?)</rgt>',results_string[i]).group(1)
            setattr(offers[j], "price", price)

        if search(r'<lft>Outlet Price From</lft><rgt>.+?</rgt>',results_string[i]):
            price = search(r'<lft>Outlet Price From</lft><rgt>£(.+?)</rgt>',results_string[i]).group(1)
            setattr(offers[j], "price", price)

        if search(r'<div class="fl-config-desc-container">',results_string[i]):
            # by observation, model name is 2 lines below the search line above
            model = search(r'<div>(.+?)</div>',results_string[i+2]).group(1)
            setattr(offers[j], "model", model)

            # by observation, model name is 2 lines below the search line above
            processor = search(r'<div>.+?i7-(.+?)</div>',results_string[i+4]).group(1)
            setattr(offers[j], "processor", processor)

            # by observation, model name is 2 lines below the search line above
            memory = search(r'<div>(.+?)</div>',results_string[i+8]).group(1)
            setattr(offers[j], "memory", memory)

        if search(r'<div>.+?B.+?SSD</div>',results_string[i]):
            SSD = search(r'<div>(.+?B.+?)SSD</div>',results_string[i]).group(1)
            setattr(offers[j], "SSD1", SSD)

        if search(r'<div>.+?B.+?Solid State.+?</div>',results_string[i]):
            SSD = search(r'<div>(.+?B).+?Solid State.+?</div>',results_string[i]).group(1)
            setattr(offers[j], "SSD2", SSD)

        if search(r'<div>(.+?B).+?Hard Drive.+?</div>',results_string[i]):
            HD = search(r'<div>(.+?B).+?Hard Drive.+?</div>',results_string[i]).group(1)
            setattr(offers[j], "HD", HD)

        if search(r'<div>.+?cell(.+?)Battery</div>',results_string[i]):
            battery = search(r'<div>.+?cell\s(.+?) Battery</div>',results_string[i]).group(1)
            setattr(offers[j], "battery", battery)








    # ## Output Results



    output.write("run time: " + str(run_time))
    output.write("\n")

    output.write("filtering condition:")
    output.write("- XPS 15 9560")
    output.write("- i7")
    output.write("- 15-16inch")
    output.write("- 3840x2160")
    output.write("")
    output.write("\n")

    num_offers = len(offers)
    output.write("number of offers found: "+str(num_offers))
    output.write("\n")

    # second offers list only containing 7xxx procesor
    offers_7 = []
    for i in range(num_offers):
        if search(r'^7',offers[i].processor):
            offers_7.append(offers[i])

    num_offers_7 = len(offers_7)
    output.write("number of 7xxx processor offers found: "+str(num_offers_7))
    output.write("\n")

    # third offers list only containing scratch and dent condition
    offers_dent = []
    for i in range(num_offers):
        if search(r'.+ent', offers[i].condition):
            offers_dent.append(offers[i])

    num_offers_dent = len(offers_dent)
    output.write("number of Scratch and Dent offers found: " + str(num_offers_dent))
    output.write("\n")

    output.write("\n")

    output.write("======================== offers with scratch and dent: ===========================")
    output.write("\n")

    if num_offers_dent == 0:
        output.write("None Found")
        output.write("\n")
    else:
        for i in range(num_offers_dent):
            output.write(offers_dent[i].model)
            output.write("\n")
            output.write(offers_dent[i].processor)
            output.write("\n")

            storage = ""
            if hasattr(offers_dent[i], "SSD1"):
                storage = storage + offers_dent[i].SSD1 + "SSD"
            if hasattr(offers_dent[i], "SSD2"):
                storage = storage + offers_dent[i].SSD2 + "SSD"
            if hasattr(offers_dent[i], "HD"):
                storage = storage + offers_dent[i].HD + "HD"
            storage.strip()
            output.write(storage)
            output.write("\n")

            output.write(offers_dent[i].price)
            output.write("\n")
            output.write(offers_dent[i].condition)
            output.write("\n")
            output.write(offers_dent[i].memory)
            output.write("\n")
            output.write("\n")


    output.write("======================== offers with 7xxx processor: ===========================")
    output.write("\n")

    for i in range(num_offers_7):
        output.write(offers_7[i].model)
        output.write("\n")
        output.write(offers_7[i].processor)
        output.write("\n")

        storage = ""
        if hasattr(offers_7[i], "SSD1"):
            storage = storage + offers_7[i].SSD1 + "SSD"
        if hasattr(offers_7[i], "SSD2"):
            storage = storage + offers_7[i].SSD2 + "SSD"
        if hasattr(offers_7[i], "HD"):
            storage = storage + offers_7[i].HD + "HD"
        storage.strip()
        output.write(storage)
        output.write("\n")

        output.write(offers_7[i].price)
        output.write("\n")
        output.write(offers_7[i].condition)
        output.write("\n")
        output.write(offers_7[i].memory)
        output.write("\n")
        output.write("\n")


    output.write("================================== all offers ====================================")
    output.write("\n")

    for i in range(num_offers):
        output.write(offers[i].model)
        output.write("\n")
        output.write(offers[i].processor)
        output.write("\n")

        storage = ""
        if hasattr(offers[i], "SSD1"):
            storage = storage + offers[i].SSD1 + "SSD"
        if hasattr(offers[i], "SSD2"):
            storage = storage + offers[i].SSD2 + "SSD"
        if hasattr(offers[i], "HD"):
            storage = storage + offers[i].HD + "HD"
        storage.strip()
        output.write(storage)
        output.write("\n")

        output.write(offers[i].price)
        output.write("\n")
        output.write(offers[i].condition)
        output.write("\n")
        output.write(offers[i].memory)
        output.write("\n")
        output.write("\n")

    output.close()

    return output_file

'''================================== send email ===================================='''

import win32com.client

def email_results(output_file):

    results_file = open(output_file, 'r')
    results = results_file.read()

    olMailItem = 0x0
    obj = win32com.client.Dispatch("Outlook.Application")
    newMail = obj.CreateItem(olMailItem)
    newMail.Subject = "dell outlet scan"
    newMail.Body = results
    newMail.To = "charleszhao@hotmail.co.uk"
    newMail.Send()

    results_file.close()

'''================================== run at interval ===================================='''

import subprocess
import time
from datetime import datetime


def run(run_interval, output_path):

    while True:
        start_time = time.time()
        run_time = datetime.now()

        interval_min = run_interval

        output_file = scan(output_path)
        email_results(output_file)

        print("scan completed at " + str(run_time))
        print("next scan scheduled in " + str(interval_min) + " mins")
        print
        time.sleep(60.0 * interval_min - (time.time() - start_time))

import sys
run_interval = sys.argv[1]
output_path = sys.argv[2]

run(run_interval, output_path)

