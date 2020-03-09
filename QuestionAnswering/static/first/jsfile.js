$(function() {
    setTimeout(function() { $("#automplete-1").focus(); }, 3000);
    var words_arr = [];
    $.ajax({
        url: '/getwords',
        type: 'GET',
        success: function(response) {
            var arr = response.content.result;
            i = -1;
            while (++i < arr.length) {
                words_arr.push(arr[i]);
            }
        },
        error: function(response) {}
    });
    $("#automplete-1").autocomplete({
        maxResults: 10,
        minLength: 3,
        multiple: true,
        multipleSeparator: " ",
        source: words_arr

    });
    $.ui.autocomplete.filter = function(array, term) {
        var matcher = new RegExp("^" + $.ui.autocomplete.escapeRegex(term), "i");
        return $.grep(array, function(value) {
            return matcher.test(value.label || value.value || value);
        });
    };
    //text to speech
    $('#soundbutton').click(function() {
        $('#soundbutton').addClass("SoundPluse");
        $.ajax({
            url: '/playsnd',
            type: 'GET',
            success: function(response) {
                $('#soundbutton').removeClass("SoundPluse");
                console.log(response.result)
            },
            error: function() {
                $('#soundbutton').removeClass("SoundPluse");
                alert("error in playsound")
            }
        });
    });
    //speech to text
    $('#mic').click(function() {
        $("#automplete-1").val("Listening...");
        $("#automplete-1").attr("disabled", "disabled");
        $('#mic').addClass("Rec");
        $.ajax({
            url: '/openmic',
            type: 'GET',
            success: function(response) {
                if (response.content.result === "NO") {
                    alert("please check your microphone and audio levels");
                    $("#automplete-1").val("");
                } else {
                    var query = response.content.result;
                    query = query.toLowerCase();
                    $("#automplete-1").val(query);
                    setTimeout(function() { $("#Queform").trigger("submit"); }, 1000);
                }
                $("#automplete-1").removeAttr("disabled");
                $('#mic').removeClass("Rec");

            },
            error: function() {
                $("#automplete-1").removeAttr("disabled");
                alert("please check your microphone and audio levels");
                $('#mic').removeClass("Rec");
            }
        });
    });
});