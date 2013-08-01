var csrftoken = $.cookie('csrftoken');
var friend_list;
var invited_list=[];

// See http://www.djbp.co.uk/django-poll-tutorial-ajax/
$.ajaxSetup({
  crossDomain: false, // obviates need for sameOrigin test
  beforeSend: function(xhr, settings) {
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
  }
});



$(document).ready(function() {
  // Handler for .ready() called.
  $.post("/api/friends/", { action: "friends" }, null, "json")
  .done(function(data) {
    friend_list=data;
    console.log(friend_list);
    for (i in friend_list) {
      friend=friend_list[i];
      $("#friend-list").append('<div id="'+ friend["u"] + '" class="invite-friend"><img src="' +friend.p + '" class="invite-friend" /><p class="invite-friend">' +friend.n +'</p></div>');
      //do whatever you want with the data, such as:
      //    console.log("The value of ", key, " is ", value);
    }

    $("div.invite-friend").click(function() {
      friend=$(this).get(0);
      $(this).toggleClass("invited");
      var is_contained ="";
      var at_index="";
      $.each(invited_list,function(index, value) {
          console.log(friend.id);
        if (invited_list[index][0]==friend.id)
        {
       is_contained =  "1";
        at_index=index;
        }
      
      });

      if (!is_contained)
      {
  
      invited_list.push([friend.id,"1"]);
      }
      else
    {
      if (invited_list[at_index][1]=="0")
      {
      invited_list[at_index][1]="1";
      }
      else
      {
       invited_list[at_index][1]="0"; 
      }
    }

    });


  });





});

