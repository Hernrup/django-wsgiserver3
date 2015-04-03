// using jQuery

// would be simplier with jquery cookie plugin
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}


function handleErrFullPageJQ(event,jqXHR,ajaxsettings, thrownerror) {
    // based on someone else's code, this does not work currently
    var errorWin;

    // Create new window and display error
    try {
	errorWin = window.open('', 'errorWin');
	// errorWin.document.body.innerHTML = strIn; // works in IE 6
	errorWin.document.write(event, jqXHR, ajaxsettings, thrownerror); // works in firefox and IE 6

    }
    // If pop-up gets blocked, inform user
    catch(e) {
	alert('An error occurred, but the error message cannot be' +
              ' displayed because of your browser\'s pop-up blocker.\n' +
	      'Please allow pop-ups from this Web site.');
    }
}



function csrfSafeMethod(method) {
    // These HTTP methods do not require CSRF protection
    return (/ˆ(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

// jquery recommneds against using $.ajaxSetup as it may confuse plugins
// so instead we will use our own custom function
// $.ajaxSetup({
//     crossDomain: false, // Obviates need for sameOrigin test
//     beforeSend: function(xhr, settings) {
// 	if (!csrfSafeMethod(settings.type)) {
//             xhr.setRequestHeader("X-CSRFToken", csrftoken);
// 	}
//     }
   
// });

$(document).ajaxError( function (event, jqXHR, ajaxsettings, thrownerror) {
    console.log(event, jqXHR, ajaxsettings, thrownerror);
    handleErrFullPageJQ(event, jqXHR, ajaxsettings, thrownerror);
}
		       )
function django_ajax(request_type, url, onsuccess)
{
    $.ajax({
	crossDomain: false, // avoid need for same origin test
	url: url,
	type: request_type, // 'GET'|'PUT'|'POST'
	beforeSend: function(xhr, settings) {
 	    if (!csrfSafeMethod(settings.type))  {
		xhr.setRequestHeader("X-CSRFToken", csrftoken);
 	    }
	    },
	success: onsuccess,
	})
   
}
