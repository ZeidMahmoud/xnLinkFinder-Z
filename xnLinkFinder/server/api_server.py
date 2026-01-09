"""FastAPI REST API Server"""
try:
    from fastapi import FastAPI
    app = FastAPI(title="xnLinkFinder API", version="1.0")
    
    @app.get("/")
    def root():
        return {"message": "xnLinkFinder API Server"}
    
    @app.get("/scan")
    def scan(url: str):
        return {"url": url, "status": "queued"}
        
except ImportError:
    print("[!] FastAPI not installed. Server mode unavailable.")
    app = None

def start_server(host: str = "0.0.0.0", port: int = 8080):
    """Start the API server"""
    if app:
        try:
            import uvicorn
            uvicorn.run(app, host=host, port=port)
        except ImportError:
            print("[!] uvicorn not installed")
