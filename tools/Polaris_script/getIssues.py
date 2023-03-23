#!/usr/bin/python
'''
Copyright (c) 2020 Synopsys, Inc. All rights reserved worldwide. The information
contained in this file is the proprietary and confidential information of
Synopsys, Inc. and its licensors, and is supplied subject to, and may be used
only by Synopsys customers in accordance with the terms and conditions of a
previously executed license agreement between Synopsys and that customer.

Purpose: get issues for a given project & branch

Requires:
pip install requests pandas

Usage:
getIssues.py [-h] [--debug DEBUG] [--url URL] [--token TOKEN] --project PROJECT
             [--branch BRANCH | --run RUN] [--compare COMPARE]
             [--all | --opened | --closed | --untriaged | --bugs | --dismissed | --new | --fixed | --date DATE | --age AGE]
             [--path PATH] [--quality | --security] [--legacy | --nonlegacy]
             [--spec SPEC] [--csv] [--html] [--email EMAIL] [--exit1-if-issues]

get issues for a given project & branch

optional arguments:
  -h, --help         show this help message and exit
  --debug DEBUG      set debug level [0-9]
  --url URL          Polaris URL
  --token TOKEN      Polaris Access Token
  --project PROJECT  project name
  --branch BRANCH    branch name
  --run RUN          run id
  --compare COMPARE  comparison branch name for new or fixed
  --all              all issues in project
  --opened           open issues (default)
  --closed           closed / fixed issues
  --untriaged        untriaged issues
  --bugs             to-be-fixed issues
  --dismissed        dismissed issues
  --new              new issues relative to comparison branch
  --fixed            fixed issues relative to comparison branch
  --date DATE        issues newer than date YYYY-MM-DDTHH:MM:SS
  --age AGE          issues older than AGE days
  --path PATH        limit issues to path
  --quality          quality issues
  --security         security issues
  --legacy           legacy issues
  --nonlegacy        non-legacy issues
  --spec SPEC        report specification
  --csv              output to CSV
  --html             output to HTML
  --email EMAIL      comma delimited list of email addresses
  --exit1-if-issues  exit with error code 1 if issues found

where SPEC is a comma delimited list of one or more of the following:
  projectId         project id
  branchId          branch id
  issue-key         issue key
  finding-key       finding key
  checker           checker aka subtool
  severity          severity
  type              issue type
  local_effect      local effect
  name              checker description
  description       description
  path              file path
  state             state (open/closed)
  status            triage status
  first_detected    date first detected on
  closed_date       date issue was closed
  age               days since issue first detected
  ttr               time to resolution in days
  url               URL to issue on Polaris
  cwe               List of CWE's associated with issues
  Evidence          Code snippet from the scan
  Vulnerability desc - Description of the code snippet
  Support description - Additional info on the code snippet
  
Examples:

list open issues:
python getIssues.py --project cs-polaris-api-scripts

list closed (fixed + dismissed) issues:
python getIssues.py --project cs-polaris-api-scripts --closed

list dismissed issues:
python getIssues.py --project cs-polaris-api-scripts --dismissed

list issues detected after 2021-05-01 and output to csv:
python getIssues.py --project cs-polaris-api-scripts --date 2021-05-01T00:00:00 --csv

list issues older than 30 days and display owner:
python getIssues.py --project cs-polaris-api-scripts --age 30 --spec path,checker,name,first_detected,owner,age

list new issues since previous scan and send as email:
python getIssues.py --project chuckaude-hello-java --branch new --new --email aude@synopsys.com

break the build if any new issues are detected:
python getIssues.py --project chuckaude-hello-java --branch new --exit1-if-issues

list fixed issues since previous scan and display time to resolution
python getIssues.py --project chuckaude-hello-java --branch fixed --fixed --spec path,checker,name,ttr

list new issues compared to master and fail the merge request with email:
python getIssues.py --project chuckaude-hello-java --branch merge-request --compare master \
    --new --email aude@synopsys.com --exit1-if-issues
'''

import sys
import os
import argparse
import polaris
import json
import requests
import pandas as pd

pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 50)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 300)

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# -----------------------------------------------------------------------------

def send_email(receiver_email):

    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = os.getenv('SMTP_PORT')
    smtp_ssl = os.getenv('SMTP_SSL')
    smtp_tls = os.getenv('SMTP_TLS')
    smtp_username = os.getenv('SMTP_USERNAME')
    smtp_password = os.getenv('SMTP_PASSWORD')
    sender_email = os.getenv('SENDER_EMAIL')
    if not all([smtp_server,smtp_port,smtp_username,smtp_password,sender_email]):
        print('FATAL: SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, SENDER_EMAIL must be set to send email')
        sys.exit(1)

    message = MIMEMultipart('alternative')
    message['Subject'] = 'issue report for ' + args.project + '/' + args.branch
    if args.new: message['Subject'] = 'new ' + message['Subject']
    if args.fixed: message['Subject'] = 'fixed ' + message['Subject']
    message['From'] = sender_email
    message['To'] = receiver_email

    # Create the plain-text and HTML version of your message
    #text = str(df)
    html = '<html>\n<body>\n' + df.to_html(escape=False) + '\n</body>\n</html>\n'

    # Turn these into plain/html MIMEText objects
    #part1 = MIMEText(text, 'plain')
    #part2 = MIMEText(html, 'html')

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    try:
        if smtp_ssl: server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        else: server = smtplib.SMTP(smtp_server, smtp_port)
        if smtp_tls: server.starttls()
        server.ehlo()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.close()
        print('email sent')
    except:
        print('email failure')

# -----------------------------------------------------------------------------

def addKindFilter():
    if args.quality: query="quality"
    elif args.security: query="security"

    taxons = polaris.getTaxonomyIds()
    taxonId = taxons['issue-kind']
    kind_filter = dict([
        ('filter[issue][taxonomy][id][' + taxonId + '][taxon][$eq]', query)
        ])
    return(kind_filter)

# -----------------------------------------------------------------------------

if __name__ == '__main__':
        

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
        description='get issues for a given project & branch',
        epilog='''
where SPEC is a comma delimited list of one or more of the following:
  projectId         project id
  branchId          branch id
  issue-key         issue key
  finding-key       finding key
  checker           checker aka subtool
  severity          severity
  type              issue type
  local_effect      local effect
  name              checker description
  description       description
  path              file path
  state             state (open/closed)
  status            triage status
  first_detected    date first detected on
  closed_date       date issue was closed
  age               days since issue first detected
  ttr               time to resolution in days
  url               URL to issue on Polaris
        ''')
    parser.add_argument('--debug', default=0, help='set debug level [0-9]')
    parser.add_argument('--url', default=os.getenv('POLARIS_SERVER_URL'), help='Polaris URL')
    parser.add_argument('--token', default=os.getenv('POLARIS_ACCESS_TOKEN'), help='Polaris Access Token')
    parser.add_argument('--project', required=True, help='project name')

    # branch name or run id
    #borr = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('--branch', default='master', help='branch name')
    parser.add_argument('--run', required=False, help='run id')

    parser.add_argument('--compare', help='comparison branch name for new or fixed')

    # issue filter options
    filter = parser.add_mutually_exclusive_group(required=False)
    filter.add_argument('--all', action='store_true', help='all issues in project')
    filter.add_argument('--opened', action='store_true', help='open issues (default)')
    filter.add_argument('--closed', action='store_true', help='closed / fixed issues')
    filter.add_argument('--untriaged', action='store_true', help='untriaged issues')
    filter.add_argument('--bugs', action='store_true', help='to-be-fixed issues')
    filter.add_argument('--dismissed', action='store_true', help='dismissed issues')
    filter.add_argument('--new', action='store_true', help='new issues relative to comparison branch')
    filter.add_argument('--fixed', action='store_true', help='fixed issues relative to comparison branch')
    filter.add_argument('--date', help='issues newer than date YYYY-MM-DDTHH:MM:SS')
    filter.add_argument('--age', help='issues older than AGE days')

    # issue path filter
    parser.add_argument('--path', help='limit issues to path')

    # issue kind filter
    kind = parser.add_mutually_exclusive_group(required=False)
    kind.add_argument('--quality', action='store_true', help='quality issues')
    kind.add_argument('--security', action='store_true', help='security issues')

    # severity filter
    parser.add_argument('--severity', help='comma delimited list of severities')

    # legacy filter
    legacy = parser.add_mutually_exclusive_group(required=False)
    legacy.add_argument('--legacy', action='store_true', help='legacy issues')
    legacy.add_argument('--nonlegacy', action='store_true', help='non-legacy issues')

    # output options
    parser.add_argument('--spec', default='name,description,b_name,url,issue-key,finding-key,severity,state,status,cwe,path,checker', help='report specification')
    parser.add_argument('--csv', action='store_true', help='output to CSV')
    parser.add_argument('--html', action='store_true', help='output to HTML')
    parser.add_argument('--email', help='comma delimited list of email addresses')
    parser.add_argument('--exit1-if-issues', action='store_true', help='exit with error code 1 if issues found')

    args = parser.parse_args()

    polaris.debug = debug = int(args.debug)
    reportSpec = args.spec.split(',')
    if debug: print(args)

    if ((args.url == None) or (args.token == None)):
        print('FATAL: POLARIS_SERVER_URL and POLARIS_ACCESS_TOKEN must be set via environment variables or the CLI')
        sys.exit(1)

    # convert token to JWT and create a requests session
    polaris.baseUrl, polaris.jwt, polaris.session = polaris.createSession(args.url, args.token)

    projectId, branchId = polaris.getProjectAndBranchId(args.project, args.branch)
    if args.run:
        branch_name = polaris.getbranchName(branchId)
    if debug: print("projectId = " + projectId)
    if debug: print("branchId = " + branchId)
    #if debug: print("branchName = " + branch_name)
    

    if any(column in args.spec for column in ['owner','status','comment','jira','closed_date']):
        getTriage = True
    else: getTriage = False

    if args.new or args.fixed: # run comparison use cmpIssuesForRuns
        runs = polaris.getRuns(projectId, branchId)
        #print(runs)
        currRunId = runs[0]['runId']
        if args.run is None and not (args.new or args.fixed):
            print("Current Run ID is\n",currRunId)
        if debug: print ('currRunId = ' + currRunId)
        if (args.compare == None):
            try: cmpRunId = runs[1]['runId']
            # if no previous run, compare with self
            except: cmpRunId = currRunId
        else:
            compareId = polaris.getBranchId(projectId, args.compare)
            if debug: print('compare = ' + args.compare + '\ncompareId = ' + compareId)
            runs = polaris.getRuns(projectId, compareId)
            cmpRunId = runs[0]['runId']
        if debug: print ('cmpRunId = ' + cmpRunId)
        filter = None
        if (args.quality or args.security):
            filter = addKindFilter()
        new_issues_df, fixed_issues_df = \
          polaris.cmpIssuesForRuns(projectId, currRunId, cmpRunId, getTriage, False, filter)
        if args.new: issues = new_issues_df
        if args.fixed: issues = fixed_issues_df

    else: # no comparison, set a filter and use getIssues
        if args.all:
            filter = None
        elif args.closed:
            filter=dict([('filter[issue][status][eq]', 'closed')])
        elif args.untriaged:
            filter=dict([('filter[issue][triage-status][eq]','not-triaged')])
        elif args.bugs:
            filter=dict([('filter[issue][triage-status][eq]','to-be-fixed')])
        elif args.dismissed:
            filter=dict([('filter[issue][triage-status][in]',
                '[dismiss-requested,dismissed-false-positive,dismissed-intentional,dismissed-other]')])
        elif args.date:
            filter=dict([('filter[issue][status-opened-date][gte]', str(args.date) + 'Z')])
        else: # args.opened
            filter=dict([('filter[issue][status][eq]', 'opened')])
        if (args.quality or args.security):
            filter.update(addKindFilter())
        if (args.path):
            pathFilter = dict([('path', json.dumps(args.path.split("/")))])
            filter.update(pathFilter)
        if debug: print(filter)
        #print(filter)
        if args.run:
            issues = polaris.getIssues(projectId, None, args.run, polaris.MAX_LIMIT, filter, getTriage,events=True)
        else:
            issues = polaris.getIssues(projectId, branchId, None, polaris.MAX_LIMIT, filter, getTriage,events=False)

    if (debug > 3): print(issues)

    # create a dataframe from issues dictionary
    df = pd.DataFrame(issues)
    
    # get issue count. exit if nothing returned
    count = len(df.index)
    if (count == 0):
        print ('noissues')
        sys.exit(0)
        
    if(args.run and not (args.new or args.fixed)):
        df['Vulnerability desc'] = df['mainevent_description']
        df['Support description'] = df['support_description']
        df['Evidence'] = df['mainevent_source']
    # calculate mean ttr if reporting on only closed / fixed issues
    if ("ttr" in args.spec) and (args.closed or args.fixed):
        df["ttr_tmp"] = pd.to_numeric(df["ttr"], errors='coerce')
        mtr = pd.to_timedelta(df["ttr_tmp"].mean())
        print("\nMean time to resolution: " + str(mtr) + "\n")

    # convert age and ttr to days
    if ("age" in args.spec): df['age'] = df['age'].dt.floor('d')
    if ("ttr" in args.spec): df['ttr'] = df['ttr'].dt.floor('d')

    # link path to url
    if args.email or args.html: df['path'] = '<a href=' + df['url'] + '>' + df['path'] + '</a>'

    # limit to issues older than age if requested
    if args.age: df = df[df.age.dt.days > int(args.age)]

    if args.severity: df = df.loc[df['severity'] == args.severity]

    # apply legacy filter
    if args.legacy: df = df.loc[df['cause'] == 'LEGACY']
    if args.nonlegacy: df = df.loc[df['cause'] != 'LEGACY']
    df['b_name'] = args.branch
    # select what we want from the dataframe
    df = df[reportSpec]
    df['app_name'] = sys.argv[6]
    df['App_branch'] =  sys.argv[6] + "-" + df['b_name']
    # display the report
    if args.csv: df.to_csv(sys.stdout)
    elif args.html: df.to_html(sys.stdout, escape=False)
    elif args.email: send_email(args.email)
    else: print(df)

    if args.exit1_if_issues: sys.exit(1)
    else: sys.exit(0)
