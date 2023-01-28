function makeSuggestedSearch(keywords) {
    document.getElementById("searched-text").value = keywords; 
    document.getElementById("searcher-form").submit();
}

function nextExploitsPage(last_exploits_page) {
    if (parseInt(document.getElementById("exploit-page-number").value) < parseInt(last_exploits_page)){
        document.getElementById("current-view").value = "exploits";
        document.getElementById("exploit-page-number").value = parseInt(document.getElementById("exploit-page-number").value) + 1;
        document.getElementById("hid-e-page").value = document.getElementById("exploit-page-number").value;
        document.getElementById("searcher-form").submit();
    }
}

function previousExploitsPage() {
    if (parseInt(document.getElementById("exploit-page-number").value) > 1) {
        document.getElementById("current-view").value = "exploits";
        document.getElementById("exploit-page-number").value = parseInt(document.getElementById("exploit-page-number").value) - 1;
        document.getElementById("hid-e-page").value = document.getElementById("exploit-page-number").value;
        document.getElementById("searcher-form").submit();
    }
}

function goExploitsPage() {
    document.getElementById("current-view").value = "exploits";
    document.getElementById("exploit-page-number").value = document.getElementById("exploit-page-number").value;
    document.getElementById("hid-e-page").value = document.getElementById("exploit-page-number").value;
    document.getElementById("searcher-form").submit();
}

function goFirstExploitsPage() {
    document.getElementById("current-view").value = "exploits";
    document.getElementById("exploit-page-number").value = 1;
    goExploitsPage()
}

function goLastExploitsPage(last_exploits_page) {
    document.getElementById("current-view").value = "exploits";
    document.getElementById("exploit-page-number").value = last_exploits_page;
    goExploitsPage()
}

function nextShellcodesPage(last_shellcodes_page) {
    if (parseInt(document.getElementById("shellcode-page-number").value) < parseInt(last_shellcodes_page)){
        document.getElementById("current-view").value = "shellcodes";
        document.getElementById("shellcode-page-number").value = parseInt(document.getElementById("shellcode-page-number").value) + 1;
        document.getElementById("hid-s-page").value = document.getElementById("shellcode-page-number").value;
        document.getElementById("searcher-form").submit();
    }
}

function previousShellcodesPage() {
    if (parseInt(document.getElementById("shellcode-page-number").value) > 1) {
        document.getElementById("current-view").value = "shellcodes";
        document.getElementById("shellcode-page-number").value = parseInt(document.getElementById("shellcode-page-number").value) - 1;
        document.getElementById("hid-s-page").value = document.getElementById("shellcode-page-number").value;
        document.getElementById("searcher-form").submit();
    }
}

function goShellcodesPage() {
    document.getElementById("current-view").value = "shellcodes"
    document.getElementById("shellcode-page-number").value = document.getElementById("shellcode-page-number").value;
    document.getElementById("hid-s-page").value = document.getElementById("shellcode-page-number").value;
    document.getElementById("searcher-form").submit();
}

function goFirstShellcodesPage() {
    document.getElementById("current-view").value = "shellcodes";
    document.getElementById("shellcode-page-number").value = 1;
    goShellcodesPage()
}

function goLastShellcodesPage(latest_shellcode_page) {
    document.getElementById("current-view").value = "shellcodes";
    document.getElementById("shellcode-page-number").value = latest_shellcode_page;
    goShellcodesPage()
}

function resetPages() {
    document.getElementById("current-view").value = "";
    document.getElementById("exploit-page-number").value = 1;
    document.getElementById("hid-e-page").value = document.getElementById("exploit-page-number").value;
    document.getElementById("shellcode-page-number").value = 1;
    document.getElementById("hid-s-page").value = document.getElementById("shellcode-page-number").value;
}

function sortResultsBy() {
    document.getElementById("sorting-type").value = document.getElementById("sort-by-selector").value;
    resetPages();
    document.getElementById("searcher-form").submit();
}

function goFirstBookmarksPage() {
    document.getElementById("bookmark-page-number").value = 1;
    goBookmarksPage()
}

function goLastBookmarksPage(latest_bookmarks_page) {
    document.getElementById("bookmark-page-number").value = latest_bookmarks_page;
    goBookmarksPage()
}

function goBookmarksPage() {
    document.getElementById("bookmark-page-number").value = document.getElementById("bookmark-page-number").value;
    document.getElementById("hid-b-page").value = document.getElementById("bookmark-page-number").value;
    document.getElementById("searcher-form").submit();
}

function nextBookmarksPage(latest_bookmarks_page) {
    if (parseInt(document.getElementById("bookmark-page-number").value) < parseInt(latest_bookmarks_page)){
        document.getElementById("bookmark-page-number").value = parseInt(document.getElementById("bookmark-page-number").value) + 1;
        document.getElementById("hid-b-page").value = document.getElementById("bookmark-page-number").value;
        document.getElementById("searcher-form").submit();
    }
}

function previousBookmarksPage() {
    if (parseInt(document.getElementById("bookmark-page-number").value) > 1) {
        document.getElementById("bookmark-page-number").value = parseInt(document.getElementById("bookmark-page-number").value) - 1;
        document.getElementById("hid-b-page").value = document.getElementById("bookmark-page-number").value;
        document.getElementById("searcher-form").submit();
    }
}