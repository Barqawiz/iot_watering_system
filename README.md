# final_project

Automated plant watering system that reads monitors soil moisture levels and activates a water pump as needed.

# Dashboard

<img src="dashboard/dashboard_screen2.png" width="850px" />

## Run the dashboard
`python3 -m http.server 8000`

# Watering System Code

## Raspberry Pi with Sunfounder PCF8591 Module 

The watering system logic, including the moisture sensor readings, threshold comparison, and pump control, is implemented in the following file:
`sunfounder_component/watering_system.py`


