package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
)

func DDos() error {
	req, err := http.Get("http://localhost:8080")
	if err != nil {
		return err
	}
	defer req.Body.Close()
	return nil
}

func TestLoginEndpoint() error {
	// JSON-Daten für den POST-Request
	loginData := map[string]string{
		"e-mail":   "febernard2111@gmail.com",
		"password": "123",
	}
	jsonData, err := json.Marshal(loginData)
	if err != nil {
		return err
	}

	// Erstelle eine neue HTTP POST-Anfrage
	req, err := http.NewRequest("POST", "http://localhost:8080/api/login", bytes.NewBuffer(jsonData))
	if err != nil {
		return err
	}

	// Setze den Content-Type Header
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Accept", "application/json")

	// req.AddCookie()

	// Erstelle einen HTTP-Client
	client := &http.Client{}

	// Versende die Anfrage
	resp, err := client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	// Überprüfe den Statuscode
	if status := resp.StatusCode; status != http.StatusOK {
		return fmt.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
	}

	// Cookies überprüfen
	cookies := resp.Cookies()
	var sessionIDCookie *http.Cookie
	for _, cookie := range cookies {
		if cookie.Name == "user" {
			sessionIDCookie = cookie
			break
		}
	}
	if sessionIDCookie == nil || sessionIDCookie.Value != "abc123" {
		return fmt.Errorf("expected session_id cookie with value 'abc123', got: %v", sessionIDCookie)
	}

	// Überprüfe die Antwortdaten
	expected := `{"message":"Login successful!"}`
	bodyBytes, _ := io.ReadAll(resp.Body)
	if string(bodyBytes) != expected {
		return fmt.Errorf("handler returned unexpected body: got %v want %v",
			string(bodyBytes), expected)
	}
	fmt.Println("Login successful")
	return nil
}

func TestProtectedEndpoint() error {
	// Erstes Login, um das Cookie zu erhalten
	loginData := map[string]string{
		"username": "testuser",
		"password": "testpass",
	}
	jsonData, err := json.Marshal(loginData)
	if err != nil {
		return err
	}
	req, err := http.NewRequest("POST", "http://192.168.2.118:8080/test", bytes.NewBuffer(jsonData))
	if err != nil {
		return err
	}
	req.Header.Set("Content-Type", "application/json")
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	// Extrahiere das Cookie
	var sessionIDCookie *http.Cookie
	for _, cookie := range resp.Cookies() {
		if cookie.Name == "user" {
			sessionIDCookie = cookie
			break
		}
	}

	if sessionIDCookie == nil {
		return fmt.Errorf("no session_id cookie found")
	}

	// Zweite Anfrage mit dem Cookie
	req, err = http.NewRequest("GET", "http://localhost:5000/protected", nil)
	if err != nil {
		return err
	}
	req.AddCookie(sessionIDCookie)

	resp, err = client.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	// Überprüfe den Statuscode
	if status := resp.StatusCode; status != http.StatusOK {
		return fmt.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusOK)
	}

	// Überprüfe die Antwortdaten
	expected := `{"message":"You are logged in!"}`
	bodyBytes, _ := io.ReadAll(resp.Body)
	if string(bodyBytes) != expected {
		return fmt.Errorf("handler returned unexpected body: got %v want %v", string(bodyBytes), expected)
	}
	fmt.Println("Access to Profile successful")
	return nil
}

// APIRequest enthält die Konfigurationsdaten für eine Anfrage
type APIRequest struct {
	URL                 string
	JSONPayload         map[string]string
	CookieName          string
	CookieValue         string
	CookieName2         string
	CookieValue2        string
	CookieName3         string
	CookieValue3        string
	ExpectedID          string // Erwarteter Cookie-Wert (z. B. "abc123")
	ExpectedBody        string
	ExpectedStatus      int
	Checkcookie         bool
	ToCheckCookieName   string
	ToCheckCookieValues string
}

// SendAPIRequest führt eine HTTP-Anfrage mit den angegebenen Parametern aus
func SendAPIRequest(apiReq APIRequest) error {
	// JSON-Daten erstellen
	jsonData, err := json.Marshal(apiReq.JSONPayload)
	if err != nil {
		return fmt.Errorf("error marshaling JSON: %v", err)
	}

	// Erstelle eine neue HTTP POST-Anfrage
	req, err := http.NewRequest("POST", apiReq.URL, bytes.NewBuffer(jsonData))
	if err != nil {
		return fmt.Errorf("error creating HTTP request: %v", err)
	}

	// Setze Header
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Accept", "application/json")

	// Setze den Cookie
	req.AddCookie(&http.Cookie{Name: apiReq.CookieName, Value: apiReq.CookieValue})
	req.AddCookie(&http.Cookie{Name: apiReq.CookieName2, Value: apiReq.CookieValue2})
	req.AddCookie(&http.Cookie{Name: apiReq.CookieName3, Value: apiReq.CookieValue3})

	// HTTP-Client erstellen
	client := &http.Client{}

	// Anfrage senden
	resp, err := client.Do(req)
	if err != nil {
		return fmt.Errorf("error executing HTTP request: %v", err)
	}
	defer resp.Body.Close()

	// Überprüfen der Antwort des Servers
	// Überprüfe den Statuscode
	if status := resp.StatusCode; status != apiReq.ExpectedStatus {
		return fmt.Errorf("handler returned wrong status code: got %v want %v", status, apiReq.ExpectedStatus)
	}

	// Cookies überprüfen
	cookies := resp.Cookies()
	var idCookie *http.Cookie
	for _, cookie := range cookies {
		if cookie.Name == apiReq.ToCheckCookieName { // Ersetze "user" durch den Namen des erwarteten Cookies
			idCookie = cookie
			break
		}
	}

	// Überprüfe, ob der 5. Buchstabe des ID-Cookies ein 'm' ist
	if apiReq.Checkcookie {
		if idCookie == nil || len(idCookie.Value) < 1 || idCookie.Value[0] != apiReq.ToCheckCookieValues[0] {
			return fmt.Errorf("expected the 5th character of the 'user' cookie to be 'm', got: %v", idCookie)
		}
		fmt.Printf("got cookie: %v\n", idCookie)
	}

	// Antwortdaten überprüfen
	// bodyBytes, err := io.ReadAll(resp.Body)
	// if err != nil {
	// 	return fmt.Errorf("error reading response body: %v", err)
	// }
	// if string(bodyBytes) != apiReq.ExpectedBody {
	// 	return fmt.Errorf("handler returned unexpected body: got %v want %v",
	// 		string(bodyBytes), apiReq.ExpectedBody)
	// }

	fmt.Println("Request successful")
	return nil
}

// Beispiel für mehrere API-Anfragen
func TestMultipleAPIRequests() {
	requests := []APIRequest{
		{
			URL:            "http://localhost:8080/api/nimda/283bf3/login",
			JSONPayload:    map[string]string{"e-mail": "febernard.business@web.de", "password": "123"},
			CookieName:     "key",
			CookieValue:    "a",
			CookieName2:    "none",
			CookieValue2:   "none",
			CookieName3:    "none",
			CookieValue3:   "none",
			ExpectedID:     "abc123",
			ExpectedBody:   `{"message":"Login successful!"}`,
			ExpectedStatus: 400,
			Checkcookie:    false,
		},
		{
			URL:                 "http://localhost:8080/api/nimda/283bf3/login",
			JSONPayload:         map[string]string{"e-mail": "febernard2111@gmail.com", "password": "123"},
			CookieName:          "joo",
			CookieValue:         "b",
			CookieName2:         "none",
			CookieValue2:        "none",
			CookieName3:         "none",
			CookieValue3:        "none",
			ExpectedID:          "xyz456",
			ExpectedBody:        `{"message":"Bitte geben sie eine andere E-mail an"}`,
			ExpectedStatus:      200,
			Checkcookie:         true,
			ToCheckCookieName:   "user",
			ToCheckCookieValues: "mm",
		},
	}

	for i, req := range requests {
		fmt.Printf("Testing request #%d...\n", i+1)
		if err := SendAPIRequest(req); err != nil {
			fmt.Printf("Error in request #%d: %v\n", i+1, err)
		}
	}
}

func main() {
	// for i := 0; i < 100; i++ {
	// 	if err := DDos(); err != nil {
	// 		fmt.Printf("Error in request #%d: %v\n", i+1, err)
	// 	}
	// }

	TestMultipleAPIRequests()

}
