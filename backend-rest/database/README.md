# Database
The SQL in this file is meant to be run by PSQL - it will not work as 
standard SQL syntax. 

Be sure to update this file when the schema changes.

Instructions for Docker will be available soon.

## When Updating
Right-click the DB to be backed up, select `Backup`, choose the file name and
location, then change the format to `Plain`.  This is very important because
otherwise it will spit out a bunch of gibberish. 

## To Build Locally
In pgAdmin 4:
- Select the DB to update, or create a new one and name it `RobotRadarAlpha`
- Open up `PSQL Tool` from the `Tools` menu
- Copy and paste the contents of this `.sql` file into the shell

## Docker Guide 
1. Run docker build -t robot-radar-db . 
(NOTE: the ending period is very important do not forget)
2. Run: docker run docker run -dp 36000:8080 robot-radar-db
3. To use postgres:
    - Run docker exec -it <container-name> bash
    - Run psql -U postgres