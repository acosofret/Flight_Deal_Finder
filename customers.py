import random
import requests
from my_vars import *
from data_manager import *

class NewCustomer:
  def __init__(self):
    print("Welcome to Andrei's Flight Club! \n")
    print("We save you the hassle, look up for best deals 24/7 and email you the best deals available.\n")
    self.first_name = input("What is your First Name ?\n")
    name_greetings = ["Cool name!","Lovely name!","Great name!","Sweet name!","Awesome name!","Fabulous name!","Wonderful name!","Terrific name!","Neat name!","Fantastic name!","Lovely choice of name!","Beautiful name!","Impressive name!","Excellent name!","Superb name!","Delightful name!","Admirable name!","Marvelous name!","Splendid name!","Outstanding name!"]
    print(random.choice(name_greetings))
    self.last_name = input("\nWhat is your Last Name ?\n")
    email_repeat = True
    while email_repeat:
      self.email = input("\nWhat you best email address?\n")
      email_test = input("Please type your email again:\n")
      if self.email == email_test:
        email_repeat = False
      else:
        print("The password didn't match. Please try again!")

    print(f"\nGreat! You are on-board now {self.first_name}. Welcome !")
    self.user_data = {
      "user": {
        "firstName": self.first_name,
        "lastName": self.last_name,
        "email": self.email,
      }
    }

  def sign_up(self):
    response = requests.post(url=my_users_spreadsheet, json=self.user_data)
    response.raise_for_status()
    code = response.json()["locations"][0]["code"]
    return code


  def add_new_user(self, update_endpoint, new_data):
    response = requests.post(url=update_endpoint, json=new_data)
    response.raise_for_status()

