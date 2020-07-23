import os
import subprocess
import numpy as np

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

def gen_spaces(num):
    spaces = []
    for j in range(0,space_num):
        space = np.random.randint(2, size=num)
        spaces.append(space)
    return spaces

def get_time(str):
    str=str.strip()
    len_str = len(str)
    str = str[0:len_str-1]
    start = str.find(":")
    time = float(str[start+1:])
    return time

spaces2 = gen_spaces(opt2_len)
spaces3 = gen_spaces(opt3_len)
""" generate opt """
def gen_opt(spaces,opt_flags):
    time_result = 10000
    opt_space_id = -1
    time_repo = []
    for space_id in range(0,len(spaces)):
        flags = ["gcc", "-O1"]
        for i in range(0, len(spaces[space_id])):
            if spaces[space_id][i] == 1:
                flags.append(opt_flags[i])
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
        if time<time_result:
            opt_space_id = space_id
            time_result = time
    return (opt_space_id, time_result, time_repo)

print("-------------------------")

print("####### only -O2 #######")
space_id, time_result, time_repo = gen_opt(spaces2, opt2_flag)
opt_flags = []
for i in range(0, opt2_len):
    if spaces2[space_id][i] == 1:
        opt_flags.append(opt2_flag[i])
print("\n# min-time flags")
print(*opt_flags) 
print("\n# min-time")
print(time_result)
print("\n# random flags time repo")
print (["{0:0.4f}".format(i) for i in time_repo])
print("\n# opt spaces")
print (*spaces2)

print("-------------------------")

print("####### only -O3 #######")
space_id, time_result, time_repo = gen_opt(spaces3, opt3_flag)
opt_flags = []
for i in range(0, opt3_len):
    if spaces3[space_id][i] == 1:
        opt_flags.append(opt3_flag[i])
print("\n# min-time flags")
print(*opt_flags) 
print("\n# min-time")
print(time_result)
print("\n# random flags time repo")
print (["{0:0.4f}".format(i) for i in time_repo])
print("\n# opt spaces")
print (*spaces2)

print("-------------------------")

print("####### -O2 -O3 #######")
spaces23= spaces2+spaces3
opt23_flags = opt2_flag+opt3_flag
space_id, time_result, time_repo = gen_opt(spaces23, opt23_flags)
opt_flags_2 = []
for i in range(0, opt2_len):
    if spaces2[space_id][i] == 1:
        opt_flags_2.append(opt2_flag[i])
opt_flags_3 = []
for i in range(0, opt3_len):
    if spaces3[space_id][i] == 1:
        opt_flags_3.append(opt3_flag[i])
print("\n# min-time flags -O2")
print(*opt_flags_2) 
print("# min-time flags -O3")
print(*opt_flags_3) 
print("\n# min-time")
print(time_result)
print("\n# random flags time repo")
print (["{0:0.4f}".format(i) for i in time_repo])
print("\n# opt spaces -O2")
print (*spaces2)
print("# opt spaces -O3")
print (*spaces3)
