# Catalyst Center Device Configuration Downloader

## Project Title
Catalyst Center Device Configuration Downloader


## Overview
This project is designed to facilitate the easy retrieval and downloading of the full configuration of Catalyst Center (DNA Center) devices through a user-friendly web interface. It utilizes Flask as the web framework and requires specific libraries for proper functionality.


## Prerequisites
Ensure the following libraries are installed:

```bash
pip install flask json requests urllib3
```


## Installation

Clone this repository:

```bash
git clone https://github.com/jumaluwati/dnac.git
```

Navigate to the ConfigUI directory:

```bash
cd dnac/ConfigUI
```

Edit the app.py file to add your Catalyst Center credentials and the IP address of the Catalyst Center:

```python
# Edit the following lines in app.py
DNAC_IP = "your_dna_center_ip"
USERNAME = "your_username"
PASSWORD = "your_password"
```

Create a folder named "templates" in the same directory and place the list_devices.html file in it:

```bash
mkdir templates
cp path/to/list_devices.html path/to/dnac/ConfigUI/templates/
```

Run the application by executing the following command:

```bash
python app.py
```

Visit http://localhost:5000 in your web browser to access the Catalyst Center Device Configuration Downloader.


## Usage

Open the web interface by navigating to http://localhost:5000.
Click on the arrow next to each device to view additional options.
Download the full configuration of a device by clicking the respective option.



![Catalyst Center Device Config Downloader](https://github.com/jumaluwati/dnac/raw/main/ConfigUI/Collateral/screenshot1.png)



## Important Note

Ensure that your Catalyst Center credentials are kept secure and not shared with unauthorized individuals.


## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request. Issues and feature requests can be submitted through the GitHub issue tracker.

