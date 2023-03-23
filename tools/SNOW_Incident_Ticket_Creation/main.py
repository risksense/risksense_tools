""" *******************************************************************************************************************
|
|  Name        :  main.py
|  Description :  ServiceNow Incident Connector Ticket Creation.
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



class SNOWIncTicketCreation:

	""" SNOWIncTicketCreation class""" 

	def __init__(self):

		""" Main body of script """

		conf_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf', 'config.toml')
		config = self.read_config_file(conf_file)
		
		self.rs_platform = config['RS_Platform_Configuration']['platform']
		self.rs_api_key = config['RS_Platform_Configuration']['apiToken']
		self.rs_snow_incident_connector = config['RS_Platform_Configuration']['SNOWConnectorName']

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
			if connector['type'] == "SERVICE_NOW" and connector['name'] == self.rs_snow_incident_connector:
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
				selected_template = self.select_template(self.connectorID)
				ticket_form = self.rs.ticket.getfieldsfromtemplateid(self.connectorID,selected_template['id'])

				ticket_creation_body = self.get_ticket_creation_body(ticket_form,self.connectorID,selected_template['id'])
				tag_id = self.tag_creation()
				ticket_creation_response = self.rs.ticket.create_ticket(tag_id, ticket_creation_body)
				ticket_id = ticket_creation_response['ticketId']
				ticket_tag_response = self.rs.host_findings.add_ticket_tag(search_filters,tag_id)
				print(f"\nTicket is created. Ticket ID is '{ticket_id}'.")
			elif hf_count == 0:
				print('No Host Findings available for the above search filters')	
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
				selected_template = self.select_template(self.connectorID)
				ticket_form = self.rs.ticket.getfieldsfromtemplateid(self.connectorID,selected_template['id'])

				ticket_creation_body = self.get_ticket_creation_body(ticket_form,self.connectorID,selected_template['id'])
				tag_id = self.tag_creation()
				ticket_creation_response = self.rs.ticket.create_ticket(tag_id, ticket_creation_body)
				ticket_id = ticket_creation_response['ticketId']
				ticket_tag_response = self.rs.application_findings.add_ticket_tag(search_filters,tag_id)
				print(f"\nTicket is created. Ticket ID is '{ticket_id}'.")
			elif af_count == 0:
				print('No Application Findings available for the above search filters')			
		else:
			raise ValueError("Entered FINDING TYPE is not valid. Please enter a valid one.")

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
				
			is_or_isNot = input("\nSelect FILTER TYPE. Enter anyone 'Is' or 'Is Not'? ").strip().lower()
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
		tag_name = f"SNOW Incident Ticket Creation {str(time_obj)}"
		description = "created by JIRA Ticket Creation script"
		user_json = self.rs.users.get_my_profile()
		user_id = user_json['userId']
		tag_id = self.rs.tags.create(selected_tag_type,tag_name,description,user_id)
		print(f"\nTag is created - {tag_name}")

		return tag_id

	def select_template(self,connector_id: int) -> dict:
		default_template = ""
		template_json = self.rs.ticket.gettemplateid(connector_id)
		for template in template_json['templates']:
			if template['isDefault'] == True:
				default_template = template
				break
		if default_template == "":
			print("\nThere is no DEFAULT TEMPLATE selected in the connector configuration.")
			print("\nThese are the available TEMPLATES available for this connector")
			for ind in range(len(template_json['templates'])):
				print(f"Index : {ind} - Value : '{template_json['templates'][ind]['label']}'")
			template_index = int(input("\nEnter the index number of TEMPLATE you want to select: "))
			default_template = template_json['templates'][template_index]
		
		return default_template

	def get_ticket_creation_body(self,ticket_form: dict, connector_id: int, template_id: str) -> dict:
		required_field_list = []
		optional_field_list = []
		optional_field_value_index_list = []
		ticket_api_body = {"connectorId":connector_id,"templateId":template_id,"fields":[],"type":"SERVICE_NOW","slaDateField":"","usePluginInfoFields":[],"publishTicketStats":False}
		for field in ticket_form['fields']:
			if field['isSupported'] == True and field['locked'] == False:
				if field['required'] == True:
					required_field_list.append(field)
				elif field['required'] == False:
					optional_field_list.append(field)
		# print(required_field_list)
		# print(optional_field_list)	
		ticket_api_body = self._required_fields_ticket_form(required_field_list,ticket_api_body,connector_id)
		print(ticket_api_body)

		print("\nThese are the available OPTIONAL FIELDS in the ticket form")
		for ind in range(len(optional_field_list)):
			print(f"Index : {ind} - Value : '{optional_field_list[ind]['label']}'")
		optional_field_value_index = input("Enter the index number of OPTIONAL FIELDS that you want to work with. If multiple values have to be selected, enter the index number as comma separated values (or) Enter 'no' if you do not want to work with any optional fields: ").strip().lower()
		if optional_field_value_index == 'no':
			pass
		elif ',' in optional_field_value_index:
			entered_index_values = optional_field_value_index.split(',')
			entered_index_values = [x.strip() for x in entered_index_values]
			for val in entered_index_values:
				if (val.isdigit() == False) or (int(val) < 0) or (int(val) >= len(optional_field_list)):
					raise ValueError("Entered value is not valid. Please enter a valid one.")		
			for val in entered_index_values:
				optional_field_value_index_list.append(int(val))
		elif optional_field_value_index.isdigit() == True:
			if (int(optional_field_value_index) < 0) or (int(optional_field_value_index) >= len(optional_field_list)):
				raise ValueError("Entered value is not valid. Please enter a valid one.")
			optional_field_value_index_list.append(int(optional_field_value_index))
		else:
			raise ValueError("Entered value for OPTIONAL FIELDS selection is not valid. Please enter a valid one.")

		ticket_api_body = self._optional_fields_ticket_form(optional_field_value_index_list,optional_field_list,connector_id,ticket_api_body)

		if len(ticket_form['slaDateFieldOptions']) > 0:	
			print('\nThese are the available Service Now fields that can be selected for mapping with the RiskSense SLA date')
			for ind in range(len(ticket_form['slaDateFieldOptions'])):
				print(f"Index : {ind} - Value : '{ticket_form['slaDateFieldOptions'][ind]['displayValue']}'")
			sla_dropdown_index = int(input('Enter the index of value you want to select: '))
			if sla_dropdown_index < 0 or sla_dropdown_index >= len(ticket_form['slaDateFieldOptions']):
				raise ValueError("Entered value is not valid. Please enter a valid one.")		
			ticket_api_body['slaDateField'] = ticket_form['slaDateFieldOptions'][sla_dropdown_index]['value']	

		return ticket_api_body

	def _required_fields_ticket_form(self, required_field_list,ticket_api_body,connector_id):
		for required_field in required_field_list:
			if required_field['type'] == 'textArea':
				if (required_field['key'] == 'short_description') or (required_field['key'] == 'description'):
					check_plugin_use = input(f"\n[Required Field] -  Are you willing to use PLUGIN INFORMATION for '{required_field['label']}' field? Enter 'yes' or 'no': ").strip().lower()
					if check_plugin_use != 'yes' and check_plugin_use != 'no':
						raise ValueError("Entered value is not valid. Please enter a valid one.")
					elif check_plugin_use == 'yes':
						ticket_api_body['usePluginInfoFields'].append(required_field['key'])
					elif check_plugin_use == 'no':
						summary_description_input = input(f"Enter the value for '{required_field['label']}' field: ")
						summary_description_dict = {'key':required_field['key'],'value':summary_description_input,'displayValue':''}
						ticket_api_body['fields'].append(summary_description_dict)
				else:
					required_field_input = input(f"\nEnter the value for '{required_field['label']}' field: ")
					required_field_dict = {'key':required_field['key'],'value':required_field_input,'displayValue':''}
					ticket_api_body['fields'].append(required_field_dict)
			elif required_field['type'] == 'dateTime':
				required_field_input = input(f"\nEnter the dateTime value for '{required_field['label']}' field. It should be in 'yyyy-mm-dd HH:MM' format: ").strip()
				try:
					required_field_input = str(datetime.datetime.strptime(required_field_input, '%Y-%m-%d %H:%M'))
				except ValueError as ex:
					print(ex)

				required_field_dict = {'key':required_field['key'],'value':required_field_input,'displayValue':''}
				ticket_api_body['fields'].append(required_field_dict)	
			elif required_field['type'] == 'string':
				required_field_input = input(f"\nEnter the value for '{required_field['label']}' field: ")
				required_field_dict = {'key':required_field['key'],'value':required_field_input,'displayValue':''}
				ticket_api_body['fields'].append(required_field_dict)		
			elif required_field['type'] == 'number':
				required_field_input = int(input(f"\nEnter a number for '{required_field['label']}' field. Supported Range '-10000 to 10000': "))
				required_field_dict = {'key':required_field['key'],'value':required_field_input,'displayValue':''}
				ticket_api_body['fields'].append(required_field_dict)					
			elif required_field['type'] == 'boolean':
				required_field_input = input(f"\nEnter either 'true' or 'false' for '{required_field['label']}' field: ").strip().lower()
				if required_field_input != 'true' and required_field_input != 'false':
					raise ValueError("Entered value is not valid. Please enter a valid one.")
				elif required_field_input == 'true':
					required_field_input = True
				elif required_field_input == 'false':
					required_field_input = False
				required_field_dict = {'key':required_field['key'],'value':required_field_input,'displayValue':''}
				ticket_api_body['fields'].append(required_field_dict)	
			elif 'queryParameters' in required_field:
				user_satisfied = None
				while user_satisfied == None:
					search_value = input(f"\nEnter the value to search for '{required_field['label']}' field. If you are not aware of search values for this filter, press ENTER to see some available values for this filter: ")
					query_parameter_body = {"queryParameters":required_field['queryParameters'],"key":required_field['key'],"connectorId":connector_id,"type":"SERVICE_NOW","query":search_value}
					query_parameter_json = self.rs.connectors.search_query_parameter(query_parameter_body)
					if len(query_parameter_json['selectOptions']) > 0:
						for ind in range(len(query_parameter_json['selectOptions'])):
							print(f"Index : {ind} - Value : '{query_parameter_json['selectOptions'][ind]['displayValue']}'")
						qp_value_index = input("Enter the index of value you want to select (or) Enter 'no' to again go to search for values: ").strip().lower()
						if qp_value_index == 'no':
							continue
						elif qp_value_index.isdigit() == True:
							if int(qp_value_index) < 0 or int(qp_value_index) >= len(query_parameter_json['selectOptions']):
								raise ValueError("Entered value is not valid. Please enter a valid one.")
							qp_dict = {'key':required_field['key'],'value':query_parameter_json['selectOptions'][int(qp_value_index)]['value'],'displayValue':query_parameter_json['selectOptions'][int(qp_value_index)]['displayValue']}	
							ticket_api_body['fields'].append(qp_dict)
							user_satisfied = True
						else:
							raise ValueError("Entered value is not valid. Please enter a valid one.")			
					else:
						print(f"No value available for the search string - '{search_value}'")					
			elif 'queryParameters' not in required_field and len(required_field['selectOptions']) > 0:
				print(f"\nThese are the available options for '{required_field['label']}' field")
				for ind in range(len(required_field['selectOptions'])):
					print(f"Index : {ind} - Value : '{required_field['selectOptions'][ind]['displayValue']}'")
				value_dropdown_index = int(input('Enter the index of value you want to select: '))
				if value_dropdown_index < 0 or value_dropdown_index >= len(required_field['selectOptions']):
					raise ValueError("Entered value is not valid. Please enter a valid one.")
				value_dropdown_dict = {'key':required_field['key'],'value':required_field['selectOptions'][value_dropdown_index]['value'],'displayValue':required_field['selectOptions'][value_dropdown_index]['displayValue']}	
				ticket_api_body['fields'].append(value_dropdown_dict)
			else:
				raise NotImplementedError(f"Logic is not implemented for this field type {required_field['type']}")		

		return ticket_api_body

	def _optional_fields_ticket_form(self,optional_field_value_index_list,optional_field_list,connector_id,ticket_api_body):
		for val in optional_field_value_index_list:
			optional_field = optional_field_list[int(val)]
			if optional_field['type'] == 'textArea':
				if optional_field['key'] != 'description' and optional_field['key'] != 'short_description':
					optional_field_input = input(f"\nEnter the value for '{optional_field['label']}' field: ")
					optional_field_dict = {'key':optional_field['key'],'value':optional_field_input,'displayValue':''}		
					ticket_api_body['fields'].append(optional_field_dict)	
				else:
					optional_field_input = input(f"\nAre you willing to use PLUGIN INFORMATION for '{optional_field['label']}' field? Enter 'yes' or 'no': ").strip().lower()
					if optional_field_input != 'yes' and optional_field_input != 'no':
						raise ValueError("Entered value is not valid. Please enter a valid one.")
					elif optional_field_input == 'yes':
						ticket_api_body['usePluginInfoFields'].append(optional_field['key'])
					elif optional_field_input == 'no':
						summary_description_field_input = input(f"Enter the value for '{optional_field['label']}' field: ")
						summary_description_field_dict = {'key':optional_field['key'],'value':summary_description_field_input,'displayValue':''}
						ticket_api_body['fields'].append(summary_description_field_dict)							 		
			elif optional_field['type'] == 'dateTime':
				optional_field_input = input(f"\nEnter the dateTime value for '{optional_field['label']}' field. It should be in 'yyyy-mm-dd HH:MM' format: ")
				try:
					optional_field_input = str(datetime.datetime.strptime(optional_field_input, '%Y-%m-%d %H:%M'))
				except ValueError as ex:
					print(ex)						
				optional_field_dict = {'key':optional_field['key'],'value':optional_field_input,'displayValue':''}		
				ticket_api_body['fields'].append(optional_field_dict)
			elif optional_field['type'] == 'string':
				optional_field_input = input(f"\nEnter the value for '{optional_field['label']}' field: ")
				optional_field_dict = {'key':optional_field['key'],'value':optional_field_input,'displayValue':''}		
				ticket_api_body['fields'].append(optional_field_dict)	
			elif optional_field['type'] == 'number':
				optional_field_input = int(input(f"\nEnter a number for '{optional_field['label']}' field. Supported Range '-10000 to 10000': "))
				optional_field_dict = {'key':optional_field['key'],'value':optional_field_input,'displayValue':''}		
				ticket_api_body['fields'].append(optional_field_dict)				
			elif optional_field['type'] == 'boolean':
				optional_field_input = input(f"\nEnter either 'true' or 'false' for '{optional_field['label']}' field: ").strip().lower()
				if optional_field_input != 'true' and optional_field_input != 'false':
					raise ValueError("Entered value is not valid. Please enter a valid one.")
				elif optional_field_input == 'true':
					optional_field_input = True
				elif optional_field_input == 'false':
					optional_field_input = False				
				optional_field_dict = {'key':optional_field['key'],'value':optional_field_input,'displayValue':''}		
				ticket_api_body['fields'].append(optional_field_dict)			
			elif 'queryParameters' in optional_field:
				user_satisfied = None
				while user_satisfied == None:
					search_value = input(f"\nEnter the value to search for '{optional_field['label']}' field. If you are not aware of search values for this filter, press ENTER to see some available values for this filter: ")
					query_parameter_body = {"queryParameters":optional_field['queryParameters'],"key":optional_field['key'],"connectorId":connector_id,"type":"SERVICE_NOW","query":search_value}
					query_parameter_json = self.rs.connectors.search_query_parameter(query_parameter_body)
					if len(query_parameter_json['selectOptions']) > 0:
						for ind in range(len(query_parameter_json['selectOptions'])):
							print(f"Index : {ind} - Value : '{query_parameter_json['selectOptions'][ind]['displayValue']}'")
						qp_value_index = input("Enter the index of value you want to select (or) Enter 'no' to again go to search for values: ").strip().lower()
						if qp_value_index == 'no':
							continue
						elif qp_value_index.isdigit() == True:
							if int(qp_value_index) < 0 or int(qp_value_index) >= len(query_parameter_json['selectOptions']):
								raise ValueError("Entered value is not valid. Please enter a valid one.")
							qp_dict = {'key':optional_field['key'],'value':query_parameter_json['selectOptions'][int(qp_value_index)]['value'],'displayValue':query_parameter_json['selectOptions'][int(qp_value_index)]['displayValue']}	
							ticket_api_body['fields'].append(qp_dict)
							user_satisfied = True
						else:
							raise ValueError("Entered value is not valid. Please enter a valid one.")			
					else:
						print(f"No value available for the search string - '{search_value}'")				
			elif 'queryParameters' not in optional_field and len(optional_field['selectOptions']) > 0:
				print(f"\nThese are the available options for '{optional_field['label']}' field")
				for ind in range(len(optional_field['selectOptions'])):
					print(f"Index : {ind} - Value : '{optional_field['selectOptions'][ind]['displayValue']}'")
				value_dropdown_index = int(input('Enter the index of value you want to select: '))
				if value_dropdown_index < 0 or value_dropdown_index >= len(optional_field['selectOptions']):
					raise ValueError("Entered value is not valid. Please enter a valid one.")
				value_dropdown_dict = {'key':optional_field['key'],'value':optional_field['selectOptions'][value_dropdown_index]['value'],'displayValue':optional_field['selectOptions'][value_dropdown_index]['displayValue']}	
				ticket_api_body['fields'].append(value_dropdown_dict)
				
			else:
				raise NotImplementedError(f"Logic is not implemented for this field type {optional_field['type']}")		

		return ticket_api_body





#  Execute the script
if __name__ == "__main__":
    try:
        SNOWIncTicketCreation()
    except KeyboardInterrupt:
        print()
        print("KeyboardInterrupt detected.  Exiting...")
        print()
        sys.exit(0)


"""
   Copyright 2022 RiskSense, Inc.
   
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at:
   
   http://www.apache.org/licenses/LICENSE-2.0
   
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
