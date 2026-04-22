# Darkweb Scrapper

Full-stack dark web intelligence platform built with FastAPI + React.

This README is the complete A-to-Z guide for how the system works, how requests flow, how files are connected, and how to run/verify it in a real environment.

## 1) What This Project Does

Darkweb Scrapper scans URLs (including .onion targets), extracts intelligence signals, scores risk, stores historical scans, supports scheduled monitoring, and raises alerts when monitored risk increases.

Core outputs include:
- URL availability status (ONLINE, OFFLINE, TIMEOUT, ERROR)
- Threat score and risk level
- Category classification
- Extracted emails and crypto addresses
- Content change tracking via hash comparison
- Optional file forensics (strings, binwalk, exiftool, clamscan)
- Alert timeline and history views in frontend

## 2) Tech Stack

Backend:
- FastAPI, Uvicorn
- Pydantic + pydantic-settings
- Requests + SOCKS proxy (Tor)
- BeautifulSoup parser
- MongoDB via pymongo
- APScheduler for monitor jobs

Frontend:
- React + Vite
- Axios API client
- React Router
- Recharts for charts

External services/tools:
- Tor (required for .onion access)
- MongoDB Atlas/local MongoDB
- Optional: clamscan, binwalk, exiftool, strings

## 3) High-Level Architecture

Request path:
1. User interacts with React page.
2. Frontend calls API helper in `frontend/src/services/api.js`.
3. FastAPI route receives request.
4. Route calls service layer.
5. Service orchestrates scraper/parser/analyzer/downloader/file analyzer + DB.
6. Response is formatted and returned to frontend.
7. Frontend renders cards/charts/history/alerts.

Main backend entry:
- `backend/main.py`

Main frontend entry:
- `frontend/src/main.jsx`
- `frontend/src/App.jsx`

## 4) File Connection Map (Important)

### Backend flow map

- `backend/main.py`
  - Creates FastAPI app
  - Registers routers from `backend/app/api/routes`

- `backend/app/api/routes/*.py`
  - HTTP layer only
  - Calls service methods in `backend/app/services`

- `backend/app/services/scan_service.py`
  - Main scan orchestrator
  - Uses:
    - `backend/app/tor_proxy.py`
    - `backend/app/scraper.py`
    - `backend/app/parser.py`
    - `backend/app/analyzer.py`
    - `backend/app/downloader.py`
    - `backend/app/file_analyzer.py`
    - `backend/app/database.py`

- `backend/app/services/monitor_service.py`
  - Uses singleton `monitor_manager` from `backend/app/monitor.py`

- `backend/app/monitor.py`
  - APScheduler jobs
  - Re-runs scan pipeline periodically
  - Inserts alerts through `DatabaseManager.insert_alert`

- `backend/app/database.py`
  - MongoDB connection and CRUD
  - Collections:
    - `scraped_data`
    - `alerts`
    - `iocs`
    - `monitors`

- `backend/app/core/config.py`
  - Loads env configuration
  - Host/port, Tor proxy, DB, logging defaults

- `backend/app/logger.py`
  - Rotating log handlers:
    - `logs/system.log`
    - `logs/alerts.log`

### Frontend flow map

- `frontend/src/App.jsx`
  - Route shell with pages:
    - Dashboard
    - Monitors
    - History
    - Alerts
    - Analytics

- `frontend/src/pages/Dashboard.jsx`
  - Runs scans (`scanOnion`)
  - Loads comparison (`compareScans`)
  - Fetches alerts (`getAlerts`)
  - Creates/removes monitor (`createMonitor`, `deleteMonitor`)

- `frontend/src/pages/Monitors.jsx`
  - Lists and controls monitors

- `frontend/src/pages/History.jsx`
  - Reads latest-per-URL history list

- `frontend/src/pages/Alerts.jsx`
  - Reads and acknowledges alerts

- `frontend/src/pages/Analytics.jsx`
  - Builds statistics from history dataset

- `frontend/src/services/api.js`
  - Single API client used by all pages

## 5) End-to-End Scan Workflow

When user scans a URL from Dashboard:

1. Frontend POSTs `/scan` with `{ url }`.
2. Route `backend/app/api/routes/scan.py` calls `ScanService.scan_url`.
3. `sanitize_url` checks scheme (`http://` or `https://`).
4. `DatabaseManager` connects to MongoDB.
5. Tor session is created in `create_tor_session()`.
6. If URL is `.onion`, `test_tor_connection()` must pass.
7. `scrape_url()` fetches content and returns status metadata.
8. `parse_html()` extracts title, links, file links, text preview, keywords.
9. File links are downloaded (`download_file`) and analyzed (`analyze_file`).
10. `analyze_content()` computes hashes, IOC extraction, threat score, classification, risk.
11. `insert_scraped_data()` stores scan + status history + content change signal.
12. Service reloads latest document and formats API response.
13. Frontend renders cards/charts and timeline.

## 6) Monitoring Workflow

1. Frontend POSTs `/monitors` with URL + interval.
2. `MonitorService.create_monitor()` generates monitor id and registers scheduler job.
3. `MonitorManager` schedules `_scan_and_compare()` every interval minutes.
4. On each cycle:
   - fetch + parse + analyze
   - persist scan
   - compare threat score against previous scan
5. If risk score increases, alert is inserted in `alerts` collection.
6. Frontend pages refresh and show updated monitor/alert state.

## 7) History and Analytics Workflow

History:
- `/history` returns latest scan per URL using Mongo aggregation.
- `/history/{entry_id}` returns full detail for one document.

Comparison:
- `/compare?url=...` compares first (baseline) vs latest scan for same URL.
- Returns deltas (threat score, status changes, new IOCs, malicious files, reasons).

Analytics page:
- Reads history list and computes aggregate metrics in browser.

## 8) API Endpoints (Current)

Health:
- `GET /health`

Scan:
- `POST /scan`
- `GET /compare?url=<url>`

History:
- `GET /history`
- `GET /history/{entry_id}`

Monitors:
- `GET /monitors`
- `POST /monitors`
- `GET /monitors/{monitor_id}`
- `DELETE /monitors/all`
- `DELETE /monitors/{monitor_id}`
- `POST /monitors/{monitor_id}/pause`
- `POST /monitors/{monitor_id}/resume`

Alerts:
- `GET /alerts`
- `POST /alerts/{alert_id}/acknowledge`

## 9) Environment Configuration

Backend env file: `backend/.env`

Minimum required:
```env
MONGODB_URI=mongodb+srv://<user>:<pass>@<cluster>.mongodb.net/darkweb_scrapper?appName=darkwebCluster
DATABASE_NAME=darkweb_scrapper
COLLECTION_NAME=scraped_data
```

Optional/important:
```env
HOST=0.0.0.0
PORT=8000
REQUEST_TIMEOUT=30
DELAY_BETWEEN_REQUESTS=5
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
TOR_PROXY_HTTP=socks5h://127.0.0.1:9050
TOR_PROXY_HTTPS=socks5h://127.0.0.1:9050
```

Frontend env file: `frontend/.env`
```env
VITE_API_BASE_URL=http://localhost:8000
```

## 10) Installation and Run (A to Z)

A. Clone repository
```bash
git clone <your-repo-url>
cd darkweb-monitor
```

B. Backend virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

C. Install missing scheduler dependency if needed
```bash
pip install apscheduler
```

D. Configure backend env
- Copy values into `backend/.env`

E. Start Tor service
```bash
sudo apt install tor -y
sudo systemctl enable --now tor
ss -tlnp | grep 9050
```

F. Optional forensic tools
```bash
sudo apt install clamav clamav-daemon libimage-exiftool-perl binwalk -y
sudo freshclam
```

G. Frontend setup
```bash
cd frontend
npm install
```

H. Run backend
```bash
cd ..
./.venv/bin/python backend/main.py
```

I. Run frontend (new terminal)
```bash
cd frontend
npm run dev
```

J. Open app
- Frontend: `http://localhost:5173`
- Backend docs: `http://localhost:8000/docs`

## 11) How to Verify It Is Working

Backend checks:
```bash
curl http://localhost:8000/health
```
Expected:
```json
{"status":"ok"}
```

Scan test:
```bash
curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'
```

Frontend checks:
- Dashboard loads without CORS errors
- Scan request returns cards/charts
- History page shows records after scan
- Monitors page creates and refreshes monitor list
- Alerts page updates when threat increase occurs

## 12) Logging and Observability

Generated logs:
- `logs/system.log` (all events)
- `logs/alerts.log` (warning/error/critical focus)

Common startup messages:
- MongoDB connected
- monitor manager initialized
- API startup banner

## 13) Troubleshooting Guide

If `/scan` fails with connection errors:
- Verify Tor is running on `127.0.0.1:9050` for `.onion` targets.
- Verify `MONGODB_URI` is correct.

If monitor endpoints fail:
- Ensure `apscheduler` is installed.

If scan returns low data:
- Target may block requests or return non-text content.
- Parser intentionally rejects clear binary content types.

If file analysis is missing:
- Install `clamscan`, `binwalk`, and `exiftool`.
- System still runs without them; result includes tool status/errors.

If frontend cannot reach backend:
- Check `VITE_API_BASE_URL`.
- Check backend host/port and CORS settings.

## 14) Current Implementation Notes

- `.onion` URLs require Tor.
- Content change raises stored threat score by +15 (capped at 100).
- Monitor alerts are triggered when latest threat score exceeds previous score.
- History endpoint returns latest scan per URL for compact view.
- Monitor delete route currently shares decorators with pause handler in `backend/app/api/routes/monitors.py`; if DELETE `/monitors/{monitor_id}` does not remove a monitor in your environment, call `DELETE /monitors/all` or patch the route mapping.

## 15) Security and Legal Notice

This project is for research and defensive threat intelligence workflows.

You must:
- follow applicable law,
- only monitor targets you are authorized to access,
- avoid illegal or harmful use.

## 16) Quick File Index

- Backend entry: `backend/main.py`
- Frontend entry: `frontend/src/main.jsx`
- Router shell: `frontend/src/App.jsx`
- API client: `frontend/src/services/api.js`
- Scan orchestration: `backend/app/services/scan_service.py`
- Monitor scheduler: `backend/app/monitor.py`
- DB layer: `backend/app/database.py`
- Scraper: `backend/app/scraper.py`
- Parser: `backend/app/parser.py`
- Analyzer: `backend/app/analyzer.py`
- File downloader: `backend/app/downloader.py`
- File analyzer: `backend/app/file_analyzer.py`
- Config: `backend/app/core/config.py`
- Logger: `backend/app/logger.py`

---

If you want, the next step is I can also generate a matching `ARCHITECTURE.md` with sequence diagrams for `/scan`, monitor scheduler cycles, and alerts lifecycle.
