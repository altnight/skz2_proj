
$(document).ready(function() {
  return $.ajax({
    type: "GET",
    url: "http://192.168.56.101:8000/get_home_timeline",
    dataType: "json",
    success: function(arg) {
      return console.log(arg);
    }
  });
});
