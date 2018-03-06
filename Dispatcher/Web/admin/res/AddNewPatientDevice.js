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

function addNewDevice(){
	//post the details
	//navigate to patientDevEdit with ? being the new ids in success block
	//handle duplicate name in error block
}