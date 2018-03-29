$(function() {
  document.getElementById("login").onclick = () => {
  	$.post("https://api.svh/nurse/login", { //TODO Can be changed?
  		uuid: document.getElementById("uuid").value
  	}).fail(function() {
		document.getElementById('responding').classList.remove('is-invisible');
		document.getElementById('pending').classList.remove('is-invisible');
		document.getElementById('nurseLogin').classList.remove('is-active');
  	}).done(function() {
	    alert("Invalid nurse UUID");
  	})
  }
});
