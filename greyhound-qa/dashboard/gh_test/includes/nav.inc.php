<?php
/**
* Generates the top navigation menu
* $page_idx is the current page id (0,1,2...)
*/
function print_navigation($page_idx) {
	$class = array('','','','','');
	$class[$page_idx] = 'current';
	$href = array(
		"index.php",
		"constants.php",
		"pools.php",
		"ghclient.html",
		"web.php"
	);
	
echo <<<EOF
	<div id="navigation">
		<ul class="menu">
			<li><a class='none' style="visibility:hidden;"></a></li>
			<li><a class='none' style="visibility:hidden;"></a></li>
			<li><a class='none' style="visibility:hidden;"></a></li>
			<li><a class='none' style="visibility:hidden;"></a></li>
			<li><a class='none' style="visibility:hidden;"></a></li>	
			<li><a class='{$class[0]}' href='{$href[0]}'>Home</a></li>
			<li><a class='{$class[4]}' href='{$href[4]}' id="web">Web</a></li>
			<li><a class='{$class[1]}' href='{$href[1]}'>Constants</a></li>
			<li><a class='{$class[2]}' href='{$href[2]}'>Pools</a></li>
			<li><a class='{$class[3]}' href='{$href[3]}'>Client</a></li>	
		</ul>
	</div>

	<script type="text/javascript">
		$(document).ready( function ()
		{
			document.getElementById("panel").style.height = $(document).height();
		});
	</script>
EOF;
}
