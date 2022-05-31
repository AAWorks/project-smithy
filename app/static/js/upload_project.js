$('#project_image').bind('change', function () {
    var filename = $("#project_image").val();
    if (/^\s*$/.test(filename)) {
      $(".file-upload").removeClass('active');
      $("#noFile").text("No file chosen..."); 
    }
    else {
      $(".file-upload").addClass('active');
      $("#noFile").text(filename.replace("C:\\fakepath\\", "")); 
    }
  });
$('#team_flag').bind('change', function () {
    var filename = $("#team_flag").val();
    if (/^\s*$/.test(filename)) {
      $(".file-upload-2").removeClass('active');
      $("#noFile2").text("No file chosen..."); 
    }
    else {
      $(".file-upload-2").addClass('active');
      $("#noFile2").text(filename.replace("C:\\fakepath\\", "")); 
    }
  });
  