// Для Chrome/Яндекс
if (typeof chrome !== "undefined" && chrome.action) {
    chrome.action.onClicked.addListener(() => {
        chrome.tabs.create({ url: chrome.runtime.getURL("popup/popup.html") });
    });
}
// Для Firefox
else if (typeof browser !== "undefined" && browser.action) {
    browser.action.onClicked.addListener(() => {
        browser.tabs.create({
            url: browser.runtime.getURL("popup/popup.html"),
        });
    });
}
