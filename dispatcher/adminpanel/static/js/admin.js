var service = '';//'https://api.svh';
var table;

$(document).ready(function(){
	table = $('#deviceTable').DataTable();

	//Populate the table of all devices (default to 'ACTIVE')


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

	filterTable("ALL");

	addAlertDiv();
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
		filter=event.currentTarget.id;
	}

	table.clear();



	$.ajax({
		type: "GET",
		url: 'devices',
		data: "used_by=patient&status="+filter,
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		success: function (data) {
			$.each(data.devices, function (index, device) {
				table.row.add([
					device.serial_number, device.devicetype, device.status, device.location
				]);
				table.draw();
			});
		},
		error: function (msg) {
			alert(msg);
		}
	});
	table.draw();
}

//Fetch the details of the specified device from the service
function populateDeviceEditDialog(devId){

	$.ajax({
		type: "GET",
		url: 'device',
		data: "id=" + devId,
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		success: function (data) {
				document.getElementById("id").value=data.device.id;
				document.getElementById("devicetype").value=data.device.devicetype;
				document.getElementById("location").value=data.device.location;
				document.getElementById("status").value=data.device.status;
		},
		error: function (msg) {
			alert(msg);
			//Temp JSON
			msg='{"id":"dev1","devicetype":"autoFallDetection","status":"INACTIVE","location":"Narnia","username":"aUserName","password":"password1234"}';
			var jsonMSG=JSON.parse(msg);
			/*$.each(jsonMSG, function (k, v) {
				document.getElementById(k).value=v;
			});*/
		}
	});
}

//POST updated details of a device to the service (or add a new device)
function updatePatientDev(){
	var deviceDetails = '{"device":{"used_by":"patient","device_type":"'+document.getElementById("id").value+'", "status":"'+ document.getElementById("status").value+'","location":"'+document.getElementById("location").value+'"}}';

		$.ajax({
		type: "POST",
		url: 'device',
		data: deviceDetails,
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		success: function (data) {
			alert("success");
		},
		error: function (msg) {
			alert(msg);
			alert(deviceDetails);
		}
	});
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

	document.getElementById("deviceAlert").innerHTML="";
}

//Send a new device type/update existing
//type to the service
function updateDeviceType(){

	var devType = document.getElementById("deviceType").value;

	var desc = document.getElementById("shortDescription").value;
	var deviceTypeId="";

	var element = document.getElementById("selectManageDeviceTypes");
	var selectedDeviceType = element.options[element.selectedIndex].innerHTML;

	if(selectedDeviceType!='[Add a New Device Type]'){

		deviceTypeId = '"devicetype_id":"'+element.options[element.selectedIndex].value+'",';
	}
	var alertTypes = document.getElementById("deviceAlert").children;

	var json = '{"device_type":{'+deviceTypeId+'"used_by":"patient","product_name":"'+devType+'","product_description":"'+desc+'"}}';

	$.ajax({
		type: "POST",
		url: 'devicetype',
		data: json,
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		success: function (data) {
			deviceTypeId=data.devicetype_id;

			var alerts=[];

			$.each(document.getElementById("deviceAlert").children,function(k,v){
				var inputs=v.children[1].children;
				var name = inputs[1].value;
				var description = inputs[3].value;
				var priority = inputs[5].value;
				alerts.push('{"devicetype":"'+deviceTypeId+'","request_id":"'+name+'", "description":"'+description+'","priority":"'+priority+'"}');
			});
			$.each(alerts, function(k,v){

				$.ajax({
					type: "POST",
					url: 'requesttype',
					data: '{"request_type":'+v+'}',
					contentType: "application/json; charset=utf-8",
					dataType: "json",
					success: function (data) {

					},
					error: function (msg) {
						alert(msg);
						alert(requestTypesJson);
					}
				});

			});
		},
		error: function (msg) {
			alert(msg);
			alert(json);
		}
	});



}

function populateManageDeviceTypeSelect(){
	var deviceTypeOptions = document.getElementById("selectManageDeviceTypes").options;

	while(deviceTypeOptions.length > 1){
		deviceTypeOptions[1].remove();
	}

	$.ajax({
		type: "GET",
		url: 'devicetypes',
		data: "used_by=patient",
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		success: function (data) {

			$.each(data.device_types, function(k,v){
				var option = document.createElement("option");
				option.value=v.id;
				option.innerHTML=v.product_name;
				document.getElementById("selectManageDeviceTypes").appendChild(option);
			});
		},
		error: function (msg) {
			alert(msg);
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
		url: 'devicetypes',
		data: "used_by=patient",
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		success: function (data) {
			$.each(data.device_types, function(k,v){
				var option = document.createElement("option");
				option.value=v.id;
				option.innerHTML=v.product_name;
				document.getElementById("selectAddNewDeviceType").appendChild(option);
			});
		},
		error: function (msg) {
			alert(msg);
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
	var selectedDeviceId = element.options[element.selectedIndex].value;
	//Get the data for the selected device type and populate the inputs
		$.ajax({
		type: "GET",
		url: 'devicetype',
		data: "id="+selectedDeviceId,
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		success: function (data) {
			document.getElementById("deviceType").value=data.device_type.product_name;
			document.getElementById("shortDescription").value=data.device_type.product_description;
		},
		error: function (msg) {
			//Temp JSON
			alert(msg);
		}
	});
}

function addNewPatientDevice(){
	var element = document.getElementById("selectAddNewDeviceType");
	var selectedDeviceType = element.options[element.selectedIndex].value;
	var serial = document.getElementById("serial").value;

	var deviceDetails = '{"device":{"serial":"'+serial+'","used_by":"patient", "device_type":"' + selectedDeviceType + '", "status":"INACTIVE"}}';

		$.ajax({
		type: "POST",
		url: 'device',
		data: deviceDetails,
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		success: function (data) {
		},
		error: function (msg) {
			alert(msg);
			alert(deviceDetails);
		}
	});
}

function addAlertDiv(name, description, priority){

	var newElem = document.createElement('div');
	newElem.className="field";

	var mainLabel = document.createElement('label');
	mainLabel.className="label";
	mainLabel.innerHTML="AlertType";

	var controlDiv = document.createElement('div');
	controlDiv.className="control";

	var nameLabel = document.createElement('label');
	nameLabel.className = "label is-small";
	nameLabel.innerHTML="Name";

	var descLabel = document.createElement('label');
	descLabel.className = "label is-small";
	descLabel.innerHTML="Short Description";

	var priorityLabel = document.createElement('label');
	priorityLabel.className = "label is-small";
	priorityLabel.innerHTML="Priority";

	var nameInput = document.createElement('input');
	nameInput.className = "input";
	nameInput.type = "text";
	if(name)nameInput.value=name;

	var descInput = document.createElement('input');
	descInput.className = "input";
	descInput.type = "text";
	if(description)descInput.value=description;

	var priorityInput = document.createElement('input');
	priorityInput.className = "input";
	priorityInput.type = "number";
	if(priority)priorityInput.value=priority;

	newElem.appendChild(mainLabel);
	newElem.appendChild(controlDiv);
	controlDiv.appendChild(nameLabel);
	controlDiv.appendChild(nameInput);
	controlDiv.appendChild(descLabel);
	controlDiv.appendChild(descInput);
	controlDiv.appendChild(priorityLabel);
	controlDiv.appendChild(priorityInput);

	document.getElementById("deviceAlert").appendChild(newElem);

}
