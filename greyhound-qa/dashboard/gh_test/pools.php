<?php
require_once("includes/head.inc.php");

print_navigation(2); //top navigation menu

?>
<div id = "pools_container"></div>
<div id = "pools_frame" class="content">

<?php

$golden_blobtypes = ConfigService::getGoldenBlobTypes();
$blobtypes = ConfigService::getBlobTypes();

$blobtypes_map = array();
$pools = array();
$pool_ips = array();
$golden_pool_ips = array();

foreach($blobtypes as $blobtype) {
	$blob_pool = ConfigService::getBlobPool($blobtype);

	$ip = "-- None --";
    $ip_golden = "-- None --";
	
	$golden_blob_pool = "-- None --";
	if(array_search($blobtype, $golden_blobtypes) !== false) {
		$golden_blob_pool = ConfigService::getGoldenBlobPool($blobtype);
	}

	$blobtypes_map[$blobtype] = array(
		"pool" => $blob_pool,
		"golden_pool" => $golden_blob_pool
	);

	if(array_search($blob_pool, $pools) === false) $pools[] = $blob_pool;
	if($golden_blob_pool != "-- None --" && array_search($golden_blob_pool, $pools) === false) $pools[] = $golden_blob_pool;
}

//get pool ips
foreach($pools as $pool) {
	$ips = get_const($pool); //comma separated values
	$pool_ips[$pool] = split(',', $ips);
}	

//generate table for blobtype -> pools map
$tbl_struct = array(
    array(
        "label" => "Blobtype",
        "bold" => 1
    ),
    array(
        "label" => "Pool"
    ),
    array(
        "label" => "Golden Pool"
    )
);
$tbl_data = array();
$i = 0;
foreach($blobtypes_map as $blobtype => $pool_data) {
	$blob_pool = $pool_data["pool"] ? $pool_data["pool"] : "<b><i>-- Undefined --</i></b>";
	$golden_blob_pool = $pool_data["golden_pool"] ? $pool_data["golden_pool"] : "<b><i>-- Undefined --</i></b>";
	$tbl_data[$i][] = $blobtype;
	$tbl_data[$i][] = $blob_pool;
	$tbl_data[$i][] = $golden_blob_pool;
	$i++;
}
$markup = TableMarkup::get_table_markup($tbl_struct, $tbl_data);
echo $markup;


//generate table for pools -> ips 
$tbl_struct = array(
	array(
		"label" => "Pool",
		"bold" => 1
	),
	array(
		"label" => "IPs"
	)
);
$tbl_data = array();
for($i = 0; $i < sizeof($pools); $i++) {
	$pool = $pools[$i];
	$ips = $pool_ips[$pool];
	$ips_str = implode('<br>', $ips);
	$tbl_data[$i][] = $pool;
	$tbl_data[$i][] = $ips_str ? $ips_str : "<b><i>-- Undefined --</i></b>";
}
$markup = TableMarkup::get_table_markup($tbl_struct, $tbl_data);
echo $markup;


//check if MB_GOLDEN_MASTER had ip same as any other pool
$ip_clash = false;
$clash_pool = "";
$clash_ip = "";
$golden_pool = 'MB_GOLDEN_MASTER';
$golden_pool_ips = $pool_ips[$golden_pool];
foreach($pools as $pool) {
	if($pool == $golden_pool) continue;

	$golden_ips = $pool_ips[$golden_pool];
	$other_ips = $pool_ips[$pool];

	foreach($golden_ips as $golden_ip) {
		if(!$golden_ip) continue;
		foreach($other_ips as $other_ip) {
			if($golden_ip == $other_ip) {
				$ip_clash = true;
				$clash_pool = $pool;
				$clash_ip = $golden_ip;
				break;
			}
		}
		if($ip_clash) break;
	}
	if($ip_clash) break;
}

if($ip_clash) {
	print_error("$clash_pool has same ip as $golden_pool ($clash_ip)");
}
?>

</div>

<div id = "gidpools_container"></div>

<?php
if (isset($_GET['Game_ID']))
        $name = $_GET['Game_ID'];
else
{
        $name = null;
        $flag = 0;
}

echo '<div id = "gidpools">';
$hd = opendir("/apps/");
echo "<select id = \"pools_drop\" name = \"pool_drop\">";
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

<p id = "label_gidpools">Game ID:</p>

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
	$("#pools_drop").change(function()
        {
                var name='pools.php?Game_ID=' + $("#pools_drop").val();
                window.location.href = name;
        });
	$(document).ready(function()
        {
		get_version();
	});
 
</script>

<?php require_once("includes/foot.inc.php"); ?>
