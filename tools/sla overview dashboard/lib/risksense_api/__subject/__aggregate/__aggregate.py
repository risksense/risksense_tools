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
from warnings import filters
from .. import Subject
from ..._params import *
from ..._api_request_handler import *
from datetime import date,timedelta,datetime
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

    def get_ransomwarefindings(self,filters,client_id=None):
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

        url = self.aggregate_url.format(str(client_id))+"findingWithRansomware/aggregate"

        body={"subject":"hostFinding","filters":filters}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
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

    def get_dynamic_aggregationformeantimesla(self,filter=[],client_id=None):
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
            body=[{"name":"HF Remidation Time","subject":"hostFinding","field":"remediationTime","esAggregator":{"type":"AVERAGE"},"filterRequest":{"filters":[{"field":"resolved_on","exclusive":False,"operator":"LAST_X_DAYS","orWithPrevious":False,"implicitFilters":[],"value":"90"},{"field":"due_dates","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"HF Finding Count","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"resolved_on","exclusive":False,"operator":"LAST_X_DAYS","orWithPrevious":False,"implicitFilters":[],"value":"90"},{"field":"due_dates","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"AF Remidation Time","subject":"applicationFinding","field":"remediationTime","esAggregator":{"type":"AVERAGE"},"filterRequest":{"filters":[{"field":"resolved_on","exclusive":False,"operator":"LAST_X_DAYS","orWithPrevious":False,"implicitFilters":[],"value":"90"},{"field":"due_dates","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"AF Finding Count","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"resolved_on","exclusive":False,"operator":"LAST_X_DAYS","orWithPrevious":False,"implicitFilters":[],"value":"90"},{"field":"due_dates","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"}]
        if filter!=[]:
            body=[{"name":"HF Remidation Time","subject":"hostFinding","field":"remediationTime","esAggregator":{"type":"AVERAGE"},"filterRequest":{"filters":[{"field":"resolved_on","exclusive":False,"operator":"LAST_X_DAYS","orWithPrevious":False,"implicitFilters":[],"value":"90"},{"field":"due_dates","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""},filter]},"type":"METRIC_AGGREGATION"},{"name":"HF Finding Count","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"resolved_on","exclusive":False,"operator":"LAST_X_DAYS","orWithPrevious":False,"implicitFilters":[],"value":"90"},{"field":"due_dates","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""},filter]},"type":"METRIC_AGGREGATION"},{"name":"AF Remidation Time","subject":"applicationFinding","field":"remediationTime","esAggregator":{"type":"AVERAGE"},"filterRequest":{"filters":[{"field":"resolved_on","exclusive":False,"operator":"LAST_X_DAYS","orWithPrevious":False,"implicitFilters":[],"value":"90"},{"field":"due_dates","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""},filter]},"type":"METRIC_AGGREGATION"},{"name":"AF Finding Count","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"resolved_on","exclusive":False,"operator":"LAST_X_DAYS","orWithPrevious":False,"implicitFilters":[],"value":"90"},{"field":"due_dates","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""},filter]},"type":"METRIC_AGGREGATION"}]
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response

    def get_newpattern(self,client_id=None):
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

        url = self.aggregate_url.format(str(client_id))+"patterns"

        body={"filters":[{"field":"subject","operator":"EXACT","value":"limitedGroup"},{"field":"enabled","operator":"EXACT","value":"1"}]}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST,body=body,url=url)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response


    def limitedgroupattern(self,patternid,client_id=None):
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

        url = self.aggregate_url.format(str(client_id))+"limitedGroup/pattern"

        body={"patternId":patternid,"filters":[],"size":10}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST,body=body,url=url)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response





    def get_dynamic_aggregationforpatchablefindings(self,filter=[],client_id=None):
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
            body=[{"name":"HF Count","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_patch","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"},{"field":"due_dates","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"AF Count","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_patch","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"},{"field":"due_dates","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"}]
        if filter!=[]:
            body=[{"name":"HF Count","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_patch","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"},{"field":"due_dates","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""},filter]},"type":"METRIC_AGGREGATION"},{"name":"AF Count","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_patch","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"},{"field":"due_dates","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""},filter]},"type":"METRIC_AGGREGATION"}]
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response

    def get_remediationslaoverviewaggregate(self,delta,filter=[],client_id=None):
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
        previousdate=date.today()-timedelta(1)
        currentdate=date.today()
        onemonthagodate=date.today()-timedelta(int(delta))
        nextmonthdate=date.today()+timedelta(int(delta))
        url = self.dynamicaggregate_url.format(str(client_id))
        if filter==[]:
            body=[{"name":"Scoring Metric","subject":"hostFinding","field":"vrr_group","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"metSLA","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"resolved_on","exclusive":False,"operator":"LAST_X_DAYS","orWithPrevious":False,"implicitFilters":[],"value":delta},{"field":"has_met_sla","exclusive":False,"operator":"MET_SLA","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"missedSLA","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"resolved_on","exclusive":False,"operator":"LAST_X_DAYS","orWithPrevious":False,"implicitFilters":[],"value":delta},{"field":"has_met_sla","exclusive":False,"operator":"MISSED_SLA","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"overdueInDays","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"due_dates","exclusive":False,"operator":"RANGE","orWithPrevious":False,"implicitFilters":[],"value":f"{onemonthagodate},{previousdate}"}]},"type":"METRIC_AGGREGATION"},{"name":"overdueOutDays","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"due_dates","exclusive":False,"operator":"BEFORE","orWithPrevious":False,"implicitFilters":[],"value":f"{onemonthagodate}"}]},"type":"METRIC_AGGREGATION"},{"name":"withinSLAInDays","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"due_dates","exclusive":False,"operator":"RANGE","orWithPrevious":False,"implicitFilters":[],"value":f"{currentdate},{nextmonthdate}"}]},"type":"METRIC_AGGREGATION"},{"name":"withinSLAOutDays","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"due_dates","exclusive":False,"operator":"AFTER","orWithPrevious":False,"implicitFilters":[],"value":f"{nextmonthdate}"}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Scoring Metric","subject":"applicationFinding","field":"vrr_group","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"metSLA","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"resolved_on","exclusive":False,"operator":"LAST_X_DAYS","orWithPrevious":False,"implicitFilters":[],"value":delta},{"field":"has_met_sla","exclusive":False,"operator":"MET_SLA","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"missedSLA","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"resolved_on","exclusive":False,"operator":"LAST_X_DAYS","orWithPrevious":False,"implicitFilters":[],"value":delta},{"field":"has_met_sla","exclusive":False,"operator":"MISSED_SLA","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"overdueInDays","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"due_dates","exclusive":False,"operator":"RANGE","orWithPrevious":False,"implicitFilters":[],"value":f"{onemonthagodate},{previousdate}"}]},"type":"METRIC_AGGREGATION"},{"name":"overdueOutDays","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"due_dates","exclusive":False,"operator":"BEFORE","orWithPrevious":False,"implicitFilters":[],"value":f"{onemonthagodate}"}]},"type":"METRIC_AGGREGATION"},{"name":"withinSLAInDays","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"due_dates","exclusive":False,"operator":"RANGE","orWithPrevious":False,"implicitFilters":[],"value":f"{currentdate},{nextmonthdate}"}]},"type":"METRIC_AGGREGATION"},{"name":"withinSLAOutDays","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"due_dates","exclusive":False,"operator":"AFTER","orWithPrevious":False,"implicitFilters":[],"value":f"{nextmonthdate}"}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]}]
        if filter!=[]:
            body=[{"name":"Scoring Metric","subject":"hostFinding","field":"vrr_group","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""},filter]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"metSLA","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"resolved_on","exclusive":False,"operator":"LAST_X_DAYS","orWithPrevious":False,"implicitFilters":[],"value":delta},{"field":"has_met_sla","exclusive":False,"operator":"MET_SLA","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"missedSLA","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"resolved_on","exclusive":False,"operator":"LAST_X_DAYS","orWithPrevious":False,"implicitFilters":[],"value":delta},{"field":"has_met_sla","exclusive":False,"operator":"MISSED_SLA","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"overdueInDays","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"due_dates","exclusive":False,"operator":"RANGE","orWithPrevious":False,"implicitFilters":[],"value":f"{onemonthagodate},{previousdate}"}]},"type":"METRIC_AGGREGATION"},{"name":"overdueOutDays","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"due_dates","exclusive":False,"operator":"BEFORE","orWithPrevious":False,"implicitFilters":[],"value":f"{onemonthagodate}"}]},"type":"METRIC_AGGREGATION"},{"name":"withinSLAInDays","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"due_dates","exclusive":False,"operator":"RANGE","orWithPrevious":False,"implicitFilters":[],"value":f"{currentdate},{nextmonthdate}"}]},"type":"METRIC_AGGREGATION"},{"name":"withinSLAOutDays","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"due_dates","exclusive":False,"operator":"AFTER","orWithPrevious":False,"implicitFilters":[],"value":f"{nextmonthdate}"}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Scoring Metric","subject":"applicationFinding","field":"vrr_group","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""},filter]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"metSLA","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"resolved_on","exclusive":False,"operator":"LAST_X_DAYS","orWithPrevious":False,"implicitFilters":[],"value":delta},{"field":"has_met_sla","exclusive":False,"operator":"MET_SLA","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"missedSLA","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"resolved_on","exclusive":False,"operator":"LAST_X_DAYS","orWithPrevious":False,"implicitFilters":[],"value":delta},{"field":"has_met_sla","exclusive":False,"operator":"MISSED_SLA","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"overdueInDays","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"due_dates","exclusive":False,"operator":"RANGE","orWithPrevious":False,"implicitFilters":[],"value":f"{onemonthagodate},{previousdate}"}]},"type":"METRIC_AGGREGATION"},{"name":"overdueOutDays","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"due_dates","exclusive":False,"operator":"BEFORE","orWithPrevious":False,"implicitFilters":[],"value":f"{onemonthagodate}"}]},"type":"METRIC_AGGREGATION"},{"name":"withinSLAInDays","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"due_dates","exclusive":False,"operator":"RANGE","orWithPrevious":False,"implicitFilters":[],"value":f"{currentdate},{nextmonthdate}"}]},"type":"METRIC_AGGREGATION"},{"name":"withinSLAOutDays","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"due_dates","exclusive":False,"operator":"AFTER","orWithPrevious":False,"implicitFilters":[],"value":f"{nextmonthdate}"}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]}]
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response
    
    def get_assetswithremediationsla(self,filter=[],client_id=None):

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.dynamicaggregate_url.format(str(client_id))
        if filter==[]:
            body=[{"name":"HF Count with SLA","subject":"hostFinding","field":"host_id","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"AF Count with SLA","subject":"applicationFinding","field":"web_app_id","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"HF Count","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_and_closed_finding_count","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"0"},{"field":"sla_rule_name","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"AF Count","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_and_closed_finding_count","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"0"},{"field":"sla_rule_name","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Host Count","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"App Count","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}]
        if filter!=[]:
            body=[{"name":"HF Count with SLA","subject":"hostFinding","field":"host_id","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""},filter]},"type":"METRIC_AGGREGATION"},{"name":"AF Count with SLA","subject":"applicationFinding","field":"web_app_id","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""},filter]},"type":"METRIC_AGGREGATION"},{"name":"HF Count","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_and_closed_finding_count","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"0"},{"field":"sla_rule_name","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""},filter]},"type":"METRIC_AGGREGATION"},{"name":"AF Count","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_and_closed_finding_count","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"0"},{"field":"sla_rule_name","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""},filter]},"type":"METRIC_AGGREGATION"},{"name":"Host Count","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[filter]},"type":"METRIC_AGGREGATION"},{"name":"App Count","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[filter]},"type":"METRIC_AGGREGATION"}]
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response

    def get_weaponizedfindingsnotundersla(self,filter=[],client_id=None):

        if client_id is None:
            client_id = self._use_default_client_id()[0]

        url = self.dynamicaggregate_url.format(str(client_id))
        if filter==[]:
            body=[{"name":"HF Count","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"},{"field":"due_dates","exclusive":True,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"AF Count","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"},{"field":"due_dates","exclusive":True,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"}]
        if filter!=[]:
            body=[{"name":"HF Count","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"},{"field":"due_dates","exclusive":True,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""},filter]},"type":"METRIC_AGGREGATION"},{"name":"AF Count","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"},{"field":"due_dates","exclusive":True,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""},filter]},"type":"METRIC_AGGREGATION"}]
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response


    def get_organizationalslaoverview(self,delta,filter=[],client_id=None):
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
        currentdate=date.today()
        previousdate=date.today()-timedelta(1)
        datebefore=currentdate-timedelta(int(delta))
        dateafter=currentdate+timedelta(int(delta))
        if filter==[]:
            body=[{"name":"Total Findings Section","subject":"hostFinding","field":"generic_state","filterRequest":{"filters":[]},"esAggregator":{"type":"TERMS","size":2},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Total Findings","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Findings Under SLA","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Findings Not Under SLA","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":True,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Overdue","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","orWithPrevious":False,"implicitFilters":[],"value":f"{currentdate}"}]},"type":"METRIC_AGGREGATION"},{"name":"Within SLA","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"AFTER","orWithPrevious":False,"implicitFilters":[],"value":f"{previousdate}"}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Overdue Findings","subject":"hostFinding","field":"generic_state","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"due_dates","exclusive":False,"operator":"RANGE","orWithPrevious":False,"implicitFilters":[],"value":f"{datebefore},{previousdate}"}]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":f"{delta} Days","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Average overdue time","subject":"hostFinding","field":"due_dates","esAggregator":{"type":"AVERAGE"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Critical","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"vrr_group","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Critical"}]},"type":"METRIC_AGGREGATION"},{"name":"High","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"vrr_group","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"High"}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Findings Within SLA","subject":"hostFinding","field":"generic_state","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"due_dates","exclusive":False,"operator":"RANGE","orWithPrevious":False,"implicitFilters":[],"value":f"{currentdate},{dateafter}"}]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":f"Due in the next {delta} days","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Critical","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"vrr_group","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Critical"}]},"type":"METRIC_AGGREGATION"},{"name":"High","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"vrr_group","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"High"}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Closed Findings","subject":"hostFinding","field":"generic_state","filterRequest":{"filters":[{"field":"resolved_on","exclusive":False,"operator":"LAST_X_DAYS","orWithPrevious":False,"implicitFilters":[],"value":f"{delta}"},{"field":"due_dates","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Met SLA","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"MET_SLA","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Missed SLA","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"MISSED_SLA","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Mean time to remediate","subject":"hostFinding","field":"remediationTime","esAggregator":{"type":"AVERAGE"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Critical","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"vrr_group","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Critical"}]},"type":"METRIC_AGGREGATION"},{"name":"High","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"vrr_group","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"High"}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Total Findings Section","subject":"applicationFinding","field":"generic_state","filterRequest":{"filters":[]},"esAggregator":{"type":"TERMS","size":2},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Total Findings","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Findings Under SLA","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Findings Not Under SLA","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":True,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Overdue","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","orWithPrevious":False,"implicitFilters":[],"value":f"{currentdate}"}]},"type":"METRIC_AGGREGATION"},{"name":"Within SLA","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"AFTER","orWithPrevious":False,"implicitFilters":[],"value":f"{previousdate}"}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Overdue Findings","subject":"applicationFinding","field":"generic_state","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"due_dates","exclusive":False,"operator":"RANGE","orWithPrevious":False,"implicitFilters":[],"value":f"{datebefore},{previousdate}"}]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":f"{delta} Days","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Average overdue time","subject":"applicationFinding","field":"due_dates","esAggregator":{"type":"AVERAGE"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Critical","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"vrr_group","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Critical"}]},"type":"METRIC_AGGREGATION"},{"name":"High","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"vrr_group","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"High"}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Findings Within SLA","subject":"applicationFinding","field":"generic_state","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"due_dates","exclusive":False,"operator":"RANGE","orWithPrevious":False,"implicitFilters":[],"value":f"{currentdate},{dateafter}"}]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":f"Due in the next {delta} days","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Critical","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"vrr_group","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Critical"}]},"type":"METRIC_AGGREGATION"},{"name":"High","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"vrr_group","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"High"}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Closed Findings","subject":"applicationFinding","field":"generic_state","filterRequest":{"filters":[{"field":"resolved_on","exclusive":False,"operator":"LAST_X_DAYS","orWithPrevious":False,"implicitFilters":[],"value":f"{delta}"},{"field":"due_dates","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Met SLA","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"MET_SLA","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Missed SLA","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"MISSED_SLA","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Mean time to remediate","subject":"applicationFinding","field":"remediationTime","esAggregator":{"type":"AVERAGE"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Critical","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"vrr_group","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Critical"}]},"type":"METRIC_AGGREGATION"},{"name":"High","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"vrr_group","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"High"}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]}]
        if filter!=[]:
            body=[{"name":"Total Findings Section","subject":"hostFinding","field":"generic_state","filterRequest":{"filters":[filter]},"esAggregator":{"type":"TERMS","size":2},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Total Findings","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Findings Under SLA","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Findings Not Under SLA","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":True,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Overdue","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","orWithPrevious":False,"implicitFilters":[],"value":f"{currentdate}"}]},"type":"METRIC_AGGREGATION"},{"name":"Within SLA","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"AFTER","orWithPrevious":False,"implicitFilters":[],"value":f"{previousdate}"}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Overdue Findings","subject":"hostFinding","field":"generic_state","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"due_dates","exclusive":False,"operator":"RANGE","orWithPrevious":False,"implicitFilters":[],"value":f"{datebefore},{previousdate}"},filter]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":f"{delta} Days","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Average overdue time","subject":"hostFinding","field":"due_dates","esAggregator":{"type":"AVERAGE"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Critical","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"vrr_group","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Critical"}]},"type":"METRIC_AGGREGATION"},{"name":"High","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"vrr_group","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"High"}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Findings Within SLA","subject":"hostFinding","field":"generic_state","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"due_dates","exclusive":False,"operator":"RANGE","orWithPrevious":False,"implicitFilters":[],"value":f"{currentdate},{dateafter}"},filter]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":f"Due in the next {delta} days","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Critical","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"vrr_group","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Critical"}]},"type":"METRIC_AGGREGATION"},{"name":"High","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"vrr_group","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"High"}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Closed Findings","subject":"hostFinding","field":"generic_state","filterRequest":{"filters":[{"field":"resolved_on","exclusive":False,"operator":"LAST_X_DAYS","orWithPrevious":False,"implicitFilters":[],"value":f"{delta}"},{"field":"due_dates","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""},filter]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Met SLA","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"MET_SLA","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Missed SLA","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"MISSED_SLA","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Mean time to remediate","subject":"hostFinding","field":"remediationTime","esAggregator":{"type":"AVERAGE"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Critical","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"vrr_group","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Critical"}]},"type":"METRIC_AGGREGATION"},{"name":"High","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"vrr_group","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"High"}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Total Findings Section","subject":"applicationFinding","field":"generic_state","filterRequest":{"filters":[filter]},"esAggregator":{"type":"TERMS","size":2},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Total Findings","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Findings Under SLA","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Findings Not Under SLA","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":True,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Overdue","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","orWithPrevious":False,"implicitFilters":[],"value":f"{currentdate}"}]},"type":"METRIC_AGGREGATION"},{"name":"Within SLA","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"AFTER","orWithPrevious":False,"implicitFilters":[],"value":f"{previousdate}"}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Overdue Findings","subject":"applicationFinding","field":"generic_state","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"due_dates","exclusive":False,"operator":"RANGE","orWithPrevious":False,"implicitFilters":[],"value":f"{datebefore},{previousdate}"},filter]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":f"{delta} Days","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Average overdue time","subject":"applicationFinding","field":"due_dates","esAggregator":{"type":"AVERAGE"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Critical","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"vrr_group","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Critical"}]},"type":"METRIC_AGGREGATION"},{"name":"High","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"vrr_group","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"High"}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Findings Within SLA","subject":"applicationFinding","field":"generic_state","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"due_dates","exclusive":False,"operator":"RANGE","orWithPrevious":False,"implicitFilters":[],"value":f"{currentdate},{dateafter}"},filter]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":f"Due in the next {delta} days","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Critical","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"vrr_group","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Critical"}]},"type":"METRIC_AGGREGATION"},{"name":"High","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"vrr_group","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"High"}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Closed Findings","subject":"applicationFinding","field":"generic_state","filterRequest":{"filters":[{"field":"resolved_on","exclusive":False,"operator":"LAST_X_DAYS","orWithPrevious":False,"implicitFilters":[],"value":f"{delta}"},{"field":"due_dates","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""},filter]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Met SLA","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"MET_SLA","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Missed SLA","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"MISSED_SLA","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Mean time to remediate","subject":"applicationFinding","field":"remediationTime","esAggregator":{"type":"AVERAGE"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Critical","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"vrr_group","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Critical"}]},"type":"METRIC_AGGREGATION"},{"name":"High","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"vrr_group","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"High"}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]}]
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response

    def get_closedfindingsslaoverview(self,delta,filter=[],client_id=None):
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
            body=[{"name":"Met SLA","subject":"hostFinding","field":"has_met_sla","filterRequest":{"filters":[{"field":"resolved_on","exclusive":False,"operator":"LAST_X_DAYS","orWithPrevious":False,"implicitFilters":[],"value":delta}]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"findingCount","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"vrrGroup","subject":"hostFinding","field":"vrr_group","filterRequest":{"filters":[]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"findingCount","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]}],"additionalOrdering":[]},{"name":"Met SLA","subject":"applicationFinding","field":"has_met_sla","filterRequest":{"filters":[{"field":"resolved_on","exclusive":False,"operator":"LAST_X_DAYS","orWithPrevious":False,"implicitFilters":[],"value":delta}]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"findingCount","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"vrrGroup","subject":"applicationFinding","field":"vrr_group","filterRequest":{"filters":[]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"findingCount","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]}],"additionalOrdering":[]}]
        if filter!=[]:
            body=[{"name":"Met SLA","subject":"hostFinding","field":"has_met_sla","filterRequest":{"filters":[{"field":"resolved_on","exclusive":False,"operator":"LAST_X_DAYS","orWithPrevious":False,"implicitFilters":[],"value":delta},filter]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"findingCount","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"vrrGroup","subject":"hostFinding","field":"vrr_group","filterRequest":{"filters":[]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"findingCount","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]}],"additionalOrdering":[]},{"name":"Met SLA","subject":"applicationFinding","field":"has_met_sla","filterRequest":{"filters":[{"field":"resolved_on","exclusive":False,"operator":"LAST_X_DAYS","orWithPrevious":False,"implicitFilters":[],"value":delta},filter]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"findingCount","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"vrrGroup","subject":"applicationFinding","field":"vrr_group","filterRequest":{"filters":[]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"findingCount","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]}],"additionalOrdering":[]}]
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response

    def get_groupidsfrompattern(self,pattern,filter=[],client_id=None):
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

        url = self.aggregate_url.format(str(client_id))+'limitedGroup/pattern'

        body={"patternId":pattern,"filters":[],"size":10}

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response

    def get_groupnamefromgroupids(self,groupnames,client_id=None):
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
        url = self.aggregate_url.format(str(client_id))+'limitedGroup/search'
        body={"filters":[{"field":"name","exclusive":False,"operator":"IN","value":','.join(groupnames)}],"projection":"basic","sort":[{"field":"name","direction":"ASC"}],"size":50}
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response

    def get_datafromgroupids(self,ids,client_id=None):
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
        url = self.aggregate_url.format(str(client_id))+'limitedGroup/search'
        body={"filters":[{"field":"id","exclusive":False,"operator":"IN","value":','.join(ids)}],"projection":"basic","sort":[{"field":"name","direction":"ASC"}],"size":150}
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response


    def get_dashboardkpi(self,client_id=None):
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
    
        url = self.aggregate_url.format(str(client_id))+'dashboardKpi'
        body={"filters":[{"field":"category","exclusive":False,"operator":"EXACT","value":"sla"},{"field":"kpiType","exclusive":False,"operator":"EXACT","value":"TIMESERIES"},{"field":"enabled","exclusive":False,"operator":"EXACT","value":"1"}],"sort":[{"field":"kpiKey","direction":"ASC"}],"size":50}
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response

    def get_groupslaperformanceovertime(self,kpiint,newdate,groupid,client_id=None):
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
        newdate=datetime.strptime(newdate, "%Y-%m-%d")
        newdate=newdate.strftime('%Y-%m-01')
        url = self.dynamicaggregate_url.format(str(client_id))
        if kpiint==1:
            body=[{"name":"Distinct Group Ids","subject":"hostFinding","field":"group_ids","esAggregator":{"type":"TERMS","size":5000,"includeList":groupid},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"EXACT","value":"false"},{"field":"group_ids","exclusive":False,"operator":"IN","value":",".join(groupid)},{"field":"resolved_on","exclusive":False,"operator":"RANGE","value":f"{newdate},{date.today()}"}]},"definableOrder":{"orderType":"NONE"},"subAggregators":[{"name":"Date","subject":"hostFinding","field":"resolved_on","esAggregator":{"type":"DATE_HISTOGRAM","interval":"MONTH"},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Count","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"type":"METRIC_AGGREGATION"}]}],"fillBuckets":False,"type":"BUCKET_AGGREGATION"},{"name":"Distinct Group Ids","subject":"applicationFinding","field":"group_ids","esAggregator":{"type":"TERMS","size":5000,"includeList":groupid},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"EXACT","value":"false"},{"field":"group_ids","exclusive":False,"operator":"IN","value":",".join(groupid)},{"field":"resolved_on","exclusive":False,"operator":"RANGE","value":f"{newdate},{date.today()}"}]},"definableOrder":{"orderType":"NONE"},"subAggregators":[{"name":"Date","subject":"applicationFinding","field":"resolved_on","esAggregator":{"type":"DATE_HISTOGRAM","interval":"MONTH"},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Count","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"type":"METRIC_AGGREGATION"}]}],"fillBuckets":False,"type":"BUCKET_AGGREGATION"}]
        if kpiint==0:
            body=[{"name":"Distinct Group Ids","subject":"hostFinding","field":"group_ids","esAggregator":{"type":"TERMS","size":5000,"includeList":groupid},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"EXACT","value":"true"},{"field":"group_ids","exclusive":False,"operator":"IN","value":",".join(groupid)},{"field":"resolved_on","exclusive":False,"operator":"RANGE","value":f"{newdate},{date.today()}"}]},"definableOrder":{"orderType":"NONE"},"subAggregators":[{"name":"Date","subject":"hostFinding","field":"resolved_on","esAggregator":{"type":"DATE_HISTOGRAM","interval":"MONTH"},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Count","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"type":"METRIC_AGGREGATION"}]}],"fillBuckets":False,"type":"BUCKET_AGGREGATION"},{"name":"Distinct Group Ids","subject":"applicationFinding","field":"group_ids","esAggregator":{"type":"TERMS","size":5000,"includeList":groupid},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"EXACT","value":"true"},{"field":"group_ids","exclusive":False,"operator":"IN","value":",".join(groupid)},{"field":"resolved_on","exclusive":False,"operator":"RANGE","value":f"{newdate},{date.today()}"}]},"definableOrder":{"orderType":"NONE"},"subAggregators":[{"name":"Date","subject":"applicationFinding","field":"resolved_on","esAggregator":{"type":"DATE_HISTOGRAM","interval":"MONTH"},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Count","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"type":"METRIC_AGGREGATION"}]}],"fillBuckets":False,"type":"BUCKET_AGGREGATION"}]

        if kpiint==2:
            body=[{"name":"Distinct Group Ids","subject":"hostFinding","field":"group_ids","esAggregator":{"type":"TERMS","size":5000,"includeList":groupid},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"OVERDUE","value":""},{"field":"severity_group","exclusive":False,"operator":"EXACT","value":"Critical"},{"field":"group_ids","exclusive":False,"operator":"IN","value":",".join(groupid)},{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{newdate},{date.today()}"}]},"definableOrder":{"orderType":"NONE"},"subAggregators":[{"name":"Date","subject":"hostFinding","field":"due_dates","esAggregator":{"type":"DATE_HISTOGRAM","interval":"MONTH"},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Count","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"type":"METRIC_AGGREGATION"}]}],"fillBuckets":False,"type":"BUCKET_AGGREGATION"},{"name":"Distinct Group Ids","subject":"applicationFinding","field":"group_ids","esAggregator":{"type":"TERMS","size":5000,"includeList":groupid},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"OVERDUE","value":""},{"field":"severity_group","exclusive":False,"operator":"EXACT","value":"Critical"},{"field":"group_ids","exclusive":False,"operator":"IN","value":",".join(groupid)},{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{newdate},{date.today()}"}]},"definableOrder":{"orderType":"NONE"},"subAggregators":[{"name":"Date","subject":"applicationFinding","field":"due_dates","esAggregator":{"type":"DATE_HISTOGRAM","interval":"MONTH"},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Count","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"type":"METRIC_AGGREGATION"}]}],"fillBuckets":False,"type":"BUCKET_AGGREGATION"}]

        if kpiint==3:
            body=[{"name":"Distinct Group Ids","subject":"hostFinding","field":"group_ids","esAggregator":{"type":"TERMS","size":5000,"includeList":groupid},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"OVERDUE","value":""},{"field":"vrr_group","exclusive":False,"operator":"EXACT","value":"Critical"},{"field":"group_ids","exclusive":False,"operator":"IN","value":",".join(groupid)},{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{newdate},{date.today()}"}]},"definableOrder":{"orderType":"NONE"},"subAggregators":[{"name":"Date","subject":"hostFinding","field":"due_dates","esAggregator":{"type":"DATE_HISTOGRAM","interval":"MONTH"},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Count","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"type":"METRIC_AGGREGATION"}]}],"fillBuckets":False,"type":"BUCKET_AGGREGATION"},{"name":"Distinct Group Ids","subject":"applicationFinding","field":"group_ids","esAggregator":{"type":"TERMS","size":5000,"includeList":groupid},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"OVERDUE","value":""},{"field":"vrr_group","exclusive":False,"operator":"EXACT","value":"Critical"},{"field":"group_ids","exclusive":False,"operator":"IN","value":",".join(groupid)},{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{newdate},{date.today()}"}]},"definableOrder":{"orderType":"NONE"},"subAggregators":[{"name":"Date","subject":"applicationFinding","field":"due_dates","esAggregator":{"type":"DATE_HISTOGRAM","interval":"MONTH"},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Count","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"type":"METRIC_AGGREGATION"}]}],"fillBuckets":False,"type":"BUCKET_AGGREGATION"}]

        if kpiint==4:
            body=[{"name":"Distinct Group Ids","subject":"hostFinding","field":"group_ids","esAggregator":{"type":"TERMS","size":5000,"includeList":groupid},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"OVERDUE","value":""},{"field":"group_ids","exclusive":False,"operator":"IN","value":",".join(groupid)},{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{newdate},{date.today()}"}]},"definableOrder":{"orderType":"NONE"},"subAggregators":[{"name":"Date","subject":"hostFinding","field":"due_dates","esAggregator":{"type":"DATE_HISTOGRAM","interval":"MONTH"},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Count","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"type":"METRIC_AGGREGATION"}]}],"fillBuckets":False,"type":"BUCKET_AGGREGATION"},{"name":"Distinct Group Ids","subject":"applicationFinding","field":"group_ids","esAggregator":{"type":"TERMS","size":5000,"includeList":groupid},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"OVERDUE","value":""},{"field":"group_ids","exclusive":False,"operator":"IN","value":",".join(groupid)},{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{newdate},{date.today()}"}]},"definableOrder":{"orderType":"NONE"},"subAggregators":[{"name":"Date","subject":"applicationFinding","field":"due_dates","esAggregator":{"type":"DATE_HISTOGRAM","interval":"MONTH"},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Count","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"type":"METRIC_AGGREGATION"}]}],"fillBuckets":False,"type":"BUCKET_AGGREGATION"}]

        if kpiint==5:
            body=[{"name":"Distinct Group Ids","subject":"hostFinding","field":"group_ids","esAggregator":{"type":"TERMS","size":5000,"includeList":groupid},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"OVERDUE","value":""},{"field":"has_threat","exclusive":False,"operator":"EXACT","value":"true"},{"field":"group_ids","exclusive":False,"operator":"IN","value":",".join(groupid)},{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{newdate},{date.today()}"}]},"definableOrder":{"orderType":"NONE"},"subAggregators":[{"name":"Date","subject":"hostFinding","field":"due_dates","esAggregator":{"type":"DATE_HISTOGRAM","interval":"MONTH"},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Count","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"type":"METRIC_AGGREGATION"}]}],"fillBuckets":False,"type":"BUCKET_AGGREGATION"},{"name":"Distinct Group Ids","subject":"applicationFinding","field":"group_ids","esAggregator":{"type":"TERMS","size":5000,"includeList":groupid},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"OVERDUE","value":""},{"field":"has_threat","exclusive":False,"operator":"EXACT","value":"true"},{"field":"group_ids","exclusive":False,"operator":"IN","value":",".join(groupid)},{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{newdate},{date.today()}"}]},"definableOrder":{"orderType":"NONE"},"subAggregators":[{"name":"Date","subject":"applicationFinding","field":"due_dates","esAggregator":{"type":"DATE_HISTOGRAM","interval":"MONTH"},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Count","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"type":"METRIC_AGGREGATION"}]}],"fillBuckets":False,"type":"BUCKET_AGGREGATION"}]

        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response


    def get_aggregationforgroupslasbyduedates(self,groupids,filter=[],client_id=None):
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
        previousdate=date.today()-timedelta(1)
        duedatebefore7days=date.today()-timedelta(7)
        duedatebefore15days=date.today()-timedelta(15)
        duedatebefore30days=date.today()-timedelta(30)
        duedatebefore45days=date.today()-timedelta(45)
        url = self.dynamicaggregate_url.format(str(client_id))
        
        body=[{"name":"Group","subject":"limitedGroup","field":"id","filterRequest":{"filters":[{"field":"id","operator":"IN","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":','.join(groupids)}]},"esAggregator":{"type":"TERMS","size":100},"definableOrder":{"orderType":"AGGREGATION","path":"RS3","orderAscending":True},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"RS3","subject":"limitedGroup","field":"rs3","esAggregator":{"type":"SUM"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"findingCount","subject":"hostFinding","field":"group_ids","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"group_ids","operator":"IN","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":','.join(groupids)}]},"esAggregator":{"type":"TERMS","size":100,"includeList":groupids},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"openFindings","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"withinSLA","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","operator":"AFTER","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":f"{previousdate}"}]},"type":"METRIC_AGGREGATION"},{"name":"More than 7 Days","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","operator":"BEFORE","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":f"{duedatebefore7days}"}]},"type":"METRIC_AGGREGATION"},{"name":"More than 15 Days","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","operator":"BEFORE","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":f"{duedatebefore15days}"}]},"type":"METRIC_AGGREGATION"},{"name":"More than 30 Days","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","operator":"BEFORE","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":f"{duedatebefore30days}"}]},"type":"METRIC_AGGREGATION"},{"name":"More than 45 Days","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","operator":"BEFORE","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":f"{duedatebefore45days}"}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"findingCount","subject":"applicationFinding","field":"group_ids","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"group_ids","operator":"IN","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":','.join(groupids)}]},"esAggregator":{"type":"TERMS","size":100,"includeList":groupids},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"openFindings","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"withinSLA","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","operator":"AFTER","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":f"{previousdate}"}]},"type":"METRIC_AGGREGATION"},{"name":"More than 7 Days","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","operator":"BEFORE","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":f"{duedatebefore7days}"}]},"type":"METRIC_AGGREGATION"},{"name":"More than 15 Days","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","operator":"BEFORE","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":f"{duedatebefore15days}"}]},"type":"METRIC_AGGREGATION"},{"name":"More than 30 Days","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","operator":"BEFORE","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":f"{duedatebefore30days}"}]},"type":"METRIC_AGGREGATION"},{"name":"More than 45 Days","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","operator":"BEFORE","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":f"{duedatebefore45days}"}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]}]
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response

    def get_aggregationforgroupslasbyduedates2(self,groupids,filter=[],client_id=None):
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
        previousdate=date.today()-timedelta(1)
        duedatebefore60days=date.today()-timedelta(60)
        duedatebefore90days=date.today()-timedelta(90)
        duedatebefore120days=date.today()-timedelta(120)
        url = self.dynamicaggregate_url.format(str(client_id))
        
        body=[{"name":"Group","subject":"limitedGroup","field":"id","filterRequest":{"filters":[{"field":"id","operator":"IN","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":','.join(groupids)}]},"esAggregator":{"type":"TERMS","size":100},"definableOrder":{"orderType":"AGGREGATION","path":"RS3","orderAscending":True},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"RS3","subject":"limitedGroup","field":"rs3","esAggregator":{"type":"SUM"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"findingCount","subject":"hostFinding","field":"group_ids","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"group_ids","operator":"IN","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":','.join(groupids)}]},"esAggregator":{"type":"TERMS","size":100,"includeList":groupids},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"openFindings","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"withinSLA","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","operator":"AFTER","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":f"{previousdate}"}]},"type":"METRIC_AGGREGATION"},{"name":"More than 60 Days","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","operator":"BEFORE","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":f"{duedatebefore60days}"}]},"type":"METRIC_AGGREGATION"},{"name":"More than 90 Days","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","operator":"BEFORE","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":f"{duedatebefore90days}"}]},"type":"METRIC_AGGREGATION"},{"name":"More than 120 Days","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","operator":"BEFORE","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":f"{duedatebefore120days}"}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"findingCount","subject":"applicationFinding","field":"group_ids","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"group_ids","operator":"IN","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":','.join(groupids)}]},"esAggregator":{"type":"TERMS","size":100,"includeList":groupids},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"openFindings","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"withinSLA","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","operator":"AFTER","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":f"{previousdate}"}]},"type":"METRIC_AGGREGATION"},{"name":"More than 60 Days","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","operator":"BEFORE","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":f"{duedatebefore60days}"}]},"type":"METRIC_AGGREGATION"},{"name":"More than 90 Days","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","operator":"BEFORE","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":f"{duedatebefore90days}"}]},"type":"METRIC_AGGREGATION"},{"name":"More than 120 Days","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","operator":"BEFORE","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":f"{duedatebefore120days}"}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]}]
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response

    def get_groupslasbyprioritizationaggregate(self,groupids,filter=[],client_id=None):
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
        previousdate=date.today()-timedelta(1)
        url = self.dynamicaggregate_url.format(str(client_id))

        body=[{"name":"Group","subject":"limitedGroup","field":"id","filterRequest":{"filters":[{"field":"id","operator":"IN","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":','.join(groupids)}]},"esAggregator":{"type":"TERMS","size":100},"definableOrder":{"orderType":"AGGREGATION","path":"RS3","orderAscending":True},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"RS3","subject":"limitedGroup","field":"rs3","esAggregator":{"type":"SUM"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"findingCount","subject":"hostFinding","field":"group_ids","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"group_ids","operator":"IN","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":','.join(groupids)}]},"esAggregator":{"type":"TERMS","size":100,"includeList":groupids},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"VRR Group","subject":"hostFinding","field":"vrr_group","filterRequest":{"filters":[]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Within SLA","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","operator":"AFTER","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":f"{previousdate}"}]},"type":"METRIC_AGGREGATION"},{"name":"Overdue","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","operator":"BEFORE","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":f"{date.today()}"}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]}],"additionalOrdering":[]},{"name":"findingCount","subject":"applicationFinding","field":"group_ids","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"group_ids","operator":"IN","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":','.join(groupids)}]},"esAggregator":{"type":"TERMS","size":100,"includeList":groupids},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"VRR Group","subject":"applicationFinding","field":"vrr_group","filterRequest":{"filters":[]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Within SLA","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","operator":"AFTER","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":f"{previousdate}"}]},"type":"METRIC_AGGREGATION"},{"name":"Overdue","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","operator":"BEFORE","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":f"{date.today()}"}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]}],"additionalOrdering":[]}]
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response



    def get_pattern(self,delta,filter=[],client_id=None):
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

        url = self.aggregate_url.format(str(client_id))+'patterns'
        body={"filters":[{"field":"subject","operator":"EXACT","value":"limitedGroup"},{"field":"enabled","operator":"EXACT","value":"1"}]}
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response


    def get_overduefindingspart1(self,filter=[],client_id=None):
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
        currentdate=date.today()
        previousdate=date.today()-timedelta(1)
        dateaweekago=date.today()-timedelta(7)
        date14days=date.today()-timedelta(14)
        date30days=date.today()-timedelta(30)
        if filter==[]:
            body=[{"name":"OpenFindings","subject":"hostFinding","field":"generic_state","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{currentdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"1Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"EXACT","value":f"{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"7Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{dateaweekago},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"14Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date14days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"30Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date30days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"30LastRow","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{date30days}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"OVERDUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Weaponized","subject":"hostFinding","field":"generic_state","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{currentdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"1Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"EXACT","value":f"{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"7Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{dateaweekago},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"14Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date14days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"30Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date30days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"30LastRow","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{date30days}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"OVERDUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Scoring Metric","subject":"hostFinding","field":"vrr_group","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{currentdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"1Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"EXACT","value":f"{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"7Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{dateaweekago},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"14Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date14days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"30Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date30days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"30LastRow","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{date30days}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"OVERDUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"OpenFindings","subject":"applicationFinding","field":"generic_state","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{currentdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"1Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"EXACT","value":f"{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"7Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{dateaweekago},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"14Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date14days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"30Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date30days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"30LastRow","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{date30days}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"OVERDUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Weaponized","subject":"applicationFinding","field":"generic_state","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{currentdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"1Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"EXACT","value":f"{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"7Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{dateaweekago},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"14Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date14days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"30Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date30days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"30LastRow","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{date30days}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"OVERDUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Scoring Metric","subject":"applicationFinding","field":"vrr_group","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{currentdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"1Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"EXACT","value":f"{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"7Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{dateaweekago},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"14Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date14days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"30Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date30days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"30LastRow","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{date30days}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"OVERDUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]}]
        if filter!=[]:
            body=[{"name":"OpenFindings","subject":"hostFinding","field":"generic_state","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{currentdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},filter]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"1Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"EXACT","value":f"{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"7Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{dateaweekago},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"14Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date14days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"30Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date30days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"30LastRow","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{date30days}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"OVERDUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Weaponized","subject":"hostFinding","field":"generic_state","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{currentdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"},filter]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"1Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"EXACT","value":f"{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"7Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{dateaweekago},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"14Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date14days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"30Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date30days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"30LastRow","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{date30days}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"OVERDUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Scoring Metric","subject":"hostFinding","field":"vrr_group","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{currentdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},filter]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"1Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"EXACT","value":f"{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"7Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{dateaweekago},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"14Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date14days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"30Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date30days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"30LastRow","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{date30days}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"OVERDUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"OpenFindings","subject":"applicationFinding","field":"generic_state","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{currentdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},filter]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"1Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"EXACT","value":f"{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"7Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{dateaweekago},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"14Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date14days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"30Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date30days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"30LastRow","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{date30days}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"OVERDUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Weaponized","subject":"applicationFinding","field":"generic_state","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{currentdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"},filter]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"1Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"EXACT","value":f"{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"7Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{dateaweekago},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"14Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date14days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"30Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date30days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"30LastRow","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{date30days}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"OVERDUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Scoring Metric","subject":"applicationFinding","field":"vrr_group","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{currentdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},filter]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"1Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"EXACT","value":f"{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"7Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{dateaweekago},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"14Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date14days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"30Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date30days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"30LastRow","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{date30days}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"OVERDUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]}]
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response

    def get_overduefindingspart2(self,filter=[],client_id=None):
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
        currentdate=date.today()
        previousdate=date.today()-timedelta(1)
        date45days=date.today()-timedelta(45)
        date60days=date.today()-timedelta(60)
        date90days=date.today()-timedelta(90)
        date120days=date.today()-timedelta(120)

        if filter==[]:
            body=[{"name":"OpenFindings","subject":"hostFinding","field":"generic_state","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{currentdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"45Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date45days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"60Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date60days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"90Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date90days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"120Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date120days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"120LastRow","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{date120days}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"OVERDUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Weaponized","subject":"hostFinding","field":"generic_state","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{currentdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"45Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date45days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"60Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date60days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"90Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date90days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"120Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date120days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"120LastRow","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{date120days}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"OVERDUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Scoring Metric","subject":"hostFinding","field":"vrr_group","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{currentdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"45Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date45days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"60Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date60days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"90Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date90days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"120Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date120days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"120LastRow","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{date120days}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"OVERDUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"OpenFindings","subject":"applicationFinding","field":"generic_state","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{currentdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"45Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date45days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"60Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date60days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"90Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date90days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"120Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date120days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"120LastRow","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{date120days}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"OVERDUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Weaponized","subject":"applicationFinding","field":"generic_state","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{currentdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"45Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date45days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"60Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date60days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"90Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date90days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"120Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date120days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"120LastRow","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{date120days}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"OVERDUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Scoring Metric","subject":"applicationFinding","field":"vrr_group","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{currentdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"45Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date45days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"60Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date60days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"90Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date90days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"120Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date120days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"120LastRow","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{date120days}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"OVERDUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]}]
        if filter!=[]:
            body=[{"name":"OpenFindings","subject":"hostFinding","field":"generic_state","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{currentdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},filter]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"45Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date45days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"60Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date60days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"90Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date90days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"120Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date120days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"120LastRow","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{date120days}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"OVERDUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Weaponized","subject":"hostFinding","field":"generic_state","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{currentdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"},filter]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"45Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date45days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"60Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date60days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"90Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date90days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"120Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date120days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"120LastRow","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{date120days}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"OVERDUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Scoring Metric","subject":"hostFinding","field":"vrr_group","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{currentdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},filter]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"45Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date45days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"60Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date60days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"90Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date90days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"120Row","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date120days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"120LastRow","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{date120days}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"OVERDUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"OpenFindings","subject":"applicationFinding","field":"generic_state","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{currentdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},filter]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"45Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date45days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"60Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date60days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"90Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date90days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"120Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date120days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"120LastRow","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{date120days}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"OVERDUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Weaponized","subject":"applicationFinding","field":"generic_state","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{currentdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"},filter]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"45Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date45days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"60Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date60days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"90Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date90days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"120Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date120days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"120LastRow","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{date120days}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"OVERDUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Scoring Metric","subject":"applicationFinding","field":"vrr_group","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{currentdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},filter]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"45Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date45days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"60Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date60days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"90Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date90days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"120Row","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{date120days},{previousdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"120LastRow","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"BEFORE","value":f"{date120days}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_met_sla","exclusive":False,"operator":"OVERDUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]}]
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response


    def get_findingswithinsla(self,filter=[],client_id=None):
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
        currentdate=date.today()
        previousdate=date.today()-timedelta(1)
        weekrange=date.today()+timedelta((12 - date.today().weekday()) % 7)

        def last_day_of_month(date):
            if date.month == 12:
                return date.replace(day=31)
            return date.replace(month=date.month+1, day=1) - timedelta(days=1)

        def quarterdate(date):
                q1=[1,2,3]
                q2=[4,5,6]
                q3=[7,8,9]
                q4=[10,11,12]
                if date.month in q1:
                    return f'{date.year}-03-31'
                if date.month in q2:
                    return f'{date.year}-06-30'
                if date.month in q3:
                    return f'{date.year}-09-30'
                if date.month in q4:
                    return f'{date.year}-12-31'
        lastdayofmonth=f"{last_day_of_month(date.today())}"
        quarterdates=quarterdate(date.today())

        if filter==[]:
            body=[{"name":"OpenFindings","subject":"hostFinding","field":"generic_state","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"AFTER","value":f"{previousdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Today","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"EXACT","value":f"{currentdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"This Week","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{currentdate},{weekrange}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"This Month","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{currentdate},{lastdayofmonth}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"This Quarter","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{currentdate},{quarterdates}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Beyond This Quarter","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"AFTER","value":f"{quarterdates}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Weaponized","subject":"hostFinding","field":"generic_state","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"AFTER","value":f"{previousdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Today","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"EXACT","value":f"{currentdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"This Week","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{currentdate},{weekrange}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"This Month","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{currentdate},{quarterdates}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"This Quarter","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{currentdate},{quarterdates}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Beyond This Quarter","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"AFTER","value":f"{quarterdates}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Scoring Metric","subject":"hostFinding","field":"vrr_group","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"AFTER","value":f"{previousdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Today","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"EXACT","value":f"{currentdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"This Week","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{currentdate},{weekrange}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"This Month","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{currentdate},{lastdayofmonth}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"This Quarter","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{currentdate},{quarterdates}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Beyond This Quarter","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"AFTER","value":f"{quarterdates}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"OpenFindings","subject":"applicationFinding","field":"generic_state","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"AFTER","value":f"{previousdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Today","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"EXACT","value":f"{currentdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"This Week","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{currentdate},{weekrange}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"This Month","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{currentdate},{lastdayofmonth}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"This Quarter","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{currentdate},{quarterdates}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Beyond This Quarter","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"AFTER","value":f"{quarterdates}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Weaponized","subject":"applicationFinding","field":"generic_state","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"AFTER","value":f"{previousdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Today","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"EXACT","value":f"{currentdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"This Week","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{currentdate},{weekrange}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"This Month","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{currentdate},{lastdayofmonth}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"This Quarter","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{currentdate},{quarterdates}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Beyond This Quarter","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"AFTER","value":f"{quarterdates}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Scoring Metric","subject":"applicationFinding","field":"vrr_group","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"AFTER","value":f"{previousdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Today","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"EXACT","value":f"{currentdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"This Week","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{currentdate},{weekrange}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"This Month","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{currentdate},{lastdayofmonth}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"This Quarter","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{currentdate},{quarterdates}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Beyond This Quarter","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"AFTER","value":f"{quarterdates}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]}]
        if filter!=[]:
            body=[{"name":"OpenFindings","subject":"hostFinding","field":"generic_state","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"AFTER","value":f"{previousdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},filter]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Today","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"EXACT","value":f"{currentdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"This Week","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{currentdate},{weekrange}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"This Month","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{currentdate},{lastdayofmonth}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"This Quarter","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{currentdate},{quarterdates}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Beyond This Quarter","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"AFTER","value":f"{quarterdates}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Weaponized","subject":"hostFinding","field":"generic_state","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"AFTER","value":f"{previousdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"},filter]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Today","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"EXACT","value":f"{currentdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"This Week","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{currentdate},{weekrange}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"This Month","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{currentdate},{quarterdates}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"This Quarter","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{currentdate},{quarterdates}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Beyond This Quarter","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"AFTER","value":f"{quarterdates}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Scoring Metric","subject":"hostFinding","field":"vrr_group","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"AFTER","value":f"{previousdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},filter]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Today","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"EXACT","value":f"{currentdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"This Week","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{currentdate},{weekrange}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"This Month","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{currentdate},{lastdayofmonth}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"This Quarter","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{currentdate},{quarterdates}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Beyond This Quarter","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"AFTER","value":f"{quarterdates}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"OpenFindings","subject":"applicationFinding","field":"generic_state","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"AFTER","value":f"{previousdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},filter]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Today","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"EXACT","value":f"{currentdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"This Week","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{currentdate},{weekrange}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"This Month","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{currentdate},{lastdayofmonth}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"This Quarter","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{currentdate},{quarterdates}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Beyond This Quarter","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"AFTER","value":f"{quarterdates}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Weaponized","subject":"applicationFinding","field":"generic_state","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"AFTER","value":f"{previousdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"},filter]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Today","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"EXACT","value":f"{currentdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"This Week","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{currentdate},{weekrange}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"This Month","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{currentdate},{lastdayofmonth}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"This Quarter","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{currentdate},{quarterdates}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Beyond This Quarter","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"AFTER","value":f"{quarterdates}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Scoring Metric","subject":"applicationFinding","field":"vrr_group","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"AFTER","value":f"{previousdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},filter]},"esAggregator":{"type":"TERMS","size":5},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"Today","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"EXACT","value":f"{currentdate}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"This Week","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{currentdate},{weekrange}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"This Month","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{currentdate},{lastdayofmonth}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"This Quarter","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{currentdate},{quarterdates}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Beyond This Quarter","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"AFTER","value":f"{quarterdates}","orWithPrevious":False}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]}]
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

    def get_ransomwarethreatbyage(self,filters=[],client_id=None):
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

        url = self.aggregate_url.format(str(client_id))+"ransomwareVulnerabilitiesByAge/aggregate"
        if filters!=[]:
            body={"interval":"1y","filterRequest":{"subject":"hostFinding","filterRequest":{"filters":[
                filters,{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"threat_categories","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"Ransomware"}]}}}
        if filters==[]:
            body={"interval":"1y","filterRequest":{"subject":"hostFinding","filterRequest":{"filters":[
                {"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"threat_categories","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"Ransomware"}]}}}
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response

    def get_ransomwarevulnerabilitiesbyfamily(self,filters=[],client_id=None):
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

        url = self.aggregate_url.format(str(client_id))+"ransomwareVulnerabilitiesByFamily/aggregate"
        if filters!=[]:
            body={"subject":"hostFinding","filters":[filters,{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"threat_categories","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"Ransomware"}],"size":10}
        if filters==[]:
            body={"subject":"hostFinding","filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"threat_categories","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"Ransomware"}],"size":10}
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response

    def get_topransomwarefamilies(self,filters=[],client_id=None):
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

        url = self.aggregate_url.format(str(client_id))+"topRansomwareFamilies/aggregate"
        if filters!=[]:
            body={"subject":"hostFinding","filters":[filters,{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"threat_categories","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"Ransomware"},{"field":"cve_data","exclusive":False,"operator":"NESTED","value":"[{\"field\":\"cve_data.has_ransomware\",\"operator\":\"EXACT\",\"exclusive\":False,\"orWithPrevious\":False,\"implicitFilters\":[],\"value\":\"true\"}]"}],"size":5}
        if filters==[]:
            body={"subject":"hostFinding","filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"threat_categories","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"Ransomware"},{"field":"cve_data","exclusive":False,"operator":"NESTED","value":"[{\"field\":\"cve_data.has_ransomware\",\"operator\":\"EXACT\",\"exclusive\":False,\"orWithPrevious\":False,\"implicitFilters\":[],\"value\":\"true\"}]"}],"size":5}
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response

    def get_topransomwarecve(self,filters=[],client_id=None):
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

        url = self.aggregate_url.format(str(client_id))+"topRansomwareCve/aggregate"
        if filters!=[]:
            body={"subject":"hostFinding","filters":[filters,{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"threat_categories","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"Ransomware"},{"field":"cve_data","exclusive":False,"operator":"NESTED","value":"[{\"field\":\"cve_data.has_ransomware\",\"operator\":\"EXACT\",\"exclusive\":False,\"orWithPrevious\":False,\"implicitFilters\":[],\"value\":\"true\"}]"}],"size":5}
        if filters==[]:
            body={"subject":"hostFinding","filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"threat_categories","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"Ransomware"},{"field":"cve_data","exclusive":False,"operator":"NESTED","value":"[{\"field\":\"cve_data.has_ransomware\",\"operator\":\"EXACT\",\"exclusive\":False,\"orWithPrevious\":False,\"implicitFilters\":[],\"value\":\"true\"}]"}],"size":5}
        try:
            raw_response = self.request_handler.make_request(ApiRequestHandler.POST, url,body=body)
        except RequestFailed:
            raise

        jsonified_response = json.loads(raw_response.text)
        
        return jsonified_response

    def get_findingsduecalender(self,fromdate,filters=[],client_id=None):
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
        currentdate=date.today()+timedelta(30)
        previousdate=fromdate
        url = self.dynamicaggregate_url.format(str(client_id))
        if filters==[]:
            body=[{"name":"Due Dates","subject":"hostFinding","field":"due_dates","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{previousdate},{currentdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]},"esAggregator":{"type":"DATE_HISTOGRAM","interval":"DAY"},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"count","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Due Dates","subject":"applicationFinding","field":"due_dates","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{previousdate},{currentdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]},"esAggregator":{"type":"DATE_HISTOGRAM","interval":"DAY"},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"count","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]}]
        if filters!=[]:
            body=[{"name":"Due Dates","subject":"hostFinding","field":"due_dates","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{previousdate},{currentdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},filters]},"esAggregator":{"type":"DATE_HISTOGRAM","interval":"DAY"},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"count","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Due Dates","subject":"applicationFinding","field":"due_dates","filterRequest":{"filters":[{"field":"due_dates","exclusive":False,"operator":"RANGE","value":f"{previousdate},{currentdate}","orWithPrevious":False},{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},filters]},"esAggregator":{"type":"DATE_HISTOGRAM","interval":"DAY"},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"count","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]}]
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
            body=[{"name":"Finding","subject":"hostFinding","field":"generic_state","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"openFindings","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueFindings","subject":"hostFinding","field":"found_by_id","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueCVEs","subject":"hostFinding","field":"cves","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"threats","subject":"hostFinding","field":"threat_ids","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Weaponized","subject":"hostFinding","field":"generic_state","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"openFindings","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueFindings","subject":"hostFinding","field":"found_by_id","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueCVEs","subject":"hostFinding","field":"cves","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"threats","subject":"hostFinding","field":"threat_ids","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"RCE PE","subject":"hostFinding","field":"generic_state","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_pe_rce","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"openFindings","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueFindings","subject":"hostFinding","field":"found_by_id","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueCVEs","subject":"hostFinding","field":"cves","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"threats","subject":"hostFinding","field":"threat_ids","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Trending","subject":"hostFinding","field":"generic_state","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"vulnLastTrendingOn","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"openFindings","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueFindings","subject":"hostFinding","field":"found_by_id","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueCVEs","subject":"hostFinding","field":"cves","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"threats","subject":"hostFinding","field":"threat_ids","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"ME","subject":"hostFinding","field":"generic_state","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_manual_exploit","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"openFindings","subject":"hostFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueFindings","subject":"hostFinding","field":"found_by_id","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueCVEs","subject":"hostFinding","field":"cves","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"threats","subject":"hostFinding","field":"threat_ids","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]}],"additionalOrdering":[]},{"name":"Total","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Weaponized","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_threat_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"RCE PE","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_rce_pe_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Trending","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_group_trending_dates","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"ME","subject":"host","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_me_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"patch","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Weaponized","subject":"patch","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"type":"METRIC_AGGREGATION"},{"name":"RCE PE","subject":"patch","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_exploit_rce_pe","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"type":"METRIC_AGGREGATION"},{"name":"Trending","subject":"patch","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"threatLastTrendingOn","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"ME","subject":"patch","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_manual_exploit","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"type":"METRIC_AGGREGATION"},{"name":"Finding","subject":"applicationFinding","field":"generic_state","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"}]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"openFindings","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueFindings","subject":"applicationFinding","field":"found_by_id","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueCVEs","subject":"applicationFinding","field":"cves","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"threats","subject":"applicationFinding","field":"threat_ids","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Weaponized","subject":"applicationFinding","field":"generic_state","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"},filter]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"openFindings","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueFindings","subject":"applicationFinding","field":"found_by_id","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueCVEs","subject":"applicationFinding","field":"cves","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"threats","subject":"applicationFinding","field":"threat_ids","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"RCE PE","subject":"applicationFinding","field":"generic_state","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_pe_rce","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"openFindings","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueFindings","subject":"applicationFinding","field":"found_by_id","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueCVEs","subject":"applicationFinding","field":"cves","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"threats","subject":"applicationFinding","field":"threat_ids","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"Trending","subject":"applicationFinding","field":"generic_state","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"vulnLastTrendingOn","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"openFindings","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueFindings","subject":"applicationFinding","field":"found_by_id","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueCVEs","subject":"applicationFinding","field":"cves","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"threats","subject":"applicationFinding","field":"threat_ids","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]},{"name":"ME","subject":"applicationFinding","field":"generic_state","filterRequest":{"filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"has_manual_exploit","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"esAggregator":{"type":"TERMS","size":1},"definableOrder":{"orderType":"NONE"},"type":"BUCKET_AGGREGATION","subAggregators":[{"name":"openFindings","subject":"applicationFinding","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueFindings","subject":"applicationFinding","field":"found_by_id","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"uniqueCVEs","subject":"applicationFinding","field":"cves","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"threats","subject":"applicationFinding","field":"threat_ids","esAggregator":{"type":"CARDINALITY"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"}],"additionalOrdering":[]}],"additionalOrdering":[]},{"name":"Total","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Weaponized","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_threat_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"RCE PE","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_rce_pe_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Trending","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_vrr_group_trending_dates","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"ME","subject":"application","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"open_me_vrr_groups","exclusive":False,"operator":"PRESENT","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"Total","subject":"patch","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[]},"type":"METRIC_AGGREGATION"},{"name":"Weaponized","subject":"patch","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_threat","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"type":"METRIC_AGGREGATION"},{"name":"RCE PE","subject":"patch","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_exploit_rce_pe","operator":"EXACT","exclusive":False,"orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"type":"METRIC_AGGREGATION"},{"name":"Trending","subject":"patch","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"threatLastTrendingOn","exclusive":False,"operator":"TRUE","orWithPrevious":False,"implicitFilters":[],"value":""}]},"type":"METRIC_AGGREGATION"},{"name":"ME","subject":"patch","field":"id","esAggregator":{"type":"VALUE_COUNT"},"filterRequest":{"filters":[{"field":"has_manual_exploit","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"true"}]},"type":"METRIC_AGGREGATION"}]
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