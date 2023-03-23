# cmdb_update
A Python script for updating a series of host's CMDB information by reading the information from a .csv file.

----

## Configuration
The configuration file is located at `conf/config.toml`. Open this file
in you preferred text editor, and update each parameter to reflect those
pertinent to your user and client.

### Test case

    1. Run the tool with Network type as 'IP based'
    2. Run the tool with Network type as 'Hostname based'
    3. Run the tool with blanks values to some columns in the csv file


#### CSV file
An example .csv file has been provided in this folder. There should be one row per host. __Do not edit the headers of this file.__

A `host` entry fields are required.  Other fields are optional depending on your need to update them.

##### Column Names:
 * `ec2_identifier` (__REQUIRED__ if this field is included in precedence of MIXED network type)
 * `netbios` (__REQUIRED__ if this field is included in precedence of MIXED network type)
 * `ip_address` (__REQUIRED__ if this field is included in precedence of IP Address or MIXED network types)
 * `hostname` (__REQUIRED__ if this field is included in precedence of Hostname or MIXED network types)
 * `fqdn` (__REQUIRED__ if this field is included in precedence of MIXED network type)
 * `dns` (__REQUIRED__ if this field is included in precedence of MIXED network type)
 * `mac_addr` (__REQUIRED__ if this field is included in precedence of MIXED network type)
 * `scanner_specific_unique_id` (__REQUIRED__ if this field is included in precedence of MIXED network type)
 * `os` (Operating System)
 * `manufacturer` (Manufactured By)
 * `model_id` (Model)
 * `location` (Location)
 * `managed_by` (Managed By)
 * `owned_by` (Owned By)
 * `supported_by` (Supported By)
 * `support_group` (Support Group)
 * `sys_updated_on` (Last Scanned)
 * `asset_tag` (Asset tag(s))
 * `mac_address` (Mac Address)
 * `ferpa` (FERPA Compliance Asset)
 * `hipaa` (HIPAA Compliance Asset)
 * `pci` (PCI Compliance Asset)
 * `sys_id` (Unique Id)
 * `cf_1` (Custom Field 1)
 * `cf_2` (Custom Field 2)
 * `cf_3` (Custom Field 3)
 * `cf_4` (Custom Field 4)
 * `cf_5` (Custom Field 5)
 * `cf_6` (Custom Field 6)
 * `cf_7` (Custom Field 7)
 * `cf_8` (Custom Field 8)
 * `cf_9` (Custom Field 9)
 * `cf_10` (Custom Field 10)
 * `am_1`  (Asset Matching Field 1)
 * `am_2`  (Asset Matching Field 2)
 * `am_3`  (Asset Matching Field 3)

## Execution
Once you have completed configuration of the script, and completed your .csv file, the script can be run from your
terminal as follows:

```commandline

python3 update_cmdb.py

 -- OR (depending on your installation) --

python update_cmdb.py

```