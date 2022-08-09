#import jsonl file
import srsly

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import signal
import time
from selenium.common.exceptions import UnexpectedAlertPresentException

import prodigy

#import threading
import multiprocessing

#os.system('export PRODIGY_HOST="0.0.0.0"')
os.system('export PRODIGY_PORT=8081')

#set up browser options
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
d = webdriver.Chrome(chrome_options=chrome_options)


def serve_prodigy(datasetName, annotatorName, annotatorJsonl):
		#	prodigy.serve("rel.manual "+dataset_name+"-"+annotator_name+" en_core_web_md ./root/"+annotator_jsonl+" --label Contributes_To,Concept_Member,Same_As --span-label base,type_of,change_direction,aspect_changing,to_whom,effect_size,confidence,where,when,predicate --wrap")
		prodigy.serve("rel.manual "+datasetName+"-"+annotatorName+" en_core_web_md ./"+annotatorJsonl+" --label Contributes_To,Concept_Member,Same_As --span-label base,type_of,change_direction,aspect_changing,to_whom,effect_size,confidence,where,when,predicate --wrap")
		#os.system("prodigy rel.manual "+datasetName+"-"+annotatorName+" en_core_web_md ./"+annotatorJsonl+" --label Contributes_To,Concept_Member,Same_As --span-label base,type_of,change_direction,aspect_changing,to_whom,effect_size,confidence,where,when,predicate --wrap")

def take_screenshots(annotatorName, sentencePositions):
		#print("Annotator: "+annotatorName)
		#os.makedirs(os.path.join("screenshots", annotator))

		refresh_with_alert(d)
		url = "http://localhost:8081/"
		#url = "http:127.0.0.1:8081/"
		d.get(url)

		d.set_window_size(800, 1200)
		time.sleep(2)

		#take and name screenshots appropriately
		for sentence_position in sentencePositions:
			screenshot_file_name = annotatorName+"_sentence_"+str(sentence_position)+".png"
			
			#print(screenshot_file_name)

			#while True:
			try:
				if(d.find_element("xpath", "//div[@class='c01116']")):
					break
			except UnexpectedAlertPresentException as u:
				alert = d.switch_to.alert
				alert.accept()
			except Exception as e:
				next_btn = d.find_element("xpath", "//button[@class='prodigy-button-accept c01125 c01126']")
				screenshot_file_path = os.path.join("./root/screenshots", screenshot_file_name)
				d.save_screenshot(screenshot_file_path)
				next_btn.click()
				time.sleep(2)

		d.quit()



#os.environ[var] = val

# while switching urls to a different session_id, chrome sends a "Reload Page"
# warning, and this function helps with accepting that alert box and moving forward
def refresh_with_alert(driver):
    try:
        driver.refresh()
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        driver.switch_to.alert.accept()
    except TimeoutException as t:
        #print("No alert was present.")
        pass


def screenshots():
	master_annotation_file = "./root/checkin_four_all_labels_download.096f6496-127f-4543-b5bc-8318659f2413_corrected.jsonl" 
	input_jsonl = srsly.read_jsonl(master_annotation_file)

	dataset_name = "checkin_four_all_labels_screenshots"

	session_prefix = "checkin_four_all_labels-"
	#stream through the answers just once
	#make a dictionary with keys that are each annotator and values that are a list of the jsonl responses from that annotator.
	#check to see if the annotator has been seen before, if not, then start a new key-value pairing for that annotator
	#make another dictionary like above but listing the sentence position (order) for each annotators response 
	responses_jsonl_dict={}
	responses_position_dict={}

	for response in input_jsonl:
		session_id = response["_session_id"]
		annotator = session_id.replace(session_prefix,"")

		position = response["order"]
		document_index = response["document_index"]
		sentence_index = response["md_sentence_index"]

		if annotator in responses_jsonl_dict:
			responses_jsonl_dict[annotator].append(response)
		else:
			responses_jsonl_dict[annotator]=[response]

		if annotator in responses_position_dict:
			responses_position_dict[annotator].append(position)
		else:
			responses_position_dict[annotator]=[position]

	#after dictionary is made, then get list of all the keys (make a list of all the annotators) 
	annotators = list(responses_jsonl_dict.keys())

	#for each annotator in the list of annotators, output a jsonl file of their answers (making sure the order of their responses stays the same as the order in both the response dictionary and the position dictionary) (i.e. don't change the order!)
	#ensure the files are saved someplace accessible in the docker container (i.e. somewhere in the current working directory)
	#make a list of the file name saved as for each annotator
	file_names = []
	for annotator in annotators:
		responses = responses_jsonl_dict[annotator]
		file_name = "./root/responses_"+annotator+".jsonl"
		srsly.write_jsonl(file_name, responses)
		file_names.append(file_name)


	#zip into a list of lists, with each list containing the following 3 elements: the annotator name, the annotation file jsonl name, and list of sentence positions in the same order as is associated with the subsetted jsonl file
	#screenshot_queue = []
	#for annotator in annotators:

	sentence_positions_list = [responses_position_dict[annotator] for annotator in annotators]
	screenshot_queue = list(zip(annotators, file_names, sentence_positions_list))

	#then stream through each item in screenshot_queue (each annotator) and take screenshots of each annotator's responses and for the saved file, title each one to include the name of the annotator and the sentence position number 
	#(later might also want separate screenshots labeled based on the annotator and the sentence id) 

	os.makedirs("./root/screenshots")#os.path.join("screenshots",annotator_name))

	for annotator_name,annotator_jsonl,sentence_positions in screenshot_queue:
		#run prodigy in 1 process
		#run screenshots in another process

		prodigy_worker = multiprocessing.Process(target=serve_prodigy, args=(dataset_name, annotator_name, annotator_jsonl))
		selenium_worker = multiprocessing.Process(target=take_screenshots, args=(take_screenshots, sentence_positions))

		# starting thread 1 (prodigy thread)
		prodigy_worker.start()
		# starting thread 2 (selenium thread)
		selenium_worker.start()

			# wait until thread 2 (selenium) is completely executed
		selenium_worker.join()
		print(annotator_name+"'s selenium worker process done!")
		# wait until thread 1 (prodigy) is completely executed
		prodigy_worker.join()
		print(annotator_name+"'s prodigy worker process done!")

		#once screenshots thread finishes, then ensure both threads are stopped 
		#then go to the next cycle in the for loop (start 2 more threads for the next annotator)



	#need to add in a check that no errors occur and if they do to notify the person running this code! Good way to check is to count all the screenshots in the end and confirm it's the same number as the sum of all the dictionary lists entries.
	number_screenshots_expected = sum([len(responses_position_dict[x]) for x in responses_position_dict if isinstance(responses_position_dict[x], list)])




if __name__=="__main__":
    screenshots()
    print("Done!")



	#	prodigy.serve("rel.manual "+dataset_name+"-"+annotator_name+" en_core_web_md ./root/"+annotator_jsonl+" --label Contributes_To,Concept_Member,Same_As --span-label base,type_of,change_direction,aspect_changing,to_whom,effect_size,confidence,where,when,predicate --wrap")
		#prodigy.serve("rel.manual "+dataset_name+"-"+annotator_name+" en_core_web_md ./"+annotator_jsonl+" --label Contributes_To,Concept_Member,Same_As --span-label base,type_of,change_direction,aspect_changing,to_whom,effect_size,confidence,where,when,predicate --wrap")
		# os.system("prodigy rel.manual "+dataset_name+"-"+annotator_name+" en_core_web_md ./"+annotator_jsonl+" --label Contributes_To,Concept_Member,Same_As --span-label base,type_of,change_direction,aspect_changing,to_whom,effect_size,confidence,where,when,predicate --wrap")

		# print("Annotator: "+annotator_name)
		# #os.makedirs(os.path.join("screenshots", annotator))

		# refresh_with_alert(d)
		# url = "http://localhost:8081/"
		# #url = "http:127.0.0.1:8081/"
		# d.get(url)

		# d.set_window_size(800, 1200)
		# time.sleep(2)

		# #take and name screenshots appropriately
		# for sentence_position in sentence_positions:
		# 	screenshot_file_name = annotator_name+"_sentence_"+str(sentence_position)+".png"
			
		# 	print(screenshot_file_name)

		# 	#while True:
		# 	try:
		# 		if(d.find_element("xpath", "//div[@class='c01116']")):
		# 			break
		# 	except UnexpectedAlertPresentException as u:
		# 		alert = d.switch_to.alert
		# 		alert.accept()
		# 	except Exception as e:
		# 		next_btn = d.find_element("xpath", "//button[@class='prodigy-button-accept c01125 c01126']")
		# 		screenshot_file_path = os.path.join("./root/screenshots", screenshot_file_name)
		# 		d.save_screenshot(screenshot_file_path)
		# 		next_btn.click()
		# 		time.sleep(2)

		# d.quit()
		# #"kill $(lsof -t -i :PORT_NUMBER)"
		# #os.system("kill $(lsof -t -i :PRODIGY_PORT)")
		# #os.system("kill $(lsof -t -i :8081)")
		# os.kill(p.pid,signal.SIGINT)


