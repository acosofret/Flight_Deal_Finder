import smtplib

from twilio.rest import Client
from my_vars import *
class NotificationManager:
	# This class is responsible for sending notifications with the deal flight details.
	def __init__(self):
		self.client = Client(my_twilio_acc_sid, my_twilio_auth_token)

	def send_sms_notification(self, message_body):
		message = self.client.messages.create(body=message_body, from_=my_twilio_number, to=my_phone_number)
		print(message.sid)

	def send_email_notification(self, my_email, password, customer, message_body):
		with smtplib.SMTP("smtp.gmail.com") as connection:
			connection.starttls()
			connection.login(user=my_email, password=password)
			connection.sendmail(from_addr=my_email, to_addrs=customer, msg=message_body)



