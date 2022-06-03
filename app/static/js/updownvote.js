$(function () {
    $(".increment").click(function () {



        var count = parseInt($("~ .count", this).text());
        // var id = this.id
        // const jsoony = [
        //     count,
        //     id
        // ]

        if ($(this).hasClass("up")) {
            var count = count + 1;

            $("~ .count", this).text(count);
        } else {
            var count = count - 1;
            $("~ .count", this).text(count);
        }

        $(this).parent().addClass("bump");


        fetch("http://127.0.0.1:5000/receiver", 
        {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'Accept': 'application/json'
            },
        // Strigify the payload into JSON:
        body:JSON.stringify(count)}).then(res=>{
                if(res.ok){
                    return res.json()
                }else{
                    alert("something is wrong")
                }
            }).then(jsonResponse=>{
                
                // Log the response data in the console
                console.log(jsonResponse)
            } 
            ).catch((err) => console.error(err));


    });
});