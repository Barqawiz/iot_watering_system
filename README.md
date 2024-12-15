# Watering System - IoT Final Project

Automated plant watering system that reads monitors soil moisture levels and activates a water pump as needed.

# Key Features
- Soil Moisture Monitoring.
- Pump Control.
- Configurable Thresholds.
- Logging.
- Monitoring dashboard.
- Mobile notification.

# Watering System Code

## Raspberry Pi with Sunfounder PCF8591 Module 

The watering system logic, including the moisture sensor readings, threshold comparison, and pump control, is implemented in the following file:
`sunfounder_component/watering_system.py`

# Dashboard

<img src="dashboard/dashboard_screen2.png" width="850px" />

## Run the dashboard
```bash
cd dashboard
python3 -m http.server 8000
```


# Disclaimer
This project is published under the MIT license. 
Any third-party libraries and modules used in this project are subject to their respective licenses.





