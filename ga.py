
import numpy
import subprocess
import os
import pandas as pd  

opt2_flag = ["-fthread-jumps", 
          "-fcrossjumping", 
          "-foptimize-sibling-calls", 
          "-fcse-follow-jumps",  "-fcse-skip-blocks", 
          "-fgcse",  "-fgcse-lm",  
          "-fexpensive-optimizations", 
          "-fstrength-reduce", 
          "-frerun-cse-after-loop",  "-frerun-loop-opt", 
          "-fcaller-saves", 
          "-fpeephole2", 
          "-fschedule-insns",  "-fschedule-insns2", 
          "-fsched-interblock",  "-fsched-spec", 
          "-fregmove", 
          "-fstrict-aliasing", 
          "-fdelete-null-pointer-checks", 
          "-freorder-blocks",  "-freorder-functions", 
          "-funit-at-a-time", 
          "-falign-functions",  "-falign-jumps", 
          "-falign-loops",  "-falign-labels", 
          "-ftree-vrp", 
          "-ftree-pre"]
          
opt3_flag = ["-fgcse-after-reload", 
    "-fipa-cp-clone",
    "-floop-interchange",
    "-floop-unroll-and-jam", 
    "-fpeel-loops", 
    "-fpredictive-commoning", 
    "-fsplit-loops", 
    "-fsplit-paths", 
    "-ftree-loop-distribution", 
    "-ftree-loop-vectorize", 
    "-ftree-partial-pre", 
    "-ftree-slp-vectorize", 
    "-funswitch-loops", 
    "-fvect-cost-model"]
opt2_len = len(opt2_flag)
opt3_len = len(opt3_flag)
space_num = 20
exe_file_name = "test_ex"
benchmark_file_name = "simple.c"
execute_times = 5
dict = {'generation': [], 'space': [],'flags':[], 'time': []}    
df = pd.DataFrame(dict) 

def gen_spaces(num):
    spaces = []
    for j in range(0,space_num):
        space = numpy.random.randint(2, size=(num+1))
        spaces.append(space.tolist())
    return spaces

def get_time(str):
    str=str.strip()
    len_str = len(str)
    str = str[0:len_str-1]
    start = str.find(":")
    time = float(str[start+1:])
    return time

def gen_opt(spaces,opt_flags):
    time_result = 10000
    opt_space_id = -1
    time_repo = []
    flags_repo = []
    flags = ["gcc"]
    for space_id in range(0,len(spaces)):
        if spaces[space_id][0] == 1 :
            flags = ["gcc", "-O1"]
        else :
            flags = ["gcc"]
        for i in range(1, len(spaces[space_id])):
            if spaces[space_id][i] == 1:
                flags.append(opt_flags[i-1])
        flags.append("-o")
        flags.append(exe_file_name)
        flags.append(benchmark_file_name)
        subprocess.run(flags)
        total_time = 0
        for j in range(0, execute_times):
            os.system("echo>output")
            outfile = open("out", "w")
            subprocess.call(["/usr/bin/time", "-f'%E'","./test_ex"],stderr=outfile)
            f = open("out", "r")
            f.readline()
            t_str = f.readline()
            total_time = total_time + get_time(t_str)
        time = total_time/execute_times
        time_repo.append(time)
        flags_repo.append(flags)
        if time<time_result:
            opt_space_id = space_id
            time_result = time
    return (flags_repo, time_result, time_repo)

def cal_pop_fitness(spaces,opt_flags):
    # Calculating the fitness value of each solution in the current population.
    # The fitness function caulcuates the sum of products between each input and its corresponding weight.
    (flags,y,fitness) = gen_opt(spaces,opt_flags)
    return (flags,fitness)

def smallest_N_index(n,test_list):
    res = sorted(range(len(test_list)), key = lambda sub: test_list[sub])[:n] 
    return res

def select_mating_pool(pop, fitness, num_parents):
    # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
    parents_indexs = smallest_N_index(num_parents,fitness)
    parents = []
    for parent_num in range(num_parents):
        parents.append(pop[parents_indexs[parent_num]])
    return parents

def crossover(parents, offspring_size):
    offspring = []
    # The point at which crossover takes place between two parents. Usually it is at the center.
    crossover_point = numpy.uint8((len(parents[0])+1)/2)

    for k in range(offspring_size):
        # Index of the first parent to mate.
        parent1_idx = k%(len(parents))
        # Index of the second parent to mate.
        parent2_idx = (k+1)%(len(parents))
        # The new offspring will have its first half of its genes taken from the first parent.
        offspring_item = parents[parent1_idx][0:crossover_point] + parents[parent2_idx][crossover_point:]
        # The new offspring will have its second half of its genes taken from the second parent.
        offspring.append(offspring_item)
    return offspring

def mutation(offspring_crossover):
    # Mutation changes a single gene in each offspring randomly.
    for idx in range(len(offspring_crossover)):
        # The random value to be added to the gene.
        random_value = numpy.random.randint(2)
        offspring_crossover[idx][10] = random_value
    return offspring_crossover


sol_per_pop = 20
num_parents_mating = 10

# Defining the population size.
#pop_size = (sol_per_pop,num_weights) # The population will have sol_per_pop chromosome where each chromosome has num_weights genes.
#Creating the initial population.
spaces2 = gen_spaces(opt2_len)
spaces3 = gen_spaces(opt3_len)
spaces23 = gen_spaces(opt2_len+opt3_len-1)
opt_flgas_23 =opt2_flag+opt3_flag
num_generations = 10
new_population = spaces23
# Measing the fitness of each chromosome in the population.
(flags,fitness) = cal_pop_fitness(new_population, opt_flgas_23)

generation_ls = [0 for i in range(len(new_population))]
dict_new = {'generation': generation_ls, 'space': new_population,'flags': flags, 'time': fitness}    
df_new = pd.DataFrame(dict_new) 
df_new.sort_values(by=['time'], inplace=True, ascending=False)
small_id = smallest_N_index(1,fitness)
frames = [df,df_new]
df = pd.concat(frames)
print("Best result : ", min(fitness))

for generation in range(1, num_generations):
    print("Generation : ", generation)
    
    # Selecting the best parents in the population for mating.
    parents = select_mating_pool(new_population, fitness, num_parents_mating)

    # Generating next generation using crossover.
    offspring_crossover = crossover(parents,offspring_size=len(parents))

    # Adding some variations to the offsrping using mutation.
    offspring_mutation = mutation(offspring_crossover)

    # Creating the new population based on the parents and offspring.
    new_population = parents + offspring_mutation
    # Measing the fitness of each chromosome in the population.
    (flags,fitness) = cal_pop_fitness(new_population, opt_flgas_23)
    generation_ls = [generation for i in range(len(new_population))]
    dict_new = {'generation': generation_ls, 'space': new_population,'flags': flags, 'time': fitness}    
    df_new = pd.DataFrame(dict_new) 
    df_new.sort_values(by=['time'], inplace=True, ascending=False)
    frames = [df,df_new]
    df = pd.concat(frames)
    # The best result in the current iteration.
    print("Best result : ", min(fitness))
    

# Getting the best solution after iterating finishing all generations.
#At first, the fitness is calculated for each solution in the final generation.
(flags,fitness) = cal_pop_fitness(new_population, opt_flgas_23)
# Then return the index of that solution corresponding to the best fitness.
small_id = smallest_N_index(1,fitness)

print("Best solution : ", flags[small_id[0]])
print("Best solution fitness : ", min(fitness))
df.to_csv(r'dataframe.csv',index = False)
