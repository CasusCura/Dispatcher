var service = 'happyfeet';//'https://api.svh';
var table;

$(document).ready(function(){
	table = $('#deviceTable').DataTable();
	
	//Populate the table of all devices (default to 'isUse')
	filterTable("ALL");
	
	//Make the table click-able
	$('#deviceTable tbody').on( 'click', 'tr', function () {
		if ( $(this).hasClass('selected') ) {
			$(this).removeClass('selected');
		} else {
			table.$('tr.selected').removeClass('selected');
			$(this).addClass('selected');
			console.log( table.row( this ).data()[0] );
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

	$.ajax({
		type: "GET",
		url: service+'/devices/',
		data: "devicestatus="+filter,
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		success: function (data) {
			//TODO Duplicate error block here
		},
		error: function (msg) {
			
			//Temp JSON
			msg='{ "deviceArray":[{"id":"dev1","devicetype":"autoFallDetection","status":"active","location":"Narnia"},{"id":"dev12","devicetype":"ManualFallDetection","status":"active","location":"Mordor"}]}';
			var jsonMSG=JSON.parse(msg);
			$.each(jsonMSG.deviceArray, function (deviceArray, device) {
				table.row.add([
					device.id, device.devicetype, device.status, device.location
				]);
			});
			table.draw();
		}
	});
	table.draw();
}

//Fetch the details of the specified device from the service
function populateDeviceEditDialog(devId){
	
	$.ajax({
		type: "GET",
		url: 'devices/',
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
	alert("DING");
	var deviceDetails = "{}";
	
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
		}
	});
	
	//Refresh the page
	location.href = service;
}	

//TODO rm?
function getQueryVariable(variable){
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

//Close any open modal dialog
function closeModal(){
	var target=event.currentTarget;
	
	while(!target.className.split(' ').includes('modal') && !target.className.split(' ').includes('is-active')){
		target = target.parentElement;
	}

	target.className = "modal";
}

//Send either a new device type or an update to an existing device
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
		url: 'devices/',
		data: typeDetails,
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		success: function (data) {
			alert("hi");
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
					document.getElementById("selectManageDeviceTypes").appendChild(option);
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

function addNewPatientDevice(){
	//Implement it
	closeModal();
}