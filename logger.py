from datetime import datetime


class Logger(object):
    ''' Utility class responsible for logging all interactions during the simulation. '''
    # TODO: Write a test suite for this class to make sure each method is working
    # as expected.

    # PROTIP: Write your tests before you solve each function, that way you can
    # test them one by one as you write your class.

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
        

    def log_interaction(self, person, random_person, random_person_sick=None,
                        random_person_vacc=None, did_infect=None):
        '''
        The Simulation object should use this method to log every interaction
        a sick person has during each time step.

        The format of the log should be: "{person.ID} infects {random_person.ID} \n"

        or the other edge cases:
            "{person.ID} didn't infect {random_person.ID} because {'vaccinated' or 'already sick'} \n"
        '''
        outfile = open(self.file_name, "a")
        if (not random_person_sick and not random_person_vacc and did_infect):
            outfile.writelines(f"{person._id} infects {random_person._id} \n")
        elif (not random_person_sick and random_person_vacc and not did_infect):
            outfile.writelines(f"{person._id} didn't infect {random_person._id} because vaccinated \n")
        #log other edge cases that might have been missed
        else:
            outfile.write(f"Edge case uncaught: random person id {random_person._id}, sick? {random_person_sick} vacc? {random_person_vacc} infect? {did_infect} \n")
        
        outfile.close()

    def log_infection_survival(self, person, did_die_from_infection):
        ''' The Simulation object uses this method to log the results of every
        call of a Person object's .resolve_infection() method.

        The format of the log should be:
            "{person.ID} died from infection\n" or "{person.ID} survived infection.\n"
        '''
        outfile = open(self.file_name, "a")
        if(did_die_from_infection):
            outfile.write(f"{person._id} died from infection\n")
        elif(not did_die_from_infection):
            outfile.write(f"{person._id} survived infection.\n")
        
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
        f'''
            New infections (including infections resulting in deaths): {current_infected} \n 
            Total infection in population (including initialy infected, if applicable): {total_infected} \n
            New deaths: {new_death} \n
            Total deaths: {total_dead} \n
            POPULATION STATS \n
            Number of living: {pop_size - total_dead}\n
            Total number of vaccinated: {total_vaccinated}** \n
            ** We opted not to test mortality of initially, per FAQ question-2 answer.)\n
            Time step {time_step_number} ended, beginning {time_step_number + 1}... \n
        '''
            )
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
        f'''
            ---------------------------------END OF SIMULATION---------------------------------
            Simulation ended because all members of the population (except for initialy infected**) are either vaccinated or dead\n 
            {time_step_number * 100} interactions happened in the simulation.
            RESULTS:\n
            Initial infected: {initial_infected}\n
            Total deaths: {total_dead} \n
            Total living (incl. initial infected): {pop_size - total_dead} \n
            Total persons that have been infected (excl. initialy infected): {total_infected} \n
            Total number of vaccinated and alive (incl. survivors and initially vaccinated): {total_vaccinated}** \n
            Number of interactions resulting in vaccination and survival: {total_vaccinated - initial_vaccinated}\n
            Number of interactions resulting in death: {total_dead}\n
            ** We opted not to test mortality of initially, per FAQ question-2 answer.)\n
            ------------------------------------------------------------------------------------
        '''
            )
        outfile.close()

if __name__ == "__main__":
    #Use for testing      
    log_test = Logger('example.txt')
    log_test.write_metadata(1000, 0.20, 'Ebola', 0.2, 0.3, 10)