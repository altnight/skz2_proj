
$(document).ready(function() {
  var createDateTimeFormat, getCurrentDate, max_length;
  $('#status').on('focus', function() {
    $(this).css('rows', 8);
    $(this).css('cols', 80);
    $(this).css('width', '400px');
    return $(this).css('height', '80px');
  });
  $('#status').on('blur', function() {
    $(this).css('rows', 1);
    $(this).css('cols', 30);
    $(this).css('width', '227px');
    return $(this).css('height', '13px');
  });
  max_length = 140;
  $('#count').text(max_length);
  $('#status').on('keyup', function(ev) {
    if (ev.keyCode === 13) {
      if (max_length < $(this).val().length) {
        alert('140字を超えています');
        return false;
      }
      $.ajax({
        type: "GET",
        data: {
          q: $(this).val()
        },
        url: "http://192.168.56.101:8000/update_status",
        dataTpye: "json"
      });
      alert('発言しました');
      return $(this).val('');
    }
  });
  $('#status').on('keyup', function(ev) {
    $('#count').text(max_length - $(this).val().length);
    if (max_length < $(this).val().length) {
      return $('#count').css('color', 'red');
    } else {
      return $('#count').css('color', 'black');
    }
  });
  getCurrentDate = function() {
    return new Date;
  };
  createDateTimeFormat = function(d) {
    var date, hour, minutes, month, seconds, year;
    year = d.getFullYear();
    month = d.getMonth() + 1;
    date = d.getDate();
    hour = d.getHours();
    minutes = ("0" + d.getMinutes()).slice(-2);
    seconds = ("0" + d.getSeconds()).slice(-2);
    return "" + year + "/" + month + "/" + date + " " + hour + ":" + minutes + ":" + seconds;
  };
  return $('#current_date').append(createDateTimeFormat(getCurrentDate()));
});
