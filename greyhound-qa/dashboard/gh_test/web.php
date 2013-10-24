<?php
require_once("includes/head.inc.php");
print_navigation(4);

require_once(dirname(__FILE__) . "/../shared/includes/greyhound.inc.php");
require_once (dirname(__FILE__) . "/../shared/includes/config.inc.php");
?>

<div id = "web_container"></div>
<div id = "game"></div>
<div id = "gids">
	<select id = "id_drop" name = "id_change"></select>
</div>
<div id = "web_header"></div>
<div id = "icon_config"></div>
<div id = "icon_flush"></div>
<div id = "icon_run"></div>

<div id = "web_embed_div"></div>

<div id = "drop_embed_div"></div>
<div id = "drop_embed_panel"></div>
<form method="post" id = "form_settings" style="">
<div class="content">
	<input type="image" id = "img_config" src = "css/images/services.png" name="config"  alt = "Create config file" value="Create config file"/>
	<input type="image" id = "img_flush" src = "css/images/support.png" name="flush" alt = "Flush All Servers" value="Flush all"/>
</div>
</form>

<p id = "label_game_app">Game App Name</p>
<p id = "label_game_sec">Game App Secret</p>
<p id = "label_game">Select Game ID</p>
<p id = "label_more_config"><i>>> more config</i></p>

<p id = "label_name"></p>
<p id = "text_name"></p>
<p id = "text_sec"></p>

<div id = "label_name_panel_exp"></div>
<div id = "label_name_panel_small"></div>
<div id = "label_more_config_panel"></div>

<p id = "label_select">Select Test Cases</p>
<p id = "label_config">Config</p>
<p id = "label_flush">Flush</p>
<p id = "label_info"><i>>>Press 'Ctrl' to select multiple test cases.</i></p>

<form method="post" id = "form_tests">
	<div id = "web_content" class="content">
	
	<select id = "my_drop" name = "my_drop[]" multiple = "multiple">
		<option value="all">---All---</option>
		<option value="blob_unit.py">IStorage</option>
                <option value="iauth_unit.py" >IAuth</option>
		<option value="delta_unit.py" >Delta</option>
                <option value="scoreboard_unit.py" >Scoreboard</option>
                <option value="blob_diff.py">Blob diff</option>
                <option value="MQS_main.py">MQS</option>
		<option value="Internal_unit.py" >Internal</option>
                <option value="admin_unit.py" >Admin</option>
	</select>
	</div>	
	<input type="image" src = "css/images/right_round.png" alt = "Run Tests" id = "img_run" name="submit" value="Run tests"/>
</form>

<div id="panel"></div>

<div id = "tile_glass2" style="display:none;"></div>

<div id = "tile_glass4" style="display:none;"></div>

<div id="ghweb">
        <div id = "box1"></div>
        <div id = "pic"><img id="gh_ic" src="css/images/gh_icr.png"/></div>
        <div id="para1"><p id="display1" style="position:relative;top:0.25%;color:#FFFFFF;"></p></div>
</div>

<div id="constants">
        <div id = "box2a"></div>
        <div id = "pic2a"><img id="const_pic" src="css/images/constant_icon.png"/></div>
</div>

<div id="pools">
        <div id = "box2b"></div>
        <div id = "pic2b"><img id="pools_pic" src="css/images/mbpool_icon.png"/></div>
</div>

<div id ="results">
         <div id = "box2c"></div>
         <div id = "pic2c"><img id="results_pic" src="css/images/result_icon.png"/></div>
</div>


<div id = "box2d" style="display:none;"></div>

<div id = "ghclient_div" style="display:none;">
        <div id = "box3"></div>
        <div id="pic3"><img id="gh_ic2" src="css/images/gh_icr02.png"/></div>
        <div id="para3"><p id="display3"></p></div>
</div>

<div id = "test_link" style="display:none;">
        <div id = "box4"></div>
        <div id="pic4"><img id="test_l" src="css/images/testlink.png"/></div>
</div>

<div id="ghweb_panel"></div>
<div id="constants_panel"></div>
<div id="pools_panel"></div>
<div id="results_panel"></div>

<div id = "loading_box"></div>
<script type="text/javascript">
	$("#drop_embed_div").click(function()
	{
                $("#web_embed_div").css({top:"55%"});
                $("#icon_run").css({top:"62.9%"});
                $("#img_run").css({top:"62.9%"});
                $("#web_content").css({top:"59.3%"});
                $("#label_select").css({top:"54.8%"});
                $("#label_info").css({top:"66.8%"});
		$("#game").css({display:"block"});
		$("#web_container").css({height:"61%"});
		$("#drop_embed_panel").css({display:"block"});
		$("#gids").css({display:"block"});
		$("#label_game").css({display:"block"});
		$("#label_game_app").css({display:"block"});
		$("#label_game_sec").css({display:"block"});	
                $("#label_more_config").css({display:"block"});
                $("#label_more_config_panel").css({display:"block"});
                $("#text_name").css({display:"block"});
                $("#text_sec").css({display:"block"});
                $("#label_name_panel_exp").css({display:"none"});
                $("#label_name_panel_small").css({display:"block"});
	});
	$("#drop_embed_panel").click(function()
	{
                $("#web_embed_div").css({top:"33.7%"});
                $("#icon_run").css({top:"41.6%"});
                $("#img_run").css({top:"41.6%"});
                $("#web_content").css({top:"38%"});
                $("#label_select").css({top:"33.5%"});
                $("#label_info").css({top:"45.5%"});
                $("#game").css({display:"none"});
                $("#web_container").css({height:"40%"});
                $("#drop_embed_panel").css({display:"none"});
                $("#gids").css({display:"none"});
                $("#label_game").css({display:"none"});
                $("#label_game_app").css({display:"none"});
                $("#label_game_sec").css({display:"none"});
                $("#label_more_config").css({display:"none"});
                $("#label_more_config_panel").css({display:"none"});
                $("#text_name").css({display:"none"});
                $("#text_sec").css({display:"none"});
                $("#label_name_panel_small").css({display:"none"});
                $("#label_name_panel_exp").css({display:"block"});
	});
        $("#label_name_panel_exp").click(function()
        {
                $("#drop_embed_div").click();
        });
        $("#label_name_panel_small").click(function()
        {
                $("#drop_embed_panel").click();
        });
        $("#label_more_config_panel").click(function ()
        {
                $("#img_config").click();
        });
	$("#img_run").click(function()
	{
		run();
		return(false);
	});
	
	$("#img_config").click(function()
	{
		load("constants.php");
        	return(false);
        });
	
	$("#img_flush").click(function()
	{
		flush();	
        	return(false);
        });
	$("#ghweb_panel").click(function() 
        {
                ghweb_panel_animation();
                setTimeout(function()
                {
                        load("index.php");
                },600);
        });

        $("#constants_panel").click(function()
        {
                
                load("constants.php");
        });
        $("#pools_panel").click(function()
        {
                load("pools.php");
        });
        $("#results_panel").click(function()
        {
                load("results.php");  
        });
        $("#id_drop").change(function()
        {
                sessionStorage.setItem("GAME_ID",$("#id_drop").val());
                config_id();
        
                return(false);
        });
        $(document).ready(function()
        {
                get_version();
                cache_game();
        });

</script>
