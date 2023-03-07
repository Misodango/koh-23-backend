import os
import sys

from fastapi.logger import logger
from pydantic import BaseSettings


class Settings(BaseSettings):
    # ... The rest of our FastAPI settings

    BASE_URL = "http://localhost:8000"
    USE_NGROK = os.environ.get("USE_NGROK", "False") == "True"

def init_webhooks(base_url):
      # Update inbound traffic via APIs to use the public-facing ngrok URL
      pass

def setup_ngrok():
    settings = Settings()

    if settings.USE_NGROK:
        # pyngrok should only ever be installed or initialized in a dev environment when this flag is set
        from pyngrok import conf, ngrok

        # Get the dev server port (defaults to 8000 for Uvicorn, can be overridden with `--port`
        # when starting the server
        port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else 8000

        # Open a ngrok tunnel to the dev server
        conf.get_default().auth_token = os.environ.get("NGROK_AUTH_TOKEN")
        public_url = ngrok.connect(port).public_url
        logger.info("ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))

        # Update any base URLs or webhooks to use the public ngrok URL
        settings.BASE_URL = public_url
        init_webhooks(public_url)
  
    return settings