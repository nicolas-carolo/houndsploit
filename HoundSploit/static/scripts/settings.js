function checkForUpdates() {
    location.href = "/update"
}

function savePreferences() {
    var theme = document.getElementById("theme-selector").value;
    document.cookie = "theme=" + theme;
    alert("Your preferences have been updated");
    location.reload();
}

function getTheme(template) {
   if (getCookie("theme") == "dark" ) {
       document.write('<link href="/static/css/dark-theme/' + template + '" rel="stylesheet">');
   } else {
       document.write('<link href="/static/css/light-theme/' + template + '" rel="stylesheet">');
   }
}

function getCookie(cookie_name) {
    var cookie_string = RegExp(""+cookie_name+"[^;]+").exec(document.cookie);
    return decodeURIComponent(!!cookie_string ? cookie_string.toString().replace(/^[^=]+./,"") : "");
}