import json
import os
import glob

def getPedoLocations(postvis_path):

	pedos = {}
	#finds the most recently created file and reads it line by line
	postvis = open(glob.glob(postvis_path)[-1], "r")
	for line in postvis:
		l_arr = line.split()
		pedos[l_arr[1]] = [l_arr[2], l_arr[3]]

	return pedos_location # a dict with key value pedestrian id and value as an array of coordinates [x, y]

def removeSourceField(path_of_scenario_file, path_to_new_scenario):

	with open(path_of_scenario_file, 'r') as f:
	    scenario = json.load(f)
	scenario['scenario']["topography"]["sources"] = []

	with open(path_to_new_scenario, 'w') as outfile:
	    json.dump(scenario, outfile, indent=2)


def runScenario(path_of_vadere, path_of_scenario, path_of_output):

	run_scenario = 'java -jar '+ path_of_vadere + ' scenario-run --scenario-file "' + path_of_scenario + '" --output-dir="' + path_of_output + '"'
	os.system(run_scenario)

def addPedos(path_of_scenario, path_of_output, path_of_postvis):
	
	with open(path_of_scenario, 'r') as f:
	    scenario = json.load(f)

	path_of_output = glob.glob(path_of_output)[-1]

	pedo_count = countPedos(path_of_output)

	pedos = {}

	postvis = open(path_of_output, "r")
	for line in postvis:
		l_arr = line.split()
		pedos[l_arr[1]] = [l_arr[2], l_arr[3]]

	print(pedos.keys())

	i = 1
	while (i <= pedo_count):


		if str(i) in pedos.keys():
			#print(pedos["1"])
			#reads the dynamic element json to append easily
			with open('pedo.json', 'r') as f:
			    dynamic_element = json.load(f)
			#set target id
			dynamic_element["targetIds"] = [ 2 ]
			dynamic_element["attributes"]["id"] = i
			dynamic_element["position"]["x"] = pedos[str(i)][0]
			dynamic_element["position"]["y"] = pedos[str(i)][1]
			scenario['scenario']['topography']['dynamicElements'].append(dynamic_element)
		i = i + 1

	with open(path_of_postvis, 'w') as outfile:
	    json.dump(scenario, outfile, indent=2)



def countPedos(path_of_output):

	pedos = {}
	#finds the most recently created file and reads it line by line
	postvis = open(glob.glob(path_of_output)[-1], "r")
	for line in postvis:
		l_arr = line.split()
		pedos[l_arr[1]] = l_arr[2]

	return len(pedos.keys())-1

'''
1 pedestrians are created in the source field
2 they get out of the source field at the end of time 1
3 delete the source field
4 take their locations
5 put them locations in the same scenario and run one more time1
repeat from 3 until time is out
'''

def task4():

	max_finish_time = 40
	time = 0

	runScenario("vadere/vadere-console.jar", "practikum/Exercise 2/task5/scenarios/task5.scenario", "output")
	runScenario("vadere/vadere-console.jar", "practikum/Exercise 2/task5GNM/scenarios/task5.scenario", "outputGNM")

	while (time < max_finish_time):
		removeSourceField("practikum/Exercise 2/task5/scenarios/task5.scenario", "task5_changed.scenario")
		removeSourceField("practikum/Exercise 2/task5GNM/scenarios/task5.scenario", "task5GNM_changed.scenario")
		addPedos("task5_changed.scenario", "output/task5_*/postvis.trajectories", "task5_changed.scenario")
		addPedos("task5GNM_changed.scenario", "outputGNM/task5_*/postvis.trajectories", "task5GNM_changed.scenario")
		runScenario("vadere/vadere-console.jar", "task5_changed.scenario", "output")
		runScenario("vadere/vadere-console.jar", "task5GNM_changed.scenario", "outputGNM")

		time += 1

task4()