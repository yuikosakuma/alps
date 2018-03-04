# ALPS
collecting ALPS sensor data,   
sending to PostgreSQL database
## Collecting ALPS sensor data
- Blog: https://tomosoft.jp/design/?p=8104
- Used python interface "bluepy"
- Outputting sensor values to console
- Sampling rate
  - Motion sensor : 1sec
  - Environmental sensor : 1min
## Sending to database
- PostgreSQL database on Docker container 
- Used python subprocess to read console output
