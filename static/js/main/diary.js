const button_show = document.getElementById('show-diary');
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
        table = document.getElementById('diary-table');
        table.innerHTML = '';
        let list = data.body.massage.datas;
        if (list.length == 0) {
            let row = table.insertRow();
            let cell = row.insertCell();
            cell.textContent = 'Leere Liste';
        } else {
            list.forEach(item => {
                
                let row = table.insertRow();
                
                for (let key in item) {
                    const isHeader = (item['date'] === 'date');
                    let cell = row.insertCell();
                    if (isHeader) {
                        cell.textContent = item[key];
                    } 
                    else if (key == 'active') {
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
                        let input = document.createElement('input');
                        input.type = 'text';
                        input.value = item[key];
                        input.className = 'table-input'; // Für Styling in CSS

                        // Optional: ID oder Name setzen, um Änderungen später zu speichern
                        input.dataset.key = key;
                        input.dataset.id = item[data.body.massage.primary_key];

                        // Update function
                        input.onblur = function () {
                            const newValue = this.value;
                            const fieldName = this.dataset.key;
                            const entryId = this.dataset.id;

                            fetch('/api/update_diary', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({
                                    "id": entryId,
                                    "field": fieldName,
                                    "value": newValue
                                })
                            })
                            .then(response => response.json())
                            .then(data => {
                                if (data.status === 'ok') {;
                                    this.style.transition = "0.5s"; // Sanfter Übergang
                                    this.style.boxShadow = "0 0 10px #1fff1f8d"; // Kurz grün aufleuchten lassen
                                    this.style.backgroundColor = "#1fff1f8d"; // Kurz grün aufleuchten lassen
                                    setTimeout(() => this.style.boxShadow = "none", 500);
                                    setTimeout(() => this.style.backgroundColor = "transparent", 500);
                                } else {
                                    this.style.transition = "0.5s"; // Sanfter Übergang
                                    this.style.boxShadow = "0 0 10px #ff1f1f8d"; // Kurz rot aufleuchten lassen
                                    this.style.backgroundColor = "#ff2a2a8d"; // Kurz rot aufleuchten lassen
                                    setTimeout(() => this.style.boxShadow = "none", 500);
                                    setTimeout(() => this.style.backgroundColor = "transparent", 500);
                                    console.error("Fehler beim Speichern:", data.msg);
                                }
                            })
                            .catch(err => {
                                console.error("Fehler beim Speichern:", err);
                                this.style.transition = "0.5s"; // Sanfter Übergang
                                this.style.boxShadow = "0 0 10px #ff1f1f8d"; // Kurz rot aufleuchten lassen
                                this.style.backgroundColor = "#ff2a2a8d"; // Kurz rot aufleuchten lassen
                                setTimeout(() => this.style.boxShadow = "none", 500);
                                setTimeout(() => this.style.backgroundColor = "transparent", 500);
                            });
                        };

                        cell.appendChild(input);
                    }
                }
                let buttonCell = row.insertCell();
                // damit die erste reihe kein button hat, funktioniert leider nicht für db's die keine id haben
                if (item['date'] == 'date'){
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