""" *******************************************************************************************************************
|
|  Name        :  __groupBy.py
|  Module      :  risksense_api
|  Description : A class to utilize the groupby endpoint
|  Copyright   : (c) RiskSense, Inc.
|  License     : Apache-2.0 (http://www.apache.org/licenses/LICENSE-2.0)
|
******************************************************************************************************************* """

from http import client
import json
from .. import Subject
from ..._params import *
from ..._api_request_handler import *
from datetime import date
from dateutil.relativedelta import relativedelta


class Aggregate(Subject):

    """ Groupby Class """

    def __init__(self, profile):

        """
        Initialization of Groupby object.

        :param profile:     Profile Object
        :type  profile:     _profile

        """
        Subject.__init__(self, profile)
        self.dynamicaggregate_url = self.profile.platform_url + "/api/v1/client/{}/dynamic-aggregation"
        self.aggregate_url = self.profile.platform_url + "/api/v1/client/{}/"



    def get_configurable_widget(self,client_id=None):
        """
        Get groupby values for host finding

        :param hostfindingkey: The main key where other metric fields depend on
        :type  hostfindingkey: Str

        :param metricfields:   The fields that will be populated
        :type  metricfields:   list
        
        :param filters:        The filters which will populate in groupby
        :type filters:         list

        :param sortorderfield: The order to sort the groupby values, please choose ASC for ascending and DESC for descending
        :type sortorderfield:  str

        :param client_id:      The client id , if none, default client id is taken
        :type  client_id:       int
        
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.aggregate_url.format(str(client_id))+"?widgetType=SYSTEM&widgetConfigType=kpi&page=0&size=500"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response


    def get_dynamic_aggregation(self,filter=[],client_id=None):
        """
        Get groupby values for host finding

        :param hostfindingkey: The main key where other metric fields depend on
        :type  hostfindingkey: Str

        :param metricfields:   The fields that will be populated
        :type  metricfields:   list
        
        :param filters:        The filters which will populate in groupby
        :type filters:         list

        :param sortorderfield: The order to sort the groupby values, please choose ASC for ascending and DESC for descending
        :type sortorderfield:  str

        :param client_id:      The client id , if none, default client id is taken
        :type  client_id:       int
        
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.dynamicaggregate_url.format(str(client_id))

        body=[{"type":"METRIC_AGGREGATION","name":"Count","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":filter},"resultFormat":None},{"type":"METRIC_AGGREGATION","name":"Count","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":filter},"resultFormat":None}]

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response

    def get_dynamic_aggregationforfindings(self,filter=[],client_id=None):
        """
        Get groupby values for host finding

        :param hostfindingkey: The main key where other metric fields depend on
        :type  hostfindingkey: Str

        :param metricfields:   The fields that will be populated
        :type  metricfields:   list
        
        :param filters:        The filters which will populate in groupby
        :type filters:         list

        :param sortorderfield: The order to sort the groupby values, please choose ASC for ascending and DESC for descending
        :type sortorderfield:  str

        :param client_id:      The client id , if none, default client id is taken
        :type  client_id:       int
        
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.dynamicaggregate_url.format(str(client_id))

        body=[{"type":"METRIC_AGGREGATION","name":"Count","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":filter},"resultFormat":None},{"type":"METRIC_AGGREGATION","name":"Count","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":filter},"resultFormat":None}]

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response

    def get_dynamic_aggregationforopenfindingsprioritization(self,apporhost,filter=[],client_id=None):
        """
        Get groupby values for host finding

        :param hostfindingkey: The main key where other metric fields depend on
        :type  hostfindingkey: Str

        :param metricfields:   The fields that will be populated
        :type  metricfields:   list
        
        :param filters:        The filters which will populate in groupby
        :type filters:         list

        :param sortorderfield: The order to sort the groupby values, please choose ASC for ascending and DESC for descending
        :type sortorderfield:  str

        :param client_id:      The client id , if none, default client id is taken
        :type  client_id:       int
        
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.dynamicaggregate_url.format(str(client_id))
        if filter==[]:
            body=[{"name":"Scoring Metric","subject":apporhost,"field":"vrr_group","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"total","subject":apporhost,"field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"weaponized","subject":apporhost,"field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"type":"METRIC_AGGREGATION"},{"name":"rcePe","subject":apporhost,"field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_pe_rce","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"type":"METRIC_AGGREGATION"},{"name":"trending","subject":apporhost,"field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"vulnLastTrendingOn","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"manualExploit","subject":apporhost,"field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_manual_exploit","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]}]
        if filter!=[]:
            body=[{"name":"Scoring Metric","subject":apporhost,"field":"vrr_group","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},filter]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"total","subject":apporhost,"field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"weaponized","subject":apporhost,"field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"type":"METRIC_AGGREGATION"},{"name":"rcePe","subject":apporhost,"field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_pe_rce","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"type":"METRIC_AGGREGATION"},{"name":"trending","subject":apporhost,"field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"vulnLastTrendingOn","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"manualExploit","subject":apporhost,"field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_manual_exploit","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]}]
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response

    def get_dynamic_aggregationforclosedfindingsprioritization(self,apporhost,filter=[],client_id=None):
        """
        Get groupby values for host finding

        :param hostfindingkey: The main key where other metric fields depend on
        :type  hostfindingkey: Str

        :param metricfields:   The fields that will be populated
        :type  metricfields:   list
        
        :param filters:        The filters which will populate in groupby
        :type filters:         list

        :param sortorderfield: The order to sort the groupby values, please choose ASC for ascending and DESC for descending
        :type sortorderfield:  str

        :param client_id:      The client id , if none, default client id is taken
        :type  client_id:       int
        
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.dynamicaggregate_url.format(str(client_id))
        if filter==[]:
            body=[{"name":"Scoring Metric","subject":apporhost,"field":"vrr_group","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Closed"}]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"total","subject":apporhost,"field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"weaponized","subject":apporhost,"field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"type":"METRIC_AGGREGATION"},{"name":"rcePe","subject":apporhost,"field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_pe_rce","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"type":"METRIC_AGGREGATION"},{"name":"trending","subject":apporhost,"field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"vulnLastTrendingOn","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"manualExploit","subject":apporhost,"field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_manual_exploit","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]}]
        if filter!=[]:
            body=[{"name":"Scoring Metric","subject":apporhost,"field":"vrr_group","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Closed"},filter]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"total","subject":apporhost,"field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"weaponized","subject":apporhost,"field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"type":"METRIC_AGGREGATION"},{"name":"rcePe","subject":apporhost,"field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_pe_rce","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"type":"METRIC_AGGREGATION"},{"name":"trending","subject":apporhost,"field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"vulnLastTrendingOn","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"manualExploit","subject":apporhost,"field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_manual_exploit","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]}]
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response



    def get_meantime_toremediate(self,filter=[],client_id=None):
        """
        Get groupby values for host finding

        :param hostfindingkey: The main key where other metric fields depend on
        :type  hostfindingkey: Str

        :param metricfields:   The fields that will be populated
        :type  metricfields:   list
        
        :param filters:        The filters which will populate in groupby
        :type filters:         list

        :param sortorderfield: The order to sort the groupby values, please choose ASC for ascending and DESC for descending
        :type sortorderfield:  str

        :param client_id:      The client id , if none, default client id is taken
        :type  client_id:       int
        
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.dynamicaggregate_url.format(str(client_id))

        body=[{"type":"METRIC_AGGREGATION","name":"Count","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"resultFormat":None},{"type":"METRIC_AGGREGATION","name":"Remediation Time","subject":"hostFinding","field":"remediationTime","esAggregator":{"type":"AVERAGE"},"filterRequest":{"filters":[]},"resultFormat":None},{"type":"METRIC_AGGREGATION","name":"Count","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"resultFormat":None},{"type":"METRIC_AGGREGATION","name":"Remediation Time","subject":"applicationFinding","field":"remediationTime","esAggregator":{"type":"AVERAGE"},"filterRequest":{"filters":[]},"resultFormat":None}]

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response

    def get_findingbyaddresstype(self,apporhost,filter=[],client_id=None):
        """
        Get groupby values for host finding

        :param hostfindingkey: The main key where other metric fields depend on
        :type  hostfindingkey: Str

        :param metricfields:   The fields that will be populated
        :type  metricfields:   list
        
        :param filters:        The filters which will populate in groupby
        :type filters:         list

        :param sortorderfield: The order to sort the groupby values, please choose ASC for ascending and DESC for descending
        :type sortorderfield:  str

        :param client_id:      The client id , if none, default client id is taken
        :type  client_id:       int
        
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.aggregate_url.format(str(client_id))+'hostFindingByIPType/aggregate'
        if filter==[]:
            body={"subject":apporhost,"filterRequest":{"filters":[{"field":"vrr_group","exclusive":False,"operator":"IN","value":"Critical,High,Medium,Low,Info","orWithPrevious":False}]}}
        if filter!=[]:
            body={"subject":apporhost,"filterRequest":{"filters":[filter,{"field":"vrr_group","exclusive":False,"operator":"IN","value":"Critical,High,Medium,Low,Info","orWithPrevious":False}]}}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response

    def get_recent_findings_status(self,apporhost,closeoropenchoice,filter=[],client_id=None):
        """
        Get groupby values for host finding

        :param hostfindingkey: The main key where other metric fields depend on
        :type  hostfindingkey: Str

        :param metricfields:   The fields that will be populated
        :type  metricfields:   list
        
        :param filters:        The filters which will populate in groupby
        :type filters:         list

        :param sortorderfield: The order to sort the groupby values, please choose ASC for ascending and DESC for descending
        :type sortorderfield:  str

        :param client_id:      The client id , if none, default client id is taken
        :type  client_id:       int
        
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.aggregate_url.format(str(client_id))+'ageOfDiscoveredFindingByRiskRating/aggregate?useFirstIngestedOn=true'
        if filter==[]:
            body={"subject":apporhost,"filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":closeoropenchoice}]}}
        if filter!=[]:
            body={"subject":apporhost,"filterRequest":{"filters":[filter,{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":closeoropenchoice}]}}
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response


    def get_findingsummary(self,apporhost,filter=[],client_id=None):
        """
        Get groupby values for host finding

        :param hostfindingkey: The main key where other metric fields depend on
        :type  hostfindingkey: Str

        :param metricfields:   The fields that will be populated
        :type  metricfields:   list
        
        :param filters:        The filters which will populate in groupby
        :type filters:         list

        :param sortorderfield: The order to sort the groupby values, please choose ASC for ascending and DESC for descending
        :type sortorderfield:  str

        :param client_id:      The client id , if none, default client id is taken
        :type  client_id:       int
        
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.aggregate_url.format(str(client_id))+'hostFindingByRiskRating/aggregate'
        if filter==[]:
            body={"subject":apporhost,"filterRequest":{"filters":[]}}
        if filter!=[]:
            body={"subject":apporhost,"filterRequest":{"filters":[filter]}}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response

    def get_findingsfirstingestedvslastingested(self,apporhost,duration,filter=[],client_id=None):
        """
        Get groupby values for host finding

        :param hostfindingkey: The main key where other metric fields depend on
        :type  hostfindingkey: Str

        :param metricfields:   The fields that will be populated
        :type  metricfields:   list
        
        :param filters:        The filters which will populate in groupby
        :type filters:         list

        :param sortorderfield: The order to sort the groupby values, please choose ASC for ascending and DESC for descending
        :type sortorderfield:  str

        :param client_id:      The client id , if none, default client id is taken
        :type  client_id:       int
        
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        interval={'monthly':'1M','quarterly':'1q','daily':'1d','weekly':'1w'}
        endates={'1M':f"{date.today() - relativedelta(months=12)}",'1q':f"{date.today() - relativedelta(months=36)}",'1d':f"{date.today() - relativedelta(days=12)}",'1w':f"{date.today() - relativedelta(weeks=12)}"}
        url = self.aggregate_url.format(str(client_id))+'findingDateHistogram/aggregate?useFirstIngestedOn=true'
        if filter==[]:
            body={"interval":interval[duration],"start":f"{endates[interval[duration]]}","end":f"{date.today()}","filterRequest":{"subject":apporhost,"filterRequest":{"filters":[]}},"priority":"vrr_group"}
        if filter!=[]:
            body={"interval":interval[duration],"start":f"{endates[interval[duration]]}","end":f"{date.today()}","filterRequest":{"subject":apporhost,"filterRequest":{"filters":[filter]}},"priority":"vrr_group"}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response

    def get_openfindingsovertime(self,apporhost,duration,filter=[],client_id=None):
        """
        Get groupby values for host finding

        :param hostfindingkey: The main key where other metric fields depend on
        :type  hostfindingkey: Str

        :param metricfields:   The fields that will be populated
        :type  metricfields:   list
        
        :param filters:        The filters which will populate in groupby
        :type filters:         list

        :param sortorderfield: The order to sort the groupby values, please choose ASC for ascending and DESC for descending
        :type sortorderfield:  str

        :param client_id:      The client id , if none, default client id is taken
        :type  client_id:       int
        
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]
        interval={'monthly':'1M','daily':'1d','weekly':'1w'}
        endates={'1M':f"{date.today() - relativedelta(months=12)}",'1d':f"{date.today() - relativedelta(days=12)}",'1w':f"{date.today() - relativedelta(weeks=12)}"}
        url = self.aggregate_url.format(str(client_id))+'assetFindingTrendCount/aggregate'
        if filter==[]:
            body={"interval":interval[duration],"start":f"{endates[interval[duration]]}","end":f"{date.today()}","filterRequest":{"subject":apporhost,"filterRequest":{"filters":[]}},"priority":"vrr_group"}
        if filter!=[]:
            body={"interval":interval[duration],"start":f"{endates[interval[duration]]}","end":f"{date.today()}","filterRequest":{"subject":apporhost,"filterRequest":{"filters":[filter]}},"priority":"vrr_group"}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response



    def get_total_fixes(self,filter=[],client_id=None):
        """
        Get groupby values for host finding

        :param hostfindingkey: The main key where other metric fields depend on
        :type  hostfindingkey: Str

        :param metricfields:   The fields that will be populated
        :type  metricfields:   list
        
        :param filters:        The filters which will populate in groupby
        :type filters:         list

        :param sortorderfield: The order to sort the groupby values, please choose ASC for ascending and DESC for descending
        :type sortorderfield:  str

        :param client_id:      The client id , if none, default client id is taken
        :type  client_id:       int
        
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.dynamicaggregate_url.format(str(client_id))

        body=[{"type":"METRIC_AGGREGATION","name":"Count","subject":"patch","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":filter},"resultFormat":None}]
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response

    def get_rs3_aggregate(self,filter=[],client_id=None):
        """
        Get groupby values for host finding

        :param hostfindingkey: The main key where other metric fields depend on
        :type  hostfindingkey: Str

        :param metricfields:   The fields that will be populated
        :type  metricfields:   list
        
        :param filters:        The filters which will populate in groupby
        :type filters:         list

        :param sortorderfield: The order to sort the groupby values, please choose ASC for ascending and DESC for descending
        :type sortorderfield:  str

        :param client_id:      The client id , if none, default client id is taken
        :type  client_id:       int
        
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.aggregate_url.format(str(client_id))+'rs3/aggregate?applyMeCheck=True'

        body={"filters":filter}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response

    def get_findings_funnel(self,filters=[],client_id=None):

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url=self.dynamicaggregate_url.format(str(client_id))
        if filters==[]:
            body=[{"name":"Scoring Metric","subject":"hostFinding","field":"vrr_group","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Total","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Weaponized","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"type":"METRIC_AGGREGATION"},{"name":"RCE PE","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_pe_rce","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"type":"METRIC_AGGREGATION"},{"name":"Trending","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"vulnLastTrendingOn","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"ME","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_manual_exploit","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Total","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Total Distribution","subject":"host","field":"open_vrr_groups","filterRequest":{"filters":[]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Total","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Weaponized","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_threat_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Weaponized Distribution","subject":"host","field":"open_threat_vrr_groups","filterRequest":{"filters":[]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Total","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"RCE PE","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_rce_pe_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"RCE PE Distribution","subject":"host","field":"open_rce_pe_vrr_groups","filterRequest":{"filters":[]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Total","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Trending","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_group_trending_dates","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Trending Critical","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_critical_trending_dates","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Trending High","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_high_trending_dates","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Trending Medium","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_medium_trending_dates","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Trending Low","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_low_trending_dates","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Trending Info","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_info_trending_dates","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"ME","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_me_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"ME Distribution","subject":"host","field":"open_me_vrr_groups","filterRequest":{"filters":[]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Total","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Scoring Metric","subject":"applicationFinding","field":"vrr_group","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Total","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Weaponized","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"type":"METRIC_AGGREGATION"},{"name":"RCE PE","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_pe_rce","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"type":"METRIC_AGGREGATION"},{"name":"Trending","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"vulnLastTrendingOn","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"ME","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_manual_exploit","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Total","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Total Distribution","subject":"application","field":"open_vrr_groups","filterRequest":{"filters":[]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Total","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Weaponized","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_threat_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Weaponized Distribution","subject":"application","field":"open_threat_vrr_groups","filterRequest":{"filters":[]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Total","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"RCE PE","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_rce_pe_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"RCE PE Distribution","subject":"application","field":"open_rce_pe_vrr_groups","filterRequest":{"filters":[]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Total","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Trending","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_group_trending_dates","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Trending Critical","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_critical_trending_dates","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Trending High","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_high_trending_dates","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Trending Medium","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_medium_trending_dates","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Trending Low","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_low_trending_dates","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Trending Info","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_info_trending_dates","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"ME","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_me_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"ME Distribution","subject":"application","field":"open_me_vrr_groups","filterRequest":{"filters":[]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Total","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]}]
        elif filters!=[]:
            body=[{"name":"Scoring Metric","subject":"hostFinding","field":"vrr_group","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},filters]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Total","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Weaponized","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"type":"METRIC_AGGREGATION"},{"name":"RCE PE","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_pe_rce","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"type":"METRIC_AGGREGATION"},{"name":"Trending","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"vulnLastTrendingOn","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"ME","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_manual_exploit","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Total","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""},filters]},"type":"METRIC_AGGREGATION"},{"name":"Total Distribution","subject":"host","field":"open_vrr_groups","filterRequest":{"filters":[filters]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Total","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Weaponized","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_threat_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""},filters]},"type":"METRIC_AGGREGATION"},{"name":"Weaponized Distribution","subject":"host","field":"open_threat_vrr_groups","filterRequest":{"filters":[filters]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Total","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"RCE PE","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_rce_pe_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""},filters]},"type":"METRIC_AGGREGATION"},{"name":"RCE PE Distribution","subject":"host","field":"open_rce_pe_vrr_groups","filterRequest":{"filters":[filters]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Total","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Trending","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_group_trending_dates","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""},filters]},"type":"METRIC_AGGREGATION"},{"name":"Trending Critical","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_critical_trending_dates","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""},filters]},"type":"METRIC_AGGREGATION"},{"name":"Trending High","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_high_trending_dates","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""},filters]},"type":"METRIC_AGGREGATION"},{"name":"Trending Medium","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_medium_trending_dates","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""},filters]},"type":"METRIC_AGGREGATION"},{"name":"Trending Low","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_low_trending_dates","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""},filters]},"type":"METRIC_AGGREGATION"},{"name":"Trending Info","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_info_trending_dates","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""},filters]},"type":"METRIC_AGGREGATION"},{"name":"ME","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_me_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""},filters]},"type":"METRIC_AGGREGATION"},{"name":"ME Distribution","subject":"host","field":"open_me_vrr_groups","filterRequest":{"filters":[filters]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Total","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Scoring Metric","subject":"applicationFinding","field":"vrr_group","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},filters]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Total","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Weaponized","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"type":"METRIC_AGGREGATION"},{"name":"RCE PE","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_pe_rce","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"type":"METRIC_AGGREGATION"},{"name":"Trending","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"vulnLastTrendingOn","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"ME","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_manual_exploit","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Total","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""},filters]},"type":"METRIC_AGGREGATION"},{"name":"Total Distribution","subject":"application","field":"open_vrr_groups","filterRequest":{"filters":[filters]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Total","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Weaponized","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_threat_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""},filters]},"type":"METRIC_AGGREGATION"},{"name":"Weaponized Distribution","subject":"application","field":"open_threat_vrr_groups","filterRequest":{"filters":[filters]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Total","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"RCE PE","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_rce_pe_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""},filters]},"type":"METRIC_AGGREGATION"},{"name":"RCE PE Distribution","subject":"application","field":"open_rce_pe_vrr_groups","filterRequest":{"filters":[filters]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Total","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Trending","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_group_trending_dates","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""},filters]},"type":"METRIC_AGGREGATION"},{"name":"Trending Critical","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_critical_trending_dates","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""},filters]},"type":"METRIC_AGGREGATION"},{"name":"Trending High","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_high_trending_dates","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""},filters]},"type":"METRIC_AGGREGATION"},{"name":"Trending Medium","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_medium_trending_dates","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""},filters]},"type":"METRIC_AGGREGATION"},{"name":"Trending Low","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_low_trending_dates","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""},filters]},"type":"METRIC_AGGREGATION"},{"name":"Trending Info","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_info_trending_dates","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""},filters]},"type":"METRIC_AGGREGATION"},{"name":"ME","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_me_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""},filters]},"type":"METRIC_AGGREGATION"},{"name":"ME Distribution","subject":"application","field":"open_me_vrr_groups","filterRequest":{"filters":[filters]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Total","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]}]

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise
        
        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response

    def get_weaponization_funnel(self,filter=[],client_id=None):
        
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        if filter==[]:
            body=[{"name":"Finding","subject":"hostFinding","field":"generic_state","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"openFindings","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueFindings","subject":"hostFinding","field":"found_by_id","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueCVEs","subject":"hostFinding","field":"cves","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"threats","subject":"hostFinding","field":"threat_ids","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Weaponized","subject":"hostFinding","field":"generic_state","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"openFindings","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueFindings","subject":"hostFinding","field":"found_by_id","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueCVEs","subject":"hostFinding","field":"cves","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"threats","subject":"hostFinding","field":"threat_ids","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"RCE PE","subject":"hostFinding","field":"generic_state","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_pe_rce","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"openFindings","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueFindings","subject":"hostFinding","field":"found_by_id","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueCVEs","subject":"hostFinding","field":"cves","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"threats","subject":"hostFinding","field":"threat_ids","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Trending","subject":"hostFinding","field":"generic_state","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"vulnLastTrendingOn","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"openFindings","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueFindings","subject":"hostFinding","field":"found_by_id","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueCVEs","subject":"hostFinding","field":"cves","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"threats","subject":"hostFinding","field":"threat_ids","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"ME","subject":"hostFinding","field":"generic_state","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_manual_exploit","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"openFindings","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueFindings","subject":"hostFinding","field":"found_by_id","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueCVEs","subject":"hostFinding","field":"cves","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"threats","subject":"hostFinding","field":"threat_ids","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]}],"additionalOrdering":[]},{"name":"Total","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Weaponized","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_threat_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"RCE PE","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_rce_pe_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Trending","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_group_trending_dates","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"ME","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_me_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"patch","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Weaponized","subject":"patch","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"type":"METRIC_AGGREGATION"},{"name":"RCE PE","subject":"patch","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_exploit_rce_pe","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"type":"METRIC_AGGREGATION"},{"name":"Trending","subject":"patch","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"threatLastTrendingOn","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"ME","subject":"patch","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_manual_exploit","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"type":"METRIC_AGGREGATION"},{"name":"Finding","subject":"applicationFinding","field":"generic_state","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"openFindings","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueFindings","subject":"applicationFinding","field":"found_by_id","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueCVEs","subject":"applicationFinding","field":"cves","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"threats","subject":"applicationFinding","field":"threat_ids","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Weaponized","subject":"applicationFinding","field":"generic_state","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"openFindings","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueFindings","subject":"applicationFinding","field":"found_by_id","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueCVEs","subject":"applicationFinding","field":"cves","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"threats","subject":"applicationFinding","field":"threat_ids","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"RCE PE","subject":"applicationFinding","field":"generic_state","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_pe_rce","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"openFindings","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueFindings","subject":"applicationFinding","field":"found_by_id","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueCVEs","subject":"applicationFinding","field":"cves","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"threats","subject":"applicationFinding","field":"threat_ids","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Trending","subject":"applicationFinding","field":"generic_state","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"vulnLastTrendingOn","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"openFindings","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueFindings","subject":"applicationFinding","field":"found_by_id","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueCVEs","subject":"applicationFinding","field":"cves","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"threats","subject":"applicationFinding","field":"threat_ids","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"ME","subject":"applicationFinding","field":"generic_state","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_manual_exploit","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"openFindings","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueFindings","subject":"applicationFinding","field":"found_by_id","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueCVEs","subject":"applicationFinding","field":"cves","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"threats","subject":"applicationFinding","field":"threat_ids","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]}],"additionalOrdering":[]},{"name":"Total","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Weaponized","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_threat_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"RCE PE","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_rce_pe_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Trending","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_group_trending_dates","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"ME","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_me_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"patch","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Weaponized","subject":"patch","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"type":"METRIC_AGGREGATION"},{"name":"RCE PE","subject":"patch","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_exploit_rce_pe","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"type":"METRIC_AGGREGATION"},{"name":"Trending","subject":"patch","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"threatLastTrendingOn","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"ME","subject":"patch","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_manual_exploit","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"type":"METRIC_AGGREGATION"}]
        elif filter!=[]:
            body=[{"name":"Finding","subject":"hostFinding","field":"generic_state","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},filter]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"openFindings","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueFindings","subject":"hostFinding","field":"found_by_id","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueCVEs","subject":"hostFinding","field":"cves","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"threats","subject":"hostFinding","field":"threat_ids","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Weaponized","subject":"hostFinding","field":"generic_state","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"openFindings","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueFindings","subject":"hostFinding","field":"found_by_id","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueCVEs","subject":"hostFinding","field":"cves","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"threats","subject":"hostFinding","field":"threat_ids","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"RCE PE","subject":"hostFinding","field":"generic_state","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_pe_rce","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"openFindings","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueFindings","subject":"hostFinding","field":"found_by_id","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueCVEs","subject":"hostFinding","field":"cves","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"threats","subject":"hostFinding","field":"threat_ids","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Trending","subject":"hostFinding","field":"generic_state","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"vulnLastTrendingOn","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"openFindings","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueFindings","subject":"hostFinding","field":"found_by_id","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueCVEs","subject":"hostFinding","field":"cves","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"threats","subject":"hostFinding","field":"threat_ids","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"ME","subject":"hostFinding","field":"generic_state","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_manual_exploit","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"openFindings","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueFindings","subject":"hostFinding","field":"found_by_id","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueCVEs","subject":"hostFinding","field":"cves","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"threats","subject":"hostFinding","field":"threat_ids","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]}],"additionalOrdering":[]},{"name":"Total","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""},filter]},"type":"METRIC_AGGREGATION"},{"name":"Weaponized","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_threat_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""},filter]},"type":"METRIC_AGGREGATION"},{"name":"RCE PE","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_rce_pe_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""},filter]},"type":"METRIC_AGGREGATION"},{"name":"Trending","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_group_trending_dates","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""},filter]},"type":"METRIC_AGGREGATION"},{"name":"ME","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_me_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""},filter]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"patch","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[filter]},"type":"METRIC_AGGREGATION"},{"name":"Weaponized","subject":"patch","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"},filter]},"type":"METRIC_AGGREGATION"},{"name":"RCE PE","subject":"patch","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_exploit_rce_pe","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"},filter]},"type":"METRIC_AGGREGATION"},{"name":"Trending","subject":"patch","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"threatLastTrendingOn","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""},filter]},"type":"METRIC_AGGREGATION"},{"name":"ME","subject":"patch","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_manual_exploit","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"true"},filter]},"type":"METRIC_AGGREGATION"},{"name":"Finding","subject":"applicationFinding","field":"generic_state","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},filter]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"openFindings","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueFindings","subject":"applicationFinding","field":"found_by_id","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueCVEs","subject":"applicationFinding","field":"cves","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"threats","subject":"applicationFinding","field":"threat_ids","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Weaponized","subject":"applicationFinding","field":"generic_state","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"openFindings","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueFindings","subject":"applicationFinding","field":"found_by_id","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueCVEs","subject":"applicationFinding","field":"cves","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"threats","subject":"applicationFinding","field":"threat_ids","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"RCE PE","subject":"applicationFinding","field":"generic_state","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_pe_rce","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"openFindings","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueFindings","subject":"applicationFinding","field":"found_by_id","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueCVEs","subject":"applicationFinding","field":"cves","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"threats","subject":"applicationFinding","field":"threat_ids","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Trending","subject":"applicationFinding","field":"generic_state","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"vulnLastTrendingOn","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"openFindings","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueFindings","subject":"applicationFinding","field":"found_by_id","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueCVEs","subject":"applicationFinding","field":"cves","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"threats","subject":"applicationFinding","field":"threat_ids","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"ME","subject":"applicationFinding","field":"generic_state","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_manual_exploit","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"openFindings","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueFindings","subject":"applicationFinding","field":"found_by_id","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueCVEs","subject":"applicationFinding","field":"cves","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"threats","subject":"applicationFinding","field":"threat_ids","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]}],"additionalOrdering":[]},{"name":"Total","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""},filter]},"type":"METRIC_AGGREGATION"},{"name":"Weaponized","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_threat_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""},filter]},"type":"METRIC_AGGREGATION"},{"name":"RCE PE","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_rce_pe_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""},filter]},"type":"METRIC_AGGREGATION"},{"name":"Trending","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_group_trending_dates","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""},filter]},"type":"METRIC_AGGREGATION"},{"name":"ME","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_me_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""},filter]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"patch","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[filter]},"type":"METRIC_AGGREGATION"},{"name":"Weaponized","subject":"patch","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"},filter]},"type":"METRIC_AGGREGATION"},{"name":"RCE PE","subject":"patch","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_exploit_rce_pe","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"},filter]},"type":"METRIC_AGGREGATION"},{"name":"Trending","subject":"patch","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"threatLastTrendingOn","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""},filter]},"type":"METRIC_AGGREGATION"},{"name":"ME","subject":"patch","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_manual_exploit","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"true"},filter]},"type":"METRIC_AGGREGATION"}]

        try:

            url=self.dynamicaggregate_url.format(str(client_id))
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response

    def get_exploitassetsbycriticality(self,filter=[],client_id=None):
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.dynamicaggregate_url.format(str(client_id))

        if filter==[]: 

            body=[{"name":"RS3 Group","subject":"host","field":"rs3_group","filterRequest":{"filters":[{"field":"has_open_weaponization","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Criticality","subject":"host","field":"criticality","filterRequest":{"filters":[]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Count","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]}],"additionalOrdering":[]},{"name":"RS3 Group","subject":"application","field":"rs3_group","filterRequest":{"filters":[{"field":"has_open_weaponization","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Criticality","subject":"application","field":"criticality","filterRequest":{"filters":[]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Count","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]}],"additionalOrdering":[]}]
        elif filter!=[]:
            body=[{"name":"RS3 Group","subject":"host","field":"rs3_group","filterRequest":{"filters":[{"field":"has_open_weaponization","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"true"},filter]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Criticality","subject":"host","field":"criticality","filterRequest":{"filters":[]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Count","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]}],"additionalOrdering":[]},{"name":"RS3 Group","subject":"application","field":"rs3_group","filterRequest":{"filters":[{"field":"has_open_weaponization","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"true"},filter]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Criticality","subject":"application","field":"criticality","filterRequest":{"filters":[]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Count","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]}],"additionalOrdering":[]}]

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response

    def get_systemfilter(self,client_id=None):
        """
        Get groupby values for host finding

        :param hostfindingkey: The main key where other metric fields depend on
        :type  hostfindingkey: Str

        :param metricfields:   The fields that will be populated
        :type  metricfields:   list
        
        :param filters:        The filters which will populate in groupby
        :type filters:         list

        :param sortorderfield: The order to sort the groupby values, please choose ASC for ascending and DESC for descending
        :type sortorderfield:  str

        :param client_id:      The client id , if none, default client id is taken
        :type  client_id:       int
        
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.profile.platform_url + "/api/v1/search/systemFilter"

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.GET, url)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response
    
    def get_groupsbyfilter(self,value='',client_id=None):
        """
        Get groupby values for host finding

        :param hostfindingkey: The main key where other metric fields depend on
        :type  hostfindingkey: Str

        :param metricfields:   The fields that will be populated
        :type  metricfields:   list
        
        :param filters:        The filters which will populate in groupby
        :type filters:         list

        :param sortorderfield: The order to sort the groupby values, please choose ASC for ascending and DESC for descending
        :type sortorderfield:  str

        :param client_id:      The client id , if none, default client id is taken
        :type  client_id:       int
        
        """
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.aggregate_url.format(str(client_id)) + "/limitedGroup/suggest"
        
        body={"filters":[],"filter":{"field":"name","exclusive":False,"operator":"WILDCARD","value":value,"implicitFilters":[]}}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise
        
        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response
 
    def get_cisaexploited_systemfilter(self,uuid,filters=[],client_id=None):
        """
        Get groupby values for host finding

        :param hostfindingkey: The main key where other metric fields depend on
        :type  hostfindingkey: Str

        :param metricfields:   The fields that will be populated
        :type  metricfields:   list
        
        :param filters:        The filters which will populate in groupby
        :type filters:         list

        :param sortorderfield: The order to sort the groupby values, please choose ASC for ascending and DESC for descending
        :type sortorderfield:  str

        :param client_id:      The client id , if none, default client id is taken
        :type  client_id:       int
        
        """
        
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.aggregate_url.format(str(client_id))+ "/filterOverview/aggregate"
        
        if filters!=[]:
            body= {"filters":[filters],"includeHostCount":True,"includeAppCount":True,"systemFilter":uuid,"ingestTimeline":7}
        elif filters==[]:
            body= {"filters":filters,"includeHostCount":True,"includeAppCount":True,"systemFilter":uuid,"ingestTimeline":7}
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response


    def get_rs3_history(self,startdate,enddate,filters=[],client_id=None):
        """
        Get groupby values for host finding

        :param hostfindingkey: The main key where other metric fields depend on
        :type  hostfindingkey: Str

        :param metricfields:   The fields that will be populated
        :type  metricfields:   list
        
        :param filters:        The filters which will populate in groupby
        :type filters:         list

        :param sortorderfield: The order to sort the groupby values, please choose ASC for ascending and DESC for descending
        :type sortorderfield:  str

        :param client_id:      The client id , if none, default client id is taken
        :type  client_id:       int
        
        """
        
        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.aggregate_url.format(str(client_id))+ "/rs3History/aggregate"
        
        body= {"startDate":startdate,"endDate":enddate,"filters":filters,"includeHostRs3":True,"includeAppRs3":True}
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response


    def get_highimpactfindings(self,filter=[],client_id=None):

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.dynamicaggregate_url.format(str(client_id))

        if filter==[]:
            body=[{"name":"hostFindingPluginId","subject":"hostFinding","field":"found_by_id","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"cve_publish_dates","operator":"PRESENT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":""}]},"esAggregator":{"type":"TERMS","size":50},"definableOrder":{"orderType":"AGGREGATION","orderAscending":False,"path":"Scoring Metric"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Finding Title","subject":"hostFinding","field":"title","filterRequest":{"filters":[]},"esAggregator":{"type":"TOP_HITS","fields":["title"]},"type":"METRIC_AGGREGATION"},{"name":"Footprint Count","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Scoring Metric","subject":"hostFinding","field":"riskRating","esAggregator":{"type":"MAX"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Earliest CVE Publication","subject":"hostFinding","field":"cve_publish_dates","esAggregator":{"type":"MIN"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[{"orderType":"AGGREGATION","orderAscending":False,"path":"Footprint Count"}]},{"name":"applicationFindingPluginId","subject":"applicationFinding","field":"found_by_id","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"cve_publish_dates","operator":"PRESENT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":""}]},"esAggregator":{"type":"TERMS","size":50},"definableOrder":{"orderType":"AGGREGATION","orderAscending":False,"path":"Scoring Metric"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Finding Title","subject":"applicationFinding","field":"title","filterRequest":{"filters":[]},"esAggregator":{"type":"TOP_HITS","fields":["title"]},"type":"METRIC_AGGREGATION"},{"name":"Footprint Count","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Scoring Metric","subject":"applicationFinding","field":"riskRating","esAggregator":{"type":"MAX"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Earliest CVE Publication","subject":"applicationFinding","field":"cve_publish_dates","esAggregator":{"type":"MIN"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[{"orderType":"AGGREGATION","orderAscending":False,"path":"Footprint Count"}]}]
        elif filter!=[]:
            body=[{"name":"hostFindingPluginId","subject":"hostFinding","field":"found_by_id","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"cve_publish_dates","operator":"PRESENT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":""},filter]},"esAggregator":{"type":"TERMS","size":50},"definableOrder":{"orderType":"AGGREGATION","orderAscending":False,"path":"Scoring Metric"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Finding Title","subject":"hostFinding","field":"title","filterRequest":{"filters":[]},"esAggregator":{"type":"TOP_HITS","fields":["title"]},"type":"METRIC_AGGREGATION"},{"name":"Footprint Count","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Scoring Metric","subject":"hostFinding","field":"riskRating","esAggregator":{"type":"MAX"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Earliest CVE Publication","subject":"hostFinding","field":"cve_publish_dates","esAggregator":{"type":"MIN"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[{"orderType":"AGGREGATION","orderAscending":False,"path":"Footprint Count"}]},{"name":"applicationFindingPluginId","subject":"applicationFinding","field":"found_by_id","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"cve_publish_dates","operator":"PRESENT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":""},filter]},"esAggregator":{"type":"TERMS","size":50},"definableOrder":{"orderType":"AGGREGATION","orderAscending":False,"path":"Scoring Metric"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Finding Title","subject":"applicationFinding","field":"title","filterRequest":{"filters":[]},"esAggregator":{"type":"TOP_HITS","fields":["title"]},"type":"METRIC_AGGREGATION"},{"name":"Footprint Count","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Scoring Metric","subject":"applicationFinding","field":"riskRating","esAggregator":{"type":"MAX"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Earliest CVE Publication","subject":"applicationFinding","field":"cve_publish_dates","esAggregator":{"type":"MIN"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[{"orderType":"AGGREGATION","orderAscending":False,"path":"Footprint Count"}]}]
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response

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