const searchForm = document.querySelector("#userInput");
const searchFormInput = searchForm.querySelector("#textInput");

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
if(SpeechRecognition) {
    console.log("Your Browser supports speech Recognition");
    
    const recognition = new SpeechRecognition();
    recognition.continuous = true;
    // recognition.lang = "en-US";
    recognition.interimResults = true;

    // searchForm.insertAdjacentHTML("beforeend", '<button type="button" id="micBtn"><i class="fas fa-microphone"></i></button>');
    // searchFormInput.style.paddingRight = "50px";
    // const micBtn = searchForm.querySelector("button");
    // const micIcon = micBtn.firstElementChild;
    const micBtn = searchForm.querySelector("#micBtn");
    // const micIcon = micBtn.childNodes[1];
    const micIcon = micBtn.firstElementChild;

    micBtn.addEventListener("click", micBtnClick);
    function micBtnClick() {
        if(micIcon.classList.contains("fa-microphone")) { // Start Voice Recognition
            recognition.start(); // First time you have to allow access to mic!
        }
        else {
            recognition.stop();
        }
    }
    recognition.addEventListener("start", startSpeechRecognition); // <=> recognition.onstart = function() {...}
    function startSpeechRecognition() {
        micIcon.classList.remove("fa-microphone");
        micIcon.classList.add("fa-microphone-slash");
        searchFormInput.focus();
        console.log("Voice activated, SPEAK");
    }

    recognition.addEventListener("end", endSpeechRecognition); // <=> recognition.onend = function() {...}
    function endSpeechRecognition() {
        micIcon.classList.remove("fa-microphone-slash");
        micIcon.classList.add("fa-microphone");
        searchFormInput.focus();
        console.log("Speech recognition service disconnected");
    }

    recognition.addEventListener("result", resultOfSpeechRecognition); // <=> recognition.onresult = function(event) {...} - Fires when you stop talking
    function resultOfSpeechRecognition(event) {
        const current = event.resultIndex;
        const transcript = event.results[current][0].transcript;
        
        if(transcript.toLowerCase().trim()==="stop recording") {
            recognition.stop();
            searchFormInput.value = '';
            // document.getElementById('textInput') = '';
        }
        else if(!searchFormInput.value) {
            searchFormInput.value = transcript;
        }
        else {
        if(transcript.toLowerCase().trim()==="go") {
            // searchForm.submit();
            getBotResponse();
        }
        else if(transcript.toLowerCase().trim()==="reset input") {
            searchFormInput.value = '';
        }
        else {
            searchFormInput.value = transcript;
        }
        }
        // searchFormInput.value = transcript;
        // searchFormInput.focus();
        // setTimeout(() => {
        //   searchForm.submit();
        // }, 500);
    }
}
else {
    console.log("Your Browser does not support speech Recognition");
    // info.textContent = "Your Browser does not support Speech Recognition";
}
// searchForm.insertAdjacentHTML("beforeend", '<button type="button" id="soundButton"><i class="fas fa-volume-up"></i></button>');
// const soundBtn = searchForm.querySelector('button:nth-of-type(2)');
const soundBtn = searchForm.querySelector("#soundButton");
// soundBtn.style.backgroundColor = 'Red';
const soundIcon = soundBtn.firstElementChild;
// const soundIcon = soundBtn.childNodes[2];
// soundIcon.style.color = "#66c144";
soundBtn.addEventListener("click", soundBtnClick);
    function soundBtnClick(){
        if(soundIcon.classList.contains('fa-volume-up')){
            soundIcon.classList.remove("fa-volume-up");
            soundIcon.classList.add("fa-volume-mute");
            // window.speechSynthesis.speak(speech);
            // speech.volume = 1;
            stopText();
        }
        else{
            soundIcon.classList.remove("fa-volume-mute");
            soundIcon.classList.add("fa-volume-up");
            // speech.volume = 0;
            // if(window.speechSynthesis.speaking){
                // window.speechSynthesis.stop();
                // speech.volume = 0;
            // }
        }   
    }     
// Text to Speech

let speech = new SpeechSynthesisUtterance();
function textToAudio(text){
    speech.lang = "en-US";
    speech.text = text;
    speech.rate = 1;
    speech.pitch = 1;    
    var temp;
    check();
    function check(){
        // let temp
        if(soundIcon.classList.contains('fa-volume-up')){
            temp = 1;
            console.log("Sound is playing"); 
        }
        else{
            temp = 0;
            console.log("Sound is not playing");
        }
        return temp
    }
    speech.volume = temp;
    return window.speechSynthesis.speak(speech);
}  
function stopText(){
    speechSynthesis.resume();
    speechSynthesis.cancel();
}