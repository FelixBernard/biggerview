const button = document.getElementById('login-button');

button.addEventListener('click', (event) => {
  // document.getElementById('login-form').submit();
    event.preventDefault();

    const email = document.getElementById('textbox_e-mail').value;
    const password = document.getElementById('textbox_password').value;

    const link = window.origin + '/api/login';
    fetch(link, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "e-mail": email, "password": password })
    })

    .then(response => response.json())
    .then(data => {
        const side = data.body.url;
        const cookie = data.body.cookie;
        console.log(side);

        if (data.body.status == "error"){
            window.alert(data.body.massage);
        }
        else{
            let path = side;
            // document.cookie = "user=" + cookie;
            window.location.replace(path);
        }
        
        });
});

