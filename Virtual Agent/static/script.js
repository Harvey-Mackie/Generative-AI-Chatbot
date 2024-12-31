var emotionName = "" //global variable - holding the current user emotional state
var webcamActive = "" //global variable - holding the current user webcam active status
$(function () {

    /*
    Setting on click listeners and changing the viewable components
    - popup is the loading (progress bar) component
    - chatCategories is the container of the three chat personalties (inital page)
    - chatBackground is the container of the chat and webcam functionality
    - message is the messagebox located at the bottom of the chat
    - chat is the collection of messages located in the chat
    - backArrow is the fixed element (top right) which redirects back to the chat peronalities
    Run Function once Javascript and jQuery has loaded (document ready)
    */
    scriptInit()
    function scriptInit(){
        $('.popup').slideUp()
        $('.chatCategories').slideDown()

        $('.chatPersonality').on('click',function(){
            var chatbotType = $(this).attr('id')
            $('.message').attr('name', chatbotType)
            $('.chatCategories').slideUp()
            $('.popup').slideDown(400,function(){
                $(this).slideUp()
                $('.chatBackground').slideDown()
                $('.backArrow').slideDown()
            })
        })
    
        $('.backArrow').on('click',function(){
            $('.chatBackground').slideUp()
            $('.backArrow').slideUp()
            $('.popup').slideDown(400,function(){
                $(this).slideUp()
                $('.chatCategories').slideDown()
                $('.chat').empty()
            })
        })
    } 

    // Intialise Affectiva SDK
    intialiseEmotionRecognition()

    //Set onclick  and keyup (on press of the enter) listeners for sending sending a message to the chatbot
    initialiseMessageBox()
    function initialiseMessageBox(){
        $('.sendMessage').click(function (e) { 
            e.preventDefault();
            sendMessage()
        });
        $('.messageBox').keyup(function(e){
            if(e.keyCode == 13){   
                e.preventDefault();
                sendMessage()
            }
        });
    }

}) 

// Append user message to chat and Generate chatbot message to append to the chat
function sendMessage(){
    var message = $('.messageBox').val() //retrieve messagebox value
    $('.messageBox').val('') //set messagebox value to null
        //Append message to users messages div [mine textMessages]
        generateMessage('mine',message)
        //Retrieve message from chatbot AI model (generated back-end with Flask) and Append message to chatbots messages div [yours textMessages]
        var reply = generateReply(message,emotionName)
        generateMessage('reply',reply)

        emotionName = "" //set global emotionName variable to inital state (empty)
}

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

//Append message to the chat HTML element (append user and chatbot messages to different divs)
function generateMessage(type,message){
    message = '<div class="textMessage">'+message+'</div>'
    if(type == "reply"){
        if($('.textMessages:last-child').hasClass('yours')){
            $(message).appendTo('.yours:last-child')
        }else{
            $('.textMessages:last-child').children().addClass('last') 
            $('.chat').append('<div class="yours textMessages">'+message+'</div>')
        }
    }else{
        if($('.textMessages:last-child').hasClass('mine')){
            $(message).appendTo('.mine:last-child')
        }else{
            $('.textMessages:last-child').children().addClass('last')
            $('.chat').append('<div class="mine textMessages">'+message+'</div>')
        }
    }
    updateScroll()
}

// AJAX POST Request to the FLASK backend to retrieve the chatbots message 
function generateReply(message,userEmotion){
    var chatbotType = $('.message').attr('name')
    var chatbotReply = ""
    $.ajax({
        url : '/generateMessage',
        data: { userMessage: message, emotion:userEmotion, chatType:chatbotType},
        async: false,
            success: function(data) {
                chatbotReply = data
            }
        });
        return chatbotReply
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

//Ensure the user can see the most recent messages at all times by ensuring the scroll is fixed to the bottom upon new messages
function updateScroll(){
    if($(".chat").scrollTop() != null){
        $(".chat").scrollTop($(".chat")[0].scrollHeight);
    }
}