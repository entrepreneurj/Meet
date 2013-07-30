var csrftoken = $.cookie('csrftoken');
var friend_list;

$.ajaxSetup({
      crossDomain: false, // obviates need for sameOrigin test
      beforeSend: function(xhr, settings) {
                              xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
});

$(document).ready(function() {
    // Handler for .ready() called.
alert( $.cookie("sessionid") );
console.log($.cookie("sessionid")); 
$.post("/api/friends/", { action: "friends" }, null, "json")
  .done(function(data) {
    console.log(data);
    console.log(data.error);
    friend_list=data;
      alert("Data Loaded: " + friend_list   );
  });

});

for(key in friend_list) {
      var value = blah[key];
          //do whatever you want with the data, such as:
          console.log("The value of ", key, " is ", value);
}
