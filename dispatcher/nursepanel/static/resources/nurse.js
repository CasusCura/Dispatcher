const base = "/nurse"
let uuid = "";
let failed = false;

let showRepondingModal = issue => {
  document.getElementById('responding-modal-title').textContent = issue.name;
  document.getElementById('responding-modal-description').textContent = issue.description;
  document.getElementById('responding-modal-eta').textContent = issue.status;

  document.getElementById('responding-modal-submit').onclick = (issue => {
    return () => {
      $.ajax({
        method: "POST",
        url: `${base}/close`,
        data: JSON.stringify({
          'nurse_id': uuid,
          'issue_id': issue.id
        }),
        dataType: "json",
      }).done(() => {
        document.getElementById('responding-modal').classList.remove('is-active');;
      }).fail(() => {
        console.log("Error communicating with the server, please try again later.");
      });

      //refresh the lists
      main();
    };
  })(issue);

  document.getElementById('responding-modal-cancel').onclick = (issue => {
    return () => {
  /*    $.ajax({
        method: "POST",
        url: `${base}/close`,
        data: JSON.stringify({
          'issue_id': issue.id,
          'nurse_id': uuid,
        }),
        dataType: "json",
      }).done(() => {
        document.getElementById('responding-modal').classList.remove('is-active');;
      }).fail(() => {
        console.log("Error communicating with the server, please try again later.");
      });
*/
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
      $.ajax({
        method: "POST",
        url: `${base}/response`,
        data: JSON.stringify({'response': {
          'issue_id': issue.id,
          'nurse_id': uuid,
          'eta': document.getElementById('pending-modal-eta').value,
          'data': {}
        }}),
        dataType: "json",
      }).done(() => {
        document.getElementById('pending-modal').classList.remove('is-active');;
      }).fail(() => {
        console.log("Error communicating with the server, please try again later.");
      });


      //Refresh the lists
      main();
    };
  })(issue);
  document.getElementById('pending-modal').classList.add('is-active');
}

let buildCard = (issue, responding) => {
      console.log(issue)
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
    method: "GET",
    url: `${base}/issues`,
    data: {
      'uuid': uuid
    }
  }).done(results => {
    let responding = document.getElementById("responding-tiles");
    let pending = document.getElementById("pending-tiles");

    removeChildren(responding);
    removeChildren(pending);

    results.my_queued_issues.forEach(issue => {
      let card = buildCard(issue, true);
      responding.appendChild(card);
    });

    results.pending_issues.forEach(issue => {
      let card = buildCard(issue, false)
      pending.appendChild(card);
    });
  }).fail(()=> {
    console.log("Failed to retrieve issues. Please Refresh.")
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
  	let data = {
      uuid: document.getElementById("uuid").value,
      ran: 5
    };
    $.ajax({
      method: "POST",
      url: `${base}/login`,
  		data: JSON.stringify(data),
      contentType: "application/json; charset=utf-8",
      dataType: "json",
  	}).done(() => {
      uuid = document.getElementById("uuid").value,
      document.getElementById('responding').classList.remove('is-invisible');
      document.getElementById('pending').classList.remove('is-invisible');
      document.getElementById('nurseLogin').classList.remove('is-active');
      setInterval(main, 5000);
    }).fail(() => {
      console.log("Invalid nurse UUID");
    });
  }
});
