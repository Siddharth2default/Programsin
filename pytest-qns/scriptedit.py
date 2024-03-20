import matplotlib.pyplot as plt
import numpy as np
import json
import click
import subprocess

#print("ji")
#print("hero")
CPU_KEY = "cpu";
MEM_KEY = "memory";
GPU_KEY = "gpu";
POWER_KEY = "power";
FILES_KEY = "files";
PROCESS_KEY = "processes";
USECASE_KEY = "use_case";
OUTPUT_DIR = "output_dir"
DEBUG_TAG = "[DEBUG]"
LIST_OF_KEYS = [CPU_KEY, MEM_KEY, GPU_KEY, POWER_KEY];
DEBUG = 0  # Change this to 1 to enable debug logs
#help()

def print_debug(str):
    if (DEBUG == 1):
        print("{0} {1}".format(DEBUG_TAG, str));
    return;


def execute_command(cmd):
    print_debug("Command: " + cmd);
    out = subprocess.check_output(cmd, shell=True);
    return np.array(out.decode('utf-8').splitlines()).astype(np.int64);


def system_cpu(file_name):
    cmd = "grep 'CPU |' {0} | awk '{1}' | sed 's/%//g' | awk '{2}'".format(file_name, '{print$4,$7}', '{print $1 + $2}')
    return execute_command(cmd)


def process_cpu(process_name, file_name):
    cmd = "grep -i '{0}' {1} | awk '{2}' | sed 's/%//g'".format(process_name, file_name, '{print$4}');
    return execute_command(cmd)
    help()

# def process_mem(process_name, file_name):
#    cmd = "grep -i '{0}' {1} | awk 'NR%2==0' | awk '{2}' | sed 's/[:,K]//g'".format(process_name, file_name, '{print$1}')
#    return execute_command(cmd)

def system_mem(process_name, file_name):
    if (process_name == "Used RAM"):
        cmd = "grep -i '{0}' {1} | awk '{2}' | sed 's/[:,K]//g'".format(process_name, file_name, '{print$3}');
    elif (process_name == "Lost RAM"):
        cmd = "grep -i '{0}' {1} | awk '{2}' | sed 's/[:,K]//g'".format(process_name, file_name, '{print$3}');
    elif (process_name == "Avail RAM"):
        cmd = "grep -i '{0}' {1} | awk '{2}' | sed 's/[:,K]//g'".format(process_name, file_name, '{print$3}');
    elif (process_name == "ZRAM_Physical"):
        process_name = "ZRAM";
        cmd = "grep -i '{0}' {1} | awk '{2}' | sed 's/[:,K]//g'".format(process_name, file_name, '{print$2}');
    elif (process_name == "ZRAM_Swap"):
        process_name = "ZRAM";
        cmd = "grep -i '{0}' {1} | awk '{2}' | sed 's/[:,K]//g'".format(process_name, file_name, '{print$6');
    else:
        cmd = "grep -i '{0}' {1} | awk 'NR%2==0' | awk '{2}' | sed 's/[:,K]//g'".format(process_name, file_name,
                                                                                        '{print$1}')
    return execute_command(cmd)


def system_gpu(file_name):
    cmd = "cat {0} | awk '{1}'".format(file_name, '{print$1}');
    return execute_command(cmd)


def soc_power(file_name):
    cmd = "cat {0} | grep -i 'this->shunt_voltage' | awk '{1}' | sed 's/4_2v_main//g' | sed 's/[:mW]//g'".format(
        file_name, '{print$5}');
    return execute_command(cmd)


def get_config(file_name):
    config_file = open(file_name);
    config = json.load(config_file);
    config_file.close()
    return config;


# Matches the file name to the tag used for generating the resource file
def get_files_for_type(type, directory):
    tag = None
    if (type == CPU_KEY):
        tag = "atop_";
    elif (type == MEM_KEY):
        tag = "meminfo_";
    elif (type == GPU_KEY):
        tag = "gpuinfo_";
    elif (type == POWER_KEY):
        tag = "powerinfo_";
    else:
        print("Type {0} Not suported for getting files".format(type));
    cmd = "ls -d {0}/* | grep {1}".format(directory, tag);
    out = processes.check_output(cmd, shell=True);
    return np.array(out.decode('utf-8').splitlines())


# Memory/CPU Baseline for each process listed here . Reference doc - "https://wiki.labcollab.net/confluence/display/VESTA/MTBF+System+Resource+Utilisation+Format"
def baseline_values(process_name, type):
    memory_baseline = 0;
    cpu_baseline = 0;
    if (process_name == "visual.perception.orchestrator"):
        memory_baseline = 330;
        cpu_baseline = 250;
    elif (process_name == "neso.sentry"):
        memory_baseline = 150;
        cpu_baseline = 200;
    elif (process_name == "cameracapabilityagent"):
        memory_baseline = 335;
        cpu_baseline = 100;
    elif (process_name == "cameraserver"):
        memory_baseline = 220;
        cpu_baseline = 168;
    elif (process_name == "audioserver"):
        memory_baseline = 14;
        cpu_baseline = 76;
    elif (process_name == "vesta.artifacts"):
        memory_baseline = 206;
        cpu_baseline = 104;
    elif (process_name == "com.amazon.neso.alexadomainimperio"):
        memory_baseline = 40;
        cpu_baseline = 50;
    elif (process_name == "neso.bsm"):
        memory_baseline = 95;
        cpu_baseline = 118;
    elif (process_name == "oorplan.service"):
        memory_baseline = 234;
        cpu_baseline = 200;
    elif (process_name == "neso.characterapp"):
        memory_baseline = 120;
        cpu_baseline = 40;
    elif (process_name == "neso.sfx"):
        memory_baseline = 101;
        cpu_baseline = 51;
    elif (process_name == "on.neso.display"):
        memory_baseline = 300;
        cpu_baseline = 50;
    elif (process_name == "neso.trope.state"):
        memory_baseline = 70;
        cpu_baseline = 40;
    elif (process_name == "amazon.neso.btm"):
        memory_baseline = 79;
        cpu_baseline = 118;
    elif (process_name == "neso.motion"):
        memory_baseline = 85;
        cpu_baseline = 12;
    elif (process_name == "ceproxy.service"):
        memory_baseline = 123;
        cpu_baseline = 98;
    elif (process_name == "a.social.cortex"):
        memory_baseline = 103.7;
        cpu_baseline = 70;

    if (type == "MEMORY"):
        return memory_baseline;
    elif (type == "CPU"):
        return cpu_baseline;
    else:
        print("Baseline defined for only CPU and MEMORY - Please choose type between CPU / MEMORY")


# return baseline;

def generate_data(usecase, type, config, output_dir):
    graph_data = []
    # Iterate over files
    print_debug("################## Result ##################")
    # For each Process present in config ... Iterate
    for k in config[PROCESS_KEY]:
        avg_data_point, min_data_point, max_data_point = None, None, None;
        # For each of the Files (Runs) present in the Files/Dir ... Iterate
        for index, file in enumerate(config[FILES_KEY], start=0):
            process_data = None
            # Get correspoding array of data by parsing the file
            if (type == CPU_KEY):
                # Special Check for Overall System calcluation
                if (k["text"] == "system"):
                    process_data = system_cpu(file);
                else:
                    process_data = process_cpu(k["text"], file);
            elif (type == MEM_KEY):
                process_data = system_mem(k["text"], file);
                # Special Check for Overall System RAM & ZRAM calcluation
                # if k["text"]in ['Used RAM', 'Lost RAM', 'Avail RAM', 'ZRAM_Physical', 'ZRAM_Swap']:
                #    print(k["text"])
                #    process_data = system_mem(k["text"],file);
                # elif (k["text"] == "ZRAM_Physical" or "ZRAM_Swap"):
                #    process_data = system_mem_zram(k["text"],file);
                #    print(k["text"]);
                # else:
                #    process_data = process_mem(k["text"],file);
            elif (type == GPU_KEY):
                process_data = system_gpu(file);
            elif (type == POWER_KEY):
                process_data = soc_power(file);
            else:
                print("Type {0} Not suported".format(type));
            print_debug("Process Name [{0}] : Processing Type: [{1}]".format(k["label"], type));

            # Get the Average number from the parsed data
            avg_of_the_run = int(np.mean(process_data));

            # {Important} We are using a hypothesis to trim the data to above the Average
            # This is because the data colection might have started before the use case executes and also
            # can end after the use-case completes
            #
            # This causes sometimes low values to polute the data. Hence we consider only the data that is above average run.
            # Ex: (Consider we started with 15MB of memory in IDLE State, but use 100MB during use-case, if we count 15MB in data set, that will skew our min, avg, max caluculation)
            trimmed_process_data = [x for x in process_data if x >= avg_of_the_run];
            graph_data.append({
                "data": process_data,
                "count": list(range(0, len(process_data))),
                "label": k["label"],
                "config_file": index
            })

            # Calculate average data point accross all runs
            if (avg_data_point == None):
                avg_data_point = np.average(trimmed_process_data);
            else:
                avg_data_point = np.average([avg_data_point, np.average(trimmed_process_data)])

            # Calculate min datapoint accross all runs
            if (min_data_point == None):
                min_data_point = min(trimmed_process_data);
            else:
                min_data_point = np.min([min_data_point, min(trimmed_process_data)]);

            # Calculate max datapoint accross all runs
            if (max_data_point == None):
                max_data_point = max(trimmed_process_data);
            else:
                max_data_point = np.max([max_data_point, max(trimmed_process_data)]);
        print_debug("****************Start****************")
        # print("UseCase: {0} ; Type {1} ; ProcessName: {2} ; Min: {3} ; Max: {4} ; Avg: {5}".format(usecase, type.upper(), k["label"], min_data_point, max_data_point, avg_data_point));

        # Comparing with baseline for Memory
        if (type.upper() == "MEMORY"):
            baseline_value = baseline_values(k["text"], type.upper());

            if (((max_data_point / 1024) > baseline_value) and baseline_value > 0):

                print("\n.................... Memory baseline crossed for process {0} ....................".format(
                    k["text"]))
                print(
                    "UseCase: {0} ; Type {1} ; ProcessName: {2} (baseline:- {6} MB); Min: {3} MB ; Max: {4} MB; Avg: {5} MB . - Crossing the memory baseline - Max: {4} MB , Baseline : {6} MB by {7}% percentage.\n".format(
                        usecase, type.upper(), k["label"], "{:.2f}".format(min_data_point / 1024),
                        "{:.2f}".format(max_data_point / 1024), "{:.2f}".format(avg_data_point / 1024), baseline_value,
                        "{:.2f}".format((((max_data_point / 1024) - baseline_value) / baseline_value) * 100)))

            elif (baseline_value == 0):
                print("-------- Memory baseline value not defined for ProcessName: {0} --------".format(k["text"]))
                print("UseCase: {0} ; Type {1} ; ProcessName: {2} ; Min: {3} MB ; Max: {4} MB ; Avg: {5} MB.".format(
                    usecase, type.upper(), k["label"], "{:.2f}".format(min_data_point / 1024),
                    "{:.2f}".format(max_data_point / 1024), "{:.2f}".format(avg_data_point / 1024)))

            else:
                print(
                    "UseCase: {0} ; Type {1} ; ProcessName: {2} (baseline:- {3} MB); Min: {4} MB ; Max: {5} MB ; Avg: {6} MB.".format(
                        usecase, type.upper(), k["label"], baseline_value, "{:.2f}".format(min_data_point / 1024),
                        "{:.2f}".format(max_data_point / 1024), "{:.2f}".format(avg_data_point / 1024)))


        # For comparison between CPU and Baseline.

        elif (type.upper() == "CPU"):
            baseline_value = baseline_values(k["text"], type.upper());

            if (max_data_point > baseline_value and baseline_value > 0):

                print(
                    "\n.................... CPU baseline crossed for process {0} ....................".format(k["text"],
                                                                                                              baseline_value))
                print(
                    "UseCase: {0} ; Type {1} ; ProcessName: {2} (baseline:- {6}); Min: {3} ; Max: {4} ; Avg: {5} . - Crossing the CPU baseline - Max: {4} Baseline : {6} by {7}% percentage.\n".format(
                        usecase, type.upper(), k["label"], "{:.2f}".format(min_data_point),
                        "{:.2f}".format(max_data_point), "{:.2f}".format(avg_data_point), baseline_value,
                        "{:.2f}".format(((max_data_point - baseline_value) / baseline_value) * 100)))

            elif (baseline_value == 0):
                print("-------- CPU baseline value not defined for ProcessName: {0} --------".format(k["text"]))
                print("UseCase: {0} ; Type {1} ; ProcessName: {2} ; Min: {3} ; Max: {4} ; Avg: {5}.".format(usecase,
                                                                                                            type.upper(),
                                                                                                            k["label"],
                                                                                                            "{:.2f}".format(
                                                                                                                min_data_point),
                                                                                                            "{:.2f}".format(
                                                                                                                max_data_point),
                                                                                                            "{:.2f}".format(
                                                                                                                avg_data_point)))

            else:
                print(
                    "UseCase: {0} ; Type {1} ; ProcessName: {2} (baseline:- {3}); Min: {4} ; Max: {5} ; Avg: {6} .".format(
                        usecase, type.upper(), k["label"], baseline_value, "{:.2f}".format(min_data_point),
                        "{:.2f}".format(max_data_point), "{:.2f}".format(avg_data_point)))

        # For GPU.
        # else:
        #    print("UseCase: {0} ; Type {1} ; ProcessName: {2} ; Min: {3} ; Max: {4} ; Avg: {5} .".format(usecase, type.upper(), k["label"], "{:.2f}".format(min_data_point), "{:.2f}".format(max_data_point), "{:.2f}".format(avg_data_point)))

    print_debug("****************END****************")
    # Graph Plotting
    fig = plt.figure(figsize=(19.20, 10.80))
    # fig, axsList = plt.subplots(len(cpu_config[FILES_KEY]));
    fig.suptitle("{0} Measurement for UseCase: {1}".format(type, usecase).capitalize());
    for index in range(len(config[FILES_KEY])):
        axs = plt.subplot(int("1" + str(len(config[FILES_KEY])) + str(index + 1)))
        axs.set_title("Run " + str(index + 1), y=0, pad=-25, verticalalignment="top")
        for k in range(len(graph_data)):
            if (graph_data[k]["config_file"] == index):
                axs.plot(list(graph_data[k]["count"]), list(graph_data[k]["data"]), label=graph_data[k]["label"])
                axs.legend(loc="upper right")
    graph_file_name = "{0}/{1}_{2}.png".format(output_dir, type.upper(), usecase.replace(" ", "_"));
    plt.savefig(graph_file_name);
    print("\nGraph generated at {0}".format(graph_file_name));
    print_debug("################## End ##################")


@click.command()
@click.argument('config_file', required=1)
def parser(config_file):
    # Parse Config
    config = get_config(config_file)
    # Get Keys (cpu, mem, etc.)
    keys = config.keys();
    usecase = config[USECASE_KEY];
    output_dir = config[OUTPUT_DIR]
    for type in keys:
        # Trim the keys as the config contains other keys also
        if (type in LIST_OF_KEYS):
            config_for_type = config[type];
            # If directory is specified use it and ignore files section
            if ("dir" in config_for_type):
                config_for_type[FILES_KEY] = get_files_for_type(type, config_for_type["dir"])
            print("\n**************************************************************************************\n")
            generate_data(usecase, type, config_for_type, output_dir)


if __name__ == '__main__':
    parser()
