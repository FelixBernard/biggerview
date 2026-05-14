var dropdown = document.getElementById("bank");

window.onload = function() {
    // document.getElementById('singup-form').submit();
  
    event.preventDefault();
    
    const link = window.origin +'/api/get_banks';
    
    fetch(link, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "banks": "banks"})
    })
    .then(response => response.json())
    .then(data => {
        dropdown.innerHTML = '';
        let list = data.body.massage.datas;
        list.forEach(bank => {
            var option = document.createElement("option");
            option.value = bank["bankid"];
            option.text = bank["bankkonto"];
            dropdown.appendChild(option);
        });
    })
    .catch(error => console.error('Error:', error));
};