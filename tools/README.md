# Tools
## Pre-requisite
* Install python3
* Make sure pip3 executable is recognized from terminals or command prompts
* pip3 install requests

## Get Code to you system
* Create live247 directory and go to it
* Clone git repo https://github.com/healthyvibes/tools
* Clone git repo https://github.com/healthyvibes/automation

## Send Sensor Data to one patient and one sensor
* Set PYTHONPATH enviornment variable like on bash shell - export PYTHONPATH=/home/arunmandava/live247/automation/
* cd live247/tools/bin/sensordata
* Execute ./sensor_data.py command with required options to send sensor data to cloud application
    ```commandline
    cd tools/bin/sensordata
    
    # Show command help
    python3 ./send_data.py -h
  
    # Send Temperature Data
    python3 ./send_data.py -M ArunTest001 -S http://20.230.234.202:7124 -U testadmin001@test.com -P admin123 -L hospital -T temp -F 10
 
     # Send ECG Data for 120secs with frequency of 1 sec
    python3 ./send_data.py -M ArunTest001 -S http://20.230.234.202:7124 -U testadmin001@test.com -P admin123 -L hospital -T ecg -F 1 -D 120

    # Send SPo2 data every 2 mins for 3 hrs
    python3 ./send_data.py -M 00.09 -S http://20.230.234.202:7124 -U superadmin@demohospital.com -P admin123 -L hospital -T spo2 -F 120 -D 10800

    # Send Alphamed data ever 2 mins for 3 hrs
    python3 ./send_data.py -M 00.09 -S http://20.230.234.202:7124 -U superadmin@demohospital.com -P admin123 -L hospital -T bp_alphamed -F 120 -D 10800

    # Send iHealth data ever 2 mins for 3 hrs
    python3 ./send_data.py -M 00.09 -S http://20.230.234.202:7124 -U superadmin@demohospital.com -P admin123 -L hospital -T bp_ihealth -F 120 -D 10800

    # Send Digital scal data every 10 mins for 3 hrs
    python3 ./send_data.py -M 00.09 -S http://20.230.234.202:7124 -U superadmin@demohospital.com -P admin123 -L hospital -T digital -F 600 -D 10800

    # Send keep alive every 10 mins for 3 hrs
    python3 ./send_data.py -M 00.09 -S http://20.230.234.202:7124 -U superadmin@demohospital.com -P admin123 -L hospital -T keepalive -F 60 -D 10800

     ```
 
## Send Sensor data to all devices attached to a patient
* cd live247/tools/bin
* Execute ./simulate_sensor_data.py command with required options to send data as sensors attahed to a patient 
  ``` 
  python3 simulate_sensor_data.py -S http://us.livehealthyvibes.com:7124 -U demoadmin01@live247.com -P admin123 -T "Demo Hospital 01" --mrn=MRNDemo0100000001 --ptype Hospital -D 1200
  
* Inorder to send data for multple patients we can use shall script like below (till we have pure python solution)
  * Example:
  ```
  DURATION=120
  MRNLIST="MRNDemo0100000002 MRNDemo0100000003 MRNDemo0100000004"
  for mrn in $MRNLIST
  do
       echo "Simulating data for $mrn"
       python3 simulate_sensor_data.py -S http://us.livehealthyvibes.com:7124 -U user@test.com -P admin123 -T "Demo Hospital 01" --mrn=$mrn --ptype Hospital -D $DURATION &
  done
  ```
  Note: Use different terminal or task manager to kill the runs.      

