# Tour de France Route Generator

## What this is and why I built it

This project generates random but realistic Tour de France race routes. Instead of just picking random cities, the core of the project models route generation as a set of requirements to be met. 

It ensures that is consists exactly on 21 stages and 2 rest days. Individual Time Trials are placed according to frequency rules, the generator does as well respect a minimum and maximum number of foreign stages (established by the user). It also uses a mountain-bias parameter to determine the distribution of stage types (flat, hilly, mountain).


## Architecture

The system is divided into three main parts: a data pipeline, a Python backend, and a web frontend.

### Data Pipeline
Before the generator can actually build routes, a clean dataset of start and finish locations is needed. The data pipeline takes raw location data and runs it through a multi-step process:
1. Normalization to standardize the names and formats.
2. Geocoding using Nominatim. This step includes strict caching and rate limiting to respect the API's usage policies.
3. Adding tags to classify locations based on geography and history.
4. Grouping into zones.

### Backend
The backend is a FastAPI application that serves the route generation logic. 

A design decision here is the use of the Singleton pattern for the LocationRepository. Because the location dataset is relatively large and it is only read, it is loaded it into memory exactly once at application startup rather than reading from disk for every request.

### Frontend
The frontend is a single page application built with React, Vite, and Tailwind CSS v4. Leaflet is used to visualize the routes on a map.

## How to run it locally

You will need Python 3 and Node.js installed on your machine.

To start the backend:
1. Navigate to the `backend` directory.
2. Create and activate a virtual environment (`python -m venv venv` and `source venv/bin/activate` in macOS/Linux or 'python -m venv venv' and 'venv\Scripts\activate' in Windows).
3. Install the dependencies using `pip install -r requirements.txt`.
4. Run the development server with `uvicorn app.main:app --reload`. It will be available at `http://localhost:8000`.

To start the frontend:
1. Navigate to the `frontend` directory.
2. Install the dependencies by running `npm install`.
3. Start the Vite development server with `npm run dev`. The application will be accessible at the local URL provided in the terminal (usually `http://localhost:5173`).