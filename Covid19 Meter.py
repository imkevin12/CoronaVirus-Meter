def slider():
    global count, sliderWords
    text = 'KEVIN CORONA METER'
    if (count >= len(text)):
        count = 0
        sliderWords = ''
    sliderWords += text[count]
    count += 1
    title.configure(text=sliderWords)
    title.after(200, slider)


def Scrap():
    def notifyme(title, message):
        plyer.notification.notify(
            title='CORONA UPDATE',
            message=message,
            app_icon='corona.ico',
            timeout=20
        )
    url = 'https://www.worldometers.info/coronavirus/'
    htmlCode = requests.get(url)
    soup = BeautifulSoup(htmlCode.content, 'html.parser')
    tableBody = soup.find('tbody')
    tableRow = tableBody.find_all('tr')
    notifycountry = countryName.get()

    if(notifycountry == ''):
        messagebox.showerror('Error', 'Please search country by name !')

    sn, countries, total_cases, new_cases, total_deaths, new_deaths, total_recovered, active_cases, serious_critical, totalcases_permillion, totaldeaths_permillion, total_tests, totaltests_permillion, population = [], [], [], [], [], [], [], [], [], [], [], [], [], []
    headers = ['sn', 'countries', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'total_recovered', 'active_cases',
               'serious_critical', 'totalcases_permillion', 'totaldeaths_permillion', 'total_tests', 'totaltests_permillion', 'population']

    for column in tableRow:
        tableColumn = column.find_all('td')
        if(tableColumn[1].text.strip().lower() == notifycountry.lower()):
            country_total_cases = tableColumn[2].text.strip()
            country_new_cases = tableColumn[3].text.strip()
            country_total_deaths = tableColumn[4].text.strip()
            country_new_deaths = tableColumn[5].text.strip()

            notifyme('Latest CoronaVirus Cases in {}'.format(notifycountry),
                     'Total Cases: {}\nNew Cases: {}\nTotal Deaths: {}\nNew Deaths: {}'.format(country_total_cases, country_new_cases, country_total_deaths, country_new_deaths))

        sn.append(tableColumn[0].text.strip())
        countries.append(tableColumn[1].text.strip())
        total_cases.append(int(tableColumn[2].text.strip().replace(',', '')))
        new_cases.append(tableColumn[3].text.strip())
        total_deaths.append(tableColumn[4].text.strip())
        new_deaths.append(tableColumn[5].text.strip())
        total_recovered.append(tableColumn[6].text.strip())
        active_cases.append(tableColumn[7].text.strip())
        serious_critical.append(tableColumn[8].text.strip())
        totalcases_permillion.append(tableColumn[9].text.strip())
        totaldeaths_permillion.append(tableColumn[10].text.strip())
        total_tests.append(tableColumn[11].text.strip())
        totaltests_permillion.append(tableColumn[12].text.strip())
        population.append(tableColumn[13].text.strip())

    df = pd.DataFrame(list(zip(sn, countries, total_cases, new_cases,total_deaths, new_deaths, total_recovered, active_cases,serious_critical,
                               totalcases_permillion, totaldeaths_permillion, total_tests, totaltests_permillion, population)),columns=headers)
    sor = df.sort_values('total_cases',ascending=False)
    for k in formatlist:
        if(k == 'html'):
            path2 = '{}/covid19 DATA.html'.format(path)
            sor.to_html(r'{}'.format(path2))
        if(k == 'json'):
            path2 = '{}/covid19 DATA.json'.format(path)
            sor.to_json(r'{}'.format(path2))
        if(k == 'csv'):
            path2 = '{}/covid19 DATA.csv'.format(path)
            sor.to_csv(r'{}'.format(path2))
    if(len(formatlist) !=0):
        messagebox.showinfo("Saved",'Covid19 Records are saved at: {}'.format(path2),parent=root)

def download():
    global path
    if(len(formatlist) != 0):
        path = filedialog.askdirectory()
    else:
        pass
    Scrap()
    formatlist.clear()
    html_btn.configure(state='normal')
    json_btn.configure(state='normal')
    csv_btn.configure(state='normal')

def dw_html():
    formatlist.append('html')
    html_btn.configure(state='disabled')

def dw_json():
    formatlist.append('json')
    json_btn.configure(state='disabled')

def dw_csv():
    formatlist.append('csv')
    csv_btn.configure(state='disabled')


# *************** Initially *************** #
import plyer
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tkinter import *
from tkinter import messagebox,filedialog

root = Tk()
root.title('CoronaVirus Meter')
root.geometry('390x160+450+200')
root.iconbitmap('corona.ico')
formatlist = []
path = ''
count = 0
sliderWords = ''


# *************** Labels *************** #
title = Label(root, text='', font=('open sans', 14, 'bold'), width=32, bg='#7FB3D5', justify=CENTER)
title.place(x=0,y=0)
slider()

countryName_label = Label(root, text='Country Name', font=('verdana', 12, 'bold'))
countryName_label.place(x=5, y=40)

downloads_label = Label(root, text='Downloads', font=('verdana', 12, 'bold'))
downloads_label.place(x=15, y=80)


# *************** Entries *************** #
countryName = StringVar()
countryName_entry = Entry(root, textvariable=countryName, font=('calibri', 14), relief=FLAT, width=24, bg='#A3E4D7')
countryName_entry.place(x=150, y=40)


# *************** Buttons *************** #
html_btn = Button(root, text='HTML', font=('sans serif', 12, 'bold'), bg='#F5B041', activebackground='#F8C471', relief=RAISED, bd=3, width=5, command=dw_html)
html_btn.place(x=170, y=75)

json_btn = Button(root, text='JSON', font=('sans serif', 12, 'bold'), bg='#F5B041', activebackground='#F8C471', relief=RAISED, bd=3, width=5, command=dw_json)
json_btn.place(x=240, y=75)

csv_btn = Button(root, text='CSV', font=('sans serif', 12, 'bold'), bg='#F5B041', activebackground='#F8C471', relief=RAISED, bd=3, width=5, command=dw_csv)
csv_btn.place(x=310, y=75)

search_btn = Button(root, text='SEARCH', font=('sans serif', 13, 'bold'), bg='#CB4335', activebackground='#CD6155', relief=FLAT, width=11, command=download)
search_btn.place(x=200, y=120)


root.mainloop()