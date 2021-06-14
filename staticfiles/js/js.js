$(document).ready(function() {
    var termTemplate = "<span style='font-weight: bold;'>%s</span>";
    $("#course_number").autocomplete({
        position: {
            my : "right top",
            at: "right bottom"
        },
        source: "suggest.php?action=1",
        minLength: 4,
        search: function(e, ui) {
            $("#searching1").css("background-image", "url('ajax-loader.gif')");
        },
        response: function(e, ui) {
            $("#searching1").css("background-image", "none");
        },
        open: function(e, ui) {
            var acData = $(this).data('uiAutocomplete');
            var styledTerm = termTemplate.replace('%s', acData.term);

            acData.menu.element.find('li').each(function() {
                var me = $(this);
                me.html( me.text().replace(acData.term, styledTerm) );
            });
        },
        select: function( event, ui ) {
            if(ui.item) {
                loadChart(ui.item.course_number, ui.item.course_name);
            }
        }
    }).bind("click", function(e) {
        $("#course_name").val("");
        $("#course_number").val("");
    });
});

$(document).ready(function() { 
    var termTemplate = "<span style='font-weight: bold;'>%s</span>";
    $("#course_name").autocomplete({
        position: {
            my : "right top",
            at: "right bottom"
        },
        source: "suggest.php?action=2",
        minLength: 4,
        search: function(e, ui) {
            $("#searching2").css("background-image", "url('ajax-loader.gif')");
        },
        response: function(e, ui) {
            $("#searching2").css("background-image", "none");
        },
        open: function(e, ui) {
            var acData = $(this).data('uiAutocomplete');
            var styledTerm = termTemplate.replace('%s', acData.term);

            acData.menu.element.find('li').each(function() {
                var me = $(this);
                me.html( me.text().replace(acData.term, styledTerm) );
            });
        },
        select: function( event, ui ) {
            if(ui.item) {
                loadChart(ui.item.course_number, ui.item.course_name);
            }
        },
    }).bind("click", function(e) {
        $("#course_name").val("");
        $("#course_number").val("");
    });
});