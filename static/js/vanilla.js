window.onload = function() {
    if (location.pathname === "/ben_console") {
         getBenAcctInfo();
    }
    if (location.pathname === "/bus_console") {
         getBusAcctInfo();
         getFoodLoss();
    }
};

//------------------------------------------------------------------------------
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

//------------------------------------------------------------------------------
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

//------------------------------------------------------------------------------
function getFoodLoss() {
    var httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function() {
        if (this.readyState === 4) {
          if (this.status === 200) {
              
            // --- create title/header row -------------------------------------  
            row = document.createElement('tr');
            title = document.createElement('th'); title.innerHTML = 'Name'; row.appendChild(title);
            title = document.createElement('th'); title.innerHTML = 'Category'; row.appendChild(title);
            title = document.createElement('th'); title.innerHTML = 'Volume'; row.appendChild(title);
            title = document.createElement('th'); title.innerHTML = 'Units'; row.appendChild(title);
            title = document.createElement('th'); title.innerHTML = 'Quantity'; row.appendChild(title);
            title = document.createElement('th'); title.innerHTML = 'Sell By'; row.appendChild(title);
            title = document.createElement('th'); title.innerHTML = 'Best By'; row.appendChild(title);
            title = document.createElement('th'); title.innerHTML = 'Expiration'; row.appendChild(title);
            title = document.createElement('th'); title.colSpan = '2'; title.innerHTML = 'Modify Item'; row.appendChild(title);
            head = document.createElement('thead');
            head.appendChild(row);
            document.getElementById('foodlosses').appendChild(head);
        
            // --- create row with details for each item -----------------------  
            var response = JSON.parse("[" + this.response + "]")[0];
            for (i = 0; i < response.length; i++) {
                row = document.createElement('tr');
                for (j = 1; j < response[i].length; j++) {
                    cell = document.createElement('td');
                    cell.innerHTML = response[i][j];
                    row.appendChild(cell);
                }
                cell = document.createElement('td');
                button = '<input type="button" value="Update" class="btn btn-primary" disabled>';
                cell.innerHTML = button;
                row.appendChild(cell);
                cell = document.createElement('td');
                button = '<input type="button" value="Delete" class="btn btn-primary" onclick="deleteFoodLossItem(' + response[i][0] + ')">';
                cell.innerHTML = button;
                row.appendChild(cell);
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

//------------------------------------------------------------------------------
function deleteFoodLossItem(item_id) {
    var httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function() {
        if (this.readyState === 4) {
          if (this.status === 200) {
            var element = document.getElementById('foodlosses');
            while (element.firstChild) {
                element.removeChild(element.firstChild);
            }
            getFoodLoss();
          }
          else {
            // display error
          }
        }
    };
    
    httpRequest.open('POST', location.origin.concat("/delete_item_from_table"));
    httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    var params = 'item_id=' + item_id + '&tablename=foodlosses'
    httpRequest.send(params);
}
