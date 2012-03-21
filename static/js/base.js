
$(document).ready(function() {
  $('#status').on('focus', function() {
    this.style.rows = 8;
    this.style.cols = 80;
    this.style.width = "400px";
    return this.style.height = "80px";
  });
  return $('#status').on('blur', function() {
    this.style.rows = 1;
    this.style.cols = 30;
    this.style.width = "227px";
    return this.style.height = "13px";
  });
});
