import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    filename="out/app.log"
)

logger = logging.getLogger("freedom-finder")
