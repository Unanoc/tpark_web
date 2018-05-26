'use strict';

function like() {
    var like = $(this);
    var type = like.data('type');
    var pk = like.data('id');
    var action = like.data('action');
    var dislike = like.next();

    $.ajax({
        url : "/api/" + type +"/" + pk + "/" + action + "/",
        type : 'POST',
        data : { 'obj' : pk },
        success : function (json) {
            like.find("[data-count='like']").text(json.like_count);
            dislike.find("[data-count='dislike']").text(json.dislike_count);
            like[0].text = "<span class=\"glyphicon glyphicon-thumbs-up\"></span>" + "<span data-count=\"like\">" + toString(json.like_count) + "</span>";
            dislike[0].text = "<span class=\"glyphicon glyphicon-thumbs-down\"></span>" + "<span data-count=\"dislike\">" + toString(json.dislike_count) + "</span>";
        }
    });
    return false;
}

function dislike() {
    var dislike = $(this);
    var type = dislike.data('type');
    var pk = dislike.data('id');
    var action = dislike.data('action');
    var like = dislike.prev();

    $.ajax({
        url: "/api/" + type + "/" + pk + "/" + action + "/",
        type: 'POST',
        data: {'obj': pk},

        success: function (json) {
            like.find("[data-count='like']").text(json.like_count);
            dislike.find("[data-count='dislike']").text(json.dislike_count);
            dislike[0].text = "<span class=\"glyphicon glyphicon-thumbs-down\"></span>" + "<span data-count=\"dislike\">" + toString(json.dislike_count) + "</span>";
            like[0].text = "<span class=\"glyphicon glyphicon-thumbs-up\"></span>" + "<span data-count=\"like\">" + toString(json.like_count) + "</span>";
        }
    });

    return false;
}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Настройка AJAX
$(function () {
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
});

// Подключение обработчиков
$(function() {
    $('[data-action="like"]').click(like);
    $('[data-action="dislike"]').click(dislike);
});