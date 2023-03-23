""" *******************************************************************************************************************
|
|  Name        :  snow_incident_connector_create.py
|  Description :  Service Now Incident connector creation
|  Project     :  risksense_tools
|  Copyright   :  (c) RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

from http import client
import os
import sys
import toml
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'lib'))
import risksense_api as rsapi


class Cherwellconnectortool:
	""" SnowIncidentConnectorTool class """

	def __init__(self):
		""" Main body of script """

		conf_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf', 'config.toml')
		config = self.read_config_file(conf_file)
		self.rs_platform = config['platform_url']
		self.api_key = config['api_key']
		self.cherwellurl = config['cherwell_url']
		self.cherwellname=config['cherwell_name']
		self.cherwell_username = config['cherwell_username']
		self.cherwell_password	= config['cherwell_password']
		self.cherwell_clientidkey = config['cherwell_clientidkey']
		self.cherwell_priority=config['cherwell_priority']
		self.cherwell_description=config['cherwell_description']
		self.cherwell_title=config['cherwell_title']
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

		try:
			self.connector_id = self.rs.connectors.create_cherwell_problem_connector(self.cherwellname,self.cherwell_username,self.cherwell_password,self.cherwell_clientidkey,self.cherwellurl,self.cherwell_priority,self.cherwell_description,self.cherwell_title)			
			print(f"[+] Connector ID - {self.connector_id}, Cherwell Service type connector created successfully!")
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


#  Execute the script
if __name__ == "__main__":
    try:
        Cherwellconnectortool()
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
