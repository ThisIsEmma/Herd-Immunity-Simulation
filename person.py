import random
from random import randint
random.seed(42)
from virus import Virus


class Person(object):
    ''' Person objects will populate the simulation. '''

    def __init__(self, _id, is_vaccinated, infection=None):
        ''' We start out with is_alive = True, because we don't make vampires or zombies.
        All other values will be set by the simulation when it makes each Person object.

        If person is chosen to be infected when the population is created, the simulation
        should instantiate a Virus object and set it as the value
        self.infection. Otherwise, self.infection should be set to None.
        '''
        self._id = _id  # int
        self.is_alive = True  # boolean
        self.is_vaccinated = is_vaccinated  # boolean
        self.infection = infection  # Virus object or None

    def did_survive_infection(self, virus):
        ''' Generate a random number and compare to virus's mortality_rate.
        If random number is smaller, person dies from the disease.
        If Person survives, they become vaccinated and they have no infection.
        Return a boolean value indicating whether they survived the infection.
        '''
        # Only called if infection attribute is not None.
        random_number = random.randint(0,100)/100
        if (random_number < virus.mortality_rate):
            self.is_alive = False 
            self.is_vaccinated = True 
            return False
        elif (random_number > virus.mortality_rate):
            self.is_alive = True 
            self.is_vaccinated = True 
            self.infection = None
            return True
        
''' These are simple tests to ensure that you are instantiating your Person class correctly. '''
def test_vacc_person_instantiation():
    # create some people to test if our init method works as expected
    person = Person(1, True)
    assert person._id == 1
    assert person.is_alive is True
    assert person.is_vaccinated is True
    assert person.infection is None


def test_not_vacc_person_instantiation():
    person = Person(2, False)
    assert person._id == 2
    assert person.is_alive is True
    assert person.is_vaccinated is False
    assert person.infection is None


def test_sick_person_instantiation():
    # Create a Virus object to give a Person object an infection
    virus = Virus("Dysentery", 0.7, 0.2)
    # Create a Person object and give them the virus infection
    person = Person(3, False, virus)
    assert person._id == 3
    assert person.is_alive is True
    assert person.is_vaccinated is False
    assert person.infection is virus


def test_did_survive_infection():
    virus = Virus("Dysentery", 0.7, 0.2)
    person = Person(4, False, virus)
    # Resolve whether the Person survives the infection or not
    survived = person.did_survive_infection(virus)
    if survived:
        assert person.is_alive is True
        assert person.is_vaccinated is True
        assert person.infection is None 
    else:
        assert person.is_alive is False
        assert person.is_vaccinated is True
        assert person.infection is virus 

# Per project completion requirement - 3 additional tests for person.py

def test_new_instance_is_virus_free():
    person = Person(4, False)
    assert person.infection == None

def test_infection_is_virus_object():
    virus = Virus("Dysentery", 0.7, 0.2)
    person = Person(4, False, virus)
    assert type(person.infection) == Virus

def test_person_attributes_type():
    virus = Virus("Dysentery", 0.7, 0.2)
    person = Person(1, True, virus)
    assert type(person._id) == int
    assert type(person.is_alive) == bool
    assert type(person.is_vaccinated) == bool
    assert type(person.infection) == Virus

if __name__ == "__main__":
    # run tests 
    test_vacc_person_instantiation()
    test_not_vacc_person_instantiation()
    test_sick_person_instantiation()
    test_did_survive_infection()
    test_new_instance_is_virus_free()
    test_person_attributes_type()
