window.onload = function() {
    if (location.pathname === "/ben_console") {
         getBenAcctInfo();
    }
    if (location.pathname === "/bus_console") {
         getBusAcctInfo();
         getFoodLoss();
    }
};

function getBenAcctInfo() {
    var httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function() {
        if (this.readyState === 4) {
          if (this.status === 200) {
            var response = JSON.parse("[" + this.response + "]")[0];
            document.getElementById('fName').innerHTML = response[0].replace(/"/g, '');
            document.getElementById('lName').innerHTML = response[1].replace(/"/g, '');
            document.getElementById('addr').innerHTML = response[2].replace(/"/g, '');
            document.getElementById('city').innerHTML = response[3].replace(/"/g, '');
            document.getElementById('ST').innerHTML = response[4].replace(/"/g, '');
            document.getElementById('zip').innerHTML = response[5].replace(/"/g, '');
            document.getElementById('nHouse').innerHTML = response[6];
          }
          else {
            // display error
          }
        }
    };
    
    httpRequest.open('GET', location.origin.concat("/ben_info"));
    httpRequest.send(null);
}

function getBusAcctInfo() {
    var httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function() {
        if (this.readyState === 4) {
          if (this.status === 200) {
            var response = JSON.parse("[" + this.response + "]")[0];
            document.getElementById('name').innerHTML = response[0].replace(/"/g, '');
            document.getElementById('addr').innerHTML = response[1].replace(/"/g, '');
            document.getElementById('city').innerHTML = response[2].replace(/"/g, '');
            document.getElementById('ST').innerHTML = response[3].replace(/"/g, '');
            document.getElementById('zip').innerHTML = response[4].replace(/"/g, '');
          }
          else {
            // display error
          }
        }
    };
    
    httpRequest.open('GET', location.origin.concat("/bus_info"));
    httpRequest.send(null);
}

function getFoodLoss() {
    var httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function() {
        if (this.readyState === 4) {
          if (this.status === 200) {
            var response = JSON.parse("[" + this.response + "]")[0];
            for (i = 0; i < response.length; i++) {
                row = document.createElement('tr');
                for (j = 0; j < response[i].length; j++) {
                    cell = document.createElement('td');
                    cell.innerHTML = response[i][j];
                    row.appendChild(cell);
                }
                document.getElementById('foodlosses').appendChild(row);
            }
          }
          else {
            // display error
          }
        }
    };
    
    httpRequest.open('GET', location.origin.concat("/food_loss"));
    httpRequest.send(null);
}