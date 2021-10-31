function checkForUpdates() {
    location.href = "/update"
}

function savePreferences() {
    var current_db = getCookie("database")
    var theme = document.getElementById("theme-selector").value;
    var new_db = document.getElementById("db-selector").value;
    document.cookie = "theme=" + theme + "; expires=Tue, 31 Dec 2030 23:59:59 UTC";
    document.cookie = "database=" + new_db + "; expires=Tue, 31 Dec 2030 23:59:59 UTC";
    if (new_db == current_db) {
        alert("Your preferences have been updated");
        location.reload();
    } else if (new_db = "fixed-dates" && current_db == "exploitdb") {
        alert("Your preferences have been updated. Building the new database can take a while. You can follow the progress of the process from the terminal window ");
        location.href = "/fix-dates"
    } else {
        alert("Restore original ExploitDB database (to be implemented)");
        location.reload();
    }
    
}

function getTheme(template) {
   if (getCookie("theme") == "light" ) {
       document.write('<link href="/static/css/light-theme/' + template + '" rel="stylesheet">');
   } else {
       document.write('<link href="/static/css/dark-theme/' + template + '" rel="stylesheet">');
   }
}

function getThemeOptions() {
    if (getCookie("theme") == "light" ) {
        document.write('<option value="dark">Dark</option>');
        document.write('<option value="light" selected>Light</option>');
    } else {
        document.write('<option value="dark" selected>Dark</option>');
        document.write('<option value="light">Light</option>');
    }
 }

 function getDBOptions() {
    if (getCookie("database") == "fixed-dates" ) {
        document.write('<option value="exploitdb">ExploitDB</option>');
        document.write('<option value="fixed-dates" selected>ExploitDB (with dates fix)</option>');
    } else {
        document.write('<option value="exploitdb" selected>ExploitDB</option>');
        document.write('<option value="fixed-dates">ExploitDB (with dates fix)</option>');
    }
 }

function getCookie(cookie_name) {
    var cookie_string = RegExp(""+cookie_name+"[^;]+").exec(document.cookie);
    return decodeURIComponent(!!cookie_string ? cookie_string.toString().replace(/^[^=]+./,"") : "");
}