$(function() {

    function Octopus(){
        this.searchText = $("#search-text");

    }
    Octopus.prototype.init=function(){
        this.addStar();
        this.addSlider();
        this.addAutoComplete();
    };
    Octopus.prototype.addStar=function(){
        $('.input-3').rating({displayOnly: true, step: 0.5});
    }
    Octopus.prototype.addSlider=function(){
           $(".content-slider").lightSlider({
                    loop:true,
                    keyPress:true
                });
    }

    Octopus.prototype.addAutoComplete=function(){
        $( "#search_query" ).autocomplete({
            source: function (request, response) {
              $.ajax({
                  url: '/book_names/'+request.term,
                  delay:400,
                  success: function (data) {
                      response(data);
                  },
                  error: function () {
                      response([]);
                  }
              });
          },
          minLength: 2,
          select: function(event, ui) {
              var nextUrl = "/search_book/" +  ui.item.value ;
              window.location.href = nextUrl;
          }
        });
    }

    octopus = new Octopus();
    octopus.init();
});
