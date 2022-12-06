class Virus(object):
    '''Properties and attributes of the virus used in Simulation.'''

    def __init__(self, name, repro_rate, mortality_rate):
        self.name = name
        self.repro_rate = repro_rate
        self.mortality_rate = mortality_rate


def test_virus_is_instance():
    new_virus = Virus('Flu', 0.12, 0.3)
    assert type(new_virus) == Virus

# Per project completion requirement - 2 additional tests:

def test_virus_instantiation():
    #TODO: Create your own test that models the virus you are working with
    '''Check to make sure that the virus instantiator is working.'''
    virus = Virus("enterovirus", 0.5, 0.7) #gave standard value of 0.5 
    assert virus.name == "enterovirus"
    assert virus.repro_rate == 0.5
    assert virus.mortality_rate == 0.7

def test_virus_attributes_type():
    virus = Virus('Corona', 0.5, 0.2)
    assert type(virus.name) == str
    assert type(virus.repro_rate) == int
    assert type(virus.mortality_rate) == int

if __name__ == "__main__":
    test_virus_instantiation()
    test_virus_is_instance()
    test_virus_attributes_type()