# 🌍 AgenticTrip AI

An AI-powered travel planning assistant built using FastAPI, React, OpenAI, Duffel Flights API, Google Places API, and Azure Cloud.

AgenticTrip helps users plan trips using natural language by combining multiple specialized travel agents for itinerary generation, flight discovery, hotel recommendations, and destination insights.

---

# 🏗️ Architecture Diagram

![AgenticTrip Architecture](docs/agentictrip-architecture.png)

The system follows a multi-agent architecture where user requests are routed through an intent detection layer and delegated to specialized travel agents.

---

# 🚀 Features

## ✈️ Flight Search Agent

Search available flights using natural language.

### Examples

* Find flights from Pune to Bali tomorrow
* Show flights from Mumbai to Singapore
* Flights from Delhi to Bangkok next week

### Powered By

* Duffel Flights API

---

## 🏨 Hotel Recommendation Agent

Discover highly-rated hotels for any destination.

### Examples

* Show hotels in Bali
* Best hotels in Singapore
* Find places to stay in Bangkok

### Powered By

* Google Places API

---

## 🗺️ AI Trip Planning Agent

Generate complete travel itineraries.

### Examples

* Plan a 5-day trip to Bali
* Create a 7-day itinerary for Thailand
* Plan a luxury vacation in Dubai

### Generated Itinerary Includes

* Destination overview
* Best areas to stay
* Estimated budget
* Food recommendations
* Daily activities

### Powered By

* OpenAI GPT-4.1 Mini

---

## 🧠 Session Memory

AgenticTrip maintains user session context.

### Example

User:

Plan a trip to Bali

Follow-up:

Show hotels

The application remembers the destination and can use previous context.

---

## 🎯 Intent Detection Engine

Natural language requests are routed automatically to the appropriate agent.

### Supported Intents

| Intent        | Agent              |
| ------------- | ------------------ |
| flight        | Flight Agent       |
| hotels        | Hotel Agent        |
| trip_planning | Trip Planner Agent |
| restaurants   | Planned            |
| weather       | Planned            |
| nightlife     | Planned            |
| booking       | Planned            |

---

# 🏛️ High-Level Architecture

```text
User
  │
  ▼
React Frontend
  │
  ▼
FastAPI Backend
  │
  ▼
Intent Router
  │
  ├── Trip Planner Agent
  │        │
  │        └── OpenAI GPT-4.1 Mini
  │
  ├── Flight Agent
  │        │
  │        └── Duffel Flights API
  │
  ├── Hotel Agent
  │        │
  │        └── Google Places API
  │
  └── Session Memory
```

---
# 🏗️ Architecture Diagram

![AgenticTrip Architecture](docs/agentictrip-architecture.png)

# 🛠️ Technology Stack

## Frontend

* React
* Vite
* Axios
* CSS

## Backend

* FastAPI
* Python
* Pydantic
* Uvicorn
* Gunicorn

## AI & External APIs

* OpenAI GPT-4.1 Mini
* Duffel Flights API
* Google Places API

## Cloud

* Azure Static Web Apps
* Azure App Service

## DevOps

* GitHub Actions
* CI/CD Pipelines

---

# 📂 Project Structure

```text
agentictrip-ai/

├── backend/
│
│   └── app/
│       ├── agents/
│       │   ├── flight_agent.py
│       │   ├── hotel_agent.py
│       │   └── trip_planner_agent.py
│       │
│       ├── memory/
│       │   └── session_memory.py
│       │
│       ├── tools/
│       │   ├── duffel_tool.py
│       │   ├── places_tool.py
│       │   └── weather_tool.py
│       │
│       ├── router.py
│       └── main.py
│
├── frontend/
│   ├── src/
│   ├── App.jsx
│   └── components/
│
├── docs/
│   └── agentictrip-architecture.png
│
└── README.md
```

---

# 🔑 Environment Variables

Create a `.env` file inside the backend folder.

```env
OPENAI_API_KEY=your_openai_api_key

DUFFEL_API_KEY=your_duffel_api_key
DUFFEL_API_URL=https://api.duffel.com

GOOGLE_API_KEY=your_google_api_key
GOOGLE_PLACES_API_KEY=your_google_places_api_key

OPENWEATHER_API_KEY=your_openweather_api_key

LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=AgenticTrip
LANGCHAIN_TRACING_V2=true
```

---

# ⚙️ Local Setup

## Clone Repository

```bash
git clone https://github.com/yourusername/agentictrip-ai.git

cd agentictrip-ai
```

---

## Backend Setup

```bash
cd backend

python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Backend

```bash
uvicorn app.main:app --reload
```

Backend URL:

```text
http://localhost:8000
```

Swagger Documentation:

```text
http://localhost:8000/docs
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

---

# ☁️ Azure Deployment

## Backend Deployment

Azure App Service

Startup Command:

```bash
gunicorn -w 1 -k uvicorn.workers.UvicornWorker app.main:app --bind=0.0.0.0:8000
```

---

## Frontend Deployment

Azure Static Web Apps

Deployment Flow:

```text
GitHub Repository
       │
       ▼
GitHub Actions
       │
       ▼
Azure Static Web Apps
```

---

# 🔄 Deployment Architecture

```text
GitHub Repo
     │
     ▼
GitHub Actions
     │
 ┌───┴─────────────┐
 ▼                 ▼

Azure Static       Azure App
Web Apps           Service

React UI           FastAPI Backend
```

---

# 📸 Sample Queries

### Trip Planning

```text
Plan a 5-day trip to Bali
```

### Hotels

```text
Show hotels in Bali
```

### Flights

```text
Flights from Pune to Bali tomorrow
```

---

# 🛣️ Roadmap

## Sprint 5

* Restaurant Agent
* Weather Agent
* Nightlife Agent

## Sprint 6

* Flight Booking Workflow
* Booking Confirmation Flow
* Enhanced Session Memory

## Sprint 7

* LangGraph Agent Orchestration
* Supervisor Agent
* Tool Calling Framework

## Sprint 8

* Persistent Memory Storage
* User Profiles
* Saved Trips
* Trip History

---

# 👨‍💻 Author

**Abhijeet Supnekar**

AI Engineer | Generative AI Developer | Agentic Systems Enthusiast

---

# 📄 License

This project is intended for educational, learning, and portfolio purposes.
