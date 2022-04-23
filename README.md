# Smart Card System with Arduino & Flask

## Table of contents

- [Overview](#overview)
- [Getting Started](#gettingstarted)
- [Contributors](#contributors)

## Overview  <a id="overview"></a>

Due to Pandemic and even before the COVID-19 pandemic, contactless payments were already a widely used payment method. There are very high chances that you lose the track of your expenditures while dealing with cash. People tend to rely more on online/contactless payment methods than traditional methods of transacting with cash. It helps the customer as well as the store to keep the record of all the transactions occurring throughout the system. In addition to that there are less chances of your cash getting robbed.
Smart Card System is such a unique website which works with the help of Arduino. RFID cards are used in the system which stands uniquely among each other due to its distinct identification number. It will act as a unique identity to every user in the system. In this website, login and register for both admin and user, add card, block/activate card, create payment, load balance functionalities are added for better user interaction.

<br>
With the Smart Card System you can :
<br>
🔽 Register & Login into the system.<br>
🔽 Get details about your card and transactions..<br>
🔽 Activate/Block your card for security purpose.<br>
🔽 Store/Admin login.<br>
🔽 Add Card, Load balance, Payment Gateaway at Store/Admin side.<br>
<br>
Functionalities Screenshot :

🔽 [User Registration](./output_images/user_registration.png)<br>
🔽 [User Login](./output_images/user_login.png)<br>
🔽 [User Dashboard](./output_images/user_dashboard.png)<br>
🔽 [Forgot Password](/output_images/reset_password.png)<br>
🔽 [Store/Admin Login](./output_images/admin_login.png)<br>
🔽 [Store/Admin Dashboard](./output_images/store_dashboard.png)<br>
🔽 [Create Payment](./output_images/payment.png)<br>
🔽 [OTP Received on Phone](./output_images/mobile_otp.jpg)<br>
🔽 [Enter OTP](./output_images/enter_otp.png)<br>
🔽 [Payment Unsuccessful 1](./output_images/payment_un_1.png)<br>
🔽 [Payment Unsuccessful 2](./output_images/payment_un_2.png)<br>
🔽 [Payment Successful](./output_images/payment_successful.png)<br>
🔽 [Add Card](./output_images/add_card.png)<br>
🔽 [Load Balance](./output_images/load_balance.png)<br>
🔽 [User DB](./output_images/user_db.png)<br>
🔽 [Store/Admin DB](./output_images/admin_db.png)<br>
🔽 [Transactions DB](./output_images/transactions_db.png)<br>
🔽 [Cards DB](./output_images/cards_db.png)<br>

## Built With
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Twilio](https://img.shields.io/badge/Twilio-F22F46?style=for-the-badge&logo=Twilio&logoColor=white)
![HTML](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

## Getting Started  <a id="gettingstarted"></a>

#### Step 1:

Download or clone this repository by using the command given below:

```
git clone https://github.com/lavsharmaa/ccl-mini-project.git
```

#### Step 2:

Go to project root and create a python environment using the below comamnd:

```
# For windows
python -m venv pyenv

# For Linux
python3 -m venv pyenv

# Alternate for Linux
pip install virtualenv

virtualenv pyenv
```

#### Step 3:

Activate your python environment using the below comamnd:

```
# For windows
pyenv\Scripts\activate

# For Linux
source pyenv/bin/activate
```

#### Step 4:

Install the dependencies using the below comamnd:

```
# For windows
pip install -r windows_requirements.txt

# For Linux
pip3 install -r linux_reuirements.txt
```

#### Step 5:

Since we have used twilio for messaging API you need to signup at [Twilio](https://www.twilio.com/) and register for the [MessagingAPI](https://www.twilio.com/docs/sms/send-messages):

You will need in total 3 keys
1. Account SID
2. Auth Token
3. Messaging API

which you need to put in the ```app.py``` file

#### Step 6:

For setting up the database we used postgresql and pgadmin4
```
# default values, might change for your system
host = "localhost"
dbname = "postgres"
user = "postgres"
password = "root"
```

#### Step 7:

Run flask using the below command:

```
python app.py
```
Load the website at ```localhost:5000```

## Contributors <a id="contributors"></a>
  - Samuel Monteiro<br> 
  [![Linkedin](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/samuel-monteiro-86103320a/)
  [![Github](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ssBEASTss)
  - Lav Sharma<br>
  [![Linkedin](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/lavsharmaa/)
  [![Github](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/lavsharmaa)
  - Rutuja Bhate<br>
  [![Linkedin](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/rutuja-bhate-2a5999192/)
  [![Github](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/rutuja1908)