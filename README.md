## Instructions and Notes

### Notes
- I added the library dotenv to handle secrets.
- I had some issues with the Dates in Pandas. I wanted to have Nan values end up as Null in the DB but could not get sqlAlchemy to do it. Instead they get set to the lowest possible values for a sql date type. Probably missing something simple.
- In power bi I set the refresh to daily but at 8 different times so it should refresh every 3 hours.
- Initially i tried setting up the sql server through parrells VM on mac but it would Not install. So I ran a docker image on my mac and got it working.
- to get access to powerBI.com I ended up making an Azure account to get a non personal email address. After i setup the report I got the idea to move my sql server to Azure so that I didn't have to open ports on my home network and worry about my IP changing when I setup the web server. I can give you the IP and creds if you want them. 
- the web server is also running in Azure on a Ubuntu VM
- The web server is running on go using the http library that's part of the standard library. There's a couple of dependencies but they should auto install when you run go run main.go.
- I didn't bother with ssl/tls for the web server since it's just a demo and time was wanning.
- I also kept the styling and responsiveness of the page to a minimum for the sake of time.
### First
make a .env file and set the variables for 
- DATABASE = 
- USERNAME = 
- PASSWORD = 
- HOST = 
- PORT = 1433
- DRIVER = ODBC Driver 17 for SQL Server
- CSV_PATH=
- XLSX_PATH=
- TABLE_NAME=
Both the golang server and the python script will refrence these.
### Second install neccessary dependencies for python
```bash
pip install -r py_deps.txt
```
### Install GoLang if it's not installed. Required for the Web Server.
- Windows: https://go.dev/dl/go1.21.1.windows-amd64.msi
- Mac(Apple Silicon): https://go.dev/dl/go1.21.1.darwin-arm64.pkg
- Mac(Intel): https://go.dev/dl/go1.21.1.darwin-amd64.pkg
- Linux: https://go.dev/dl/go1.21.1.linux-amd64.tar.gz

cd into /web and run
```bash
go run main.go
```