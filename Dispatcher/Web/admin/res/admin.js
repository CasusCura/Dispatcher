var service = 'wherever this is going';
var table;

$(document).ready(function(){
	table = $('#deviceTable').DataTable();
	
	//Populate the table of all devices (default to 'isUse')
	filterTable("inUse");
	
	//Make the table clickable
	$('#deviceTable tbody').on( 'click', 'tr', function () {
		if ( $(this).hasClass('selected') ) {
			$(this).removeClass('selected');
		} else {
			table.$('tr.selected').removeClass('selected');
			$(this).addClass('selected');
		}
	});
})

//Get the list of devices from the service & populate the main table
function filterTable(filter){

	//highlight the clicked button
	if(event){	
		document.getElementById("inUse").className="";
		document.getElementById("inStorage").className="";
		document.getElementById("activeAlerts").className="";
		event.currentTarget.className = "is-active";
	}

	table.clear();

	$.ajax({
		type: "GET",
		url: 'devices/',
		data: "{}",
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		success: function (data) {
			$.each(data.device, function (k, v) {
			table.row.add([
			"devId","dev type1","dev status","<a href=\"PatientDevEdit.html?devId=devId\" class=\"btn btn-primary\">edit</a>"
			]).draw();
			});
					
		},
		error: function (msg) {
			
			//Temp JSON
			msg='{ "deviceArray":[{"deviceId":"dev1","deviceType":"autoFallDetection","deviceStatus":"active"},{"deviceId":"dev2","deviceType":"autoFallDetection","deviceStatus":"active"}]}';
			var jsonMSG=JSON.parse(msg);
			//TODO duplicate / move to success block once schema is finalized
			$.each(jsonMSG.deviceArray, function (deviceArray, device) {
				table.row.add([
					device.deviceId,device.deviceType,device.deviceStatus,"<a href=# onClick=\"openDeviceModal('"+device.deviceId+"')\" class=\"btn btn-primary\">edit</a>"
				]);
			});
			table.draw();
		}
	});
	table.draw();
}

//Fetch the details of the specified device from the service
function populateDeviceEditDialog(deviceId){
	//TODO make ajax call to get this device's data, 
	//then populate all the inputs with the current values
	
	$.ajax({
		type: "GET",
		url: 'devices/',
		data: "{}",
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		success: function (data) {
			$.each(data.device, function (k, v) {
				document.getElementById(k).innerHTML=v;
			});
		},
		error: function (msg) {
			
			//Temp JSON
			msg='{"deviceId":"devId1","deviceType":"autoFallDetection","room":"1234","status":"Storage","username":"aUserName","password":"password1234"}';
			var jsonMSG=JSON.parse(msg);
			$.each(jsonMSG, function (k, v) {
				
				document.getElementById(k).value=v;
				
			/*	if(k == "notificationGroups"){
					$.each(v, function (num, group){
					var option = document.createElement("option");
					option.value=group;
					option.innerHTML=group;
					document.getElementById("notificationGroups").appendChild(option);
					});
				}else{
					document.getElementById(k).value=v;
				}*/
			});
		}
	});
}

//Send updated details of a device to the service
function updatePatientDev(){
	alert(getQueryVariable("devId"));
	alert("send to service");
	
	//TODO ajax data to service
	
	location.href="admin.html";
}	

//TODO rm?
function getQueryVariable(variable)
{
	var query = window.location.search.substring(1);
	var vars = query.split("&");
	for (var i=0;i<vars.length;i++) {
		var pair = vars[i].split("=");
		if(pair[0] == variable){
			return pair[1];
		}
	}
	return(false);
}

//Opens the modal for editing a device's details, after populating its fields
function openDeviceModal(devId){
	//TODO populate the fields
	document.getElementById("DeviceEditModal").className = "modal is-active";
}

//Close any open modal dialog
function closeModal(){
	event.currentTarget.parentElement.parentElement.parentElement.className = "modal";
}

//Send either a new device type or an update to an existing device
//type to the service
function updateDeviceType(){
	
	//TODO if not [add...]
	//TODO make 2 dif ajax?
	var element = document.getElementById("selectDeviceType");
	alert(element.options[element.selectedIndex].innerHTML);
	$.ajax({
		type: "POST",
		url: 'devices/',
		data: "{}",
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		success: function (data) {
			alert(data);
		},
		error: function (msg) {
			alert(msg);
		}
	});
	//TODO move to success block?
	location.href="admin.html";
}

function populateDeviceTypeSelect(){
		
		//Get all device types and populate the <select>
	$.ajax({
		type: "GET",
		url: 'devices/',
		data: "{}",
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		success: function (data) {
			alert("hi");
		},
		error: function (msg) {
			//Temp JSON
			msg='{"deviceTypes":["push button detection", "auto fall detection", "HALP"]}';
			var jsonMSG=JSON.parse(msg);
			$.each(jsonMSG, function (k, v) {
				$.each(v, function (num, deviceType){
					var option = document.createElement("option");
					option.value=deviceType;
					option.innerHTML=deviceType;
					document.getElementById("selectDeviceType").appendChild(option);
				});
			});
		}
	});
}

function deviceTypeSelectChange(thing){
	var element = document.getElementById("selectDeviceType");
	var selectedDeviceType = element.options[element.selectedIndex].innerHTML;
	if(selectedDeviceType == "[Add a New Device Type]"){
		document.getElementById("deviceType").value="";
		document.getElementById("shortDescription").value="";
		return;
	}
	//Get the data for the selected device type and populate the inputs
		$.ajax({
		type: "GET",
		url: 'devices/',
		data: "{}",
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		success: function (data) {
			alert("hi");
		},
		error: function (msg) {
			//Temp JSON
			msg='{"deviceType":"auto fall detection","shortDescription":"An accelerometer-based fall detection bracelet"}';
			var jsonMSG=JSON.parse(msg);
			$.each(jsonMSG, function (k, v) {
				document.getElementById(k).value=v;
			});
		}
	});
}