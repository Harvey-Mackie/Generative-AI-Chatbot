$(function () {
    // Move the Jasmine HTML Location to the navbar (TOP OF THE PAGE)
    var checkExist = setInterval(function() {
        if ($('.jasmine_html-reporter').length) {
            clearInterval(checkExist);
            $('.jasmine_html-reporter').appendTo($('#nav'))
        }
     }, 100); // check every 100ms

    // Collection of Tests

    // Testing the getEmotion Function
    emotionObject = '{"joy":0,"sadness":0,"disgust":2,"contempt":0,"anger":0,"fear":0,"surprise":1}'
    expectedEmotion = "disgust"
    describe("Get User Emotion", () => {
        it("Emotion should equal disgust", () =>{
            actualEmotion = getEmotion(emotionObject, "None")
            expect(expectedEmotion).toBe(actualEmotion)
        })
    });

    // Testing the generateReply Function
    describe("Generate Chatbot Reply", () => {
        it("Reply should not be empty", () =>{
            chatbotReply = generateReply("Hey how are you?", "Joy")
            expect(chatbotReply.length >= 0).toBeGreaterThan(0)
        })
    });

    // Testing the sendMessage Function
    describe("Ensure User and Chatbot Messages are appended to the chat environment", () => {
        // Initialisng the users message and the chatbot personality in use
        $('.messageBox').val('Hey how are you?')
        $('.message').attr('name', "emotionChatbot")

        // retrieving current message lengths
        var userChatLength = $('.chat .mine .textMessage').length
        var chatbotChatLength = $('.chat .yours .textMessage').length
        // sending message via FLASK
        sendMessage()
        it("Users Message has been added", () =>{
            expect($('.chat .mine .textMessage').length).toBe((userChatLength+1))
        })
        it("Chatbots Message has been added", () =>{
            expect($('.chat .yours .textMessage').length).toBe((chatbotChatLength+1))
        })
        it("MessageBox should be made empty", () =>{
            expect($('.messageBox').val()).toBe("")
        })
    });

})