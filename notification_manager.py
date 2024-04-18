from twilio.rest import Client
from my_vars import *
class NotificationManager:
	# This class is responsible for sending notifications with the deal flight details.
	def __init__(self):
		self.client = Client(my_twilio_acc_sid, my_twilio_auth_token)

	def send_sms_notification(self, message_body):
		message = self.client.messages.create(body=message_body, from_=my_phone_number, to=my_twilio_number)
		print(message.sid)

