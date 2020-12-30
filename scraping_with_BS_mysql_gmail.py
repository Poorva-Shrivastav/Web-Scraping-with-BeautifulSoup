from bs4 import BeautifulSoup 
import requests 

import csv

import mysql.connector


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


import time 

my_url = "link_of_the_page_you_want_scarpe"

page = requests.get(my_url) 

soup = BeautifulSoup(page.content, "html.parser")
	
containers = soup.find_all("div", class_="_1xHGtK _373qXS")
#print(containers)

container = containers[0]


db = mysql.connector.connect(
	host="localhost",
	user="root",
	password="root@123",
	database='Minki'
	)

print(db)
print("Hello")

cursor = db.cursor()

for container in containers: 
	product_name = container.find_all("a", class_="IRpwTa") 

	name = (product_name[0].text)
	# print(name)

	price = container.find_all("div", class_="_30jeq3")
	#print(price[0])
	price = (price[0].text.lstrip('₹').replace(',','')) 
	int_price = (int(price)) 
	#print(int_price)

	link = container.find_all('a') 
	link_final = link[0].get('href') #returns only content in href 

	if int_price < 1000: 
		final_price = int_price
		# print(final_price)
		# print(name)
		#print(link_final)

		queryInsertInto = 'INSERT INTO sale_data(Name, Price, Link) \
		VALUES("%s", "%s", "%s")' % \
		(name, final_price, link_final)
		cursor.execute(queryInsertInto)  

db.commit()


print("Commit successful")

while True: #for scheduling mail. it will be sent only when the condition is True

	gmail_user = "gmail_user_name"
	gmail_password = "gmail_password"
	receiver = "who_should_receive_this_email"
	subject = "Alert Price Drop - Sale 2020"
	
	#setting up MIME
	msg = MIMEMultipart()
	msg['From'] = gmail_user
	msg['To'] = receiver
	msg['Subject'] = subject
	
	#Body of the mail
	body = "Price drop on Sale_2020"
	msg.attach(MIMEText(body,'plain'))

	filename = "file.csv" #csv file extracted from mysql table
	attachment = open(filename, 'rb')

	part = MIMEBase('application', 'octet-stream')
	part.set_payload(attachment.read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', "attachment; filename= " + filename)

	msg.attach(part)
	text = msg.as_string()
	
	#creating smtp session for sending the email
	server = smtplib.SMTP('smtp.gmail.com', 587) #using the port. 
	server.starttls() #enabling security
	server.login(gmail_user, gmail_password)

	server.sendmail(gmail_user, receiver, text)
	server.quit()

	time.sleep(30*60)  # 30 mins * 60 seconds 

file.close()

#use the less secure access for gmail account. Put in ON

