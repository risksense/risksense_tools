import pandas as pd,os

# RS parameters

platform = "    " # Risksense Platform needs to be filled, eg, platform4
clientID =          # Client ID in RiskSense Platform needs to be filled , eg,1363
apiToken = ""         # API token of RiskSense Platform accont needs to be filled
tagowner = "" # Used to rename the tag in RS after ticket creation , eg. 9920
ADO_RS_tag = "ADO_INC-"  # Name of the prefix tag in RS after creation of ticket in ADO


# App details to be exported (Nothing to be changed here...)

file_loc = os.getcwd() + "/Config.xlsx"
df_grp_sev = pd.read_excel(file_loc, sheet_name="Config",index_col=None, na_values=['NA'], usecols="I")
df_group_id = pd.read_excel(file_loc, sheet_name="Config",index_col=None, na_values=['NA'], usecols="A")
df_project = pd.read_excel(file_loc, sheet_name="Config",index_col=None, na_values=['NA'], usecols="B")
df_instance = pd.read_excel(file_loc, sheet_name="Config",index_col=None, na_values=['NA'], usecols="C")
df_token = pd.read_excel(file_loc, sheet_name="Config",index_col=None, na_values=['NA'], usecols="D")
df_user = pd.read_excel(file_loc, sheet_name="Config",index_col=None, na_values=['NA'], usecols="E")
df_area = pd.read_excel(file_loc, sheet_name="Config",index_col=None, na_values=['NA'], usecols="F")
df_iteration = pd.read_excel(file_loc, sheet_name="Config",index_col=None, na_values=['NA'], usecols="G")
df_sev = pd.read_excel(file_loc, sheet_name="Config",index_col=None, na_values=['NA'], usecols="H")
