import uvicorn
from modules.code_reader.code_reader import CodeReader
from api import app



if __name__ == '__main__':
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
