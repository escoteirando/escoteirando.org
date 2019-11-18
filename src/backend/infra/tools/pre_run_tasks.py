from ..config import config
from ..log import getLogger
from .networking import test_mongodb

logger = getLogger("pre_run_tasks")


def pre_run_tasks():
    logger.info("Pre-run tasks")
    if not test_mongodb(config.MONGODB_URL):
        logger.error("MONGODB UNAVAILABLE")
        return False

    logger.info("MONGODB OK")
    return True
