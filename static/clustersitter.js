function set_progress_bars() {
	let capacity = 0;
	let clusters = ["cluster1", "cluster2", "cluster3"];

	for (let i = 0; i < clusters.length; i++) {
		if (document.getElementById(clusters[i]).checked === true) {
			capacity += g_cluster_capacities[i];
		}
	}
	if (document.getElementById("max_people").innerHTML != "?") {
		document.getElementById("progress_max").style.width = (parseInt(document.getElementById("max_people").innerHTML) / capacity * 100).toFixed(1)+'%';
	}
	if (document.getElementById("subscribed_users").innerHTML != "?") {
		document.getElementById("progress_current").style.width = (parseInt(document.getElementById("subscribed_users").innerHTML) / capacity * 100).toFixed(1)+'%';
	}
}

function uncheck_clusters() {
	document.getElementById("cluster1").checked = false;
	document.getElementById("cluster2").checked = false;
	document.getElementById("cluster3").checked = false;
}

function set_fields(response) {
	if (response === null) {
		uncheck_clusters();
		document.getElementById("id").value = "";
		document.getElementById("date").value = "";
		document.getElementById("name").value = "";
		document.getElementById("cursus").value = "";
		document.getElementById("location").value = "";
		document.getElementById("subscribed_users").innerHTML = "?";
		document.getElementById("max_people").innerHTML = "?";
	}
	else {
		uncheck_clusters();
		document.getElementById("id").value = response.id;
		document.getElementById("date").value = response.begin_at.slice(0,10);
		document.getElementById("name").value = response.name;
		document.getElementById("cursus").value = response.cursus[0].name;
		document.getElementById("location").value = response.location;
		document.getElementById("subscribed_users").innerHTML = response.nbr_subscribers;
		document.getElementById("max_people").innerHTML = response.max_people;
		let clusters = ["cluster1", "cluster2", "cluster3"];
		for (c of response.location)
		{
			if (c === "1" || c === "2" || c === "3") {
				document.getElementById(clusters[parseInt(c) - 1]).checked = true;
			}
		}
	}
	set_progress_bars();
}

function get_exam(search_type) {
	let id = "-1";
	let date = "0";
	if (search_type === "id") {
		id = document.getElementById("id").value;
	}
	else {
		date = document.getElementById("date").value;
	}
	date = date || '0';

	let xhr = new XMLHttpRequest();
	xhr.open('GET', '/get_exam?date='+date+'&id='+id);
	xhr.onload = function() {
		if (xhr.status === 200) {
			response = JSON.parse(xhr.responseText);
			if (response.id === -1) {
				document.getElementById("error").innerHTML = "Couldn't find any exams for today, please give an event ID or date"
				response = null;
			}
			else {
				document.getElementById("error").innerHTML = "&nbsp;";
			}
		}
		else {
			document.getElementById("error").innerHTML = "Couldn't connect to the service";
			response = null;
		}
		set_fields(response);
	}
	xhr.send()
}

function assign_seats_onload() {
	let capacities = document.getElementsByClassName("cluster_capacity");
	for (let i = 0; i < capacities.length; i++) {
		capacities[i].innerHTML = g_cluster_capacities[i].toString();
	}
	get_exam();
}
