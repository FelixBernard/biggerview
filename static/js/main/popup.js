function get_cookie(name) {
    let cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i].trim();
        // Prüfen, ob der Cookie-Name mit dem gegebenen Namen übereinstimmt
        if (cookie.startsWith(name + '=')) {
            return cookie.substring(name.length + 1);
        }
    }
    return null;
}

function check_for_cookie(event) {
    if (get_cookie('firstacces') == 'y'){
        document.cookie = "firstacces=false; path=/;";
        document.getElementById("cookie").style.display = 'flex';
        document.getElementById("popup").style.display = 'flex';
    }
    else if (get_cookie('user').length == 0) {
        document.getElementById("cookie").style.display = 'flex';
        document.getElementById("popup").style.display = 'flex';
    }
}

function desappir_popup(event) {
    document.getElementById("cookie").style.display = 'none';
    document.getElementById("popup").style.display = 'none';
}

window.addEventListener('load', function() {
    check_for_cookie();
});