
const textInput = document.getElementById("qr-data");
const characterCount = document.getElementById("character-count");

function updateCharacterCount() {
    characterCount.textContent = textInput.value.length;
}

textInput.addEventListener("input", updateCharacterCount);
updateCharacterCount();
