function makeSuggestedSearch(suggested_search) {
    document.getElementById("searched-text").value = suggested_search;
    document.getElementById("searcher-form").submit();
}