class Virus(object):
    '''Properties and attributes of the virus used in Simulation.'''

    def __init__(self, name, repro_rate, mortality_rate):
        self.name = name
        self.repro_rate = repro_rate
        self.mortality_rate = mortality_rate


def test_virus_instantiation():
    #TODO: Create your own test that models the virus you are working with
    '''Check to make sure that the virus instantiator is working.'''
    # virus = Virus("HIV", 0.8, 0.3)
    virus = Virus("enterovirus", 0.5, 0.7) #gave standard value of 0.5 
    assert virus.name == "enterovirus"
    assert virus.repro_rate == 0.5
    assert virus.mortality_rate == 0.7

#run tests
test_virus_instantiation()