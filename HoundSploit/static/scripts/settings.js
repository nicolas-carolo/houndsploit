function checkForUpdates() {
    location.href = "/update"
}

function savePreferences() {
    var theme = document.getElementById("theme-selector").value;
    document.cookie = "theme=" + theme + "; expires=Tue, 31 Dec 2030 23:59:59 UTC";
    alert("Your preferences have been updated");
    location.reload();
}

function getTheme(template) {
   if (getCookie("theme") == "light" ) {
       document.write('<link href="/static/css/light-theme/' + template + '" rel="stylesheet">');
   } else {
       document.write('<link href="/static/css/dark-theme/' + template + '" rel="stylesheet">');
   }
}

function getThemeOptions() {
    if (getCookie("theme") == "dark" ) {
        document.write('<option value="dark" selected>Dark</option>');
        document.write('<option value="light">Light</option>');
    } else {
        document.write('<option value="dark">Dark</option>');
        document.write('<option value="light" selected>Light</option>');
    }
 }

function getCookie(cookie_name) {
    var cookie_string = RegExp(""+cookie_name+"[^;]+").exec(document.cookie);
    return decodeURIComponent(!!cookie_string ? cookie_string.toString().replace(/^[^=]+./,"") : "");
}