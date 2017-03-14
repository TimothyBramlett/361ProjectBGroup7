window.onload = function() {
    if (location.pathname === "/ben_console") {
         getBenAcctInfo();
         getPreferences();
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
function getPreferences() {
    var httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function() {
        if (this.readyState === 4) {
          if (this.status === 200) {
            var response = JSON.parse("[" + this.response + "]")[0];
            response = response[0]
            var tf = [false, true];
            document.getElementById('kosh').checked  = tf[response[0]];
            document.getElementById('glut').checked  = tf[response[1]];
            document.getElementById('vegan').checked  = tf[response[2]];
            document.getElementById('ovoveg').checked  = tf[response[3]];
            document.getElementById('lactoveg').checked  = tf[response[4]];
            document.getElementById('lactoovoveg').checked  = tf[response[5]];
            document.getElementById('pesc').checked  = tf[response[6]];
            document.getElementById('peanut').checked  = tf[response[7]];
            document.getElementById('tree').checked  = tf[response[8]];
            document.getElementById('milk').checked  = tf[response[9]];
            document.getElementById('egg').checked  = tf[response[10]];
            document.getElementById('wheat').checked  = tf[response[11]];
            document.getElementById('soy').checked  = tf[response[12]];
            document.getElementById('fish').checked  = tf[response[13]];
            document.getElementById('shellfish').checked  = tf[response[14]];
            document.getElementById('sesame').checked  = tf[response[15]];
          }
          else {
            // display error
          }
        }
    };
    
    httpRequest.open('GET', location.origin.concat("/preferences"));
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

//------------------------------------------------------------------------------
function savePreferences() {
    var httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function() {
        if (this.readyState === 4) {
          if (this.status === 200) {
            // it worked
          }
          else {
            // display error
          }
        }
    };
    
    httpRequest.open('POST', location.origin.concat("/save_preferences"));
    httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    var params = ''
    if (!document.getElementById('kosh').checked) {params += "kosh=0&";} else {params += "kosh=1&";}
    if (!document.getElementById('glut').checked) {params += "glut=0&";} else {params += "glut=1&";}
    if (!document.getElementById('vegan').checked) {params += "vegan=0&";} else {params += "vegan=1&";}
    if (!document.getElementById('ovoveg').checked) {params += "ovoveg=0&";} else {params += "ovoveg=1&";}
    if (!document.getElementById('lactoveg').checked) {params += "lactoveg=0&";} else {params += "lactoveg=1&";}
    if (!document.getElementById('lactoovoveg').checked) {params += "lactoovoveg=0&";} else {params += "lactoovoveg=1&";}
    if (!document.getElementById('pesc').checked) {params += "pesc=0&";} else {params += "pesc=1&";}
    if (!document.getElementById('peanut').checked) {params += "peanut=0&";} else {params += "peanut=1&";}
    if (!document.getElementById('tree').checked) {params += "tree=0&";} else {params += "tree=1&";}
    if (!document.getElementById('milk').checked) {params += "milk=0&";} else {params += "milk=1&";}
    if (!document.getElementById('egg').checked) {params += "egg=0&";} else {params += "egg=1&";}
    if (!document.getElementById('wheat').checked) {params += "wheat=0&";} else {params += "wheat=1&";}
    if (!document.getElementById('soy').checked) {params += "soy=0&";} else {params += "soy=1&";}
    if (!document.getElementById('fish').checked) {params += "fish=0&";} else {params += "fish=1&";}
    if (!document.getElementById('shellfish').checked) {params += "shellfish=0&";} else {params += "shellfish=1&";}
    if (!document.getElementById('sesame').checked) {params += "sesame=0";} else {params += "sesame=1";}
    httpRequest.send(params);
}
