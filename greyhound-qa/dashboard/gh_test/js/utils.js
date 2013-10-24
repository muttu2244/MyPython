//------------------------LOADING FUNCTION (ALL - MULTITENANT)-------------------------------------------------------------------
function load(file)
{
        var game = sessionStorage.getItem("GAME_ID");
        if (game != null && game != '')
                var page = file + '?Game_ID=' + game;
        else
                var page = file;
        console.log(page);
        window.location.href = page;
}

//-----------------------CLICK FUNCTIONS (CONSTANT.PHP/POOLS.PHP/RESULTS.PHP)--------------------------------
var time = 300, clicks = 0, timer = null;
function animat()
{
                clicks++;
                if (clicks == 1)
                {
                        timer = setTimeout(function()
                        {
                                //alert("Single Click");
                                clicks = 0;
                                load("web.php");
                        },time);
                }
                else
                {
                        clearTimeout(timer);
                        //alert("Double Click");
                        clicks = 0;
                        ghweb_panel_animation();
                        setTimeout( function()
                        {
                                load("index.php");
                        },600);

                }

}

//-------------------------------------GET VERSION FUNCTIONS--------------------------------------------------
function index_get_version()
{
        var access = sessionStorage.getItem("ACCESS");
                var make_ajax = false;
                if (access != null)
                {
                        var value = parseInt(access);
                        if ( value%5 == 0)
                                make_ajax = true;
                        sessionStorage.setItem("ACCESS",value+1);
                }
                else
                {

                        sessionStorage.setItem("ACCESS","2");
                        make_ajax = true;
                }
                if (make_ajax)
                {
                        var data = "Version=get";
                        console.log(data);
                        $.ajax(
                        {

                          url : "handler.php",
                          type: "POST",
                          data: data,
                        success: function (data)
                        {
                                console.log(data);
                                var str_web = "Greyhound Web-" + data;
                                var str_client = "Greyhound Client-" + data;
                                $("#display1").text(str_web);
                                $("#display3").text(str_client);
                                VERSION = data;
                                sessionStorage.setItem("VERSION",data);
                        }
                        } );
                }
                else
                {

                        var version = sessionStorage.getItem("VERSION");
                        console.log(version);

                        var str_web = "Greyhound Web-" + version;
                        var str_client = "Greyhound Client-" + version;
                        $("#display1").text(str_web);
                        $("#display3").text(str_client);

                }

}
function get_version()
        {
                var access = sessionStorage.getItem("ACCESS");
                if (access == null)
                {
                        sessionStorage.setItem("ACCESS","1");
                        var data = "Version=get";
                        console.log(data);
                        $.ajax(
                        {

                          url : "handler.php",
                          type: "POST",
                          data: data,
                        success: function (data)
                        {
                                console.log(data);
                                var str_web = "Greyhound Web-" + data;
                                var str_client = "Greyhound Client-" + data;
                                $("#display1").text(str_web);
                                $("#display3").text(str_client);
                                VERSION = data;
                                sessionStorage.setItem("VERSION",data);
                        }
                        } );
                }
                else
                {
                        var version = sessionStorage.getItem("VERSION");
                        console.log(version);

                        var str_web = "Greyhound Web-" + version;
                        var str_client = "Greyhound Client-" + version;
                        $("#display1").text(str_web);
                        $("#display3").text(str_client);

                }

        }

function ghclient_get_version()
        {
                var access = sessionStorage.getItem("ACCESS");
                console.log(access)
               if (access == null)
                {
                        sessionStorage.setItem("ACCESS","1");
                        var data = "Version=get";
                        console.log(data);
                        $.ajax(
                        {

                          url : "handler.php",
                          type: "POST",
                          data: data,
                        success: function (data)
                        {
                                console.log(data);
                                var str_web = "Greyhound Web-" + data;
                                var str_client = "Greyhound Client-" + data;
                                $("#display1").text(str_web);
                                $("#display3").text(str_client);
                                VERSION = data;
                                sessionStorage.setItem("VERSION",data);
                        }
                        } );
                }
                else
                {
                        var version = sessionStorage.getItem("VERSION");
                        console.log(version);

                        var str_web = "Greyhound Web-" + version;
                        var str_client = "Greyhound Client-" + version;
                        console.log(str_client);
                        $("#display1").text(str_web);
                        $("#display3").text(str_client);

                }

        }


//----------------------------------RESULTS.PHP FUNCTIONS-----------------------------------------------------
function dropdown_change()
{
               var name = $("#mydropdown").val();
                if (name != "default")
                {
                        var path = 'scripts/test/results/';
                        path = path + $("#mydropdown").val() + '.html';
                        document.getElementById("load_frame").style.display = "block";
                        $('#load_frame').load(path);
                        fetch_chart(name);
                        $("#chart").css({display:"block"});
                }

                else
                {
                        document.getElementById("load_frame").style.display = "none";
                        document.getElementById("chart").style.display = "none";
                }

}
function refresh()
{
                $("#load_frame").css({display:"none"});
                $("#chart").css({display:"none"});
                $("#loading_box").css({display:"block"});
                $("#loading_box").showLoading();
                var data = 'Refresh=flush results';
                console.log(data);
                $.ajax(
                {

                  url : "handler.php",
                  type: "POST",
                  data: data,
                 success: function (data)
                {
                        console.log(data);
                        $("#loading_box").css({display:"none"});
                        $("#loading_box").hideLoading();
                        if (data == "Flushed")
                        {
                                sessionStorage.setItem("PIE",'0,0,0,0,0,');

                              jSuccess("Results Flushed!!!",{
                                        autoHide : true, // added in v2.0
                                        clickOverlay : false, // added in v2.0
                                        MinWidth : 150,
                                        TimeShown : 1000,
                                        ShowTimeEffect : 200,
                                        HideTimeEffect : 200,
                                        LongTrip :20,
                                        HorizontalPosition : 'right',
                                        VerticalPosition : 'top',
                                        ShowOverlay : true,
                                        ColorOverlay : '#000',
                                        OpacityOverlay : 0.3,
                                        onClosed : function(){ },
                                        onCompleted : function(){ }
                                        });
                        }
                        load("results.php");
                }
                });
}

//---------------------------------------------WEB.PHP FUNCTIONS------------------------------------------
function display_drop(game_id)
{
        var data = 'Drop=' + game_id;
        console.log(data);
        $.ajax(
        {
                url : "handler.php",
                type: "POST",
                data: data,
                success: function (data)
                {
                        console.log(data);
                        $("#id_drop").html(data);
                        config_id();
                }
        });
}

function config_id()
{
        var data = 'Game_ID='+ $("#id_drop").val();
        data = data + '&Config=create config';
        console.log(data);
        $.ajax(
        {
                url : "handler.php",
                type: "POST",
                data: data,
                success: function (data)
                {
                        console.log(data);
                        if (data != 'not created')
                        {
                                var parts = data.split('\n');
                                console.log(parts);
                                var secret = '  ' + parts[1];
                                var name = '  ' + parts[2];
                                $("#text_sec").text(secret);
                                $("#text_name").text(name);
                                $("#label_name").text(parts[2]);


                        }
                        else
                        {
                                jError("Unable to create!!!",{
                                        autoHide : true, // added in v2.0
                                        clickOverlay : false, // added in v2.0
                                        MinWidth : 150,
                                        TimeShown : 1500,
                                        ShowTimeEffect : 200,
                                        HideTimeEffect : 200,
                                        LongTrip :20,
                                        HorizontalPosition : 'right',
                                        VerticalPosition : 'top',
                                        ShowOverlay : true,
                                        ColorOverlay : '#000',
                                        OpacityOverlay : 0.3,
                                        onClosed : function(){ },
                                        onCompleted : function(){ }
                                        });

                        }
                }
        });
}
function run()
{
                $("#loading_box").css({display:"block"});
                $("#loading_box").showLoading();

                var data = $("#form_tests").serialize();
                console.log(data);
                $.ajax(
                {

                  url : "handler.php",
                  type: "POST",
                  data: data,
                success: function (data)
                {
                        console.log(data);
                        $("#loading_box").css({display:"none"});
                        $("#loading_box").hideLoading();
                        sessionStorage.setItem("PIE",data);
                        if (data != '0,0,0,0,0,' && data != '')
                        {
                                jSuccess("Done!!!",{
                                        autoHide : true, // added in v2.0
                                        clickOverlay : false, // added in v2.0
                                        MinWidth : 150,
                                        TimeShown : 1500,
                                        ShowTimeEffect : 200,
                                        HideTimeEffect : 200,
                                        LongTrip :20,
                                        HorizontalPosition : 'right',
                                        VerticalPosition : 'top',
                                        ShowOverlay : true,
                                        ColorOverlay : '#000',
                                        OpacityOverlay : 0.3,
                                        onClosed : function(){ },
                                        onCompleted : function(){ }
                                        });

                                setTimeout(function()
                                {
                                        load("results.php");
                                },200);

                        }
                        else
                        {
                                jError("Error!!!",{
                                        autoHide : true, // added in v2.0
                                        clickOverlay : false, // added in v2.0
                                        MinWidth : 150,
                                        TimeShown : 1500,
                                        ShowTimeEffect : 200,
                                        HideTimeEffect : 200,
                                        LongTrip :20,
                                        HorizontalPosition : 'right',
                                        VerticalPosition : 'top',
                                        ShowOverlay : true,
                                        ColorOverlay : '#000',
                                        OpacityOverlay : 0.3,
                                        onClosed : function(){ },
                                        onCompleted : function(){ }
                                        });

                        }

                }
                } );

}
function default_gid()
{
        var data = 'Find=default';
        console.log(data);
        $.ajax(
        {
                url : "handler.php",
                type: "POST",
                data: data,
                success: function (data)
                {
                        console.log(data);
                        sessionStorage.setItem("GAME_ID",data);
                        var url = document.URL;
                        if (url.indexOf("web.php") != -1)
                                display_drop(data);
                }
        });
}
function cache_game()
{
        var url = document.URL;
        console.log(url);
        var parts = url.split('?Game_ID=');
        console.log(parts);
        if (parts[1] == null)
                default_gid();
        else
        {
                var old_id = sessionStorage.getItem("GAME_ID");
                if (parts[1] == old_id)
                {
                        if (url.indexOf("web.php") != -1)
                                display_drop(parts[1]);
                }
                else
                {
                        sessionStorage.setItem("GAME_ID",parts[1]);
                        if (url.indexOf("web.php") != -1)
                                display_drop(parts[1]);
                }
        }
}
function flush()
{
                $("#loading_box").css({display:"block"});
                $("#loading_box").showLoading();
                var data = 'flush=flush all';
                console.log(data);
                $.ajax(
                {

                  url : "handler.php",
                  type: "POST",
                  data: data,
                success: function (data)
                {
                        console.log(data);
                        $("#loading_box").css({display:"none"});
                        $("#loading_box").hideLoading();
                        if (data == "Flushed")
                        {
                                jSuccess("Servers Flushed!!!",{
                                        autoHide : true, // added in v2.0
                                        clickOverlay : false, // added in v2.0
                                        MinWidth : 150,
                                        TimeShown : 1500,
                                        ShowTimeEffect : 200,
                                        HideTimeEffect : 200,
                                        LongTrip :20,
                                        HorizontalPosition : 'right',
                                        VerticalPosition : 'top',
                                        ShowOverlay : true,
                                        ColorOverlay : '#000',
                                        OpacityOverlay : 0.3,
                                        onClosed : function(){ },
                                        onCompleted : function(){ }
                                        });
                        }
                        else
                        {
                                jError("Fatal Error!!!",{
                                        autoHide : true, // added in v2.0
                                        clickOverlay : false, // added in v2.0
                                        MinWidth : 150,
                                        TimeShown : 1500,
                                        ShowTimeEffect : 200,
                                        HideTimeEffect : 200,
                                        LongTrip :20,
                                        HorizontalPosition : 'right',
                                        VerticalPosition : 'top',
                                        ShowOverlay : true,
                                        ColorOverlay : '#000',
                                        OpacityOverlay : 0.3,
                                        onClosed : function(){ },
                                        onCompleted : function(){ }
                                        });

                        }

                }
                } );

}

//------------------------ANIMATION FUNCTIONS---------------------------------------------
function ghweb_animation()
        {
                $("#box1").animate({left:"1%",top:"8%",width:"12%",height:"21%"},'slow');
                $("#pic").animate({left:"2.5%",top:"9%",width:"9%",height:"17%"},'slow');
                $("#para1").animate({left:"1%",top:"22%",width:"12%",height:"5%"},'slow');
                $("#display1").css({top:"0.25%",size:"3px"});

                $("#box2a").animate({left:"3.5%",top:"33%"},'slow');
                $("#box2b").animate({left:"3.5%",top:"48%"},'slow');
                $("#box2c").animate({left:"3.5%",top:"63%"},'slow');
                $("#box2d").css({display:"none"});

                $("#pic2a").animate({left:"5.5%",top:"36%"},'slow');
                $("#pic2b").animate({left:"5.5%",top:"51%"},'slow');
                $("#pic2c").animate({left:"5.5%",top:"66%"},'slow');

                $("#ghclient_div").css({display:"none"});
                $("#panel").css({display:"block"});
                $("#tile_glass1").css({display:"none"});
                $("#tile_glass2").css({display:"none"});
                $("#tile_glass3").css({display:"none"});
                $("#tile_glass4").css({display:"none"});
                $("#test_link").css({display:"none"});

                $("#pie_header").css({display:"none"});
                $("#label_result").css({display:"none"});
                $("#label_data").css({display:"none"});
        }
function ghclient_animation()
{
                $("#box3").animate({left:"1%",top:"8%",width:"12%",height:"21%"},'slow');
                $("#pic3").animate({left:"2.5%",top:"9%",width:"9%",height:"17%"},'slow');
                $("#para3").animate({left:"1%",top:"22%",width:"12%",height:"5%"},'slow');
                $("#display3").css({top:"0.25%",size:"3px"});

                $("#constants").css({display:"none"});
                $("#pools").css({display:"none"});
                $("#results").css({display:"none"});
                $("#box2d").css({display:"none"});

                $("#ghweb").css({display:"none"});
                $("#panel").css({display:"block"});
                $("#tile_glass1").css({display:"none"});
                $("#tile_glass2").css({display:"none"});
                $("#tile_glass3").css({display:"none"});
                $("#tile_glass4").css({display:"none"});
                $("#test_link").css({display:"none"});
                $("#label_result").css({display:"none"});
                $("#pie_header").css({display:"none"});
                $("#label_data").css({display:"none"});
}
function ghweb_panel_animation()
        {
                $("#box1").animate({top:"28%",left:"34%",width:"15%",height:"25%"},'slow');
                $("#pic").animate({left:"36.5%",top:"29.4%",height:"19%",width:"10%"},'slow');
                $("#para1").animate({left:"34%",top:"44%",height:"7%",width:"15%"},'slow');
                $("#display1").css({top:"15%",bottom:"10%"});

                $("#box2a").animate({left:"34%",top:"54%"},'slow');
                $("#box2b").animate({left:"42%",top:"54%"},'slow');
                $("#box2c").animate({left:"34%",top:"67.5%"},'slow');
                $("#box2d").css({display:"block"});

                $("#pic2a").animate({left:"36%",top:"57%"},'slow');
                $("#pic2b").animate({left:"44%",top:"57%"},'slow');
                $("#pic2c").animate({left:"36%",top:"70%"},'slow');

                $("#ghclient_div").css({display:"block"});
                $("#panel").css({display:"none"});
                $("#test_link").css({display:"block"});
                $("#tile_glass2").css({display:"block"});
                $("#tile_glass4").css({display:"block"});

//-----------------WEB.PHP\CONSTANTS.PHP\POOLS.PHP\RESULTS.PHP------                
                $("#web_container").css({display:"none"});
                $("#web_header").css({display:"none"});
                $("#icon_config").css({display:"none"});
                $("#icon_flush").css({display:"none"});
                $("#icon_run").css({display:"none"});
                $("#web_embed_div").css({display:"none"});
                $("#form_settings").css({display:"none"});
                $("#form_tests").css({display:"none"});
                $("#label_select").css({display:"none"});
                $("#label_config").css({display:"none"});
                $("#label_flush").css({display:"none"});
                $("#label_info").css({display:"none"});
                $("#drop_embed_div").css({display:"none"});
                $("#drop_embed_panel").css({display:"none"});
                $("#gids").css({display:"none"});
                $("#label_game").css({display:"none"});
                $("#label_game_app").css({display:"none"});
                $("#label_game_sec").css({display:"none"});
                $("#label_name").css({display:"none"});
                $("#label_more_config").css({display:"none"});
                $("#text_name").css({display:"none"});
                $("#text_sec").css({display:"none"});

                $("#const_container").css({display:"none"});
                $("#const_frame").css({display:"none"});

                $("#pools_container").css({display:"none"});
                $("#pools_frame").css({display:"none"});

                $("#results_container").css({display:"none"});
                $("#results_header").css({display:"none"});
                $("#results_content").css({display:"none"});
                $("#results_embed_div").css({display:"none"});
                $("#chart").css({display:"none"});
                $("#form_res").css({display:"none"});
                $("#icon_refresh").css({display:"none"});
                $("#label_refresh").css({display:"none"});
                $("#label_view").css({display:"none"});
                $("#label_info_res").css({display:"none"});
                $("#load_frame").css({display:"none"});

        }
function ghclient_panel_animation()
{
                        $("#box3").animate({left:"50%",top:"54%",width:"15%",height:"25%"},'slow');
                        $("#pic3").animate({left:"52.5%",top:"55.4%",height:"19%",width:"10%"},'slow');
                        $("#para3").animate({left:"50%",top:"70%",height:"7%",width:"15%"},'slow');
                        $("#display3").css({top:"10%"});

                        $("#main_div").css({display:"none"});
                        $("#ghclient").css({display:"none"});
                        $("#ghweb").css({display:"block"});
                        $("#panel").css({display:"none"});
                        $("body").css({backgroundImage:"none"});
                        $("#tile_glass2").css({display:"block"});
                        $("#tile_glass4").css({display:"block"});
                        $("#test_link").css({display:"block"});
                        $("#constants").css({display:"block"});
                        $("#pools").css({display:"block"});
                        $("#results").css({display:"block"});
                        $("#box2d").css({display:"block"});
                        $("#ghclient_loading_box").css({display:"none"});

                          setTimeout(function()
                          {
                                 load("index.php");
                          },600);
}
//-----------------GHCLIENT.HTML-----------------------------------

var Z = {};
function remove()
{
        document.getElementById("form_div").style.display = "none";
        document.getElementById("main_div").style.display = "none";
}
function ghclient_run()
                {
                        // For version detection, set to min. required Flash Player version, or 0 (or 0.0.0), for no version detection. 
            var swfVersionStr = "11.1.0";
            // To use express install, set to playerProductInstall.swf, otherwise the empty string. 
            var xiSwfUrlStr = "playerProductInstall.swf";
            var flashvars = {
                // change this to your domain
                //greyhound_url: "http://assetstest.sample.greyhound.zynga.com/Greyhound.swf",^M                                
                gh_services_url: "http://sample.greyhound.zynga.com/services/",
                zcdiff: true,
                mqs_url: "http://ghcluster-staging-mqs-web-01.zc2.zynga.com/services/",
            };
            var params = {};
            params.quality = "high";
            params.bgimage = "bg.png";
            params.allowscriptaccess = "always";
            params.allowfullscreen = "true";
            params.wmode = "transparent";
            var attributes = {};
            attributes.id = "ghclient";
            attributes.name = "ghclient";
            attributes.align = "middle";
            swfobject.embedSWF(
                "ghclient/bin/ghclient.swf", "flashContent",
                "75%", "75%",
                swfVersionStr, xiSwfUrlStr,
                flashvars, params, attributes);
            // JavaScript enabled so display the flashContent div in case it is not replaced with a swf object.
            swfobject.createCSS("#flashContent", "display:block;text-align:left;");

                //      var obj = document.getElementById("ghclient");
        var obj = document.getElementById("ghclient_loading_box");
       obj.style.display = "block";
        obj.style.backgroundImage = 'url(css/images/loading.gif)';
        obj.style.backgroundRepeat = 'no-repeat';
        obj.style.backgroundPosition = '50% 50%';
        obj.style.backgroundColor = 'rgba(154,0,0,0.1)';

        }
function gen_auth(uid)
{

        console.log(uid);
        var jsobject = {};
        jsobject.version = 1;
        jsobject.uid = uid;
	$.post("http://internal.sample.greyhound.zynga.com/services/user.token.issue.php",
        JSON.stringify(jsobject),function(data){
                                                //console.log(data);
                                                Z.auth = {
                                                /* this is a long lasting auth token for the greyhound-config-sample auth */
                                                "getAuthToken" : function() { return data.result.userToken; },

                                                "getAuthZID" : function() { return jsobject.uid; },

                                                "getBlobTypes" : function() { return ["player", "game-world"]; },

                                                "getDeltaTypes" : function() { return ["gift", "visit"]; }
                                                };
                                                console.log(Z.auth.getAuthToken());
                                                },"json");

                                                return true
}
function ghclient_submit()
{
        Object.prototype.isInteger = function ()
        {
                return (this.toString().search(/^-?[0-9]+$/) == 0 )
        }
        var temp = {};
        temp.uid = $("input:first").val();
        if (temp.uid != "" && temp.uid.isInteger() == true)
        {
                gen_auth(temp.uid)
                remove();
                ghclient_run();
        }
        else
        {
                alert("Enter Valid Zid");
        }
        return false;
}

