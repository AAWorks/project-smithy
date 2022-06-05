$(".upFunc").click(function () {
    var count = parseInt($("~ .count", this).text());
    count += 1
    $("~ .count", this).text(count);

    var id = this.id
    console.log(id)

    this.style.zIndex = '-1'
    var sibling = document.getElementById('ud' + id.substring(2))
    sibling.style.zIndex='1'

    $(this).parent().addClass("bump");


    fetch("http://127.0.0.1:5000/up_receiver",
        {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'Accept': 'application/json'
            },
            // Strigify the payload into JSON:
            body: JSON.stringify(id)
        }).then(res => {
            if (res.ok) {
                return res.json()
            } else {
                alert("something is wrong")
            }
        }).then(jsonResponse => {

            // Log the response data in the console
            console.log(jsonResponse)
        }
        ).catch((err) => console.error(err));

});


$(".upFunc2").click(function () {
    var count = parseInt($("~ .count", this).text());
    count += 1
    $("~ .count", this).text(count);

    var id = this.id
    console.log(id)

    this.style.zIndex = '-1'
    var sibling = document.getElementById('dd' + id.substring(2))
    sibling.style.zIndex='1'

    $(this).parent().addClass("bump");


    fetch("http://127.0.0.1:5000/up_receiver",
        {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'Accept': 'application/json'
            },
            // Strigify the payload into JSON:
            body: JSON.stringify(id)
        }).then(res => {
            if (res.ok) {
                return res.json()
            } else {
                alert("something is wrong")
            }
        }).then(jsonResponse => {

            // Log the response data in the console
            console.log(jsonResponse)
        }
        ).catch((err) => console.error(err));

});


$(".downFunc").click(function () {
    var count = parseInt($("~ .count", this).text());
    count -= 1
    $("~ .count", this).text(count);

    var id = this.id
    console.log(id)

    this.style.zIndex='-1'
    var sibling = document.getElementById('du' + id.substring(2))
    sibling.style.zIndex='1'
    
    $(this).parent().addClass("bump");


    fetch("http://127.0.0.1:5000/down_reciever",
        {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'Accept': 'application/json'
            },
            // Strigify the payload into JSON:
            body: JSON.stringify(id)
        }).then(res => {
            if (res.ok) {
                return res.json()
            } else {
                alert("something is wrong")
            }
        }).then(jsonResponse => {

            // Log the response data in the console
            console.log(jsonResponse)
        }
        ).catch((err) => console.error(err));

    setTimeout(function () {
        $(this).parent().removeClass("bump");
    }, 400);
});

$(".downFunc2").click(function () {
    var count = parseInt($("~ .count", this).text());
    count -= 1
    $("~ .count", this).text(count);

    var id = this.id
    console.log(id)

    this.style.zIndex='-1'
    var sibling = document.getElementById('uu' + id.substring(2))
    sibling.style.zIndex='1'
    
    $(this).parent().addClass("bump");


    fetch("http://127.0.0.1:5000/down_reciever",
        {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'Accept': 'application/json'
            },
            // Strigify the payload into JSON:
            body: JSON.stringify(id)
        }).then(res => {
            if (res.ok) {
                return res.json()
            } else {
                alert("something is wrong")
            }
        }).then(jsonResponse => {

            // Log the response data in the console
            console.log(jsonResponse)
        }
        ).catch((err) => console.error(err));

    setTimeout(function () {
        $(this).parent().removeClass("bump");
    }, 400);
});