import logging


def configure_logger():
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )


configure_logger()


def die(message):
    logging.error(message)
    exit(1)
