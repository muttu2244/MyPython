<?php

function get_time($ts) {
	$format = 'd M Y H:i';
	return date($format, $ts);
}

function print_success($msg) {
	echo "<div class='notice success'>$msg</div>";
}

function print_error($msg) {
	echo "<div class='notice error'>$msg</div>";
}

function createconfig($filepath)
{
        $yml = array();
        $file = file_get_contents($filepath);
        if(!$file) {
                return false;
        }
        $yml = yaml_parse($file);
        $yml["storage"]["app_namespace"] = APP_NAMESPACE;
        $yml["storage"]["url"] = $_SERVER["SERVER_NAME"]."/services/";
        $yml["storage"]["secret"] = GH_APP_SECRET;
        $yml["storage"]["game_id"] = GH_GAME_ID;
        $blobtypes = ConfigService::getBlobTypes();
        $deltas = ConfigService::getDeltaTypes();
        $yml["storage"]["delta_type"] = $deltas[0];
        $yml["storage"]["blob_type"] = $blobtypes[0];
	$yml["internal"]["url"] = GH_INT_SERVICES_URL;
	$yml["admin"]["url"] = GH_ADMIN_SERVICES_URL;
        $yml["mqs"]["url"] = MQS_URL;
	$yml["internal"]["gh_memsched"] = GH_MSCHED;
        if(!file_put_contents($filepath,yaml_emit($yml))) {
                return false;
        }
        return true;
}

function request($auth_token, $url, $data = null, $headers = null)
{
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        if($headers != null)
        {
                $headers[] = "Z-Authorization: $auth_token";
        }
        else
        {
                $headers = array("Z-Authorization: $auth_token");
        }
        //$headers[] = "Host: sample.greyhound.zynga.com";
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_UPLOAD, 1);
        curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
        if($data != null)
        {
                $fp = fopen("php://memory" ,"rw");
                fwrite($fp, $data);
                fseek($fp, 0);
                curl_setopt($ch, CURLOPT_INFILE, $fp);
        }
        return $ch;
}
