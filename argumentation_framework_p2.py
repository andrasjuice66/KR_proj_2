import json
import random
import timeit
import time
import matplotlib.pyplot as plt


def plot_execution_times(execution_times):
    # Create a 2x2 subplot grid
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    axes = axes.flatten()

    # Iterate over each file and its execution times
    for idx, (filename, times) in enumerate(execution_times.items()):
        if idx < len(axes):
            arguments = list(times.keys())
            times = list(times.values())

            axes[idx].bar(arguments, times, color='skyblue')
            axes[idx].set_title(f'Execution Times for {filename}')
            axes[idx].set_ylabel('Time (seconds)')
            axes[idx].set_xlabel('Arguments')
        else:
            break

    plt.tight_layout()
    for i in range(idx + 1, 4):
        fig.delaxes(axes[i])

    plt.show()


class ArgumentationFramework:
    def __init__(self, filepath):
        with open(filepath, 'r') as file:
            data = json.load(file)
        self.arguments = data["Arguments"]
        self.attacks_relations = data["Attack Relations"]

    def attacks_itself(self, argument):
        for i in self.attacks_relations:
            if i[0] == argument and i[1] == argument:
                return True  
        return False

    def find_cf(self):
        cf = []
        for key, value in self.arguments.items():
            if self.attacks_itself(key):
                continue
            else:
                cf.append({key})
            # find if empty set is applicable
            for attacks in self.attacks_relations:
                if attacks[1] == key:
                    break
            else:
                if {} not in cf:
                    cf.append({})
            # add all sets that do not attack each other
            for key2, value2 in self.arguments.items():
                if key != key2:
                    for i in self.attacks_relations:
                        if (i[1] == key and i[0] == key2) or (i[1] == key2 and i[0] == key):
                            break
                    else:
                        if {key2, key} not in cf:
                            cf.append({key2, key})
        return cf

    def find_stb(self):
        cf = self.find_cf()
        stb = cf.copy()
        for set in cf:
            if len(set) <= 1:
                stb.remove(set)
                continue
            for key, value in self.arguments.items():
                if key not in set:
                    for item in set:
                        if [item, key] in self.attacks_relations:
                            break
                    else:
                        stb.remove(set)
                        break
        return stb

# you can use this code example why we wanted to take the other one 
# as this one is longer 1. seeing which arguments are not admissable and then
# remove them from the conflict free list compared to go through each set in cf 
# and directly remove it if it does not defend itself

# Could imagine thogh that the runtime is slightly faster in the first example as smaller loops

    def find_adm(self):
        cf = self.find_cf()
        adm = cf.copy()
        
        not_adm = []
        
        for key, value in self.arguments.items():
            outs = 0
            ins = 0
            for i in self.attacks_relations:
                    if i[0] == key:
                        outs += 1
                    if i[1] == key:
                        ins += 1
            if ins > outs:
                not_adm.append(key)
        print(not_adm)
    
        for set in adm[:]:
            if set == {}:
                adm.remove(set)
                continue
            for element in not_adm:
                if (element in set) and (set in adm):
                    adm.remove(set)
        return adm

    # finds admissable arguments different way of coding
    def find_adm2(self):
        cf = self.find_cf()
        adm2 = cf.copy()
        
        for set in adm2[:]:
            if set == {}:
                adm2.remove(set)
                continue
            for element in set:
                ins = 0
                outs = 0
                for i in self.attacks_relations:
                    if i[0] == element:
                        outs += 1
                    if i[1] == element:
                        ins += 1
                if ins > outs:
                    adm2.remove(set)
                    break
        return adm2
        
    def proof_ca_adm(self, argument):
        adm = self.find_adm2()
        is_ca = False
        for i in adm:
            if argument in i:
                is_ca = True
                break
        return is_ca

    def proof_ca_stb(self, argument):
        stb = self.find_stb()
        is_ca = False
        for i in stb:
            if argument in i:
                is_ca = True
                break
        return is_ca
    

def main(filename, argument):

    print(f"\nRunning for file: {filename} with argument: '{argument}'")

    start_time = time.time()
    af = ArgumentationFramework(filename)

    if af.proof_ca_adm(argument):
        print(f"Argument {argument} in {filename} is credulously acceptable with regards to admissible")
    else:
        print(f"Argument {argument} in {filename} is not credulously acceptable with regards to admissible")

    if af.proof_ca_stb(argument):
        print(f"Argument {argument} in {filename} is credulously acceptable with regards to stable")
    else:
        print(f"Argument {argument} in {filename} is not credulously acceptable with regards to stable")

    end_time = time.time()
    return end_time - start_time  



if __name__ == '__main__':
    # data_files = {"example-input-format_original.json" : ['a'], "example-input-format-1.json": ['a','k'], 
    #          "example-input-format-2.json": ['c','d','a'], "example-input-format-3.json": ['b','d','e']}

    # execution_times = {}

    # for filename in data_files:
    #     for argument in data_files[filename]:
    #         execution_time = main(filename, argument)
    #         execution_times[filename] = execution_time
    #         print(f"Execution time for {filename}: {execution_time} seconds")

    # print("\nAll Execution Times:")
    # for filename, time in execution_times.items():
    #     print(f"{filename}: {time} seconds")

    data_files = {
        "example-input-format_original.json": ['a'], 
        "example-input-format-1.json": ['a', 'k'], 
        "example-input-format-2.json": ['c', 'd', 'a'], 
        "example-input-format-3.json": ['b', 'd', 'e']
    }

    execution_times = {}

    for filename in data_files:
        execution_times[filename] = {}
        for argument in data_files[filename]:
            execution_time = main(filename, argument)
            execution_times[filename][argument] = execution_time
            print(f"Execution time for {filename} with argument '{argument}': {execution_time} seconds")

    print("\nAll Execution Times:")
    for filename, times in execution_times.items():
        for argument, time in times.items():
            print(f"{filename} with argument '{argument}': {time} seconds")

    plot_execution_times(execution_times)

