var displaying_query_id;
var random_pk,reserved_pk;
var NEW_RANDOM_URL, RESERVED_URL;
var NEW_RANDOM_PERIOD_MS;
var CHECK_RESERVED_PAGE_PERIOD_MS;

DIV_TO_UPDATE_ID = 'main_display';

function main_ready()
{
    check_new_random();
    check_reserved();
}

function check_new_random()
{
    $.ajax({
               url: NEW_RANDOM_URL,
               type: 'GET',
               data: {'from': displaying_query_id},
               success: function(result)
               {
                   ++displaying_query_id;
                   random_pk = parseInt(result);
                   if (reserved_pk === 0)
                       display_new_iframe(random_pk);
               }
        });
    setTimeout(check_new_random, NEW_RANDOM_PERIOD_MS);
}


function check_reserved()
{
        $.ajax({
                   url: RESERVED_URL,
                   type: 'GET',
                   success: function(result)
                   {
                       reserved_pk = parseInt(result);
                       if (reserved_pk === 0)
                           display_new_iframe(random_pk);
                       else
                           display_new_iframe(reserved_pk);
                   }
               });
    setTimeout(check_reserved, CHECK_RESERVED_PAGE_PERIOD_MS);
}


function display_new_iframe(resource_pk_to_download_from)
{
    $('#' + DIV_TO_UPDATE_ID).html(
        '<iframe src="' + RESOURCE_URL +
            '?resource_pk=' + resource_pk_to_download_from + '" ' +
            'style="width: 100%; height: 100%; overflow: hidden;" />' );
}