const characterOptions = [
    { name: "P1", credit: 3 },
    { name: "H1", credit: 5 },
    { name: "H2", credit: 5 }
];

let selectedCharacters = [];
let totalCredits = 0;
const maxCredits = 21;

function initializeSelection() {
    const container = document.getElementById("character-options");

    characterOptions.forEach(char => {
        const optionDiv = document.createElement("div");
        optionDiv.classList.add("character-option");
        
        const name = document.createElement("span");
        name.textContent = `${char.name} - ${char.credit} credits`;
        optionDiv.appendChild(name);
        
        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.id = char.name;
        checkbox.value = char.credit;
        checkbox.onchange = handleCheckboxChange;
        optionDiv.appendChild(checkbox);
        
        container.appendChild(optionDiv);
    });
}

function handleCheckboxChange(event) {
    const checkbox = event.target;
    const charName = checkbox.id;
    const charCredit = parseInt(checkbox.value, 10);

    if (checkbox.checked) {
        if (totalCredits + charCredit > maxCredits) {
            alert("Exceeds maximum credit limit of 21.");
            checkbox.checked = false;
            return;
        }
        selectedCharacters.push(charName);
        totalCredits += charCredit;
    } else {
        selectedCharacters = selectedCharacters.filter(name => name !== charName);
        totalCredits -= charCredit;
    }

    updateCreditsDisplay();
}

function updateCreditsDisplay() {
    const display = document.getElementById("credits-display");
    display.textContent = `Total Credits: ${totalCredits}/${maxCredits}`;
}

function submitSelection() {
    if (selectedCharacters.length === 0) {
        alert("You must select at least one character.");
        return;
    }

    // Save selected characters and credits to local storage or send to server
    localStorage.setItem("selectedCharacters", JSON.stringify(selectedCharacters));
    localStorage.setItem("totalCredits", totalCredits);

    // Redirect to the main game page
    window.location.href = "index.html";
}

// Initialize the character selection page
initializeSelection();
