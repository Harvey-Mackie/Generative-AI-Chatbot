var emotionName = "" //global variable - holding the current user emotional state
var oldEmotion = ""
var username = ""
var emotions = ['joy','contempt','surprise','fear','anger','disgust','sad']
$(function () {
    
    $('#usernameSubmit').on('click',function(){
        if($('#username').length > 0){
            // Intialise Affectiva SDK
            intialiseEmotionRecognition()

            //Testing Environment
            $('.overlay').fadeOut()
            $('#chatBackground').fadeIn()
            username = $('#username').val()
            countdownTimer(10)  
        }
    })
})


//Users image is savd and stored to a table to allow for the results to be visualised.
function saveImageWithEmotion(){
    var canvas = $("#face_video_canvas")[0];
    var userImage = canvas.toDataURL("image/png");
    var tableRow = '<tr><td>' + oldEmotion +'</td><td>'+ emotionName +'</td><td><a href="'+userImage+'" download="'+ emotionName + " - " + username + " - " + oldEmotion +'"><img src="'+userImage+'"/></a></td></tr>'
    $("table.emotionResults tbody").append(tableRow);
}
//Display emotion user should express
function retrieveCurrentEmotionToBeExpressed(){
    var currentEmotion = $('span.emotion').text()
    oldEmotion = currentEmotion
    for (let index = 0; index < emotions.length; index++) {
        if(emotions[index].toLowerCase() == currentEmotion.toLowerCase() && (index+1) < emotions.length ){
            return emotions[(index+1)]
        }
    }
    return 'None'
}

//Reset timer until testing is complete.
function restartTimer(countdownClock){
    clearInterval(countdownClock)
    // Alter the emotion to be expressed
    emotion = retrieveCurrentEmotionToBeExpressed()
    if(emotion !== 'None'){
        saveImageWithEmotion()
        $('span.emotion').text(emotion)
        countdownTimer(10)
    }else{
        saveImageWithEmotion()
        alert("Testing Complete - Collect Results")
    }
    
}

// Commence testing timer
function countdownTimer(timer){
    $('.backArrow').show()
    var countdownClock = setInterval(function(){ 
        $('.backArrow p').text(timer)
        if(timer <= 0){
            restartTimer(countdownClock)
        }
        timer--;
    }, 1000);
}

// Initalise Affectiva APK 
function intialiseEmotionRecognition(){
    // SDK Needs to create video and canvas nodes in the DOM in order to function
    // Here we are adding those nodes a predefined div.
    var divRoot = $("#affdex_elements")[0];
    var width = 320;
    var height = 240;
    var faceMode = affdex.FaceDetectorMode.LARGE_FACES;
    //Construct a CameraDetector and specify the image width / height and face detector mode.
    var detector = new affdex.CameraDetector(divRoot, width, height, faceMode);
    //Enable detection of all Emotions
    detector.detectAllEmotions();
    detector.start()
    //Initialise webcam and image listeners
    webcamEventListeners()
    recivedImageListener()

    //Add a callback to notify when camera access is allowed
    function webcamEventListeners(){
        //Add a callback to notify when the detector is initialized and ready for runing.
        detector.addEventListener("onInitializeSuccess", function () {
            console.log('#logs', "Load Successful");
        });
        detector.addEventListener("onWebcamConnectSuccess", function () {
            console.log('#logs', "Webcam Connected");
            webcamActive = "True"
        });
    
        //Add a callback to notify when camera access is denied
        detector.addEventListener("onWebcamConnectFailure", function () {
            console.log('#logs', "Webcam Not Connected");
            webcamActive = "False"
        });
    }

    function recivedImageListener(){
        //Add a callback to receive the results from processing an image.
        //The faces object contains the list of the faces detected in an image.
        //Faces object contains probabilities for all the different expressions, emotions and appearance metrics
        detector.addEventListener("onImageResultsSuccess", function (faces) {
            if (faces.length > 0) {
                var emotions = JSON.stringify(faces[0].emotions, function (key, val) { return val.toFixed ? Number(val.toFixed(0)) : val; })
                emotionName = getEmotion(emotions, emotionName)
                console.log(emotionName)
            }
        });
    }
}

//get users emotion from json string and store the value in the emotionName global variable
function getEmotion(emotions, emotionName) {
    emotions = JSON.parse(emotions)
    var emotionValidator = { originalEmotion: emotionName, newEmotionValue: 0, newEmotionName: "" };
    $.each(emotions, function (key, value) {
        if (Math.abs(value) >= emotionValidator.newEmotionValue && key != "engagement" && key != "valence") {
            emotionValidator.newEmotionValue = value
            emotionValidator.newEmotionName = key
        }
    });
    if (emotionValidator.originalEmotion != emotionValidator.newEmotionName && emotionValidator.newEmotionName.length > 0) {
        return emotionValidator.newEmotionName 
    }else{
        return emotionName
    }
}
