var service = 'wherever this is going';

$(document).ready(function(){
	//TODO make ajax call to get this device's data, 
	//then populate all the inputs with the current values
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
