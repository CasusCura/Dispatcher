$(document).ready(function(){
		
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
});

function submitUpdate(){
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

function selectChange(thing){
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
