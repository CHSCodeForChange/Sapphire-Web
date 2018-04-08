window.setTimeout(function() {
    $(".alert").fadeTo(500, 0).slideUp(500, function(){
        $(this).remove();
    });
    $('#myModal').on('shown.bs.modal', function () {
  $('#myInput').trigger('focus')
})
}, 1000);
