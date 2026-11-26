// Слушаем сообщения от popup.js
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "insertText") {
        const text = request.text;

        // Ищем поле ввода в ВК (это поле обычно имеет класс "_im_text" или contenteditable="true")
        // В ВК очень сложная верстка, поэтому ищем по атрибуту contenteditable
        const messageInput = document.querySelector('[contenteditable="true"]');

        if (messageInput) {
            messageInput.focus();
            // Вставляем текст
            document.execCommand("insertText", false, text);
        } else {
            alert(
                "Не удалось найти поле ввода ВК. Убедитесь, что вы открыли диалог!",
            );
        }
    }
});
