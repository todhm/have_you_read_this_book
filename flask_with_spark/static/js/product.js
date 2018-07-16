$('.input-3').rating({displayOnly: true, step: 0.5});
$('.star_rating').rating({
    step: 1,
    starCaptions: {1: 'Very Poor', 2: 'Poor', 3: 'Ok', 4: 'Good', 5: 'Very Good'},
    starCaptionClasses: {1: 'text-danger', 2: 'text-warning', 3: 'text-info', 4: 'text-primary', 5: 'text-success'}
});
