"""
FastAPI Static File Server for GNS3 Copilot Reports

This module provides a simple FastAPI application to serve static HTML reports
from the reports directory. It allows users to browse and access generated
technical reports through a web interface.
"""

import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from tools.logging_config import setup_tool_logger

# Load environment variables
load_dotenv()

# Set up logger for static server
logger = setup_tool_logger("static_server")

# Create FastAPI application
app = FastAPI(
    title="GNS3 Copilot Reports Server",
    description="Static file server for GNS3 Copilot technical reports",
    version="1.0.0"
)

# Get the absolute path to the reports directory
reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")

# Check if reports directory exists
if not os.path.exists(reports_dir):
    os.makedirs(reports_dir, exist_ok=True)
    logger.info("Created reports directory: %s", reports_dir)
else:
    logger.debug("Reports directory exists: %s", reports_dir)

# Mount the reports directory as static files
app.mount("/reports", StaticFiles(directory=reports_dir, html=True), name="reports")

@app.get("/")
async def root():
    """
    Redirect root path to reports directory
    """
    return RedirectResponse(url="/reports/")

@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return {
        "status": "healthy",
        "service": "GNS3 Copilot Reports Server",
        "reports_dir": reports_dir,
        "reports_count": len([f for f in os.listdir(reports_dir) if f.endswith('.html')])
    }

if __name__ == "__main__":
    import uvicorn

    # Get configuration from environment variables
    host = os.getenv("FASTAPI_HOST", "0.0.0.0")
    port = int(os.getenv("FASTAPI_PORT", "8001"))

    logger.info("Starting GNS3 Copilot Reports Server...")
    logger.info("Reports directory: %s", reports_dir)
    logger.info("Server configuration: %s:%s", host, port)
    logger.info("Access URLs:")
    logger.info("  - Root: http://%s:%s/", host, port)
    logger.info("  - Health: http://%s:%s/health", host, port)

    try:
        uvicorn.run(
            app,
            host=host,
            port=port,
            reload=False,
            log_level="info"
        )
    except Exception as e:
        logger.error("Failed to start server: %s", e)
        raise
