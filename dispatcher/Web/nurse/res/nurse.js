let uuid = "";
let failed = false;

let showRepondingModal = issue => {
  document.getElementById('responding-modal-title').textContent = issue.name;
  document.getElementById('responding-modal-description').textContent = issue.description;
  document.getElementById('responding-modal-eta').textContent = issue.status;
  document.getElementById('responding-modal-submit').onclick = (issue => {
    return () => {
      //TODO Mark the issue as resolved with the API

      //refresh the lists
      main();
    };
  })(issue);
  document.getElementById('responding-modal-cancel').onclick = (issue => {
    return () => {
      //TODO Mark the issue as cancelled with the API

      //refresh the lists
      main();
    };
  })(issue);
  document.getElementById('responding-modal').classList.add('is-active');
}

let showPendingModal = issue => {
  document.getElementById('pending-modal-title').textContent = issue.name;
  document.getElementById('pending-modal-description').textContent = issue.description;
  document.getElementById('pending-modal-submit').onclick = (issue => {
    return () => {
      //TODO submit the issue to the API

      //Refresh the lists
      main();
    };
  })(issue);
  document.getElementById('pending-modal').classList.add('is-active');
}

let buildCard = (issue, responding) => {
      let copy = document.getElementById("copy").cloneNode(true);
      copy.removeAttribute('id');
      copy.classList.remove('is-invisible');
      let notificationNode = copy.getElementsByClassName('notification')[0];
      if (responding) {
        notificationNode.classList.add('is-warning');
      } else {
        notificationNode.classList.add('is-danger');
      }
      copy.getElementsByClassName('room-number')[0].textContent = issue.location;
      copy.getElementsByClassName('issue-type')[0].textContent = issue.name;
      copy.onclick = ((responding, issue) => {
        return () => {
          responding ? showRepondingModal(issue) : showPendingModal(issue);
        };
      })(responding, issue);
      return copy;
}

let removeChildren = node => {
  while (node.firstChild) {
    node.removeChild(node.firstChild);
  }
}

let main = () => {
  if (failed || document.getElementsByClassName('is-active').length > 0) {
    return;
  }
  $.ajax({
    method: "POST",
    url: "http://dsadsad.dsadsa",
    data: {
      'uuid': uuid
    },
    dataType: "json",
  }).done(results => {
    let responding = document.getElementById("responding-tiles");
    let pending = document.getElementById("pending-tiles");

    removeChildren(responding);
    removeChildren(pending);

    results.data.queued_issues.forEach(issue => {
      let card = buildCard(issue, true);
      responding.appendChild(card);
    });

    results.data.pending_issues.forEach(issue => {
      let card = buildCard(issue, false)
      pending.appendChild(card);
    });
  }).fail(()=> {
    alert("Failed to retrieve issues. Please Refresh.")
  });
};

$(function() {

  document.getElementById("responding-modal-close").onclick = () => {
    document.getElementById('responding-modal').classList.remove('is-active');
  };

  document.getElementById("responding-modal-close-upper").onclick = () => {
    document.getElementById('responding-modal').classList.remove('is-active');
  };

  document.getElementById("pending-modal-close").onclick = () => {
    document.getElementById('pending-modal').classList.remove('is-active');
  };

  document.getElementById("pending-modal-close-upper").onclick = () => {
    document.getElementById('pending-modal').classList.remove('is-active');
  };

  document.getElementById("login").onclick = button => {
  	let uuid = document.getElementById("uuid").value;
    $.ajax({
      method: "POST",
      url: "http://fdsfsd.fdsf",
  		data: {
        'uuid': uuid
      },
      dataType: "json",
  	}).fail(() => {
      document.getElementById('responding').classList.remove('is-invisible');
      document.getElementById('pending').classList.remove('is-invisible');
      document.getElementById('nurseLogin').classList.remove('is-active');
      setInterval(main, 5000);
    }).done(() => {
      alert("Invalid nurse UUID");
    });
  }
});
