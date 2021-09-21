if (window.location.pathname == '/create') {
    // start timer
    console.log("working!")
    timer = document.querySelector("#timer h4")
    submitBtn = document.getElementById("submit")
    var startTime = new Date().getTime()

    var x = setInterval(() => {
        var now = new Date().getTime()
        var count = now - startTime
        count = Math.floor(count/1000)

        // element
        if (count < 60) {
            timer.textContent = `${count} seconds passed`
        }

        else {
            timer.textContent = `times up`
            submitBtn.setAttribute("disabled", "true")
            clearInterval(x)
        }
    }, 1000)
}