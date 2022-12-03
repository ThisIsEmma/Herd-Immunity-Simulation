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
        # TODO: Create a Logger object and bind it to self.logger.
        # Remember to call the appropriate logger method in the corresponding parts of the simulation.
        # TODO: Call self._create_population() and pass in the correct parameters.
        # Store the array that this method will return in the self.population attribute.
        # TODO: Store each newly infected person's ID in newly_infected attribute.
        # At the end of each time step, call self._infect_newly_infected()
        # and then reset .newly_infected back to an empty list.
        
        
        self.pop_size = pop_size # Int
        self.next_person_id = 0 # Int
        self.virus = virus # Virus object
        self.initial_infected = initial_infected # Int
        self.total_infected = 0 # Int
        self.current_infected = 0 # Int
        self.vacc_percentage = vacc_percentage # float between 0 and 1
        self.total_dead = 0 # Int
        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(
            virus.name, pop_size, vacc_percentage, initial_infected)
        self.newly_infected = []
        self.logger = Logger(self.file_name)
        self.population = self._create_population(initial_infected) # List of Person objects

    def _create_population(self, initial_infected):
        '''This method will create the initial population.
            Args:
                initial_infected (int): The number of infected people that the simulation
                will begin with.

            Returns:
                list: A list of Person objects.

        '''
        # TODO: Finish this method!  This method should be called when the simulation
        # begins, to create the population that will be used. This method should return
        # an array filled with Person objects that matches the specifications of the
        # simulation (correct number of people in the population, correct percentage of
        # people vaccinated, correct number of initially infected people).

        # Use the attributes created in the init method to create a population that has
        # the correct intial vaccination percentage and initial infected.

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
        # TODO: Complete this helper method.  Returns a Boolean.
        for person in self.population:
            if person.is_alive and not person.is_vaccinated and not person.infection:
                return True
        return False 

    def run(self):
        ''' This method should run the simulation until all requirements for ending
        the simulation are met.
        '''
        # TODO: Finish this method.  To simplify the logic here, use the helper method
        # _simulation_should_continue() to tell us whether or not we should continue
        # the simulation and run at least 1 more time_step.

        # TODO: Keep track of the number of time steps that have passed.
        # HINT: You may want to call the logger's log_time_step() method at the end of each time step.
        # TODO: Set this variable using a helper
        time_step_counter = 0
        should_continue = True

        while should_continue:
        # TODO: for every iteration of this loop, call self.time_step() to compute another
        # round of this simulation.
            self.time_step()
            time_step_counter += 1
            print(f'The simulation has ended after {time_step_counter} turns.')
            should_continue = self._simulation_should_continue()

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
        
        print('these are the infected: ',infected_group)

        while interaction_count < 100:
            for infected in infected_group:
                for uninfected in self.population:
                    if uninfected.is_alive and interaction_count < 100:
                        interaction_count += 1
                        self.interaction(infected, uninfected)
                    else:
                        continue
        print('interaction count: ', interaction_count)
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

        # TODO: Finish this method.
        #  The possible cases you'll need to cover are listed below:
            # random_person is vaccinated:
            #     nothing happens to random person.
            # random_person is already infected:
            #     nothing happens to random person.
            # random_person is healthy, but unvaccinated:
            #     generate a random number between 0 and 1.  If that number is smaller
            #     than repro_rate, random_person's ID should be appended to
            #     Simulation object's newly_infected array, so that their .infected
            #     attribute can be changed to True at the end of the time step.
        # TODO: Call slogger method during this method.

        #case where random_person is unvaccinated and uninfected
        print('start interaction')
        if (not random_person.is_vaccinated and not random_person.infection):
                    survival = random_person.did_survive_infection(self.virus)
                    print('survival => ', survival)
                    if(not survival):
                        # random number less than repro rate: they get infected and die
                        self.newly_infected.append(random_person._id)
                        self.logger.log_interaction(person, random_person, random_person_sick=False,
                        random_person_vacc=False, did_infect=True)
                        self.logger.log_infection_survival(random_person, did_die_from_infection = True)
                        print('log death')
                    elif(survival):
                        # random number greater than repro rate: they survive!
                        self.logger.log_interaction(person, random_person, random_person_sick=False,
                        random_person_vacc=False, did_infect=True)
                        self.logger.log_infection_survival(random_person, did_die_from_infection = False) 
                        print('log survival')
        #case where random person is vaccinated: no infection
        elif (random_person.is_vaccinated):
            print('log uninfection - scenario 2')
            self.logger.log_interaction(person, random_person, random_person_sick=False,
                        random_person_vacc=True, did_infect=False)
        '''
              #case where random person is already sick (unvaccinated and infected): log interaction but no re-infection
        elif (not random_person.is_vaccinated and random_person.infection):
            self.logger.log_interaction(person, random_person, random_person_sick=True, random_person_vacc=False, did_infect=False)
            print('log uninfection - scenario 1')

        '''

    def _infect_newly_infected(self):
        ''' This method should iterate through the list of ._id stored in self.newly_infected
        and update each Person object with the disease. '''
        # TODO: Call this method at the end of every time step and infect each Person.
        # TODO: Once you have iterated through the entire list of self.newly_infected, remember
        # to reset self.newly_infected back to an empty list.
        print('started infect_newly_infected')
        for i in self.newly_infected:
            print('print i => ',i)
            for people in self.population:
                if i == people._id:
                    people.infection = self.virus
                    print('virus added to', people._id)
                    print(f'person {i} viral status: ',people.infection)
        print('finished infect_newly_infected')
        for people in self.population:
            print('just added, is now vaccinated ', people.is_vaccinated)
        self.newly_infected.clear()


if __name__ == "__main__":
    '''
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
'''

# TO BE DELETED ! - My own test
ebola = Virus('ebola virus',0.6, 0.90)
trial = Simulation(150,0.10,1,virus = ebola)
print('should sim continue? ', trial._simulation_should_continue())
trial.run()

'''
print('see vaccinated: ')
for people in population:
    print(people.is_vaccinated)
print('see infected: ')


for people in population:
    if people.infection:
        print(people.infection.name)
    else:
        print(people.infection)


print('is alive?')

for people in population:
    print(f'{people._id} + {people.is_alive}')

print('infection?')
for people in population:
    print(f'{people._id} + {people.infection}')

trial.interaction(trial.population[2], trial.population[2])

print('AFTER SIM -is alive?')
for people in population:
    print(f'{people._id} + {people.is_alive}')

print('newly infected: ', trial.newly_infected)
trial._infect_newly_infected()

print('AFTER SIM - infection?')
for people in population:
    print(f'infection? {people._id} + {people.infection}')

if(population[2].infection):
    print('the guy is infected')
    
'''






