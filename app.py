import uvicorn
from web.core import app
# Import routes to register them with the app
import web.routes 

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)