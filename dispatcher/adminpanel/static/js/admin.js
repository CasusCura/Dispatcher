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
			openDeviceModal(table.row( this ).data()[4]);
		}
	});

	table.column(4).visible(false);

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
					device.serial_number, device.devicetype, device.status, device.location, device.id
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
		data: "device_id=" + devId,
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		success: function (data) {
				document.getElementById("id").value=data.device.id;
				document.getElementById("devicetype").value=data.device.devicetype;
				document.getElementById("location").value=data.device.location;
				document.getElementById("status").value=data.device.status;
				document.getElementById("serial").value=data.device.serial_number;
		},
		error: function (msg) {
			alert(msg);
		}
	});
}

//POST updated details of a device to the service (or add a new device)
function updatePatientDev(){
	var devType = document.getElementById("devicetype").value;
	var status = document.getElementById("status").value;
	var location = document.getElementById("location").value;
	var serial = document.getElementById("serial").value;
	var id = document.getElementById("id").value;
	var deviceDetails = '{"device":{"used_by":"patient","serial":"'+serial+'","device_type":"'+ devType +'", "status":"'+ status +'","location":"'+ location +'","device_id":"'+id+'"}}';

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
	document.getElementById("DeviceEditModal").className="modal";
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

	var json = '{"device_type":{"device_type_id":"'+deviceTypeId+'",used_by":"patient","product_name":"'+devType+'","product_description":"'+desc+'"}}';

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
				alerts.push('{"device_type_id":"'+deviceTypeId+'","request_id":"'+name+'", "description":"'+description+'","priority":"'+priority+'"}');
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
			document.getElementById("manageDeviceTypesModal").className="modal";
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
		data: "device_type_id="+selectedDeviceId,
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
			document.getElementById("addDeviceModal").className="modal";
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
