var service = 'wherever this is going';

$(document).ready(function(){

	var table = $('#deviceTable').DataTable();
 
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
			"devId","dev type1","dev status","<a href=\"#\" class=\"btn btn-primary\">edit</a>"
			]).draw( true );
			table.row.add([
			"devId2","dev type2","dev status","<a href=\"#\" class=\"btn btn-primary\">edit</a>"
			]).draw( true );
			table.row.add([
			"devId3","dev type3","dev status","<a href=\"#\" class=\"btn btn-primary\">edit</a>"
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