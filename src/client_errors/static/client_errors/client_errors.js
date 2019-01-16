window.onerror = function (msg, url, line, column, error) {
    // Get CSRF token
    var csrfToken = Cookies.get('csrftoken');

    // Create new XHR
    var xhr = new XMLHttpRequest();

    // Open async request
    xhr.open('POST', '/clientErrors/', true);

    // Set headers
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.setRequestHeader("X-CSRFToken", csrfToken);

    // Set event handler
    xhr.onreadystatechange = function () { // (3)
        if (xhr.readyState !== 4) return;

        if (xhr.status !== 200) {
            console.error('Error occured when sending client error to the server:', xhr.status, xhr.statusText);
        }
    };

    // Make request body
    var requestBodyArray = [
        'msg=' + encodeURIComponent(msg.toString()),
        'url=' + encodeURIComponent(url.toString()),
        'line=' + encodeURIComponent(line.toString())
    ];
    var requestBody = requestBodyArray.join('&');

    // Send request
    xhr.send(requestBody);

    // 'False' result here means 'propagate error to other handlers'
    return false;
};
