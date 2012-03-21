$(document).ready ->
    $('#status').on('focus', ->
        @.style.rows = 8
        @.style.cols = 80
        @.style.width = "400px"
        @.style.height = "80px"
    )
    $('#status').on('blur', ->
        @.style.rows = 1
        @.style.cols = 30
        @.style.width = "227px"
        @.style.height = "13px"
    )
    $('#status').on('keyup', (ev)->
        if ev.keyCode == 13 #Enter
            alert '発言しました'
            $.ajax
                type: "GET"
                data:
                    q: $('#status').val()
                url: "http://192.168.56.101:8000/update_status"
                dataTpye: "json"
            テキストエリアを消す
            $('#status').val('')
    )
