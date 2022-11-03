# Backend Rest

Make sure you have Docker installed!

To get testing:
1. Run `docker build -t flask-app-backend . `
2. Run `docker run -p 9823:5000 -d flask-app-backend`
3. Hit `http://localhost:9823/logs?password=<password>&istest=False` in either Postman or your
browser.  If it works, everything built correctly!