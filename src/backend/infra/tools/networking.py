import socket
from time import sleep

from pymongo.uri_parser import parse_uri

from ..log import logging

logger = logging.getLogger("networking")


def test_tcp_port(host: str, port: int, retries: int = 1) -> bool:
    if not isinstance(retries, int) or retries < 1:
        retries = 1

    success = False
    retry = False
    while retries > 0 and not success:
        try:
            s = socket.socket()
            s.connect((host, port))
            success = True
            if retry:
                logger.info(f"Connection OK on TCP {host}:{port} after retry")
        except Exception as e:
            logger.error(f"Error connecting TCP {host}:{port} = {str(e)}")
            retries = -1
            if retries > 0:
                logger.warning("Retrying...")
                sleep(0.5)

        finally:
            s.close()

    return success


def test_mongodb(connectionstring: str) -> bool:
    uri = parse_uri(connectionstring)
    try:
        host = uri['nodelist'][0][0]
        port = uri['nodelist'][0][1]
        return test_tcp_port(host, port)
    except Exception as e:
        logger.error(
            f"Error parsing connection string '{connectionstring}: {str(e)}")

    return False
