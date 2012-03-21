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

    #現在時刻を設定する
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
