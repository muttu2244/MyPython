<?php
if(defined("greyhound.game.env"))
{
        require_once(constant("greyhound.game.env"));
}
else
{
        require_once(dirname(__FILE__).'/../../../shared/config/env.inc.php');
}
require_once(dirname(__FILE__).'/../../shared/includes/greyhound.inc.php');

//check user Auth
$auth = AuthService::authenticate();

/* Check to see if the Auth belongs to Trusted Internal. If so go ahead else
 * deny 
 */
if($auth === null || $auth->authenticated !== true ||
  $auth->flags->trusted !== true)
{
        $envelope = array("status" => array("error" => 403, "description" => "Forbidden"));
        output_write_contents($envelope);
        exit();
}

addDefine('GH_VERSION', 1);
/* Parse the various parameters that are obtained from the POST body
 * Create an array of zids for whom the Golden Blobs of all types have to
 * be updated by the Current Blobs of all types
 */
$params = json_decode(upload_get_contents(), true);
$version = $params["version"];
if ($version != GH_VERSION)
{
  $envelope = array("status" => array("error" => 3, "description" => "Version not supported"));
  output_write_contents($envelope);
  exit();
}

$zidList = $params["uid-list"];
$interval = $params["interval"];

$status = !empty($zidList) && isset($interval);

$envelope = array();

if ($status === true) {
	$envelope[ 'status' ] = array('error' => 0, 'description' => "Success");
	$envelope[ 'result' ] = array();
	$envelope[ 'result' ][ 'partial' ] = false;
	$envelope[ 'result' ][ 'version' ] = GH_VERSION;
	$envelope[ 'result' ][ 'data' ] = array();

    $status = false;
    foreach ($zidList as $zid)
    {
        /* Create a impersonated Auth Token for the zid and carry out the
         * operation 
         */
        $authZid = AuthService::issue($zid, AuthService::INTERNAL_TOKEN, 500); 
        $auth = AuthService::authenticate($authZid);

        /*
         * TODO: Read the below from Config
         */
        $numRevisions = 3;

        /* Archive the blob */
        $storage = new ArchiveStorageService($auth, $interval, $numRevisions);
		$envelope[ 'result' ][ 'data' ][ $zid ] = array();
		$envelope[ 'result' ][ 'data' ][ $zid ][ 'error' ] = ($storage->restoreArchiveBlobs() == true) ? 0 : 500;

		if($envelope[ 'result' ][ 'data' ][ $zid ][ 'error' ] != 0) {
			$envelope[ 'result' ][ 'partial' ] = true;
		}
    }
}
else {
	$envelope[ 'status' ] = array('error' => 500, 'description' => "Incorrect input parameters");
}

output_write_contents($envelope);
