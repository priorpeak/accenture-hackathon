$('[id*="tab-"]').click(function (e) {
    e.preventDefault()
    $(this).tab('show')

    console.log("hellolog")
        console.log(this.id)
    var message = this.id
    $.ajax({
        url:"/project_info",
        type:"POST",
        contentType: "application/json",
        data: JSON.stringify({"message":message})
    }).done(function(data){
        console.log(data)
        $('div#info').html(data.tab)
    });


    
    if(this.id=="tab-1"){
        $('body').css('background', 'red');
    }
    else if(this.id=="tab-2"){
        $('body').css('background', 'green');
    }
    else if(this.id=="tab-3"){
        $('body').css('background', 'blue');
    }
    else if(this.id=="tab-4"){
        $('body').css('background', 'purple');
    }
});
