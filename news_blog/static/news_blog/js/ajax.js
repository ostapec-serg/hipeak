$(".fa-heart").click(function(){    $.ajax({        type: 'POST',        url: 'post/like/<int:post_id>',        dataType: 'json',        data: {},        success: function(data) {            $(".id_like").text(data.total_like);            },    });});;// using jQueryfunction getCookie(name) {    var cookieValue = null;    if (document.cookie && document.cookie !== '') {        var cookies = document.cookie.split(';');        for (var i = 0; i < cookies.length; i++) {            var cookie = jQuery.trim(cookies[i]);            if (cookie.substring(0, name.length + 1) === (name + '=')) {                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));                break;            }        }    }    return cookieValue;}var csrftoken = getCookie('csrftoken');function csrfSafeMethod(method) {    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));}$.ajaxSetup({    beforeSend: function(xhr, settings) {        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {            xhr.setRequestHeader("X-CSRFToken", csrftoken);        }    }});