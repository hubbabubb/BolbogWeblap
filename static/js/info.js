function highlightDescription() {
    const descriptions = document.getElementsByClassName("description");

    for (let description of descriptions) {
        description.innerHTML = highlightQuotes(description.innerText);
    }
}

function highlightQuotes(text) {
    let newText = "";
    let quoteStart = false;

    for (let char of text) {
        let newChar = '';

        if (char === '"') {
            if (!quoteStart) {
                newChar = "<div class='quote'>" + char;
                quoteStart = true;
            } else {
                newChar = char + "</div>";
                quoteStart = false;
            }
        } else {
            newChar = char;
        }

        newText += newChar;
    }

    console.log(newText);
    return newText
}

highlightDescription();