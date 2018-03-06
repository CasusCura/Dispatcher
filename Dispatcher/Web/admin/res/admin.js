var service = 'wherever this is going';
var table;
$(document).ready(function(){

	table = $('#deviceTable').DataTable();
	filterTable("inUse");
	$('#deviceTable tbody').on( 'click', 'tr', function () {
		if ( $(this).hasClass('selected') ) {
			$(this).removeClass('selected');
		} else {
			table.$('tr.selected').removeClass('selected');
			$(this).addClass('selected');
		}
	});
})

function filterTable(filter){

	if(event){
			//highlight the clicked button
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
					device.deviceId,device.deviceType,device.deviceStatus,"<a href=\"PatientDevEdit.html?devId="+device.deviceId+"\" class=\"btn btn-primary\">edit</a>"
				]);
			});
			table.draw();
		}
	});
	table.draw();
}
