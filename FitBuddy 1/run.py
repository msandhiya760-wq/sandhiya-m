"""
FitBuddy - Application Launcher
Runs the FastAPI Uvicorn ASGI server with live reloading.
"""
import uvicorn

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  🏋️  FitBuddy – AI Fitness Plan Generator")
    print("  Powered by FastAPI & Google Gemini Models")
    print("=" * 60)
    print("  • Web Application:  http://127.0.0.1:8000")
    print("  • Admin Dashboard:  http://127.0.0.1:8000/view-all-users")
    print("  • API Swagger Docs: http://127.0.0.1:8000/docs")
    print("=" * 60 + "\n")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
