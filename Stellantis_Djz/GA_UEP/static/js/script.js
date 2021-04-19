
$(function () {
    $("#réf").autocomplete({
        source: "/api/get_réf/",
        select: function (event, ui) { //item selected
            AutoCompleteSelectHandler(event, ui)
        },
        minLength: 2,
    });
    
});

function AutoCompleteSelectHandler(event, ui) {
    var selectedObj = ui.item; 
}








