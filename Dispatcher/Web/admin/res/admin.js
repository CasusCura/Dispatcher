var service = 'happyfeet';//'https://api.svh';
var table;

$(document).ready(function(){
	table = $('#deviceTable').DataTable();
	
	//Populate the table of all devices (default to 'ACTIVE')
	filterTable("ALL");
	
	//Make the table click-able
	$('#deviceTable tbody').on( 'click', 'tr', function () {
		if ( $(this).hasClass('selected') ) {
			$(this).removeClass('selected');
		} else {
			table.$('tr.selected').removeClass('selected');
			$(this).addClass('selected');
			openDeviceModal(table.row( this ).data()[0]);
		}
	});
})

//Get the list of devices from the service & populate the main table
function filterTable(filter){

	//highlight the clicked button
	if(event){
		document.getElementById("ALL").className="";
		document.getElementById("ACTIVE").className="";
		document.getElementById("INACTIVE").className="";
		document.getElementById("DEACTIVATED").className="";
		document.getElementById("RETIRED").className="";
		event.currentTarget.className = "is-active";
	}

	table.clear();

	if(filter=="ALL"){
		filter = "";
	}else{
		filter="event.id";
	}
	
	$.ajax({
		type: "GET",
		url: service+'/devices/',
		data: "devicestatus="+filter,
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		success: function (data) {
			$.each(data.deviceArray, function (index, device) {
				table.row.add([
					device.id, device.devicetype, device.status, device.location
				]);
			});
		},
		error: function (msg) {
			
			//TODO rm -rf & add notify user
			msg='{ "deviceArray":[{"id":"dev1","devicetype":"autoFallDetection","status":"active","location":"Narnia"},{"id":"dev12","devicetype":"ManualFallDetection","status":"active","location":"Mordor"}]}';
			var jsonMSG=JSON.parse(msg);
			$.each(jsonMSG.deviceArray, function (deviceArray, device) {
				table.row.add([
					device.id, device.devicetype, device.status, device.location
				]);
			});
		}
	});
	table.draw();
}

//Fetch the details of the specified device from the service
function populateDeviceEditDialog(devId){
	
	$.ajax({
		type: "GET",
		url: 'device/',
		data: "id=" + devId,
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		success: function (data) {
			$.each(data.device, function (k, v) {
				document.getElementById(k).value=v;
			});
		},
		error: function (msg) {
			
			//Temp JSON
			msg='{"id":"dev1","devicetype":"autoFallDetection","status":"INACTIVE","location":"Narnia","username":"aUserName","password":"password1234"}';
			var jsonMSG=JSON.parse(msg);
			$.each(jsonMSG, function (k, v) {
				document.getElementById(k).value=v;
			});
		}
	});
}

//POST updated details of a device to the service (or add a new device)
function updatePatientDev(){
	var deviceDetails = '{"id":"'+document.getElementById("id").value+'", "status":"'+ document.getElementById("status").value+'","location":"'+document.getElementById("location").value+'"}';
	
		$.ajax({
		type: "POST",
		url: 'devices/',
		data: deviceDetails,
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		success: function (data) {
			alert("success");
		},
		error: function (msg) {
			alert(deviceDetails);
		}
	});
	
	//Refresh the page
	location.href = service;
}	

//Opens the modal for editing a device's details, after populating its fields
function openDeviceModal(devId){
	populateDeviceEditDialog(devId);
	document.getElementById("DeviceEditModal").className = "modal is-active";
}

function openManageDeviceTypeModal(){
	populateManageDeviceTypeSelect();
	document.getElementById("manageDeviceTypesModal").className = "modal is-active";
}

function openAddDeviceModal(){
	populateAddDeviceTypeSelect();
	document.getElementById("addDeviceModal").className = "modal is-active";
}


function openAlertTypesModal(){
	populateAlertTypeSelect();
	document.getElementById("editAlertTypesModal").className = "modal is-active";
}

//Close any open modal dialog
function closeModal(){
	var target=event.currentTarget;
	
	while(!target.className.split(' ').includes('modal') && !target.className.split(' ').includes('is-active')){
		target = target.parentElement;
	}

	target.className = "modal";
}

//Send a new device type/update existing
//type to the service
function updateDeviceType(){
	var modalTarget = event.currentTarget;
	while(!modalTarget.className.split(' ').includes('modal')){
		modalTarget = modalTarget.parentElement;
	}
	var select;
	if(modalTarget.id == "manageDeviceTypesModal"){
		 select = document.getElementById("selectManageDeviceTypes");
	}else{
		 select = document.getElementById("selectAddNewDeviceType");
	}

	var devType = select.options[select.selectedIndex].innerHTML;
	
	var typeDetails = '{"devicetype":"' + devType + '",description":"' + document.getElementById("shortDescription") + '"}';
	
	$.ajax({
		type: "POST",
		url: 'devicetypes/',
		data: typeDetails,
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		success: function (data) {

		},
		error: function (msg) {
			alert("nope");
		}
	});
	//TODO move to success block?
	location.href="admin.html";
}

function populateManageDeviceTypeSelect(){
	var deviceTypeOptions = document.getElementById("selectManageDeviceTypes").options;

	while(deviceTypeOptions.length > 1){
		deviceTypeOptions[1].remove();
	}
	
	$.ajax({
		type: "GET",
		url: 'devicetypes/',
		data: "",
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
					document.getElementById("selectManageDeviceTypes").appendChild(option);
				});
			});
		}
	});
}

function populateAlertTypeSelect(){
		var deviceTypeOptions = document.getElementById("selectAlertTypes").options;

	while(deviceTypeOptions.length > 1){
		deviceTypeOptions[1].remove();
	}
	
	$.ajax({
		type: "GET",
		url: 'alerttypes/',
		data: "",
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		success: function (data) {
			alert("hi");
		},
		error: function (msg) {
			//Temp JSON
			msg='{"alertypes":[{"name":"I haz fallen","id":"1234"}, {"name":"and cant get up","id":"5678"}]}';
			var jsonMSG=JSON.parse(msg);
			$.each(jsonMSG, function (k, v) {
				$.each(v, function (num, alertType){
					var option = document.createElement("option");
					option.value=alertType.id;
					option.innerHTML=alertType.name;
					document.getElementById("selectAlertTypes").appendChild(option);
				});
			});
		}
	});
}

function populateAddDeviceTypeSelect(){
	var deviceTypeOptions = document.getElementById("selectAddNewDeviceType").options;

	while(deviceTypeOptions.length > 0){
		deviceTypeOptions[0].remove();
	}
	
	$.ajax({
		type: "GET",
		url: 'devicetypes/',
		data: "used_by=patient",
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
					document.getElementById("selectAddNewDeviceType").appendChild(option);
				});
			});
		}
	});
}

function deviceTypeSelectChange(){
	var element = document.getElementById("selectManageDeviceTypes");
	var selectedDeviceType = element.options[element.selectedIndex].innerHTML;
	if(selectedDeviceType == "[Add a New Device Type]"){
		document.getElementById("deviceType").value="";
		document.getElementById("shortDescription").value="";
		return;
	}
	//Get the data for the selected device type and populate the inputs
		$.ajax({
		type: "GET",
		url: 'devicetypes/',
		data: "",
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

function alertTypeSelectChange(){
	var element = document.getElementById("selectAlertTypes");
	var selectedAlertType = element.options[element.selectedIndex].value;
	if(selectedAlertType == "[Add a New Alert Type]"){
			document.getElementById("alertType").value="";
			document.getElementById("alertId").value="";
			document.getElementById("alertPriority").value="";
			document.getElementById("alertShortDescription").value="";
		return;
	}
	//Get the data for the selected device type and populate the inputs
		$.ajax({
		type: "GET",
		url: 'alerttype/',
		data: "id=" + selectedAlertType,
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		success: function (data) {
			document.getElementById("alertType").value=data.name;
			document.getElementById("alertId").value=data.id;
			document.getElementById("alertPriority").value=data.priority;
			document.getElementById("alertShortDescription").value=data.description;
		
		},
		error: function (msg) {
			//Temp JSON
			msg='{"id":"1234","name":"someName","priority":"42","description":"halp me"}';
			var jsonMSG=JSON.parse(msg);
			document.getElementById("alertType").value=jsonMSG.name;
			document.getElementById("alertId").value=jsonMSG.id;
			document.getElementById("alertPriority").value=jsonMSG.priority;
			document.getElementById("alertShortDescription").value=jsonMSG.description;
		}
	});
}

function updateAlertType(){
	//TODO stopped working here
	var element = document.getElementById("selectAlertTypes");
	var selectedAlertType = element.options[element.selectedIndex].value;
	var priority = document.getElementById("alertPriority").value;
	var alertId = document.getElementById("alertId").value;
	var description = document.getElementById("alertShortDescription").value;
	var alertType = document.getElementById("alertType").value;
	var alertDetails = '{"id":"' + alertId +'", "name":"' + alertType + '", "priority":"'+priority+'","description":"'+ description+'}';

		$.ajax({
		type: "POST",
		url: 'alerttype/',
		data: alertDetails,
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		success: function (data) {
			alert("success");
		},
		error: function (msg) {
			alert(alertDetails);
		}
	});
	location.href=service;
}

function addNewPatientDevice(){
	var element = document.getElementById("selectAddNewDeviceType");
	var selectedDeviceType = element.options[element.selectedIndex].innerHTML;
	
	var deviceDetails = '{"id":"'+document.getElementById("id").value+'", '+'"devicetype":"' + selectedDeviceType + '", "status":"INACTIVE"}';
	
		$.ajax({
		type: "POST",
		url: 'devices/',
		data: deviceDetails,
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		success: function (data) {
			alert("success");
		},
		error: function (msg) {
			alert(deviceDetails);
		}
	});
	
	//Refresh the page
	location.href = service;
}
