<?php
if (isset($_POST['Game_ID']))
{
	$path = '/apps/' . $_POST['Game_ID'] . '/current/greyhound.ini';
	ini_set('hidef.per_request_ini',$path);
}
else
{	$hd = opendir("/apps/");
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
if (isset($_POST['Find']))
{
        $hd = opendir("/apps/");
        while($file = readdir($hd))
        {
                if(($file != '.') && ($file != '..'))
                {
                        echo($file);
                        break;
                }
        }
}
// -------------------------------MULTITENANT  CONFIGURED-----------------------

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

require_once(dirname(__FILE__) . "/../shared/includes/greyhound.inc.php");

require_once("includes/utils.inc.php");

if( isset($_POST['Refresh']))
{
try {
        unlink("scripts/test/results/blob_unit.html");
        unlink("scripts/test/results/blob_delta.html");
        unlink("scripts/test/results/delta.html");
        unlink("scripts/test/results/iauth.html");
        unlink("scripts/test/results/scoreboard.html");
        unlink("scripts/test/results/internal_unit.html");
        unlink("scripts/test/results/admin_unit.html");
	unlink("scripts/test/results/mqs.html");
	
        unlink("scripts/test/results/blob_unit.csv");
        unlink("scripts/test/results/blob_delta.csv");
        unlink("scripts/test/results/delta.csv");
        unlink("scripts/test/results/iauth.csv");
        unlink("scripts/test/results/scoreboard.csv");
        unlink("scripts/test/results/internal_unit.csv");
        unlink("scripts/test/results/admin_unit.csv");
	unlink("scripts/test/results/mqs.csv");

	echo("Flushed");
}
catch(Exception $e)
{
}
}

if(isset($_POST['Config']))
{
        if(createconfig('./scripts/config/load_config.yaml'))
        {
                echo("created\n");
                $arr = parse_load();
                echo($arr[0]);
                echo($arr[1]);
        }
        else
        {
                echo('not created');
        }
}
function parse_load()
{
        $name = 'scripts/config/load_config.yaml';
        $app_arr = array();
        if (file_exists($name))
        {
                $file = fopen($name,"r");
                while (!feof($file))
                {
                        $line = fgets($file);
                        $parts = array();
                        $parts = explode(":",$line);

                        if ($parts[0] == '  secret')
                                $app_arr[0] = $parts[1];
                        else if ($parts[0] == '  app_namespace')
                                $app_arr[1] = $parts[1];
                }
                fclose($file);
        }
        return($app_arr);
}

if(isset($_POST['flush']))
{
	        $cache = ConfigService::getPoolStorage('MB_OBJECTS_MASTER','MB_DELTAS_MASTER','MB_OPAQUE_MASTER');
	        $cache->flush();
		echo('Flushed');
}

if (isset($_POST['my_drop']))
{
	$all = false;
	foreach($_POST["my_drop"] as $f)
	{
		if ($f == 'all')
		{
			$all = true;
			break;
		}
	}

	if ($all == true)
	{
		exec("python26 scripts/test/internal/Internal_unit.py");
		exec("python26 scripts/test/admin/admin_unit.py");
		exec("python26 scripts/test/public/blob_unit.py");
                exec("python26 scripts/test/public/iauth_unit.py");
                exec("python26 scripts/test/public/delta_unit.py");
                exec("python26 scripts/test/public/scoreboard_unit.py");
                exec("python26 scripts/test/public/blob_diff.py");
		exec("python26 scripts/test/mqs/main.py");
	}
	else
	{
	foreach($_POST["my_drop"] as $f)
        {
                if ($f == "Internal_unit.py")
                {

                        $cmd = "python26 scripts/test/internal/$f";
                        exec($cmd);
                }
                else if ($f == "admin_unit.py")
                {
                        $cmd = "python26 scripts/test/admin/$f";
                        exec($cmd);

                }
		else if (strncmp($f,"MQS_",4) == 0)
		{
			$file = substr($f,4);
			$cmd = "python26 scripts/test/mqs/$file";
			exec($cmd);
		}
                else
                {
                        $cmd = "python26 scripts/test/public/$f";
                        exec($cmd);
                }
        }
	}
	$arr = array();
        $arr[0] = "scripts/test/results/blob_unit.csv";
        $arr[1] = "scripts/test/results/blob_delta.csv";
        $arr[2] = "scripts/test/results/delta.csv";
        $arr[3] = "scripts/test/results/iauth.csv";
        $arr[4] = "scripts/test/results/scoreboard.csv";
        $arr[5] = "scripts/test/results/internal_unit.csv";
        $arr[6] = "scripts/test/results/admin_unit.csv";
	$arr[7] = "scripts/test/results/mqs.csv";
	
        $values = array();
        for ($j=0;$j<5;$j++)
                $values[$j] = 0;

        for($i = 0;$i<8;$i++)
        {
                if (file_exists($arr[$i]))
                {
                        $file = fopen($arr[$i],"r");
                        $line = fgets($file);
                        $line = fgets($file);
                        $parts = array();
                        $parts = explode(",",$line);

                        for ($j=0;$j<5;$j++)
                                $values[$j] = $values[$j] + intval($parts[$j+1]);

                        //echo($line);
                        fclose($file);
                }
        }
        for ($j=0;$j<5;$j++)
        {
                echo($values[$j]);
                echo(',');
        }

}

if(isset($_POST['Version']))
{
		$arr = array();
		$cmd = "rpm -qa | grep greyhound-web";
		exec($cmd,$arr);
		$total = count($arr);
		$parts = explode("-web-",$arr[$total - 1]);
		print_r(end($parts));
}

if(isset($_POST['pie']))
{
	$arr = array();
        $arr[0] = "scripts/test/results/blob_unit.csv";
        $arr[1] = "scripts/test/results/blob_delta.csv";
        $arr[2] = "scripts/test/results/delta.csv";
        $arr[3] = "scripts/test/results/iauth.csv";
        $arr[4] = "scripts/test/results/scoreboard.csv";
        $arr[5] = "scripts/test/results/internal_unit.csv";
        $arr[6] = "scripts/test/results/admin_unit.csv";
	$arr[7] = "scripts/test/results/mqs.csv";

        $values = array();
        for ($j=0;$j<5;$j++)
                $values[$j] = 0;

        for($i = 0;$i<8;$i++)
        {
                if (file_exists($arr[$i]))
                {
                        $file = fopen($arr[$i],"r");
                        $line = fgets($file);
                        $line = fgets($file);
                        $parts = array();
                        $parts = explode(",",$line);

                        for ($j=0;$j<5;$j++)
                                $values[$j] = $values[$j] + intval($parts[$j+1]);

                        //echo($line);
                        fclose($file);
                }
        }
        for ($j=0;$j<5;$j++)
        {
                echo($values[$j]);
                echo(',');
        }

}

if (isset($_POST['Drop']))
{
	$hd = opendir("/apps/");
        while($file = readdir($hd))
        {
                if(($file != '.') && ($file != '..'))
                {
                        if ($file != $_POST['Drop'])
                        {
                                echo "<option value= \"$file\">$file</option>";
                        }
                        else
                        {
                                echo "<option value= \"$file\" selected = \"selected\">$file</option>";
                        }
                }
        }
}
?>
