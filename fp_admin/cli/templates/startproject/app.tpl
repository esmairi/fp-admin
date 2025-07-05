import uvicorn
from fp_admin import FpAdmin

app = FpAdmin()

if __name__ == "__main__":
    uvicorn.run(
        "app:app", host="127.0.0.1", port=8000, reload=True, log_level="debug"
    )
