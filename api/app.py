from flask import Flask, request, jsonify, send_file, send_from_directory, g
from flask_cors import CORS
from typing import List
import logging
import os
import time
from io import BytesIO

from logging_config import setup_logging

setup_logging()

from models import Collection
from services.shuffle_manager import ShuffleManager
from services.moxfield_connector import MoxfieldConnector

logger = logging.getLogger(__name__)

app = Flask(
    __name__, static_folder="../frontend/dist/frontend/browser", static_url_path=""
)
CORS(app)


@app.before_request
def _start_timer():
    g.start_time = time.perf_counter()


@app.after_request
def _log_request(response):
    start = getattr(g, "start_time", None)
    elapsed_ms = (time.perf_counter() - start) * 1000 if start else 0
    logger.info(
        "%s %s -> %s %.0fms",
        request.method,
        request.path,
        response.status_code,
        elapsed_ms,
    )
    return response


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200


@app.route("/api/deck-name", methods=["POST"])
def get_deck_name():
    """
    Extract deck name from Moxfield URL
    Expected JSON: {"url": "https://www.moxfield.com/decks/..."}
    """
    try:
        data = request.get_json()
        url = data.get("url", "")

        if not url:
            return jsonify({"error": "URL is required"}), 400

        if "moxfield" not in url.lower():
            return jsonify({"error": "URL must be from Moxfield"}), 400

        deck_id = url.split("/")[-1]
        is_binder = "binder" in url.lower()
        deck_name = MoxfieldConnector.get_deck_name(deck_id, is_binder=is_binder)

        return jsonify({"name": deck_name}), 200
    except Exception as e:
        logger.exception("Failed to get deck name")
        return jsonify({"error": str(e)}), 500


@app.route("/api/reshuffle", methods=["POST"])
def reshuffle():
    """
    Perform reshuffle operation
    Expected JSON: [{"name": "...", "url": "...", "is_source": true/false}, ...]
    """
    try:
        data = request.get_json()

        if not data or not isinstance(data, list):
            return (
                jsonify(
                    {"error": "Invalid input format. Expected array of collections"}
                ),
                400,
            )

        if len(data) == 0:
            return jsonify({"error": "No collections provided"}), 400

        # Validate all URLs are from Moxfield
        for collection in data:
            if "moxfield" not in collection.get("url", "").lower():
                return jsonify({"error": "All URLs must be from Moxfield"}), 400

        # Filter active collections for validation
        active_data = [c for c in data if c.get("active", True)]

        # Check for at least one source and one target among active collections
        has_source = any(c.get("is_source") for c in active_data)
        has_target = any(not c.get("is_source") for c in active_data)

        if not has_source:
            return jsonify({"error": "At least one collection must be a source"}), 400
        if not has_target:
            return jsonify({"error": "At least one collection must be a target"}), 400

        # Convert to Collection objects
        collections = [Collection(**collection) for collection in data]

        # Run the shuffle manager
        manager = ShuffleManager(collections)
        logger.info(
            "Starting reshuffle: %d collections (%d active)",
            len(collections),
            len(active_data),
        )
        excel_file = manager.reshuffle()
        logger.info("Reshuffle complete (%d bytes)", len(excel_file))

        # Return the Excel file
        return send_file(
            BytesIO(excel_file),
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name="reshuffled.xlsx",
        )
    except Exception as e:
        logger.exception("Reshuffle failed")
        return jsonify({"error": str(e)}), 500


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_angular(path):
    """Serve Angular application"""
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info("Starting EDHRemixer API on port %s", port)
    app.run(host="0.0.0.0", port=port, debug=False)
