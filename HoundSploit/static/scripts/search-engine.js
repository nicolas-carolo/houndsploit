function makeSuggestedSearch(keywords) {
    document.getElementById("searched-text").value = keywords; 
    document.getElementById("searcher-form").submit();
}

function nextExploitsPage(latest_exploits_page) {
    // TODO add control on min and max page
    if (parseInt(document.getElementById("exploit-page-number").value) < parseInt(latest_exploits_page)){
        document.getElementById("current-view").value = "exploits"
        document.getElementById("exploit-page-number").value = parseInt(document.getElementById("exploit-page-number").value) + 1;
        document.getElementById("hid-e-page").value = document.getElementById("exploit-page-number").value;
        document.getElementById("searcher-form").submit();
    }
}

function previousExploitsPage() {
    if (parseInt(document.getElementById("exploit-page-number").value) > 1) {
        document.getElementById("current-view").value = "exploits"
        document.getElementById("exploit-page-number").value = parseInt(document.getElementById("exploit-page-number").value) - 1;
        document.getElementById("hid-e-page").value = document.getElementById("exploit-page-number").value;
        document.getElementById("searcher-form").submit();
    }
}

function goExploitsPage() {
    document.getElementById("current-view").value = "exploits"
    document.getElementById("exploit-page-number").value = document.getElementById("exploit-page-number").value;
    document.getElementById("hid-e-page").value = document.getElementById("exploit-page-number").value;
    document.getElementById("searcher-form").submit();
}

function goFirstExploitsPage() {
    document.getElementById("current-view").value = "exploits"
    document.getElementById("exploit-page-number").value = 1;
    goExploitsPage()
}

function goLastExploitsPage(latest_exploits_page) {
    document.getElementById("current-view").value = "exploits"
    document.getElementById("exploit-page-number").value = latest_exploits_page;
    goExploitsPage()
}
