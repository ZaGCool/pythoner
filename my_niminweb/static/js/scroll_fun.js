$(window).scroll(function () {
        console.log(111)
        if($(this).scrollTop() > $('.navbar').outerHeight()){
            console.log(123)
            $('.navbar').css({
                position:"fixed",
                left:"50%",
                top:0,
                transform: "translateX(-50%)"
            })
            $('#con').css({
                marginTop:$('.navbar').outerHeight()
            })
        }else {
            $('.navbar').css({
                position:"static",
                transform:"none"

            })
            $('#con').css({
                marginTop:''
            })
        }
    })