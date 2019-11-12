import json
import os
import glob

def task3():
	
	with open('practikum/Exercise 2/test6_corner/scenarios/straightline.scenario', 'r') as f:
	    scenario = json.load(f)

	scenario["scenario"]["attributesSimulation"]["finishTime"] = 300

	#reads the dynamic element json to append easily
	with open('pedo.json', 'r') as f:
	    dynamic_element = json.load(f)

	#set target id
	dynamic_element["targetIds"].append(2)
	dynamic_element["attributes"]["id"] = 0
	dynamic_element["position"]["x"] = 11.5
	dynamic_element["position"]["y"] = 53.1

	#add pedo
	scenario['scenario']['topography']['dynamicElements'].append(dynamic_element)

	with open('task3_corner.scenario', 'w') as outfile:
	    json.dump(scenario, outfile, indent=2)

	run_scenario = 'java -jar vadere/vadere-console.jar scenario-run --scenario-file "task3_corner.scenario" --output-dir="output"'
	os.system(run_scenario)

	pedos = {}
	#finds the most recently created file and reads it line by line
	postvis = open(glob.glob('output/straightline_*/postvis.trajectories')[-1], "r")
	for line in postvis:
		l_arr = line.split()
		pedos[l_arr[1]] = l_arr[0]

	for key in pedos.keys():
		print(str(key) + "  =  " + str(pedos[key]))

task3()