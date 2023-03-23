import json, requests, time, os, zipfile,base64
from conf.config import platform, apiToken, clientID
import logging

api_header = {
     "content-type": "application/json",
     "x-api-key": apiToken
    }
headers = {
     "content-type": "application/json",
     "x-api-key": apiToken    
    }

def get_id_for_path(data, path):
   #print(data['path'],path)
   if(data['path'] == path):
      return data['id']
   for child in data["children"]:
      
      if child["path"] == path:
         return child["id"]
      if child["hasChildren"]:
         result = get_id_for_path(child, path)
         if result is not None:
            return result
   return 

def add_url(Blackduck_project,scanner_plugin):
   url1 = "https://{}.risksense.com/api/v1/client/{}/tiny-url".format(platform,clientID)
   payload1 = json.dumps({"url":"https://{}.risksense.com/start/#/Manage/ApplicationFindings?activeViewId=-1&activeViewSettings=%7B%22activeGroupByKey%22%3Anull%2C%22density%22%3A%22standard%22%2C%22filterDrawerCollapsed%22%3Afalse%2C%22kpiCollapsed%22%3Afalse%2C%22pinnedColumns%22%3A%5B%5D%2C%22rowsPerPage%22%3A50%2C%22enabledColumns%22%3A%5B%7B%22key%22%3A%22KEY_RISK%22%2C%22width%22%3A150%2C%22sort%22%3A%7B%22index%22%3A1%2C%22direction%22%3A%22DESC%22%7D%7D%2C%7B%22key%22%3A%22KEY_STATUS%22%2C%22width%22%3A150%2C%22sort%22%3A%7B%22index%22%3A2%2C%22direction%22%3A%22DESC%22%7D%7D%2C%7B%22key%22%3A%22KEY_TITLE%22%2C%22width%22%3A250%2C%22sort%22%3A%7B%22index%22%3A3%2C%22direction%22%3A%22ASC%22%7D%7D%2C%7B%22key%22%3A%22KEY_INT_EXT_WEB_APP%22%2C%22width%22%3A250%2C%22sort%22%3Anull%7D%2C%7B%22key%22%3A%22KEY_URL%22%2C%22width%22%3A250%2C%22sort%22%3Anull%7D%2C%7B%22key%22%3A%22KEY_PLATFORM_LAST_FOUND_ON%22%2C%22width%22%3A200%2C%22sort%22%3Anull%7D%2C%7B%22key%22%3A%22KEY_SCANNER_LAST_DISCOVERED_ON%22%2C%22width%22%3A200%2C%22sort%22%3Anull%7D%5D%2C%22configuredKPIs%22%3A%5B%7B%22key%22%3A%224f50454e-5f46-494e-4449-4e4753000000%22%2C%22config%22%3A%5B%7B%22id%22%3A%22assetType%22%2C%22value%22%3A%22App%22%7D%5D%7D%2C%7B%22key%22%3A%224e45575f-4649-4e44-494e-470000000000%22%2C%22config%22%3A%5B%7B%22id%22%3A%22assetType%22%2C%22value%22%3A%22App%22%7D%2C%7B%22id%22%3A%22timeline%22%2C%22value%22%3A%22%3E30%22%7D%5D%7D%2C%7B%22key%22%3A%224f564552-4455-455f-4649-4e44494e4700%22%2C%22config%22%3A%5B%7B%22id%22%3A%22assetType%22%2C%22value%22%3A%22App%22%7D%2C%7B%22id%22%3A%22timeline%22%2C%22value%22%3A%22%3E30%22%7D%5D%7D%2C%7B%22key%22%3A%224f574153-505f-4649-4e44-494e47000000%22%2C%22config%22%3A%5B%7B%22id%22%3A%22assetType%22%2C%22value%22%3A%22App%22%7D%5D%7D%2C%7B%22key%22%3A%225553525f-4153-475f-4649-4e44494e4700%22%2C%22config%22%3A%5B%7B%22id%22%3A%22assetType%22%2C%22value%22%3A%22App%22%7D%5D%7D%5D%2C%22viewId%22%3A-1%7D&filter=%5B%7B%22field%22%3A%22found_by_id%22%2C%22exclusive%22%3Afalse%2C%22operator%22%3A%22IN%22%2C%22orWithPrevious%22%3Afalse%2C%22implicitFilters%22%3A%5B%5D%2C%22value%22%3A%22{}%22%7D%2C%7B%22field%22%3A%22riskType%22%2C%22exclusive%22%3Afalse%2C%22operator%22%3A%22IN%22%2C%22orWithPrevious%22%3Afalse%2C%22implicitFilters%22%3A%5B%5D%2C%22value%22%3A%22security%22%7D%2C%7B%22field%22%3A%22generic_state%22%2C%22exclusive%22%3Afalse%2C%22operator%22%3A%22EXACT%22%2C%22orWithPrevious%22%3Afalse%2C%22implicitFilters%22%3A%5B%5D%2C%22value%22%3A%22Open%22%7D%2C%7B%22field%22%3A%22webAppAdditionalDetails.project_name%22%2C%22exclusive%22%3Afalse%2C%22operator%22%3A%22IN%22%2C%22orWithPrevious%22%3Afalse%2C%22implicitFilters%22%3A%5B%5D%2C%22value%22%3A%22{}%22%7D%5D&page=1&size=50&sort=%5B%7B%22id%22%3A%22riskRating%22%2C%22dir%22%3A%22desc%22%7D%2C%7B%22id%22%3A%22workflow_status%22%2C%22dir%22%3A%22desc%22%7D%2C%7B%22id%22%3A%22title%22%2C%22dir%22%3A%22asc%22%7D%5D".format(platform,scanner_plugin,Blackduck_project)})

   response = requests.request("POST", url1, headers=headers, data=payload1)
   json_res = json.loads(response.text)
   return json_res["url"]


def ado_ai_fields(app,proj_id,config_dict):

   template_url = "https://{}/{}/_apis/wit/classificationNodes?%24depth=15".format(config_dict[app][1],config_dict[app][0])
   headers = {
   'Content-Type': 'application/json',
   }
   response = requests.request("GET", template_url, headers=headers,auth=(config_dict[app][3],config_dict[app][2]))
   
   json_response = json.loads(response.text)
   #print(json_response)

   a_value = json_response["value"][0]
   i_value = json_response["value"][1]

   area_name = config_dict[app][4]
   area_name = area_name.replace("/","\\Area\\",1)
   area_name = area_name.replace("/","\\")
   area_name = "\\" + area_name

   iter_name = config_dict[app][5]
   iter_name = iter_name.replace("/","\\Iteration\\",1)
   iter_name = iter_name.replace("/","\\")
   iter_name = "\\" + iter_name
  
   if("/" not in config_dict[app][4]):
      area_name = "\\" + config_dict[app][4] +  "\\" + "Area"
      #print(area_name) 

   if("/" not in config_dict[app][5]):
      iter_name = "\\" + config_dict[app][5]  +  "\\" + "Iteration"
   # print(area_name,iter_name)
   
   area_id = get_id_for_path(a_value,area_name)
   iter_id = get_id_for_path(i_value,iter_name)
   
   # print(area_id,iter_id)

   '''url = "https://{}/_apis/Settings/project/{}/Entries/me/ClassificationFieldsMru".format(config_dict[app][1],proj_id)

   response = requests.request("GET", url, headers=headers,auth=(config_dict[app][3],config_dict[app][2]))
   response_json = json.loads(response.text)

   print(response_json["value"]["AreaPath"],response_json["value"]["IterationPath"])'''

   return area_id,iter_id
   
def app_level_grouping(groupid,sev):
    url = "https://{}.risksense.com/api/v1/client/{}/applicationFinding/group-by".format(platform,clientID)
    app_name =[]
    print(type(sev))
    payload = json.dumps({"metricFields":["App Finding Apps Count","App Finding Open Count","App Finding Closed Count","App Finding VRR Critical Count","App Finding VRR High Count","App Finding VRR Medium Count","App Finding VRR Low Count","App Finding VRR Info Count"],"key":"project_name","filters":[{"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},{"field":"riskType","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":"security"},{"field":"group_ids","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":str(groupid)},{"field":"vrr_group","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":str(sev)}],"sortOrder":[{"field":"project_name","direction":"ASC"}]})

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text,response.status_code)
    jsonified_result = json.loads(response.text)

    for i in range (len(jsonified_result["data"])):
        app_name.append(jsonified_result["data"][i]["project_name"])

    #print(app_name)
    print("\n[+]  Total Applications Grouped by is {}".format(len(app_name)))
    logging.info("\n[+]  Total Applications Grouped by is {}".format(len(app_name)))
    return app_name


def groupby(appname,sev) :
    print("\n[+]  Application '{}' Scanner Plugins are grouped by...".format(appname))
    logging.info("\n[+]  Application '{}' Scanner Plugins are grouped by...".format(appname))
    grp_url = "https://{}.risksense.com/api/v1/client/{}/applicationFinding/group-by".format(platform,clientID)

    payload = json.dumps({
    "metricFields": [
        "App Finding Title",
        "App Finding Scanner Name",
        "App Finding Apps Count",
        "App Finding Open Count",
        "App Finding Closed Count",
        "App Finding VRR Critical Count",
        "App Finding VRR High Count",
        "App Finding VRR Medium Count",
        "App Finding VRR Low Count",
        "App Finding VRR Info Count"
    ],
    "key": "App Finding Scanner Plugin",
    "filters": [
        {
        "field": "webAppAdditionalDetails.project_name",
        "exclusive": False,
        "operator": "IN",
        "orWithPrevious": False,
        "implicitFilters": [],
        "value": appname
        },
        {"field":"vrr_group","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":sev},
        {
           "field":"riskType",
           "exclusive":False,
           "operator":"IN",
           "orWithPrevious":False,
           "implicitFilters":[],
           "value":"security"
           }
    ],
    "sortOrder": [
        {
        "field": "App Finding Scanner Plugin",
        "direction": "ASC"
        }
    ]
    })

    response = requests.request("POST", grp_url, headers=headers, data=payload)
    jsonified_result = json.loads(response.text)

    print("\n[+] There are {} scanner plugins for the '{}' application ".format(len(jsonified_result["data"]),appname))
    logging.info("\n[+] There are {} scanner plugins for the '{}' application ".format(len(jsonified_result["data"]),appname))

    return jsonified_result


def groupby_new(BD_prj,sev):
   grp_url = "https://{}.risksense.com/api/v1/client/{}/applicationFinding/group-by".format(platform,clientID)
   payload = json.dumps({
   "metricFields": [
   "App Finding Title",
   "App Finding Scanner Name",
   "App Finding Apps Count",
   "App Finding Open Count",
   "App Finding Closed Count",
   "App Finding VRR Critical Count",
   "App Finding VRR High Count",
   "App Finding VRR Medium Count",
   "App Finding VRR Low Count",
   "App Finding VRR Info Count"
   ],
   "key": "App Finding Scanner Plugin",
   "filters": [
   {
   "field": "webAppAdditionalDetails.project_name",
   "exclusive": False,
   "operator": "IN",
   "orWithPrevious": False,
   "implicitFilters": [],
   "value": BD_prj
   },
   {"field":"generic_state","exclusive":False,"operator":"EXACT","orWithPrevious":False,"implicitFilters":[],"value":"Open"},
   {
      "field":"riskType",
      "exclusive":False,
      "operator":"IN",
      "orWithPrevious":False,
      "implicitFilters":[],
      "value":"security"
      },
   {"field":"vrr_group","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":sev}
   ],
   "sortOrder": [
   {
   "field": "App Finding Scanner Plugin",
   "direction": "ASC"
   }
   ]
   })

   response = requests.request("POST", grp_url, headers=headers, data=payload)
   jsonified_result = json.loads(response.text)
   return jsonified_result

def ado_template(config_dict,app):

   template_url = "https://{}/_apis/Contribution/dataProviders/query?api-version=7.0-preview".format(config_dict[app][1])
   #print(template_url)
   payload = json.dumps({
   "contributionIds": [
      "ms.vss-work-web.work-item-types-data-provider"
   ],
   "context": {
      "properties": {
         "projectId": get_proj_id(config_dict,app),
         "typeNames": [
         "Security Vulnerability"
         ],
         "pageSource": {
         "contributionPaths": [
            "VSS",
            "VSS/Resources",
            "q",
            "knockout",
            "mousetrap",
            "mustache",
            "react",
            "react-dom",
            "react-transition-group",
            "jQueryUI",
            "jquery",
            "OfficeFabric",
            "tslib",
            "@uifabric",
            "VSSUI",
            "TFSUI",
            "TFSUI/Resources",
            "Charts",
            "Charts/Resources",
            "ContentRendering",
            "ContentRendering/Resources",
            "WidgetComponents",
            "WidgetComponents/Resources",
            "TFS",
            "Notifications",
            "Presentation/Scripts/marked",
            "Presentation/Scripts/URI",
            "Presentation/Scripts/punycode",
            "Presentation/Scripts/IPv6",
            "Presentation/Scripts/SecondLevelDomains",
            "highcharts",
            "highcharts/highcharts-more",
            "highcharts/modules/accessibility",
            "highcharts/modules/heatmap",
            "highcharts/modules/funnel",
            "Analytics"
         ],
         "diagnostics": {
            "sessionId": "dd9322d0-b7f9-46d6-8997-78b99e8da672",
            "activityId": "dd9322d0-b7f9-46d6-8997-78b99e8da672",
            "bundlingEnabled": True,
            "cdnAvailable": True,
            "cdnEnabled": True,
            "webPlatformVersion": "M213",
            "serviceVersion": "Dev19.M213.1 (build: AzureDevOps_M213_20221207.1)"
         },
         "navigation": {
            "topMostLevel": 8,
            "area": "",
            "currentController": "Apps",
            "currentAction": "ContributedHub",
            "currentParameters": "Security Vulnerability",
            "commandName": "ms.vss-work-web.work-items-create-route",
            "routeId": "ms.vss-work-web.work-items-create-route",
            "routeTemplates": [
               "{project}/{team}/_workitems/create/{*parameters}",
               "{project}/_workitems/create/{*parameters}"
            ],
            "routeValues": {
               "project": config_dict[app][0],
               "parameters": "Security Vulnerability",
               "controller": "Apps",
               "action": "ContributedHub",
               "viewname": "work-items-create-view"
            }
         },
         "project": {
            "id": get_proj_id(config_dict,app),
            "name": config_dict[app][0]
         },
         "selectedHubGroupId": "ms.vss-work-web.work-hub-group",
         "selectedHubId": "ms.vss-work-web.new-work-items-hub",
         "url": "https://{}/{}/_workitems/create/Security%20Vulnerability".format(config_dict[app][1],config_dict[app][0])
         },
         "sourcePage": {
         "url": "https://{}/{}/_workitems/create/Security%20Vulnerability".format(config_dict[app][1],config_dict[app][0]),
         "routeId": "ms.vss-work-web.work-items-create-route",
         "routeValues": {
            "project": config_dict[app][0],
            "parameters": "Security Vulnerability",
            "controller": "Apps",
            "action": "ContributedHub",
            "viewname": "work-items-create-view"
         }
         }
      }
   }
   })

   headers = {
   'Content-Type': 'application/json',
   }

   response = requests.request("POST", template_url, headers=headers,auth=(config_dict[app][3],config_dict[app][2]), data=payload)
   #print(response.status_code,response.text)
   json_template = json.loads(response.text)
   return json_template
   
def get_proj_id(config_dict,app):
   headers = {
   'Content-Type': 'application/json',
   }
   
 # Fetching project id
   project_url = "https://{}/_apis/projects?api-version=7.0".format(config_dict[app][1])
   #print(project_url)
   response = requests.request("GET", project_url, auth=(config_dict[app][3], config_dict[app][2]), headers=headers)
   #print(response.status_code)
   response_json = json.loads(response.text)
   #print(response.status_code, response_json["value"][0]["id"],response_json["value"])
   if(response.status_code == 200):
      for i in range(len(response_json["value"])):
            #print(response_json["value"][i]["name"],config_dict[app][1])
            if(response_json["value"][i]["name"] == config_dict[app][0]):
               proj_id = response_json["value"][i]["id"]
               break
            continue

   else:
      print("\nPlease check if you have provide proper values in config.xlsx...")
      logging.info("\nPlease check if you have provide proper values in config.xlsx...")

   return proj_id

def ado_app_ticket_creation(config_dict,uniqueVulnerability,app,Title,Priority_group,Scanner_Name,CVSS3score,CVSS3vector,CWE,VRR,Scanner_Name_org,Description,Location,SolutionString,PatchString,OWASP,RAS,CVSS_sev,appname,Source_link,rs_url,ex_date,cves):
   
   url = "https://{}/_apis/Contribution/dataProviders/query?api-version=4.1-preview.1".format(config_dict[app][1])
   #print(url)
   #ADO_url = "https://ivanti.visualstudio.com/DevOps/_workitems/Security%20Vulnerability?api-version=7.1-preview.3"
   headers = {
   'Content-Type': 'application/json',
   }   
   # print(Location)
   #print(uniqueVulnerability,Description,Location,PatchString,SolutionString,CWE,Scanner_Name_org,OWASP)
   Description_json = "<p><strong>Vulnerability</strong></p><p>"+str(uniqueVulnerability)+"</p><p><strong>Description</strong></p><p>"+str(Description)+"</p><p><strong>Scanner Name</strong></p><p>"+str(Scanner_Name_org)+"</p><p><strong>Location</strong></p><p>"+str(Location)+"</p><p><strong>Applications Affected</strong></p>"+str(appname)+"</p><p><strong>Risksense Redirect</strong></p>"+str(rs_url + " - This link will expire on "+ex_date)+"</p><p><strong>CWE IDs</strong></p>"+str(CWE)+"</p><p><strong>OWASP Category</strong></p>"+str(OWASP)+"</p><p><strong>Possible Solution</strong></p><p>"+str(SolutionString)+"</p><p><strong>Possible Patch</strong></p><p>"+str(PatchString)+"</p><br>"


   #print(proj_id)
   #print(df_instance["Instance"][app],df_project["Project"][app])

   proj_id = get_proj_id(config_dict,app)
   area,iteration = ado_ai_fields(app,proj_id, config_dict)

   if(not (area and iteration)):
      print("\nPlease Check if the provided area/iteration is right in the Config.xlsx file\n")
      logging.error("\nPlease Check if the provided area/iteration is right in the Config.xlsx file\n")
      

   #print(Scanner_Name,Scanner_output,CVSS3vector,CVSS3score,CVSS_sev,VRR,CWE,Title,Priority_group,area,iteration)
   payload = json.dumps({
   "contributionIds": [
         "ms.vss-work-web.update-work-items-data-provider"
   ],
   "context": {
         "properties": {
         "updatePackage": "[{\"id\":0,\"rev\":0,\"projectId\":\""+str(proj_id)+"\",\"isDirty\":true,\"tempId\":-2,\"fields\":{\"1\":\""+str(Title)+"\",\"2\":\"New\",\"22\":\"Moved to state New\",\"25\":\"Security Vulnerability\",\"52\":\""+str(Description_json)+"\",\"537277\":{\"type\":1},\"537285\":\""+str(Priority_group)+"\",\"537327\":\"\",\"10562881\":\"Process documentation and help with this form <a href=\\\"https://landeskinc.sharepoint.com/:w:/s/globaldevops/EbFo_vCYJ9xGklo0kd4tg5YBn8e-hPmLXctTN3m-lLJblg?e=RDGJga\\\">Ivanti Sharepoint</a>\",\"10562883\":\"Uknown\",\"10562884\":\""+str(Scanner_Name)+"\",\"10562885\":\""+str(Source_link)+"\",\"10562886\":\""+str(RAS)+"\",\"10562887\":\""+str(CVSS_sev)+"\",\"10562888\":\""+str(CVSS3score)+"\",\"10562889\":\""+str(CVSS3vector)+"\",\"10562890\":\""+str(cves)+"\",\"10562891\":\""+str(CWE)+"\",\"10562892\":\""+str(VRR)+"\",\"10563660\":\"Risksense-sync\",\"-2\":\""+str(area)+"\",\"-104\":\""+str(iteration)+"\"}}]",
         # "updatePackage": "[{\"id\":0,\"rev\":0,\"projectId\":\""+str(proj_id)+"\",\"isDirty\":true,\"tempId\":-2,\"fields\":{\"1\":\""+str(Title)+"\",\"2\":\"New\",\"22\":\"Moved to state New\",\"25\":\"Security Vulnerability\",\"52\":\""+str(Description_json)+"\",\"537277\":{\"type\":1},\"537285\":\""+str(Priority_group)+"\",\"537327\":\"\",\"10562881\":\"Process documentation and help with this form <a href=\\\"https://landeskinc.sharepoint.com/:w:/s/globaldevops/EbFo_vCYJ9xGklo0kd4tg5YBn8e-hPmLXctTN3m-lLJblg?e=RDGJga\\\">Ivanti Sharepoint</a>\",\"10562883\":\"Uknown\",\"10562884\":\""+str(Scanner_Name)+"\",\"10562885\":\""+str(Source_link)+"\",\"10562886\":\""+str(RAS)+"\",\"10562887\":\""+str(CVSS_sev)+"\",\"10562888\":\""+str(CVSS3score)+"\",\"10562889\":\""+str(CVSS3vector)+"\",\"10562890\":\"\",\"10562891\":\""+str(CWE)+"\",\"10562892\":\""+str(VRR)+"\",\"10563660\":\""+str(rs_url + " - This link will expire on "+ex_date)+"\",\"-2\":\""+str(area)+"\",\"-104\":\""+str(iteration)+"\"}}]",
         "pageSource": {
            "contributionPaths": [
            "VSS",
            "VSS/Resources",
            "q",
            "knockout",
            "mousetrap",
            "mustache",
            "react",
            "react-dom",
            "react-transition-group",
            "jQueryUI",
            "jquery",
            "OfficeFabric",
            "tslib",
            "@uifabric",
            "VSSUI",
            "TFSUI",
            "TFSUI/Resources",
            "Charts",
            "Charts/Resources",
            "ContentRendering",
            "ContentRendering/Resources",
            "WidgetComponents",
            "WidgetComponents/Resources",
            "TFS",
            "Notifications",
            "Presentation/Scripts/marked",
            "Presentation/Scripts/URI",
            "Presentation/Scripts/punycode",
            "Presentation/Scripts/IPv6",
            "Presentation/Scripts/SecondLevelDomains",
            "highcharts",
            "highcharts/highcharts-more",
            "highcharts/modules/accessibility",
            "highcharts/modules/heatmap",
            "highcharts/modules/funnel",
            "Analytics"
            ],
            "diagnostics": {
            "sessionId": "fc7e629e-97dc-4aaf-81cb-610cdv6a2ffa",
            "activityId": "fc7e629e-97dc-4aaf-81cb-610cdv6a2ffa",
            "bundlingEnabled": True,
            "cdnAvailable": True,
            "cdnEnabled": True,
            "webPlatformVersion": "M212",
            "serviceVersion": "Dev19.M212.1 (build: AzureDevOps_M212_20221130.1)"
            },
            "navigation": {
            "topMostLevel": 8,
            "area": "",
            "currentController": "Apps",
            "currentAction": "ContributedHub",
            "currentParameters": "Security Vulnerability",
            "commandName": "ms.vss-work-web.work-items-create-route",
            "routeId": "ms.vss-work-web.work-items-create-route",
            "routeTemplates": [
               "{project}/{team}/_workitems/create/{*parameters}",
               "{project}/_workitems/create/{*parameters}"
            ],
            "routeValues": {
               "project": config_dict[app][0],
               "parameters": "Security Vulnerability",
               "controller": "Apps",
               "action": "ContributedHub",
               "viewname": "work-items-create-view"
            }
            },
            "project": {
            "id": str(proj_id),
            "name": config_dict[app][0]
            },
            "selectedHubGroupId": "ms.vss-work-web.work-hub-group",
            "selectedHubId": "ms.vss-work-web.new-work-items-hub",
            "url": "https://{}/{}/_workitems/create/Security%20Vulnerability".format(config_dict[app][1],config_dict[app][0])
         },
         "sourcePage": {
            "url": "https://{}/{}/_workitems/create/Security%20Vulnerability".format(config_dict[app][1],config_dict[app][0]),
            "routeId": "ms.vss-work-web.work-items-create-route",
            "routeValues": {
            "project": config_dict[app][0],
            "parameters": "Security Vulnerability",
            "controller": "Apps",
            "action": "ContributedHub",
            "viewname": "work-items-create-view"
            }
         }
         }
   }
   })
   response = requests.request("POST", url, auth=(config_dict[app][3], config_dict[app][2]), headers=headers,data=payload)
   #print(response.text)
   return response

def attach_findings(config_dict,WorkitemID,app):
   org_url = config_dict[app][1]
   pat = config_dict[app][2]
   # print(config_dict)
   # hi = config_dict[app][0]
   # print(hi)
   # Azure DevOps project name and work item ID
   project = config_dict[app][0]
   work_item_id = WorkitemID

   # URL to upload attachment to work item
   url = f"{org_url}/{project}/_apis/wit/attachments?fileName=example.csv&api-version=6.0"

   # Read CSV file as bytes
   with open("Findings\Findings.csv", "rb") as file:
      file_bytes = file.read()

   # Set request headers and data
   headers = {
      "Content-Type": "application/octet-stream",
      'Authorization': f'Basic {base64.b64encode(bytes(f":{pat}", encoding="ascii")).decode("ascii")}',

   }
   data = file_bytes
   # Make request to upload attachment
   response = requests.post(url, headers=headers, data=data)
   # print(response.status_code)
   # Get attachment ID from response
   attachment_id = response.json()["id"]

   # URL to add attachment to work item
   url = f"{org_url}/{project}/_apis/wit/workitems/{work_item_id}?fileName=Findings.csv&api-version=6.0"

   # Set request headers and data
   headers = {
      "Content-Type": "application/json-patch+json",
      'Authorization': f'Basic {base64.b64encode(bytes(f":{pat}", encoding="ascii")).decode("ascii")}',
         "Slug": "example.csv"  # specify file name here
   }
   data = [
      {
         "op": "add",
         "path": "/relations/-",
         "value": {
               "rel": "AttachedFile",
               "url": f"{org_url}/_apis/wit/attachments/{attachment_id}"
         }
      }
   ]

   # Make request to add attachment to work item
   response = requests.patch(url, headers=headers, json=data)
   print (response.status_code)
   # Check response status code
   if response.status_code == 200:
      print("CSV file uploaded and attached to work item successfully!")
   else:
      print("Error: CSV file upload and attachment failed.")


def ado_host_ticket_creation(config_dict,uniqueVulnerability,app,Title,Priority_group,Scanner_Name,CVSS3score,CVSS3vector,VRR,SolutionString,PatchString,RAS,CVSS_sev):

   url = "https://{}/_apis/Contribution/dataProviders/query?api-version=4.1-preview.1".format(config_dict[app][1])
   #print(url)
   #ADO_url = "https://ivanti.visualstudio.com/DevOps/_workitems/Security%20Vulnerability?api-version=7.1-preview.3"
   Description_json = "<p><strong>Vulnerability</strong></p><p>"+str(uniqueVulnerability)+"</p><p><strong>Scanner Name</strong></p><p>"+str(Scanner_Name)+"</p><p><strong>Possible Solution</strong></p><p>"+str(SolutionString)+"</p><p><strong>Possible Patch</strong></p><p>"+str(PatchString)+"</p><br>"

   proj_id = get_proj_id(config_dict,app)
   area,iteration = ado_ai_fields(app,proj_id,config_dict)
   #print(area,iteration)
   #print(Scanner_Name,Scanner_output,CVSS3vector,CVSS3score,CVSS_sev,VRR,CWE,Title,Priority_group,area,iteration)
   payload = json.dumps({
   "contributionIds": [
         "ms.vss-work-web.update-work-items-data-provider"
   ],
   "context": {
         "properties": {
         "updatePackage": "[{\"id\":0,\"rev\":0,\"projectId\":\""+str(proj_id)+"\",\"isDirty\":true,\"tempId\":-2,\"fields\":{\"1\":\""+str(Title)+"\",\"2\":\"New\",\"22\":\"Moved to state New\",\"25\":\"Security Vulnerability\",\"52\":\""+str(Description_json)+"\",\"537277\":{\"type\":1},\"537285\":\""+str(Priority_group)+"\",\"537327\":\"\",\"10562881\":\"Process documentation and help with this form <a href=\\\"https://landeskinc.sharepoint.com/:w:/s/globaldevops/EbFo_vCYJ9xGklo0kd4tg5YBn8e-hPmLXctTN3m-lLJblg?e=RDGJga\\\">Ivanti Sharepoint</a>\",\"10562883\":\"Uknown\",\"10562884\":\""+str(Scanner_Name)+"\",\"10562885\":\"\",\"10562886\":\""+str(RAS)+"\",\"10562887\":\""+str(CVSS_sev)+"\",\"10562888\":\""+str(CVSS3score)+"\",\"10562889\":\""+str(CVSS3vector)+"\",\"10562890\":\"\",\"10562891\":\"\",\"10562892\":\""+str(VRR)+"\",\"10563660\":\"Risksense-sync\",\"-2\":\""+str(area)+"\",\"-104\":\""+str(iteration)+"\"}}]",
         "pageSource": {
            "contributionPaths": [
            "VSS",
            "VSS/Resources",
            "q",
            "knockout",
            "mousetrap",
            "mustache",
            "react",
            "react-dom",
            "react-transition-group",
            "jQueryUI",
            "jquery",
            "OfficeFabric",
            "tslib",
            "@uifabric",
            "VSSUI",
            "TFSUI",
            "TFSUI/Resources",
            "Charts",
            "Charts/Resources",
            "ContentRendering",
            "ContentRendering/Resources",
            "WidgetComponents",
            "WidgetComponents/Resources",
            "TFS",
            "Notifications",
            "Presentation/Scripts/marked",
            "Presentation/Scripts/URI",
            "Presentation/Scripts/punycode",
            "Presentation/Scripts/IPv6",
            "Presentation/Scripts/SecondLevelDomains",
            "highcharts",
            "highcharts/highcharts-more",
            "highcharts/modules/accessibility",
            "highcharts/modules/heatmap",
            "highcharts/modules/funnel",
            "Analytics"
            ],
            "diagnostics": {
            "sessionId": "fc7e629e-97dc-4aaf-81cb-610cdv6a2ffa",
            "activityId": "fc7e629e-97dc-4aaf-81cb-610cdv6a2ffa",
            "bundlingEnabled": True,
            "cdnAvailable": True,
            "cdnEnabled": True,
            "webPlatformVersion": "M212",
            "serviceVersion": "Dev19.M212.1 (build: AzureDevOps_M212_20221130.1)"
            },
            "navigation": {
            "topMostLevel": 8,
            "area": "",
            "currentController": "Apps",
            "currentAction": "ContributedHub",
            "currentParameters": "Security Vulnerability",
            "commandName": "ms.vss-work-web.work-items-create-route",
            "routeId": "ms.vss-work-web.work-items-create-route",
            "routeTemplates": [
               "{project}/{team}/_workitems/create/{*parameters}",
               "{project}/_workitems/create/{*parameters}"
            ],
            "routeValues": {
               "project": config_dict[app][0],
               "parameters": "Security Vulnerability",
               "controller": "Apps",
               "action": "ContributedHub",
               "viewname": "work-items-create-view"
            }
            },
            "project": {
            "id": str(proj_id),
            "name": config_dict[app][0]
            },
            "selectedHubGroupId": "ms.vss-work-web.work-hub-group",
            "selectedHubId": "ms.vss-work-web.new-work-items-hub",
            "url": "https://{}/{}/_workitems/create/Security%20Vulnerability".format(config_dict[app][1],config_dict[app][0])
         },
         "sourcePage": {
            "url": "https://{}/{}/_workitems/create/Security%20Vulnerability".format(config_dict[app][1],config_dict[app][0]),
            "routeId": "ms.vss-work-web.work-items-create-route",
            "routeValues": {
            "project": config_dict[app][0],
            "parameters": "Security Vulnerability",
            "controller": "Apps",
            "action": "ContributedHub",
            "viewname": "work-items-create-view"
            }
         }
         }
   }
   })
   headers = {
   'Content-Type': 'application/json',
   }

   response = requests.request("POST", url, auth=(config_dict[app][3], config_dict[app][2]), headers=headers,data=payload)
   #print(response.text)
   return response,proj_id

def export(scanner_plugin,name,sev):
    ex_url = "https://{}.risksense.com/api/v1/client/{}/applicationFinding/export".format(platform,clientID)

    payload = json.dumps({
    "fileName": "export",
    "fileType": "CSV",
    "noOfRows": "5000",
    "filterRequest": {
        "filters": [
        {
            "field": "webAppAdditionalDetails.project_name",
            "exclusive": False,
            "operator": "IN",
            "orWithPrevious": False,
            "implicitFilters": [],
            "value": str(name)
        },
        {"field":"vrr_group","exclusive":False,"operator":"IN","orWithPrevious":False,"implicitFilters":[],"value":sev},
        {
            "field": "generic_state",
            "exclusive": False,
            "operator": "EXACT",
            "orWithPrevious": False,
            "implicitFilters": [],
            "value": "Open"
        },
        {
            "field": "found_by_id",
            "exclusive": False,
            "operator": "EXACT",
            "orWithPrevious": False,
            "implicitFilters": [],
            "value": str(scanner_plugin)
        },
        {
        "field":"HAS_CONNECTOR_TICKET",
        "exclusive":False,
        "operator":"EXACT",
        "value": "False"
        }
    #    {"field":"generic_state","exclusive":false,"operator":"EXACT","value":"Open"},,{"field":"webAppAdditionalDetails.project_name","exclusive":false,"operator":"IN","value":"Patch Cloud Device Patching"}],"filter":{"field":"found_by_id","exclusive":false,"operator":"IN","value":"","implicitFilters":[]}}
        
        ]
    },
    "exportableFields": [
        {
        "heading": "asset_options",
        "fields": [
            {
            "identifierField": "location",
            "displayText": "Address",
            "sortable": False,
            "fieldOrder": 1,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "addressType",
            "displayText": "Address Type",
            "sortable": False,
            "fieldOrder": 2,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "name",
            "displayText": "Application Name",
            "sortable": False,
            "fieldOrder": 3,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "assetCriticality",
            "displayText": "Asset Criticality",
            "sortable": False,
            "fieldOrder": 4,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "asset_owner",
            "displayText": "Asset Owner",
            "sortable": False,
            "fieldOrder": 5,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "owner",
            "displayText": "CHECKMARXSAST Scan Owner",
            "sortable": False,
            "fieldOrder": 6,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "critical",
            "displayText": "Critical",
            "sortable": False,
            "fieldOrder": 7,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "exploit",
            "displayText": "Exploit",
            "sortable": False,
            "fieldOrder": 8,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "assetIdentifiedBy",
            "displayText": "First Asset Identified By",
            "sortable": False,
            "fieldOrder": 9,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "assetIdentifier",
            "displayText": "First Asset Identifier",
            "sortable": False,
            "fieldOrder": 10,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "scannerFirstDiscoveredOn",
            "displayText": "First Discovered On",
            "sortable": False,
            "fieldOrder": 11,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "platformFirstIngestedOn",
            "displayText": "First Ingested On",
            "sortable": False,
            "fieldOrder": 12,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "groupIds",
            "displayText": "Group Ids",
            "sortable": False,
            "fieldOrder": 13,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "groupNames",
            "displayText": "Group Names",
            "sortable": False,
            "fieldOrder": 14,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "high",
            "displayText": "High",
            "sortable": False,
            "fieldOrder": 15,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "id",
            "displayText": "Id",
            "sortable": False,
            "fieldOrder": 16,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "info",
            "displayText": "Info",
            "sortable": False,
            "fieldOrder": 17,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "lastAssetIdentifiedBy",
            "displayText": "Last Asset Identified By",
            "sortable": False,
            "fieldOrder": 18,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "lastAssetIdentifier",
            "displayText": "Last Asset Identifier",
            "sortable": False,
            "fieldOrder": 19,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "scannerLastDiscoveredOn",
            "displayText": "Last Discovered On",
            "sortable": False,
            "fieldOrder": 20,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "lastFoundOn",
            "displayText": "Last Found On",
            "sortable": False,
            "fieldOrder": 21,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "platformLastIngestedOn",
            "displayText": "Last Ingested On",
            "sortable": False,
            "fieldOrder": 22,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "locationCount",
            "displayText": "Location Count",
            "sortable": False,
            "fieldOrder": 23,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "low",
            "displayText": "Low",
            "sortable": False,
            "fieldOrder": 24,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "medium",
            "displayText": "Medium",
            "sortable": False,
            "fieldOrder": 25,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "metricsOverrideDate",
            "displayText": "Metric Exclude Override Date",
            "sortable": False,
            "fieldOrder": 26,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "metricsOverrideType",
            "displayText": "Metric Exclude Override Status",
            "sortable": False,
            "fieldOrder": 27,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "metricsOverrideUser",
            "displayText": "Metric Exclude Override User",
            "sortable": False,
            "fieldOrder": 28,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "network",
            "displayText": "Network",
            "sortable": False,
            "fieldOrder": 29,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "networkType",
            "displayText": "Network Type",
            "sortable": False,
            "fieldOrder": 30,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "app_name",
            "displayText": "Nexus Lifecycle Application Name",
            "sortable": False,
            "fieldOrder": 31,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "org_name",
            "displayText": "Nexus Lifecycle Organization",
            "sortable": False,
            "fieldOrder": 32,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "stage_name",
            "displayText": "Nexus Lifecycle Stage",
            "sortable": False,
            "fieldOrder": 33,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "osName",
            "displayText": "OS Name",
            "sortable": False,
            "fieldOrder": 34,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "pii",
            "displayText": "PII",
            "sortable": False,
            "fieldOrder": 35,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "account_id",
            "displayText": "Prisma Cloud Compute Account ID",
            "sortable": False,
            "fieldOrder": 36,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "collections",
            "displayText": "Prisma Cloud Compute Collections",
            "sortable": False,
            "fieldOrder": 37,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "cluster",
            "displayText": "Prisma Cloud Compute Container Cluster",
            "sortable": False,
            "fieldOrder": 38,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "container_labels_wildcard",
            "displayText": "Prisma Cloud Compute Container Labels",
            "sortable": False,
            "fieldOrder": 39,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "namespace",
            "displayText": "Prisma Cloud Compute Container Namespace",
            "sortable": False,
            "fieldOrder": 40,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "clusters",
            "displayText": "Prisma Cloud Compute Image Clusters",
            "sortable": False,
            "fieldOrder": 41,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "labels_wildcard",
            "displayText": "Prisma Cloud Compute Image Labels",
            "sortable": False,
            "fieldOrder": 42,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "namespaces",
            "displayText": "Prisma Cloud Compute Image Namespaces",
            "sortable": False,
            "fieldOrder": 43,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "rs3",
            "displayText": "RS3",
            "sortable": False,
            "fieldOrder": 44,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "sla_rule_name",
            "displayText": "SLA Name",
            "sortable": False,
            "fieldOrder": 45,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "AssetTagIds",
            "displayText": "Tag Ids",
            "sortable": False,
            "fieldOrder": 46,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "tags",
            "displayText": "Tags",
            "sortable": False,
            "fieldOrder": 47,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "ticketsId",
            "displayText": "Tickets Id",
            "sortable": False,
            "fieldOrder": 48,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "ticketsLink",
            "displayText": "Tickets Link",
            "sortable": False,
            "fieldOrder": 49,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "ticketsStatus",
            "displayText": "Tickets Status",
            "sortable": False,
            "fieldOrder": 50,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "vrrCritical",
            "displayText": "VRR Critical",
            "sortable": False,
            "fieldOrder": 51,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "vrrHigh",
            "displayText": "VRR High",
            "sortable": False,
            "fieldOrder": 52,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "vrrInfo",
            "displayText": "VRR Info",
            "sortable": False,
            "fieldOrder": 53,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "vrrLow",
            "displayText": "VRR Low",
            "sortable": False,
            "fieldOrder": 54,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "vrrMedium",
            "displayText": "VRR Medium",
            "sortable": False,
            "fieldOrder": 55,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            }
        ]
        },
        {
        "heading": "finding_options",
        "fields": [
            {
            "identifierField": "addressType",
            "displayText": "Address Type",
            "sortable": False,
            "fieldOrder": 1,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "appId",
            "displayText": "App Id",
            "sortable": False,
            "fieldOrder": 2,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "name",
            "displayText": "App Name",
            "sortable": False,
            "fieldOrder": 3,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "applicationAddress",
            "displayText": "Application Address",
            "sortable": False,
            "fieldOrder": 4,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "assetCriticality",
            "displayText": "Asset Criticality",
            "sortable": False,
            "fieldOrder": 5,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "asset_owner",
            "displayText": "Asset Owner",
            "sortable": False,
            "fieldOrder": 6,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "assignedTo",
            "displayText": "Assigned To",
            "sortable": False,
            "fieldOrder": 7,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "burpsuite_deeplink",
            "displayText": "BurpSuite Enterprise Deep Link",
            "sortable": False,
            "fieldOrder": 8,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
               "displayText" : "CVEs Associated",
               "fieldOrder": 11,
               "identifierField" : "cves",
               "selected" : True,
               "sortOrder": 0,
               "sortType": "ASC",
               "sortable": False
            },
            {
            "identifierField": "cvss2Score",
            "displayText": "CVSS 2.0",
            "sortable": False,
            "fieldOrder": 9,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "cvss2Vector",
            "displayText": "CVSS 2.0 Vector",
            "sortable": False,
            "fieldOrder": 10,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "cvss3Score",
            "displayText": "CVSS 3.0",
            "sortable": False,
            "fieldOrder": 11,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "cvss3Vector",
            "displayText": "CVSS 3.0 Vector",
            "sortable": False,
            "fieldOrder": 12,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "cweIds",
            "displayText": "CWE ID",
            "sortable": False,
            "fieldOrder": 13,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "description",
            "displayText": "Description",
            "sortable": False,
            "fieldOrder": 14,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "dueDate",
            "displayText": "Due Date",
            "sortable": False,
            "fieldOrder": 15,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "due_date_updated_date",
            "displayText": "Due Date Updated On",
            "sortable": False,
            "fieldOrder": 16,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "expireDate",
            "displayText": "Expire Date",
            "sortable": False,
            "fieldOrder": 17,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "exploits",
            "displayText": "Exploits",
            "sortable": False,
            "fieldOrder": 18,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "assetIdentifiedBy",
            "displayText": "First Asset Identified By",
            "sortable": False,
            "fieldOrder": 19,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "assetIdentifier",
            "displayText": "First Asset Identifier",
            "sortable": False,
            "fieldOrder": 20,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "firstAssignedOn",
            "displayText": "First Assigned On Date",
            "sortable": False,
            "fieldOrder": 21,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "scannerFirstDiscoveredOn",
            "displayText": "First Discovered On",
            "sortable": False,
            "fieldOrder": 22,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "platformFirstIngestedOn",
            "displayText": "First Ingested On",
            "sortable": False,
            "fieldOrder": 23,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "vulnerability_id",
            "displayText": "FortifyonDemand Vuln Id",
            "sortable": False,
            "fieldOrder": 24,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "groupIds",
            "displayText": "Group Ids",
            "sortable": False,
            "fieldOrder": 25,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "groupNames",
            "displayText": "Group Names",
            "sortable": False,
            "fieldOrder": 26,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "id",
            "displayText": "Id",
            "sortable": False,
            "fieldOrder": 27,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "lastAssetIdentifiedBy",
            "displayText": "Last Asset Identified By",
            "sortable": False,
            "fieldOrder": 28,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "lastAssetIdentifier",
            "displayText": "Last Asset Identifier",
            "sortable": False,
            "fieldOrder": 29,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "scannerLastDiscoveredOn",
            "displayText": "Last Discovered On",
            "sortable": False,
            "fieldOrder": 30,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "lastFoundOn",
            "displayText": "Last Found On",
            "sortable": False,
            "fieldOrder": 31,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "platformLastIngestedOn",
            "displayText": "Last Ingested On",
            "sortable": False,
            "fieldOrder": 32,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "location",
            "displayText": "Location",
            "sortable": False,
            "fieldOrder": 33,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "network",
            "displayText": "Network",
            "sortable": False,
            "fieldOrder": 34,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "networkType",
            "displayText": "Network Type",
            "sortable": False,
            "fieldOrder": 35,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "app_name",
            "displayText": "Nexus Lifecycle Application Name",
            "sortable": False,
            "fieldOrder": 36,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "sonatype_cvss_v2_score",
            "displayText": "Nexus Lifecycle CVSS V2 Score",
            "sortable": False,
            "fieldOrder": 37,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "sonatype_cvss_v3_score",
            "displayText": "Nexus Lifecycle CVSS V3 Score",
            "sortable": False,
            "fieldOrder": 38,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "finding_deeplink",
            "displayText": "Nexus Lifecycle Deep Link",
            "sortable": False,
            "fieldOrder": 39,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "effective_licenses",
            "displayText": "Nexus Lifecycle Effective Licenses",
            "sortable": False,
            "fieldOrder": 40,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "org_name",
            "displayText": "Nexus Lifecycle Organization",
            "sortable": False,
            "fieldOrder": 41,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "policy_name",
            "displayText": "Nexus Lifecycle Policy Name",
            "sortable": False,
            "fieldOrder": 42,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "policy_violation_id",
            "displayText": "Nexus Lifecycle Policy Violation Id",
            "sortable": False,
            "fieldOrder": 43,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "sonatype_score",
            "displayText": "Nexus Lifecycle Score",
            "sortable": False,
            "fieldOrder": 44,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "stage_name",
            "displayText": "Nexus Lifecycle Stage",
            "sortable": False,
            "fieldOrder": 45,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "notes",
            "displayText": "Notes",
            "sortable": False,
            "fieldOrder": 46,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "originalAggregatedSeverity",
            "displayText": "Original Aggregated Severity",
            "sortable": False,
            "fieldOrder": 47,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "osName",
            "displayText": "OS Name",
            "sortable": False,
            "fieldOrder": 48,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "owasp",
            "displayText": "OWASP",
            "sortable": False,
            "fieldOrder": 49,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "parameter",
            "displayText": "Parameter",
            "sortable": False,
            "fieldOrder": 50,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "patchId",
            "displayText": "Patch Id",
            "sortable": False,
            "fieldOrder": 51,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "payload",
            "displayText": "Payload",
            "sortable": False,
            "fieldOrder": 52,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "possiblePatches",
            "displayText": "Possible Patches",
            "sortable": False,
            "fieldOrder": 53,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "solution",
            "displayText": "Possible Solution",
            "sortable": False,
            "fieldOrder": 54,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "account_id",
            "displayText": "Prisma Cloud Compute Account ID",
            "sortable": False,
            "fieldOrder": 55,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "collections",
            "displayText": "Prisma Cloud Compute Collections",
            "sortable": False,
            "fieldOrder": 56,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "cluster",
            "displayText": "Prisma Cloud Compute Container Cluster",
            "sortable": False,
            "fieldOrder": 57,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "container_labels_wildcard",
            "displayText": "Prisma Cloud Compute Container Labels",
            "sortable": False,
            "fieldOrder": 58,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "namespace",
            "displayText": "Prisma Cloud Compute Container Namespace",
            "sortable": False,
            "fieldOrder": 59,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "clusters",
            "displayText": "Prisma Cloud Compute Image Clusters",
            "sortable": False,
            "fieldOrder": 60,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "labels_wildcard",
            "displayText": "Prisma Cloud Compute Image Labels",
            "sortable": False,
            "fieldOrder": 61,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "namespaces",
            "displayText": "Prisma Cloud Compute Image Namespaces",
            "sortable": False,
            "fieldOrder": 62,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "package_name",
            "displayText": "Prisma Cloud Compute Image Package Name",
            "sortable": False,
            "fieldOrder": 63,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "package_version",
            "displayText": "Prisma Cloud Compute Image Package Version",
            "sortable": False,
            "fieldOrder": 64,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "ransomwareFamily",
            "displayText": "Ransomware Family",
            "sortable": False,
            "fieldOrder": 65,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "resolvedOn",
            "displayText": "Resolved On",
            "sortable": False,
            "fieldOrder": 66,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "resourceCpe",
            "displayText": "Resource CPE",
            "sortable": False,
            "fieldOrder": 67,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "scannerName",
            "displayText": "Scanner Name",
            "sortable": False,
            "fieldOrder": 68,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "scannerOutput",
            "displayText": "Scanner Output",
            "sortable": False,
            "fieldOrder": 69,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "scannerPlugin",
            "displayText": "Scanner Plugin",
            "sortable": False,
            "fieldOrder": 70,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "scannerReportedSeverity",
            "displayText": "Scanner Reported Severity",
            "sortable": False,
            "fieldOrder": 71,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "severity",
            "displayText": "Severity",
            "sortable": False,
            "fieldOrder": 72,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "severityGroup",
            "displayText": "Severity Group",
            "sortable": False,
            "fieldOrder": 73,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "severityOverride",
            "displayText": "Severity Override",
            "sortable": False,
            "fieldOrder": 74,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "status",
            "displayText": "Status",
            "sortable": False,
            "fieldOrder": 75,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "tagIds",
            "displayText": "Tag Ids",
            "sortable": False,
            "fieldOrder": 76,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "tags",
            "displayText": "Tags",
            "sortable": False,
            "fieldOrder": 77,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "ticketsId",
            "displayText": "Tickets Id",
            "sortable": False,
            "fieldOrder": 78,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "ticketsLink",
            "displayText": "Tickets Link",
            "sortable": False,
            "fieldOrder": 79,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "ticketsStatus",
            "displayText": "Tickets Status",
            "sortable": False,
            "fieldOrder": 80,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "vrrGroup",
            "displayText": "VRR Group",
            "sortable": False,
            "fieldOrder": 81,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "vulnerability",
            "displayText": "Vulnerability",
            "sortable": False,
            "fieldOrder": 82,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "vulnerabilityRiskRating",
            "displayText": "Vulnerability Risk Rating",
            "sortable": False,
            "fieldOrder": 83,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "wascIds",
            "displayText": "WASC ID",
            "sortable": False,
            "fieldOrder": 84,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "workflowBatchCreated",
            "displayText": "Workflow Create Date",
            "sortable": False,
            "fieldOrder": 85,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "workflowBatchCreatedBy",
            "displayText": "Workflow Created By",
            "sortable": False,
            "fieldOrder": 86,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "workflowBatchExpiration",
            "displayText": "Workflow Expiration Date",
            "sortable": False,
            "fieldOrder": 87,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "workflowBatchId",
            "displayText": "Workflow Id",
            "sortable": False,
            "fieldOrder": 88,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "workflowBatchReason",
            "displayText": "Workflow Reason",
            "sortable": False,
            "fieldOrder": 89,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "workflowBatchState",
            "displayText": "Workflow State",
            "sortable": False,
            "fieldOrder": 90,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            },
            {
            "identifierField": "workflowBatchUserNote",
            "displayText": "Workflow State User Note",
            "sortable": False,
            "fieldOrder": 91,
            "selected": True,
            "sortOrder": 0,
            "sortType": "ASC"
            }
        ]
        }
    ],
    "exportInSingleFile": False
    })

    app_findings_req = requests.request("POST", ex_url, headers=headers, data=payload)
    print("\n[+] Status code",app_findings_req.status_code)
    json_object = json.loads(app_findings_req.text)
    exportName = "App_Blackduck"
    gen_id=json_object["id"]
    print("[+] The Job ID is {}\n".format(gen_id))

    print("[+] Waiting for the Job to Complete\n")

    while True:
        status_check = requests.get("https://{}.risksense.com/api/v1/client/{}/export/{}/status".format(platform,clientID,gen_id),headers=headers)
        status_json = json.loads(status_check.text)
        # print(status_json["fileId"])
        if status_json["fileId"] != None and status_json["status"] == "COMPLETE":
            print("[+] Downloading the Report\n")
            # time.sleep(2)
            down_report = requests.get("https://{}.risksense.com/api/v1/client/{}/export/{}".format(platform,clientID,gen_id),headers=headers)
            fileName = "Client_"+str(clientID)
            with open (fileName+".zip", 'wb') as f:
                f.write(down_report.content)
            z = zipfile.ZipFile(fileName+".zip")
            z.extractall("Findings")
            z.close()
            time.sleep(2)            
            #del_report = requests.delete("https://{}.risksense.com/api/v1/client/{}/export/{}".format(platform,clientID,gen_id),headers=headers)
            os.remove(fileName+".zip")
            break
        else:
            time.sleep(10)

def rs_ADO_field_data(VRR_group,CVSS3score,Scanner_Name,ado_template_fields): 
   if CVSS3score != "":
      if CVSS3score >= 9.0 and CVSS3score <= 10.0:
         CVSS_sev = ado_template_fields["data"]["ms.vss-work-web.work-item-types-data-provider"]["data"][0]["rules"]["fieldRules"]["10562887"][1][0][0]
      if CVSS3score >= 7.0 and CVSS3score <= 8.9 :
         CVSS_sev = ado_template_fields["data"]["ms.vss-work-web.work-item-types-data-provider"]["data"][0]["rules"]["fieldRules"]["10562887"][1][0][1]
      if CVSS3score >= 4.0 and CVSS3score <= 6.9 :
         CVSS_sev = ado_template_fields["data"]["ms.vss-work-web.work-item-types-data-provider"]["data"][0]["rules"]["fieldRules"]["10562887"][1][0][4]
      if CVSS3score >= 0.1 and CVSS3score <= 3.9 :
         CVSS_sev = ado_template_fields["data"]["ms.vss-work-web.work-item-types-data-provider"]["data"][0]["rules"]["fieldRules"]["10562887"][1][0][3]
      if CVSS3score == "" :
         CVSS_sev = ado_template_fields["data"]["ms.vss-work-web.work-item-types-data-provider"]["data"][0]["rules"]["fieldRules"]["10562887"][1][0][2]
         pass
   else:
      CVSS_sev = ""
      # ado_template_fields["data"]["ms.vss-work-web.work-item-types-data-provider"]["data"][0]["rules"]["fieldRules"]["10562887"][1][0][2]""

   if(VRR_group) == "Critical":
      RAS = ado_template_fields["data"]["ms.vss-work-web.work-item-types-data-provider"]["data"][0]["rules"]["fieldRules"]["10562886"][3][0][0]
      Priority_group = ado_template_fields["data"]["ms.vss-work-web.work-item-types-data-provider"]["data"][0]["rules"]["fieldRules"]["537285"][3][0][0]
   if(VRR_group) == "High":
      RAS = ado_template_fields["data"]["ms.vss-work-web.work-item-types-data-provider"]["data"][0]["rules"]["fieldRules"]["10562886"][3][0][1]
      Priority_group = ado_template_fields["data"]["ms.vss-work-web.work-item-types-data-provider"]["data"][0]["rules"]["fieldRules"]["537285"][3][0][0]
   if(VRR_group) == "Medium":
      RAS = ado_template_fields["data"]["ms.vss-work-web.work-item-types-data-provider"]["data"][0]["rules"]["fieldRules"]["10562886"][3][0][4]
      Priority_group = ado_template_fields["data"]["ms.vss-work-web.work-item-types-data-provider"]["data"][0]["rules"]["fieldRules"]["537285"][3][0][1]
   if(VRR_group) == "Low":
      RAS = ado_template_fields["data"]["ms.vss-work-web.work-item-types-data-provider"]["data"][0]["rules"]["fieldRules"]["10562886"][3][0][3]
      Priority_group = ado_template_fields["data"]["ms.vss-work-web.work-item-types-data-provider"]["data"][0]["rules"]["fieldRules"]["537285"][3][0][2]
   if(VRR_group) == "Info":
      RAS = ado_template_fields["data"]["ms.vss-work-web.work-item-types-data-provider"]["data"][0]["rules"]["fieldRules"]["10562886"][3][0][2]
      Priority_group = ado_template_fields["data"]["ms.vss-work-web.work-item-types-data-provider"]["data"][0]["rules"]["fieldRules"]["537285"][3][0][3]

   if(VRR_group) == "":
      if(CVSS_sev != "" and CVSS_sev == "Critical"):
         RAS = ado_template_fields["data"]["ms.vss-work-web.work-item-types-data-provider"]["data"][0]["rules"]["fieldRules"]["10562886"][3][0][0]
         Priority_group = ado_template_fields["data"]["ms.vss-work-web.work-item-types-data-provider"]["data"][0]["rules"]["fieldRules"]["537285"][3][0][0]
      elif(CVSS_sev != "" and CVSS_sev == "High"):
         RAS = ado_template_fields["data"]["ms.vss-work-web.work-item-types-data-provider"]["data"][0]["rules"]["fieldRules"]["10562886"][3][0][1]
         Priority_group = ado_template_fields["data"]["ms.vss-work-web.work-item-types-data-provider"]["data"][0]["rules"]["fieldRules"]["537285"][3][0][0]
      elif(CVSS_sev != "" and CVSS_sev == "Medium"):
         RAS = ado_template_fields["data"]["ms.vss-work-web.work-item-types-data-provider"]["data"][0]["rules"]["fieldRules"]["10562886"][3][0][4]
         Priority_group = ado_template_fields["data"]["ms.vss-work-web.work-item-types-data-provider"]["data"][0]["rules"]["fieldRules"]["537285"][3][0][1]
      elif(CVSS_sev != "" and CVSS_sev == "Low"):
         RAS = ado_template_fields["data"]["ms.vss-work-web.work-item-types-data-provider"]["data"][0]["rules"]["fieldRules"]["10562886"][3][0][3]
         Priority_group = ado_template_fields["data"]["ms.vss-work-web.work-item-types-data-provider"]["data"][0]["rules"]["fieldRules"]["537285"][3][0][2]
      else:
         RAS = ado_template_fields["data"]["ms.vss-work-web.work-item-types-data-provider"]["data"][0]["rules"]["fieldRules"]["10562886"][3][0][6] 
         Priority_group = ado_template_fields["data"]["ms.vss-work-web.work-item-types-data-provider"]["data"][0]["rules"]["fieldRules"]["537285"][3][0][3]

   if("polaris" in Scanner_Name.lower()):
      Scanner_Name = ado_template_fields["data"]["ms.vss-work-web.work-item-types-data-provider"]["data"][0]["rules"]["fieldRules"]["10562884"][3][0][6]
   elif("blackduck" in Scanner_Name.lower()):
      Scanner_Name = ado_template_fields["data"]["ms.vss-work-web.work-item-types-data-provider"]["data"][0]["rules"]["fieldRules"]["10562884"][3][0][0]
   elif("prisma" in Scanner_Name.lower()):
      Scanner_Name = ado_template_fields["data"]["ms.vss-work-web.work-item-types-data-provider"]["data"][0]["rules"]["fieldRules"]["10562884"][3][0][7]
   elif("qualys" in Scanner_Name.lower()):
      Scanner_Name = ado_template_fields["data"]["ms.vss-work-web.work-item-types-data-provider"]["data"][0]["rules"]["fieldRules"]["10562884"][3][0][8]
   elif("whitehat" in Scanner_Name.lower()):
      Scanner_Name = ado_template_fields["data"]["ms.vss-work-web.work-item-types-data-provider"]["data"][0]["rules"]["fieldRules"]["10562884"][3][0][9]
   elif("hackerone" in Scanner_Name.lower()):
      Scanner_Name = ado_template_fields["data"]["ms.vss-work-web.work-item-types-data-provider"]["data"][0]["rules"]["fieldRules"]["10562884"][3][0][2]
   else:
      Scanner_Name = ado_template_fields["data"]["ms.vss-work-web.work-item-types-data-provider"]["data"][0]["rules"]["fieldRules"]["10562884"][3][0][3]

   return RAS,CVSS_sev,Scanner_Name,Priority_group

def get_userId():
   user_details = requests.get("https://{}.risksense.com/api/v1/user/profile".format(platform),headers=api_header)
   user_details = json.loads(user_details.text)
   userID = str(user_details["userId"])
   return userID
