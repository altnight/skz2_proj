
$(document).ready(function() {
  var buildStream, createAPILimitFormat, createDateTimeFormat, createImage, createText, createTimeLink, createTweetdiv, createUserName, getAPILimit, getCurrentDate, getHomeTimeline, max_length, twitter_url;
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
  $('#current_date').append(createDateTimeFormat(getCurrentDate()));
  createAPILimitFormat = function(json) {
    var hourly_limit, remaining, reset_time;
    remaining = json.remaining;
    hourly_limit = json.hourly_limit;
    reset_time = createDateTimeFormat(new Date(json.reset_time));
    return "" + remaining + "/" + hourly_limit + " resetTime::" + reset_time;
  };
  getAPILimit = function() {
    return $.ajax({
      type: "GET",
      url: "http://192.168.56.101:8000/get_api_limit",
      dataTpye: "json",
      success: function(json) {
        return $('#api_limit').append(createAPILimitFormat(json));
      }
    });
  };
  getAPILimit();
  twitter_url = {
    url: "https://twitter.com/",
    api: "https://api.twitter.com/1/"
  };
  getHomeTimeline = function() {
    return $.ajax({
      type: "GET",
      url: "http://192.168.56.101:8000/get_home_timeline",
      dataTpye: "json",
      success: function(json) {
        return buildStream(json);
      }
    });
  };
  createTweetdiv = function(arg) {
    var tweetdiv;
    tweetdiv = $("<div>");
    tweetdiv.attr('class', 'tweet');
    return tweetdiv.attr('id', arg.status_id);
  };
  createImage = function(arg) {
    var img;
    img = $("<img/>");
    img.attr('src', arg.user_image_url);
    img.attr('alt', arg.screen_name);
    return img.attr('class', 'user_icon');
  };
  createUserName = function(arg) {
    var display_name, user_name;
    user_name = $("<a>");
    if (arg.screen_name === arg.name) {
      display_name = arg.screen_name;
    } else {
      display_name = "" + arg.screen_name + "(" + arg.name + ")";
    }
    user_name.attr('href', twitter_url.url + arg.screen_name);
    user_name.attr('class', 'user_name');
    return user_name.text(display_name);
  };
  createText = function(arg) {
    var textdiv, tweet;
    textdiv = $('<div>');
    textdiv.attr('class', 'text');
    tweet = arg.text;
    if (/shindanmaker/.test(tweet)) tweet = 'また診断メーカーか。';
    if (/#[一-龠ぁ-んァ-ヴー０-９]{10,}/.test(tweet)) tweet = 'また日本語ハッシュタグか';
    if (/gohantabeyo/.test(tweet)) tweet = 'またごはんか';
    return textdiv.text(tweet);
  };
  createTimeLink = function(arg) {
    var time, timelink;
    timelink = $('<a>');
    timelink.attr('href', "" + twitter_url.url + arg.screen_name + "/status/" + arg.status_id);
    timelink.attr('class', 'time');
    time = createDateTimeFormat(new Date(arg.created_at));
    return timelink.text(time);
  };
  buildStream = function(json) {
    var arg, tweetdiv, _i, _len, _results;
    _results = [];
    for (_i = 0, _len = json.length; _i < _len; _i++) {
      arg = json[_i];
      tweetdiv = createTweetdiv(arg);
      $("#column1").append(tweetdiv);
      tweetdiv.append(createImage(arg));
      tweetdiv.append(createUserName(arg));
      tweetdiv.append(createText(arg));
      _results.push(tweetdiv.append(createTimeLink(arg)));
    }
    return _results;
  };
  return getHomeTimeline();
});
