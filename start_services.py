"""
GNS3 Copilot Services Manager

This module provides a unified service manager for starting both Chainlit
and FastAPI static server simultaneously with proper monitoring and
graceful shutdown capabilities.
"""

import subprocess
import signal
import sys
import time
import os
from typing import Dict, Optional
import threading
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ServiceManager:
    """Manages multiple services with monitoring and graceful shutdown."""

    def __init__(self):
        self.processes: Dict[str, subprocess.Popen] = {}
        self.running = True
        self.shutdown_event = threading.Event()

    def start_chainlit(self) -> bool:
        """Start Chainlit service."""
        try:
            # Get configuration from environment variables
            host = os.getenv("CHAINLIT_HOST", "0.0.0.0")
            port = os.getenv("CHAINLIT_PORT", "8000")

            print(f"[INFO] Starting Chainlit service on {host}:{port}...")
            process = subprocess.Popen(
                [
                    sys.executable, "-m", "chainlit", "run", "gns3_copilot.py",
                    "--host", host, "--port", port,"-w"
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            self.processes["chainlit"] = process
            print("[INFO] Chainlit service started successfully")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to start Chainlit: {e}")
            return False

    def start_fastapi(self) -> bool:
        """Start FastAPI static server."""
        try:
            # Get configuration from environment variables
            host = os.getenv("FASTAPI_HOST", "0.0.0.0")
            port = os.getenv("FASTAPI_PORT", "8001")

            print(f"[INFO] Starting FastAPI static service on {host}:{port}...")
            process = subprocess.Popen(
                [sys.executable, "static_server.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            self.processes["fastapi"] = process
            print("[INFO] FastAPI static service started successfully")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to start FastAPI: {e}")
            return False

    def monitor_services(self):
        """Monitor service processes and log their output."""
        while self.running and not self.shutdown_event.is_set():
            for service_name, process in list(self.processes.items()):
                if process.poll() is not None:
                    print(f"[WARNING] {service_name} service has stopped (exit code: {process.poll()})")
                    if self.running:
                        print(f"[INFO] Attempting to restart {service_name} service...")
                        if service_name == "chainlit":
                            self.start_chainlit()
                        elif service_name == "fastapi":
                            self.start_fastapi()

            time.sleep(2)  # Check every 2 seconds

    def wait_for_services(self):
        """Wait for services to be ready."""
        print("[INFO] Waiting for services to be ready...")
        time.sleep(3)  # Give services time to start

    def shutdown(self):
        """Gracefully shutdown all services."""
        print("\n[INFO] Shutting down all services...")
        self.running = False
        self.shutdown_event.set()

        for service_name, process in self.processes.items():
            try:
                print(f"[INFO] Stopping {service_name} service...")
                process.terminate()

                # Wait for graceful shutdown
                try:
                    process.wait(timeout=5)
                    print(f"[INFO] {service_name} service stopped gracefully")
                except subprocess.TimeoutExpired:
                    print(f"[WARNING] {service_name} service didn't stop gracefully, forcing...")
                    process.kill()
                    process.wait()
                    print(f"[INFO] {service_name} service stopped forcefully")

            except Exception as e:
                print(f"[ERROR] Failed to stop {service_name} service: {e}")

        print("[INFO] All services stopped")

    def check_ports(self) -> bool:
        """Check if required ports are available."""
        import socket

        def is_port_available(port):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind(('localhost', port))
                    return True
                except:
                    return False

        # Get ports from environment variables
        chainlit_port = int(os.getenv("CHAINLIT_PORT", "8000"))
        fastapi_port = int(os.getenv("FASTAPI_PORT", "8001"))

        if not is_port_available(chainlit_port):
            print(f"[ERROR] Port {chainlit_port} is already in use (Chainlit)")
            return False

        if not is_port_available(fastapi_port):
            print(f"[ERROR] Port {fastapi_port} is already in use (FastAPI)")
            return False

        return True

    def start(self):
        """Start all services."""
        print("=" * 60)
        print("GNS3 Copilot Services Manager")
        print("=" * 60)

        # Check ports availability
        if not self.check_ports():
            print("[ERROR] Required ports are not available. Please stop conflicting services.")
            return False

        # Start services
        if not self.start_chainlit():
            return False

        if not self.start_fastapi():
            self.shutdown()
            return False

        # Wait for services to be ready
        self.wait_for_services()

        # Get configuration from environment variables
        chainlit_host = os.getenv("CHAINLIT_HOST", "localhost")
        chainlit_port = os.getenv("CHAINLIT_PORT", "8000")
        fastapi_host = os.getenv("FASTAPI_HOST", "localhost")
        fastapi_port = os.getenv("FASTAPI_PORT", "8001")

        print("\n" + "=" * 60)
        print("✅ All services started successfully!")
        print("=" * 60)
        print("📊 Service URLs:")
        print(f"  • Chainlit Chat:     http://{chainlit_host}:{chainlit_port}")
        print(f"  • Reports Browser:   http://{fastapi_host}:{fastapi_port}/reports/")
        print(f"  • Health Check:      http://{fastapi_host}:{fastapi_port}/health")
        print("=" * 60)
        print("📝 Usage:")
        print("  • Use Chainlit interface for network automation")
        print(f"  • Browse reports at http://{fastapi_host}:{fastapi_port}/reports/")
        print("  • Press Ctrl+C to stop all services")
        print("=" * 60)

        # Start monitoring in background
        monitor_thread = threading.Thread(target=self.monitor_services, daemon=True)
        monitor_thread.start()

        return True


def signal_handler(signum, frame):
    """Handle Ctrl+C signal for graceful shutdown."""
    print("\n[INFO] Received shutdown signal")
    if 'manager' in globals():
        manager.shutdown()
    sys.exit(0)


def main():
    """Main entry point."""
    global manager

    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Check if we're in the right directory
    if not os.path.exists("gns3_copilot.py"):
        print("[ERROR] gns3_copilot.py not found. Please run from project root.")
        sys.exit(1)

    if not os.path.exists("static_server.py"):
        print("[ERROR] static_server.py not found. Please run from project root.")
        sys.exit(1)

    # Create and start service manager
    manager = ServiceManager()

    if manager.start():
        try:
            # Keep the main thread alive
            while manager.running:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            manager.shutdown()
    else:
        print("[ERROR] Failed to start services")
        sys.exit(1)


if __name__ == "__main__":
    main()
