<?php
require_once("includes/head.inc.php");
print_navigation(0);
require_once(dirname(__FILE__) . "/../shared/includes/greyhound.inc.php");

echo '<div id = "results_container"></div>';

echo '<div id = "results_embed_div"></div>';

echo '<div id = "results_content" class="content">';
$hd = opendir("scripts/test/results/");

echo "<select id = \"mydropdown\" name = \"my_drop\">";
	echo "<option value= \"default\" selected = \"selected\">---None---</option>";
	while($file = readdir($hd))
        {
                if(($file != '.') && ($file != '..'))
                {
                        $parts = explode(".", $file);
                        if(is_array($parts) && count($parts)>1)
                        {
                                $ext = end($parts);
                                if(($ext == 'htm') || ($ext == 'html'))
                                {
                                        echo "<option value= \"$parts[0]\">$parts[0]</option>";
				}
                        }
                }
        }
        echo '</select>';
echo '</div>';


?>
<div id = "chart" class = "chart_div"></div>

<div id="panel"></div>

<div id = "tile_glass2" style="display:none;"></div>

<div id = "tile_glass4" style="display:none;"></div>

<div id = "results_header"></div>

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

<div id = "icon_refresh"></div>

<form method="post" id = "form_res"><input type="image" src = "css/images/support.png" alt = "Flush Results" id = "img_refresh" name="Refresh" value="Flush Results"/></form>

<p id = "label_view">View Test Results</p>
<p id = "label_refresh">Flush</p>
<p id = "label_info_res">To rerun test cases, click on Web.</p>

<div id = "load_frame"></div>

<script type="text/javascript">
        $("#ghweb_panel")
        .bind("click",function(e) 
        {
                animat();
	})
	 .bind("dblclick",function(e)
        {
                e.preventDefault();
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
	
	$("#img_refresh").click(function()
	{

		refresh();
		return(false);
	});

	$("#mydropdown").change(function()
	{
		dropdown_change();
	});
	
	$(document).ready(function()
        {
		get_version();
		cache_game();
	});
</script>
