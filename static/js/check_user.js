$('#usernmae').keyup(function()
{

    var = username = $('username').val();
    if(username!=''){
        $.post('/write', {username:username})

        function(data){
            $('#status').html(data);
        }

    }
    else{
        $('#status').html('');

    }
}
