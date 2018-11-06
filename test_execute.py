__author__ = "Vinodkumar Kouthal"

from selenium.webdriver.support.ui import Select
from openpyxl import load_workbook
from selenium import webdriver
import logging_conf
import unittest
import logging
import time
LOGGER = logging.getLogger("L2")

DATA_PATH = "/home/vinod/automation/Learn_2/test_data.xlsx" # Excel Test Data Path
SHEET_NAME = "Test_Data" # Sheet Name

# Excel Test Data Column IDs (for openpyxl, col id starts from 1)
COL_INP_1 = 1
COL_OPER = 2
COL_INP_2 = 3
COL_EXP = 4

def super_calculator(driver, inp_1, oper, inp_2, exp_out):
	try:
		LOGGER.info("##########################################################################")

		# Enter the value in the first field
		driver.find_element_by_xpath("//input[@ng-model='first']").send_keys(inp_1)
		LOGGER.info(str("Value '" + str(inp_1) + "' is successfully inputed in input_1 field."))

		# Choose the operator from the drop down list (Select Method)
		select = Select(driver.find_element_by_xpath("//select[@ng-model='operator']"))
		select.select_by_visible_text(oper)
		LOGGER.info(str("Operation '" + str(oper) + "' is selected."))

		# Enter the value in the second field
		driver.find_element_by_xpath("//input[@ng-model='second']").send_keys(inp_2)
		LOGGER.info(str("Value '" + str(inp_2) + "'' is successfully inputed in input_2 field."))

		# Click on the 'Go' button
		driver.find_element_by_xpath("//button[@id='gobutton']").click()
		LOGGER.info("Click on 'Go' button.")

		time.sleep(5) # Waiting for the output to be shown. 
		super_calculator_output = driver.find_element_by_xpath("//h2[@class='ng-binding']").text # retrieve the output text
		LOGGER.info(str("Expected Value: " + str(exp_out) + " | Actual Value: " + str(super_calculator_output)))
		
		# Compare the expected and actual value to pass or fail a test case.
		if int(super_calculator_output) == exp_out:
			LOGGER.info("PASS: Value matches!")
			return True
		else:
			LOGGER.info("FAIL: Value doesn't match!")
			return False
	except Exception as e: ## In case of any exception occur during try block execution
		LOGGER.debug(str(e))
		return False

def make_method(driver, inp_1, oper, inp_2, exp_out):

	def test_input(self):
		self.assertTrue(super_calculator(driver, inp_1, oper, inp_2, exp_out), u'{} {} {} != {} is NOT MATCH.'.format(inp_1, oper, inp_2, exp_out))

	test_input.__name__ = 'test_super_calculator_{}{}{}'.format(inp_1, oper, inp_2)
	
	return test_input

def add_methods(inputs):
	""" Take a TestCase and add a test method for each input """
	def decorator(klass):
		
		for inps in inputs:
			test_input = make_method(inps[0], inps[1], inps[2], inps[3], inps[4])
			setattr(klass, test_input.__name__, test_input)
		
		return klass

	return decorator

def get_inputs():

	driver = webdriver.Chrome()
	driver.get("https://juliemr.github.io/protractor-demo/")
	driver.maximize_window()
	driver.implicitly_wait(10)
	assert 'Super Calculator' == driver.title

	work_book = load_workbook(DATA_PATH)
	work_sheet = work_book[SHEET_NAME]
	tot_inputs = len(list(work_sheet.columns)[0])
	LOGGER.info(str("Total no. of test case: " + str(tot_inputs - 1)))

	input_query = []
	for row_no in range(2, tot_inputs + 1):
		individual_input = []
		
		individual_input.append(driver)
		individual_input.append(work_sheet.cell(row=row_no, column=COL_INP_1).value)
		individual_input.append(work_sheet.cell(row=row_no, column=COL_OPER).value)
		individual_input.append(work_sheet.cell(row=row_no, column=COL_INP_2).value)
		individual_input.append(work_sheet.cell(row=row_no, column=COL_EXP).value)
		
		input_query.append(individual_input)

	LOGGER.info(str(input_query))
	return input_query

@add_methods(get_inputs())
class TestSuperCalculator(unittest.TestCase):
	pass
