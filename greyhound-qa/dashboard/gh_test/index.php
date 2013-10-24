<?php
require_once("includes/head.inc.php");
print_navigation(0);

require_once(dirname(__FILE__) . "/../shared/includes/greyhound.inc.php");
require_once (dirname(__FILE__) . "/../shared/includes/config.inc.php");
?>

<div id="panel" style="display:none;"></div>

<div id = "tile_glass1"></div>

<div id = "pie_header"></div>

<p id = "label_result">Results</p>

<p id = "label_data">No Data Available</p>

<div id = "tile_glass2"></div>

<div id="tile_glass3"></div>

<div id = "tile_glass4"></div>

<div id="ghweb">
	<div id = "box1" style="position:absolute;top:28%;left:34%;width:15%;height:25%;float:left;webkit-border-radius: 21px 20px 20px 20px;-moz-border-radius: 21px 20px 20px 20px;border-radius: 21px 20px 20px 20px;background-color:#FFFFFF;"></div>
	<div id = "pic" style="position:absolute;float:left;left:36.5%;top:29.4%;height:19%;width:10%;"><img id="gh_ic" style="position:relative;width:100%;height:100%;" src="css/images/gh_icr.png"/></div>
	<div id="para1" style="position:absolute;float:left;left:34%;top:44%;height:7%;width:15%;text-align:center;background-color:rgba(0,0,0,0.3);"><p id="display1" style="position:relative;top:15%;color:#FFFFFF;bottom:10%;"></p></div>
</div>

<div id="constants">
	<div id = "box2a" style="position:absolute;top:54%;left:34%;width:7%;height:12%;float:left;webkit-border-radius: 21px 20px 20px 20px;-moz-border-radius: 21px 20px 20px 20px;border-radius: 21px 20px 20px 20px;background-color:#73B054"></div>
	<div id = "pic2a" style="position:absolute;float:left;left:36%;top:57%;height:6%;width:3%;"><img id="const_pic" style="position:relative;width:100%;height:100%;" src="css/images/constant_icon.png"/></div>
</div>
<div id="pools">
	<div id = "box2b" style="position:absolute;top:54%;left:42%;width:7%;height:12%;float:left;webkit-border-radius: 21px 20px 20px 20px;-moz-border-radius: 21px 20px 20px 20px;border-radius: 21px 20px 20px 20px;background-color:#73B054;"></div>
	<div id = "pic2b" style="position:absolute;float:left;left:44%;top:57%;height:6%;width:3%;"><img id="pools_pic" style="position:relative;width:100%;height:100%;" src="css/images/mbpool_icon.png"/></div>
</div>
<div id ="results">
	<div id = "box2c" style="position:absolute;top:67.45%;left:34%;width:7%;height:12%;float:left;webkit-border-radius: 21px 20px 20px 20px;-moz-border-radius: 21px 20px 20px 20px;border-radius: 21px 20px 20px 20px;background-color:#73B054;"></div>
	<div id = "pic2c" style="position:absolute;float:left;left:36%;top:70%;height:6%;width:3%;"><img id="results_pic" style="position:relative;width:100%;height:100%;" src="css/images/result_icon.png"/></div>
</div>

	<div id = "box2d"></div>

<div id = "ghclient_div">
        <div id = "box3"></div>
        <div id="pic3"><img id="gh_ic2" src="css/images/gh_icr02.png"/></div>
        <div id="para3"><p id="display3"></p></div>
</div>

<div id = "test_link">
        <div id = "box4"></div>
        <div id="pic4"><img id="test_l" src="css/images/testlink.png"/></div>
</div>

<script type="text/javascript">
	$("#test_link").click(function()
	{
		window.open('http://testlink.seg.zynga.com','_newtab');
	});	
	$("#ghweb").click(function()
	{
		ghweb_animation();
		setTimeout( function()
                {
                	load("web.php");
		},600);
	});

	$("#ghclient_div").click(function()
        {
		ghclient_animation();
		setTimeout( function()
                {
                        window.location.href = "ghclient.html";
                },600);

        });
	
	$("#constants").click(function()
	{
		ghweb_animation();
		setTimeout( function()
		{
			load("constants.php");
		},600);
	});
	$("#pools").click(function()
        {
                ghweb_animation();
                setTimeout( function()
                {
                        load("pools.php");
                },600);
        });

	$("#results").click(function()
        {
                ghweb_animation();
                setTimeout( function()
                {
                        load("results.php");
                },600);
        });
	$("#tile_glass3").click(function ()
	{	
		ghweb_animation();
		setTimeout( function()
                {
                        load("results.php");
                },600);
	});
	$(document).ready(function()
	{
		index_get_version();
		get_pie();
                cache_game();
	
	});
</script>
