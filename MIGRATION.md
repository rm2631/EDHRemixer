# Migration from Streamlit to Angular + Flask

This document describes the migration from the original Streamlit application to an Angular SPA with Flask API backend.

## Original Architecture

The original application was built using:
- **Streamlit** for the UI (`ui.py`)
- **Python services** for backend logic
- Direct integration between UI and services

### Files from Original Implementation
- `ui.py` - Streamlit UI (deprecated)
- `main.py` - Main application logic
- `models/__init__.py` - Data models
- `services/` - Business logic services
- `requirements.txt` - Python dependencies

## New Architecture

The refactored application uses:
- **Angular 18** for the frontend SPA
- **Flask 3.1** for the REST API backend
- **Separation of concerns** with clear API boundaries

### New File Structure

```
EDHRemixer/
├── api/                          # Flask Backend
│   ├── app.py                   # Flask application with API endpoints
│   ├── models/                  # Data models (copied from root)
│   │   └── __init__.py
│   ├── services/                # Business logic (copied from root)
│   │   ├── moxfield_connector.py
│   │   ├── shuffle_manager.py
│   │   └── cost_optimizer.py
│   └── requirements.txt         # Backend dependencies
│
├── frontend/                     # Angular Frontend
│   ├── src/
│   │   ├── app/
│   │   │   ├── models/         # TypeScript interfaces
│   │   │   │   └── collection.model.ts
│   │   │   ├── services/       # API service layer
│   │   │   │   └── api.service.ts
│   │   │   ├── app.component.ts
│   │   │   ├── app.component.html
│   │   │   └── app.component.css
│   │   ├── environments/       # Environment configs
│   │   │   ├── environment.ts
│   │   │   └── environment.prod.ts
│   │   └── styles.css
│   ├── angular.json
│   ├── package.json
│   └── proxy.conf.json         # Dev proxy configuration
│
├── render.yaml                  # Render deployment config
└── README.md                    # Updated documentation
```

## API Endpoints

The Flask backend exposes the following REST API endpoints:

### `GET /api/health`
Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "healthy"
}
```

### `POST /api/deck-name`
Retrieves the deck name from a Moxfield URL.

**Request:**
```json
{
  "url": "https://www.moxfield.com/decks/..."
}
```

**Response:**
```json
{
  "name": "Deck Name"
}
```

### `POST /api/reshuffle`
Processes card redistribution and returns an Excel file.

**Request:**
```json
[
  {
    "name": "Collection 1",
    "url": "https://www.moxfield.com/decks/...",
    "is_source": true
  },
  {
    "name": "Collection 2",
    "url": "https://www.moxfield.com/decks/...",
    "is_source": false
  }
]
```

**Response:**
Binary Excel file download

## Migration Benefits

### 1. Modern Architecture
- Clean separation between frontend and backend
- RESTful API design
- Industry-standard frameworks

### 2. Better Development Experience
- Hot reload for both frontend and backend
- Type safety with TypeScript
- Better debugging tools

### 3. Improved Deployment
- Single deployment configuration
- Better scalability options
- Easier to integrate with CI/CD

### 4. Future Extensibility
- API can support mobile apps or other clients
- Frontend can be easily updated independently
- Backend can be scaled separately

## Feature Mapping

All features from the original Streamlit application have been preserved:

| Feature | Streamlit Implementation | Angular + Flask Implementation |
|---------|-------------------------|-------------------------------|
| Add Collection | Text input + button | Text input + button with API call |
| Collection List | Streamlit dataframe | HTML table with sorting |
| Type Selection | Streamlit selectbox | HTML select dropdown |
| Delete Collection | Streamlit button | Delete button with confirmation |
| Reshuffle | Streamlit download button | API call with blob download |
| Sorting | Streamlit session state | Client-side sorting |
| Error Handling | Streamlit error messages | Alert components |
| Loading States | Streamlit spinner | Loading overlay |

## Deployment Changes

### Original (Streamlit on Azure)
- Deployed as Python web app
- Required Streamlit-specific configuration
- Azure-specific deployment files

### New (Flask + Angular on Render)
- Unified deployment with `render.yaml`
- Build process handles both frontend and backend
- More flexible deployment options

## Development Workflow

### Original
1. Install Python dependencies
2. Run `streamlit run ui.py`
3. Access at `http://localhost:8501`

### New
1. **Backend:**
   ```bash
   cd api
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   python app.py
   ```

2. **Frontend:**
   ```bash
   cd frontend
   npm install
   npm start
   ```

3. Access at `http://localhost:4200` (proxies to backend at port 5000)

## Testing

### Original
- Manual testing through Streamlit UI
- Python unit tests

### New
- Frontend: Angular component tests
- Backend: Flask API endpoint tests
- Integration: End-to-end API tests
- Same Python unit tests for business logic

## Maintenance Notes

### Legacy Files
The following files are kept for reference but are no longer used:
- `ui.py` - Original Streamlit UI
- Root-level `models/` and `services/` - Replaced by `api/models/` and `api/services/`

These can be removed in a future cleanup if desired.

### Configuration
- **Development:** Uses proxy to forward API calls
- **Production:** Flask serves Angular static files directly
- **Environment Variables:** PORT for Render deployment

## Troubleshooting

### Issue: CORS errors in development
**Solution:** Ensure Flask-CORS is installed and CORS is enabled in `api/app.py`

### Issue: API calls fail from Angular
**Solution:** Check that `proxy.conf.json` is configured and Flask is running on port 5000

### Issue: Build fails on Render
**Solution:** Verify `render.yaml` has correct build commands for both frontend and backend

### Issue: Static files not served in production
**Solution:** Ensure Angular build output is in `frontend/dist/frontend/browser` and Flask `static_folder` is configured correctly

## Future Enhancements

Potential improvements for the future:
1. Add authentication/authorization
2. Implement user accounts for saving collections
3. Add real-time updates using WebSockets
4. Create mobile-responsive design improvements
5. Add comprehensive test suite
6. Implement caching for Moxfield API calls
7. Add analytics and monitoring
8. Implement dark mode
9. Add export formats beyond Excel
10. Create admin dashboard

## Questions or Issues?

For questions about this migration, please refer to:
- README.md for deployment instructions
- This MIGRATION.md for architecture details
- GitHub Issues for bug reports or feature requests
