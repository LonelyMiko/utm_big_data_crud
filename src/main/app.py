from dotenv import load_dotenv, find_dotenv
import uvicorn


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    uvicorn.run("src.main.ui.main:app", reload=True)
