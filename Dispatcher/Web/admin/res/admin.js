var service = 'wherever this is going';
var table;
$(document).ready(function(){

	table = $('#deviceTable').DataTable();
 
	$.ajax({
		type: "GET",
		url: service + '/devices/',
		data: "{}",
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		success: function (data) {
			$.each(data.Countries, function (i, item) {
				table.row.add([
				"devId","dev type","dev status","<a href=\"#\" class=\"btn btn-primary\">edit</a>"
				]).draw( true );
			});
					
		},
		error: function (msg) {
			//alert(msg.responseText);

			table.row.add([
			"devId","dev type1","dev status","<a href=\"PatientDevEdit.html?devId=devId\" class=\"btn btn-primary\">edit</a>"
			]).draw( true );
			table.row.add([
			"devId2","dev type2","dev status","<a href=\"PatientDevEdit.html?devId=devId2\" class=\"btn btn-primary\">edit</a>"
			]).draw( true );
			table.row.add([
			"devId3","dev type3","dev status","<a href=\"PatientDevEdit.html?devId=devId3\" class=\"btn btn-primary\">edit</a>"
			]).draw( true );

					
		}
	});
	
	
	
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

	table.clear();
	
	//TODO make ajax call to get all devices which match the filter (see onLoad for example)
	
	//TODO add all new values to table
	
	table.draw();
	alert(filter);
}
