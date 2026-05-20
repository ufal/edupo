
window.onpagehide = (event) => {
    document.querySelectorAll('input[type="submit"][disabled]').forEach(button => { button.disabled = false; button.value=button.title });
};

