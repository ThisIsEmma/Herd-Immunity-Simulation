from logger import Logger

def test_logger_instantiation():
    test_logger = Logger('new_file.txt')
    assert test_logger.file_name == 'new_file.txt'

def test_write_metadata():
    test_logger = Logger('new_file.txt')
    data = test_logger.write_metadata(1000, 0.20, 'Ebola', 0.2, 0.3, 10)
    assert type(data) is list
    assert data[0] == {'population size' : 1000}

def test_log_time_step(time_step_number=3, new_death=2, total_death=12, current_infected=4, total_infected=25, pop_size=150, total_vaccinated=70):
    assert time_step_number == int
    assert new_death == int
    assert total_death == int
    assert current_infected == int
    assert total_infected == int
    assert pop_size == int
    assert total_vaccinated == int


if __name__ == "__main__":
    test_logger_instantiation()
    test_write_metadata()
    