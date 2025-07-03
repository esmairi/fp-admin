import uvicorn

from fp_admin.app import app


if __name__ == "__main__":
    uvicorn.run("fp_admin.app:app", host="127.0.0.1", port=8000, reload=True, log_level="debug")
