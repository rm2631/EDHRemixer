# EDHRemixer

A web application for managing and optimizing Magic: The Gathering EDH (Elder Dragon Highlander) collections and decks using Moxfield integration.

## Architecture

This application consists of two main components:

### Frontend (Angular SPA)
- Located in `/frontend` directory
- Built with Angular 18
- Provides a clean, user-friendly interface for collection management
- Communicates with the Flask API backend

### Backend (Flask API)
- Located in `/api` directory
- Python Flask REST API
- Handles Moxfield integration
- Processes card shuffling and optimization logic

## Features

- **Collection Management**: Add and manage Moxfield decks and binders
- **Type Classification**: Mark collections as Source or Target
- **Reshuffle Engine**: Optimally redistribute cards between collections
- **Sortable Interface**: Sort collections by name, URL, or type
- **Excel Export**: Download reshuffled collection data as Excel files

## Development Setup

### Prerequisites
- Python 3.12+
- Node.js 18+
- npm

### Backend Setup

```bash
cd api
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Setup

```bash
cd frontend
npm install
```

### Running Locally

1. Start the Flask API:
```bash
cd api
source .venv/bin/activate
python app.py
```

The API will run on `http://localhost:5000`

2. In another terminal, start the Angular dev server:
```bash
cd frontend
npm start
```

The frontend will run on `http://localhost:4200`

Note: For local development, the frontend will proxy API requests to the backend.

## Deployment on Render

This application is configured for deployment on Render using the `render.yaml` blueprint.

### Deployment Steps

1. Push your code to GitHub
2. Connect your repository to Render
3. Render will automatically detect the `render.yaml` file
4. The build process will:
   - Install Python dependencies
   - Build the Angular application
   - Configure the Flask app to serve the Angular SPA

### Environment Variables

No additional environment variables are required for basic operation. All Moxfield API calls are made server-side.

## API Endpoints

- `GET /api/health` - Health check endpoint
- `POST /api/deck-name` - Get deck name from Moxfield URL
  - Body: `{"url": "https://www.moxfield.com/decks/..."}`
- `POST /api/reshuffle` - Process card redistribution
  - Body: Array of collections with `name`, `url`, and `is_source` fields

## Project Structure

```
EDHRemixer/
├── api/                      # Flask backend
│   ├── app.py               # Main Flask application
│   ├── models/              # Data models
│   ├── services/            # Business logic
│   └── requirements.txt     # Python dependencies
├── frontend/                 # Angular frontend
│   ├── src/
│   │   ├── app/            # Angular components and services
│   │   ├── environments/   # Environment configuration
│   │   └── styles.css      # Global styles
│   ├── angular.json         # Angular CLI configuration
│   └── package.json         # Node dependencies
├── models/                   # Shared models (legacy)
├── services/                 # Shared services (legacy)
├── render.yaml              # Render deployment configuration
└── README.md                # This file
```

## Legacy Files

The following files are from the previous Streamlit implementation and are kept for reference:
- `main.py` - Original main application logic
- `ui.py` - Streamlit UI (deprecated)
- `test.py` - Test file

## License

This project is licensed under the MIT License.
