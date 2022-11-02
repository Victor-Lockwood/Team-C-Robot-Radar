# Backend Rest

Make sure you have Docker installed!

To get testing:
1. Run `docker build -t flask-app-backend:1.0.2 . `
2. Run `docker run -p 9823:5000 -d flask-app-backend:1.0.2`
3. Hit `http://localhost:9823/mapdata` in either Postman or your
browser.  If it works, everything built correctly!