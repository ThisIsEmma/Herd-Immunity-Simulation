from logger import Logger
from simulation import Simulation
from virus import Virus

# test new simulation instantiation

def test_simulation_instantiation():
    flu = Virus('Flu', 0.6, 0.8)
    flu_sim = Simulation(10, 0.1, initial_infected=2, virus = flu)
    assert flu_sim.pop_size == 10
    assert flu_sim.virus is flu
    assert flu_sim.initial_infected == 2
    assert flu_sim.current_infected == 0
    assert flu_sim.vacc_percentage == 0.1
    assert flu_sim.file_name == "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(
            flu.name, flu_sim.pop_size, flu_sim.vacc_percentage, flu_sim.initial_infected)
    assert type(flu_sim.logger) is Logger

def test_create_population():
    flu = Virus('Flu', 0.6, 0.8)
    flu_sim = Simulation(10, 0.1, initial_infected=2, virus = flu)
    population = flu_sim._create_population(initial_infected=2)
    assert type(population) is list
    assert len(population) == flu_sim.pop_size

def test_get_total_vaccinated():
    flu = Virus('Flu', 0.6, 0.8)
    flu_sim = Simulation(10, 0.1, initial_infected=3, virus = flu)
    assert type(flu_sim.get_total_vaccinated()) is int
    assert flu_sim.get_total_vaccinated() == 1


if __name__ == "__main__":
    test_simulation_instantiation()
    test_create_population()
    test_get_total_vaccinated()