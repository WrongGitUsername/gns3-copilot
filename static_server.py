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

# Load environment variables
load_dotenv()

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
    print(f"Created reports directory: {reports_dir}")

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

    print("Starting GNS3 Copilot Reports Server...")
    print(f"Reports directory: {reports_dir}")
    print(f"Server configuration: {host}:{port}")
    print("Access URLs:")
    print(f"  - Root: http://{host}:{port}/")
    print(f"  - Reports: http://{host}:{port}/reports/")
    print(f"  - Health: http://{host}:{port}/health")

    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=False,
        log_level="info"
    )
