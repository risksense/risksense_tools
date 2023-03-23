""" *******************************************************************************************************************
|
|  Name        :  main.py
|  Description :  Defender ATP vuln ingestion
|  Copyright   :  2022 RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|  Version     :  3.1.0
|  Note:       :  This version only write output where Health Status is 'Active' and Assets has at least 1 Vulnerability
******************************************************************************************************************* """

import os
import csv
import sys
import toml
import json
import time
import zipfile
import datetime
import logging
import requests
from upload_to_platform.upload_to_platform import UploadToPlatform
import argparse
from datetime import datetime
import pandas as pd


class DefenderDataIngester:

    """ DefenderDataIngester class """

    def __init__(self, api_key, _defender_token_url, _defender_tenant_id, _defender_client_id, _defender_client_secret):

        """ Main body of script """

        print("Starting script...")

        #Set acquired values
        self._defender_token_url = _defender_token_url
        self._defender_tenant_id = _defender_tenant_id
        self._defender_client_id = _defender_client_id
        self._defender_client_secret = _defender_client_secret

        #  Set up logging
        log_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'log', 'defender_output.log')
        logging.basicConfig(filename=log_file, level=logging.DEBUG,
                            format='%(levelname)s:  %(asctime)s > %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        logging.info("***** STARTING SCRIPT ********************************************************************")
        #logging.info(f"Date: {datetime.datetime.now()}")

        #  Read the config file
        conf_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'conf', 'config.toml')
        logging.info(f"Reading config file at \"{conf_file}\"")
        config = self._read_config_file(conf_file)

        #  Set variables based on config values
        rs_platform = config['risksense_platform']['url']
        output_file_folder = config['output']['file_folder']
        api_key = config['risksense_platform']['api_key']

        if self._defender_token_url == "":
            self._defender_token_url = config['defender']['token_url']
        if  self._defender_tenant_id == "":
            self._defender_tenant_id = config['defender']['tenant_id']
        if self._defender_client_id == "":
            self._defender_client_id = config['defender']['client_id']
        if self._defender_client_secret == "":
            self._defender_client_secret = config['defender']['client_secret']

        print(f" -    URL: {self._defender_token_url}")
        print(f" - Tenant: {self._defender_tenant_id}")
        print(f" - Client: {self._defender_client_id}")
        print(f" - Secret: {self._defender_client_secret}")

        self._debug_write_json = config['debug']['write_raw_json_responses']
        self._debug_host_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'debug_files', 'host_data.txt')
        self._debug_vuln_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'debug_files', 'vuln_data.txt')
        self._debug_vuln_detail_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'debug_files', 'vuln_detail_data.txt')

        #  If there is not an API KEY found in the configuration file, the
        #  script will check for an environmental variable called "RS_API_KEY".
        #  If not found there, the script will exit.

        if api_key == "":
            logging.info("No API key found in config. Checking environmental variables.")
            api_key = os.getenv('RS_API_KEY')
            if api_key is None:
                print()
                logging.info("No API key found in environmental variables. Exiting.")
                print("No API Key found. Exiting.")
                exit(1)



        output_filename = f"output_{str(time.time())}.csv"
        if not os.path.exists(os.path.join(os.path.abspath(os.path.dirname(__file__)), output_file_folder)):
            os.makedirs(os.path.join(os.path.abspath(os.path.dirname(__file__)), output_file_folder),exist_ok=True)
        self.output_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), output_file_folder, output_filename)

        upload_log = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'log', 'upload.log')
        auto_urba = config['upload_to_platform']['auto_urba']
        network_id = config['upload_to_platform']['network_id']
        if not network_id:
            network_id = None
        client_id = config['upload_to_platform']['client_id']
        if not client_id:
            client_id = None


        #  Read in host and vuln data

        print(f"Attempting to get a Defender access token")
        try:
            _defender_access_token = self._get_defender_token()
            print()
        except Exception as ex:
            _defender_access_token = None
            print("An error has occurred while trying to get an access token from Defender. Exiting.")
            logging.error("An error has occurred while trying to get an access token from Defender")
            logging.error(ex)


        logging.info("Defender access token retrieved")
        #print(_defender_access_token)

        print(f"Attempting to get Defender host data")
        try:
            _raw_host_data = self._get_defender_machines(_defender_access_token)
            print("Fetching machine data complete "+str(len(_raw_host_data))+" machines fetched")
            #self.raw_csv_write(_raw_host_data, 'raw_host_data.csv')
        except Exception as ex:
            _raw_host_data = None
            print("An error has occurred while trying to get machine data from Defender. Exiting.")
            logging.error("An error has occurred while trying to get machine data from Defender")
            logging.error(ex)
            exit(1)
        print(f" - {len(_raw_host_data)} Hosts returned")
        logging.info("Raw Defender host data retrieved")

        print(f"Attempting to get Defender vuln data")
        try:
            _raw_vuln_data = self._get_defender_vulns(_defender_access_token)
            print("Fetching raw Defender vuln data complete")
            #self.raw_csv_write(_raw_vuln_data, 'raw_vuln_data.csv')
        except Exception as ex:
            _raw_vuln_data = None
            print("An error has occurred while trying to get vuln data from Defender. Exiting.")
            print(ex)
            logging.error("An error has occurred while trying to get vuln data from Defender")
            logging.error(ex)
            exit(1)
        print(f" - {len(_raw_vuln_data)} vulns returned")
        logging.info("Raw Defender vuln data retrieved")

        print("Attempting to get vuln details from Defender")
        try:
            _raw_vuln_details = self._get_defender_vuln_details(_defender_access_token)
            print("Fetching raw Defender vuln details data complete")
        except Exception as ex:
            _raw_vuln_details = None
            print("An error has occurred while trying to get vuln details from Defender. Exiting.")
            print(ex)
            logging.error("An error has occurred while trying to get vuln details from Defender")
            logging.error(ex)
            exit(1)
        print(f" - Details returned for {len(_raw_vuln_details)} vulns.")
        logging.info("Raw Defender vuln details retrieved.")

        #  Reformat the Defender data correlating vulns to machine to increase speed and efficiency
        print("Scrubbing the host and vuln data")
        _host_data = self._process_host_data(_raw_host_data)
        _vuln_data = self._process_vuln_data(_raw_vuln_data)
        _vuln_descs = self._process_vuln_details(_raw_vuln_details)

        _scrubbed_data = self._data_mashup(_host_data, _vuln_data)
        logging.info("Host and vuln data have been scrubbed and correlated")

        #  Write Scrubbed data to a csv file
        print("Writing data to csv file for ingestion.")

        self._write_csv_file(_scrubbed_data, _vuln_descs)
        logging.info(f"Retrieved data has been written to {self.output_file_path}")

        #  Zip up output file

        print("Zipping up the csv file")
        os.chdir(output_file_folder)
        zipfile.ZipFile(output_filename.split(".")[0] + ".zip", mode='w', compression=zipfile.ZIP_DEFLATED).write(output_filename)
        os.remove(output_filename)
        os.chdir("..")
        print(" - File zipped")

        #  Upload the file to the platform
        logging.info("Beginning upload process")
        print("Attempting begin the upload of csv data to RiskSense platform.")

        #UploadToPlatform(rs_platform, api_key, output_file_folder, upload_log, auto_urba, client_id, network_id)

    def _write_csv_file(self, scrubbed_data, vuln_details):

        """
        Write the scrubbed data to a CSV file to be ingested into RiskSense platform.

        :param scrubbed_data:   Scrubbed Defender data
        :type  scrubbed_data:   dict
        """

        severity = {
            "Info": 0.0,
            "Low": 3.9,
            "Medium": 6.9,
            "High": 8.9,
            "Critical": 10.0
        }

        today = datetime.today().strftime('%Y-%m-%d')

        csv_header = [
            "aadDeviceId",
            "agentVersion",
            "computerDnsName",
            "deviceValue",
            "exposureLevel",
            "firstSeen",
            "healthStatus",
            "lastExternalIpAddress",
            "lastIpAddress",
            "lastSeen",
            "machineTags",
            "osBuild",
            "osPlatform",
            "osProcessor",
            "osVersion",
            "rbacGroupId",
            "rbacGroupName",
            "riskScore",
            "version",
            "cveId",
            "fixingKbId",
            "id",
            "discoveredOn",
            "productName",
            "productVendor",
            "productVersion",
            "severity",
            "title",
            "description",
            "pluginId"
        ]

        with open(self.output_file_path, 'w', newline='\n', encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            csv_writer.writerow(csv_header)

            for machine in scrubbed_data:

                for vuln in scrubbed_data[machine]['vulns']:

                    #pluginId = "INFO-MDATP"

                    if vuln['cveId'] in vuln_details:
                        pluginId = vuln['cveId']
                        vuln_description = vuln_details[vuln['cveId']]
                        if vuln_description == "":
                            vuln_description = "See CVE description."
                    else:
                        pluginId = vuln['cveId']
                        vuln_description = "See CVE description."



                    #if vuln['cveId'] == "":
                        #pluginId = "INFO-MDATP"
                    healthStatus = scrubbed_data[machine]['properties']['healthStatus']

                    if vuln['fixingKbId'] is not None:
                        kb_link = f"https://www.catalog.update.microsoft.com/Search.aspx?q=KB{vuln['fixingKbId']}"
                    else:
                        kb_link = "No KB entry provided."

                    if vuln['severity'] is not None:
                        vuln_severity = vuln['severity']
                        if vuln_severity in severity:
                            vuln_severity_score = severity[vuln_severity]
                    else:
                        #default value
                        vuln_severity_score = 0.0

                    vuln_title = "{0}_{1}_{2}_{3}".format(vuln['productVendor'].title(),vuln['productName'].title(),vuln['productVersion'],vuln['cveId'])

                    if vuln_title == '___':
                        vuln_severity_score = 0.0

                    row = [
                        scrubbed_data[machine]['properties']['aadDeviceId'],
                        scrubbed_data[machine]['properties']['agentVersion'],
                        str(scrubbed_data[machine]['properties']['computerDnsName']).split('.')[0],
                        scrubbed_data[machine]['properties']['deviceValue'],
                        scrubbed_data[machine]['properties']['exposureLevel'],
                        str(scrubbed_data[machine]['properties']['firstSeen'].split('T')[0]).replace('/', '-'),
                        scrubbed_data[machine]['properties']['healthStatus'],
                        scrubbed_data[machine]['properties']['lastExternalIpAddress'],
                        scrubbed_data[machine]['properties']['lastIpAddress'],
                        str(scrubbed_data[machine]['properties']['lastSeen'].split('T')[0]).replace('/', '-'),
                        scrubbed_data[machine]['properties']['machineTags'],
                        scrubbed_data[machine]['properties']['osBuild'],
                        scrubbed_data[machine]['properties']['osPlatform'],
                        scrubbed_data[machine]['properties']['osProcessor'],
                        scrubbed_data[machine]['properties']['osVersion'],
                        scrubbed_data[machine]['properties']['rbacGroupId'],
                        scrubbed_data[machine]['properties']['rbacGroupName'],
                        scrubbed_data[machine]['properties']['riskScore'],
                        scrubbed_data[machine]['properties']['version'],
                        vuln['cveId'],
                        kb_link,
                        vuln['id'],
                        today,
                        vuln['productName'].title(),
                        vuln['productVendor'].title(),
                        vuln['productVersion'],
                        vuln_severity_score,
                        "{0}_{1}_{2}_{3}".format(vuln['productVendor'].title(),vuln['productName'].title(),vuln['productVersion'],vuln['cveId']),
                        vuln_description,
                        pluginId
                    ]

                    #if healthStatus == 'Active':
                    csv_writer.writerow(row)

    @staticmethod
    def raw_csv_write(raw_data, filename):
        print("Writing raw data to csv file")
        df = pd.DataFrame(raw_data)
        df.to_csv(filename, index = False, encoding = "utf-8")


    @staticmethod
    def _data_mashup(host_data, vuln_data):

        """
        Correlate and combine Defender host data and vuln data

        :param host_data:   Host data from Defender
        :type  host_data:   dict

        :param vuln_data:   Vuln data from Defender
        :type  vuln_data:   dict

        :return:    New dict correlating host details and associated vulns
        :rtype:     dict
        """

        scrubbed_vuln_data = {}

        logging.info(f"Scrubbing and correlating host/vuln data.")
        for item in vuln_data:
            if item in host_data:
                scrubbed_vuln_data.update({item: vuln_data[item]})
            else:
                logging.info(f"No host data found for {item}")

        for item in host_data:
            if item in scrubbed_vuln_data:
                scrubbed_vuln_data[item].update({'properties': host_data[item]})
            else:
                logging.info(f"No vulns found for {item}")
                scrubbed_vuln_data[item] = {'vulns': [{'id':None,'cveId':'','productName':'','productVendor':'','productVersion':'','severity':'','fixingKbId':None}]}
                scrubbed_vuln_data[item].update({'properties': host_data[item]})
                continue

        logging.info(f"Done scrubbing and correlating host/vuln data.")

        return scrubbed_vuln_data

    @staticmethod
    def _process_host_data(host_data):

        """
        Convert the host data to a dict keyed off of 'id'.  Will make correlation easier and faster.

        :param host_data:   Host data as read from Defender JSON.
        :type  host_data:   list

        :return:    Host data as dict, keyed off of 'id'
        :rtype:     dict
        """

        new_dict = {}

        for item in host_data:
            host_id = item['id']
            try:
                item.pop('id')
            except KeyError as ex:
                logging.error(f"There was an error processing {item} while processing host data.")
                logging.error(ex)
                continue

            new_dict.update({host_id: item})

        return new_dict

    @staticmethod
    def _process_vuln_data(vuln_data):

        """
        Convert the vuln data to a dict keyed off of 'machineId', with vulns associated as list.
        Will make correlation easier and much faster.

        :param vuln_data:   Vuln data as read from Defender JSON.
        :type  vuln_data:   list

        :return:    Vuln data as dict, keyed off of 'machineId', and aggregated
                    into an associated list for each machine
        :rtype:     dict
        """

        new_dict = {}

        for item in vuln_data:
            host_id = item['machineId']
            try:
                item.pop('machineId')
            except KeyError as ex:
                logging.error(f"There was an error while processing {item} while processing vuln data")
                logging.error(ex)
                continue

            if host_id not in new_dict:
                new_dict.update({host_id: {'vulns': [item]}})
            else:
                new_dict[host_id]['vulns'].append(item)

        return new_dict

    @staticmethod
    def _process_vuln_details(vuln_details):

        new_dict = {}

        for item in vuln_details:
            cve_id = item['id']
            cve_disc = item['description']
            new_dict[cve_id] = cve_disc

        return new_dict

    @staticmethod
    def _read_json_file(filename):

        """
        Read a JSON file

        :param filename:    Path to file to be read
        :type  filename:    str

        :return:    JSON data contained in the file
        :rtype:     json
        """

        try:
            with open(filename) as f:
                read_data = json.load(f)
        except (FileNotFoundError, Exception) as ex:
            print(f"An error has occurred while trying to read file \"{filename}\"")
            print(ex)
            print("Exiting")
            exit(1)

        return read_data

    def _get_defender_token(self):

        url = f"https://login.microsoftonline.com/{self._defender_tenant_id}/oauth2/token"
        scope_uri = "https://api.securitycenter.microsoft.com"
        payload = {
            "resource": scope_uri,
            "client_id": self._defender_client_id,
            "client_secret": self._defender_client_secret,
            "grant_type": "client_credentials"
        }
        files = {}
        headers = {}

        try:
            raw_response = requests.request("POST", url, headers=headers, data=payload, files=files)
            if raw_response.status_code != 200:
                print(raw_response.text)
                raise ValueError("Attempt to get defender token was unsuccessful.")
        except Exception:
            raise

        jsonified_response = json.loads(raw_response.text)
        access_token = jsonified_response['access_token']

        return access_token

    def _get_defender_machines(self, access_token):

        """
        Get defender host data via API

        :param access_token:    Defender API access token
        :type  access_token:    str

        :return:    Defender host data
        :rtype:     list
        """

        all_machines = []

        url = "https://api.securitycenter.windows.com/api/machines"

        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        try:
            raw_response = requests.request("GET", url, headers=headers)
            #print(raw_response.text)
            if raw_response.status_code != 200:
                raise ValueError("Attempt to get defender machine information was unsuccessful.")
            if self._debug_write_json:
                with open(self._debug_host_file_path, 'w', encoding='utf-8') as host_file:
                    host_file.write(raw_response.text)

        except Exception:
            raise

        jsonified_response = json.loads(raw_response.text)
        all_machines += jsonified_response['value']

        try:
            next_page = jsonified_response['@odata.nextLink']
        except KeyError:
            return all_machines

        while '@odata.nextLink' in jsonified_response:
            try:
                raw_response = requests.request("GET", next_page, headers=headers)
                if raw_response.status_code != 200:
                    #print(raw_response.text)
                    raise ValueError("Attempt to get defender machine information was unsuccessful.")
                if self._debug_write_json:
                    with open(self._debug_host_file_path, 'a', encoding='utf-8') as host_file:
                        host_file.write(raw_response.text)
            except Exception:
                raise

            jsonified_response = json.loads(raw_response.text)
            try:
                all_machines += jsonified_response['value']
                next_page = jsonified_response['@odata.nextLink']
            except KeyError:
                break

        return all_machines

    def _get_defender_vulns(self, access_token):

        """
        Get Defender vuln data via API

        :param access_token:    Defender API access token
        :type  access_token:    str

        :return:    Defender vuln data
        :rtype:     list
        """

        all_vulns = []

        url = "https://api.securitycenter.windows.com/api/vulnerabilities/machinesVulnerabilities"

        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        pages_fetched = 1
        try:
            raw_response = requests.request("GET", url, headers=headers)
            if raw_response.status_code != 200:
                if raw_response.status_code == 401:
                    jsonified_response = json.loads(raw_response.text)
                    try:
                        all_vulns += jsonified_response['value']
                    except KeyError:
                        print("No data anymore")
                    return all_vulns
                else:
                    raise ValueError("Attempt to get defender vuln information was unsuccessful.")
            if self._debug_write_json:
                with open(self._debug_vuln_file_path, 'w', encoding='utf-8') as vuln_file:
                    vuln_file.write(raw_response.text)
        except Exception:
            raise

        jsonified_response = json.loads(raw_response.text)
        all_vulns += jsonified_response['value']

        try:
            next_page = jsonified_response['@odata.nextLink']
        except KeyError:
            #print("++++++++++++++++++++No next Page??+++++++++++++++++++++++++++++++++")
            #exit(1)
            return all_vulns

        while '@odata.nextLink' in jsonified_response:
            pages_fetched+=1
            try:
                raw_response = requests.request("GET", next_page, headers=headers)
                if raw_response.status_code != 200:
                    if raw_response.status_code == 401:
                        jsonified_response = json.loads(raw_response.text)
                        try:
                            all_vulns += jsonified_response['value']
                        except KeyError:
                            print("No data anymore")
                        print("Pages fetched = "+str(pages_fetched))
                        return all_vulns
                    else:
                        raise ValueError("Attempt to get defender vuln information was unsuccessful.")
                if self._debug_write_json:
                    with open(self._debug_vuln_file_path, 'a', encoding='utf-8') as vuln_file:
                        vuln_file.write(raw_response.text)
            except Exception:
                raise

            jsonified_response = json.loads(raw_response.text)
            try:
                all_vulns += jsonified_response['value']
                next_page = jsonified_response['@odata.nextLink']
            except KeyError:
                break

        print("Pages fetched = "+str(pages_fetched))
        return all_vulns

    def _get_defender_vuln_details(self, access_token):

        """
        Get Defender vuln data via API

        :param access_token:    Defender API access token
        :type  access_token:    str

        :return:    Defender vuln data
        :rtype:     list
        """

        all_vuln_details = []

        url = "https://api.securitycenter.windows.com/api/Vulnerabilities"

        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        try:
            raw_response = requests.request("GET", url, headers=headers)
            if raw_response.status_code != 200:
                if raw_response.status_code == 401:
                    jsonified_response = json.loads(raw_response.text)
                    try:
                        all_vuln_details += jsonified_response['value']
                    except KeyError:
                        print("No data anymore")
                    return all_vuln_details
                else:
                    raise ValueError("Attempt to get defender vuln information was unsuccessful.")
            if self._debug_write_json:
                with open(self._debug_vuln_detail_file_path, 'w', encoding='utf-8') as vuln_detail_file:
                    vuln_detail_file.write(raw_response.text)
        except Exception:
            raise

        jsonified_response = json.loads(raw_response.text)
        all_vuln_details += jsonified_response['value']

        try:
            next_page = jsonified_response['@odata.nextLink']
        except KeyError:
            return all_vuln_details

        while '@odata.nextLink' in jsonified_response:
            try:
                raw_response = requests.request("GET", next_page, headers=headers)
                if raw_response.status_code != 200:
                    if raw_response.status_code == 401:
                        jsonified_response = json.loads(raw_response.text)
                        try:
                            all_vuln_details += jsonified_response['value']
                        except KeyError:
                            print("No data anymore")
                        return all_vuln_details
                    else:
                        raise ValueError("Attempt to get defender vuln information was unsuccessful.")
                if self._debug_write_json:
                    with open(self._debug_vuln_detail_file_path, 'a', encoding='utf-8') as vuln_detail_file:
                        vuln_detail_file.write(raw_response.text)
            except Exception:
                raise

            jsonified_response = json.loads(raw_response.text)
            try:
                all_vuln_details += jsonified_response['value']
                next_page = jsonified_response['@odata.nextLink']
            except KeyError:
                break

        return all_vuln_details

    @staticmethod
    def _read_config_file(filename):

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
            print("Error reading configuration file. Exiting.")
            print(ex)
            print()
            exit(1)


#  Execute the script
if __name__ == "__main__":


    parser = argparse.ArgumentParser(description='Credentials required: RiskSense API Key, Defender Token URL, Defender Tenant ID, Defender Client ID and Secret.\nSee README.md for details on how to pass arguments\n')

    #Add arguments to parser
    parser.add_argument('--rsapikey', type=str, required=False, help='Risksense API Key required', default='')
    parser.add_argument('--tokenurl', type=str, required=False, help='Defender Token URL required', default='')
    parser.add_argument('--tenantid', type=str, required=False, help='Defender Tenant ID required', default='')
    parser.add_argument('--clientid', type=str, required=False, help='Defender Client ID required', default='')
    parser.add_argument('--secret', type=str, required=False, help='Defender Client Secret required', default='')

    args = parser.parse_args()

    api_key = args.rsapikey                                                     #RiskSense API Key
    _defender_token_url = args.tokenurl                                         #Defender Token URL
    _defender_tenant_id = args.tenantid                                         #Defender Tenant ID
    _defender_client_id = args.clientid                                         #Defender Client ID
    _defender_client_secret = args.secret                                       #Defender Client Secret

    try:
        DefenderDataIngester(api_key, _defender_token_url, _defender_tenant_id, _defender_client_id, _defender_client_secret)
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
