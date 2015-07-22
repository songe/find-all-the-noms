// scrape from http://offthegridsf.com/vendors

// import jQuery
var jq = document.createElement('script');
jq.src = "https://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js";
document.getElementsByTagName('head')[0].appendChild(jq);
jQuery.noConflict();

// parse & generate models
models = [];
$('.otg-vendor').map(function(i, vendor) {
    var name = $(vendor).find('.otg-vendor-name-link').text().trim();
    // e.g. "Big Ed's Buzzard BBQ & Co." => "big-eds-buzzard-bbq-co"
    var id = name.replace(/['.()]/g, "").replace(/(\s\&\s)|\s/g, "-").toLowerCase();
    var website = $(vendor).find('.otg-vendor-name-link').attr('href');
    var description = $(vendor).find('.otg-vendor-cuisines').text().trim();

    var model = {
        "fields": {
            "description": description,
            "name": name,
            "website": website,
        },
        "model": "offthegrid.vendor",
        "pk": id
    };
    models.push(model);
});
copy(models);
