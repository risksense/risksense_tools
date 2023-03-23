""" *******************************************************************************************************************
|
|  Name        :  main.py
|  Description :  Ivanti Neurons ITSM Connector Ticket Creation.
|  Project     :  risksense_tools
|  Copyright   :  (c) RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

import os
import sys
from turtle import update
import toml
import json
import datetime
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'lib'))
import risksense_api as rsapi



class IvantiITSMTicketCreation:

	""" SNOWServReqTicketCreation class""" 

	def __init__(self):

		""" Main body of script """

		conf_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf', 'config.toml')
		config = self.read_config_file(conf_file)
		
		self.rs_platform = config['RS_Platform_Configuration']['platform']
		self.rs_api_key = config['RS_Platform_Configuration']['apiToken']
		self.rs_ivanti_itsm_connector = config['RS_Platform_Configuration']['ITSMConnectorName']

		#  Instantiate RiskSenseApi
		self.rs = rsapi.RiskSenseApi(self.rs_platform, self.rs_api_key)

		#  Get client id, or validate supplied client ID
		if 'clientID' not in config['RS_Platform_Configuration']:
			raise ValueError('Please provide client id in the config folder')
		else:
			client_id = config['RS_Platform_Configuration']['clientID']
			try:
				self.validate_client_id(client_id)
			except ValueError:
				print(f"Unable to validate that you belong to client ID {client_id}.")
				print("Exiting.")
				sys.exit(1)

		#  Set default client ID
		self.rs.set_default_client_id(client_id)	

		# Get connector ID
		self.connectorID = None
		get_connectors_json = self.rs.connectors.paginate_connector(page_size=250)
		for connector in get_connectors_json['_embedded']['connectors']:
			if connector['type'] == "IVANTIITSM" and connector['name'] == self.rs_ivanti_itsm_connector:
				self.connectorID = connector['id']
		if self.connectorID == None:
			raise ValueError("Provided CONNECTOR NAME is not present in the RiskSense account.")

		#Select the FINDING TYPE
		finding_type = input("Enter the FINDING TYPE that you want to create a ticket for. Enter either 'Host Finding' or 'App Finding'(Beware of whitespace): ").strip().lower()
		
		if str(finding_type) == 'host finding':
			hf_filter_category_list = self.rs.host_findings.list_hostfinding_filter_fields()
			search_filters = self.get_search_filters(hf_filter_category_list,finding_type)
			print()
			print("This is the selected search filter")
			print(search_filters)
			print()
			hf_search_json = self.rs.host_findings.get_single_search_page(search_filters)
			hf_count = hf_search_json['page']['totalElements']
			if hf_count > 0:
				print(f'There are {hf_count} host findings under these search filters\n')
				ticket_form = self.get_ticket_fields(self.connectorID)
				ticket_creation_body, ticket_form = self.get_ticket_creation_body(ticket_form,self.connectorID)
				ticket_api_body = self.form_validation(ticket_creation_body, ticket_form, self.connectorID)
				tag_id = self.tag_creation()
				ticket_creation_response = self.rs.ticket.create_ticket(tag_id, ticket_api_body)
				ticket_id = ticket_creation_response['ticketId']
				ticket_tag_response = self.rs.host_findings.add_ticket_tag(search_filters,tag_id)				
				print(f"\nTicket is created. Ticket ID is '{ticket_id}'.")
		elif str(finding_type) == 'app finding':
			af_filter_category_list = self.rs.application_findings.list_applicationfinding_filter_fields()
			search_filters = self.get_search_filters(af_filter_category_list,finding_type)
			print()
			print("This is the selected search filter")
			print(search_filters)
			print()
			af_search_json = self.rs.application_findings.get_single_search_page(search_filters)
			af_count = af_search_json['page']['totalElements']
			if af_count > 0:
				print(f'There are {af_count} application findings under these search filters\n')
				ticket_form = self.get_ticket_fields(self.connectorID)
				ticket_creation_body, ticket_form = self.get_ticket_creation_body(ticket_form,self.connectorID)
				ticket_api_body = self.form_validation(ticket_creation_body, ticket_form, self.connectorID)
				tag_id = self.tag_creation()
				ticket_creation_response = self.rs.ticket.create_ticket(tag_id, ticket_api_body)
				ticket_id = ticket_creation_response['ticketId']
				ticket_tag_response = self.rs.application_findings.add_ticket_tag(search_filters,tag_id)				
				print(f"\nTicket is created. Ticket ID is '{ticket_id}'.")


	@staticmethod
	def read_config_file(filename: str) -> dict:

		"""
		Reads a TOML-formatted configuration file.

		:param filename:    Path to the TOML-formatted file to be read.
		:type  filename:    str

		:return:  Values contained in config file.
		:rtype:   dict
		"""

		try:
			data = toml.loads(open(filename).read())
			return data
		except (Exception, FileNotFoundError, toml.TomlDecodeError) as ex:
			print("Error reading configuration file.")
			print(ex)
			print()
			exit(1)

	def validate_client_id(self, submitted_client_id: int):

		"""
		Validate the supplied CLIENT_ID variable

		:param submitted_client_id:     Client ID to validate
		:type  submitted_client_id:     int

		:raises:    ValueError
		"""
		my_client_ids = []

		for client in self.rs.my_clients:
			my_client_ids.append(client['id'])

		if submitted_client_id in my_client_ids:
			pass
		else:
			raise ValueError("User not assigned to the submitted client ID.")

	def get_search_filters(self, filter_category_list: list,finding_type: str) -> list:
		search_filter = []
		user_satisfied = None
		while user_satisfied == None:
			filter_json = {
				"field":None,
				"exclusive":None,
				"operator":None,
				"orWithPrevious":False,
				"implicitFilters":[],
				"value":None
			}

			filter_category_selected_dict = self._get_filter_category(filter_category_list)
			filter_category_selected = filter_category_selected_dict[list(filter_category_selected_dict.keys())[0]]					
			filter_json['field'] = filter_category_selected
			for ind in range(len(filter_category_list)):
				if filter_category_list[ind]['uid'] == filter_category_selected:
					filter_category_index = ind
					print(filter_category_index)
					break
				
			is_or_isNot = input("\nSelect FILTER TYPE. Enter anyone 'Is' or 'Is Not'?: ").strip().lower()
			if is_or_isNot == 'is':
				filter_json['exclusive'] = False
			elif is_or_isNot == 'is not':
				filter_json['exclusive'] = True
			else:
				raise ValueError("Entered FILTER TYPE is not valid. Please enter a valid one.")
			
			print(f"\nThere are the available OPERATOR for \'{filter_category_list[filter_category_index]['name']}\' filter")
			for ind in range(len(filter_category_list[filter_category_index]['operators'])):
				print(f"Index : {ind} - Value : '{filter_category_list[filter_category_index]['operators'][ind]}'")
			operator_select_index = int(input('\nEnter the index of OPERATOR you want to select: '))
			if (operator_select_index >= len(filter_category_list[filter_category_index]['operators'])) or (operator_select_index < 0):
				raise ValueError("Entered index value of OPERATOR is not valid. Please enter a valid one.")
			operator_selected = filter_category_list[filter_category_index]['operators'][operator_select_index]
			if (operator_selected == "TRUE") or (operator_selected == "FALSE") or (operator_selected == "PRESENT") or (operator_selected == "MET_SLA") or (operator_selected == "MISSED_SLA") or (operator_selected == "WITHIN_SLA") or (operator_selected == "OVERDUE"):
				filter_json['operator'] = operator_selected
				filter_json['value'] = ""
			elif operator_selected == "IN":
				filter_json['operator'] = operator_selected
				# iterate to select values
				filter_values = self._search_suggest_multiple(filter_category_selected,finding_type)
				filter_json['value'] = filter_values
			elif (operator_selected == "EXACT") or (operator_selected == "LIKE") or (operator_selected == "WILDCARD") or (operator_selected == "LAST_X_DAYS") or (operator_selected == "BEFORE") or (operator_selected == "AFTER") or (operator_selected == "GREATER") or (operator_selected == "LESSER"):
				filter_json['operator'] = operator_selected
				# only one value
				filter_values = self._search_suggest_single(filter_category_selected,finding_type)
				filter_json['value'] = filter_values
			elif operator_selected == "RANGE":
				filter_json['operator'] = operator_selected
				# 2 value must
				filter_values = self._search_suggest_two(filter_category_selected,finding_type)
				filter_json['value'] = filter_values			
			else:
				raise NotImplementedError(f"Logic not implemented for the OPERATOR - {operator_selected}")

			search_filter.append(filter_json)
			another_iteration = input("\nDo you want to add another filter? Enter 'yes' or 'no': ").strip().lower()
			if another_iteration == 'no':
				user_satisfied = True
			elif another_iteration == 'yes':
				pass
			else:
				raise ValueError("Entered value is not valid. Please enter a valid one.")


		return search_filter

	def _get_filter_category(self, filter_category_list):
		filter_category_dict = {}
		sample_list = []
		count = 1
		for ind in range(len(filter_category_list)):
			filter_category_dict[filter_category_list[ind]['name']] = filter_category_list[ind]['uid']

		for key,value in filter_category_dict.items():
			if count <= 10:
				sample_list.append({key : value})
			count = count + 1
		print('\nHere are some available FILTER CATEGORY sample for this finding page')	
		for ind in range(len(sample_list)):
			print(f"Index : {ind} - Value : '{list(sample_list[ind].keys())[0]}'")	
		filter_category_index = input("\nEnter the index of FILTER CATEGORY you want to select. If the filter category that you are looking for is not displayed in the terminal, please enter 'no': ").strip().lower()
		if filter_category_index == 'no':
			user_satisfied = None
			while user_satisfied == None:
				search_pattern_match = []
				search_string = input("\nEnter the search string for FILTER CATEGORY: ").strip().lower()
				for key,value in filter_category_dict.items():
					start_index = str(key).lower().find(search_string)
					if start_index != -1:
						search_pattern_match.append({key:value})
				if len(search_pattern_match) == 0:
					print("\nNo FILTER CATEGORY that matches the search string. Search again!")
				else:
					print("\nHere are the available FILTER CATEGORY that matches the search string")
					for ind in range(len(search_pattern_match)):
						print(f"Index : {ind} - Value : '{list(search_pattern_match[ind].keys())[0]}'")
					filter_category_index = input("\nEnter the index of FILTER CATEGORY you want to select. If the filter category that you are looking for is not displayed in the terminal, please enter 'no': ").strip().lower()		
					if filter_category_index == 'no':
						pass
					elif filter_category_index.isdigit() == True:
						if (int(filter_category_index) < 0) and (int(filter_category_index) >= len(search_pattern_match)):
							raise ValueError("Entered value for FILTER CATEGORY is not valid. Please enter a valid one.")
						filter_category = search_pattern_match[int(filter_category_index)]
						user_satisfied = True
					else:
						raise ValueError("Entered value of FILTER CATEGORY is not valid. Please enter a valid one.")

		elif filter_category_index.isdigit() == True:
			if (int(filter_category_index) < 0) and (int(filter_category_index) >= len(sample_list)):
				raise ValueError("Entered value for FILTER CATEGORY is not valid. Please enter a valid one.")
			filter_category = sample_list[int(filter_category_index)]
		else:
			raise ValueError("Entered value of FILTER CATEGORY is not valid. Please enter a valid one.")
		
		return filter_category
			
	def _search_suggest_multiple(self, filter_category_selected,finding_type):
		filter_value_list = []
		user_satisfied = None
		while user_satisfied == None:
			search_value = input('\nEnter the value to search in this filter. If you are not aware of search values for this filter, press ENTER to see some available values for this filter: ')
			suggest_filter = {
				'field':filter_category_selected,
				'exclusive':False,
				"operator":"WILDCARD",
				"value":search_value,
				"implicitFilters":[]
			}
			if finding_type == 'host finding':
				suggest_response_list = self.rs.host_findings.suggest([],suggest_filter)
			elif finding_type == 'app finding':
				suggest_response_list = self.rs.application_findings.suggest([],suggest_filter)				
			if len(suggest_response_list) > 0:
				for ind in range(len(suggest_response_list)):
					print(f"Index : {ind} - Value : '{suggest_response_list[ind]['key']}'")
				value_index = input("\nEnter the index of value you want to select. If multiple values have to be selected, enter the index number as comma separated values (or) Enter 'no' to again go to search for values: ").strip().lower()
				if value_index == 'no':
					continue
				elif ',' in value_index:
					entered_index_values = value_index.split(',')
					entered_index_values = [x.strip() for x in entered_index_values]
					for val in entered_index_values:
						if (val.isdigit() == False) or (int(val) < 0) or (int(val) >= len(suggest_response_list)):
							raise ValueError("Entered value is not valid. Please enter a valid one.")
					for val in entered_index_values:
						filter_value_list.append(suggest_response_list[int(val)]['key'])
				elif value_index.isdigit() == True:
					if (int(value_index) < 0) or (int(value_index) >= len(suggest_response_list)):
						raise ValueError("Entered value is not valid. Please enter a valid one.")
					value_index = int(value_index)
					filter_value_list.append(suggest_response_list[value_index]['key'])
				else:
					raise ValueError("Entered value is not valid. Please enter a valid one.")
			elif len(suggest_response_list) == 0 and search_value != '':
				print(f"No value available for the search string - '{search_value}'")
			elif len(suggest_response_list) == 0 and search_value == '':
				print(f"No value available for this filter. It may be due to current filter chaining.")				
			another_iteration = input("\nDo you want to add another value to the filter? Enter 'yes' or 'no': ").strip().lower()
			if another_iteration == 'no':
				user_satisfied = True
				
			elif another_iteration == 'yes':
				continue
			else:
				raise ValueError("Entered value is not valid. Please enter a valid one.")
		
		filter_value_string = ','.join(filter_value_list)

		return filter_value_string

	def _search_suggest_single(self, filter_category_selected,finding_type):
		filter_value_list = []
		user_satisfied = None
		while user_satisfied == None:
			search_value = input('\nEnter the value to search in this filter. If you are not aware of search values for this filter, press ENTER to see some available values for this filter: ')
			suggest_filter = {
				'field':filter_category_selected,
				'exclusive':False,
				"operator":"WILDCARD",
				"value":search_value,
				"implicitFilters":[]
			}
			if finding_type == 'host finding':
				suggest_response_list = self.rs.host_findings.suggest([],suggest_filter)
			elif finding_type == 'app finding':
				suggest_response_list = self.rs.application_findings.suggest([],suggest_filter)	
			if len(suggest_response_list) > 0:
				for ind in range(len(suggest_response_list)):
					print(f"Index : {ind} - Value : '{suggest_response_list[ind]['key']}'")
				value_index = input("\nEnter the index of value you want to select (or) Enter 'no' to again go to search for values: ").strip().lower()
				if value_index == 'no':
					continue
				elif value_index.isdigit() == True:
					if (int(value_index) < 0) or (int(value_index) >= len(suggest_response_list)):
						raise ValueError("Entered value is not valid. Please enter a valid one.")
					value_index = int(value_index)
					filter_value_list.append(suggest_response_list[value_index]['key'])
					user_satisfied = True
				else:
					raise ValueError("Entered value is not valid. Please enter a valid one.")
			elif len(suggest_response_list) == 0 and search_value != '':
				print(f"No value available for the search string - '{search_value}'")
			elif len(suggest_response_list) == 0 and search_value == '':
				print(f"No value available for this filter. It may be due to current filter chaining.")				
		
		filter_value_string = ','.join(filter_value_list)

		return filter_value_string

	def _search_suggest_two(self, filter_category_selected,finding_type):
		filter_value_list = []
		two_input = ['From', 'To']
		for field in two_input:
			user_satisfied = None
			while user_satisfied == None:
				search_value = input(f"\nEnter the value to search in this filter. If you are not aware of search values for this filter, press ENTER to see some available values for this '{field}' field : ")
				suggest_filter = {
					'field':filter_category_selected,
					'exclusive':False,
					"operator":"WILDCARD",
					"value":search_value,
					"implicitFilters":[]
				}
				if finding_type == 'host finding':
					suggest_response_list = self.rs.host_findings.suggest([],suggest_filter)
				elif finding_type == 'app finding':
					suggest_response_list = self.rs.application_findings.suggest([],suggest_filter)	
				if len(suggest_response_list) > 0:
					for ind in range(len(suggest_response_list)):
						print(f"Index : {ind} - Value : '{suggest_response_list[ind]['key']}'")
					value_index = input("\nEnter the index of value you want to select (or) Enter 'no' to again go to search for values: ").strip().lower()
					if value_index == 'no':
						continue
					elif value_index.isdigit() == True:
						if (int(value_index) < 0) or (int(value_index) >= len(suggest_response_list)):
							raise ValueError("Entered value is not valid. Please enter a valid one.")
						value_index = int(value_index)
						filter_value_list.append(suggest_response_list[value_index]['key'])
						user_satisfied = True
					else:
						raise ValueError("Entered value is not valid. Please enter a valid one.")
				elif len(suggest_response_list) == 0 and search_value != '':
					print(f"No value available for the search string - '{search_value}'")
				elif len(suggest_response_list) == 0 and search_value == '':
					print(f"No value available for this filter. It may be due to current filter chaining.")							
		
		filter_value_string = ','.join(filter_value_list)

		return filter_value_string

	def get_ticket_fields(self, connector_id):	
		ticketField_values_editable = []
		ticketField_values = self.rs.ticket.ivanti_itsm_fetch_ticketField_values(connector_id)
		for rec in ticketField_values['fields']:
			if rec['islocked'] == False:
				ticketField_values_editable.append(rec)
		retrieve_ticketFields = self.rs.ticket.ivanti_itsm_retrieve_ticketFields(connector_id, ticketField_values['ticketType'])
		retrieve_ticketFields['pluingInfoUsedKeys'].extend(ticketField_values['pluingInfoUsedKeys'])
		retrieve_ticketFields['ticketType'] = ticketField_values['ticketType']
		retrieve_ticketFields['slaDateFieldOptions'].extend(ticketField_values['slaDateFieldOptions'])
		retrieve_ticketFields['slaDateField'] = ticketField_values['slaDateField']
		for rec in ticketField_values_editable:
			found = False
			for rec1 in retrieve_ticketFields['formControlReqFields']:
				if rec['key'] == rec1['fieldName']:
					rec1['displayValue'] = rec['label']
					rec1['valueKey'] = rec['value']
					found = True
					break
			if found == False:
				for rec1 in retrieve_ticketFields['formControlOptionalFields']:
					if rec['key'] == rec1['fieldName']:
						rec1['displayValue'] = rec['label']
						rec1['valueKey'] = rec['value']
						break
	

		return retrieve_ticketFields

	def get_ticket_creation_body(self,ticket_form: dict, connector_id: int) -> dict:
		ticket_form_fields = []
		dropdown_fields_dict = {}
		ticket_form_fields_dict = {}
		dependency_field_dict = {}
		ticket_form_fields.extend(ticket_form['formControlReqFields'])
		ticket_form_fields.extend(ticket_form['formControlOptionalFields'])		
		for index,field in enumerate(ticket_form['fieldsWithValues']):
			dropdown_fields_dict[field['FieldName']] = index
			if len(field['FieldRef']) == 1:
				dependency_field_dict[field['FieldRef'][0]] = field['FieldName']
			elif len(field['FieldRef']) == 0:
				pass
			elif len(field['FieldRef']) > 1:
				raise NotImplementedError('The logic is not implement for this scenario')
		# print(dropdown_fields_dict)		
		for index,field in enumerate(ticket_form_fields):
			ticket_form_fields_dict[field['fieldName']]	 = index	

		for index, field in enumerate(ticket_form_fields):
			if 'displayValue' in field:
				print(f"\nPre-Configured value present. Field : '{field['label']}' - Value : '{field['displayValue']}'")
				if field['isPluginInfo'] == True:
					if field['fieldName'] in ticket_form['pluingInfoUsedKeys']:
						print(f"'Use Plugin Information' option is checked in for '{field['label']}' field")
					elif field['fieldName'] not in ticket_form['pluingInfoUsedKeys']:
						print(f"'Use Plugin Information' option is checked out for '{field['label']}' field")						
				pre_conf_check = input("\nDo you want to edit the value? Enter 'yes' or 'no': ").strip().lower()
				if pre_conf_check == 'yes':
					if field['label'] == 'Customer':
						fetch_available_values = self.rs.ticket.ivanti_itsm_fetch_customers(connector_id)
						print(f"\nThese are the available options available for '{field['label']}' field")
						for ind,value in enumerate(fetch_available_values):
							print(f"Index : {ind} - Value : '{value['displayName']}'")
						customer_index = int(input('\nEnter the index number of value you want to select: '))
						field['displayValue'] = fetch_available_values[customer_index]['displayName']
						field['valueKey'] = fetch_available_values[customer_index]['RecId']
					elif field['isPluginInfo'] == True:
						if field['fieldName'] in ticket_form['pluingInfoUsedKeys']:
							print(f"\n'Use Plugin Information' option is checked out for '{field['label']}' field")
							checkbox_field_input = input(f"Enter the value for '{field['label']}' field: ").strip()
							ticket_form['pluingInfoUsedKeys'].remove(field['fieldName'])
							field['displayValue'] = checkbox_field_input
							field['valueKey'] = checkbox_field_input
						elif field['fieldName'] not in ticket_form['pluingInfoUsedKeys']:
							print(f"\n'Use Plugin Information' option is checked in for '{field['label']}' field")
							ticket_form['pluingInfoUsedKeys'].append(field['fieldName'])
							field['displayValue'] = 'Summary will be updated shortly.'
							field['valueKey'] = 'Summary will be updated shortly.'
					elif field['type'] == 'Text':
						text_field_input = input(f"Enter the value for '{field['label']}' field: ").strip()
						field['displayValue'] = text_field_input
						field['valueKey'] = text_field_input						
					elif field['type'] == 'DropDown':
						dropdown_check = input("\nDo you want to delete the value or change the value? Enter either 'delete' for removing pre-configured value or 'change' for changing pre-configured value: ").strip().lower()
						if dropdown_check == 'delete':
							del field['displayValue']
							del field['valueKey']
							if field['fieldName'] in dependency_field_dict:
								dependent_field_name = dependency_field_dict[field['fieldName']]
								dependent_field_dict = ticket_form_fields[ticket_form_fields_dict[dependent_field_name]]
								if 'displayValue' in dependent_field_dict:
									del dependent_field_dict['displayValue']
									del dependent_field_dict['valueKey']
								print(field)
								print(dependent_field_dict)
						elif dropdown_check == 'change':
							field = self._get_dropdown_values(ticket_form,dropdown_fields_dict,field,ticket_form_fields,ticket_form_fields_dict,connector_id)
						else:
							raise ValueError("Entered value is not valid. Please enter a valid one.")
					elif field['type'] == 'DateTime':
						dropdown_check = input("\nDo you want to delete the value or change the value? Enter either 'delete' for removing pre-configured value or 'change' for changing pre-configured value: ").strip().lower()
						if dropdown_check == 'delete':
							del field['displayValue']
							del field['valueKey']	
						elif dropdown_check == 'change':					
							date_time_input = input(f"\nEnter the dataTime value for '{field['label']}' field. It should be in 'yyyy-mm-ddThh:mm:ss' format: ").strip()
							timezone_input = input(f"\nEnter the TIMEZONE value for '{field['label']}' field. It should be in '+hh:mm' or '-hh:mm' format: ").strip()
							date_time_input_string = f'{date_time_input}{timezone_input}'
							try:
								date_time_input_validated = str(datetime.datetime.strptime(date_time_input_string, '%Y-%m-%dT%H:%M:%S%z'))
							except ValueError as ex:
								print(ex)
							field['displayValue'] = date_time_input_validated
							field['valueKey'] = date_time_input_validated	
						else:
							raise ValueError("Entered value is not valid. Please enter a valid one.")						
					elif field['label'] == 'ReleaseLink':
						dropdown_check = input("\nDo you want to delete the value or change the value? Enter either 'delete' for removing pre-configured value or 'change' for changing pre-configured value: ").strip().lower()
						if dropdown_check == 'delete':
							del field['displayValue']
							del field['valueKey']	
						elif dropdown_check == 'change':						
							fetch_available_values = self.rs.ticket.ivanti_itsm_fetch_releaseLink(connector_id)
							print(f"\nThese are the available options available for '{field['label']}' field")
							for ind,value in enumerate(fetch_available_values):
								print(f"Index : {ind} - Value : '{value['displayName']}'")
							customer_index = int(input('\nEnter the index number of value you want to select: '))
							field['displayValue'] = fetch_available_values[customer_index]['displayName']
							field['valueKey'] = fetch_available_values[customer_index]['RecId']	
						else:
							raise ValueError("Entered value is not valid. Please enter a valid one.")										
					elif field['label'] == 'Requestor Link':
						dropdown_check = input("\nDo you want to delete the value or change the value? Enter either 'delete' for removing pre-configured value or 'change' for changing pre-configured value: ").strip().lower()
						if dropdown_check == 'delete':
							del field['displayValue']
							del field['valueKey']	
						elif dropdown_check == 'change':						
							fetch_available_values = self.rs.ticket.ivanti_itsm_fetch_requestorLink(connector_id)
							print(f"\nThese are the available options available for '{field['label']}' field")
							for ind,value in enumerate(fetch_available_values):
								print(f"Index : {ind} - Value : '{value['displayName']}'")
							customer_index = int(input('\nEnter the index number of value you want to select: '))
							field['displayValue'] = fetch_available_values[customer_index]['displayName']
							field['valueKey'] = fetch_available_values[customer_index]['RecId']		
						else:
							raise ValueError("Entered value is not valid. Please enter a valid one.")																	
					else:
						raise NotImplementedError('The logic is not implement for this scenario')
				elif pre_conf_check == 'no':
					pass
				else:
					raise ValueError("Entered value is not valid. Please enter a valid one.")
			else:
				enter_value_check = input(f"\nDo you want to enter a value for '{field['label']}' field? Enter 'yes' or 'no': ").strip().lower()
				if enter_value_check == 'yes':
					if field['label'] == 'Customer':
						fetch_available_values = self.rs.ticket.ivanti_itsm_fetch_customers(connector_id)
						print(f"\nThese are the available options available for '{field['label']}' field")
						for ind,value in enumerate(fetch_available_values):
							print(f"Index : {ind} - Value : '{value['displayName']}'")
						customer_index = int(input('\nEnter the index number of value you want to select: '))
						field['displayValue'] = fetch_available_values[customer_index]['displayName']
						field['valueKey'] = fetch_available_values[customer_index]['RecId']
					elif field['isPluginInfo'] == True:
						if field['fieldName'] in ticket_form['pluingInfoUsedKeys']:
							print(f"\n'Use Plugin Information' option is checked out for '{field['label']}' field")
							checkbox_field_input = input(f"Enter the value for '{field['label']}' field: ").strip()
							ticket_form['pluingInfoUsedKeys'].remove(field['fieldName'])
							field['displayValue'] = checkbox_field_input
							field['valueKey'] = checkbox_field_input
						elif field['fieldName'] not in ticket_form['pluingInfoUsedKeys']:
							print(f"\n'Use Plugin Information' option is checked in for '{field['label']}' field")
							ticket_form['pluingInfoUsedKeys'].append(field['fieldName'])
							field['displayValue'] = 'Summary will be updated shortly.'
							field['valueKey'] = 'Summary will be updated shortly.'
					elif field['type'] == 'Text':
						text_field_input = input(f"Enter the value for '{field['label']}' field: ").strip()
						field['displayValue'] = text_field_input
						field['valueKey'] = text_field_input						
					elif field['type'] == 'DropDown':
						field = self._get_dropdown_values(ticket_form,dropdown_fields_dict,field,ticket_form_fields,ticket_form_fields_dict,connector_id)
					elif field['type'] == 'DateTime':
						date_time_input = input(f"\nEnter the dataTime value for '{field['label']}' field. It should be in 'yyyy-mm-ddThh:mm:ss' format: ").strip()
						timezone_input = input(f"\nEnter the TIMEZONE value for '{field['label']}' field. It should be in '+hh:mm' or '-hh:mm' format: ").strip()
						date_time_input_string = f'{date_time_input}{timezone_input}'
						try:
							date_time_input_validated = str(datetime.datetime.strptime(date_time_input_string, '%Y-%m-%dT%H:%M:%S%z'))
						except ValueError as ex:
							print(ex)
						field['displayValue'] = date_time_input_validated
						field['valueKey'] = date_time_input_validated	
					elif field['label'] == 'ReleaseLink':
						fetch_available_values = self.rs.ticket.ivanti_itsm_fetch_releaseLink(connector_id)
						print(f"\nThese are the available options available for '{field['label']}' field")
						for ind,value in enumerate(fetch_available_values):
							print(f"Index : {ind} - Value : '{value['displayName']}'")
						customer_index = int(input('\nEnter the index number of value you want to select: '))
						field['displayValue'] = fetch_available_values[customer_index]['displayName']
						field['valueKey'] = fetch_available_values[customer_index]['RecId']			
					elif field['label'] == 'Requestor Link':
						fetch_available_values = self.rs.ticket.ivanti_itsm_fetch_requestorLink(connector_id)
						print(f"\nThese are the available options available for '{field['label']}' field")
						for ind,value in enumerate(fetch_available_values):
							print(f"Index : {ind} - Value : '{value['displayName']}'")
						customer_index = int(input('\nEnter the index number of value you want to select: '))
						field['displayValue'] = fetch_available_values[customer_index]['displayName']
						field['valueKey'] = fetch_available_values[customer_index]['RecId']											
					else:
						raise NotImplementedError('The logic is not implement for this scenario')
				elif enter_value_check == 'no':
					pass
				else:
					raise ValueError("Entered value is not valid. Please enter a valid one.")		

		if len(ticket_form['slaDateFieldOptions']) > 0:	
			print('\nThese are the available JIRA fields that can be selected for mapping with the RiskSense SLA date')
			for ind in range(len(ticket_form['slaDateFieldOptions'])):
				print(f"Index : {ind} - Value : '{ticket_form['slaDateFieldOptions'][ind]['displayValue']}'")
			sla_dropdown_index = int(input('Enter the index of value you want to select: '))
			if sla_dropdown_index < 0 or sla_dropdown_index >= len(ticket_form['slaDateFieldOptions']):
				raise ValueError("Entered value is not valid. Please enter a valid one.")		
			ticket_form['slaDateField'] = (ticket_form['slaDateFieldOptions'][sla_dropdown_index]['value'])

		return ticket_form_fields, ticket_form

	def _get_dropdown_values(self, ticket_form, dropdown_fields_dict, field, ticket_form_fields, ticket_form_fields_dict, connector_id):
		available_option_records = ticket_form['fieldsWithValues'][dropdown_fields_dict[field['fieldName']]]
		if available_option_records['sameAs'] == "":
			if len(available_option_records['FieldRef']) == 0:
				if len(available_option_records['values']) == 0:
					raise NotImplementedError('The logic is not implement for this scenario')		
				else:
					print(f"\nThese are the available options available for '{field['label']}' field")
					for i,op in enumerate(available_option_records['values']):
						print(f"Index : {i} - Value : '{op['Label']}'")
					dropdown_index = int(input('\nEnter the index number of value you want to select: '))
					field['displayValue'] = available_option_records['values'][dropdown_index]['Label']
					field['valueKey'] = available_option_records['values'][dropdown_index]['value']
			elif len(available_option_records['FieldRef']) == 1:
				"""API CALL"""	
				reference_field = ticket_form_fields[ticket_form_fields_dict[available_option_records['FieldRef'][0]]]
				if 'displayValue' in reference_field:
					on_the_fly_resp = self.rs.ticket.ivanti_itsm_fetch_fieldValue_wrt_dependentField(ticket_form['ticketType'], connector_id, available_option_records['FieldName'], reference_field['fieldName'], reference_field['valueKey'])
					print(f"\nThese are the available options available for '{field['label']}' field")
					for i,op in enumerate(on_the_fly_resp):
						print(f"Index : {i} - Value : '{op['label']}'")
					on_the_fly_value_index = int(input('\nEnter the index number of value you want to select: '))
					field['displayValue'] = on_the_fly_resp[on_the_fly_value_index]['label']
					field['valueKey'] = on_the_fly_resp[on_the_fly_value_index]['value']
				else:
					if len(available_option_records['values']) == 0:
						raise NotImplementedError('The logic is not implement for this scenario')		
					else:					
						print(f"\nThese are the available options available for '{field['label']}' field")
						for i,op in enumerate(available_option_records['values']):
							print(f"Index : {i} - Value : '{op['Label']}'")
						dropdown_index = int(input('\nEnter the index number of value you want to select: '))
						field['displayValue'] = available_option_records['values'][dropdown_index]['Label']
						field['valueKey'] = available_option_records['values'][dropdown_index]['value']
			else:
				raise NotImplementedError('The logic is not implement for this scenario')
		elif available_option_records['sameAs'] != "":
			if len(available_option_records['FieldRef']) == 0:
				if len(available_option_records['values']) == 0:
					raise NotImplementedError('The logic is not implement for this scenario')		
				else:
					print(f"\nThese are the available options available for '{field['label']}' field")
					for i,op in enumerate(available_option_records['values']):
						print(f"Index : {i} - Value : '{op['Label']}'")
					dropdown_index = int(input('\nEnter the index number of value you want to select: '))
					field['displayValue'] = available_option_records['values'][dropdown_index]['Label']
					field['valueKey'] = available_option_records['values'][dropdown_index]['value']
			elif len(available_option_records['FieldRef']) == 1:
				"""API CALL"""		
				reference_field = ticket_form_fields[ticket_form_fields_dict[available_option_records['FieldRef'][0]]]
				if 'displayValue' in reference_field:
					on_the_fly_resp = self.rs.ticket.ivanti_itsm_fetch_fieldValue_wrt_dependentField(ticket_form['ticketType'], connector_id, available_option_records['FieldName'], reference_field['fieldName'], reference_field['valueKey'])
					print(f"\nThese are the available options available for '{field['label']}' field")
					for i,op in enumerate(on_the_fly_resp):
						print(f"Index : {i} - Value : '{op['label']}'")
					on_the_fly_value_index = int(input('\nEnter the index number of value you want to select: '))
					field['displayValue'] = on_the_fly_resp[on_the_fly_value_index]['label']
					field['valueKey'] = on_the_fly_resp[on_the_fly_value_index]['value']
				else:
					sameAs_field_dict = ticket_form_fields[ticket_form_fields_dict[available_option_records['sameAs']]]
					sameAs_field_option_dict = ticket_form['fieldsWithValues'][dropdown_fields_dict[sameAs_field_dict['fieldName']]]
					if len(sameAs_field_option_dict['FieldRef']) == 0:
						if len(sameAs_field_option_dict['values']) == 0:
							raise NotImplementedError('The logic is not implement for this scenario')
						else:				
							print(f"\nThese are the available options available for '{field['label']}' field")
							for i,op in enumerate(sameAs_field_option_dict['values']):
								print(f"Index : {i} - Value : '{op['Label']}'")
							dropdown_index = int(input('\nEnter the index number of value you want to select: '))
							field['displayValue'] = sameAs_field_option_dict['values'][dropdown_index]['Label']
							field['valueKey'] = sameAs_field_option_dict['values'][dropdown_index]['value']
					elif  len(sameAs_field_option_dict['FieldRef']) == 1:
						sameAs_dependent_field_name = sameAs_field_option_dict['FieldRef'][0]
						sameAs_dependent_field_dict = ticket_form_fields[ticket_form_fields_dict[sameAs_dependent_field_name]]
						if 'displayValue' in sameAs_dependent_field_dict:
							on_the_fly_resp = self.rs.ticket.ivanti_itsm_fetch_fieldValue_wrt_dependentField(ticket_form['ticketType'], connector_id, sameAs_field_dict['fieldName'], sameAs_dependent_field_name, sameAs_dependent_field_dict['valueKey'])
							print(f"\nThese are the available options available for '{field['label']}' field")
							for i,op in enumerate(on_the_fly_resp):
								print(f"Index : {i} - Value : '{op['label']}'")
							on_the_fly_value_index = int(input('\nEnter the index number of value you want to select: '))
							field['displayValue'] = on_the_fly_resp[on_the_fly_value_index]['label']
							field['valueKey'] = on_the_fly_resp[on_the_fly_value_index]['value']
						else:
							if len(sameAs_field_option_dict['values']) == 0:
								raise NotImplementedError('The logic is not implement for this scenario')
							else:				
								print(f"\nThese are the available options available for '{field['label']}' field")
								for i,op in enumerate(sameAs_field_option_dict['values']):
									print(f"Index : {i} - Value : '{op['Label']}'")
								dropdown_index = int(input('\nEnter the index number of value you want to select: '))
								field['displayValue'] = sameAs_field_option_dict['values'][dropdown_index]['Label']
								field['valueKey'] = sameAs_field_option_dict['values'][dropdown_index]['value']
					elif len(sameAs_field_option_dict['FieldRef']) > 1:
						raise NotImplementedError('The logic is not implement for this scenario')

					
			else:
				raise NotImplementedError('The logic is not implement for this scenario')

		return field

	def form_validation(self, ticket_creation_body, ticket_form, connector_id):
		body = {"type":"IVANTIITSM","ticketType":ticket_form['ticketType'],"connectorId":connector_id,"updatedValuesByUserList":[], "defaultValuefieldsList":[]}
		ticket_api_body = {"connectorId":connector_id,"templateId":"none","fields":[],"type":"IVANTIITSM","usePluginInfoFields":[],"slaDateField":"","publishTicketStats":False}
		for index, field in enumerate(ticket_creation_body):
			if 'valueKey' in field:
				body_dict = {"displayName":field['fieldName'],"name":field['fieldName'],"dirty":True,"fieldId":field['fieldName'],"value":field['valueKey']}
				body['updatedValuesByUserList'].append(body_dict)
		for index, field in enumerate(ticket_form['defaultFieldValues']):
			body_dict = {"displayName":field['key'],"name":field['key'],"dirty":True,"fieldId":field['key'],"value":field['label']}
			body['defaultValuefieldsList'].append(body_dict)
		response = self.rs.ticket.ivanti_itsm_fetch_validation(body)

		if response['isValid'] == False:
			print("\n\n---Form Validation Failed---\n\n")
			print(response)
			print("Please run the script again and rectify the mistakes mentioned in the above error message")
			sys.exit(0)
		elif response['isValid'] == True:
			ticket_api_body['usePluginInfoFields'].extend(ticket_form['pluingInfoUsedKeys'])
			ticket_api_body['slaDateField'] = ticket_form['slaDateField']
			ticket_api_body['fields'].extend(body['updatedValuesByUserList'])
		
		return ticket_api_body

	def tag_creation(self) -> int:
		available_tag_types = ['COMPLIANCE', 'LOCATION', 'CUSTOM', 'REMEDIATION', 'PEOPLE', 'PROJECT', 'SCANNER', 'CMDB']
		print("\nThese are the available TAG TYPES")
		for ind in range(len(available_tag_types)):
			print(f"Index : {ind} - Value : '{available_tag_types[ind]}'")
		selected_tag_type_index = int(input('\nEnter the index number of TAG TYPE that you want to select: '))
		if (int(selected_tag_type_index) < 0) or (int(selected_tag_type_index) >= len(available_tag_types)):
			raise ValueError("Entered value is not valid. Please enter a valid one.")		
		selected_tag_type = available_tag_types[selected_tag_type_index]
		time_obj = datetime.datetime.now()
		time_obj = time_obj.strftime('%Y-%m-%d T%H-%M-%S')
		tag_name = f"Ivanti Neurons ITSM Ticket Creation {str(time_obj)}"
		description = "created by JIRA Ticket Creation script"
		user_json = self.rs.users.get_my_profile()
		user_id = user_json['userId']
		tag_id = self.rs.tags.create(selected_tag_type,tag_name,description,user_id)
		print(f"\nTag is created - {tag_name}")

		return tag_id











#  Execute the script
if __name__ == "__main__":
    try:
        IvantiITSMTicketCreation()
    except KeyboardInterrupt:
        print()
        print("KeyboardInterrupt detected.  Exiting...")
        print()
        sys.exit(0)