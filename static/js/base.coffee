$(document).ready ->
    #投稿するところをほげほげする
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

    $('#status').on('keyup', (ev)->
        if ev.keyCode == 13 #Enter
            if max_length < $(@).val().length
                alert '140字を超えています'
                return false
            $.ajax
                type: "GET"
                data:
                    q: $(@).val()
                url: "http://192.168.56.101:8000/update_status"
                dataTpye: "json"
            alert '発言しました'
            #テキストエリアを消す
            $(@).val('')
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
        return "#{remaining}/#{hourly_limit} resetTime::#{reset_time}"

    getAPILimit = ->
        $.ajax
            type: "GET"
            url: "http://192.168.56.101:8000/get_api_limit"
            dataTpye: "json"
            success: (json) ->
                $('#api_limit').append(createAPILimitFormat(json))

    getAPILimit()

    #=========================
    twitter_url =
        url: "https://twitter.com/"
        api: "https://api.twitter.com/1/"

    getHomeTimeline = ->
        $.ajax
            type: "GET"
            url: "http://192.168.56.101:8000/get_home_timeline"
            dataTpye: "json"
            success: (json) ->
                buildStream(json)

    createTweetdiv = (arg) ->
        tweetdiv = $("<div></div>")
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
        user_name.textContent = display_name

    createText = (arg) ->
        textdiv = $('<div></div>')
        textdiv.attr('class', 'text')
        text = arg.text
        textdiv.innerHTML = text

    createTimeLink = (arg) ->
        timelink = $('<a>')
        timelink.attr('href', "#{twitter_url.url}#{arg.screen_name}/status/#{arg.status_id}")
        timelink.attr('class', 'time')
        time = createDateTimeFormat(new Date(arg.created_at))
        timelink.textContent= time

    buildStream = (json) ->
        for arg in json
            debugger
            tweetdiv = createTweetdiv(arg)
            $("#column1").append(tweetdiv)
            tweetdiv.append(createImage(arg))
            tweetdiv.append(createUserName(arg))
            tweetdiv.append(createText(arg))
            tweetdiv.append(createTimeLink(arg))

    getHomeTimeline()
