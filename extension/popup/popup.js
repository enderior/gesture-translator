document.getElementById("uploadBtn").addEventListener("click", async () => {
    const fileInput = document.getElementById("videoFile");
    const statusDiv = document.getElementById("status");
    const resultDiv = document.getElementById("result");

    if (!fileInput.files.length) {
        statusDiv.innerText = "Пожалуйста, выберите файл!";
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("file", file);

    statusDiv.innerText = "Отправка на сервер...";
    resultDiv.innerText = "";
    document.getElementById("uploadBtn").disabled = true;

    try {
        const response = await fetch("http://localhost:8000/api/jobs", {
            method: "POST",
            body: formData,
        });
        const data = await response.json();

        if (data.job_id) {
            statusDiv.innerText = "Сервер обрабатывает видео...";

            setTimeout(async () => {
                const res = await fetch(
                    `http://localhost:8000/api/jobs/${data.job_id}`,
                );
                const result = await res.json();

                statusDiv.innerText = "Успешно!";
                resultDiv.innerText = `Распознанный текст: ${result.text}`;

                // Вывод в консоль, как просил наставник
                console.log("=== РЕЗУЛЬТАТ ОБРАБОТКИ ===");
                console.log("Глоссы:", result.glosses);
                console.log("Текст:", result.text);

                document.getElementById("uploadBtn").disabled = false;
            }, 1000);
        }
    } catch (error) {
        statusDiv.innerText = "Ошибка: Бэкенд не отвечает. Запущен ли Uvicorn?";
        console.error("Ошибка соединения:", error);
        document.getElementById("uploadBtn").disabled = false;
    }
});
