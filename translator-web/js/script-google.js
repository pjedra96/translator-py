const fromText = document.querySelector(".from-text");
const toText = document.querySelector(".to-text");
const exchageIcon = document.querySelector(".exchange");
const speechIcon = document.getElementById('says');
const selectTag = document.querySelectorAll("select");
const icons = document.querySelectorAll(".row i");
const translateBtn = document.getElementById('translate');

// Click event listener for the speech button
window.addEventListener("DOMContentLoaded", () => {
    let listening = false;
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (typeof SpeechRecognition === "undefined") {
        speechIcon.remove();
    } else {
        let listening = false;
        const recognition = new SpeechRecognition();
        const start = () => {
            fromText.value = "";
            recognition.start();
            speechIcon.classList.remove("fa-microphone");
            speechIcon.classList.add("fa-stop");
        };
        const stop = () => {
            recognition.stop();
            speechIcon.classList.remove("fa-stop");
            speechIcon.classList.add("fa-microphone");
        };
        const onResult = event => {
            fromText.value = "";
            let recognisedSpeech = "";
            for (const res of event.results) {
                if (res.isFinal) {
                    fromText.value += res[0].transcript + ' ';
                }
            }
        };

        recognition.continuous = true;
        recognition.interimResults = false;
        recognition.addEventListener("result", onResult);

        // Listen for start and stop of the speech recognition
        speechIcon.addEventListener("click", () => {
            listening ? stop() : start();
            listening = !listening;
        });
    }
});

selectTag.forEach((tag, id) => {
    for (let country_code in countries) {
        let selected = id == 0 ? country_code == "en-GB" ? "selected" : "" : country_code == "de" ? "selected" : "";
        let option = `<option ${selected} value="${country_code}">${countries[country_code]}</option>`;
        tag.insertAdjacentHTML("beforeend", option);
    }
});

exchageIcon.addEventListener("click", () => {
    let tempText = fromText.value,
        tempLang = selectTag[0].value;
    fromText.value = toText.value;
    toText.value = tempText;
    selectTag[0].value = selectTag[1].value;
    selectTag[1].value = tempLang;
});

fromText.addEventListener("keyup", () => {
    if (!fromText.value) {
        toText.value = "";
    }
});

translateBtn.addEventListener("click", () => {
    let text = fromText.value.trim(),
        translateFrom = selectTag[0].value,
        translateTo = selectTag[1].value;
    if (!text) return;
    toText.setAttribute("placeholder", "Translating...");
    
    let apiUrl = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=${translateFrom}&tl=${translateTo}&dt=t&q=${encodeURI(text)}`;
    //let apiUrl = `https://api.mymemory.translated.net/get?q=${text}&langpair=${translateFrom}|${translateTo}`;
    fetch(apiUrl).then(res => res.json()).then(data => {
        console.log(data[0][0][0]);
        toText.value = data[0][0][0];
        toText.setAttribute("placeholder", "Translation");

        /*toText.value = data.responseData.translatedText;
        data.matches.forEach(data => {
            if (data.id === 0) {
                toText.value = data.translation;
            }
        });
        toText.setAttribute("placeholder", "Translation");*/
    });
});

icons.forEach(icon => {
    icon.addEventListener("click", ({ target }) => {
        if (!fromText.value || !toText.value) return;
        if (target.classList.contains("fa-copy")) {
            if (target.id == "from") {
                navigator.clipboard.writeText(fromText.value);
            } else {
                navigator.clipboard.writeText(toText.value);
            }
        } else {
            let utterance;
            if (target.id == "from") {
                utterance = new SpeechSynthesisUtterance(fromText.value);
                utterance.lang = selectTag[0].value;
            } else {
                utterance = new SpeechSynthesisUtterance(toText.value);
                utterance.lang = selectTag[1].value;
            }
            speechSynthesis.speak(utterance);
        }
    });
});