# Jet, Set, Go!

This project is a simple travel application that incorporates flight bookings (Jet), hotel bookings (Set) and travel route planning (Go). 

## Description

There are 3 main scenarios that this web application supports.

1. Hotel and flight booking<br><br>

   Search process:
   <br>
   ![image](https://github.com/seldomearly69/ESD/assets/108080458/c87507a8-2553-4a26-a1bc-76f8d75b6abb)

   Booking process:
   <br>
   ![image](https://github.com/seldomearly69/ESD/assets/108080458/4bd2474b-1c4e-4e26-85f6-adc35d3554f0)



2. Hotel Administration<br><br>
   ![image](https://github.com/seldomearly69/ESD/assets/108080458/7a5ee183-c89d-4682-a9ff-075608675983)


3. Route planning and saving<br><br>
   ![image](https://github.com/seldomearly69/ESD/assets/108080458/7b12eb95-0d92-4913-8c40-369ea3faf214)
   


## Getting Started

### Executing program

1. Clone the repo
2. Open terminal and cd to the main directory (ESD)
3. Run the command : <code>docker compose build</code>
4. Run the command : <code>docker compose up</code>
5. Access the login page via <code>http://localhost:5050/login </code>

### Account details

You will need to log in to the web application to go through the different scenarios. It is recommended that you <b>create your personal account</b> using your own email and password as only then will you be able to see the email service in action (by checking your own email inbox).<br> Nonetheless, 2 dummy accounts have been created for ease of use without registering. They are:

<b>1. Regular customer</b>
   
Email: abc@gmail.com<br>
Password: 111


<br><b>2. Hotel Admin</b>

Email: admin@company.com <br>
Password: admin


## Help

1. If it does not run as intended, try removing all images before running docker compose build again.
2. There are multiple services that depend on rabbitmq connection, so please retry docker compose up if the service run out of retries.

