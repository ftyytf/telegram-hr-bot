const tg = window.Telegram.WebApp;
tg.ready();
tg.expand();

const answers = {};
let currentStep = 0;
const totalSteps = 5;

document.querySelectorAll(".btn").forEach(btn => {
    btn.addEventListener("click", () => {
        const key = btn.dataset.key;
        const value = btn.dataset.value;
        answers[key] = value;

        // Hide current question
        const current = document.querySelector(`.question[data-step="${currentStep}"]`);
        current.classList.add("hidden");

        currentStep++;

        if (currentStep < totalSteps) {
            // Show next question
            const next = document.querySelector(`.question[data-step="${currentStep}"]`);
            next.classList.remove("hidden");
        } else {
            // All done — send data to bot
            document.getElementById("result").classList.remove("hidden");
            tg.sendData(JSON.stringify(answers));
        }
    });
});
