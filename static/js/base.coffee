$ ->
    #投稿する
    #=========================
    $('#status').on('focus', ->
        $(@).css('rows', 8)
        $(@).css('cols', 80)
        $(@).css('width', '400px')
        $(@).css('height', '80px')
    )
    $('#status').on('blur', ->
        $(@).css('rows', 1)
        $(@).css('cols', 30)
        $(@).css('width', '227px')
        $(@).css('height', '13px')
    )

    max_length= 140
    $('#count').text(max_length)

    $('#status').on('keypress', (ev)->
        if ev.keyCode == 13 #Enter
            if max_length < $(@).val().length
                alert '140字を超えています'
                return false
            $.ajax
                type: "GET"
                data:
                    q: $(@).val()
                #url: "http://192.168.56.101:8000/update_status"
                url: "http://127.0.0.1:8000/update_status"
                dataTpye: "json"
                success: =>
                    alert "発言しました"
                    #テキストエリアを消す
                    $(@).val('')
                    $(@).blur()
                    $('#count').text(max_length)
                error: (XMLHttpRequest, textStatus, errorThrown)->
                    alert "なんか発言失敗したっぽい"
    )

    $('#status').on('keyup', (ev)->
        $('#count').text(max_length - $(@).val().length)
        if max_length < $(@).val().length
            $('#count').css('color', 'red')
        else
            $('#count').css('color', 'black')
    )
    #=========================

    #時刻を設定する
    #=========================
    getCurrentDate = ->
        new Date
    createDateTimeFormat = (d) ->
        year = d.getFullYear()
        month = (d.getMonth() + 1)
        date = d.getDate()
        hour = d.getHours()
        minutes = ("0" + d.getMinutes()).slice(-2)
        seconds = ("0" + d.getSeconds()).slice(-2)
        return "#{year}/#{month}/#{date} #{hour}:#{minutes}:#{seconds}"

    $('#current_date').append(createDateTimeFormat(getCurrentDate()))
    #=========================


    #APILimit
    #=========================

    createAPILimitFormat = (json)->
        remaining = json.remaining
        hourly_limit= json.hourly_limit
        reset_time= createDateTimeFormat(new Date(json.reset_time))
        return "APILimit::#{remaining}/#{hourly_limit} resetTime::#{reset_time}"

    getAPILimit = ->
        $.ajax
            type: "GET"
            #url: "http://192.168.56.101:8000/get_api_limit"
            url: "http://127.0.0.1:8000/get_api_limit"
            dataTpye: "json"
            success: (json) ->
                $('#api_limit').append(createAPILimitFormat(json))
            error: (XMLHttpRequest, textStatus, errorThrown)->
                $('#api_limit').append("さーせん、うまくいかなかったっす")


    getAPILimit()
    #=========================

    #ajaxでとってくる
    #=========================
    getHomeTimeline = ->
        $.ajax
            type: "GET"
            #url: "http://192.168.56.101:8000/get_home_timeline"
            url: "http://127.0.0.1:8000/get_home_timeline"
            dataTpye: "json"
            success: (json) ->
                buildStream(json)
            error: (XMLHttpRequest, textStatus, errorThrown)->
                alert "さーせん、うまくとれなかったっす"

    getLists = ->
        $.ajax
            type: "GET"
            #url: "http://192.168.56.101:8000/get_lists"
            url: "http://127.0.0.1:8000/get_lists"
            dataTpye: "json"
            success: (json) ->
                console.log json
            error: (XMLHttpRequest, textStatus, errorThrown)->
                alert "さーせん、うまくとれなかったっす"

    getListTimeline = (list_owner, list_name, include_rts)->
        $.ajax
            type: "GET"
            #url: "http://192.168.56.101:8000/get_list_timeline/#{list_owner}/#{list_name}/?rts=#{include_rts}"
            url: "http://127.0.0.1:8000/get_list_timeline/#{list_owner}/#{list_name}/?rts=#{include_rts}"
            dataTpye: "json"
            success: (json) ->
                buildStream(json)
            error: (XMLHttpRequest, textStatus, errorThrown)->
                alert "さーせん、うまくとれなかったっす"

    #Streamを組み立てる
    #=========================
    twitter_url =
        url: "https://twitter.com/"
        api: "https://api.twitter.com/1/"

    createTweetdiv = (arg) ->
        tweetdiv = $("<div>")
        tweetdiv.attr('class', 'tweet')
        tweetdiv.attr('id', arg.status_id)

    createImage = (arg) ->
        img = $("<img/>")
        img.attr('src', arg.user_image_url)
        img.attr('alt', arg.screen_name)
        img.attr('class', 'user_icon')

    createUserName = (arg) ->
        user_name = $("<a>")
        if arg.screen_name == arg.name
            display_name= arg.screen_name
        else
            display_name = "#{arg.screen_name}(#{arg.name})"
        user_name.attr('href', twitter_url.url + arg.screen_name)
        user_name.attr('class', 'user_name')
        user_name.text(display_name)

    createText = (arg) ->
        textdiv = $('<div>')
        textdiv.attr('class', 'text')

        tweet = arg.text
        tweet = tweet.replace(/(https?:\/\/[\w\.\,\-\+\?\/\%#=\&\!]+)/ig , "<a href='$1' class='url'>$1</a>")
        tweet = tweet.replace(/@([\a-zA-Z0-9_]+)/g , "<a href=#{twitter_url.url}$1>@$1</a>")
        tweet = tweet.replace(/#([\w一-龠ぁ-んァ-ヴー]+)/g , "<a href=#{twitter_url.url}search/%23$1>#$1</a>")
        if /shindanmaker/.test(tweet)
             tweet = 'また診断メーカーか。'
        if /#[一-龠ぁ-んァ-ヴー０-９]{10,}/.test(tweet)
             tweet = 'また日本語ハッシュタグか'
        if /gohantabeyo/.test(tweet)
             tweet = 'またごはんか'

        textdiv.html(tweet)

    createRTImg = (arg) ->
        img = $('<img/>')
        img.attr('src', arg.old_tweet_user_image_url)
        img.attr('class', 'retweeted')
        img.attr('alt', arg.old_tweet_screen_name)

    createRTSpan = (arg) ->
        span = $('<span>')
        span.text("RT::#{arg.old_tweet_screen_name}")

    createRTcount = (arg) ->
        span = $('<span>')
        retweeted_count = parseInt(arg.retweeted_count) + 1
        span.text("&#{retweeted_count}")

    createTimeLink = (arg) ->
        timelink = $('<a>')
        timelink.attr('href', "#{twitter_url.url}#{arg.screen_name}/status/#{arg.status_id}")
        timelink.attr('class', 'time')
        time = createDateTimeFormat(new Date(arg.created_at))
        timelink.text(time)

    createReplyButton = ->
        button = $('<img/>')
        button.attr('src', 'static/image/reply.png')
        button.attr('alt', 'replyButton')
        button.attr('class', 'reply')

    createFavButton = ->
        button = $('<img/>')
        button.attr('src', 'static/image/favorite.png')
        button.attr('alt', 'FavButton')
        button.attr('class', 'fav')

    createRTButton = ->
        button = $('<img/>')
        button.attr('src', 'static/image/retweet.png')
        button.attr('alt', 'RTButton')
        button.attr('class', 'retweet')

    buildStream = (json) ->
       for arg in json
           tweetdiv = createTweetdiv(arg)
           $("#column1").append(tweetdiv)
           tweetdiv.append(createImage(arg))
           tweetdiv.append(createUserName(arg))
           tweetdiv.append(createText(arg))
           tweetdiv.append(createTimeLink(arg))
           tweetdiv.append(createReplyButton())
           tweetdiv.append(createFavButton())
           tweetdiv.append(createRTButton())
           #公式RTの場合
           if arg.old_tweet_screen_name
               tweetdiv.append(createRTImg(arg))
               tweetdiv.append(createRTSpan(arg))
               tweetdiv.append(createRTcount(arg))

    buildColumn = ->
        column_id = 0
        incID: ->
            column_id++
        getCloumnID: ->
            return column_id
    #=========================

    #各ボタンのホバーイベント
    #=========================
    $('.reply').live("mouseenter", ->
        $(@).attr('src', 'static/image/reply_hover.png')
    )
    $('.reply').live("mouseleave", ->
        $(@).attr('src', 'static/image/reply.png')
    )
    $('.fav').live("mouseenter", ->
        $(@).attr('src', 'static/image/favorite_hover.png')
    )
    $('.fav').live("mouseleave", ->
        $(@).attr('src', 'static/image/favorite.png')
    )
    $('.retweet').live("mouseenter", ->
        $(@).attr('src', 'static/image/retweet_hover.png')
    )
    $('.retweet').live("mouseleave", ->
        $(@).attr('src', 'static/image/retweet.png')
    )

    #=========================
    #試験的に実行している
    #getHomeTimeline()
    #getLists()
    #getListTimeline("__altnight__", "list2", "True")
    mainStream = ->
        #getHomeTimeline()
        getListTimeline("altnight", "skz", "True")
    #build_column = buildColumn()
    mainStream()
    #=========================
