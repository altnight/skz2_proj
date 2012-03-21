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
