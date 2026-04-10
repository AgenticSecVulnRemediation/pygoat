// Ensure DOMPurify is loaded: include via <script src='https://cdn.jsdelivr.net/npm/dompurify@2.0.17/dist/purify.min.js'></script>

event5 = function(){

    const code = document.getElementById('a6_t1').value;
    const sanitizedCode = DOMPurify.sanitize(code); // Ensure DOMPurify is loaded in HTML
    var myHeaders = new Headers();
    var formdata = new FormData();

    formdata.append("code", sanitizedCode);
    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: formdata,
        redirect: 'follow'
    };
    fetch("/2021/discussion/A6/api2", requestOptions)
    .then(response => response.text())
    .then(result => {
        let data = JSON.parse(result);
        if (data.message == "success"){
            alert("code saved");
        }  // parse JSON string into object
    })
    .catch(error => console.log('error', error));
}

event6 = function(){
    const code = document.getElementById('a6_t1').value;
    const sanitizedCode = DOMPurify.sanitize(code); // Ensure DOMPurify is loaded in HTML
    var myHeaders = new Headers();
    var formdata = new FormData();

    formdata.append("code", sanitizedCode);
    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: formdata,
        redirect: 'follow'
    };
    fetch("/2021/discussion/A6/api", requestOptions)
    .then(response => response.text())
    .then(result => {
        let data = JSON.parse(result);  // parse JSON string into object
        console.log(data.vulns);
        document.getElementById("a6_d5").style.display = 'flex';
        // document.getElementById("a6_d5").innerText =  data.vulns;

        for (var i = 0; i < data.vulns.length; i++) {
            var vuln = data.vulns[i];
            var vuln_div = document.createElement("div");
            vuln_div.innerText = JSON.stringify(vuln)   ;
            document.getElementById("a6_d5").appendChild(vuln_div);
        }
        
    })
    .catch(error => console.log('error', error));
}

