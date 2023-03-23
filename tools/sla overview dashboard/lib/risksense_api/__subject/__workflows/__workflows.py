""" *******************************************************************************************************************
|
|  Name        :  __workflows.py
|  Description :  Create functions for various utilities of the workflow endpoints
|  Project     :  risksense_api
|  Copyright   :  2022 RiskSense, Inc.
|  License     :  Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)
|
******************************************************************************************************************* """

import json
from ...__subject import Subject
from ..._params import *
from ..._api_request_handler import *
import datetime


class Workflows(Subject):

    """ Workflows class """

    def __init__(self, profile):

        """
        Initialization of Workflows object.

        :param profile:     Profile Object
        :type  profile:     _profile
        """

        self.subject_name = "workflowBatch"
        Subject.__init__(self, profile, self.subject_name)

    def search(self, search_filters, projection=Projection.BASIC, page_size=150,
               sort_field=SortField.ID, sort_dir=SortDirection.ASC, client_id=None):

        """
        Searches for and returns hosts based on the provided filter(s) and other parameters.  Rather
        than returning paginated results, this function cycles through all pages of results and returns
        them all in a single list.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param projection:      Projection to be used in API request.  Projection.BASIC or Projection.DETAIL
        :type  projection:      Projection attribute

        :param page_size:       The number of results per page to be returned.
        :type  page_size:       int

        :param sort_field:      The field to be used for sorting results returned.
        :type  sort_field:      SortField attribute

        :param sort_dir:        The direction of sorting to be used. SortDirection.ASC or SortDirection.DESC
        :type  sort_dir:        SortDirection attribute

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    A list containing all hosts returned by the search using the filter provided.
        :rtype:     list

        :raises RequestFailed:
        :raises Exception:
        """

        func_args = locals()
        func_args.pop('self')

        if client_id is None:
            client_id, func_args['client_id'] = self._use_default_client_id()

        try:
            page_info = self._get_page_info(self.subject_name, search_filters, page_size=page_size, client_id=client_id)
            num_pages = page_info[1]
        except RequestFailed:
            raise

        page_range = range(0, num_pages)

        try:
            all_results = self._search(self.subject_name, self.get_single_search_page, page_range, **func_args)
        except (RequestFailed, Exception):
            raise

        return all_results

    def get_single_search_page(self, search_filters, projection=Projection.BASIC, page_num=0, page_size=150,
                               sort_field=SortField.ID, sort_dir=SortDirection.ASC, client_id=None):

        """
        Searches for and returns hosts based on the provided filter(s) and other parameters.

        :param search_filters:  A list of dictionaries containing filter parameters.
        :type  search_filters:  list

        :param projection:      Projection to be used in API request.  Projection.BASIC or Projection.DETAIL
        :type  projection:      Projection attribute

        :param page_num:        The page number of results to be returned.
        :type  page_num:        int

        :param page_size:       The number of results per page to be returned.
        :type  page_size:       int

        :param sort_field:      The field to be used for sorting results returned.
        :type  sort_field:      SortField attribute

        :param sort_dir:        The direction of sorting to be used. SortDirection.ASC or SortDirection.DESC
        :type  sort_dir:        SortDirection attribute

        :param client_id:       Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:       int

        :return:    The JSON response from the platform is returned.
        :rtype:     dict

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/search"

        body = {
            "filters": search_filters,
            "projection": projection,
            "sort": [
                {
                    "field": sort_field,
                    "direction": sort_dir
                }
            ],
            "page": page_num,
            "size": page_size
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)

        return jsonified_response

    def get_model(self, client_id=None):

        """
        Get available projections and models for Networks.

        :param client_id:   Client ID
        :type  client_id:   int

        :return:    Networks projections and models are returned.
        :rtype:     dict

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            response = self._model(self.subject_name, client_id)
        except RequestFailed:
            raise

        return response

    def suggest(self, search_filter_1, search_filter_2, client_id=None):

        """
        Suggest values for filter fields.

        :param search_filter_1:     Search Filter 1
        :type  search_filter_1:     list

        :param search_filter_2:     Search Filter 2
        :type  search_filter_2:     list

        :param client_id:           Client ID
        :type  client_id:           int

        :return:    Value suggestions
        :rtype:     list

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        try:
            response = self._suggest(self.subject_name, search_filter_1, search_filter_2, client_id)
        except RequestFailed:
            raise

        return response


    def request_acceptance(self, finding_type, search_filter, workflow_name, description, reason, override_control, compensating_controls="NONE", expiration_date=None, attachment=None, client_id=None):

        """
        Request acceptance for applicationFindings / hostfFindings as defined in the filter_request parameter.

        :param finding_type:            Finding type. Possible options : ("hostFinding" or "applicationFinding")
        :type  finding_type:            str

        :param search_filter:           A list of dictionaries containing filter parameters.
        :type  search_filter:           list

        :param workflow_name:           Workflow Name
        :type  workflow_name:           str

        :param description:             A description of the request.
        :type  description:             str

        :param reason:                  A reason for the request.
        :type  reason:                  str

        :param override_control:        A description of override controls applied to this finding. Option available : ('NONE', 'AUTHORIZED')
        :type  override_control:        str

        :param compensating_controls:   A description of compensating controls applied to this finding. Option available : ("DLP", "Deemed not exploitable", "Endpoint Security", "IDS/IPS", "MFA Enforced", "Multiple: See Description", "Network Firewall", "Network Segmentation", "Other: See Description", "Web Application Firewall" or "NONE")
        :type  compensating_controls:   str

        :param expiration_date:         An expiration date.  Should be in "YYYY-MM-DD" format.
        :type  expiration_date:         str

        :param attachment:              A path to a file to be uploaded and attached to the request.
        :type  attachment:              str

        :param client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:               int

        :return:    The job ID within the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/acceptance/request"

        body = {"subject": finding_type, 
            "filterRequest": {
                "filters": search_filter
                }
            }
        multiform_data = {
            "name": (None,workflow_name),
            "subjectFilterRequest": (None,json.dumps(body)),
            "description": (None,description),
            "reason": (None,reason),
            "overrideControl": (None,override_control),
            "compensatingControls": (None,compensating_controls),
            "files": attachment,
            "expirationDate": (None,expiration_date),
            "isEmptyWorkflow":(None,"false")
            }

        body = self._strip_nones_from_dict(body)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, files=multiform_data)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id


    def request_false_positive(self, finding_type, search_filter, workflow_name, description, reason, override_control, expiration_date=None, attachment=None, client_id=None):

        """
        Request false positive for applicationFindings / hostFindings as defined in the filter_request parameter.

        :param finding_type:            Finding type. Possible options : ("hostFinding" or "applicationFinding")
        :type  finding_type:            str

        :param search_filter:           A list of dictionaries containing filter parameters.
        :type  search_filter:           list

        :param workflow_name:           Workflow Name
        :type  workflow_name:           str

        :param description:             A description of the request.
        :type  description:             str

        :param reason:                  A reason for the request.
        :type  reason:                  str

        :param override_control:        A description of override controls applied to this finding. Option available : ('NONE', 'AUTHORIZED')
        :type  override_control:        str

        :param expiration_date:         An expiration date.  Should be in "YYYY-MM-DD" format.
        :type  expiration_date:         str

        :param attachment:              A path to a file to be uploaded and attached to the request.
        :type  attachment:              str

        :param client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:               int

        :return:    The job ID within the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/falsePositive/request"

        body = {"subject": finding_type, 
            "filterRequest": {
                "filters": search_filter
                }
            }
        multiform_data = {
            "name": (None,workflow_name),
            "subjectFilterRequest": (None,json.dumps(body)),
            "description": (None,description),
            "reason": (None,reason),
            "overrideControl": (None,override_control),
            "files": attachment,
            "expirationDate": (None,expiration_date),
            "isEmptyWorkflow":(None,"false")
            }

        body = self._strip_nones_from_dict(body)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, files=multiform_data)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id


    def request_remediation(self, finding_type, search_filter, workflow_name, description, reason, override_control, expiration_date=None, attachment=None, client_id=None):

        """
        Request remediation for applicationFindings / hostFindings as defined in the filter_request parameter.

        :param finding_type:            Finding type. Possible options : ("hostFinding" or "applicationFinding")
        :type  finding_type:            str

        :param search_filter:           A list of dictionaries containing filter parameters.
        :type  search_filter:           list

        :param workflow_name:           Workflow Name
        :type  workflow_name:           str

        :param description:             A description of the request.
        :type  description:             str

        :param reason:                  A reason for the request.
        :type  reason:                  str

        :param override_control:        A description of override controls applied to this finding. Option available : ('NONE', 'AUTHORIZED')
        :type  override_control:        str

        :param expiration_date:         An expiration date.  Should be in "YYYY-MM-DD" format.
        :type  expiration_date:         str

        :param attachment:              A path to a file to be uploaded and attached to the request.
        :type  attachment:              str

        :param client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:               int

        :return:    The job ID within the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/remediation/request"

        body = {"subject": finding_type, 
            "filterRequest": {
                "filters": search_filter
                }
            }
        multiform_data = {
            "name": (None,workflow_name),
            "subjectFilterRequest": (None,json.dumps(body)),
            "description": (None,description),
            "reason": (None,reason),
            "overrideControl": (None,override_control),
            "files": attachment,
            "expirationDate": (None,expiration_date),
            "isEmptyWorkflow":(None,"false")
            }

        body = self._strip_nones_from_dict(body)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, files=multiform_data)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def request_severity_change(self, finding_type, search_filter, workflow_name, description, reason, override_control, severity_change, expiration_date=None, attachment=None, client_id=None):

        """
        Request severity change for applicationFindings / hostFindings as defined in the filter_request parameter.

        :param finding_type:            Finding type. Possible options : ("hostFinding" or "applicationFinding")
        :type  finding_type:            str

        :param search_filter:           A list of dictionaries containing filter parameters.
        :type  search_filter:           list

        :param workflow_name:           Workflow Name
        :type  workflow_name:           str

        :param description:             A description of the request.
        :type  description:             str

        :param reason:                  A reason for the request.
        :type  reason:                  str

        :param override_control:        A description of override controls applied to this finding. Option available : ('NONE', 'AUTHORIZED')
        :type  override_control:        str

        :param compensating_controls:   Severity change for this finding. Option available : ("1" to "10")
        :type  compensating_controls:   str

        :param expiration_date:         An expiration date.  Should be in "YYYY-MM-DD" format.
        :type  expiration_date:         str

        :param attachment:              A path to a file to be uploaded and attached to the request.
        :type  attachment:              str

        :param client_id:               Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:               int

        :return:    The job ID within the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.api_base_url.format(str(client_id)) + "/severityChange/request"

        body = {"subject": finding_type, 
            "filterRequest": {
                "filters": search_filter
                }
            }
        multiform_data = {
            "name": (None,workflow_name),
            "subjectFilterRequest": (None,json.dumps(body)),
            "description": (None,description),
            "reason": (None,reason),
            "overrideControl": (None,override_control),
            "severity": (None,severity_change),
            "files": attachment,
            "expirationDate": (None,expiration_date),
            "isEmptyWorkflow":(None,"false")
            }

        body = self._strip_nones_from_dict(body)

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, files=multiform_data)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def reject_acceptance(self, filter_request, description, client_id=None):

        """
        Reject an acceptance request.

        :param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param description:         A description of the rejection.
        :type  description:         str

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        search_response = self.get_single_search_page(filter_request)
        uuid = search_response['_embedded']['workflowBatches'][0]['uuid']

        url = self.api_base_url.format(str(client_id)) + "/acceptance/reject"

        body = {
            "workflowBatchUuid":uuid,
            "description":description
            }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def reject_false_positive(self, filter_request, description, client_id=None):

        """
        Reject a false positive request.

        :param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param description:         A description of the rejection.
        :type  description:         str

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        search_response = self.get_single_search_page(filter_request)
        uuid = search_response['_embedded']['workflowBatches'][0]['uuid']

        url = self.api_base_url.format(str(client_id)) + "/falsePositive/reject"

        body = {
            "workflowBatchUuid":uuid,
            "description":description
            }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def reject_remediation(self, filter_request, description, client_id=None):

        """
        Reject a remediation request.

        :param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param description:         A description of the rejection.
        :type  description:         str

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        search_response = self.get_single_search_page(filter_request)
        uuid = search_response['_embedded']['workflowBatches'][0]['uuid']

        url = self.api_base_url.format(str(client_id)) + "/remediation/reject"

        body = {
            "workflowBatchUuid":uuid,
            "description":description
            }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def reject_severity_change(self, filter_request, description, client_id=None):

        """
        Reject a severity change request.

        param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param description:         A description of the rejection.
        :type  description:         str

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        search_response = self.get_single_search_page(filter_request)
        uuid = search_response['_embedded']['workflowBatches'][0]['uuid']

        url = self.api_base_url.format(str(client_id)) + "/severityChange/reject"

        body = {
            "workflowBatchUuid":uuid,
            "description":description
            }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id


    def rework_acceptance(self, filter_request, description, client_id=None):

        """
        Request a rework of an acceptance.

        :param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param description:         A description of the rework.
        :type  description:         str

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        search_response = self.get_single_search_page(filter_request)
        uuid = search_response['_embedded']['workflowBatches'][0]['uuid']

        url = self.api_base_url.format(str(client_id)) + "/acceptance/rework"

        body = {
            "workflowBatchUuid":uuid,
            "description":description
            }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def rework_false_positive(self, filter_request, description, client_id=None):

        """
        Request a rework of a false positive.

        :param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param description:         A description of the rework.
        :type  description:         str

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        search_response = self.get_single_search_page(filter_request)
        uuid = search_response['_embedded']['workflowBatches'][0]['uuid']

        url = self.api_base_url.format(str(client_id)) + "/falsePositive/rework"

        body = {
            "workflowBatchUuid":uuid,
            "description":description
            }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def rework_remediation(self, filter_request, description, client_id=None):

        """
        Request a rework of a remediation.

        :param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param description:         A description of the rework.
        :type  description:         str

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        search_response = self.get_single_search_page(filter_request)
        uuid = search_response['_embedded']['workflowBatches'][0]['uuid']

        url = self.api_base_url.format(str(client_id)) + "/remediation/rework"

        body = {
            "workflowBatchUuid":uuid,
            "description":description
            }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def rework_severity_change(self, filter_request, description, client_id=None):

        """
        Request a rework of a severity change.

        :param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param description:         A description of the rework.
        :type  description:         str

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        search_response = self.get_single_search_page(filter_request)
        uuid = search_response['_embedded']['workflowBatches'][0]['uuid']

        url = self.api_base_url.format(str(client_id)) + "/severityChange/rework"

        body = {
            "workflowBatchUuid":uuid,
            "description":description
            }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id


    def approve_acceptance(self, filter_request, override_exp_date=False,
                           expiration_date=(datetime.date.today() + datetime.timedelta(days=14)), client_id=None):

        """
        Approve a acceptance request.

        :param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param override_exp_date:   True/False indicating whether or not an expiration date should be overridden.
        :type  override_exp_date:   bool

        :param expiration_date:     An expiration date for the approval.  Should be in "YYYY-MM-DD" format.
        :type  expiration_date:     str

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        search_response = self.get_single_search_page(filter_request)
        
        uuid = search_response['_embedded']['workflowBatches'][0]['uuid']
        print(uuid)
        url = self.api_base_url.format(str(client_id)) + "/acceptance/approve"

        body = {
            "workflowBatchUuid": uuid,
            "expirationDate": str(expiration_date),
            "overrideExpirationDate": override_exp_date
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def approve_false_positive(self, filter_request, override_exp_date=False,
                               expiration_date=(datetime.date.today() + datetime.timedelta(days=14)), client_id=None):

        """
        Approve a false positive change request.

        :param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param override_exp_date:   True/False indicating whether or not an expiration date should be overridden.
        :type  override_exp_date:   bool

        :param expiration_date:     An expiration date for the approval.  Should be in "YYYY-MM-DD" format.
        :type  expiration_date:     str

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        search_response = self.get_single_search_page(filter_request)
        uuid = search_response['_embedded']['workflowBatches'][0]['uuid']

        url = self.api_base_url.format(str(client_id)) + "/falsePositive/approve"

        body = {
            "workflowBatchUuid": uuid,
            "expirationDate": str(expiration_date),
            "overrideExpirationDate": override_exp_date
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def approve_remediation(self, filter_request, override_exp_date=False,
                            expiration_date=(datetime.date.today() + datetime.timedelta(days=14)), client_id=None):

        """
        Approve a remediation request.

        :param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param override_exp_date:   True/False indicating whether or not an expiration date should be overridden.
        :type  override_exp_date:   bool

        :param expiration_date:     An expiration date for the approval.  Should be in "YYYY-MM-DD" format.
        :type  expiration_date:     str

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        search_response = self.get_single_search_page(filter_request)
        uuid = search_response['_embedded']['workflowBatches'][0]['uuid']

        url = self.api_base_url.format(str(client_id)) + "/remediation/approve"

        body = {
            "workflowBatchUuid": uuid,
            "expirationDate": str(expiration_date),
            "overrideExpirationDate": override_exp_date
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

    def approve_severity_change(self, filter_request, override_exp_date=False,
                                expiration_date=(datetime.date.today() + datetime.timedelta(days=14)), client_id=None):

        """
        Approve a severity change request.

        :param filter_request:      A list of dictionaries containing filter parameters.
        :type  filter_request:      list

        :param override_exp_date:   True/False indicating whether or not an expiration date should be overridden.
        :type  override_exp_date:   bool

        :param expiration_date:     An expiration date for the approval.  Should be in "YYYY-MM-DD" format.
        :type  expiration_date:     str

        :param client_id:           Client ID.  If an ID isn't passed, will use the profile's default Client ID.
        :type  client_id:           int

        :return:    The job ID from the platform is returned.
        :rtype:     int

        :raises RequestFailed:
        """

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        search_response = self.get_single_search_page(filter_request)
        uuid = search_response['_embedded']['workflowBatches'][0]['uuid']

        url = self.api_base_url.format(str(client_id)) + "/severityChange/approve"

        body = {
            "workflowBatchUuid": uuid,
            "expirationDate": str(expiration_date),
            "overrideExpirationDate": override_exp_date
        }

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url, body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        job_id = jsonified_response['id']

        return job_id

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