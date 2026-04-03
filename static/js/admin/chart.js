const path_button = document.getElementById("path-button");
const activity_button = document.getElementById("activity-button");
const relaod_button = document.getElementById("reload-button");
let ctx = document.getElementById('myChart');
let myChart = null;
let apiData_cache = null;
let apiData_requests = null;
let apiData_activity = null;

path_button.addEventListener('click', function() {
    const ctx = document.getElementById('myChart');

    // Funktion zum Laden der Daten
    function get_data_from_db() {
        const link = window.origin + '/api/nimda/iaw34nef/requests';

        fetch(link, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(apiData => {

            apiData = apiData.body.massage.datas;
            // Extrahiere Keys und Values aus dem Objekt
            const labels = apiData.map(item => item.useragent);
            const data = apiData.map(item => item.count);

            // Erstelle das Chart mit den geladenen Daten
            reload_chart('bar', labels ,'Activity', data, {
                beginAtZero: true,
                type: 'logarithmic'
            });
        })
        .catch(error => {
            console.error('Fehler beim Laden der Daten:', error);
        });
    }

    // Rufe die Funktion auf, um die Daten zu laden
    get_data_from_db();
});

activity_button.addEventListener('click', function() {
    const ctx = document.getElementById('myChart');

    // Funktion zum Laden der Daten
    function get_data_from_db() {
        const link = window.origin + '/api/nimda/iaw34nep/activity';

        fetch(link, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(apiData => {
            apiData = apiData.body.massage.datas;
            // Extrahiere Keys und Values aus dem Objekt
            const labels = apiData.map(item => item.hour);
            const data = apiData.map(item => item.request_count);

            // Erstelle das Chart mit den geladenen Daten
            reload_chart('line', labels ,'Activity', data, {
                beginAtZero: true
            });
        })
        .catch(error => {
            console.error('Fehler beim Laden der Daten:', error);
        });
    }

    // Rufe die Funktion auf, um die Daten zu laden
    get_data_from_db();
});

relaod_button.addEventListener('click', function() {
    if (myChart !== null) {
        myChart.destroy();
    }

    temp_path = path_button.classList.contains('active') ? '/api/nimda/iaw34nef/requests' : '/api/nimda/iaw34nep/activity';
    temp_type = path_button.classList.contains('active') ? 'bar' : 'line';

    get_data_from_db(temp_path);

    y = temp_path === '/api/nimda/iaw34nef/requests' ? {
        beginAtZero: true,
        type: 'logarithmic'
    } : {
        beginAtZero: true
    };

    reload_chart('line', ['Loading...'] ,'Loading...', apiData_cache, y);
});

function reload_chart(type, labels, label, data, y) {
    if (myChart !== null) {
        myChart.destroy();
    }
    myChart = new Chart(ctx, {
        type: type,
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y
            }
        }
    });
};

function get_data_from_db(path) {
    const link = window.origin + path;

    fetch(link, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(apiData => {

        apiData_cache = apiData.body.massage.datas;

    })
    .catch(error => {
        console.error('Fehler beim Laden der Daten:', error);
    });
}