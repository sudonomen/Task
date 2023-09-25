package web

import (
	"fmt"
	"html/template"
	"net/http"
)

var templates *template.Template

func main() {

}

func loadTemplates() {
	templates = template.Must(template.ParseGlob("*.html"))
}

func setupRoutes() {
	http.HandleFunc("/", indexHandler)

}

func indexHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Hello World")
}
