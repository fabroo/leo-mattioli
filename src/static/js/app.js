$("#inputGroupFile02").change(function(){

    var input = document.getElementById('inputGroupFile02');

    for (var i=0; i<input.files.length; i++)
    {
        var ext= input.files[i].name.substring(input.files[i].name.lastIndexOf('.')+1).toLowerCase()

        if ((ext == 'jpg') || (ext == 'png')|| (ext == 'jpeg'))
        {
            $("#msg").text("Las fotos seleccionadas son válidas, subilas!")
        }
        else
        {
            $("#msg").text("Fijate que hay algunas fotos con formato no permitido, asegurate que sean PGN, JPG o JPEG, reintenta!")
            document.getElementById("file-picker").value ="";
        }

    }


} );
$("#menu-toggle").click(function(e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
  });