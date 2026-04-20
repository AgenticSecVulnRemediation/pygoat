// console.log("imported a9.js");
// Helper function to sanitize HTML input
function sanitizeHTML(input) {
    // This function escapes characters like <, >, &, ", and '
    return String(input).replace(/[&<>'"\/]/g, function (s) {
        var entityMap = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#39;',
            '/': '&#x2F;'
        };
        return entityMap[s];
    });
}

// Note: Alternatively, consider using a trusted library like DOMPurify for enhanced security. Replace this function with the library call if available.

event1 = function(){
    document.getElementById("a9_b1").style.display = 'none';
    document.getElementById("a9_d1").style.display = 'flex';
}

event2 = function(){
    document.getElementById("a9_b2").style.display = 'none';
    document.getElementById("a9_d2").style.display = 'flex';
}

event3 = function(){
    var log_code = sanitizeHTML(document.getElementById('a9_log').value);
    var target_code = sanitizeHTML(document.getElementById('a9_api').value);

    var myHeaders = new Headers();
    myHeaders.append("Cookie", "csrftoken=5fVOTXh2HNahtvJFJNRSrKkwPAgPM9YCHlrCGprAxhAAKOUWMxqMnWm8BUomv0Yd; jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjUzMzEzMDIxLCJpYXQiOjE2NTMzMDk0MjF9.dh2gfP9wKD8GKu1J-jVs2jJUYMgKu_kMaJjrD0hHP-I");

    var formdata = new FormData();
    formdata.append("csrfmiddlewaretoken", "5fVOTXh2HNahtvJFJNRSrKkwPAgPM9YCHlrCGprAxhAAKOUWMxqMnWm8BUomv0Yd");
    formdata.append("log_code", log_code);
    formdata.append("api_code", target_code);

    var requestOptions = {
    method: 'POST',
    headers: myHeaders,
    body: formdata,
    redirect: 'follow'
    };

    fetch("/2021/discussion/A9/api", requestOptions)
    .then(response => response.text())
    .then(result => {
        let data = JSON.parse(result);  // parse JSON string into object
        console.log(data.logs);
        document.getElementById("a9_d3").style.display = 'flex';
        for (var i = 0; i < data.logs.length; i++) {
            var li = document.createElement("li");
            li.innerHTML = data.logs[i];
            document.getElementById("a9_d3").appendChild(li);
        }
    })
    .catch(error => console.log('error', error));
    }
