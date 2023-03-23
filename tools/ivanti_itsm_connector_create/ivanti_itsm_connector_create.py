""" *******************************************************************************************************************
|
|  Name        :  ivanti_itsm_connector_create.py
|  Description :  Ivanti ITSM connector creation
|  Project     :  risksense_tools
|  Copyright   :  (c) RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """


import json
import os
import sys
import toml
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'lib'))
import risksense_api as rsapi
import datetime

class ItsmCreateTool:
	""" ItsmCreateTool class"""

	def __init__(self):
		""" Main body of script """

		conf_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf', 'config.toml')
		config = self.read_config_file(conf_file)

		self.rs_platform = config['platform_url']
		self.api_key = config['api_key']
		self.itsm_url = config['itsm_url']
		self.itsm_api_token = config['itsm_api_token']
		self.itsm_connector_name = config['itsm_connector_name']
		
		#  Instantiate RiskSenseApi
		self.rs = rsapi.RiskSenseApi(self.rs_platform, self.api_key)

		#  Get client id, or validate supplied client ID
		if 'client_id' not in config:
			client_id = self.get_client_id()
		else:
			client_id = config['client_id']
			try:
				self.validate_client_id(client_id)
			except ValueError:
				print(f"Unable to validate that you belong to client ID {client_id}.")
				print("Exiting.")
				sys.exit(1)

		#  Set default client ID
		self.rs.set_default_client_id(client_id)

		populate_body = {
			"username": "admin",
			"password": self.itsm_api_token,
			"url": self.itsm_url,
			"name": self.itsm_connector_name,
			"type": "IVANTIITSM",
			"projection": "internal"
		}

		try:
			populate_response = self.rs.connectors.connector_populate(populate_body, client_id=client_id)
		except (rsapi.MaxRetryError, rsapi.StatusCodeError, rsapi.NoMatchFound,
				rsapi.UserUnauthorized, rsapi.InsufficientPrivileges, Exception) as ex:
			print(ex)
		
		print("\nHere are the available ticket types for this connector type")
		for ind,item in enumerate(populate_response['ticketType']):
			print(f"Index : {ind} - Value : '{item['displayValue']}'")
		ticket_type_index = int(input("\nEnter the index number of TICKET TYPE you want to select: "))
		selected_ticket_type = populate_response['ticketType'][ticket_type_index]
		
		try:
			ticket_field_response = self.rs.connectors.itsm_get_fields_for_ticket_type(selected_ticket_type['value'], self.itsm_url, self.itsm_connector_name, self.itsm_api_token, username='admin', client_id=client_id)
			ticket_field_response['ticketType'] = selected_ticket_type['value']
		except (rsapi.MaxRetryError, rsapi.StatusCodeError, rsapi.NoMatchFound,
				rsapi.UserUnauthorized, rsapi.InsufficientPrivileges, Exception) as ex:
			print(ex)
			
		try:
			ticket_form_fields, ticket_form = self.get_ticket_creation_body(ticket_field_response)
		except (rsapi.MaxRetryError, rsapi.StatusCodeError, rsapi.NoMatchFound,
				rsapi.UserUnauthorized, rsapi.InsufficientPrivileges, Exception) as ex:
			print(ex)		

		try:
			connector_api_body = self.form_validation(ticket_form_fields, ticket_form,selected_ticket_type)
		except (rsapi.MaxRetryError, rsapi.StatusCodeError, rsapi.NoMatchFound,
				rsapi.UserUnauthorized, rsapi.InsufficientPrivileges, Exception) as ex:
			print(ex)	
		with open('ticket_create.json', 'w') as f:
			f.write(json.dumps(connector_api_body))
		try:
			connector_create_response = self.rs.connectors.create_ivanti_itsm_connector(connector_api_body,client_id=client_id)	
			print(f"\nConnector is created succesfully. Connector Id is {connector_create_response['id']}")
		except (rsapi.MaxRetryError, rsapi.StatusCodeError, rsapi.NoMatchFound,
				rsapi.UserUnauthorized, rsapi.InsufficientPrivileges, Exception) as ex:
			print(ex)				

		

	@staticmethod
	def read_config_file(filename):

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

	def validate_client_id(self, submitted_client_id):

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

	def get_client_id(self):

		"""
		Get the client ID associated with this API key.

		:return:    Client ID
		:rtype:     int

		"""

		return self.rs.my_clients[0]['id']

	def get_ticket_creation_body(self,ticket_form: dict) -> dict:
		ticket_form_fields = []
		ticket_form['ticketSyncStatus'] = []
		available_tag_types = ['COMPLIANCE', 'LOCATION', 'CUSTOM', 'REMEDIATION', 'PEOPLE', 'PROJECT', 'SCANNER', 'CMDB']
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
			
		for index,field in enumerate(ticket_form_fields):
			ticket_form_fields_dict[field['fieldName']]	 = index

		for index,field in enumerate(ticket_form_fields):
			enter_value_check = input(f"\nDo you want to enter a value for '{field['label']}' field? Enter 'yes' or 'no': ").strip().lower()			
			if enter_value_check == 'yes':
				if field['label'] == 'Customer':
					fetch_available_values = self.rs.connectors.ivanti_itsm_fetch_customers(self.itsm_url, self.itsm_api_token)
					dropdown_value_dict = {}
					sample_list = []
					for ind in range(len(fetch_available_values)):
						dropdown_value_dict[fetch_available_values[ind]['displayName']] = fetch_available_values[ind]['RecId']	
					if len(fetch_available_values) > 10:
						sample_list = fetch_available_values[:10]
						print(f"\nHere are some available options suggestion for '{field['label']}' field")
						for i,op in enumerate(sample_list):
							print(f"Index : {i} - Value : '{op['displayName']}'")		
						dropdown_suggestion_index = input("\nEnter the index of value you want to select. If the value that you are looking for is not displayed in the terminal, please enter 'no': ").strip().lower()			
						if dropdown_suggestion_index == 'no':
							user_satisfied = None
							while user_satisfied == None:
								search_pattern_match = []
								search_string = input(f"\nEnter the search string for '{field['label']}' field: ").strip().lower()
								for key,value in dropdown_value_dict.items():
									start_index = str(key).lower().find(search_string)
									if start_index != -1:
										search_pattern_match.append({key:value})
								if len(search_pattern_match) == 0:
									print("\nNo value that matches the search string. Search again!")
								else:
									print("\nHere are the available value that matches the search string")
									for ind in range(len(search_pattern_match)):
										print(f"Index : {ind} - Value : '{list(search_pattern_match[ind].keys())[0]}'")	
									dropdown_index = input("\nEnter the index of value you want to select. If the value that you are looking for is not displayed in the terminal, please enter 'no': ").strip().lower()	
									if dropdown_index == 'no':
										pass
									elif dropdown_index.isdigit() == True:
										if (int(dropdown_index) < 0) and (int(dropdown_index) >= len(search_pattern_match)):
											raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
										field['displayValue'] = list(search_pattern_match[int(dropdown_index)].keys())[0]
										field['valueKey'] = list(search_pattern_match[int(dropdown_index)].values())[0]
										user_satisfied = True	
									else:
										raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
						elif dropdown_suggestion_index.isdigit() == True:
							if (int(dropdown_suggestion_index) < 0) and (int(dropdown_suggestion_index) >= len(sample_list)):
								raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
							field['displayValue'] = fetch_available_values[int(dropdown_suggestion_index)]['displayName']
							field['valueKey'] = fetch_available_values[int(dropdown_suggestion_index)]['RecId']							
						else:
							raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
					elif len(fetch_available_values) <= 10:
						print(f"\nHere are the available options for '{field['label']}' field")
						for i,op in enumerate(fetch_available_values):
							print(f"Index : {i} - Value : '{op['Label']}'")		
						dropdown_index = int(input(f"\nEnter the index number of value you want to select for '{field['label']}' field: "))	
						field['displayValue'] = fetch_available_values[dropdown_index]['displayName']
						field['valueKey'] = fetch_available_values[dropdown_index]['RecId']					
				elif field['isPluginInfo'] == True:
					pluginInfo_field_input = input(f"\nEnter 'value' to add text to the textbox or enter 'check' to check-in the checkbox for the '{field['label']}' field. Please enter anyone: ").strip().lower()
					if pluginInfo_field_input == 'value':
						pluginInfo_field_text = input(f"Enter the value for '{field['label']}' field: ").strip()
						field['displayValue'] = pluginInfo_field_text
						field['valueKey'] = pluginInfo_field_text				
					elif pluginInfo_field_input == 'check':
						ticket_form['pluingInfoUsedKeys'].append(field['fieldName'])
						field['displayValue'] = "Summary will be updated shortly."
						field['valueKey'] = "Summary will be updated shortly."						
					else:
						raise ValueError(f"Entered invalid input for '{field['label']}' field. Please enter a valid one.")
				elif field['type'] == 'DropDown':
					field = self._get_dropdown_values(ticket_form,dropdown_fields_dict,field,ticket_form_fields,ticket_form_fields_dict)
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
					fetch_available_values = self.rs.connectors.ivanti_itsm_fetch_releaseLink(self.itsm_url, self.itsm_api_token)
					dropdown_value_dict = {}
					sample_list = []
					for ind in range(len(fetch_available_values)):
						dropdown_value_dict[fetch_available_values[ind]['displayName']] = fetch_available_values[ind]['RecId']	
					if len(fetch_available_values) > 10:
						sample_list = fetch_available_values[:10]
						print(f"\nHere are some available options suggestion for '{field['label']}' field")
						for i,op in enumerate(sample_list):
							print(f"Index : {i} - Value : '{op['displayName']}'")		
						dropdown_suggestion_index = input("\nEnter the index of value you want to select. If the value that you are looking for is not displayed in the terminal, please enter 'no': ").strip().lower()			
						if dropdown_suggestion_index == 'no':
							user_satisfied = None
							while user_satisfied == None:
								search_pattern_match = []
								search_string = input(f"\nEnter the search string for '{field['label']}' field: ").strip().lower()
								for key,value in dropdown_value_dict.items():
									start_index = str(key).lower().find(search_string)
									if start_index != -1:
										search_pattern_match.append({key:value})
								if len(search_pattern_match) == 0:
									print("\nNo value that matches the search string. Search again!")
								else:
									print("\nHere are the available value that matches the search string")
									for ind in range(len(search_pattern_match)):
										print(f"Index : {ind} - Value : '{list(search_pattern_match[ind].keys())[0]}'")	
									dropdown_index = input("\nEnter the index of value you want to select. If the value that you are looking for is not displayed in the terminal, please enter 'no': ").strip().lower()	
									if dropdown_index == 'no':
										pass
									elif dropdown_index.isdigit() == True:
										if (int(dropdown_index) < 0) and (int(dropdown_index) >= len(search_pattern_match)):
											raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
										field['displayValue'] = list(search_pattern_match[int(dropdown_index)].keys())[0]
										field['valueKey'] = list(search_pattern_match[int(dropdown_index)].values())[0]
										user_satisfied = True		
									else:
										raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
						elif dropdown_suggestion_index.isdigit() == True:
							if (int(dropdown_suggestion_index) < 0) and (int(dropdown_suggestion_index) >= len(sample_list)):
								raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
							field['displayValue'] = fetch_available_values[int(dropdown_suggestion_index)]['displayName']
							field['valueKey'] = fetch_available_values[int(dropdown_suggestion_index)]['RecId']							
						else:
							raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
					elif len(fetch_available_values) <= 10:
						print(f"\nHere are the available options for '{field['label']}' field")
						for i,op in enumerate(fetch_available_values):
							print(f"Index : {i} - Value : '{op['Label']}'")		
						dropdown_index = int(input(f"\nEnter the index number of value you want to select for '{field['label']}' field: "))	
						field['displayValue'] = fetch_available_values[dropdown_index]['displayName']
						field['valueKey'] = fetch_available_values[dropdown_index]['RecId']			
				elif field['label'] == 'Requestor Link':
					fetch_available_values = self.rs.connectors.ivanti_itsm_fetch_requestorLink(self.itsm_url, self.itsm_api_token)
					dropdown_value_dict = {}
					sample_list = []
					for ind in range(len(fetch_available_values)):
						dropdown_value_dict[fetch_available_values[ind]['displayName']] = fetch_available_values[ind]['RecId']	
					if len(fetch_available_values) > 10:
						sample_list = fetch_available_values[:10]
						print(f"\nHere are some available options suggestion for '{field['label']}' field")
						for i,op in enumerate(sample_list):
							print(f"Index : {i} - Value : '{op['displayName']}'")		
						dropdown_suggestion_index = input("\nEnter the index of value you want to select. If the value that you are looking for is not displayed in the terminal, please enter 'no': ").strip().lower()			
						if dropdown_suggestion_index == 'no':
							user_satisfied = None
							while user_satisfied == None:
								search_pattern_match = []
								search_string = input(f"\nEnter the search string for '{field['label']}' field: ").strip().lower()
								for key,value in dropdown_value_dict.items():
									start_index = str(key).lower().find(search_string)
									if start_index != -1:
										search_pattern_match.append({key:value})
								if len(search_pattern_match) == 0:
									print("\nNo value that matches the search string. Search again!")
								else:
									print("\nHere are the available value that matches the search string")
									for ind in range(len(search_pattern_match)):
										print(f"Index : {ind} - Value : '{list(search_pattern_match[ind].keys())[0]}'")	
									dropdown_index = input("\nEnter the index of value you want to select. If the value that you are looking for is not displayed in the terminal, please enter 'no': ").strip().lower()	
									if dropdown_index == 'no':
										pass
									elif dropdown_index.isdigit() == True:
										if (int(dropdown_index) < 0) and (int(dropdown_index) >= len(search_pattern_match)):
											raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
										field['displayValue'] = list(search_pattern_match[int(dropdown_index)].keys())[0]
										field['valueKey'] = list(search_pattern_match[int(dropdown_index)].values())[0]
										user_satisfied = True	
									else:
										raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
						elif dropdown_suggestion_index.isdigit() == True:
							if (int(dropdown_suggestion_index) < 0) and (int(dropdown_suggestion_index) >= len(sample_list)):
								raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
							field['displayValue'] = fetch_available_values[int(dropdown_suggestion_index)]['displayName']
							field['valueKey'] = fetch_available_values[int(dropdown_suggestion_index)]['RecId']							
						else:
							raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
					elif len(fetch_available_values) <= 10:
						print(f"\nHere are the available options for '{field['label']}' field")
						for i,op in enumerate(fetch_available_values):
							print(f"Index : {i} - Value : '{op['Label']}'")		
						dropdown_index = int(input(f"\nEnter the index number of value you want to select for '{field['label']}' field: "))	
						field['displayValue'] = fetch_available_values[dropdown_index]['displayName']
						field['valueKey'] = fetch_available_values[dropdown_index]['RecId']											
				elif field['type'] == 'Text':
					text_type_field = input(f"Enter the value for '{field['label']}' field: ").strip()
					field['displayValue'] = text_type_field
					field['valueKey'] = text_type_field					
				else:
					raise NotImplementedError('The logic is not implement for this scenario')
			elif enter_value_check == 'no':
				pass
			else:
				raise ValueError("Entered value is not valid. Please enter a valid one.")		

		# FIELDS FOR TICKET DESCRIPTION

		enter_value_check = input(f"\nDo you want to select fields for TICKET DESCRIPTION? Enter 'yes' or 'no': ").strip().lower()
		if enter_value_check == 'yes':	
			print(f"\nThese are the available fields")
			for ind,item in enumerate(ticket_form['supportedDescriptionFields']):
				print(f"Index : {ind} - Value : '{item['displayValue']}'")
			field_desp_indexes = input("\nEnter the index number of fields you want to select. If you want to select multiple fields enter it as comma seperated values: ").strip().lower()
			if ',' in field_desp_indexes:
				field_desp_indexes = field_desp_indexes.split(',')
				field_desp_indexes_value = [x.strip() for x in field_desp_indexes]
				field_desp_indexes_value = list(set(field_desp_indexes_value))
				for val in field_desp_indexes_value:
					if (val.isdigit() == False) or (int(val) < 0) or (int(val) >= len(ticket_form['supportedDescriptionFields'])):
						raise ValueError("Entered value is not valid. Please enter a valid one.")		
				for val in field_desp_indexes_value:
					ticket_form['supportedDescriptionFields'][int(val)]['isCurrentlySelected'] = True
			elif field_desp_indexes.isdigit() == True:
				if (field_desp_indexes.isdigit() == False) or (int(field_desp_indexes) < 0) or (int(field_desp_indexes) >= len(ticket_form['supportedDescriptionFields'])):
					raise ValueError("Entered value is not valid. Please enter a valid one.")
				ticket_form['supportedDescriptionFields'][int(field_desp_indexes)]['isCurrentlySelected'] = True				
			else:
				raise ValueError("Entered value is not valid. Please enter a valid one.")				
		elif enter_value_check == 'no':
			pass
		else:
			raise ValueError("Entered value is not valid. Please enter a valid one.")	

		# LOCKED FIELDS

		enter_value_check = input(f"\nDo you want to select fields that to be LOCKED? Enter 'yes' or 'no': ").strip().lower()
		if enter_value_check == 'yes':
			print(f"\nThese are the available fields")
			for ind,item in enumerate(ticket_form['lockedFields']):
				print(f"Index : {ind} - Value : '{item['displayValue']}'")
			locked_field_indexes = input("\nEnter the index number of fields you want to select. If you want to select multiple fields enter it as comma seperated values: ").strip().lower()
			if ',' in locked_field_indexes:
				locked_field_indexes = locked_field_indexes.split(',')
				locked_field_indexes_value = [x.strip() for x in locked_field_indexes]
				locked_field_indexes_value = list(set(locked_field_indexes_value))
				for val in locked_field_indexes_value:
					if (val.isdigit() == False) or (int(val) < 0) or (int(val) >= len(ticket_form['lockedFields'])):
						raise ValueError("Entered value is not valid. Please enter a valid one.")		
				for val in locked_field_indexes_value:
					ticket_form['lockedFields'][int(val)]['isCurrentlySelected'] = True
			elif locked_field_indexes.isdigit() == True:
				if (locked_field_indexes.isdigit() == False) or (int(locked_field_indexes) < 0) or (int(locked_field_indexes) >= len(ticket_form['lockedFields'])):
					raise ValueError("Entered value is not valid. Please enter a valid one.")
				ticket_form['lockedFields'][int(locked_field_indexes)]['isCurrentlySelected'] = True				
			else:
				raise ValueError("Entered value is not valid. Please enter a valid one.")
		elif enter_value_check == 'no':
			pass
		else:
			raise ValueError("Entered value is not valid. Please enter a valid one.")	


		print(f"\n{('-')*5} RISKSENSE DEFAULTS {('-')*5}")

		enter_value_check = input(f"\nDo you want to enter a value for TAG TYPE? Enter 'yes' or 'no': ").strip().lower()
		if enter_value_check == 'yes':	
			print("\nThese are the available TAG TYPES")
			for ind in range(len(available_tag_types)):
				print(f"Index : {ind} - Value : '{available_tag_types[ind]}'")
			selected_tag_type_index = int(input('\nEnter the index number of TAG TYPE that you want to select: '))
			if (int(selected_tag_type_index) < 0) or (int(selected_tag_type_index) >= len(available_tag_types)):
				raise ValueError("Entered value is not valid. Please enter a valid one.")		
			selected_tag_type = available_tag_types[selected_tag_type_index]
			ticket_form['tagTypeDefaultValue'] = selected_tag_type
		elif enter_value_check == 'no':
			pass
		else:
			raise ValueError("Entered value is not valid. Please enter a valid one.")			


		if len(ticket_form['slaDateFieldOptions']) > 0:	
			enter_value_check = input(f"\nDo you want to enter a value for '{field['label']}' field? Enter 'yes' or 'no': ").strip().lower()
			if enter_value_check == 'yes':			
				print('\nThese are the available ITSM fields that can be selected for mapping with the RiskSense SLA date')
				for ind in range(len(ticket_form['slaDateFieldOptions'])):
					print(f"Index : {ind} - Value : '{ticket_form['slaDateFieldOptions'][ind]['displayValue']}'")
				sla_dropdown_index = int(input('Enter the index of value you want to select: '))
				if sla_dropdown_index < 0 or sla_dropdown_index >= len(ticket_form['slaDateFieldOptions']):
					raise ValueError("Entered value is not valid. Please enter a valid one.")		
				ticket_form['slaDateField'] = (ticket_form['slaDateFieldOptions'][sla_dropdown_index]['value'])
			elif enter_value_check == 'no':
				pass
			else:
				raise ValueError("Entered value is not valid. Please enter a valid one.")				

		# ATTACHMENT

		enter_value_check = input(f"\nDo you want to attach asset and finding details to ticket? Enter 'yes' or 'no': ").strip().lower()
		if enter_value_check == 'yes':
			ticket_form['enabledUploadAttachment'] = True
		elif enter_value_check == 'no':
			ticket_form['enabledUploadAttachment'] = False
		else:
			raise ValueError("Entered value is not valid. Please enter a valid one.")	


		# TAG DELETION

		enter_value_check = input(f"\nDo you want to allow the deletion of tags that are associated with ITSM Ticketing connector issues from this? Enter 'yes' or 'no': ").strip().lower()
		if enter_value_check == 'yes':
			ticket_form['enabledTagRemoval'] = True
		elif enter_value_check == 'no':
			ticket_form['enabledTagRemoval'] = False
		else:
			raise ValueError("Entered value is not valid. Please enter a valid one.")	


		# TICKET SYNC STATUS

		print("\nHere are the available options for TICKET SYNC STATUS")
		for ind,item in enumerate(ticket_form['fieldsWithValues'][dropdown_fields_dict['Status']]['values']):
			print(f"Index : {ind} - Value : '{item['Label']}'")

		ticket_sync_indexes = input("\nEnter the index number of fields you want to select. If you want to select multiple fields enter it as comma seperated values: ").strip().lower()
		if ',' in ticket_sync_indexes:
			ticket_sync_indexes = ticket_sync_indexes.split(',')
			ticket_sync_indexes_value = [x.strip() for x in ticket_sync_indexes]
			ticket_sync_indexes_value = list(set(ticket_sync_indexes_value))
			for val in ticket_sync_indexes_value:
				if (val.isdigit() == False) or (int(val) < 0) or (int(val) >= len(ticket_form['fieldsWithValues'][dropdown_fields_dict['Status']]['values'])):
					raise ValueError("Entered value is not valid. Please enter a valid one.")		
			for val in ticket_sync_indexes_value:
				ticket_form['ticketSyncStatus'].append(ticket_form['fieldsWithValues'][dropdown_fields_dict['Status']]['values'][int(val)]['value'])
		elif ticket_sync_indexes.isdigit() == True:
			if (ticket_sync_indexes.isdigit() == False) or (int(ticket_sync_indexes) < 0) or (int(ticket_sync_indexes) >= len(ticket_form['fieldsWithValues'][dropdown_fields_dict['Status']]['values'])):
				raise ValueError("Entered value is not valid. Please enter a valid one.")
			ticket_form['ticketSyncStatus'].append(ticket_form['fieldsWithValues'][dropdown_fields_dict['Status']]['values'][int(ticket_sync_indexes)]['value'])			
		else:
			raise ValueError("Entered value is not valid. Please enter a valid one.")		

		# CLOSED TICKET STATE

		
		close_state_presence = False
		ticket_close_state_list = []
		for ind,item in enumerate(ticket_form['fieldsWithValues'][dropdown_fields_dict['Status']]['values']):
			if item['value'] not in ticket_form['ticketSyncStatus']:
				close_state_presence = True
				ticket_close_state_list.append(item)
		if close_state_presence == False:
			raise ValueError('Do not select all values for TICKET SYNC STATUS. Atleast one value is needed to select for TICKET CLOSE STATE.')	
		elif close_state_presence == True:
			print("\nHere are the available options for TICKET CLOSE STATE")
			for ind,item in enumerate(ticket_close_state_list):
				print(f"Index : {ind} - Value : '{item['Label']}'")	
			close_state_index = int(input("\nEnter the index number of value that you want to select: "))
			ticket_form['ticketCloseState'] = ticket_close_state_list[close_state_index]
		

		# FINDING STATUS CHANGE

		enter_value_check = input(f"\nDo you want to move the ITSM - Ticket to the selected ‘Closed Status’ above when all the associated findings for a ticket are in a closed state in RiskSense.? Enter 'yes' or 'no': ").strip().lower()
		if enter_value_check == 'yes':
			ticket_form['moveTicketState'] = True
		elif enter_value_check == 'no':
			ticket_form['moveTicketState'] = False
		else:
			raise ValueError("Entered value is not valid. Please enter a valid one.")	
		

		return ticket_form_fields, ticket_form


	def _get_dropdown_values(self, ticket_form, dropdown_fields_dict, field, ticket_form_fields, ticket_form_fields_dict):
		available_option_records = ticket_form['fieldsWithValues'][dropdown_fields_dict[field['fieldName']]]
		if available_option_records['sameAs'] == "":
			if len(available_option_records['FieldRef']) == 0:
				if len(available_option_records['values']) == 0:
					raise NotImplementedError('The logic is not implement for this scenario')		
				else:
					dropdown_value_dict = {}
					sample_list = []
					for ind in range(len(available_option_records['values'])):
						dropdown_value_dict[available_option_records['values'][ind]['Label']] = available_option_records['values'][ind]['value']	
					if len(available_option_records['values']) > 10:
						sample_list = available_option_records['values'][:10]
						print(f"\nHere are some available options suggestion for '{field['label']}' field")
						for i,op in enumerate(sample_list):
							print(f"Index : {i} - Value : '{op['Label']}'")		
						dropdown_suggestion_index = input("\nEnter the index of value you want to select. If the value that you are looking for is not displayed in the terminal, please enter 'no': ").strip().lower()			
						if dropdown_suggestion_index == 'no':
							user_satisfied = None
							while user_satisfied == None:
								search_pattern_match = []
								search_string = input(f"\nEnter the search string for '{field['label']}' field: ").strip().lower()
								for key,value in dropdown_value_dict.items():
									start_index = str(key).lower().find(search_string)
									if start_index != -1:
										search_pattern_match.append({key:value})
								if len(search_pattern_match) == 0:
									print("\nNo value that matches the search string. Search again!")
								else:
									print("\nHere are the available value that matches the search string")
									for ind in range(len(search_pattern_match)):
										print(f"Index : {ind} - Value : '{list(search_pattern_match[ind].keys())[0]}'")	
									dropdown_index = input("\nEnter the index of value you want to select. If the value that you are looking for is not displayed in the terminal, please enter 'no': ").strip().lower()	
									if dropdown_index == 'no':
										pass
									elif dropdown_index.isdigit() == True:
										if (int(dropdown_index) < 0) and (int(dropdown_index) >= len(search_pattern_match)):
											raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
										field['displayValue'] = list(search_pattern_match[int(dropdown_index)].keys())[0]
										field['valueKey'] = list(search_pattern_match[int(dropdown_index)].values())[0]
										user_satisfied = True	
									else:
										raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
						elif dropdown_suggestion_index.isdigit() == True:
							if (int(dropdown_suggestion_index) < 0) and (int(dropdown_suggestion_index) >= len(sample_list)):
								raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
							field['displayValue'] = available_option_records['values'][int(dropdown_suggestion_index)]['Label']
							field['valueKey'] = available_option_records['values'][int(dropdown_suggestion_index)]['value']							
						else:
							raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
					elif len(available_option_records['values']) <= 10:
						print(f"\nHere are the available options for '{field['label']}' field")
						for i,op in enumerate(available_option_records['values']):
							print(f"Index : {i} - Value : '{op['Label']}'")		
						dropdown_index = int(input(f"\nEnter the index number of value you want to select for '{field['label']}' field: "))	
						field['displayValue'] = available_option_records['values'][dropdown_index]['Label']
						field['valueKey'] = available_option_records['values'][dropdown_index]['value']										
			elif len(available_option_records['FieldRef']) == 1:
				"""API CALL"""	
				reference_field = ticket_form_fields[ticket_form_fields_dict[available_option_records['FieldRef'][0]]]
				if 'displayValue' in reference_field:
					on_the_fly_resp = self.rs.connectors.ivanti_itsm_fetch_fieldValue_wrt_dependentField(ticket_form['ticketType'], self.itsm_url, self.itsm_api_token, available_option_records['FieldName'], reference_field['fieldName'], reference_field['valueKey'])
					dropdown_value_dict = {}
					sample_list = []
					for ind in range(len(on_the_fly_resp))	:
						dropdown_value_dict[on_the_fly_resp[ind]['label']] = on_the_fly_resp[ind]['value']
					if len(on_the_fly_resp) > 10:
						sample_list = on_the_fly_resp[:10]
						print(f"\nHere are some available options suggestion for '{field['label']}' field")
						for i,op in enumerate(sample_list):
							print(f"Index : {i} - Value : '{op['label']}'")		
						dropdown_suggestion_index = input("\nEnter the index of value you want to select. If the value that you are looking for is not displayed in the terminal, please enter 'no': ").strip().lower()			
						if dropdown_suggestion_index == 'no':
							user_satisfied = None
							while user_satisfied == None:
								search_pattern_match = []
								search_string = input(f"\nEnter the search string for '{field['label']}' field: ").strip().lower()
								for key,value in dropdown_value_dict.items():
									start_index = str(key).lower().find(search_string)
									if start_index != -1:
										search_pattern_match.append({key:value})
								if len(search_pattern_match) == 0:
									print("\nNo value that matches the search string. Search again!")
								else:
									print("\nHere are the available options that matches the search string")
									for ind in range(len(search_pattern_match)):
										print(f"Index : {ind} - Value : '{list(search_pattern_match[ind].keys())[0]}'")	
									dropdown_index = input("\nEnter the index of value you want to select. If the value that you are looking for is not displayed in the terminal, please enter 'no': ").strip().lower()	
									if dropdown_index == 'no':
										pass
									elif dropdown_index.isdigit() == True:
										if (int(dropdown_index) < 0) and (int(dropdown_index) >= len(search_pattern_match)):
											raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
										field['displayValue'] = list(search_pattern_match[int(dropdown_index)].keys())[0]
										field['valueKey'] = list(search_pattern_match[int(dropdown_index)].values())[0]	
										user_satisfied = True	
									else:
										raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
						elif dropdown_suggestion_index.isdigit() == True:
							if (int(dropdown_suggestion_index) < 0) and (int(dropdown_suggestion_index) >= len(sample_list)):
								raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
							field['displayValue'] = on_the_fly_resp[int(dropdown_suggestion_index)]['label']
							field['valueKey'] = on_the_fly_resp[int(dropdown_suggestion_index)]['value']							
						else:
							raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")						
					elif len(on_the_fly_resp) <= 10:
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
						dropdown_value_dict = {}
						sample_list = []
						for ind in range(len(available_option_records['values'])):
							dropdown_value_dict[available_option_records['values'][ind]['Label']] = available_option_records['values'][ind]['value']	
						if len(available_option_records['values']) > 10:
							sample_list = available_option_records['values'][:10]
							print(f"\nHere are some available options suggestion for '{field['label']}' field")
							for i,op in enumerate(sample_list):
								print(f"Index : {i} - Value : '{op['Label']}'")		
							dropdown_suggestion_index = input("\nEnter the index of value you want to select. If the value that you are looking for is not displayed in the terminal, please enter 'no': ").strip().lower()			
							if dropdown_suggestion_index == 'no':
								user_satisfied = None
								while user_satisfied == None:
									search_pattern_match = []
									search_string = input(f"\nEnter the search string for '{field['label']}' field: ").strip().lower()
									for key,value in dropdown_value_dict.items():
										start_index = str(key).lower().find(search_string)
										if start_index != -1:
											search_pattern_match.append({key:value})
									if len(search_pattern_match) == 0:
										print("\nNo value that matches the search string. Search again!")
									else:
										print("\nHere are the available value that matches the search string")
										for ind in range(len(search_pattern_match)):
											print(f"Index : {ind} - Value : '{list(search_pattern_match[ind].keys())[0]}'")	
										dropdown_index = input("\nEnter the index of value you want to select. If the value that you are looking for is not displayed in the terminal, please enter 'no': ").strip().lower()	
										if dropdown_index == 'no':
											pass
										elif dropdown_index.isdigit() == True:
											if (int(dropdown_index) < 0) and (int(dropdown_index) >= len(search_pattern_match)):
												raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
											field['displayValue'] = list(search_pattern_match[int(dropdown_index)].keys())[0]
											field['valueKey'] = list(search_pattern_match[int(dropdown_index)].values())[0]	
											user_satisfied = True	
										else:
											raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
							elif dropdown_suggestion_index.isdigit() == True:
								if (int(dropdown_suggestion_index) < 0) and (int(dropdown_suggestion_index) >= len(sample_list)):
									raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
								field['displayValue'] = available_option_records['values'][int(dropdown_suggestion_index)]['Label']
								field['valueKey'] = available_option_records['values'][int(dropdown_suggestion_index)]['value']							
							else:
								raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
						elif len(available_option_records['values']) <= 10:
							print(f"\nHere are the available options for '{field['label']}' field")
							for i,op in enumerate(available_option_records['values']):
								print(f"Index : {i} - Value : '{op['Label']}'")		
							dropdown_index = int(input(f"\nEnter the index number of value you want to select for '{field['label']}' field: "))	
							field['displayValue'] = available_option_records['values'][dropdown_index]['Label']
							field['valueKey'] = available_option_records['values'][dropdown_index]['value']
			else:
				raise NotImplementedError('The logic is not implement for this scenario')
		elif available_option_records['sameAs'] != "":
			if len(available_option_records['FieldRef']) == 0:
				if len(available_option_records['values']) == 0:
					raise NotImplementedError('The logic is not implement for this scenario')		
				else:
					dropdown_value_dict = {}
					sample_list = []
					for ind in range(len(available_option_records['values'])):
						dropdown_value_dict[available_option_records['values'][ind]['Label']] = available_option_records['values'][ind]['value']	
					if len(available_option_records['values']) > 10:
						sample_list = available_option_records['values'][:10]
						print(f"\nHere are some available options suggestion for '{field['label']}' field")
						for i,op in enumerate(sample_list):
							print(f"Index : {i} - Value : '{op['Label']}'")		
						dropdown_suggestion_index = input("\nEnter the index of value you want to select. If the value that you are looking for is not displayed in the terminal, please enter 'no': ").strip().lower()			
						if dropdown_suggestion_index == 'no':
							user_satisfied = None
							while user_satisfied == None:
								search_pattern_match = []
								search_string = input(f"\nEnter the search string for '{field['label']}' field: ").strip().lower()
								for key,value in dropdown_value_dict.items():
									start_index = str(key).lower().find(search_string)
									if start_index != -1:
										search_pattern_match.append({key:value})
								if len(search_pattern_match) == 0:
									print("\nNo value that matches the search string. Search again!")
								else:
									print("\nHere are the available value that matches the search string")
									for ind in range(len(search_pattern_match)):
										print(f"Index : {ind} - Value : '{list(search_pattern_match[ind].keys())[0]}'")	
									dropdown_index = input("\nEnter the index of value you want to select. If the value that you are looking for is not displayed in the terminal, please enter 'no': ").strip().lower()	
									if dropdown_index == 'no':
										pass
									elif dropdown_index.isdigit() == True:
										if (int(dropdown_index) < 0) and (int(dropdown_index) >= len(search_pattern_match)):
											raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
										field['displayValue'] = list(search_pattern_match[int(dropdown_index)].keys())[0]
										field['valueKey'] = list(search_pattern_match[int(dropdown_index)].values())[0]	
										user_satisfied = True	
									else:
										raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
						elif dropdown_suggestion_index.isdigit() == True:
							if (int(dropdown_suggestion_index) < 0) and (int(dropdown_suggestion_index) >= len(sample_list)):
								raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
							field['displayValue'] = available_option_records['values'][int(dropdown_suggestion_index)]['Label']
							field['valueKey'] = available_option_records['values'][int(dropdown_suggestion_index)]['value']							
						else:
							raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
					elif len(available_option_records['values']) <= 10:
						print(f"\nHere are the available options for '{field['label']}' field")
						for i,op in enumerate(available_option_records['values']):
							print(f"Index : {i} - Value : '{op['Label']}'")		
						dropdown_index = int(input(f"\nEnter the index number of value you want to select for '{field['label']}' field: "))	
						field['displayValue'] = available_option_records['values'][dropdown_index]['Label']
						field['valueKey'] = available_option_records['values'][dropdown_index]['value']
			elif len(available_option_records['FieldRef']) == 1:
				"""API CALL"""		
				reference_field = ticket_form_fields[ticket_form_fields_dict[available_option_records['FieldRef'][0]]]
				if 'displayValue' in reference_field:
					on_the_fly_resp = self.rs.connectors.ivanti_itsm_fetch_fieldValue_wrt_dependentField(ticket_form['ticketType'], self.itsm_url, self.itsm_api_token, available_option_records['FieldName'], reference_field['fieldName'], reference_field['valueKey'])
					dropdown_value_dict = {}
					sample_list = []
					for ind in range(len(on_the_fly_resp))	:
						dropdown_value_dict[on_the_fly_resp[ind]['label']] = on_the_fly_resp[ind]['value']
					if len(on_the_fly_resp) > 10:
						sample_list = on_the_fly_resp[:10]
						print(f"\nHere are some available options suggestion for '{field['label']}' field")
						for i,op in enumerate(sample_list):
							print(f"Index : {i} - Value : '{op['label']}'")		
						dropdown_suggestion_index = input("\nEnter the index of value you want to select. If the value that you are looking for is not displayed in the terminal, please enter 'no': ").strip().lower()			
						if dropdown_suggestion_index == 'no':
							user_satisfied = None
							while user_satisfied == None:
								search_pattern_match = []
								search_string = input(f"\nEnter the search string for '{field['label']}' field: ").strip().lower()
								for key,value in dropdown_value_dict.items():
									start_index = str(key).lower().find(search_string)
									if start_index != -1:
										search_pattern_match.append({key:value})
								if len(search_pattern_match) == 0:
									print("\nNo value that matches the search string. Search again!")
								else:
									print("\nHere are the available options that matches the search string")
									for ind in range(len(search_pattern_match)):
										print(f"Index : {ind} - Value : '{list(search_pattern_match[ind].keys())[0]}'")	
									dropdown_index = input("\nEnter the index of value you want to select. If the value that you are looking for is not displayed in the terminal, please enter 'no': ").strip().lower()	
									if dropdown_index == 'no':
										pass
									elif dropdown_index.isdigit() == True:
										if (int(dropdown_index) < 0) and (int(dropdown_index) >= len(search_pattern_match)):
											raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
										field['displayValue'] = list(search_pattern_match[int(dropdown_index)].keys())[0]
										field['valueKey'] = list(search_pattern_match[int(dropdown_index)].values())[0]	
										user_satisfied = True	
									else:
										raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
						elif dropdown_suggestion_index.isdigit() == True:
							if (int(dropdown_suggestion_index) < 0) and (int(dropdown_suggestion_index) >= len(sample_list)):
								raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
							field['displayValue'] = on_the_fly_resp[int(dropdown_suggestion_index)]['label']
							field['valueKey'] = on_the_fly_resp[int(dropdown_suggestion_index)]['value']							
						else:
							raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")						
					elif len(on_the_fly_resp) <= 10:
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
							dropdown_value_dict = {}
							sample_list = []
							for ind in range(len(sameAs_field_option_dict['values'])):
								dropdown_value_dict[sameAs_field_option_dict['values'][ind]['Label']] = sameAs_field_option_dict['values'][ind]['value']	
							if len(sameAs_field_option_dict['values']) > 10:
								sample_list = sameAs_field_option_dict['values'][:10]
								print(f"\nHere are some available options suggestion for '{field['label']}' field")
								for i,op in enumerate(sample_list):
									print(f"Index : {i} - Value : '{op['Label']}'")		
								dropdown_suggestion_index = input("\nEnter the index of value you want to select. If the value that you are looking for is not displayed in the terminal, please enter 'no': ").strip().lower()			
								if dropdown_suggestion_index == 'no':
									user_satisfied = None
									while user_satisfied == None:
										search_pattern_match = []
										search_string = input(f"\nEnter the search string for '{field['label']}' field: ").strip().lower()
										for key,value in dropdown_value_dict.items():
											start_index = str(key).lower().find(search_string)
											if start_index != -1:
												search_pattern_match.append({key:value})
										if len(search_pattern_match) == 0:
											print("\nNo value that matches the search string. Search again!")
										else:
											print("\nHere are the available value that matches the search string")
											for ind in range(len(search_pattern_match)):
												print(f"Index : {ind} - Value : '{list(search_pattern_match[ind].keys())[0]}'")	
											dropdown_index = input("\nEnter the index of value you want to select. If the value that you are looking for is not displayed in the terminal, please enter 'no': ").strip().lower()	
											if dropdown_index == 'no':
												pass
											elif dropdown_index.isdigit() == True:
												if (int(dropdown_index) < 0) and (int(dropdown_index) >= len(search_pattern_match)):
													raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
												field['displayValue'] = list(search_pattern_match[int(dropdown_index)].keys())[0]
												field['valueKey'] = list(search_pattern_match[int(dropdown_index)].values())[0]
												user_satisfied = True		
											else:
												raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
								elif dropdown_suggestion_index.isdigit() == True:
									if (int(dropdown_suggestion_index) < 0) and (int(dropdown_suggestion_index) >= len(sample_list)):
										raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
									field['displayValue'] = sameAs_field_option_dict['values'][int(dropdown_suggestion_index)]['Label']
									field['valueKey'] = sameAs_field_option_dict['values'][int(dropdown_suggestion_index)]['value']							
								else:
									raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
							elif len(sameAs_field_option_dict['values']) <= 10:
								print(f"\nHere are the available options for '{field['label']}' field")
								for i,op in enumerate(sameAs_field_option_dict['values']):
									print(f"Index : {i} - Value : '{op['Label']}'")		
								dropdown_index = int(input(f"\nEnter the index number of value you want to select for '{field['label']}' field: "))	
								field['displayValue'] = sameAs_field_option_dict['values'][dropdown_index]['Label']
								field['valueKey'] = sameAs_field_option_dict['values'][dropdown_index]['value']
					elif  len(sameAs_field_option_dict['FieldRef']) == 1:
						sameAs_dependent_field_name = sameAs_field_option_dict['FieldRef'][0]
						sameAs_dependent_field_dict = ticket_form_fields[ticket_form_fields_dict[sameAs_dependent_field_name]]
						if 'displayValue' in sameAs_dependent_field_dict:
							on_the_fly_resp = self.rs.ticket.ivanti_itsm_fetch_fieldValue_wrt_dependentField(ticket_form['ticketType'], self.itsm_url, self.itsm_api_token, available_option_records['FieldName'], reference_field['fieldName'], reference_field['valueKey'])
							dropdown_value_dict = {}
							sample_list = []
							for ind in range(len(on_the_fly_resp))	:
								dropdown_value_dict[on_the_fly_resp[ind]['label']] = on_the_fly_resp[ind]['value']
							if len(on_the_fly_resp) > 10:
								sample_list = on_the_fly_resp[:10]
								print(f"\nHere are some available options suggestion for '{field['label']}' field")
								for i,op in enumerate(sample_list):
									print(f"Index : {i} - Value : '{op['label']}'")		
								dropdown_suggestion_index = input("\nEnter the index of value you want to select. If the value that you are looking for is not displayed in the terminal, please enter 'no': ").strip().lower()			
								if dropdown_suggestion_index == 'no':
									user_satisfied = None
									while user_satisfied == None:
										search_pattern_match = []
										search_string = input(f"\nEnter the search string for '{field['label']}' field: ").strip().lower()
										for key,value in dropdown_value_dict.items():
											start_index = str(key).lower().find(search_string)
											if start_index != -1:
												search_pattern_match.append({key:value})
										if len(search_pattern_match) == 0:
											print("\nNo value that matches the search string. Search again!")
										else:
											print("\nHere are the available options that matches the search string")
											for ind in range(len(search_pattern_match)):
												print(f"Index : {ind} - Value : '{list(search_pattern_match[ind].keys())[0]}'")	
											dropdown_index = input("\nEnter the index of value you want to select. If the value that you are looking for is not displayed in the terminal, please enter 'no': ").strip().lower()	
											if dropdown_index == 'no':
												pass
											elif dropdown_index.isdigit() == True:
												if (int(dropdown_index) < 0) and (int(dropdown_index) >= len(search_pattern_match)):
													raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
												field['displayValue'] = list(search_pattern_match[int(dropdown_index)].keys())[0]
												field['valueKey'] = list(search_pattern_match[int(dropdown_index)].values())[0]
												user_satisfied = True		
											else:
												raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
								elif dropdown_suggestion_index.isdigit() == True:
									if (int(dropdown_suggestion_index) < 0) and (int(dropdown_suggestion_index) >= len(sample_list)):
										raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
									field['displayValue'] = on_the_fly_resp[int(dropdown_suggestion_index)]['label']
									field['valueKey'] = on_the_fly_resp[int(dropdown_suggestion_index)]['value']							
								else:
									raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")						
							elif len(on_the_fly_resp) <= 10:
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
								dropdown_value_dict = {}
								sample_list = []
								for ind in range(len(sameAs_field_option_dict['values'])):
									dropdown_value_dict[sameAs_field_option_dict['values'][ind]['Label']] = sameAs_field_option_dict['values'][ind]['value']	
								if len(sameAs_field_option_dict['values']) > 10:
									sample_list = sameAs_field_option_dict['values'][:10]
									print(f"\nHere are some available options suggestion for '{field['label']}' field")
									for i,op in enumerate(sample_list):
										print(f"Index : {i} - Value : '{op['Label']}'")		
									dropdown_suggestion_index = input("\nEnter the index of value you want to select. If the value that you are looking for is not displayed in the terminal, please enter 'no': ").strip().lower()			
									if dropdown_suggestion_index == 'no':
										user_satisfied = None
										while user_satisfied == None:
											search_pattern_match = []
											search_string = input(f"\nEnter the search string for '{field['label']}' field: ").strip().lower()
											for key,value in dropdown_value_dict.items():
												start_index = str(key).lower().find(search_string)
												if start_index != -1:
													search_pattern_match.append({key:value})
											if len(search_pattern_match) == 0:
												print("\nNo value that matches the search string. Search again!")
											else:
												print("\nHere are the available value that matches the search string")
												for ind in range(len(search_pattern_match)):
													print(f"Index : {ind} - Value : '{list(search_pattern_match[ind].keys())[0]}'")	
												dropdown_index = input("\nEnter the index of value you want to select. If the value that you are looking for is not displayed in the terminal, please enter 'no': ").strip().lower()	
												if dropdown_index == 'no':
													pass
												elif dropdown_index.isdigit() == True:
													if (int(dropdown_index) < 0) and (int(dropdown_index) >= len(search_pattern_match)):
														raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
													field['displayValue'] = list(search_pattern_match[int(dropdown_index)].keys())[0]
													field['valueKey'] = list(search_pattern_match[int(dropdown_index)].values())[0]
													user_satisfied = True		
												else:
													raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
									elif dropdown_suggestion_index.isdigit() == True:
										if (int(dropdown_suggestion_index) < 0) and (int(dropdown_suggestion_index) >= len(sample_list)):
											raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
										field['displayValue'] = sameAs_field_option_dict['values'][int(dropdown_suggestion_index)]['Label']
										field['valueKey'] = sameAs_field_option_dict['values'][int(dropdown_suggestion_index)]['value']							
									else:
										raise ValueError(f"Entered value for '{field['label']}' is not valid. Please enter a valid one.")
								elif len(sameAs_field_option_dict['values']) <= 10:
									print(f"\nHere are the available options for '{field['label']}' field")
									for i,op in enumerate(sameAs_field_option_dict['values']):
										print(f"Index : {i} - Value : '{op['Label']}'")		
									dropdown_index = int(input(f"\nEnter the index number of value you want to select for '{field['label']}' field: "))	
									field['displayValue'] = sameAs_field_option_dict['values'][dropdown_index]['Label']
									field['valueKey'] = sameAs_field_option_dict['values'][dropdown_index]['value']											
					elif len(sameAs_field_option_dict['FieldRef']) > 1:
						raise NotImplementedError('The logic is not implement for this scenario')

					
			else:
				raise NotImplementedError('The logic is not implement for this scenario')

		return field

	def form_validation(self, ticket_creation_body, ticket_form, selected_ticket_type, itsm_username='admin'):
		body = {"connectorCredentials":{"restApiKey":self.itsm_api_token,"url":self.itsm_url},"updatedValuesByUserList":[], "defaultValuefieldsList":[]}
		connector_api_body = {
			"name": self.itsm_connector_name,
			"type": "IVANTIITSM",
			"schedule": {
				"enabled": True,
				"type": "DAILY",
				"hourOfDay": 0
				},
			"attributes": {
				"username": itsm_username,
				"password": self.itsm_api_token
			},	
			"connection": {
				"url": self.itsm_url
			},
			"connectorField": {
				"type": "IVANTIITSM",
				"busObjType": selected_ticket_type,
				"descriptionFields": [],
				"userSelectedValues": [],
				"lockedFields": [],	
				"tagTypeDefaultValue": ticket_form['tagTypeDefaultValue'],
				"connectorSettings": {
					"closeFindingsOnTicketCloseEnabled": False,
					"closeStatusesOfTicketToUpdate": ",".join(ticket_form['ticketSyncStatus']),
					"closeTicketOnFindingsCloseEnabled": ticket_form['moveTicketState'],
					"closedStateKey": ticket_form['ticketCloseState']['value'],
					"closedStateLabel": ticket_form['ticketCloseState']['Label'],
					"enabledTagRemoval": ticket_form['enabledTagRemoval'],
					"enabledUploadAttachment": ticket_form['enabledUploadAttachment'],
					"initialState": ""
				},
				"usePluginInfoFields": [],
				"isTagRemovalEnabled": ticket_form['enabledTagRemoval'],
				"isTicketingConnector": True,
				"autoUrba": True				
			}			
		}

		for index, field in enumerate(ticket_creation_body):
			if 'valueKey' in field:
				body_dict = {"displayName":field['fieldName'],"name":field['fieldName'],"dirty":True,"fieldId":field['fieldName'],"value":field['valueKey']}
				body['updatedValuesByUserList'].append(body_dict)
		for index, field in enumerate(ticket_form['defaultFieldValues']):
			body_dict = {"displayName":field['key'],"name":field['key'],"dirty":True,"fieldId":field['key'],"value":field['label']}
			body['defaultValuefieldsList'].append(body_dict)
		response = self.rs.connectors.ivanti_itsm_fetch_validation(body, ticket_form['ticketType'])

		if response['isValid'] == False:
			print("\n\n---Form Validation Failed---\n\n")
			print(response)
			print("Please run the script again and rectify the mistakes mentioned in the above error message")
			sys.exit(0)
		elif response['isValid'] == True:
			print("\nForm Validation is successful")
			if 'slaDateField' in ticket_form:
				connector_api_body['connectorField']['slaDateField'] = ticket_form['slaDateField']			
			connector_api_body['connectorField']['usePluginInfoFields'].extend(ticket_form['pluingInfoUsedKeys'])
			for item in ticket_form['supportedDescriptionFields']:
				connector_api_body['connectorField']['descriptionFields'].append({"key": item['value'], "enabled": item['isCurrentlySelected']})
			for item in ticket_creation_body:
				if 'valueKey' in item:
					connector_api_body['connectorField']['userSelectedValues'].append({"displayValue": item['displayValue'], "value": item['valueKey'], "key": item['fieldName']})
			for item in ticket_form['lockedFields']:
				if item['isCurrentlySelected'] == True:
					connector_api_body['connectorField']['lockedFields'].append(item['value'])
		
		return connector_api_body













#  Execute the script
if __name__ == "__main__":
    try:
        ItsmCreateTool()
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
