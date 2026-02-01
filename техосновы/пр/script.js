document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("preRegisterForm");
    const messageBox = document.getElementById("formMessage");

    const showError = (name, text) => {
        const fieldError = form.querySelector(`.form__error[data-for="${name}"]`);
        if (fieldError) fieldError.textContent = text || "";
    };

    const clearErrors = () => {
        form.querySelectorAll(".form__error").forEach(el => el.textContent = "");
        if (messageBox) {
            messageBox.textContent = "";
            messageBox.style.color = "";
        }
    };

    const validateEmail = (email) => {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email.trim());
    };

    const validatePhone = (phone) => {
        const clean = phone.replace(/[^\d+]/g, "");
        return clean.length >= 10; // простая проверка
    };

    form.addEventListener("submit", (e) => {
        e.preventDefault();
        clearErrors();

        const name = form.name.value.trim();
        const phone = form.phone.value.trim();
        const email = form.email.value.trim();
        const agree = form.agree.checked;

        let valid = true;

        if (!name) {
            showError("name", "Пожалуйста, укажите имя.");
            valid = false;
        }

        if (!phone) {
            showError("phone", "Укажите телефон для связи.");
            valid = false;
        } else if (!validatePhone(phone)) {
            showError("phone", "Похоже, номер телефона указан некорректно.");
            valid = false;
        }

        if (!email) {
            showError("email", "Введите email.");
            valid = false;
        } else if (!validateEmail(email)) {
            showError("email", "Укажите корректный email.");
            valid = false;
        }

        if (!agree) {
            showError("agree", "Необходимо согласие на обработку персональных данных.");
            valid = false;
        }

        if (!valid) return;

        // Здесь вместо реальной отправки имитируем успешную заявку
        form.reset();
        if (messageBox) {
            messageBox.textContent = "Спасибо! Ваша заявка отправлена. Мы свяжемся с вами при открытии доступа.";
            messageBox.style.color = "#22c55e";
        }
    });
});
