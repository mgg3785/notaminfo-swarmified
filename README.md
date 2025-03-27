# NOTAM Extraction & Parsing API with Django 🚀  

This repository is part of my journey in learning backend development with Django. Through this project, I’m gaining hands-on experience with building APIs, handling databases, working with background tasks, and data extraction.  

## ✨ Project Overview  

This project focuses on extracting and processing NOTAM (Notices to Airmen) texts, making them accessible via an API. The system is built with Django, Django REST Framework, Celery, and MySQL.  

### 🛠 Features  
🔍 **Automated NOTAM Extraction** – Uses web scraping to retrieve NOTAM texts  
🗄️ **Database Storage** – Stores extracted NOTAMs in a MySQL database  
📑 **Efficient Parsing** – Extracts relevant information from NOTAMs  
🌐 **REST API** – Provides a single API endpoint for accessing structured NOTAM data  
⚡ **Asynchronous Processing** – Utilizes Celery for background tasks  
🔑 **API Key Authentication** – Protects the API using `djangorestframework-api-key`  

## 🚀 Project Milestones  
- [x] Implementing MVP   
- [x] Using `UV` for dependency management   
- [x] Dockerization  
- [ ] Adding extra features      

### **Authentication: API Key Required**  
This API is **protected** using `djangorestframework-api-key`. To access it, you must provide a valid API key in the request headers.
For now, generating new API keys is only accessible through the admin panel.  

#### **Using the API Key in Requests**  
All requests must include the API key in the `Authorization` header as follows:  

```bash
Authorization: Api-Key YOUR_API_KEY_HERE
```

### **Using the API Endpoint**  

#### **1️⃣ Retrieve NOTAMs as Plain Text**  
- Retrieve a single NOTAM:  
  ```
  GET /textprovider/notams/1/
  ```
- Retrieve all NOTAMs:  
  ```
  GET /textprovider/notams/
  ```
- Search within NOTAM text using the `search` query parameter:  
  ```
  GET /textprovider/notams/?search=keyword
  ```

#### **2️⃣ Retrieve Parsed NOTAMs**  
- Fetch structured NOTAM data:  
  ```
  GET /textprovider/notams/1/?parsed=true
  ```

#### **3️⃣ Retrieve Parsed NOTAMs with Coordinates**  
- Fetch structured data including geographic coordinates:  
  ```
  GET /textprovider/notams/1/?parsed=true&coordinates=true
  ```

### **Response Example**  

A parsed NOTAM response includes structured fields such as the identifier, sections (A to F), created date, source, and optionally, extracted coordinates. Example:

```json
{
    "notam": 1,
    "identifier": "B0145/25 NOTAMN",
    "sec_q": "OIIX/QWMLW/IV/BO/W/000/090/3321N06044E006",
    "sec_a": "OIIX",
    "sec_b": "2502280330",
    "sec_c": "2503302030",
    "sec_d": "0330-2030",
    "sec_e": "GUN FIRING WILL TAKE PLACE...",
    "sec_f": "GND",
    "created": "2025-02-22T07:57:00Z",
    "source": "OIIIYNYX",
    "coordinates": [
        {
            "latitude": "33.3494444",
            "longitude": "60.7358333"
        }
    ]
}
```
