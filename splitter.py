import os
import shutil
import sys
import subprocess
import time

# change path accordingly to your location
# don´t forget to add double-backslash for subdirs, as shown below
# todo: integrate simc into autosimc-folderstructure?
simc_path = 'd:\\downloads\\simc-720-03-win64\\simc.exe'

subdir1 = "temp_step1"
subdir2 = "temp_step2"
subdir3 = "temp_step3"


# deletes and creates needed folders
# sometimes it generates a permission error; don´t know why (am i removing and recreating too fast?)
def purge_subfolder(subfolder):
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    else:
        shutil.rmtree(subfolder)
        os.makedirs(subfolder)


# splits generated permutation-file into n pieces
# calculations are therefore done much more memory-efficient; simcraft usually crashes the system if too many profiles
# have to be simulated at once
# inputfile: the output of main.py with all permutations in a big file
# size: after n profiles a new file will be created, incrementally numbered
#       50 seems to be a good number for this, it takes around 10-20s each, depending on simulation-parameters
def split(inputfile, size=50):
    if size <= 0:
        print("Size: " + str(size) + " is below 0")
    if os.path.isfile(inputfile):
        source = open(inputfile, "r")
        # create subfolder for first step, the splitting into n pieces
        # if exists, delete and recreate
        subfolder = os.path.join(os.getcwd(), subdir1)
        purge_subfolder(subfolder)

        output_file_number = 0
        profile_max = size
        profile_count = 0

        tempOutput = "";
        empty = True

        # true if weapon was detected so a profile-block can be closed
        # working with strings is fun!
        weapon_reached = False

        for line in source.readlines():
            if line != "\n":
                tempOutput += line

            if line.startswith("main_hand"):
                weapon_reached = True

            if line == "\n" and weapon_reached:
                profile_count += 1
                empty = False
                weapon_reached = False
                tempOutput += "\n"

            if profile_count >= profile_max:
                file = open(os.path.join(subfolder, "sim" + str(output_file_number) + ".sim"), "w")
                file.write(tempOutput)
                file.close()
                tempOutput = ""
                output_file_number += 1
                profile_count = 0
                empty = True
                weapon_reached = False

        # finish remaining profiles
        if not empty:
            file = open(os.path.join(subfolder, "sim" + str(output_file_number) + ".sim"), "w")
            file.write(tempOutput)
            file.close()
    else:
        print("Inputfile: " + str(inputfile) + " does not exist")
        sys.exit(1)


# Calls simcraft to simulate all .sim-files in a subdir
# iterations: can be specifically changed to finetune a stage; standard is 10000
# todo: command: calls a specific command-line for simcraft, e.g. one for patchwerk, for aoe etc.
def sim(subdir, iterations=10000, command=1):
    starttime = time.time()

    # some minor progress-bar-initialization
    amount_of_generated_splits = 0
    for root, dirs, files in os.walk(os.path.join(os.getcwd(), subdir)):
        for file in files:
            if file.endswith(".sim"):
                amount_of_generated_splits += 1

    files_processed = 0
    for root, dirs, files in os.walk(os.path.join(os.getcwd(), subdir)):
        for file in files:
            if file.endswith(".sim"):
                name = file[0:file.find(".")]
                if command == 1:
                    cmd = [simc_path, os.path.join(os.getcwd(), subdir, file),
                           'output=' + os.path.join(os.getcwd(), subdir, name) + '.result',
                           'iterations=' + str(iterations),
                           'process_priority=low', 'single_actor_batch=1']
                if command == 2:
                    cmd = [simc_path, os.path.join(os.getcwd(), subdir, file),
                           'html=' + os.path.join(os.getcwd(), subdir, name) + '.html',
                           'iterations=' + str(iterations), 'calculate_scale_factors=1',
                           'process_priority=low', 'single_actor_batch=1']
                print(cmd)
                print("-----------------------------------------------------------------")
                print("Automated Simulation within AutoSimC.")
                print("Currently processing: " + str(name))
                print("Processed: " + str(files_processed) + "/" + str(amount_of_generated_splits) + " (" + str(
                    round(100 * float(int(files_processed) / int(amount_of_generated_splits)), 1)) + "%)")
                if files_processed > 0:
                    duration = time.time() - starttime
                    avg_calctime_hist = duration / files_processed
                    remaining_time = (amount_of_generated_splits - files_processed) * avg_calctime_hist
                    print("Remaining calculation time (est.): " + str(round(remaining_time,0)) + " seconds")
                    print("Finish time for Step 1(est.): " + time.asctime(time.localtime(time.time() + remaining_time)))
                    print("Step 1 is the most time consuming, Step 2 and 3 will take ~5-20 minutes combined")
                print("-----------------------------------------------------------------")
                subprocess.call(cmd)
                files_processed += 1


# Calls simcraft to simulate all .sim-files in a subdir
# todo: command: calls a specific command-line for simcraft, e.g. one for patchwerk, for aoe etc.
def sim_targeterror(subdir, targeterror=1, command=1):
    starttime = time.time()

    # some minor progress-bar-initialization
    amount_of_generated_splits = 0
    for root, dirs, files in os.walk(os.path.join(os.getcwd(), subdir)):
        for file in files:
            if file.endswith(".sim"):
                amount_of_generated_splits += 1

    files_processed = 0
    for root, dirs, files in os.walk(os.path.join(os.getcwd(), subdir)):
        for file in files:
            if file.endswith(".sim"):
                name = file[0:file.find(".")]
                if command == 1:
                    cmd = [simc_path, os.path.join(os.getcwd(), subdir, file),
                           'output=' + os.path.join(os.getcwd(), subdir, name) + '.result',
                           'target_error=' + str(targeterror),
                           'process_priority=low', 'single_actor_batch=1']
                if command == 2:
                    cmd = [simc_path, os.path.join(os.getcwd(), subdir, file),
                           'html=' + os.path.join(os.getcwd(), subdir, name) + '.html',
                           'target_error=' + str(targeterror), 'calculate_scale_factors=1',
                           'process_priority=low', 'single_actor_batch=1']
                print(cmd)
                print("-----------------------------------------------------------------")
                print("Automated Simulation within AutoSimC.")
                print("Currently processing: " + str(name))
                print("Processed: " + str(files_processed) + "/" + str(amount_of_generated_splits) + " (" + str(
                    round(100 * float(int(files_processed) / int(amount_of_generated_splits)), 1)) + "%)")
                if files_processed > 0:
                    duration = time.time() - starttime
                    avg_calctime_hist = duration / files_processed
                    remaining_time = (amount_of_generated_splits - files_processed) * avg_calctime_hist
                    print("Remaining calculation time (est.): " + str(remaining_time) + " seconds")
                    print("Finish time for Step 1(est.): " + time.asctime(time.localtime(time.time() + remaining_time)))
                    print("Step 1 is the most time consuming, Step 2 and 3 will take a flat ~5 minutes combined")
                print("-----------------------------------------------------------------")
                subprocess.call(cmd)
                files_processed += 1


# determine best n dps-simulations and grabs their profiles for further simming
# count: number of top n dps-simulations
# source_subdir: directory of .result-files
# target_subdir: directory to store the resulting .sim-file
# origin: path to the originally in autosimc generated output-file containing all valid profiles
def grabBest(count, source_subdir, target_subdir, origin):
    print("Grabbest:")
    print("Variables: count: " + str(count))
    print("Variables: source_subdir: " + str(source_subdir))
    print("Variables: target_subdir: " + str(target_subdir))
    print("Variables: origin: " + str(origin))

    user_class = ""

    best = {}
    for root, dirs, files in os.walk(os.path.join(os.getcwd(), source_subdir)):
        for file in files:
            print("Grabbest -> file: " + str(file))
            if file.endswith(".result"):
                if os.stat(os.path.join(os.getcwd(), source_subdir, file)).st_size > 0:
                    src = open(os.path.join(os.getcwd(), source_subdir, file))
                    for line in src.readlines():
                        line = line.lstrip().rstrip()
                        if not line:
                            continue
                        if line.rstrip().startswith("HPS"):
                            continue
                        if line.rstrip().startswith("DPS"):
                            continue
                        # here parsing stops, because its useless profile-junk
                        if line.rstrip().startswith("DPS:"):
                            break
                        if line.rstrip().endswith("Raid"):
                            continue
                        # just get user_class from player_info, very dirty
                        if line.rstrip().startswith("Player"):
                            q, w, e, r, t, z = line.split()
                            user_class = r
                            break
                        # dps, percentage, profilename
                        a, b, c = line.split()
                        # put dps as key and profilename as value into dictionary
                        # dps might be equal for 2 profiles, but should very rarely happen
                        # could lead to a problem with very minor dps due to variance,
                        # but seeing dps going into millions nowadays equal dps shouldn´t pose to be a problem at all
                        best[a] = c
                    src.close()
                else:
                    print("Error: .result-file in: " + str(source_subdir) + " is empty, exiting")
                    sys.exit(1)

    # put best dps into a list, descending order
    sortedlist = []
    for entry in best.keys():
        sortedlist.append(entry)
    sortedlist.sort()
    sortedlist.reverse()

    # trim list to desired number
    while len(sortedlist) > count:
        sortedlist.pop()

    # and finally generate a second list with the corresponding profile-names
    sortednames = []
    while len(sortedlist) > 0:
        sortednames.append(best.get(sortedlist.pop()))

    bestprofiles = []

    # now parse our "database" and extract the profiles of our top n
    source = open(origin, "r")
    lines = source.readlines()
    lines_iter = iter(lines)

    for line in lines_iter:
        line = line.lstrip().rstrip()
        if not line:
            continue

        currentbestprofile = ""

        if line.startswith(user_class + "="):
            separator = line.find("=")
            profilename = line[separator + 1:len(line)]
            if profilename in sortednames:
                # print(profilename+": "+(str)(sortednames.index(profilename)))

                # print(profilename)
                line = line + "\n"
                while not line.startswith("main_hand"):
                    currentbestprofile += line
                    line = next(lines_iter)
                currentbestprofile += line
                line = next(lines_iter)
                if line.startswith("off_hand"):
                    currentbestprofile += line + "\n"
                else:
                    currentbestprofile += "\n"
                bestprofiles.append(currentbestprofile)

    source.close()

    subfolder = os.path.join(os.getcwd(), target_subdir)
    purge_subfolder(subfolder)

    output = open(os.path.join(os.getcwd(), target_subdir, "best" + str(count) + ".sim"), "w")
    for line in bestprofiles:
        output.write(line)

    output.close()
