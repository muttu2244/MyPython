<?php
require_once("includes/head.inc.php");

print_navigation(1); //top navigation menu

?>
<div id = "const_container"></div>
<div id = "const_frame" class="content">

<?php
$consts = array(
	'GH_GAME_ID', 
	'GH_APP_SECRET',
	'APP_NAMESPACE',
	'GH_SERVICES_URL',
	'GH_ADMIN_SERVICES_URL',
	'STORAGE_CONFIG',
	'ACL_FILE',
	'ACL_CACHE',
	'ZRUNTIME_PRODUCT_KEY',
	'ZRUNTIME_NAMESPACE_KEY',
	'BYPASS_ZRT',
	'ENABLE_ZPERFMON',
	'ZPERFMON_INCLUDE_FILE',
	'greyhound.game.env',
	'MB_OBJECTS_MASTER',
	'MB_SECRET_MASTER',
	'MB_DELTAS_MASTER',
	'MQS_URL',
	'MQS_INTERNAL_URL'
);

$tbl_struct = array(
	array(
		"label" => "Key",
		"bold" => 1
	),
	array(
		"label" => "Value"
	)
);

$tbl_data = array();
$i = 0;

foreach($consts as $const) {
	$val = get_const($const);
	$tbl_data[$i][] = $const;
	$tbl_data[$i][] = $val ? $val : "<b><i>-- Undefined --</i></b>";
	$i++;
}

$markup = TableMarkup::get_table_markup($tbl_struct, $tbl_data);
echo $markup;
?>
</div>

<div id = "gid_container"></div>

<?php
if (isset($_GET['Game_ID']))
	$name = $_GET['Game_ID'];
else
{	
	$name = null;
	$flag = 0;
}

echo '<div id = "gid">';
$hd = opendir("/apps/");
echo "<select id = \"const_drop\" name = \"my_drop\">";
        while($file = readdir($hd))
        {
                if(($file != '.') && ($file != '..'))
                {
			if ($name == null)
			{
				if ($flag == 0)
                		{
					echo "<option selected = \"selected\" value= \"$file\">$file</option>";
                			$flag = 1;
				}
				else
					echo "<option value= \"$file\">$file</option>";
			}
			else
			{
				if ($file == $name)
					echo "<option selected = \"selected\" value= \"$file\">$file</option>";
				else
					echo "<option value= \"$file\">$file</option>";
			}
		}
        }
        echo '</select>';
echo '</div>';
?>

<p id = "label_gid">Game ID:</p>
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
	$("#const_drop").change(function()
	{
		var name='constants.php?Game_ID=' + $("#const_drop").val();
		window.location.href = name;
	});
	$(document).ready(function()
        {
		get_version();
	});

</script>
<?php require_once("includes/foot.inc.php"); ?>
