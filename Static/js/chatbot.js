$(document).ready(function() {
    $("#send-button").click(function() {
        var userInput = $("#user-input").val();
        if (userInput.trim() === "") return;

        $("#chat-box").append("<div><strong>You:</strong> " + userInput + "</div>");
        $("#user-input").val("");

        $.ajax({
            url: "/chatbot_response",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({ message: userInput }),
            success: function(response) {
                $("#chat-box").append("<div><strong>Bot:</strong> " + response.response + "</div>");
                $("#chat-box").scrollTop($("#chat-box")[0].scrollHeight);
            },
            error: function(xhr, status, error) {
                $("#chat-box").append("<div><strong>Bot:</strong> Sorry, something went wrong. Please try again.</div>");
                $("#chat-box").scrollTop($("#chat-box")[0].scrollHeight);
            }
        });
    });

    $("#user-input").keypress(function(event) {
        if (event.which === 13) {
            $("#send-button").click();
        }
    });
});
