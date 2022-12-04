import random, sys
random.seed(42)
from person import Person
from logger import Logger
from virus import Virus
from math import floor

class Simulation(object):
    ''' Main class that will run the herd immunity simulation program.
    Expects initialization parameters passed as command line arguments when file is run.

    Simulates the spread of a virus through a given population.  The percentage of the
    population that are vaccinated, the size of the population, and the amount of initially
    infected people in a population are all variables that can be set when the program is run.
    '''
    def __init__(self, pop_size, vacc_percentage, initial_infected=1, virus = None):
        ''' Logger object logger records all events during the simulation.
        Population represents all Persons in the population.
        The next_person_id is the next available id for all created Persons,
        and should have a unique _id value.
        The vaccination percentage represents the total percentage of population
        vaccinated at the start of the simulation.
        You will need to keep track of the number of people currently infected with the disease.
        The total infected people is the running total that have been infected since the
        simulation began, including the currently infected people who died.
        You will also need to keep track of the number of people that have die as a result
        of the infection.

        All arguments will be passed as command-line arguments when the file is run.
        HINT: Look in the if __name__ == "__main__" function at the bottom.
        '''
        self.pop_size = pop_size # Int
        self.next_person_id = 0 # Int
        self.virus = virus # Virus object
        self.initial_infected = initial_infected # Int
        self.total_infected =  initial_infected # Int - Previously 0 but changed to initial infected to account for all infected
        self.current_infected = 0 # Int
        self.vacc_percentage = vacc_percentage # float between 0 and 1
        self.total_dead = 0 # Int
        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(
            virus.name, pop_size, vacc_percentage, initial_infected)
        self.newly_infected = []
        self.logger = Logger(self.file_name)
        self.population = self._create_population(initial_infected) # List of Person objects
        #Stretch challenge - implementing stats gathering for the log_time_step() logger method
        self.new_death = 0

    def _create_population(self, initial_infected):
        '''This method will create the initial population.
            Args:
                initial_infected (int): The number of infected people that the simulation
                will begin with.

            Returns:
                list: A list of Person objects.
        '''
        #create population
        initial_population_arr = []
        for i in range (int(self.pop_size)):
            initial_population_arr.append(Person(i, False, None))

        # Create proportion of vaccinated persons
        vaccinated_people = self.pop_size * self.vacc_percentage
        for i in range(0, int(vaccinated_people)):
            initial_population_arr[i].is_vaccinated = True

        #create proportion of infected persons
        for i in range(floor(vaccinated_people), (floor(vaccinated_people) + floor(initial_infected))):
            initial_population_arr[i].infection = self.virus
                
        return initial_population_arr

    def _simulation_should_continue(self):
        ''' The simulation should only end if the entire population is dead
        or everyone is vaccinated.
            Returns:
                bool: True for simulation should continue, False if it should end.
        '''
        for person in self.population:
            if person.is_alive and not person.is_vaccinated and not person.infection:
                return True
        return False 

    def run(self):
        ''' This method should run the simulation until all requirements for ending
        the simulation are met.
        '''
        time_step_counter = 0
        should_continue = True

        while should_continue:
            self.time_step()
            time_step_counter += 1
            should_continue = self._simulation_should_continue()
            self.logger.log_time_step(time_step_counter, self.new_death, self.total_dead, self.current_infected, self.total_infected)
            self.new_death = 0

        print(f'The simulation has ended after {time_step_counter} turns.')
        for people in self.population:
            print(f'Person id {people._id} - Alive: {people.is_alive} Infected: {people.infection} Vaccinated: {people.is_vaccinated}.')

    def time_step(self):
        ''' This method should contain all the logic for computing one time step
        in the simulation.

        This includes:
            1. 100 total interactions with a randon person for each infected person
                in the population
            2. If the person is dead, grab another random person from the population.
                Since we don't interact with dead people, this does not count as an interaction.
            3. Otherwise call simulation.interaction(person, random_person) and
                increment interaction counter by 1.
            ''' 
        interaction_count = 0
        infected_group = []
        for person in self.population:
            if person.infection and person.is_alive:
                infected_group.append(person)

        while interaction_count < 100:
            for infected in infected_group:
                random_person = random.choice(self.population)
                if random_person.is_alive and interaction_count < 100:
                    interaction_count += 1
                    self.interaction(infected, random_person)
                else:
                    continue
        if interaction_count == 100:
            self._infect_newly_infected()
       
        

    def interaction(self, person, random_person):
        '''This method should be called any time two living people are selected for an
        interaction. It assumes that only living people are passed in as parameters.

        Args:
            person1 (person): The initial infected person
            random_person (person): The person that person1 interacts with.
        '''
        # Assert statements are included to make sure that only living people are passed
        # in as params
        assert person.is_alive == True
        assert random_person.is_alive == True
        #case where random_person is unvaccinated and uninfected
        if (not random_person.is_vaccinated and not random_person.infection):
                    survival = random_person.did_survive_infection(self.virus)
                    if(not survival):
                        # random number less than repro rate: they get infected and die
                        self.newly_infected.append(random_person._id)
                        self.logger.log_interaction(person, random_person, random_person_sick=False,
                        random_person_vacc=False, did_infect=True)
                        self.logger.log_infection_survival(random_person, did_die_from_infection = True)
                        self.new_death += 1
                        self.total_dead += 1
                    elif(survival):
                        # random number greater than repro rate: they survive!
                        self.logger.log_interaction(person, random_person, random_person_sick=False,
                        random_person_vacc=False, did_infect=True)
                        self.logger.log_infection_survival(random_person, did_die_from_infection = False) 
        #case where random person is vaccinated: no infection
        elif (random_person.is_vaccinated):
            self.logger.log_interaction(person, random_person, random_person_sick=False,
                        random_person_vacc=True, did_infect=False)
    

    def _infect_newly_infected(self):
        ''' This method should iterate through the list of ._id stored in self.newly_infected
        and update each Person object with the disease. '''
        self.current_infected = len(self.newly_infected)
        self.total_infected += self.current_infected

        for i in self.newly_infected:
            for people in self.population:
                if i == people._id:
                    people.infection = self.virus
        self.newly_infected.clear()


if __name__ == "__main__":

    params = sys.argv[1:]
    virus_name = str(params[0])
    repro_num = float(params[1])
    mortality_rate = float(params[2])

    pop_size = int(params[3])
    vacc_percentage = float(params[4])

    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1

    virus = Virus(virus_name, repro_num, mortality_rate)
    sim = Simulation(pop_size, vacc_percentage, initial_infected, virus)

    sim.run()

    # 🔊 ❗️  Run simulation by entering 'python3 simulation.py ebola 0.25 0.70 100000 0.90 10' in terminal, 
    # as opposed to 'python3 simulation.py 100000 0.90 Ebola 0.70 0.25 10' (as stated in repo) because the params order
    # in the code is not the same. 