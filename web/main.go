package main

import (
	"database/sql"
	"fmt"
	"html"
	"html/template"
	"net/http"
	"os"
	"time"

	_ "github.com/denisenkom/go-mssqldb"
	"github.com/joho/godotenv"
)

// This web server is contrived to demonstrate the use of templates and forms in golang and over simplified. Don't judge too harshly.
// In practice it could be a lot cleaner. I just wanted to get something working quickly.
var templates *template.Template
var db *sql.DB

type Employee struct {
	Name       string
	Department string
	Title      string
}

func main() {
	err := godotenv.Load("../env.env")
	if err != nil {
		fmt.Println("Error loading .env file")
	}
	connectToDB()
	loadTemplates()
	setupRoutes()
	http.ListenAndServe(":8080", nil)
}

func connectToDB() {
	// load environment variables and build the conn str
	connString := fmt.Sprintf("server=%s;port=%s;database=%s;user id=%s;password=%s;encrypt=true;trustservercertificate=true;app name=MyAppName;",
		os.Getenv("HOST"), os.Getenv("PORT"), os.Getenv("DATABASE"), os.Getenv("USERNAME"), os.Getenv("PASSWORD"))

	// Create conn pool set to db. It will be used globally. Not the best way but for the scope it works.
	var err error
	db, err = sql.Open("sqlserver", connString)
	if err != nil {
		fmt.Println("Error creating connection pool:", err.Error())
		os.Exit(1)
	} else {
		fmt.Println("Connected!")
	}
}

func loadTemplates() {
	templates = template.Must(template.ParseGlob("*.html"))
}

func setupRoutes() {
	http.HandleFunc("/", indexHandler)
	http.HandleFunc("/form", formHandler)
	http.HandleFunc("/submit", submitHandler)
	http.HandleFunc("/pbi", pbiHandler)
}

func formHandler(w http.ResponseWriter, r *http.Request) {
	templates.ExecuteTemplate(w, "form.html", nil)
}

func indexHandler(w http.ResponseWriter, r *http.Request) {
	templates.ExecuteTemplate(w, "index.html", nil)
}

func submitHandler(w http.ResponseWriter, r *http.Request) {
	var data Employee
	data.Name = html.EscapeString(r.FormValue("name"))
	data.Department = html.EscapeString(r.FormValue("department"))
	data.Title = html.EscapeString(r.FormValue("title"))
	fmt.Println(data)
	if tryInsertIntoDB(data) {
		templates.ExecuteTemplate(w, "success.html", data)
	} else {
		templates.ExecuteTemplate(w, "error.html", nil)
	}

}

func pbiHandler(w http.ResponseWriter, r *http.Request) {
	templates.ExecuteTemplate(w, "pbi.html", nil)
}
func tryInsertIntoDB(data Employee) bool {
	//parameterize the query. Inject me not!
	currentDate := time.Now().Format("2006-01-02")
	query := `INSERT INTO [data] ([Full Name], Department, Title, [Date]) VALUES (@Name, @Department, @Title, @Date)`
	_, err := db.Exec(query, sql.Named("Name", data.Name), sql.Named("Department", data.Department), sql.Named("Title", data.Title), sql.Named("Date", currentDate))
	if err != nil {
		fmt.Println("Error inserting data:", err.Error())
		return false
	} else {
		fmt.Println("Data inserted successfully!")
		return true
	}

}
