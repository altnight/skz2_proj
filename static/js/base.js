
$(document).ready(function() {
  $('#status').on('focus', function() {
    this.style.rows = 8;
    this.style.cols = 80;
    this.style.width = "400px";
    return this.style.height = "80px";
  });
  $('#status').on('blur', function() {
    this.style.rows = 1;
    this.style.cols = 30;
    this.style.width = "227px";
    return this.style.height = "13px";
  });
  return $('#status').on('keyup', function(ev) {
    if (ev.keyCode === 13) {
      alert('発言しました');
      $.ajax({
        type: "GET",
        data: {
          q: $('#status').val()
        },
        url: "http://192.168.56.101:8000/update_status",
        dataTpye: "json"
      });
      テキストエリアを消す;
      return $('#status').val('');
    }
  });
});
