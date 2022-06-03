$(function(){
    $(".increment").click(function(){
      var count = parseInt($("~ .count", this).text());
      
      if($(this).hasClass("up")) {
        var count = count + 1;
        
         $("~ .count", this).text(count);
      } else {
        var count = count - 1;
         $("~ .count", this).text(count);     
      }
      
      $(this).parent().addClass("bump");
      
      setTimeout(function(){
        $(this).parent().removeClass("bump");    
      }, 400);
    });
  });