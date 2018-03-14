
# coding: utf-8

# In[1]:


import os 
print(os.getcwd())


# In[2]:

from dispatcher.database import init_db, get_session


# In[3]:

init_db()


# In[4]:

from dispatcher import models


# In[5]:

# Can create nurse
from dispatcher.models.users import Nurse
sess = get_session()
nurse = Nurse('alice','password','3rd')
sess.add(nurse)
sess.commit()
sess.close()


# In[6]:

# Testing assertion
sess = get_session()
t = sess.query(Nurse).filter(Nurse.username=='alice')
print([n.username for n in t.all()])
sess.close()
# Clean up
sess = get_session()
t = sess.query(Nurse).filter(Nurse.username=='alice')
print([sess.delete(n) for n in t.all()])
sess.commit()
sess.close()


# In[7]:

# Can create admin
from dispatcher.models import Admin
sess = get_session()
a = Admin('Bocar','password','the doctor')
sess.add(a)
sess.commit()
sess.close()


# In[8]:

# Testing assertion
sess = get_session()
t = sess.query(Admin).filter(Admin.username=='Bocar')
print([n.username for n in t.all()])
sess.close()
# Clean up
sess = get_session()
t = sess.query(Admin).filter(Admin.username=='Bocar')
print([sess.delete(n) for n in t.all()])
sess.commit()
sess.close()


# In[9]:

# Create New Nurse Device Type
from dispatcher.models import DeviceType, NurseDeviceType
sess = get_session()
newnursedevt = NurseDeviceType('testdev','used to testing the code')
sess.add(newnursedevt)
sess.commit()
sess.close()


# In[10]:

# Testing assertion
sess = get_session()
t = sess.query(NurseDeviceType).filter(NurseDeviceType.name=='testdev')
print([n.name for n in t.all()])
# Clean up
t = sess.query(NurseDeviceType).filter(NurseDeviceType.name=='testdev')
print([sess.delete(n) for n in t.all()])
sess.commit()
sess.close()


# In[11]:

# Create Nurse Device 
# Create new nurse device type
from dispatcher.models import DeviceType, NurseDeviceType, NurseDevice
sess = get_session()
newnursedevt = NurseDeviceType('testdev','used to testing the code')
sess.add(newnursedevt)
# create the nurse dev instance
nursedev = NurseDevice(newnursedevt.id, '3rd floor')
sess.add(nursedev)
sess.commit()
sess.close()


# In[12]:

# Testing assertion
sess = get_session()
# test relationship from type
t = sess.query(NurseDeviceType).filter(NurseDeviceType.name=='testdev')
print([n.name for n in t.all()])
print([[(nd.id,nd.floor) for nd in ndevt.devices] for ndevt in t.all()])
# test retrival by floor
t = sess.query(NurseDevice).filter(NurseDevice.floor=='3rd floor')
print([(nd.id,nd.floor) for nd in t.all()])
# Clean up
t = sess.query(NurseDevice)
print([sess.delete(n) for n in t.all()])
t = sess.query(NurseDeviceType)
print([sess.delete(n) for n in t.all()])
sess.commit()
sess.close()


# In[13]:

# Create New Patient Device Type 
from dispatcher.models import DeviceType, PatientDeviceType
sess = get_session()
newpatientdevt = PatientDeviceType('testpdev','used to testing the code')
sess.add(newpatientdevt)
sess.commit()
sess.close()


# In[14]:

# Testing assertion
sess = get_session()
t = sess.query(PatientDeviceType).filter(PatientDeviceType.name=='testpdev')
print([n.name for n in t.all()])
sess.close()
# Clean up
sess = get_session()
t = sess.query(PatientDeviceType).filter(PatientDeviceType.name=='testpdev')
print([sess.delete(n) for n in t.all()])
sess.commit()
sess.close()


# In[15]:

# Add requests to patient device type
# Create New Patient Device Type 
from dispatcher.models import DeviceType, PatientDeviceType, RequestType
sess = get_session()
newpatientdevt = PatientDeviceType('testpdev','used to testing the code')
sess.add(newpatientdevt)
# Create new requests for this new device
pdid = newpatientdevt.id
id = 0
newpreq1 = RequestType(1, 'testone','used to testing the code', pdid, 1)
id+=1
newpreq2 = RequestType(2, 'testtwo','used to testing the code', pdid, 2)
sess.add(newpreq1)
sess.add(newpreq2)
sess.commit()
sess.close()


# In[16]:

# Testing assertion
# Test relationship
sess = get_session()
t = sess.query(PatientDeviceType).filter(PatientDeviceType.name=='testpdev')
pds = t.all()
print([[rt.name for rt in pd.requesttypes] for pd in pds])
# test look up based on device
testp = pds[0]
r = sess.query(RequestType).filter(PatientDeviceType.id==testp.id)
print([rt.name for rt in r])
# test look up based on device type and device request id
testp = pds[0]
r = sess.query(RequestType).filter(PatientDeviceType.id==testp.id, 
                                           RequestType.deviceid==2)
print([rt.name for rt in r])
# Clean up
t = sess.query(PatientDeviceType).filter(PatientDeviceType.name=='testpdev')
print([[sess.delete(rt) for rt in dt.requesttypes ] for dt in t])
print([sess.delete(n) for n in t.all()])
sess.commit()
sess.close()


# In[17]:

# create new patient device
# Create New Patient Device Type 
from dispatcher.models import DeviceType, PatientDeviceType, PatientDevice
sess = get_session()
newpatientdevt = PatientDeviceType('testptdev','used to testing the code')
sess.add(newpatientdevt)
# Create patient device
pdev = PatientDevice(newpatientdevt.id, 'room:501')
sess.add(pdev)
sess.commit()
sess.close()


# In[18]:

# Testing assertion
sess = get_session()
# test relationship from type
t = sess.query(PatientDeviceType).filter(PatientDeviceType.name=='testptdev')
print([pdt.name for pdt in t.all()])
pdevt= t.first()
print([(pd.id, pd.location) for pd in pdevt.devices])
# test retrival by location
t = sess.query(PatientDevice).filter(PatientDevice.location=='room:501')
print([(pd.id, pd.location) for pd in t.all()])
# Clean up
t = sess.query(PatientDevice).filter(PatientDevice.location=='room:501')
print([sess.delete(pd) for pd in t.all()])
t = sess.query(PatientDeviceType).filter(PatientDeviceType.name=='testptdev')
print([sess.delete(n) for n in t.all()])
sess.commit()
sess.close()


# In[19]:

# Create new Issue
# Create New Patient Device Type 
from dispatcher.models import DeviceType, PatientDeviceType, RequestType, Issue, PatientDevice
sess = get_session()
newpatientdevt = PatientDeviceType('testpdevt','used to testing the code')
sess.add(newpatientdevt)
# Create new requests for this new device
pdid = newpatientdevt.id
id = 0
newpreq1 = RequestType(1, 'testone','used to testing the code', pdid, 0)
id += 1
newpreq2 = RequestType(2, 'testtwo','used to testing the code', pdid, 1)
sess.add(newpreq1)
sess.add(newpreq2)
# Create patient device
pdev = PatientDevice(newpatientdevt.id, 'room:501')
sess.add(pdev)
# Create Issue
issue = Issue(pdev.id, newpreq1.id, newpreq1.priority)
sess.add(issue)
sess.commit()
sess.close()


# In[20]:

# Testing assertion
sess = get_session()
# test retrieval of issue
t = sess.query(Issue).all()
print([(i.request.name, i.first_issued) for i in t])
# test retrieval of issue location
print([(i.request.name, i.device.location) for i in t])
print([(i.request.name, i.status) for i in t])
# Clean up
t = sess.query(Issue)
print([sess.delete(pd) for pd in t.all()])
t = sess.query(PatientDevice)
print([sess.delete(pd) for pd in t.all()])
t = sess.query(PatientDeviceType)
print([sess.delete(n) for n in t.all()])
sess.commit()
sess.close()


# In[21]:

# Create new Responses
# Create New Patient Device Type 
from dispatcher.models import DeviceType, PatientDeviceType, RequestType, Issue, PatientDevice
sess = get_session()
newpatientdevt = PatientDeviceType('testpdevt','used to testing the code')
sess.add(newpatientdevt)
# Create new requests for this new device
pdid = newpatientdevt.id
id = 0
newpreq1 = RequestType(1, 'testone','used to testing the code', pdid, 0)
id += 1
newpreq2 = RequestType(2, 'testtwo','used to testing the code', pdid, 1)
sess.add(newpreq1)
sess.add(newpreq2)
# Create patient device
pdev = PatientDevice(newpatientdevt.id, 'room:501')
sess.add(pdev)
# Create Issue
issue = Issue(pdev.id, newpreq1.id, newpreq1.priority)
sess.add(issue)
# Create new nurse device type
from dispatcher.models import NurseDeviceType, NurseDevice
nursedevt = NurseDeviceType('testdev','used to testing the code')
sess.add(nursedevt)
# create the nurse dev instance
nursedev1 = NurseDevice(nursedevt.id, '3rd floor')
sess.add(nursedev1)
nursedev2 = NurseDevice(nursedevt.id, '3rd floor')
sess.add(nursedev2)
# Create Responses
from dispatcher.models import Response
response1 = Response(nursedev1.id, 4, issue.id, '{\'data\':\'\'}')
sess.add(response1)
response2 = Response(nursedev2.id, 6, issue.id, '{\'data\':\'\'}')
sess.add(response2)
sess.commit()
sess.close()


# In[22]:

# Testing assertion
sess = get_session()
# retrieval of responses
t = sess.query(Response).all()
print([(r.id, r.first_issued, r.last_eta) for r in t])
# retrieval of issue
t = sess.query(Issue).all()
print([(i.request.name, i.first_issued) for i in t])
print([[(i.request.name, r.first_issued) for r in i.responses]for i in t])

# Clean up
t = sess.query(Response)
print([sess.delete(pd) for pd in t.all()])
t = sess.query(NurseDevice)
print([sess.delete(pd) for pd in t.all()])
t = sess.query(NurseDeviceType)
print([sess.delete(pd) for pd in t.all()])
t = sess.query(Issue)
print([sess.delete(pd) for pd in t.all()])
t = sess.query(PatientDevice)
print([sess.delete(pd) for pd in t.all()])
t = sess.query(PatientDeviceType)
print([sess.delete(n) for n in t.all()])
sess.commit()
sess.close()


# In[30]:

# Create new Request Data
# Create New Patient Device Type 
from dispatcher.models import DeviceType, PatientDeviceType, RequestType, Issue, PatientDevice
from dispatcher.models import RequestData
sess = get_session()
newpatientdevt = PatientDeviceType('testpdevt','used to testing the code')
sess.add(newpatientdevt)
# Create new requests for this new device
pdid = newpatientdevt.id
id = 0
newpreq1 = RequestType(1, 'testone','used to testing the code', pdid, 0)
id += 1
newpreq2 = RequestType(2, 'testtwo','used to testing the code', pdid, 1)
sess.add(newpreq1)
sess.add(newpreq2)
# Create patient device
pdev = PatientDevice(newpatientdevt.id, 'room:501')
sess.add(pdev)
# Create Issue
issue = Issue(pdev.id, newpreq1.id, newpreq1.priority)
sess.add(issue)
# Create Request Data
rd1 = RequestData(pdev.id, issue.id, '{\'data\':\'1\'}')
sess.add(rd1)
rd2 = RequestData(pdev.id, issue.id, '{\'data\':\'2\'}')
sess.add(rd2)
rd3 = RequestData(pdev.id, issue.id, '{\'data\':\'3\'}')
sess.add(rd3)
sess.commit()
sess.close()


# In[31]:

# Testing assertion
sess = get_session()
# retrieval of responses
t = sess.query(RequestData)
print([(r.id, r.timestamp, r.data) for r in t.all()])
# retrieval of issue
t = sess.query(Issue).all()
print([[(i.request.name, r.data) for r in i.data]for i in t])

# Clean up
t = sess.query(RequestData)
print([sess.delete(pd) for pd in t.all()])
t = sess.query(Issue)
print([sess.delete(pd) for pd in t.all()])
t = sess.query(PatientDevice)
print([sess.delete(pd) for pd in t.all()])
t = sess.query(PatientDeviceType)
print([sess.delete(n) for n in t.all()])
sess.commit()
sess.close()


# In[ ]:



