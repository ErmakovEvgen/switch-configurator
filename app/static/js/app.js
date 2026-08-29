const form = document.getElementById("config-form");

const fioInput = document.getElementById("fio");
const apartmentInput = document.getElementById("apartment");
const portInput = document.getElementById("port");
const vlanInput = document.getElementById("vlan");
const ipInput = document.getElementById("ip");
const ringSwitchInput = document.getElementById("ring-switch");
const iptvInput = document.getElementById("iptv");

const generateButton =
    document.getElementById("generate-button");

const clearButton =
    document.getElementById("clear-button");

const resultBlock =
    document.getElementById("result");

const scenarioBlock =
    document.getElementById("scenario");

const formError =
    document.getElementById("form-error");

const ciscoConfig =
    document.getElementById("cisco-config");

const dlinkConfig =
    document.getElementById("dlink-config");

const copyAllButton =
    document.getElementById("copy-all-button");


/*
 * Определяем сценарий на frontend.
 *
 * Это только визуальная подсказка.
 * Настоящее определение сценария
 * всё равно выполняется backend.
 */
function updateScenario() {

    const hasIp =
        ipInput.value.trim() !== "";

    const hasRing =
        ringSwitchInput.value.trim() !== "";

    if (hasIp) {

        scenarioBlock.textContent =
            "Сценарий: IP-клиент";

        scenarioBlock.classList.remove("hidden");

        vlanInput.disabled = false;
        ringSwitchInput.disabled = true;

        return;
    }

    if (hasRing) {

        scenarioBlock.textContent =
            "Сценарий: Клиент в кольце";

        scenarioBlock.classList.remove("hidden");

        vlanInput.disabled = true;
        ringSwitchInput.disabled = false;

        return;
    }

    scenarioBlock.textContent =
        "Сценарий: Обычный клиент";

    scenarioBlock.classList.remove("hidden");

    vlanInput.disabled = false;
    ringSwitchInput.disabled = false;
}


/*
 * Когда вводится IP —
 * отключаем кольцо.
 */
ipInput.addEventListener(
    "input",
    updateScenario
);


/*
 * Когда вводится коммутатор кольца —
 * отключаем IP.
 */
ringSwitchInput.addEventListener(
    "input",
    updateScenario
);


/*
 * Генерация конфигурации.
 */
form.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();

        hideError();

        const data = {

            fio: fioInput.value.trim(),

            apartment:
                Number(apartmentInput.value),

            port:
                Number(portInput.value),

            vlan:
                vlanInput.value.trim() === ""
                    ? null
                    : Number(vlanInput.value),

            ip:
                ipInput.value.trim() === ""
                    ? null
                    : ipInput.value.trim(),

            ring_switch:
                ringSwitchInput.value.trim() === ""
                    ? null
                    : Number(ringSwitchInput.value),

            iptv:
                iptvInput.checked,
        };


        generateButton.disabled = true;

        generateButton.textContent =
            "Формирование...";


        try {

            const response = await fetch(
                "/api/config",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json",
                    },

                    body: JSON.stringify(data),
                }
            );


            const result =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    result.detail ||
                    "Не удалось сформировать конфигурацию"
                );
            }


            showResult(result);

        } catch (error) {

            showError(error.message);

        } finally {

            generateButton.disabled = false;

            generateButton.textContent =
                "Сформировать конфигурацию";
        }
    }
);


/*
 * Показываем результат.
 */
function showResult(result) {

    ciscoConfig.textContent =
        result.cisco || "Конфигурация отсутствует";

    dlinkConfig.textContent =
        result.dlink || "Конфигурация отсутствует";

    resultBlock.classList.remove("hidden");

    window.scrollTo({
        top: resultBlock.offsetTop - 20,
        behavior: "smooth",
    });
}


/*
 * Очистка формы.
 */
clearButton.addEventListener(
    "click",
    function () {

        form.reset();

        vlanInput.disabled = false;
        ringSwitchInput.disabled = false;

        resultBlock.classList.add("hidden");

        scenarioBlock.classList.add("hidden");

        hideError();
    }
);


/*
 * Копирование конкретного конфига.
 */
document
    .querySelectorAll(".copy-button")
    .forEach(function (button) {

        button.addEventListener(
            "click",
            async function () {

                const target =
                    document.getElementById(
                        button.dataset.target
                    );

                await copyText(
                    target.textContent
                );

                const originalText =
                    button.textContent;

                button.textContent =
                    "Скопировано";

                setTimeout(
                    function () {
                        button.textContent =
                            originalText;
                    },
                    1200
                );
            }
        );
    });


/*
 * Копирование обоих конфигов.
 */
copyAllButton.addEventListener(
    "click",
    async function () {

        const text =
            "=== CISCO ===\n\n" +
            ciscoConfig.textContent +
            "\n\n" +
            "=== D-LINK ===\n\n" +
            dlinkConfig.textContent;

        await copyText(text);

        const originalText =
            copyAllButton.textContent;

        copyAllButton.textContent =
            "Скопировано";

        setTimeout(
            function () {
                copyAllButton.textContent =
                    originalText;
            },
            1200
        );
    }
);


/*
 * Clipboard.
 */
async function copyText(text) {

    await navigator.clipboard.writeText(text);
}


/*
 * Ошибка.
 */
function showError(message) {

    formError.textContent = message;

    formError.classList.remove("hidden");
}


function hideError() {

    formError.textContent = "";

    formError.classList.add("hidden");
}


/*
 * Начальное состояние.
 */
updateScenario();