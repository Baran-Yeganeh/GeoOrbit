
$('#testButton').click(function() {
    $('h1').text('Welcome to GeoOrbit. ')});

$(document).ready(function() {
    console.log($('h1'))});    

$("#searchInput").keyup(function() {
    console.log($('#searchInput').val())}); 
console.log($);    




$("#searchInput").keyup(function() {
    if ($('#searchInput').val() === '' ){
        $('#searchResults').html("");
        return;
    }
    $.ajax({
    url: '/gnss/testjava/',
    method: 'GET',
    data: {
        name: $('#searchInput').val() 
    },
    success: function(response) {
       $('#searchResults').html("");

       if (response.mission.length === 0){
             $('#searchResults').append("<div>" + 'no mission found' + "</div>")
       }
       else{
                response.mission.forEach(function (mission) {
                $('#searchResults').append("<a href='/gnss/missiondetail/" + mission.id +"/'>" +
                    mission.name + "</a><br>"
                );
                });
       }

    }
    })

    }); 


