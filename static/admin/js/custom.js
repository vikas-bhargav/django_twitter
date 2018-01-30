$('.follow').click(function(){
    var follow_id = $(this).attr('id');
    console.log(follow_id);
    alert(follow_id);
    $.ajax(
        {
            type:"GET",
            url: "follower",
            data:{
                post_id: follow_id
            },
            success: function( data )
            {
                alert(data);
                $("#follow_" + follow_id).replaceWith('<p id="unfollow_{{user.id}}"> <input type="button" ' +
                    'class="following" value="Following"><input type="submit" class="unfollow"   ' +
                    'id="{{user.id}}" value="Unfollow"></p>')

            }
        })
    return false;
});