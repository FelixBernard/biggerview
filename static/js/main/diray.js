const button_show = document.getElementById('show-diray');
const button_today = document.getElementById('today');
var before_db = "";
var offset = 0;

button_show.addEventListener('click', (event) => {
    // document.getElementById('singup-form').submit();
  
    event.preventDefault();
    
    const link = window.origin +'/api/diary';
    
    fetch(link, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "offset": offset})
    })
    .then(response => response.json())
    .then(data => {
        table = document.getElementById('diray-table');
        table.innerHTML = '';
        let l = data.body.massage.datas;
        if (l.length == 0) {
            let row = table.insertRow();
            let cell = row.insertCell();
            cell.textContent = 'Leere Liste';
        } else {
            data.body.massage.datas.forEach(item => {
                let row = table.insertRow();
                for (let key in item) {
                    let cell = row.insertCell();
                    if (key == 'active') {
                        let box = document.createElement('div');
                        box.setAttribute('class', 'activ-box');
                        let a_box = document.createElement('div');
                        if (item['active'] == 1) {
                            a_box.setAttribute('class', 'status-indicator-green');
                            box.appendChild(a_box);
                            cell.appendChild(box);
                        } else if (item['active'] == 0) {
                            a_box.setAttribute('class', 'status-indicator-red');
                            box.appendChild(a_box);
                            cell.appendChild(box);
                        } else {
                            cell.textContent = item[key];
                        }
                    } else {
                        cell.textContent = item[key];
                    }
                }
                let buttonCell = row.insertCell();
                // damit die erste reihe kein button hat, funktioniert leider nicht für db's die keine id haben
                if (item['id'] == 'id'){
                    buttonCell.appendChild(document.createElement('p'));
                }
                else {
                    let button = document.createElement('button');
                    button.onclick = delete_out_of_db;
                    button.textContent = 'Löschen'
                    button.className = 'button';
                    // button.id = 'loeschen'
                    button.setAttribute('l_id', item[data.body.massage.primary_key]);
                    buttonCell.appendChild(button);
                }
                if (item['kind'] == 'INFO') {
                    row.setAttribute('class', 'infoclass')
                } else if (item['kind'] == 'WARN') {
                    row.setAttribute('class', 'warningclass')
                } else if (item['kind'] == 'ERR') {
                    row.setAttribute('class', 'errclass') 
                }
                // } else if (item['active'] == 1) {
                //     console.log("aktive");
                // }
                
            });
        }
    })
    .catch(error => console.error('Error:', error));
});

button_today.addEventListener('click', (event) => {
    // document.getElementById('singup-form').submit();
  
    event.preventDefault();
    
    const link = window.origin +'/api/today';
    
    fetch(link, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "offset": offset})
    })
    .then(response => response.json())
    .then(data => {
        button_show.click();
    })
    .catch(error => console.error('Error:', error));
});


function delete_out_of_db(event) {
    // console.log('delete', event.id, event, event.target.closest('.button'));
    bu = event.target.closest('.button');
    console.log(bu.getAttribute('l_id'));
}

function add_offset () {
    offset += 1;
}

function minus_offset () {
    if (offset >= 1)
        offset -= 1;
}

function zero_offset() {
    offset = 0;
}

window.onload = function() {
    console.log("window loaded");
    button_show.click();
}