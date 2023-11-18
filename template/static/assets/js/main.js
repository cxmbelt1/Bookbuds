/* --------------------------------------------
 MAIN FUNCTION
-------------------------------------------- */
$(document).ready(function() {
    

    /* --------------------------------------------------------
	 NAVBAR FIXED TOP ON SCROLL
	----------------------------------------------------------- */
    $(function(){
        "use strict"; 
        if( $(".navbar-standart").length > 0 ){
            $(".navbar-light").addClass("top-nav-collapse");
        } else {
            $(window).scroll(function() {
                if ($(".navbar").offset().top > 10)  {
                    $(".navbar-light").addClass("top-nav-collapse");

                } else {
                    $(".navbar-light").removeClass("top-nav-collapse");
                }
            });
        };
    });
    
      
    
}(jQuery));

