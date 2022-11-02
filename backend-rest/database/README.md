# Database
The SQL in this `server-backup.sql` is meant to be run by PSQL - it will not work as 
standard SQL syntax. 

`flask-user.sql` establishes the user to be used by the Flask endpoints.  It needs to be run 
before `server-backup.sql`.  You will get errors otherwise.

Be sure to update `backup-server.sql` when the schema changes.

## When Updating
Right-click the DB to be backed up, select `Backup`, choose the file name and
location, then change the format to `Plain`.  This is very important because
otherwise it will spit out a bunch of gibberish. 

## To Build Locally
In pgAdmin 4:
- Select the DB to update, or create a new one and name it `RobotRadarAlpha`
- Open up `PSQL Tool` from the `Tools` menu
- Copy and paste the contents of the `.sql` files into the shell
  - `flask-user.sql` needs to be run before `server-backup.sql`

## Docker Guide 
1. Run `docker build -t robot-radar-db .`
(NOTE: the ending period is very important do not forget)
2. Run: `docker run -dp 36000:5432 robot-radar-db`

### To use Postgres:
1. Run `docker exec -it <container-name> bash`
2. Run `psql -U postgres`

Be sure to restart the container so that the database service
starts after initialization.

You can make sure the tables were created by running `\dt` while in the PSQL shell.

To get the Docker container's IP:
`docker container inspect -f '{{ .NetworkSettings.IPAddress }}' <container name>`

### Deployment
1. Run `docker save -o postgres-robot.tar robot-radar-db`
2. 
