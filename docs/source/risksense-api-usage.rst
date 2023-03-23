
======================================
Using Risksense API Library
======================================

To begin make sure you provide the system path to the lib package before importing the script
example. 

.. code:: python

     >>> sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'lib'))


To use risksense lib package please ensure you import risksense api in your script

.. code:: python

     >>> import risksense_api as rsapi


To perform usage of the subject functions you must first create an object and use that object
for subject function definitions. Please ensure you should provide the client id either during function definitions or by setting a default client id using the below function ``set_default_client_id()``

.. code:: python

    >>> self.rs=rs_api.RiskSenseApi(self._rs_platform_url, api_key)
    >>> self.rs.set_default_client_id(self.__client_id)

where self._rs_platform_url is the url of the platform and apikey is the user apikey

Now post the risksense object creation, you can use the object ``self.rs`` for using functions in risksense api packages

.. code:: python
  
    >>> self.rs.{subjectname}.{functionname}
    where 
        subjectname - The subject module present in the lib package
        functionname - The functionname define for  that particular subject

.. toctree::
   :maxdepth: 2
   :caption: Section

   /lib/applications
   /lib/applicationfindings
   /lib/applicationurl
   /lib/attachments
   /lib/clients
   /lib/findinghistory
   /lib/export
   /lib/groupby
   /lib/hosts 
   /lib/hostfinding
   /lib/patch
   /lib/playbook
   /lib/rs3
   /lib/quickfilters
   /lib/sla
   /lib/tags
   /lib/workflows
   /lib/assessments
   /lib/networks
   /lib/roles
   /lib/users
   /lib/groups  
   /lib/vulnerabilities
   /lib/weaknesses   
   /lib/uploads
   /lib/notifications
   /lib/connectors
   /lib/tickets


  