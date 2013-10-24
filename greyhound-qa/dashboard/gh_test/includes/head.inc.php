<!DOCTYPE HTML>
<head>
<title>Greyhound Dashboard</title>

<link rel="stylesheet" type="text/css" href="css/style.css" />
<link rel="stylesheet" type="text/css" href="css/common.css" />
<link rel="stylesheet" type="text/css" href="css/specific.css" />

<link rel="stylesheet" type="text/css" href="css/showLoading.css" />
<link rel="stylesheet" type="text/css" href="css/jNotify.jquery.css" />

<script type="text/javascript" src="http://code.jquery.com/jquery-latest.js"></script>
<script type="text/javascript" src="js/jquery.showLoading.js"></script>
<script type ="text/javascript" src="js/chart.js"></script>
<script type ="text/javascript" src="js/highcharts.js"></script>
<script type ="text/javascript" src="js/chart_build.js"></script>
<script type ="text/javascript" src="js/jNotify.jquery.js"></script>
<script type ="text/javascript" src="js/utils.js"></script>
</head>

<?php
if (isset($_GET['Game_ID']))
{
        $path = '/apps/' . $_GET['Game_ID'] . '/current/greyhound.ini';
        ini_set('hidef.per_request_ini',$path);
}
else
{       $hd = opendir("/apps/");
        while($file = readdir($hd))
        {
                if(($file != '.') && ($file != '..'))
                {
                        $path = '/apps/' . $file . '/current/greyhound.ini';
                        ini_set('hidef.per_request_ini',$path);
                        break;
                }
        }
}

// -------------------------------MULTITENANT  CONFIGURED-----------------------

//ini_set('hidef.per_request_ini','/apps/sodhyan/current/greyhound.ini');
if(defined("greyhound.game.env"))
{
	require_once(constant("greyhound.game.env"));
}
else
{
	require_once(dirname(__FILE__).'/../../../shared/config/env.inc.php');
}

function get_const($const) {
	return (defined($const)) ? constant($const) : null;
}

require_once (dirname(__FILE__) . "/../../shared/includes/greyhound.inc.php");
//require_once (dirname(__FILE__) . "/../../shared/includes/config.inc.php");
require_once('nav.inc.php');
require_once('utils.inc.php');
require_once('table.php');
