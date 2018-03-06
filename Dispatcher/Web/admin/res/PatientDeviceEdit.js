var service = 'wherever this is going';

$(document).ready(function(){
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
})



function updatePatientDev(){
	alert(getQueryVariable("devId"));
	alert("send to service");
	
	//TODO ajax data to service
	
	location.href="admin.html";
}	



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
