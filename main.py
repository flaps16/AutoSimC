import configparser
import sys
import datetime
import os

import splitter
import Analyzer

# Var init with default value
c_profileid = 0
c_profilemaxid = 0
legmin = 0
legmax = 2

outputFileName = "out.simc"
# txt, because standard-user cannot be trusted
inputFileName = "input.txt"

logFileName = "logs.txt"
errorFileName = "error.txt"
# quiet_mode for faster output; console is very slow
b_quiet = 0
i_generatedProfiles = 0

b_simcraft_enabled = False
s_stage = "stage1"


#   Error handle
def printLog(stringToPrint):
    if not b_quiet:
        # should this console-output be here at all? outputting to file AND console could be handled separately
        # e.g. via simple debug-toggle (if b_debug: print(...))
        print(stringToPrint)
    today = datetime.date.today()
    logFile.write(str(today) + ":" + stringToPrint + "\n")


# Add legendary to the right tab
def addToTab(x):
    stringToAdd = "L,id=" + x[1] + (",bonus_id=" + x[2] if x[2] != "" else "") + (
        ",enchant_id=" + x[3] if x[3] != "" else "") + (",gem_id=" + x[4] if x[4] != "" else "")
    if x[0] == 'head':
        l_head.append(stringToAdd)
    elif x[0] == 'neck':
        l_neck.append(stringToAdd)
    elif x[0] == 'shoulders':
        l_shoulders.append(stringToAdd)
    elif x[0] == 'back':
        l_back.append(stringToAdd)
    elif x[0] == 'chest':
        l_chest.append(stringToAdd)
    elif x[0] == 'wrist':
        l_wrists.append(stringToAdd)
    elif x[0] == 'hands':
        l_hands.append(stringToAdd)
    elif x[0] == 'waist':
        l_waist.append(stringToAdd)
    elif x[0] == 'legs':
        l_legs.append(stringToAdd)
    elif x[0] == 'feet':
        l_feet.append(stringToAdd)
    elif x[0] == 'finger1':
        l_finger1.append(stringToAdd)
    elif x[0] == 'finger2':
        l_finger2.append(stringToAdd)
    elif x[0] == 'trinket1':
        l_trinket1.append(stringToAdd)
    elif x[0] == 'trinket2':
        l_trinket2.append(stringToAdd)


# Manage legendary with command line
def handlePermutation(elements):
    for element in elements:
        pieces = element.split('|')
        addToTab(pieces)


# Check if permutation is valid
def checkUsability():
    if l_gear[10] == l_gear[11]:
        return "Same ring"
    if l_gear[12] == l_gear[13]:
        return "Same trinket"

    nbLeg = 0
    for a in range(len(l_gear)):
        if l_gear[a][0] == "L":
            nbLeg = nbLeg + 1
    if nbLeg < legmin:
        return str(nbLeg) + " leg (too low)"
    if nbLeg > legmax:
        return str(nbLeg) + " leg (too much)"

    return ""


# Print a simc profile
def scpout(oh):
    global c_profileid
    global i_generatedProfiles
    result = checkUsability()
    digits = len(str(c_profilemaxid))
    mask = '00000000000000000000000000000000000'
    maskedProfileID = (mask + str(c_profileid))[-digits:]
    # output status every 5000 permutations, user should get at least a minor progress shown; also doesn´t slow down
    # computation very much
    if int(maskedProfileID) % 5000 == 0:
        print("Processed: " + str(maskedProfileID) + "/" + str(c_profilemaxid) + " (" + str(
            round(100 * float(int(maskedProfileID) / int(c_profilemaxid)), 1)) + "%)")
    if result != "":
        printLog("Profile:" + str(maskedProfileID) + "/" + str(c_profilemaxid) + ' Warning, not printed:' + result)
    else:
        if not b_quiet:
            print("Profile:" + str(maskedProfileID) + "/" + str(c_profilemaxid))
        outputFile.write(c_class + "=" + c_profilename + "_" + maskedProfileID + "\n")
        outputFile.write("specialization=" + c_spec + "\n")
        outputFile.write("race=" + c_race + "\n")
        outputFile.write("level=" + c_level + "\n")
        outputFile.write("role=" + c_role + "\n")
        outputFile.write("position=" + c_position + "\n")
        outputFile.write("talents=" + c_talents + "\n")
        outputFile.write("artifact=" + c_artifact + "\n")
        if c_other != "":
            outputFile.write(c_other + "\n")
        outputFile.write("head=" + (l_gear[0] if l_gear[0][0] != "L" else l_gear[0][1:]) + "\n")
        outputFile.write("neck=" + (l_gear[1] if l_gear[1][0] != "L" else l_gear[1][1:]) + "\n")
        outputFile.write("shoulders=" + (l_gear[2] if l_gear[2][0] != "L" else l_gear[2][1:]) + "\n")
        outputFile.write("back=" + (l_gear[3] if l_gear[3][0] != "L" else l_gear[3][1:]) + "\n")
        outputFile.write("chest=" + (l_gear[4] if l_gear[4][0] != "L" else l_gear[4][1:]) + "\n")
        outputFile.write("wrists=" + (l_gear[5] if l_gear[5][0] != "L" else l_gear[5][1:]) + "\n")
        outputFile.write("hands=" + (l_gear[6] if l_gear[6][0] != "L" else l_gear[6][1:]) + "\n")
        outputFile.write("waist=" + (l_gear[7] if l_gear[7][0] != "L" else l_gear[7][1:]) + "\n")
        outputFile.write("legs=" + (l_gear[8] if l_gear[8][0] != "L" else l_gear[8][1:]) + "\n")
        outputFile.write("feet=" + (l_gear[9] if l_gear[9][0] != "L" else l_gear[9][1:]) + "\n")
        outputFile.write("finger1=" + (l_gear[10] if l_gear[10][0] != "L" else l_gear[10][1:]) + "\n")
        outputFile.write("finger2=" + (l_gear[11] if l_gear[11][0] != "L" else l_gear[11][1:]) + "\n")
        outputFile.write("trinket1=" + (l_gear[12] if l_gear[12][0] != "L" else l_gear[12][1:]) + "\n")
        outputFile.write("trinket2=" + (l_gear[13] if l_gear[13][0] != "L" else l_gear[13][1:]) + "\n")
        outputFile.write("main_hand=" + l_gear[14] + "\n")
        if oh == 1:
            outputFile.write("off_hand=" + l_gear[15] + "\n\n")
        else:
            outputFile.write("\n")
        i_generatedProfiles += 1
    c_profileid += 1
    return ()


# Manage command line parameters
def handleCommandLine():
    global inputFileName
    global outputFileName
    global legmin
    global legmax
    global b_quiet
    global b_simcraft_enabled
    global s_stage

    # parameter-list, so they are "protected" if user enters wrong commandline
    set_parameters = set()
    set_parameters.add("-i")
    set_parameters.add("-o")
    set_parameters.add("-l")
    set_parameters.add("-quiet")
    set_parameters.add("-sim")

    for a in range(1, len(sys.argv)):
        if sys.argv[a] == "-i":
            inputFileName = sys.argv[a + 1]
            if inputFileName not in set_parameters:
                if os.path.isfile(inputFileName):
                    printLog("Input file changed to " + inputFileName)
                else:
                    print("Error: Input file does not exist")
                    sys.exit(1)
            else:
                print("Error: No or invalid input file declared: " + inputFileName)
                sys.exit(1)
        if sys.argv[a] == "-o":
            outputFileName = sys.argv[a + 1]
            if outputFileName not in set_parameters:
                printLog("Output file changed to " + outputFileName)
                # if os.path.isfile(outputFileName):
                #    print("Error: Output file already exists")
                #    sys.exit(1)
            else:
                print("Error: No or invalid output file declared: " + outputFileName)
                sys.exit(1)
        if sys.argv[a] == "-l":
            elements = sys.argv[a + 1].split(',')
            # produced an error if <-l "" 2:2> was entered, therefore check for emptyness
            if elements:
                handlePermutation(elements)
            # number of leg
            if sys.argv[a + 2][0] != "-":
                legNb = sys.argv[a + 2].split(':')
                legmin = int(legNb[0])
                legmax = int(legNb[1])
                printLog("Set legendary to  " + str(legmin) + "/" + str(legmax))
        if sys.argv[a] == "-quiet":
            printLog("Quiet-Mode enabled")
            b_quiet = 1
        if sys.argv[a] == "-sim":
            print("SimCraft-Mode enabled")
            printLog("SimCraft-Mode enabled")
            b_simcraft_enabled = True
            # optional parameter to skip steps and continue at a certain point without deleting intermediate files:
            # usage main.py -i ... -o ... -sim [stage1|stage2|stage3]
            # staging is equivalent to the 3 iteration processes:
            #   - 1: mass processing with few iterations (default)
            #   - 2: picking best n and process these
            #   - 3: picking top n out of these
            # it is essentially used to skip the most time consuming part, stage 1
            # to test alterations and different outputs, e.g. using same gear within different scenarios
            # (standard might be patchwerk, but what happens with this gear- and talentchoice in a helterskelter-szenario?)
            if sys.argv[a + 1]:
                stage = sys.argv[a + 1]
                if stage in set_parameters:
                    printLog("Wrong parameter for -sim: " + stage)
                    print("Wrong parameter for ""-sim"" option: " + str(stage))
                    sys.exit(1)
                if not stage:
                    printLog("Missing parameter for -sim: " + stage)
                    print("Missing parameter for ""-sim"" option: " + str(stage))
                    sys.exit(1)
                if stage != "stage1" or stage != "stage2" or stage != "stage3":
                    s_stage = stage

            # check path of simc.exe
            if not os.path.exists(splitter.simc_path):
                printLog("Path to simc.exe: " + str(splitter.simc_path))
                printLog("Error: Invalid path for simc.exe, please edit splitter.py (Hit ""enter"" to exit")
                sys.exit(1)
            else:
                printLog("Path to simc.exe valid, proceeding...")


#########################
#### Program Start ###### 
#########################   
sys.stderr = open(errorFileName, 'w')
logFile = open(logFileName, 'w')

handleCommandLine()

# Read input.txt to init vars
config = configparser.ConfigParser()
config.read(inputFileName)
profile = config['Profile']
gear = config['Gear']

# Read input.txt
#   Profile
c_profilename = profile['profilename']
c_profileid = int(profile['profileid'])
c_class = profile['class']
c_race = profile['race']
c_level = profile['level']
c_spec = profile['spec']
c_role = profile['role']
c_position = profile['position']
c_talents = profile['talents']
c_artifact = profile['artifact']
c_other = profile['other']

#   Gear
c_head = gear['head']
c_neck = gear['neck']
if config.has_option('Gear', 'shoulders'):
    c_shoulders = gear['shoulders']
else:
    c_shoulders = gear['shoulder']
c_back = gear['back']
c_chest = gear['chest']
if config.has_option('Gear', 'wrists'):
    c_wrists = gear['wrists']
else:
    c_wrists = gear['wrist']
c_hands = gear['hands']
c_waist = gear['waist']
c_legs = gear['legs']
c_feet = gear['feet']
c_finger1 = gear['finger1']
c_finger2 = gear['finger2']
c_trinket1 = gear['trinket1']
c_trinket2 = gear['trinket2']
c_main_hand = gear['main_hand']
if config.has_option('Gear', 'off_hand'):
    c_off_hand = gear['off_hand']
else:
    c_off_hand = ""

# Split vars to lists
l_head = c_head.split('|')
l_neck = c_neck.split('|')
l_shoulders = c_shoulders.split('|')
l_back = c_back.split('|')
l_chest = c_chest.split('|')
l_wrists = c_wrists.split('|')
l_hands = c_hands.split('|')
l_waist = c_waist.split('|')
l_legs = c_legs.split('|')
l_feet = c_feet.split('|')
l_finger1 = c_finger1.split('|')
l_finger2 = c_finger2.split('|')
l_trinket1 = c_trinket1.split('|')
l_trinket2 = c_trinket2.split('|')
l_main_hand = c_main_hand.split('|')
l_off_hand = c_off_hand.split('|')

# better handle rings and trinket-combinations

for a in l_finger2:
    if l_finger1.count(a) == 0:
        l_finger1.append(a)

for b in l_trinket2:
    if l_trinket1.count(b) == 0:
        l_trinket1.append(b)

set_fingers = set()
set_trinkets = set()

# compare items using simple string.compare-function, so "lowest" item (bitwise) will always be in front
# if combination is not in our result-set, concatenate and insert "|"-splitter
for ring in l_finger1:
    for ring2 in l_finger1:
        if ring == ring2:
            continue
        else:
            if ring < ring2:
                ring_combo = ring + "|" + ring2
                if ring_combo not in set_fingers:
                    set_fingers.add(ring_combo)
            else:
                ring_combo = ring2 + "|" + ring
                if ring_combo not in set_fingers:
                    set_fingers.add(ring_combo)

for trinket in l_trinket1:
    for trinket2 in l_trinket1:
        if trinket == trinket2:
            continue
        else:
            if trinket < trinket2:
                trinket_combo = trinket + "|" + trinket2
                set_trinkets.add(trinket_combo)
            else:
                trinket_combo = trinket2 + "|" + trinket
                set_trinkets.add(trinket_combo)

# convert set into list, i did not want to change the "theme" of the original data-structure
l_fingers = []
l_trinkets = []
while set_fingers:
    l_fingers.append(set_fingers.pop())
while set_trinkets:
    l_trinkets.append(set_trinkets.pop())

# free some memory
del set_fingers
del set_trinkets

# Make permutations
outputFile = open(outputFileName, 'w')
l_gear = ["head", "neck", "shoulders", "back", "chest", "wrists", "hands", "waist", "legs", "feet", "finger1",
          "finger2", "trinket1", "trinket2", "main_hand", "off_hand"]

# changed according to merged fields
c_profilemaxid = len(l_head) * len(l_neck) * len(l_shoulders) * len(l_back) * len(l_chest) * len(l_wrists) * len(
    l_hands) * len(l_waist) * len(l_legs) * len(l_feet) * len(l_fingers) * len(l_trinkets) * len(l_main_hand) * len(
    l_off_hand)
printLog("Starting permutations : " + str(c_profilemaxid))
for a in range(len(l_head)):
    l_gear[0] = l_head[a]
    for b in range(len(l_neck)):
        l_gear[1] = l_neck[b]
        for c in range(len(l_shoulders)):
            l_gear[2] = l_shoulders[c]
            for d in range(len(l_back)):
                l_gear[3] = l_back[d]
                for e in range(len(l_chest)):
                    l_gear[4] = l_chest[e]
                    for f in range(len(l_wrists)):
                        l_gear[5] = l_wrists[f]
                        for g in range(len(l_hands)):
                            l_gear[6] = l_hands[g]
                            for h in range(len(l_waist)):
                                l_gear[7] = l_waist[h]
                                for i in range(len(l_legs)):
                                    l_gear[8] = l_legs[i]
                                    for j in range(len(l_feet)):
                                        l_gear[9] = l_feet[j]
                                        # changed according to new concatenated fields
                                        for k in range(len(l_fingers)):
                                            fingers = l_fingers[k].split('|')
                                            l_gear[10] = fingers[0]
                                            l_gear[11] = fingers[1]
                                            for l in range(len(l_trinkets)):
                                                trinkets = l_trinkets[l].split('|')
                                                l_gear[12] = trinkets[0]
                                                l_gear[13] = trinkets[1]
                                                if c_off_hand != "":
                                                    for o in range(len(l_main_hand)):
                                                        l_gear[14] = l_main_hand[o]
                                                        for p in range(len(l_off_hand)):
                                                            l_gear[15] = l_off_hand[p]
                                                            scpout(1)
                                                else:
                                                    for o in range(len(l_main_hand)):
                                                        l_gear[14] = l_main_hand[o]
                                                        scpout(0)

printLog("Ending permutations")
print("Generated permutations: " + str(i_generatedProfiles))
outputFile.close()

# here comes the fun part, which makes autosimc a true automatic simcraft-tool
# it splits the generated output-file into smaller chunks (default is 50), so they can be simmed faster
# and memory-efficient, with small iterations (i=100)to generate fast results
# afterwards, it grabs the n top results and sims these again, this time with i=1000 iterations
# afterwards, for a third time, the top 3 results get simmed with i=10000, html-output and scalefactors enabled

iterations_firstpart = 100
iterations_secondpart = 1000
iterations_thirdpart = 10000

user_input = ""
if i_generatedProfiles > 10000:
    user_input = input(
        "-----> Beware: Computation with Simcraft might take a long time with this amount of profiles! <----- (Press Enter to continue, q to quit)")
if i_generatedProfiles > 100000:
    user_input = input(
        "-----> Beware: Computation with Simcraft might take a VERY long time with this amount of profiles! <----- (Press Enter to continue, q to quit)")

if user_input == "q":
    print("Program exit by user")
    sys.exit(0)

if b_simcraft_enabled:
    if os.path.exists(os.path.join(Analyzer.combined_path, Analyzer.analysis_filename)):
        # uses target_error as default
        target_error_mode = True
        choice = input(
            "Do you want to use existing data to get a better estimation of calculation times? y/n: ")
        if choice == "y":
            printLog("Using: " + str(Analyzer.analysis_filename) + "\n")
            print("Using " + str(Analyzer.analysis_filename) + " as database\n")
            class_spec = ""
            if c_class == "deathknight":
                if c_spec == "frost":
                    class_spec = "Frost Death Knight"
                elif c_spec == "unholy":
                    class_spec = "Unholy Death Knight"
            elif c_class == "demonhunter":
                if c_spec == "havoc":
                    class_spec = "Havoc Demon Hunter"
            elif c_class == "druid":
                if c_spec == "balance":
                    class_spec = "Balance Druid"
                elif c_spec == "feral":
                    class_spec = "Feral Druid"
            elif c_class == "hunter":
                if c_spec == "beast_mastery":
                    class_spec = "Beast Mastery Hunter"
                elif c_spec == "survival":
                    class_spec = "Survival Hunter"
                elif c_spec == "marksmanship":
                    class_spec = "Marksmanship Hunter"
            elif c_class == "mage":
                if c_spec == "frost":
                    class_spec = "Frost Mage"
                elif c_spec == "arcane":
                    class_spec = "Arcane Mage"
                elif c_spec == "fire":
                    class_spec = "Fire Mage"
            elif c_class == "priest":
                if c_spec == "shadow":
                    class_spec = "Shadow Priest"
            elif c_class == "paladin":
                if c_spec == "retribution":
                    class_spec = "Retribution Paladin"
            elif c_class == "monk":
                if c_spec == "windwalker":
                    class_spec = "Windwalker Monk"
            elif c_class == "shaman":
                if c_spec == "enhancement":
                    class_spec = "Enhancement Shaman"
                elif c_spec == "elemental":
                    class_spec = "Elemental Shaman"
            elif c_class == "rogue":
                if c_spec == "subtlety":
                    class_spec = "Subtlety Rogue"
                elif c_spec == "outlaw":
                    class_spec = "Outlaw Rogue"
                elif c_spec == "assassination":
                    class_spec = "Assassination Rogue"
            # todo check the following names
            elif c_class == "warrior":
                if c_spec == "fury":
                    class_spec = "Fury Warrior"
                elif c_spec == "arms":
                    class_spec = "Arms Warrior"
            elif c_class == "warlock":
                if c_spec == "affliction":
                    class_spec = "Affliction Warlock"
                elif c_spec == "demonology":
                    class_spec = "Demonology Warlock"
                elif c_spec == "destruction":
                    class_spec = "Destruction Warlock"
            else:
                printLog("Unsupported class/spec-combination: " + str(c_class) + " - " + str(c_spec) + "\n")
                print("Unsupported class/spec-combination: " + str(c_class) + " - " + str(c_spec) + "\n")

            print("You have to choose one of the following modes for calculation:")
            print("1) Static mode uses a fixed amount, but less accurate calculations per profile (" + str(
                iterations_firstpart) + "," + str(iterations_secondpart) + "," + str(iterations_thirdpart) + ")")
            print("It is however faster if simulating huge amounts of profiles")
            print("2) Dynamic mode lets you choose a specific 'correctness' of the calculation, but takes more time.")
            print(
                "It uses the chosen correctness for the first part; in finetuning part the error lowers to 0.4 and 0.1 for the final top 3")
            sim_mode = input("Please choose your mode: ")

            # static mode
            if str(sim_mode) == str(1):
                printLog("Mode" + str(sim_mode) + " chosen")
                if s_stage == "stage1":
                    printLog("Entering stage 1\n")
                    # split into chunks of 50
                    splitter.split(outputFileName, 50)
                    # sim these with few iterations, can still take hours with huge permutation-sets; fewer than 100 is not advised
                    splitter.sim(splitter.subdir1, iterations_firstpart, 1)
                    s_stage = "stage2"

                if s_stage == "stage2":
                    printLog("Entering stage 2")
                    # check if files exist
                    if os.path.exists(os.path.join(os.getcwd(), splitter.subdir1)):
                        does_file_exist = False
                        for root, dirs, files in os.walk(os.path.join(os.getcwd(), splitter.subdir1)):
                            for file in files:
                                if file.endswith(".sim"):
                                    does_file_exist = True
                                    print("Stage 2: .sim-files found, proceeding..")
                                    break

                        if does_file_exist:
                            # now grab the top 100 of these and put the profiles into the 2nd temp_dir
                            splitter.grabBest(100, splitter.subdir1, splitter.subdir2, outputFileName)
                            # where they are simmed again, now with 1000 iterations
                            splitter.sim(splitter.subdir2, iterations_secondpart, 1)
                            s_stage = "stage3"
                        else:
                            print("Error: No files exist in stage1-directory\n")
                    else:
                        print("No path was created in stage1\n")

                if s_stage == "stage3":
                    printLog("Entering stage 3")
                    if os.path.exists(os.path.join(os.getcwd(), splitter.subdir2)):
                        does_file_exist = False
                        for root, dirs, files in os.walk(os.path.join(os.getcwd(), splitter.subdir2)):
                            for file in files:
                                if file.endswith(".sim"):
                                    does_file_exist = True
                                    print("Stage 3: .sim-files found, proceeding..")
                                    break

                        if does_file_exist:
                            # again, for a third time, get top 3 profiles and put them into subdir3
                            splitter.grabBest(3, splitter.subdir2, splitter.subdir3, outputFileName)
                            # sim them finally with all options enabled; html-output remains in this folder
                            splitter.sim(splitter.subdir3, iterations_thirdpart, 2)
                        else:
                            print("Error: No files exist in stage2-directory\n")
                    else:
                        print("No path was created in stage2\n")

            # dynamic mode
            if str(sim_mode) == str(2):
                printLog("Mode" + str(sim_mode) + " chosen\n")
                result_data = Analyzer.get_data(class_spec)
                print("Listing options:\n")
                print("Estimated calculation times based on your data:\n")
                print("Class/Spec: " + str(class_spec) + "\n")
                print("Number of permutations to simulate: " + str(i_generatedProfiles) + "\n")
                for current in range(len(result_data)):
                    te = result_data[current][0]
                    tp = round(float(result_data[current][2]), 2)
                    est = round(float(result_data[current][2]) * i_generatedProfiles, 0)
                    h = round(est / 3600, 1)

                    print("(" + str(current) + "): Target Error: " + str(te) + "%: " + " Time/Profile: " + str(
                        tp) + " sec => Est. calc. time: " + str(est) + " sec (~" + str(h) + " hours)")

                calc_choice = input("Please enter the type of calculation to perform (q to quit):")
                if calc_choice == "q":
                    print("Quitting application")
                    sys.exit(0)
                if int(calc_choice) < len(result_data) and int(calc_choice) > 0:
                    printLog("Sim: Chosen Class/Spec: " + str(class_spec) + "\n")
                    printLog("Sim: Number of permutations: " + str(i_generatedProfiles) + "\n")
                    printLog("Sim: Chosen calculation:" + str(int(calc_choice)) + "\n")

                    te = result_data[int(calc_choice)][0]
                    tp = round(float(result_data[int(calc_choice)][2]), 2)
                    est = round(float(result_data[int(calc_choice)][2]) * i_generatedProfiles, 0)

                    printLog(
                        "Sim: (" + str(calc_choice) + "): Target Error: " + str(te) + "%:" + "Time/Profile:" + str(
                            tp) + " => Est. calc. time: " + str(est) + " sec\n")
                    time_all = round(est, 0)
                    printLog("Estimated calculation time: " + str(time_all) + "\n")
                    if time_all > 86400:
                        proceed = input(
                            "Warning: This might take a *VERY* long time (>24h) (q to quit, Enter to continue: )")
                        if proceed == "q":
                            print("Quitting application")
                            sys.exit(0)
                    if s_stage == "stage1":
                        # split into chunks of n (max 100) to not destroy the hdd
                        # todo: calculate dynamic amount of n
                        splitter.split(outputFileName, 50)
                        # sim these with few iterations, can still take hours with huge permutation-sets; fewer than 100 is not advised
                        splitter.sim_targeterror(splitter.subdir1, str(te), 1)
                        s_stage = "stage2"

                    if s_stage == "stage2":
                        # check if files exist
                        if os.path.exists(os.path.join(os.getcwd(), splitter.subdir1)):
                            does_file_exist = False
                            for root, dirs, files in os.walk(os.path.join(os.getcwd(), splitter.subdir1)):
                                for file in files:
                                    if file.endswith(".sim"):
                                        does_file_exist = True
                                        print("Stage 2: .sim-files found, proceeding..")
                                        break

                            if does_file_exist:
                                # now grab the top 100 of these and put the profiles into the 2nd temp_dir
                                splitter.grabBest(100, splitter.subdir1, splitter.subdir2, outputFileName)
                                # where they are simmed again, now with higher quality
                                splitter.sim_targeterror(splitter.subdir2, str(0.4), 1)
                                s_stage = "stage3"
                            else:
                                print("Error: No files exist in stage1-directory")
                        else:
                            print("No path was created in stage1")

                    if s_stage == "stage3":
                        if os.path.exists(os.path.join(os.getcwd(), splitter.subdir2)):
                            does_file_exist = False
                            for root, dirs, files in os.walk(os.path.join(os.getcwd(), splitter.subdir2)):
                                for file in files:
                                    if file.endswith(".sim"):
                                        does_file_exist = True
                                        print("Stage 3: .sim-files found, proceeding..")
                                        break

                            if does_file_exist:
                                # again, for a third time, get top 3 profiles and put them into subdir3
                                splitter.grabBest(3, splitter.subdir2, splitter.subdir3, outputFileName)
                                # sim them finally with all options enabled; html-output remains in this folder
                                splitter.sim_targeterror(splitter.subdir3, str(0.1), 2)
                            else:
                                print("Error: No files exist in stage2-directory")
                        else:
                            print("No path was created in stage2")
logFile.close()
