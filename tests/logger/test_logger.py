import pytest
from src.logger.log import logger


def test_logger_debug():
    logger.debug("debug message")
    assert True


def test_logger_info():
    logger.info("info message")
    assert True


def test_logger_warning():
    logger.warning("warning message")
    assert True


def test_logger_error():
    logger.error("error message")
    assert True


if __name__ == '__main__':
    pytest.main()
