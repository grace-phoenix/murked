from sanic import Sanic, Request
from sanic.response import text, json, html
from sanic.log import logger
import asyncpg
import os

# Directory of the script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print("[INFO]: The base directory is", BASE_DIR)

# define db filepath
filepath = os.path.join(BASE_DIR, ".sectrets/db_link.txt")

app = Sanic("Murked")

@app.before_server_start
async def init(app) -> None:
    logger.info("Initializing application...")

    # Connect to the database
    try:
        with open(filepath, 'r') as f:
            app.ctx.db_pool = await asyncpg.create_pool(f.readline().rstrip('\n'))
    except FileNotFoundError:
        logger.error("[ERR]: File not found.")
        raise
    logger.info("Database connection established.")

@app.before_server_stop
async def shutdown(app) -> None:
    logger.info("Shutting down...")

    # Closing db connection
    await app.ctx.db_pool.close()
    logger.info("Database connection closed.")

@app.get("/")
async def handle_root(request):
    logger.info("Request received.")
    return html('<!DOCTYPE html><html lang="en"><meta charset="UTF-8"><div>Hai hai!</div>')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=16443)