window.onload = function() {
    if (location.pathname === "/ben_console") {
         getBenAcctInfo();
    }
    if (location.pathname === "/bus_console") {
         getBusAcctInfo();
    }
};

function getBenAcctInfo() {
    var httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function() {
        if (this.readyState === 4) {
          if (this.status === 200) {
            var response = this.response.replace('[','').replace(']','')
            response = response.split(',')
            document.getElementById('ben-acct-info').textContent = "First Name: " + response[0].replace(/"/g, '') + "\n";
            document.getElementById('ben-acct-info').textContent += "Last Name: " + response[1].replace(/"/g, '') + "\n";
            document.getElementById('ben-acct-info').textContent += "Street Addr: " + response[2].replace(/"/g, '') + "\n";
            document.getElementById('ben-acct-info').textContent += "City: " + response[3].replace(/"/g, '') + "\n";
            document.getElementById('ben-acct-info').textContent += "ST: " + response[4].replace(/"/g, '') + "\n";
            document.getElementById('ben-acct-info').textContent += "ZIP: " + response[5].replace(/"/g, '') + "\n";
            document.getElementById('ben-acct-info').textContent += "Number If Household: " + response[6];
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
            var response = this.response.replace('[','').replace(']','')
            response = response.split(',')
            document.getElementById('bus-acct-info').textContent = "Name: " + response[0].replace(/"/g, '') + "\n";
            document.getElementById('bus-acct-info').textContent += "Street Addr: " + response[1].replace(/"/g, '') + "\n";
            document.getElementById('bus-acct-info').textContent += "City: " + response[2].replace(/"/g, '') + "\n";
            document.getElementById('bus-acct-info').textContent += "ST: " + response[3].replace(/"/g, '') + "\n";
            document.getElementById('bus-acct-info').textContent += "ZIP: " + response[4].replace(/"/g, '');
          }
          else {
            // display error
          }
        }
    };
    
    httpRequest.open('GET', location.origin.concat("/bus_info"));
    httpRequest.send(null);
}