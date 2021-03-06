(function() {

  $(function() {
    var buildColumn, buildStream, build_column, createAPILimitFormat, createDateTimeFormat, createFavButton, createImage, createProtectedImg, createRTButton, createRTImg, createRTSpan, createRTcount, createReplyButton, createText, createTimeLink, createTweetdiv, createUserName, getAPILimit, getCurrentDate, getHomeTimeline, getListTimeline, getLists, max_length, readCallback, reload, toggleFav, toggleFavView, toggleRT, toggleRTView, twitter_url;
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
    $('#status').on('keypress', function(ev) {
      var _this = this;
      if (ev.keyCode === 13) {
        if (max_length < $(this).val().length) {
          alert('140字を超えています');
          return false;
        }
        return $.ajax({
          type: "GET",
          data: {
            q: $(this).val(),
            in_reply_to_status_id: localStorage.in_reply_to_status_id
          },
          url: "http://127.0.0.1:8000/update_status",
          dataTpye: "json",
          success: function() {
            alert("発言しました");
            $(_this).val('');
            $(_this).blur();
            return $('#count').text(max_length);
          },
          error: function(XMLHttpRequest, textStatus, errorThrown) {
            return alert("なんか発言失敗したっぽい");
          }
        });
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
    createAPILimitFormat = function(json) {
      var hourly_limit, remaining, reset_time;
      remaining = json.remaining;
      hourly_limit = json.hourly_limit;
      reset_time = createDateTimeFormat(new Date(json.reset_time));
      return "APILimit::" + remaining + "/" + hourly_limit + " resetTime::" + reset_time;
    };
    getAPILimit = function() {
      return $.ajax({
        type: "GET",
        url: "http://127.0.0.1:8000/get_api_limit",
        dataTpye: "json",
        success: function(json) {
          return $('#api_limit').append(createAPILimitFormat(json));
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
          return $('#api_limit').append("さーせん、うまくいかなかったっす");
        }
      });
    };
    getHomeTimeline = function(column_id) {
      return $.ajax({
        type: "GET",
        url: "http://127.0.0.1:8000/get_home_timeline",
        dataTpye: "json",
        success: function(json) {
          return buildStream(json, column_id);
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
          return alert("さーせん、うまくとれなかったっす");
        }
      });
    };
    getLists = function() {
      return $.ajax({
        type: "GET",
        url: "http://127.0.0.1:8000/get_lists",
        dataTpye: "json",
        success: function(json) {
          return console.log(json);
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
          return alert("さーせん、うまくとれなかったっす");
        }
      });
    };
    getListTimeline = function(list_owner, list_name, include_rts, column_id) {
      return $.ajax({
        type: "GET",
        url: "http://127.0.0.1:8000/get_list_timeline/" + list_owner + "/" + list_name + "/?rts=" + include_rts,
        dataTpye: "json",
        success: function(json) {
          return buildStream(json, column_id);
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
          return alert("さーせん、うまくとれなかったっす");
        }
      });
    };
    twitter_url = {
      url: "https://twitter.com/",
      api: "https://api.twitter.com/1/"
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
      tweet = tweet.replace(/(https?:\/\/[\w\.\,\-\+\?\/\%#=\&\!]+)/ig, "<a href='$1' class='url'>$1</a>");
      tweet = tweet.replace(/@([\a-zA-Z0-9_]+)/g, "<a href=" + twitter_url.url + "$1>@$1</a>");
      tweet = tweet.replace(/#([\w一-龠ぁ-んァ-ヴー]+)/g, "<a href=" + twitter_url.url + "search/%23$1>#$1</a>");
      if (/shindanmaker/.test(tweet)) tweet = 'また診断メーカーか。';
      if (/#[一-龠ぁ-んァ-ヴー０-９]{10,}/.test(tweet)) tweet = 'また日本語ハッシュタグか';
      if (/gohantabeyo/.test(tweet)) tweet = 'またごはんか';
      return textdiv.html(tweet);
    };
    createRTImg = function(arg) {
      var img;
      img = $('<img/>');
      img.attr('src', arg.old_tweet_user_image_url);
      img.attr('class', 'retweeted');
      return img.attr('alt', arg.old_tweet_screen_name);
    };
    createRTSpan = function(arg) {
      var span;
      span = $('<span>');
      return span.text("RT::" + arg.old_tweet_screen_name);
    };
    createRTcount = function(arg) {
      var retweeted_count, span;
      span = $('<span>');
      retweeted_count = parseInt(arg.retweeted_count) + 1;
      return span.text("&" + retweeted_count);
    };
    createTimeLink = function(arg) {
      var time, timelink;
      timelink = $('<a>');
      timelink.attr('href', "" + twitter_url.url + arg.screen_name + "/status/" + arg.status_id);
      timelink.attr('class', 'time');
      time = createDateTimeFormat(new Date(arg.created_at));
      return timelink.text(time);
    };
    createProtectedImg = function() {
      var button;
      button = $('<img/>');
      button.attr('src', 'static/image/protected.png');
      button.attr('alt', 'protected');
      return button.attr('class', 'protected');
    };
    createReplyButton = function() {
      var button;
      button = $('<img/>');
      button.attr('src', 'static/image/reply.png');
      button.attr('alt', 'replyButton');
      return button.attr('class', 'reply');
    };
    createFavButton = function(arg) {
      var button;
      button = $('<img/>');
      if (arg.favorited) {
        button.attr('src', 'static/image/favorite_on.png');
      } else {
        button.attr('src', 'static/image/favorite.png');
      }
      button.attr('alt', 'FavButton');
      return button.attr('class', 'fav');
    };
    createRTButton = function(arg) {
      var button;
      button = $('<img/>');
      if (arg.retweeted) {
        button.attr('src', 'static/image/retweet_on.png');
      } else {
        button.attr('src', 'static/image/retweet.png');
      }
      button.attr('alt', 'RTButton');
      return button.attr('class', 'retweet');
    };
    buildStream = function(json, column_id) {
      var arg, tweetdiv, _i, _len, _results;
      _results = [];
      for (_i = 0, _len = json.length; _i < _len; _i++) {
        arg = json[_i];
        tweetdiv = createTweetdiv(arg);
        $("#column" + column_id).append(tweetdiv);
        tweetdiv.append(createImage(arg));
        tweetdiv.append(createUserName(arg));
        if (arg.protected) tweetdiv.append(createProtectedImg());
        tweetdiv.append(createText(arg));
        tweetdiv.append(createTimeLink(arg));
        tweetdiv.append(createReplyButton());
        tweetdiv.append(createFavButton(arg));
        tweetdiv.append(createRTButton(arg));
        if (arg.old_tweet_screen_name) {
          tweetdiv.append(createRTImg(arg));
          tweetdiv.append(createRTSpan(arg));
          _results.push(tweetdiv.append(createRTcount(arg)));
        } else {
          _results.push(void 0);
        }
      }
      return _results;
    };
    toggleFav = function(id) {
      return $.ajax({
        type: "GET",
        url: "http://127.0.0.1:8000/toggleFav",
        data: {
          id: id
        },
        dataTpye: "json",
        success: function(json) {
          return toggleFavView(json);
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
          return alert("さーせん、うまくとれなかったっす");
        }
      });
    };
    toggleFavView = function(json) {
      if (json.favorited === "True") {
        return $("#" + json.tweet_id + " .fav").attr('src', './static/image/favorite_on.png');
      } else if (json.favorited === "False") {
        return $("#" + json.tweet_id + " .fav").attr('src', './static/image/favorite.png');
      }
    };
    toggleRT = function(id, protected) {
      if (protected === "protected") {
        alert("鍵垢です");
        return false;
      }
      return $.ajax({
        type: "GET",
        url: "http://127.0.0.1:8000/toggleRT",
        data: {
          id: id
        },
        dataTpye: "json",
        success: function(json) {
          return toggleRTView(json);
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
          return alert("さーせん、うまくとれなかったっす");
        }
      });
    };
    toggleRTView = function(json) {
      if (json.retweeted === "True") {
        return $("#" + json.tweet_id + " .retweet").attr('src', './static/image/retweet_on.png');
      } else if (json.retweeted === "False") {
        return $("#" + json.tweet_id + " .retweet").attr('src', './static/image/retweet.png');
      }
    };
    $('.reply').live("mouseenter", function() {
      return $(this).attr('src', './static/image/reply_hover.png');
    });
    $('.reply').live("mouseleave", function() {
      return $(this).attr('src', './static/image/reply.png');
    });
    $('.reply').live('click', function() {
      var id, screen_name, tweet;
      tweet = $(this).parent();
      id = tweet.attr('id');
      screen_name = "@" + $("#" + id + " .user_icon").attr('alt');
      localStorage.in_reply_to_status_id = id;
      $('#status').focus();
      return $('#status').val("" + screen_name + " ");
    });
    $('.fav').live('click', function() {
      var id, tweet;
      tweet = $(this).parent();
      id = tweet.attr('id');
      return toggleFav(id);
    });
    $('.retweet').live('click', function() {
      var id, protected, tweet;
      tweet = $(this).parent();
      id = tweet.attr('id');
      protected = $("#" + id + " .protected").attr('alt');
      return toggleRT(id, protected);
    });
    $('#config').on('click', function(ev) {
      if ($('#config_window').css('display') === "none") {
        return $("#config_window").css('display', 'block');
      } else {
        return $("#config_window").css('display', 'none');
      }
    });
    $('#addColumn').on('click', function(ev) {
      var column_id;
      return column_id = build_column.incID();
    });
    buildColumn = function() {
      var column_id;
      column_id = 0;
      return {
        incID: function() {
          return column_id++;
        },
        getCloumnID: function() {
          return column_id;
        },
        resetCloumnID: function() {
          return column_id = 0;
        }
      };
    };
    readCallback = function() {
      build_column.incID();
      getHomeTimeline(build_column.getCloumnID());
      build_column.incID();
      getListTimeline("altnight", "javascript", "True", build_column.getCloumnID());
      build_column.incID();
      getListTimeline("altnight", "net", "True", build_column.getCloumnID());
      build_column.incID();
      getListTimeline("altnight", "jz", "True", build_column.getCloumnID());
      build_column.incID();
      getListTimeline("altnight", "py", "True", build_column.getCloumnID());
      return build_column.resetCloumnID();
    };
    build_column = buildColumn();
    $('#current_date').append(createDateTimeFormat(getCurrentDate()));
    getAPILimit();
    readCallback();
    return reload = setInterval(function() {
      return location.reload();
    }, 4 * 60 * 1000);
  });

}).call(this);
