function makeSuggestedSearch(keywords) {
    document.getElementById("searched-text").value = keywords; 
    document.getElementById("searcher-form").submit();
}

function nextExploitsPage() {
    // TODO add control on min and max page
    document.getElementById("exploit-page-number").value = parseInt(document.getElementById("exploit-page-number").value) + 1;
    document.getElementById("hid-e-page").value = document.getElementById("exploit-page-number").value;
    document.getElementById("searcher-form").submit();
}

function previousExploitsPage() {
    // TODO add control on min and max page
    document.getElementById("exploit-page-number").value = parseInt(document.getElementById("exploit-page-number").value) - 1;
    document.getElementById("hid-e-page").value = document.getElementById("exploit-page-number").value;
    document.getElementById("searcher-form").submit();
}