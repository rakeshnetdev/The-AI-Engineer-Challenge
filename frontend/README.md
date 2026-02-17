### Front End

#### How to run

1. Start the API server (from the project root):
   ```bash
   uvicorn api.index:app --reload --host 127.0.0.1 --port 8000
   ```

2. Open the frontend:
   - Open `index.html` in a browser, or
   - Use a local server: `python -m http.server 3000` then visit `http://localhost:3000`

3. Ensure the API is running at `http://127.0.0.1:8000` so the chat can connect to `/api/chat`.
