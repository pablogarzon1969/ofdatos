from src.infraestructure.log.logData import LogData


def test_log():
    log = LogData(message="error")

    assert log.message == 'error'
