from datetime import datetime


class Logger(object):
    ''' Utility class responsible for logging all interactions during the simulation. '''
    def __init__(self, file_name):
        self.file_name = file_name

    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate,
                       basic_repro_num, initial_infected):
        '''
        The simulation class should use this method immediately to log the specific
        parameters of the simulation as the first line of the file.
        '''
        outfile = open(self.file_name, "w")
        data = [
            {'population size' : pop_size},
            {'initial infected': initial_infected},
            {'Vaccinated percentage' : vacc_percentage},
            {'Virus name' : virus_name},
            {'Virus Mortality rate' : mortality_rate},
            {'Virus Repro rate' : basic_repro_num},
            {'date': datetime.now()}
        ]
        for item in data:
            for key, value in item.items():
                outfile.writelines(str(key) + ': ')   
                outfile.writelines(str(value) + '\n')

        outfile.close()
        return data
        

    def log_interaction(self, person, random_person, random_person_sick=None,
                        random_person_vacc=None, did_infect=None):
        '''
        The Simulation object should use this method to log every interaction
        a sick person has during each time step.

        The format of the log should be: "{person.ID} infects {random_person.ID} \n"

        or the other edge cases:
            "{person.ID} didn't infect {random_person.ID} because {'vaccinated' or 'already sick'}\n"
        '''
        outfile = open(self.file_name, "a")
        if (not random_person_sick and not random_person_vacc and did_infect):
            #outfile.writelines(f'{person._id} infects {random_person._id}\n')
            outfile.writelines("{} didn't infect {} because vaccinated\n".format(person._id, random_person._id))
        elif (not random_person_sick and random_person_vacc and not did_infect):
            outfile.writelines("{} didn't infect {} because vaccinated\n".format(person._id, random_person._id))
        
        outfile.close()

    def log_infection_survival(self, person, did_die_from_infection):
        ''' The Simulation object uses this method to log the results of every
        call of a Person object's .resolve_infection() method.

        The format of the log should be:
            "{person.ID} died from infection\n" or "{person.ID} survived infection.\n"
        '''
        outfile = open(self.file_name, "a")
        if(did_die_from_infection):
            outfile.write('{} died from infection\n'.format(person._id))
        elif(not did_die_from_infection):
            outfile.write("{} survived infection.\n".format(person._id))
        
        outfile.close()

    def log_time_step(self, time_step_number, new_death, total_dead, current_infected, total_infected, pop_size, total_vaccinated):
        ''' STRETCH CHALLENGE DETAILS:
        If you choose to extend this method, the format of the summary statistics logged
        are up to you.

        At minimum, it should contain:
            The number of people that were infected during this specific time step.
            The number of people that died on this specific time step.
            The total number of people infected in the population, including the newly infected
            The total number of dead, including those that died during this time step.

        The format of this log should be:
            "Time step {time_step_number} ended, beginning {time_step_number + 1}\n"
        '''
        outfile = open(self.file_name, "a")
        outfile.write(
        '''
            New infections (including infections resulting in deaths): {}\n 
            Total infection in population (including initialy infected, if applicable): {}\n
            New deaths: {}\n
            Total deaths: {}\n
            POPULATION STATS \n
            Number of living: {}\n
            Total number of vaccinated: {}**\n
            ** We opted not to test mortality of initially, per FAQ question-2 answer.)\n
            Time step {} ended, beginning {}...\n
        '''.format(current_infected, total_infected, new_death, total_dead, pop_size - total_dead, total_vaccinated, time_step_number, time_step_number + 1))
        outfile.close()

    #helper function to end log file:
    def log_simulation_end(self, initial_infected, time_step_number, total_dead, initial_vaccinated, total_infected, pop_size, total_vaccinated):
        '''This method is called to log end of simulation data.

        Args:
            person1 (person): The initial infected person
            random_person (person): The person that person1 interacts with.
        '''
        outfile = open(self.file_name, "a")
        outfile.write(
        '''
            ---------------------------------END OF SIMULATION---------------------------------
            Simulation ended because all members of the population (except for initialy infected**) are either vaccinated or dead\n 
            {} interactions happened in the simulation.
            RESULTS:\n
            Initial infected: {}\n
            Total deaths: {} \n
            Total living (incl. initial infected): {} \n
            Total persons that have been infected (excl. initialy infected): {} \n
            Total number of vaccinated and alive (incl. survivors and initially vaccinated): {}** \n
            Number of interactions resulting in vaccination and survival: {}\n
            Number of interactions resulting in death: {}\n
            ** We opted not to test mortality of initially, per FAQ question-2 answer.)\n
            ------------------------------------------------------------------------------------
        '''.format(time_step_number * 100, initial_infected, total_dead, pop_size - total_dead, total_infected, total_vaccinated, total_vaccinated - initial_vaccinated, total_dead))
        outfile.close()
