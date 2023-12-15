This simple scipt will start a UI with all Catalyst Center (DNA Center) devices and an arrow next to each device; once clicked, the full config of the device will be downloaded in a .txt file.

important libraries to have:

- flask
- json
- requests
- uttlib3

Instructions:

1. in a directory of choice, place the app.py file in it
   1.1. edit the app.py file and add your credentials to access the Catalyst Center, and the IP address of the Catalysr Center
3. inside of that directory, create a folder with name "templates", and place the list_devices.html file in it
4. run the app.py by typing python app.py
