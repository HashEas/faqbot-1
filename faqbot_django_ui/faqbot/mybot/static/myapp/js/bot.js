function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
function  getbotans(el){
    question  =  $('.message_input').val();
    $.ajax({
        url:  '/mybot/getbotans/',
        type:  'post',
        dataType:  'json',
        data:{
        question: question
        },
        success:  function (data) {
            location.reload();
            $("#chat_box_faqbot").animate({ scrollTop: $('#chat_box_faqbot').prop("scrollHeight")}, 1000);
        }
    });
}

$(function () {
    console.log("Hello!");
    $("#chat_box_faqbot").animate({ scrollTop: $('#chat_box_faqbot').prop("scrollHeight")}, 1000);
    $(".faqbot_send").on("click", function() {
      getbotans();
    });
});




