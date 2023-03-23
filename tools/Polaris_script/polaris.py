#!/usr/bin/python
'''
Copyright (c) 2020 Synopsys, Inc. All rights reserved worldwide. The information
contained in this file is the proprietary and confidential information of
Synopsys, Inc. and its licensors, and is supplied subject to, and may be used
only by Synopsys customers in accordance with the terms and conditions of a
previously executed license agreement between Synopsys and that customer.

Purpose: library of common Polaris functions

Coding conventions:
4 space indentation, not tabs
getFoo & setFoo function names
lowerUpperCase function and variable names
hide debug output behind if debug: print(something)
values from JSON are strings, so no need to str(value)

Debug levels:
1 = normal one liners like projectId = projectId
3 = produce printCurl output
5 = various json / dictionary structures
7 = entire endpoint response structure

Variables assumed set in main:
polaris.debug
polaris.baseUrl
polaris.jwt
polaris.session

Requires the following Python modules:
pip install requests pandas
'''

import re
import sys
import json
import requests
from datetime import datetime
from datetime import timedelta
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
import pandas as pd
from _datetime import date

MAX_LIMIT = 500

# -----------------------------------------------------------------------------

'''
Function:       printCurl
Description:    output curl command
Input:          endpoint, method, params and/or data
Output:         curl command to act on endpoint
'''
def printCurl(url, method, params=None, data=None):
    headers = {'Authorization': 'Bearer ' + jwt}
    header_list = ['"{0}: {1}"'.format(k, v) for k, v in headers.items()]
    header = " -H ".join(header_list)
    if params:
        param_list = ['"{0}={1}"'.format(k, v) for k, v in params.items()]
        param_str = "&".join(param_list).replace('"','')
        # Remove spaces from 'include[issue][]': ['severity', 'related-indicators', 'related-taxa']
        param_str = param_str.replace(' ', '')
        url = url + '?' + param_str
    url = '"' + url + '"'
    if data:
        data = data.replace(' ', '')
        command = "curl -sS -X {method} {uri} -H {headers} --data-raw '{data}'"
        print(command.format(method=method, headers=header, uri=url, data=data))
    else:
        command = "curl -sS -X {method} {uri} -H {headers}"
        print(command.format(method=method, headers=header, uri=url))

# -----------------------------------------------------------------------------

'''
Function:       printError
Description:    print error and exit
Input:          response error JSON
Output:         error code and detail
'''
def printError(e):
    try:
        print("FATAL: Error Code " + e['code'] + ": " + e['detail'])
    except:
        print("FATAL: Error: " + str(e))
    sys.exit(1)

# -----------------------------------------------------------------------------

'''
Function:       printWarning
Description:    print error and continue
Input:          response error JSON
Output:         error code and detail
'''
def printWarning(e):
    try:
        print("WARNING: Error Code " + e['code'] + ": " + e['detail'])
    except:
        print("WARNING: Error: " + str(e))

# -----------------------------------------------------------------------------
# --- Polaris AUTH functions
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------

'''
Function:       getJwt
Description:    convert users access token to JSON Web Token. For service accounts,
                pass None for token and supply the email and password.
Input:          url and token or email and password
Output:         jwt
'''
def getJwt(baseUrl, token, email=None, password=None):
    endpoint = baseUrl + '/api/auth/v1/authenticate'
    headers = { 'Accept' : 'application/json', 'Content-Type' : 'application/x-www-form-urlencoded' }
    if token != None:
        params = { 'accesstoken' : token }
    else:
        params = { 'email' : email, 'password' : password }
    response = requests.post(endpoint, headers=headers, data=params)
    if debug: print(response)
    if response.status_code != 200: printError(response.json()['errors'][0])
    return response.json()['jwt']

# -----------------------------------------------------------------------------

'''
Function:       createSession
Description:    creates a requests session with JWT auth header
                https://docs.python-requests.org/en/master/user/advanced/#session-objects
Input:          url, token
Output:         url, jwt, session
'''
def createSession(url, token, email=None, password=None):
    jwt = getJwt(url, token, email, password)
    headers = { 'Authorization' : 'Bearer ' + jwt, 'Content-Type' : 'application/vnd.api+json' }
    session = requests.Session()
    session.headers.update(headers)
    return url, jwt, session

# -----------------------------------------------------------------------------
# ---- Polaris GET functions
# -----------------------------------------------------------------------------

'''
Function:       getPaginatedData
Description:    gets paginated data and returns a single concatenated data dictionary
Input:          endpoint
                params
                limit
Output:         data
                included
'''
def getPaginatedData(endpoint, params={}, limit=MAX_LIMIT):
    offset = 0
    total = limit + 1
    data = []
    included = []

    params['page[limit]'] = str(limit)
    params['page[offset]'] = str(offset)

    while (offset < total):
        if (debug >= 3): printCurl(endpoint, 'GET', params)
        response = session.get(endpoint, params=params)
        if debug: print(response)
        if response.status_code != 200: printError(response.json()['errors'][0])

        if (response.json()['data'] == []):
            # Return empty list (or 2 empty lists for issues endpoint)
            p = re.compile(r'api\/query\/v\d+\/issues')
            if p.search(endpoint):
                return [], []
            else:
                return []

        # we actually only need to fetch total once
        total = response.json()['meta']['total']

        if (data == []):
            # A single data element can have confusing results with extend, so make
            # sure we initialize cleanly
            data = response.json()['data']
        else:
            data.extend(response.json()['data'])

        try: included.extend(response.json()['included'])
        except: pass

        # update the offset to the next page
        offset += limit
        params['page[offset]'] = str(offset)

        # if limit is less than MAX_LIMIT, assume we are after the first N records
        if (limit < MAX_LIMIT): break

    if (included == []): return data
    else: return data, included

# -----------------------------------------------------------------------------

'''
Function:       getIds
Description:    get ids for given project & branch
Input:          project name
                branch name
Output:         project id
                branch id
                org id
                etag
'''

def getIds(projectName, branchName):
    projectId = getProjectId(projectName)
    endpoint = baseUrl + '/api/common/v0/branches'
    params = dict([('page[limit]', MAX_LIMIT),
        ('filter[branch][project][id][eq]', projectId),
        ('filter[branch][name][eq]', branchName),
        ])
    if (debug >= 3): printCurl(endpoint, 'GET', params)
    response = session.get(endpoint, params=params)
    if debug: print(response)
    if response.status_code != 200: printError(response.json()['errors'][0])

    if response.json()['meta']['total'] == 0:
        print('FATAL: branch ' + branchName + ' not found')
        sys.exit(1)
    bid = response.json()['data'][0]['id']
    pid = response.json()['data'][0]['relationships']['project']['data']['id']
    oid = response.json()['data'][0]['meta']['organization-id']
    etag = response.json()['data'][0]['meta']['etag']
    return pid, bid, oid, etag

# -----------------------------------------------------------------------------

'''
Function:       getBranchId
Description:    return the branchId for projectId, branchName
Input:          project id
                branch name
Output:         branch id
'''
def getBranchId(projectId, branchName):
    endpoint = baseUrl + '/api/common/v0/branches'
    params = dict([
        ('page[limit]', MAX_LIMIT),
        ('filter[branch][project][id][eq]', projectId),
        ('filter[branch][name][eq]', branchName)
    ])
    if (debug >= 3): printCurl(endpoint, 'GET', params)
    response = session.get(endpoint, params=params)
    if debug: print(response)
    if response.status_code != 200: printError(response.json()['errors'][0])

    if response.json()['meta']['total'] == 0:
        print('FATAL: branch ' + branchName + ' not found')
        sys.exit(1)
    return response.json()['data'][0]['id']

# -----------------------------------------------------------------------------

'''
Function:       getLastRunId
Description:    return the most recent runId for branchId
Input:          branchId
Output:         runId
'''
def getLastRunId(branchId):
    endpoint = baseUrl + '/api/common/v0/runs'
    params = dict([
        ('page[limit]', MAX_LIMIT),
        ('filter[run][revision][branch][id][eq]', branchId)
    ])
    if (debug >= 3): printCurl(endpoint, 'GET', params)
    response = session.get(endpoint, params=params)
    if debug: print(response.text)
    if response.status_code != 200: printError(response.json()['errors'][0])

    if response.json()['meta']['total'] == 0:
        print('FATAL: No runs for branch ' + branchName)
        sys.exit(1)
    return response.json()['data'][0]['id']

# -----------------------------------------------------------------------------

'''
Function:       getProjectAndBranchId
Description:    Returns both project and branch IDs for a project+branch pair
Input:          project name
                branch name
Output:         project id
                branch id
'''
def getProjectAndBranchId(projectName, branchName):
    projectId, branchId, orgId, etag = getIds(projectName, branchName)
    return projectId, branchId

# -----------------------------------------------------------------------------
'''
Function:       branchName
Description:    getting Branchname
Input:          branchId
Output:         branchname
'''

def getbranchName(branchId):
    endpoint = baseUrl + '/api/common/v0/branches/' + branchId
    response = session.get(endpoint)
    if response.status_code != 200: printError(response.json()['errors'][0])
    return response.json()['data']['attributes']['name']
    
    
'''
Function:       isProjectMain
Description:    is branch main-for-project
Input:          branchId
Output:         True/False
'''


def isBranchProjectMain(branchId):
    endpoint = baseUrl + '/api/common/v0/branches/' + branchId
    if (debug >= 3): printCurl(endpoint, 'GET')
    response = session.get(endpoint)
    if debug: print(response)
    if response.status_code != 200: printError(response.json()['errors'][0])
    return response.json()['data']['attributes']['main-for-project']

# -----------------------------------------------------------------------------

'''
Function:       getGroupId
Description:
Input:          group name
Output:         group id
'''
def getGroupId(groupname):
    endpoint = baseUrl + '/api/auth/v1/groups'
    if (debug >= 3): printCurl(endpoint, 'GET')
    response = session.get(endpoint)
    if debug: print(response)
    if response.status_code != 200: printError(response.json()['errors'][0])

    for group in response.json()['data']:
        if (group['attributes']['groupname'] == groupname):
            return group['id']
    print('FATAL: group ' + groupname + ' not found')
    sys.exit(1)

# -----------------------------------------------------------------------------

'''
Function:       getBranches
Description:    create a dictionary of useful branch values for a given project id
Input:          projectId
Output:         dictionary of useful branch values
'''
def getBranches(projectId, project, limit=MAX_LIMIT):
    endpoint = baseUrl + '/api/common/v0/branches'
    if projectId:
        params = dict([
            ('filter[branch][project][id][eq]', projectId ),
            ])
    else:
        params = dict([
            ('filter[branch][project][name][eq]', project ),
            ])
    branches = getPaginatedData(endpoint, params, limit)
    if branches == []:
        return []

    # loop over the list of runs and grab the fields we want to include in the dictionary
    dictionary = []
    for branch in branches:
        branchId = branch['id']
        branch_name = branch['attributes']['name']
        main = branch['attributes']['main-for-project']
        projectId = branch['relationships']['project']['data']['id']
        trash = branch['meta']['in-trash']

        entry = {
            'branchId': branchId,
            'branch_name': branch_name,
            'projectId': projectId,
            'main': main,
            'trash': trash,
        }

        if (debug >= 5): print(entry)
        dictionary.append(entry)
    print(dictionary)    

    return dictionary

# -----------------------------------------------------------------------------

'''
Function:       getRollUps
Description:    create a dictionary of rollup data given project+runId
Input:          projectId
                runId (optional, but must provide a valid filterlist if None)
                limit
                optional filter dictionary
                Example filter:
                    dict([('filter[issue][issue-key][eq]', 'xyz')])
Output:         rollup counts data
'''
def getRollUps(projectId, runId, limit=MAX_LIMIT, filterlist=None):
    endpoint = baseUrl + '/api/query/v1/roll-up-counts'

    if runId is None:
        # It's up to the caller to provide a valid filterlist
        # One of [application-id, branch-id, revision-id, run-id[]] must be specified
        params = dict([
            ('project-id', projectId),
            ('sort', "-count"),
            ])
    else:
        params = dict([
            ('run-id[]', runId),
            ('project-id', projectId),
            ('sort', "-count"),
            ])

    rollup_list = []
    inc_dict = {}

    # Use this filter to get the issue breakdown (e.g. count of issues by type)
    # ('group-by', "[issue][issue-type]"),
    if filterlist:
        params.update(filterlist)

    try: rollup_data, rollup_included = getPaginatedData(endpoint, params, limit)
    except: return rollup_list

    # Create a dict of of the "included" data keyed off the ID.
    for inc in rollup_included:
        # Will only have issue-types if filter has group-by=issue-type
        # (default case is just a single count:NNN entry)
        if "name" not in inc['attributes']:
            # Normal case, just a count
            continue
        entry = {
           'name': inc['attributes']['name'],
           'description': inc['attributes']['description'],
        }
        if ("issue-type" in inc['attributes']):
           entry['type'] = inc['attributes']['name']

        inc_dict[inc['id']] = entry

    # For the default case, this will be a list of 1.
    # When we have issue type data, append the associated dict from above.
    for count in rollup_data:
        entry = {
           'count': count['attributes']['value'],
        }
        # Append issue type data if available
        if count['relationships']['issue-type']['data']:
            id = count['relationships']['issue-type']['data']['id']
            entry['issue'] = inc_dict[id]

        # Append taxon data if available
        if count['relationships']['taxon']['data']:
            id = count['relationships']['taxon']['data']['id']
            entry['taxon'] = inc_dict[id]

        rollup_list.append(entry)

    return(rollup_list)

# -----------------------------------------------------------------------------

'''
Function:       getJobs
Description:    create a dictionary of useful job values for a given branch id
Input:          branchId
                filter
                getEvents
                getRollUpCounts - enables additional API calls for issue count and density
                limit
Output:         dictionary of useful job values
'''
def getJobs(branchId, filter, getEvents=True, getRollUpCounts=False, limit=MAX_LIMIT):
    endpoint = baseUrl + '/api/jobs/v2/jobs'
    params = dict([
        ('filter[jobs][branch][id]', branchId),
        ])

    # update params with optional user-specified filter
    if filter:
        params.update(filter)

    jobs = getPaginatedData(endpoint, params, limit)
    if jobs == []:
        return []

    # loop over the list of jobs and grab the fields we want to include in the dictionary
    dictionary = []
    timeFormat = '%Y-%m-%dT%H:%M:%S.%fZ'
    for job in jobs:
        jobId = job['id']
        projectId = job['attributes']['projectId'].split(':')[3]
        branchId = job['attributes']['branchId'].split(':')[3]
        dateCreated = job['attributes']['dateCreated']
        # to be added to Polaris 2021.03 jobs v2 API
        #dateCompleted = job['attributes']['dateCompleted']
        state = job['status']['state']
        if (state == 'COMPLETED'):
            runId = job['attributes']['runId'].split(':')[3]
            toolVersion = job['attributes']['metadata']['toolversion']
            try: loc = job['attributes']['details']['jobStats']['locAnalyzed']
            except: loc = job['attributes']['details']['intermediateDirectoryDetails']['linesOfCode']
            try: files = job['attributes']['details']['jobStats']['filesAnalyzed']['Total']
            except:
                try: files = job['attributes']['details']['jobStats']['filesAnalyzed']
                except: files = -1
            try: analysisCommand = \
              job['attributes']['details']['analysis_runtime_info']['analysisCommand']
            except: analysisCommand = None
            try: functions = job['attributes']['details']['jobStats']['functionsAnalyzed']
            except: functions = -1
            try: paths = job['attributes']['details']['jobStats']['pathsAnalyzed']
            except: paths = -1
            try: defects = int(job['attributes']['details']['jobStats']['defectOccurencesFound']['Total'])
            except: defects = -1
            try: captureTime = timedelta(milliseconds=job['attributes']['metadata']['toolMeta']['cliUsageTime']['capture'])
            except: captureTime = None
            try: captureSize = job['attributes']['metadata']['toolMeta']['captureSize']
            except: captureSize = -1
            try: artifactSize = job['attributes']['metadata']['artifactSize']
            except: artifactSize = -1

            if getEvents:
                endpoint = baseUrl + '/api/jobs/v2/jobs/' + jobId + '/events'
                if (debug >= 3): printCurl(endpoint, 'GET')
                response = session.get(endpoint)
                if debug: print(response)
                if response.status_code != 200: printError(response.json()['errors'][0])

                for event in response.json():
                    if event['key'] == 'idirUploadStart': idirUploadStart = event['timestamp']
                    if event['key'] == 'idirUploadFinish': idirUploadFinish = event['timestamp']
                    if event['key'] == 'jobQueuedStart': jobQueuedStart = event['timestamp']
                    if event['key'] == 'jobQueuedFinish': jobQueuedFinish = event['timestamp']
                    if event['key'] == 'covAnalyzeStart': covAnalyzeStart = event['timestamp']
                    if event['key'] == 'covAnalyzeFinish': covAnalyzeFinish = event['timestamp']
                    if event['key'] == 'jobCompleted': dateCompleted = event['timestamp']
                uploadTime = datetime.strptime(idirUploadFinish, timeFormat) - datetime.strptime(idirUploadStart, timeFormat)
                queueTime = datetime.strptime(jobQueuedFinish, timeFormat) - datetime.strptime(jobQueuedStart, timeFormat)
                scanTime = datetime.strptime(covAnalyzeFinish, timeFormat) - datetime.strptime(covAnalyzeStart, timeFormat)
                totalTime = datetime.strptime(dateCompleted, timeFormat) - datetime.strptime(dateCreated, timeFormat)
                events = {
                    'dateCompleted': dateCompleted,
                    'uploadTime': str(uploadTime).split('.')[0],
                    'queueTime': str(queueTime).split('.')[0],
                    'scanTime': str(scanTime).split('.')[0],
                    'totalTime': str(totalTime).split('.')[0],
                }

            if getRollUpCounts:
                rollups = getRollUps(projectId, runId, limit)
                newcount = rollups[0]['count']
                issueCountTotal = rollups[0]['count']
                try: defectDensity = issueCountTotal / loc * 1000
                except: defectDensity = None
                issues = {
                    'issues': issueCountTotal,
                    'density': defectDensity,
                }

            entry = {
                'jobId': jobId,
                'dateCreated': dateCreated,
                'projectId': projectId,
                'branchId': branchId,
                'state': state,
                'runId': runId,
                'toolVersion': toolVersion,
                'loc': loc,
                'files': files,
                'functions': functions,
                'paths': paths,
                'defects': defects,
                'captureTime': str(captureTime).split('.')[0],
                'captureSize': captureSize,
                'artifactSize': artifactSize,
                'analysisCommand': analysisCommand,
            }
            if getEvents: entry.update(events)
            if getRollUpCounts: entry.update(issues)

        if (state == 'FAILED'):
            try: dateFailed = job['attributes']['dateFailed'].split('+')[0]
            except: dateFailed = None
            failureReason = job['attributes']['details']['failureInfo']['userFriendlyFailureReason']
            entry = {
                'jobId': jobId,
                'dateCreated': dateCreated,
                'projectId': projectId,
                'branchId': branchId,
                'state': state,
                'failureReason' : failureReason,
            }

        if (debug >= 5): print(entry)
        dictionary.append(entry)

    return dictionary

# -----------------------------------------------------------------------------

'''
Function:       getRunProperties
Description:    return properties associated with run (checkers)
Input:          run ID
Output:         list of enabled checkers
'''
def getRunProperties(runId, limit=MAX_LIMIT):
    endpoint = baseUrl + '/api/common/v0/run-properties'
    params = dict([('filter[run-property][run][id][eq]', runId )])
    properties = getPaginatedData(endpoint, params, limit)
    if properties == []:
        return []

    checkers = properties[0]['attributes']['string-list-value']
    return checkers

# -----------------------------------------------------------------------------

'''
Function:       getRuns
Description:    create a dictionary of useful run values for a given branch id
Input:          project id and branch id
Output:         runs
'''
def getRuns(projectId, branchId, limit=MAX_LIMIT, getCheckers=False):
    endpoint = baseUrl + '/api/common/v0/runs'
    params = dict([
        ('filter[run][project][id][eq]', projectId ),
        ('filter[run][revision][branch][id][eq]', branchId),
        ])
    runs = getPaginatedData(endpoint, params, limit)
    if runs == []:
        return []
    #print("runs",runs)
    # loop over the list of runs and grab the fields we want to include in the dictionary
    dictionary = []
    timeFormat = '%Y-%m-%dT%H:%M:%S.%fZ'
    for run in runs:
        #print(run)
        runId = run['id']
        status = run['attributes']['status']
        dateCreated = run['attributes']['creation-date']
        dateCompleted = run['attributes']['completed-date']
        uploadId = run['attributes']['upload-id']
        projectId = run['relationships']['project']['data']['id']
        revisionId = run['relationships']['revision']['data']['id']
        toolId = run['relationships']['tool']['data']['id']
        submitting_userId = run['relationships']['submitting-user']['data']['id']
        submitting_orgId = run['relationships']['submitting-organization']['data']['id']
        if (getCheckers): checkers = ' '.join(getRunProperties(runId, limit))
        else: checkers = ''

        try: previous_runId = run['relationships']['previous-run']['data']['id']
        except: previous_runId = None

        entry = {
            'runId': runId,
            'status': status,
            'dateCreated': dateCreated,
            'dateCompleted': dateCompleted,
            'uploadId': uploadId,
            'projectId': projectId,
            'revisionId': revisionId,
            'toolId': toolId,
            'submitting_userId': submitting_userId,
            'submitting_orgId': submitting_orgId,
            'previous_runId': previous_runId,
            'checkers': checkers,
        }

        if (debug >= 5): print(entry)
        dictionary.append(entry)

    return dictionary

# -----------------------------------------------------------------------------

'''
Function:       addLineNums
Description:    Helper function to getMainEvent to add line numbers to the string
Input:          source code string, first line of main event code
Output:         source code string with line numbers
'''
def addLineNums(srcCode, startLine):
    lines = srcCode.splitlines()
    codeLines = ""
    for line in lines:
        line = str(startLine) + " \t" + line
        startLine += 1
        codeLines += line + "\n"
    return codeLines

# -----------------------------------------------------------------------------

'''
Function:       getMainEvent
Description:    Extracts main event source details (called by getIssues)
Input:          eventList from code-analysis/v0/events-with-source, line of main event
Output:         dict with main event source info
'''
def getMainEvent(eventList, meLine):
    # This will often contain remediation guidance, but it can also have more general
    # support information. There's no simple way to distinguish the two.
    supportDescription = ""

    # Fetch every event with line-number matching the main event.
    # We have to do this because there could be any number of events, with
    # no guarantee as to which events have the "source-before" and which
    # have "source-after" details.  The goal is to stich together the
    # source-before and source-after and create 1 Uber-Source.  There should
    # be only 1 of each dispersed between various events for this line.
    mainEventCode = ""
    for e in eventList:
        if e['line-number'] == meLine:
            if e["event-type"] == "MAIN":
                mainDescription = e['event-description']
            else:
                supportDescription += e['event-description'] + "\n"
            if e['source-before']:
                mainEventCode  = \
                  addLineNums(e['source-before']['source-code'], \
                  e['source-before']['start-line']) + mainEventCode
            if e['source-after']:
                mainEventCode  = mainEventCode + \
                  addLineNums(e['source-after']['source-code'], e['source-after']['start-line'])

    event_dct = {
        'mainevent_description': mainDescription,
        'support_description': supportDescription,
        'mainevent_source': str(mainEventCode)
    }

    return(event_dct)

# -----------------------------------------------------------------------------

def getSource(runId, path):
    endpoint = baseUrl + '/api/code-analysis/v0/source-code'
    params = dict([
        ('run-id',runId),
        ('path',path)
    ])
    if (debug >= 3): printCurl(endpoint, 'GET', params)
    response = session.get(endpoint, params=params)
    if debug: print(response)
    if response.status_code != 200: printError(response.json()['errors'][0])
    return response.text

# -----------------------------------------------------------------------------

'''
Function:       getIssues
Description:    get issues for a given project+branch
Input:          project id, branch id, optional filter dictionary
                Example filter:
                    dict([('filter[issue][issue-key][eq]', 'xyz')])
Output:         issues
'''
def getIssues(projectId, branchId, runId, limit=MAX_LIMIT, filter=True, triage=False, events=True):
    dictionary = []
    issues_data = []
    issues_included = []
    issues_start = datetime.now()
    triage_total_es = 0.0
    events_total_es = 0.0
    closed_date = None

    endpoint = baseUrl + '/api/query/v1/issues'
    params = dict([
        ('project-id', projectId),
        ('include[issue][]', ['severity', 'related-indicators', 'related-taxa'])
        ])

    # filter by runId or branchId but not both
    if runId is not None: params['run-id[]'] = runId
    else: params['branch-id'] = branchId
    if runId is None:
        runId = getLastRunId(branchId)
        #print("Current RunId:\n",runId)
    # update params with optional user-specified filter
    if filter:
        params.update(filter)

    issues_data, issues_included = getPaginatedData(endpoint, params, limit)
    #print("issues_included",issues_included)
    if issues_data == []:
        return []

    # Create the base url so we can build an issue url later
    # branchId is not guaranteed to be known here, so that is added later during issue processing
    __baseUrl = issues_data[0]['links']['self']['href']
    data = urlparse(__baseUrl)
    __baseUrl = data.scheme + '://' + data.netloc
    __baseUrl += '/projects/' + projectId

    timeFormat = '%Y-%m-%dT%H:%M:%S'
    #print("issues data:\n",issues_data)
    # loop over the list of issues
    for issue in issues_data:
        issueKey = issue['attributes']['issue-key']
        findingKey = issue['attributes']['finding-key']
        checker = issue['attributes']['sub-tool']
        issue_type_id = issue['relationships']['issue-type']['data']['id']
        issue_path_id = issue['relationships']['path']['data']['id']
        try: 
            severity = issue['relationships']['severity']['data']['id']
            if severity == "medium":
                severity = 7.5
            elif severity == "high":
                severity = 9.5
            elif severity == "low":
                severity = 5.5
            elif severity == "audit":
                severity = 2
            else:
                severity = 0
        except: severity = None

        # [0] = first detected
        # [1] = fixed by code change
        issue_opened_id = issue['relationships']['transitions']['data'][0]['id']
        try: issue_closed_id = issue['relationships']['transitions']['data'][1]['id']
        except: issue_closed_id = None

        cwe = None
        try:
            # There can be several CWEs, so merge them all in to a single string
            for taxa_data in issue['relationships']['related-taxa']['data']:
                if cwe is None:
                    cwe = "CWE-"+ taxa_data['id']
                else:
                    cwe += ",CWE-" + taxa_data['id']
        except: cwe = None
        indicators = None
        if issue['relationships']['related-indicators']['data']:
            # TODO just pull the id values as a straight list
            indicator_list = []
            for ind_dct in issue['relationships']['related-indicators']['data']:
                for ind_key, val in ind_dct.items():
                    if ind_key == 'id':
                        indicator_list.append(val)
            indicators = ','.join(indicator_list)
        # iterate through included to get name, description, local-effect, issue-type
        for issue_included in issues_included:
            
            if issue_included['id'] == issue_type_id:
                # check for type "issue-type"? Is id unique?
                try: name = issue_included['attributes']['name']
                except: name = None
                try: description = issue_included['attributes']['description']
                except: description = None
                try: local_effect = issue_included['attributes']['local-effect']
                except: local_effect = None
                try: type = issue_included['attributes']['issue-type']
                except: type = None
            if issue_included['id'] == issue_path_id:
                dirsep = '/'
                try: path = dirsep.join(issue_included['attributes']['path'])
                except: path = None

            if issue_included['id'] == issue_opened_id:
                # TODO should we check for issue_included['type'] == 'transition'??
                first_detected = datetime.strptime( \
                   issue_included['attributes']['transition-date'].split('.')[0], \
                   timeFormat)

                # NOTE: state/cause stored here are the first detected state/cause
                #  -- not necessarily _current state_ of the issue.
                state = issue_included['attributes']['transition-type']
                cause = issue_included['attributes']['cause']
                causeDesc = issue_included['attributes']['human-readable-cause']
                branchId = issue_included['attributes']['branch-id']
                revisionId = issue_included['attributes']['revision-id']

                # Construct issue URL
                url = __baseUrl + '/branches/' + branchId
                url += '/revisions/'
                url += revisionId
                url += '/issues/' + issueKey

            if issue_closed_id and issue_included['id'] == issue_closed_id:
                closed_date = datetime.strptime( \
                  issue_included['attributes']['transition-date'].split('.')[0], \
                  timeFormat)

        if triage:
            triage_start = datetime.now()
            triage_owner = None
            triage_status = None
            triage_comment = None
            triage_jira_ticket = None

            # TODO - add getTriageCurrent and use it instead
            triage_data = getTriageHistory(issueKey, projectId)
            if triage_data:
                comments = []
                for triage in reversed(triage_data): # go through all history updates from oldest to latest
                    timestamp = triage['attributes']['timestamp'].split('.')[0]
                    timestamp = datetime.strptime(timestamp, timeFormat)
                    # TODO replace for-loop with python dict['key'='value'] code
                    for triage_hist_value in triage['attributes']['triage-history-values']:
                        if triage_hist_value['attribute-semantic-id'] == 'OWNER':
                            triage_userid = triage_hist_value['value']
                            triage_owner = getUserById(triage_userid)['data']['attributes']['name']
                        elif triage_hist_value['attribute-semantic-id'] == 'COMMENTARY':
                            if  triage_hist_value['display-value'].startswith('JIRA ticket:'):
                                triage_jira_ticket = triage_hist_value['display-value'][len('JIRA ticket:')] # Jira ticket url should be first
                            if timestamp:
                                comments.append(str(timestamp) + ' ' + triage_hist_value['display-value'])
                            else:
                                comments.append(triage_hist_value['display-value'] )
                        # TODO - API is stuffing triage status into the Dismiss attribute, this may change
                        elif triage_hist_value['attribute-name'] == 'Dismiss':
                            triage_status = triage_hist_value['display-value']
                            if triage_status.startswith('Dismissed'):
                                closed_date = timestamp
                if comments:
                    triage_comment = ']\n['.join(comments)
                    triage_comment = '[' + triage_comment + ']'

            # create the dictionary entry
            triage_dct = {
                'owner': triage_owner, 'comment': triage_comment, \
                'status': triage_status, 'jira': triage_jira_ticket
                 }
            triage_end = datetime.now()
            triage_total = triage_end - triage_start
            triage_total_es += triage_total.total_seconds()

        if events:
            if runId == None:
                print("FATAL: runId required by events endpoint, caller should set")
                sys.exit(1)
            events_start = datetime.now()
            endpoint = baseUrl + '/api/code-analysis/v0/events-with-source'
            params = dict([('finding-key', str(findingKey)),
                ('run-id', runId),
                ('locator-path', str(path))
                ])
            headers = {'Authorization': 'Bearer ' + jwt,
                'Accept-Language': 'en'}

            if (debug >= 3): printCurl(endpoint, 'GET', params)
            response = session.get(endpoint, params=params, headers=headers)
            if debug: print(response)
            if response.status_code != 200: printError(response.json()['errors'][0])

            line = response.json()['data'][0]['main-event-line-number']
            line_dct = {'line': line}
            #print(line_dct)

            # Save main event (mainevent_description, mainevent_source, support_description)
            event_dct = getMainEvent(response.json()['data'][0]['events'], line)
            #print(event_dct)
            events_end = datetime.now()
            events_total = events_end - events_start
            events_total_es += events_total.total_seconds()
            
            '''for i,j in event_dct.items():
                print(i,j)'''
            

        age = datetime.utcnow() - first_detected
        if (closed_date is not None): ttr = closed_date - first_detected
        else: ttr = first_detected - first_detected
        Desc = [description]
        # create the dictionary entry
        entry = {'projectId': projectId, 'branchId': branchId, \
             'issue-key': issueKey, 'finding-key': findingKey, \
             'checker': checker, 'severity': severity, \
             'type': type,  'name': name, \
             'description': ".".join(Desc) , 'path': path, \
             'first_detected': first_detected , 'url': url, \
             'state' : state, 'cause' : cause, 'causeDesc' : causeDesc,
             'cwe' : cwe, 'indicators' : indicators, \
             'branchId' : branchId, 'revisionId' : revisionId, \
             'closed_date': str(closed_date), \
             'age': age, 'ttr': ttr
             }
        if triage:
            entry.update(triage_dct)
        if events:
            entry.update(line_dct)
            entry.update(event_dct)

        if (debug >= 5): print(entry)
        dictionary.append(entry)

    if (debug >= 1):
        issues_total = datetime.now() - issues_start
        issues_total_secs = issues_total.total_seconds()
        print('total getIssues elapsed time: ' + str(issues_total_secs))
        if triage:
            print('total triage elapsed time:' + str(triage_total_es))
        if events:
            print('total events elapsed time:' + str(events_total_es))
        #print("Dictionary",dictionary)
    return dictionary

# -----------------------------------------------------------------------------

'''
Function:       cmpIssuesForRun
Description:    new = present in current, but not previous scan
                fixed = present in previous, but not current scan
Input:          projectId, curr_runId, prev_runId, getTriage (optional, defaults to False),
                    userFilter (optional, for any additional filtering)
Output:         new_issues and fixed_issues
'''
def cmpIssuesForRuns(projectId, curr_runId, prev_runId, getTriage=False, getEvents=True, userFilter=None):
    limit=MAX_LIMIT

    filter = dict([('compare-run-id[]', prev_runId)])
    if userFilter:
        # append any optional filter specified
        filter.update(userFilter)

    new_issues = getIssues(projectId, '', curr_runId, limit, filter, getTriage, getEvents)
    #print(new_issues)
    # Note: overwriting the default 'opened' filter in getIssues
    filter = dict([('compare-run-id[]', curr_runId), ('filter[issue][status][eq]', 'closed')])

    fixed_issues = getIssues(projectId, '', prev_runId, limit, filter, getTriage, getEvents)

    return new_issues, fixed_issues

# -----------------------------------------------------------------------------

'''
Function:       getOrgId
Description:
Input:          none
Output:         org id
'''
def getOrgId():
    endpoint = baseUrl + '/api/auth/v1/organizations'
    if (debug >= 3): printCurl(endpoint, 'GET')
    response = session.get(endpoint)
    if debug: print(response)
    if response.status_code != 200: printError(response.json()['errors'][0])
    return response.json()['data'][0]['id']

# -----------------------------------------------------------------------------

'''
Function:       getOrgOwners
Description:
Input:          org id
Output:         array of org owners
'''
def getOrgOwners(orgId):
    endpoint = baseUrl + '/api/auth/v1/organizations/' + orgId
    if (debug >= 3): printCurl(endpoint, 'GET')
    response = session.get(endpoint)
    if debug: print(response)
    if response.status_code != 200: printError(response.json()['errors'][0])
    return response.json()['data']['relationships']['owners']['data']

# -----------------------------------------------------------------------------

'''
Function:       getProjectId
Description:
Input:          project name
Output:         project id
'''
def getProjectId(projectName):
    endpoint = baseUrl + '/api/common/v0/projects'
    params = dict([
        ('page[limit]', MAX_LIMIT),
        ('filter[project][name][eq]', projectName)
    ])
    if (debug >= 3): printCurl(endpoint, 'GET', params)
    response = session.get(endpoint, params=params)
    if debug: print(response)
    if response.status_code != 200: printError(response.json()['errors'][0])

    if response.json()['meta']['total'] == 0:
        print('FATAL: project ' + projectName + ' not found')
        sys.exit(1)
    return response.json()['data'][0]['id']

# -----------------------------------------------------------------------------

'''
Function:       getApplicationId
Description:    get Polaris Application Id
Input:          application name
Output:         application id
'''
def getApplicationId(applicationName):
    endpoint = baseUrl + '/api/common/v0/applications'
    params = dict([('page[limit]', MAX_LIMIT),
        ('filter[application][name][eq]', applicationName)])
    if (debug >= 3): printCurl(endpoint, 'GET', params)
    response = session.get(endpoint, params=params)
    if debug: print(response)
    if response.status_code != 200: printError(response.json()['errors'][0])

    if (response.json()['data'] == []):
        print('FATAL: application ' + applicationName + ' not found')
        sys.exit(1)
    return response.json()['data'][0]['id']

# -----------------------------------------------------------------------------

'''
Function:       getReportId
Description:    get Polaris Reporting Plaform Application Id
Input:          application name
Output:         application id
'''
def getReportId(applicationName):
    endpoint = baseUrl + '/reporting/rpps/v1/api/rpps/applications'
    params = dict([('searchTerm', applicationName)])
    if (debug >= 3): printCurl(endpoint, 'GET', params)
    response = session.get(endpoint, params=params)
    if debug: print(response)
    if response.status_code != 200: printError(response.json()['errors'][0])

    if (response.json()['object']['content'] == []):
        print('FATAL: application ' + applicationName + ' not found')
        sys.exit(1)
    return response.json()['object']['content'][0]['applicationUID']

# -----------------------------------------------------------------------------

'''
Function:       createReportMap
Description:    create an mapping of report ids to report names
Input:
Output:         dictionary of report names indexed by report id
'''
def createReportMap():
    endpoint = baseUrl + '/reporting/rpps/v1/api/rpps/applications'
    response = session.get(endpoint)
    if debug: print(response)
    if response.status_code != 200: printError(response.json()['errors'][0])
    dictionary = {}
    for report in response.json()['object']['content']:
        dictionary[report['applicationUID']] = report['name']
    return dictionary

# -----------------------------------------------------------------------------

'''
Function:       createUserMap
Description:    create an mapping of user ids to username
Input:
Output:         dictionary of usernames indexed by user id
'''
def createUserMap():
    endpoint = baseUrl + '/api/auth/v1/users'
    dictionary = {}
    for user in getPaginatedData(endpoint):
        dictionary[user['id']] = user['attributes']['username']
    return dictionary

# -----------------------------------------------------------------------------

'''
Function:       createProjectMap
Description:    create an mapping of project ids to project names
Input:
Output:         dictionary of project names indexed by project id
'''
def createProjectMap():
    endpoint = baseUrl + '/api/common/v0/projects'
    dictionary = {}
    for project in getPaginatedData(endpoint):
        dictionary[project['id']] = project['attributes']['name']
    return dictionary

# -----------------------------------------------------------------------------

'''
Function:       createApplicationMap
Description:    create an mapping of application ids to application names
Input:
Output:         dictionary of application names indexed by application id
'''
def createApplicationMap():
    endpoint = baseUrl + '/api/common/v0/applications'
    dictionary = {}
    for application in getPaginatedData(endpoint):
        dictionary[application['id']] = application['attributes']['name']
    return dictionary

# -----------------------------------------------------------------------------

'''
Function:       createProjectOwnerMap
Description:    create a mapping of project ids to project owner
Input:
Output:         dictionary of project owners indexed by project id
'''
def createProjectOwnerMap():
    userMap = createUserMap()
    endpoint = baseUrl + '/api/auth/v1/role-assignments'
    dictionary = {}
    for roleAssignment in getPaginatedData(endpoint):
        if 'projects' not in roleAssignment['attributes']['object']: continue
        projectId = roleAssignment['attributes']['object'].split(":")[3]
        try:
            userId = roleAssignment['relationships']['user']['data']['id']
            dictionary[projectId] = userMap[userId]
        except:
            dictionary[projectId] = None
    return dictionary

# -----------------------------------------------------------------------------

'''
Function:       getProjects
Description:    create a dictionary of useful project values
Input:          limit. optional: projectId to query a single project
Output:         dictionary of useful project values
'''
def getProjects(limit=MAX_LIMIT, projectId=None):
    dictionary = []
    projects = []
    projectOwnerMap = createProjectOwnerMap()

    params = dict([('page[limit]', str(limit))])

    if (projectId):
        endpoint = baseUrl + '/api/common/v0/projects/' + projectId
        projects.append(getPaginatedData(endpoint, params, limit))
    else:
        endpoint = baseUrl + '/api/common/v0/projects'
        projects = getPaginatedData(endpoint, params, limit)

    for project in projects:
        # grab the fields we want to include in the dictionary
        id = project['id']
        name = project['attributes']['name']
        try:
            userId = projectOwnerMap[id]
        except:
            userId = None

        # create the dictionary entry
        entry = {'id': id, 'name': name, 'owner': userId, \
          'properties': project['attributes']['properties']}
        if (debug >= 5): print(entry)

        # append it to the dictionary
        dictionary.append(entry)

    return dictionary

# -----------------------------------------------------------------------------

'''
Function:       getRoleAssignmentId
Description:
Input:          user id
Output:         role-assignment id
'''
def getRoleAssignmentId(userid):
    endpoint = baseUrl + '/api/auth/v1/users/' + userid + "/roleassignments"
    if (debug >= 3): printCurl(endpoint, 'GET')
    response = session.get(endpoint)
    if debug: print(response)
    if response.status_code != 200: printError(response.json()['errors'][0])
    return response.json()['data'][0]['id']

# -----------------------------------------------------------------------------

'''
Function:       getRoleId
Description:    return role id for role name
Input:          role name
Output:         role id
'''
def getRoleId(rolename):
    endpoint = baseUrl + '/api/auth/v1/roles'
    if (debug >= 3): printCurl(endpoint, 'GET')
    response = session.get(endpoint)
    if debug: print(response)
    if response.status_code != 200: printError(response.json()['errors'][0])

    for role in response.json()['data']:
        if (role['attributes']['rolename'] == rolename ):
            return role['id']
    print('FATAL: role ' + rolename + ' not found')
    sys.exit(1)

# -----------------------------------------------------------------------------

'''
Function:       getRoleMap
Description:
Input:          none
Output:         array of role names indexed by role id
'''
def getRoleMap():
    endpoint = baseUrl + '/api/auth/v1/roles'
    if (debug >= 3): printCurl(endpoint, 'GET')
    response = session.get(endpoint)
    if debug: print(response)
    if response.status_code != 200: printError(response.json()['errors'][0])

    roleMap = {}
    for role in response.json()['data']:
        roleMap[role['id']] = role['attributes']['rolename']
    return roleMap

# -----------------------------------------------------------------------------

'''
Function:       getUserId
Description:
Input:          username or email address
Output:         user id
'''
def getUserId(user, service=False):
    endpoint = baseUrl + '/api/auth/v1/users'
    params = dict([('filter[users][username][eq]', user)])
    params.update([('filter[users][automated]', service)])
    if (debug >= 3): printCurl(endpoint, 'GET', params)
    response = session.get(endpoint, params=params)
    if debug: print(response)
    if response.status_code != 200: printError(response.json()['errors'][0])

    if (response.json()['meta']['total'] != 0): return response.json()['data'][0]['id']

    params = dict([('filter[users][email][eq]', user)])
    if (debug >= 3): printCurl(endpoint, 'GET', params)
    response = session.get(endpoint, params=params)
    if debug: print(response)

    if response.status_code != 200: printError(response.json()['errors'][0])
    if (response.json()['meta']['total'] != 0): return response.json()['data'][0]['id']

    print("FATAL: username or email " + user + " not found")
    sys.exit(1)

# -----------------------------------------------------------------------------

'''
Function:       getUser
Description:    returns the full user data json
Input:          user = username or email address
                service = true/false to query service accounts
Output:         user data json
'''
def getUser(user, service=False):
    endpoint = baseUrl + '/api/auth/v1/users'
    params = dict([('filter[users][username][eq]', user)])
    params.update([('filter[users][automated]', service)])
    if (debug >= 3): printCurl(endpoint, 'GET', params)
    response = session.get(endpoint, params=params)
    if debug: print(response)
    if response.status_code != 200: printError(response.json()['errors'][0])

    if (response.json()['meta']['total'] != 0): return response.json()

    del params['filter[users][username][eq]']
    params.update([('filter[users][email][eq]', user)])
    if (debug >= 3): printCurl(endpoint, 'GET', params)
    response = session.get(endpoint, params=params)
    if debug: print(response)
    if response.status_code != 200: printError(response.json()['errors'][0])
    if (response.json()['meta']['total'] != 0): return response.json()

    print('WARNING: no matching username or email found')
    return None

# -----------------------------------------------------------------------------

'''
Function:       getUserById
Description:    returns the full user data json
Input:          user id
Output:         user data json
'''
def getUserById(userId):
    endpoint = baseUrl + '/api/auth/v1/users/' + userId
    if (debug >= 3): printCurl(endpoint, 'GET')
    response = session.get(endpoint)
    if debug: print(response)
    if response.status_code != 200: printError(response.json()['errors'][0])
    return response.json()

# -----------------------------------------------------------------------------

'''
Function:       createUserOrgRoleMap
Description:    create a mapping of user ids to user org role
Input:          limit
Output:         dictionary of user org roles indexed by user id
'''
def createUserOrgRoleMap(service, limit=MAX_LIMIT):
    dictionary = {}
    orgId = getOrgId()
    roleMap = getRoleMap()
    endpoint = baseUrl + '/api/auth/v1/role-assignments'
    params = dict([('page[limit]', str(limit))])
    params.update([('filter[role-assignments][user][automated]', service)])
    for roleAssignment in getPaginatedData(endpoint, params, limit):
        if orgId not in roleAssignment['attributes']['object']: continue
        userId = roleAssignment['relationships']['user']['data']['id']
        roleId = roleAssignment['relationships']['role']['data']['id']
        dictionary[userId] = roleMap[roleId]
    return dictionary

# -----------------------------------------------------------------------------

'''
Function:       getUsers
Description:    create a dictionary of useful user values
Input:          none
Output:         dictionary of useful user values
'''
def getUsers(groupId, filter, service, limit=MAX_LIMIT):
    endpoint = baseUrl + '/api/auth/v1/users'
    params = dict([('page[limit]', str(limit))])
    if filter: params.update(filter)
    params.update([('filter[users][automated]', service)])

    # improve performance by creating a user org role map
    userIdOrgRoleMap = createUserOrgRoleMap(service, limit)

    # loop over the list of users and grab the fields we want to include in the dictionary
    dictionary = []
    for user in getPaginatedData(endpoint, params, limit):
        id = user['id']
        enabled = user['attributes']['enabled']
        name = user['attributes']['name']
        email = user['attributes']['email']
        username = user['attributes']['username']
        firsttime = user['attributes']['first-time']
        role = userIdOrgRoleMap[id]
        if groupId != None:
            ids = [ group['id'] for group in user['relationships']['groups']['data'] ]
            if groupId not in ids: continue

        entry = {'id': id, 'username': username, 'name': name, 'email': email, 'enabled': enabled, 'role': role, 'firsttime': firsttime}
        if (debug >= 5): print(entry)
        dictionary.append(entry)

    return dictionary

# -----------------------------------------------------------------------------

'''
Function:       getTriageHistory
Description:    Returns complete triage history for an issue in a project
Input:          issue id
                project id
Output:         list of triage history items
'''
def getTriageHistory(issueId, projectId):
    endpoint = baseUrl + '/api/triage-query/v1/triage-history-items'
    triageList = []
    params = dict([
        ('filter[triage-history-items][issue-key][eq]', issueId),
        ('filter[triage-history-items][project-id][eq]', projectId)
    ])
    return getPaginatedData(endpoint, params)

# -----------------------------------------------------------------------------

'''
Function:       getTaxonomyIds
Description:    Returns a dict of all available taxonomies
Input:          none
Output:         Dictionary of taxonomy IDs indexed by name (e.g. "issue-kind")
                TODO: paginate... but currently there are only 8 taxons
'''
def getTaxonomyIds():
    endpoint = baseUrl + '/api/taxonomy/v0/taxonomy-info'
    params = dict([('page[limit]', MAX_LIMIT)])
    headers = {"Authorization": "Bearer " + jwt}
    if (debug >= 3): printCurl(endpoint, 'GET', params)
    response = requests.get(endpoint, headers=headers, params=params)
    if debug: print(response)
    if response.status_code != 200: printError(response.json()['errors'][0])
    taxons = {}
    for taxon in response.json()['data']:
        id = taxon['id']
        type = taxon['attributes']['type']
        taxons[type] = id
    return taxons

# -----------------------------------------------------------------------------

'''
Function:       getApplication
Description:    returns the full application data json
Input:          application Id
Output:         application data json
'''
def getApplication(applicationId):
    endpoint = baseUrl + '/api/common/v0/applications/' + applicationId
    params = dict([('page[limit]', MAX_LIMIT)])
    if (debug >= 3): printCurl(endpoint, 'GET', params)
    response = session.get(endpoint, params=params)
    if debug: print(response)
    if response.status_code != 200: printError(response.json()['errors'][0])
    return response.json()

# -----------------------------------------------------------------------------

'''
Function:       getIssuesOverTime
Description:    fetches the issues-over-time graph data for a project
Input:          project id, branch id, start date, offset (default=90days),
Output:         open and closed info
'''
def getIssuesOverTime(projectId, branchId, startDate=False, offset=90):
    endpoint = baseUrl + '/api/query/v1/counts/issues-over-time'
    timeFormat = '%Y-%m-%dT%H:%M:%S.%fZ'

    # Default to last 90 days if no date/offset provided
    if startDate is False:
        today = datetime.now()
        # add 1 day to today because issues-over-time actually is 1 day in the future
        startDate = today - timedelta(days=offset) + timedelta(days=1)

    startStr = datetime.strftime(startDate, timeFormat)
    endDate = startDate + timedelta(days=offset)
    endStr = datetime.strftime(endDate, timeFormat)

    headers = {'Authorization': 'Bearer ' + jwt, 'Accept-Language': 'en'}
    params = dict([('page[limit]', MAX_LIMIT),
        ('project-id', projectId),
        ('branch-id', branchId),
        ('start-date', startStr),
        ('end-date', endStr),
        ('group-by', '[issue][status]')
        ])
    if (debug >= 3): printCurl(endpoint, 'GET', params)
    response = session.get(endpoint, params=params, headers=headers)
    if debug: print(response)
    if response.status_code != 200: printError(response.json()['errors'][0])

    issuesOverTime = {}
    # should just be "Open" and "Closed"
    for status in response.json():
        issuesOverTime[status['name']] = status['data']

    return(issuesOverTime)

# -----------------------------------------------------------------------------
# ---- Polaris SET functions
# -----------------------------------------------------------------------------

'''
Function:       setOrgRole
Description:
Input:          org id
                user id
                role id
Output:         role assignment id
'''
# TODO: merge with setRole as special case patch vs post
def setOrgRole(orgId, userId, roleId):
    endpoint = baseUrl + '/api/auth/v1/role-assignments'
    params = dict([('page[limit]', MAX_LIMIT),
       ('filter[role-assignments][user][id][eq]', userId),
       ('filter[role-assignments][user][automated]', 'true')])
    if (debug >= 3): printCurl(endpoint, 'GET', params)
    response = session.get(endpoint, params=params)
    if debug: print(response)
    if response.status_code != 200: printError(response.json()['errors'][0])

    #assuming only 1 array element is returned
    roleAssignmentId = response.json()['data'][0]['id']

    return setRole(orgId, None, None, None, userId, None, roleId, roleAssignmentId)

# -----------------------------------------------------------------------------

'''
Function:       setRole
Description:    set a role for a user or group on a project, application, report or organization
Input:          orgId
                one or none of projectId, applicationId, reportId
                one of userId, groupId
                roleId
                roleAssignmentId (only for org role update)
Output:         roleAssignmentId
'''
def setRole(orgId, projectId, applicationId, reportId, userId, groupId, roleId, roleAssignmentId=None):
    endpoint = baseUrl + '/api/auth/v1/role-assignments'
    json_data = {
        'data' : {
            'type' : 'role-assignments',
            'relationships' : {
                'organization' : {
                    'data' : {
                        'id' : orgId,
                        'type' : 'organizations'
                    }
                },
                'role' : {
                    'data' : {
                        'id' : roleId,
                        'type' : 'roles'
                    }
                }
            }
        }
    }

    if projectId != None:
        attribute_data = {
            'attributes' : {
                'object' : 'urn:x-swip:projects:' + projectId,
                'expires-by' : 'null'
            }
        }
    elif applicationId != None:
        attribute_data = {
            'attributes' : {
                 'object' : 'urn:x-swip:applications:' + applicationId,
                 'expires-by' : 'null'
            }
        }
    elif reportId != None:
        attribute_data = {
            'attributes' : {
                 'object' : 'urn:x-reporting:applications:' + reportId,
                 'expires-by' : 'null'
            }
        }
    else:
        attribute_data = {
            "attributes": {
                "object": "urn:x-swip:organizations:" + orgId
            },
        }
    json_data['data'].update(attribute_data)

    if userId != None:
        user_data = {
             'user' : {
                'data' : {
                   'id' : userId,
                   'type' : 'users'
                }
             }
        }
        json_data['data']['relationships'].update(user_data)

    if groupId != None:
        group_data = {
             'group' : {
                'data' : {
                   'id' : groupId,
                   'type' : 'groups'
                }
             }
        }
        json_data['data']['relationships'].update(group_data)

    if (debug >= 5): print(json_data)
    if (debug >= 3): printCurl(endpoint, 'POST', None, json.dumps(json_data))
    if projectId or applicationId or reportId:
        response = session.post(endpoint, data=json.dumps(json_data))
        if debug: print(response)
        # Polaris BUG - returns 201 on success, should be 200
        if response.status_code != 201: printError(response.json()['errors'][0])
    else: # org role update
        endpoint = endpoint + '/' + roleAssignmentId
        response = session.patch(endpoint, data=json.dumps(json_data))
        if debug: print(response)
        if response.status_code != 200: printError(response.json()['errors'][0])
    return response.json()['data']['id']

# -----------------------------------------------------------------------------

'''
Function:       getRoleAssignmentId
Description:    return role assignment id for given combination of
Input:          orgId
                one or none of projectId, applicationId, reportId
                one of user, group
                roleId
                service = true/false
Output:         role assignment id, or None if not found
'''
def getRoleAssignmentId(orgId, projectId, applicationId, reportId, user, group, roleId, service):
    endpoint = baseUrl + '/api/auth/v1/role-assignments'
    if user:
        params = dict([('filter[role-assignments][name][eq]', user)])
        params.update([('filter[role-assignments][user][automated]', service)])
    else:
        params = dict([('filter[role-assignments][name][eq]', group)])
    roleAssignments = getPaginatedData(endpoint, params)

    for ra in roleAssignments:
        if debug: print('object = ' + ra['attributes']['object'])
        if debug: print('role id = ' + ra['relationships']['role']['data']['id'])
        if projectId and ra['attributes']['object'] == 'urn:x-swip:projects:' + projectId and ra['relationships']['role']['data']['id'] == roleId:
            return ra['id']
        if applicationId and ra['attributes']['object'] == 'urn:x-swip:applications:' + applicationId and ra['relationships']['role']['data']['id'] == roleId:
            return ra['id']
        if reportId and ra['attributes']['object'] == 'urn:x-reporting:applications:' + reportId and ra['relationships']['role']['data']['id'] == roleId:
            return ra['id']
        if projectId == None and applicationId == None and reportId == None and ra['attributes']['object'] == 'urn:x-swip:organizations:' + orgId:
            return ra['id']

    print('WARNING: no matching role assignment found')
    return None

# -----------------------------------------------------------------------------

'''
Function:       deleteRoleAssigment
Description:    delete a role assignment
Input:          roleAssignmentId
Output:
'''
def deleteRoleAssigment(roleAssignmentId):
    endpoint = baseUrl + '/api/auth/v1/role-assignments/' + roleAssignmentId

    # confirm we are not deleting an org role assignment
    response = session.get(endpoint)
    if debug: print(response)
    if response.status_code != 200: printError(response.json()['errors'][0])
    if response.json()['data']['attributes']['object'].split(':')[2] == 'organizations':
        print('WARNING: attempting to delete org role assignment')
        return

    response = session.delete(endpoint)
    if debug: print(response)
    # Polaris BUG - returns 204 on success, should be 200
    if response.status_code != 204: printError(response.json()['errors'][0])

# -----------------------------------------------------------------------------

'''
Function:       setTriage
Description:    Sets a triage comment for an issue
Input:          project id
                issue id
                triage data dict (ex. {'COMMENTARY': 'my comment', 'OWNER': 'id'})
Output:         API response
'''
def setTriage(projectId, issueId, triage_data):
    endpoint = baseUrl + '/api/triage-command/v1/triage-issues'
    json_data = {
        'data' : {
            'attributes' : {
                'issue-keys': [issueId],
                'project-id': projectId,
                'triage-values': triage_data
            },
            'type':'triage-issues'
        }
    }
    if (debug >= 5): print(json_data)
    response = session.post(endpoint, data=json.dumps(json_data))
    if debug: print(response)
    # Polaris BUG - returns 201 on success, should be 200
    if response.status_code != 201: printError(response.json()['errors'][0])
    return response

# -----------------------------------------------------------------------------

'''
Function:       createUser
Description:    create a user
Input:          orgId, username, displayname, email
Output:         userId
'''
def createUser(orgId, username, displayname, email):
    endpoint = baseUrl + '/api/auth/v1/users'
    json_data = {
        'data': {
            'type': 'users',
            'attributes': {
                'email': email,
                'name': displayname,
                'username': username,
                'enabled': True,
            },
            "relationships": {
                "organization": {
                    "data": {
                        "type": "organizations",
                        "id": orgId
                    }
                }
            }
        }
    }
    if (debug >= 5): print(json_data)
    response = session.post(endpoint, data=json.dumps(json_data))
    if debug: print(response)
    if response.status_code != 200: printError(response.json()['errors'][0])
    return response.json()['data']['id']

# -----------------------------------------------------------------------------

'''
Function:       changeUserPassword
Description:    change a user's password (must already have one set)
Input:          orgId, userId, oldpassword, newpassword
Output:
'''
def changeUserPassword(orgId, userId, oldpassword, newpassword):
    endpoint = baseUrl + '/api/auth/v1/users/' + userId
    json_data = {
        'data': {
            'type': 'users',
            'id': userId,
            'attributes': {
                'password-login': {
                    'password': newpassword,
                    'oldPassword': oldpassword
                },
            },

            "relationships": {
                "organization": {
                    "data": {
                        "type": "organizations",
                        "id": orgId
                    }
                }
            }
        }
    }
    if (debug >= 5): print(json_data)
    response = session.patch(endpoint, data=json.dumps(json_data))
    if debug: print(response)
    if response.status_code != 200: printError(response.json()['errors'][0])

# -----------------------------------------------------------------------------
