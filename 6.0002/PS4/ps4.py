# Problem Set 4: Simulating the Spread of Disease and Bacteria Population Dynamics
# Name:
# Collaborators (Discussion):
# Time:

import math
import numpy as np
import pylab as pl
import random


##########################
# End helper code
##########################

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleBacteria
    and ResistantBacteria classes to indicate that a bacteria cell does not
    reproduce. You should use NoChildException as is; you do not need to
    modify it or add any code.
    """


def make_one_curve_plot(x_coords, y_coords, x_label, y_label, title):
    """
    Makes a plot of the x coordinates and the y coordinates with the labels
    and title provided.

    Args:
        x_coords (list of floats): x coordinates to graph
        y_coords (list of floats): y coordinates to graph
        x_label (str): label for the x-axis
        y_label (str): label for the y-axis
        title (str): title for the graph
    """
    pl.figure()
    pl.plot(x_coords, y_coords)
    pl.xlabel(x_label)
    pl.ylabel(y_label)
    pl.title(title)
    pl.show()


def make_two_curve_plot(x_coords,
                        y_coords1,
                        y_coords2,
                        y_name1,
                        y_name2,
                        x_label,
                        y_label,
                        title):
    """
    Makes a plot with two curves on it, based on the x coordinates with each of
    the set of y coordinates provided.

    Args:
        x_coords (list of floats): the x coordinates to graph
        y_coords1 (list of floats): the first set of y coordinates to graph
        y_coords2 (list of floats): the second set of y-coordinates to graph
        y_name1 (str): name describing the first y-coordinates line
        y_name2 (str): name describing the second y-coordinates line
        x_label (str): label for the x-axis
        y_label (str): label for the y-axis
        title (str): the title of the graph
    """
    pl.figure()
    pl.plot(x_coords, y_coords1, label=y_name1)
    pl.plot(x_coords, y_coords2, label=y_name2)
    pl.legend()
    pl.xlabel(x_label)
    pl.ylabel(y_label)
    pl.title(title)
    pl.show()


##########################
# PROBLEM 1
##########################

class SimpleBacteria(object):
    """A simple bacteria cell with no antibiotic resistance"""

    def __init__(self, birth_prob, death_prob):
        """
        Args:
            birth_prob (float in [0, 1]): Maximum possible reproduction
                probability
            death_prob (float in [0, 1]): Maximum death probability
        """
        self.birth_prob = birth_prob
        self.death_prob = death_prob

    def is_killed(self):
        """
        Stochastically determines whether this bacteria cell is killed in
        the patient's body at a time step, i.e. the bacteria cell dies with
        some probability equal to the death probability each time step.

        Returns:
            bool: True with probability self.death_prob, False otherwise.
        """
        return random.random() < self.death_prob
            

    def reproduce(self, pop_density):
        """
        Stochastically determines whether this bacteria cell reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes.

        The bacteria cell reproduces with probability
        self.birth_prob * (1 - pop_density).

        If this bacteria cell reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleBacteria (which has the same
        birth_prob and death_prob values as its parent).

        Args:
            pop_density (float): The population density, defined as the
                current bacteria population divided by the maximum population

        Returns:
            SimpleBacteria: A new instance representing the offspring of
                this bacteria cell (if the bacteria reproduces). The child
                should have the same birth_prob and death_prob values as
                this bacteria.

        Raises:
            NoChildException if this bacteria cell does not reproduce.
        """
        if random.random() < self.birth_prob * (1 - pop_density):
            new_bacteria = SimpleBacteria(self.birth_prob, self.death_prob)
            return new_bacteria


class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any
    antibiotics and his/her bacteria populations have no antibiotic resistance.
    """
    def __init__(self, bacteria, max_pop):
        """
        Args:
            bacteria (list of SimpleBacteria): The bacteria in the population
            max_pop (int): Maximum possible bacteria population size for
                this patient
        """
        self.bacteria = bacteria
        self.max_pop = max_pop

    def get_total_pop(self):
        """
        Gets the size of the current total bacteria population.

        Returns:
            int: The total bacteria population
        """
        return len(self.bacteria)

    def update(self):
        """
        Update the state of the bacteria population in this patient for a
        single time step. update() should execute the following steps in
        this order:

        1. Determine whether each bacteria cell dies (according to the
           is_killed method) and create a new list of surviving bacteria cells.

        2. Calculate the current population density by dividing the surviving
           bacteria population by the maximum population. This population
           density value is used for the following steps until the next call
           to update()

        3. Based on the population density, determine whether each surviving
           bacteria cell should reproduce and add offspring bacteria cells to
           a list of bacteria in this patient. New offspring do not reproduce.

        4. Reassign the patient's bacteria list to be the list of surviving
           bacteria and new offspring bacteria

        Returns:
            int: The total bacteria population at the end of the update
        """
        remaining_bacteria = []
        for bac in self.bacteria:
            if not bac.is_killed():
                remaining_bacteria.append(bac)
                
        pop_density = len(remaining_bacteria) / self.max_pop
        total_bacteria = []
        for bac in remaining_bacteria:
            total_bacteria.append(bac)
            new_bac = bac.reproduce(pop_density)
            if new_bac != None:
                total_bacteria.append(new_bac)
        
        self.bacteria = total_bacteria
        
        return self.get_total_pop()


##########################
# PROBLEM 2
##########################

def calc_pop_avg(populations, n):
    """
    Finds the average bacteria population size across trials at time step n

    Args:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria in trial i at time step j

    Returns:
        float: The average bacteria population size at time step n
    """
    temp = 0
    for trial in populations:
        temp += trial[n]
    return temp / len(populations)


def simulation_without_antibiotic(num_bacteria,
                                  max_pop,
                                  birth_prob,
                                  death_prob,
                                  num_trials):
    """
    Run the simulation and plot the graph for problem 2. No antibiotics
    are used, and bacteria do not have any antibiotic resistance.

    For each of num_trials trials:
        * instantiate a list of SimpleBacteria
        * instantiate a Patient using the list of SimpleBacteria
        * simulate changes to the bacteria population for 300 timesteps,
          recording the bacteria population after each time step. Note
          that the first time step should contain the starting number of
          bacteria in the patient

    Then, plot the average bacteria population size (y-axis) as a function of
    elapsed time steps (x-axis) You might find the make_one_curve_plot
    function useful.

    Args:
        num_bacteria (int): number of SimpleBacteria to create for patient
        max_pop (int): maximum bacteria population for patient
        birth_prob (float in [0, 1]): maximum reproduction
            probability
        death_prob (float in [0, 1]): maximum death probability
        num_trials (int): number of simulation runs to execute

    Returns:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria in trial i at time step j
    """
    populations = []
    for trial in range(num_trials):
        bacteria = []
        for bac in range(num_bacteria):
            new_bac = SimpleBacteria(birth_prob, death_prob)
            bacteria.append(new_bac)
        patient = Patient(bacteria, max_pop)
        population = []
        for step in range(300):
            pop = patient.update()
            population.append(pop)
        populations.append(population)
    
    x_coords = []
    y_coords = []
    for x in range(300):
        y = calc_pop_avg(populations, x) 
        x_coords.append(x)
        y_coords.append(y)
    x_label = 'Timestep'
    y_label = 'Average population'
    title = 'Without Antibiotic'
    make_one_curve_plot(x_coords, y_coords, x_label, y_label, title)


# When you are ready to run the simulation, uncomment the next line
# populations = simulation_without_antibiotic(100, 1000, 0.1, 0.025, 50)



##########################
# PROBLEM 3
##########################

def calc_pop_std(populations, t):
    """
    Finds the standard deviation of populations across different trials
    at time step t by:
        * calculating the average population at time step t
        * compute average squared distance of the data points from the average
          and take its square root

    You may not use third-party functions that calculate standard deviation,
    such as numpy.std. Other built-in or third-party functions that do not
    calculate standard deviation may be used.

    Args:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria present in trial i at time step j
        t (int): time step

    Returns:
        float: the standard deviation of populations across different trials at
             a specific time step
    """
    mean = calc_pop_avg(populations, t)
    deltasquares = 0 # not sure if this is a great name lol
    for trial in populations:
        # for each entry, find the difference between the entry and the mean,
        # and square that
        deltasquares += (trial[t] - mean) ** 2
    # take the sum of all the squared differences and divide by the number
    # of entries to get the variance
    variance = deltasquares / len(populations)
    # standard deviation is the square root of variance
    return variance ** 0.5


def calc_95_ci(populations, t):
    """
    Finds a 95% confidence interval around the average bacteria population
    at time t by:
        * computing the mean and standard deviation of the sample
        * using the standard deviation of the sample to estimate the
          standard error of the mean (SEM)
        * using the SEM to construct confidence intervals around the
          sample mean

    Args:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria present in trial i at time step j
        t (int): time step

    Returns:
        mean (float): the sample mean
        width (float): 1.96 * SEM

        I.e., you should return a tuple containing (mean, width)
    """
    mean = calc_pop_avg(populations, t)
    std_dev = calc_pop_std(populations, t)
    std_err = std_dev / len(populations) ** 0.5
    width = std_err * 1.96
    return mean, width



##########################
# PROBLEM 4
##########################

class ResistantBacteria(SimpleBacteria):
    """A bacteria cell that can have antibiotic resistance."""

    def __init__(self, birth_prob, death_prob, resistant, mut_prob):
        """
        Args:
            birth_prob (float in [0, 1]): reproduction probability
            death_prob (float in [0, 1]): death probability
            resistant (bool): whether this bacteria has antibiotic resistance
            mut_prob (float): mutation probability for this
                bacteria cell. This is the maximum probability of the
                offspring acquiring antibiotic resistance
        """
        super().__init__(birth_prob, death_prob)
        self.resistant = resistant
        self.mut_prob = mut_prob

    def get_resistant(self):
        """Returns whether the bacteria has antibiotic resistance"""
        return self.resistant

    def is_killed(self):
        """Stochastically determines whether this bacteria cell is killed in
        the patient's body at a given time step.

        Checks whether the bacteria has antibiotic resistance. If resistant,
        the bacteria dies with the regular death probability. If not resistant,
        the bacteria dies with the regular death probability / 4.

        Returns:
            bool: True if the bacteria dies with the appropriate probability
                and False otherwise.
        """
        if self.get_resistant():
            return random.random() < self.death_prob
        else:
            return random.random() < self.death_prob / 4

    def reproduce(self, pop_density):
        """
        Stochastically determines whether this bacteria cell reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A surviving bacteria cell will reproduce with probability:
        self.birth_prob * (1 - pop_density).

        If the bacteria cell reproduces, then reproduce() creates and returns
        an instance of the offspring ResistantBacteria, which will have the
        same birth_prob, death_prob, and mut_prob values as its parent.

        If the bacteria has antibiotic resistance, the offspring will also be
        resistant. If the bacteria does not have antibiotic resistance, its
        offspring have a probability of self.mut_prob * (1-pop_density) of
        developing that resistance trait. That is, bacteria in less densely
        populated environments have a greater chance of mutating to have
        antibiotic resistance.

        Args:
            pop_density (float): the population density

        Returns:
            ResistantBacteria: an instance representing the offspring of
            this bacteria cell (if the bacteria reproduces). The child should
            have the same birth_prob, death_prob values and mut_prob
            as this bacteria. Otherwise, raises a NoChildException if this
            bacteria cell does not reproduce.
        """
        if self.resistant:
            if random.random() < self.birth_prob * (1 - pop_density):
                new_bacteria = ResistantBacteria(self.birth_prob, self.death_prob,
                                                 self.resistant, self.mut_prob)
                return new_bacteria
        else:
            if random.random() < self.birth_prob * (1 - pop_density):
                mutate = random.random() < self.mut_prob * (1 - pop_density)
                new_bacteria = ResistantBacteria(self.birth_prob, self.death_prob,
                                              mutate, self.mut_prob)
                return new_bacteria
            


class TreatedPatient(Patient):
    """
    Representation of a treated patient. The patient is able to take an
    antibiotic and his/her bacteria population can acquire antibiotic
    resistance. The patient cannot go off an antibiotic once on it.
    """
    def __init__(self, bacteria, max_pop):
        """
        Args:
            bacteria: The list representing the bacteria population (a list of
                      bacteria instances)
            max_pop: The maximum bacteria population for this patient (int)

        This function should initialize self.on_antibiotic, which represents
        whether a patient has been given an antibiotic. Initially, the
        patient has not been given an antibiotic.

        Don't forget to call Patient's __init__ method at the start of this
        method.
        """
        super().__init__(bacteria, max_pop)
        self.on_antibiotic = False

    def set_on_antibiotic(self):
        """
        Administer an antibiotic to this patient. The antibiotic acts on the
        bacteria population for all subsequent time steps.
        """
        self.on_antibiotic = True

    def get_resist_pop(self):
        """
        Get the population size of bacteria cells with antibiotic resistance

        Returns:
            int: the number of bacteria with antibiotic resistance
        """
        resistant = 0
        for bac in self.bacteria:
            if bac.get_resistant():
                resistant += 1
        return resistant

    def update(self):
        """
        Update the state of the bacteria population in this patient for a
        single time step. update() should execute these actions in order:

        1. Determine whether each bacteria cell dies (according to the
           is_killed method) and create a new list of surviving bacteria cells.

        2. If the patient is on antibiotics, the surviving bacteria cells from
           (1) only survive further if they are resistant. If the patient is
           not on the antibiotic, keep all surviving bacteria cells from (1)

        3. Calculate the current population density. This value is used until
           the next call to update(). Use the same calculation as in Patient

        4. Based on this value of population density, determine whether each
           surviving bacteria cell should reproduce and add offspring bacteria
           cells to the list of bacteria in this patient.

        5. Reassign the patient's bacteria list to be the list of survived
           bacteria and new offspring bacteria

        Returns:
            int: The total bacteria population at the end of the update
        """
        remaining_bacteria = []
        for bac in self.bacteria:
            if not bac.is_killed():
                remaining_bacteria.append(bac)
                
        if self.on_antibiotic:
            # for bac in remaining_bacteria:
            #     if not bac.get_resistant():
            #         remaining_bacteria.remove(bac)
                    # print('removing bacteria')
            resistant_bacteria = []
            for bac in remaining_bacteria:
                if bac.get_resistant():
                    resistant_bacteria.append(bac)
            remaining_bacteria = resistant_bacteria
        
        pop_density = len(remaining_bacteria) / self.max_pop
        total_bacteria = []
        for bac in remaining_bacteria:
            total_bacteria.append(bac)
            new_bac = bac.reproduce(pop_density)
            if new_bac != None:
                total_bacteria.append(new_bac)
        
        self.bacteria = total_bacteria
        
        return self.get_total_pop()


##########################
# PROBLEM 5
##########################

def simulation_with_antibiotic(num_bacteria,
                               max_pop,
                               birth_prob,
                               death_prob,
                               resistant,
                               mut_prob,
                               num_trials):
    """
    Runs simulations and plots graphs for problem 4.

    For each of num_trials trials:
        * instantiate a list of ResistantBacteria
        * instantiate a patient
        * run a simulation for 150 timesteps, add the antibiotic, and run the
          simulation for an additional 250 timesteps, recording the total
          bacteria population and the resistance bacteria population after
          each time step

    Plot the average bacteria population size for both the total bacteria
    population and the antibiotic-resistant bacteria population (y-axis) as a
    function of elapsed time steps (x-axis) on the same plot. You might find
    the helper function make_two_curve_plot helpful

    Args:
        num_bacteria (int): number of ResistantBacteria to create for
            the patient
        max_pop (int): maximum bacteria population for patient
        birth_prob (float int [0-1]): reproduction probability
        death_prob (float in [0, 1]): probability of a bacteria cell dying
        resistant (bool): whether the bacteria initially have
            antibiotic resistance
        mut_prob (float in [0, 1]): mutation probability for the
            ResistantBacteria cells
        num_trials (int): number of simulation runs to execute

    Returns: a tuple of two lists of lists, or two 2D arrays
        populations (list of lists or 2D array): the total number of bacteria
            at each time step for each trial; total_population[i][j] is the
            total population for trial i at time step j
        resistant_pop (list of lists or 2D array): the total number of
            resistant bacteria at each time step for each trial;
            resistant_pop[i][j] is the number of resistant bacteria for
            trial i at time step j
    """
    populations = []
    res_pops = []
    for trial in range(num_trials):
        bacteria = []
        for bac in range(num_bacteria):
            new_bac = ResistantBacteria(birth_prob, death_prob, resistant,
                                        mut_prob)
            bacteria.append(new_bac)
        patient = TreatedPatient(bacteria, max_pop)
        population = []
        res_pop = []
        # patient not on antibiotics for first half of each trial 
        for step in range(150):
            pop = patient.update()
            res = patient.get_resist_pop()
            population.append(pop)
            res_pop.append(res)
            # print(trial,step,pop,res)
        # patient put on antibiotics for last half of each trial
        patient.set_on_antibiotic()
        for step in range(150):
            pop = patient.update()
            res = patient.get_resist_pop()
            # print(trial,step,pop,res)
            population.append(pop)
            res_pop.append(res)
        populations.append(population)
        res_pops.append(res_pop)
    
    x_coords = []
    y_coords = []
    y_res_coords = []   
    for x in range(300):
        y = calc_pop_avg(populations, x)
        y_res = calc_pop_avg(res_pops, x)
        x_coords.append(x)
        y_coords.append(y)
        y_res_coords.append(y_res)      
    x_label = 'Timestep'
    y_label = 'Average population'
    y_name_1 = 'Total'
    y_name_2 = 'Resistant'
    title = 'With an Antibiotic'
    make_two_curve_plot(x_coords, y_coords, y_res_coords,
                        y_name_1, y_name_2, x_label, y_label, title)
    return populations, res_pops


# When you are ready to run the simulations, uncomment the next lines one
# at a time
# total_pop, resistant_pop = simulation_with_antibiotic(num_bacteria=100,
#                                                       max_pop=1000,
#                                                       birth_prob=0.3,
#                                                       death_prob=0.2,
#                                                       resistant=False,
#                                                       mut_prob=0.8,
#                                                       num_trials=50)

# mean, width = calc_95_ci(total_pop, 299)
# mean_res, width_res = calc_95_ci(resistant_pop, 299)
# print('Mean total population at step 299:', mean, 
#       'with 95% confidence interval of', width)
# print('Mean resistant population at step 299:', mean_res, 
#       'with 95% confidence interval of', width_res)

total_pop, resistant_pop = simulation_with_antibiotic(num_bacteria=100,
                                                      max_pop=1000,
                                                      birth_prob=0.17,
                                                      death_prob=0.2,
                                                      resistant=False,
                                                      mut_prob=0.8,
                                                      num_trials=50)

mean, width = calc_95_ci(total_pop, 299)
mean_res, width_res = calc_95_ci(resistant_pop, 299)
print('Mean total population at step 299:', mean, 
      'with 95% confidence interval of', width)
print('Mean resistant population at step 299:', mean_res, 
      'with 95% confidence interval of', width_res)


# Trends of Simulation A and Simulation B
# 1. What happens to the total population before introducing the antibiotic?

#   A: increases logarithmically
#   B: increases at first, then decays as death rate outpaces growth rate


# 2. What happens to the resistant bacteria population before introducing the antibiotic?

#   A: increases at first, then drops off as population density increases
#       (reducing chances of mutation) and non-resistant bacteria outlive 
#       resistant bacteria
#   B: follows the same growth-then-decay as the total population of B, but
#       resistant population drops off more slowly than the total population 
#       since the lowering population density increases the chances of mutation
#       so resistant bacteria make up a larger portion of total


# 3. What happens to the total population after introducing the antibiotic?

#   A: Drops immediately so that only remaining bacteria are the resistant
#       population, then slowly rises to a much lower stable level
#   B: drops immediately so only resistant bacteria remain, then quickly
#       decays to zero

#
# 4. What happens to the resistant bacteria population after introducing the antibiotic?

#   A: resistant bacteria population is not effected. the resistant bacteria
#       begins to grow again but more slowly (bc of higher death rate)
#       than non-resistant bacteria. it levels out at a lower steady population
#       level than the original population
#   B: the resistant bacteria population is not directly affecteed by the 
#       antibiotic, but since it dies so much quicker than the non-resistant
#       bacteria its population quickly drops to zero. it had only maintained
#       a population because of mutations from the non-resistant bacteria