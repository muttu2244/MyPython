<?php

$options = getopt('g:v');

if(!isset($options['g'])) {
	echo "Usage:\n";
	echo "    php client.php -g <APPNAME> -v\n";
	echo "    -g your app name\n";
	echo "    -v verbose mode (optional)\n";
	exit();
}

$appname = $options['g'];
$verbose = isset($options['v']) ? true : false;

ini_set("hidef.per_request_ini", "/apps/$appname/current/greyhound.ini");
require_once(dirname(__FILE__) . "/../shared/includes/greyhound.inc.php");
require_once (dirname(__FILE__) . "/../shared/includes/config.inc.php");

define('FG_RED', 31);
define('FG_GREEN', 32);
define('FG_YELLOW', 33);
define('BG_RED', 41);
define('BG_GREEN', 42);
define('BG_YELLOW', 43);

class EnvCheck { 

	private $gh_app_secret, $mqs_version, $zid, $fzid, $auth_token, $services_url, $server_url, $content, $blobtype, $deltas, $cas, $verbose, $result;

	public function __construct($verbose) {
		$this->gh_app_secret = GH_APP_SECRET;

		$this->mqs_version = 1; //Read from config?
		
		$this->zid1 = 1; //player 1 zid

		$this->zid2 = 2; //player 2 zid
		
		$this->auth_token_1 = AuthService::issue($this->zid1);
		$this->auth_token_2 = AuthService::issue($this->zid2);

		$this->services_url = GH_SERVICES_URL;

		$this->server_url = str_replace("services/", "", $this->services_url);

		$this->content = json_encode(array("x"=>1, "y"=>2, "z"=>3, "child"=>array("a"=>4, "b"=>5)));

		$this->blobtype = $this->get_blobtype();

		$this->deltas = null;

		$this->verbose = $verbose;

		$this->result = array();
	}

	private function request($auth_token, $url, $data = null, $headers = null)
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
		curl_setopt($ch, CURLOPT_VERBOSE, $this->verbose);
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

	private function request_mqs($auth_token, $api, $request) {
		$request['version'] = $this->mqs_version;
		if (!defined('MQS_INTERNAL_URL')) {
			throw new Exception("MQS_INTERNAL_URL is not defined");
		}
		$url = MQS_INTERNAL_URL . "/" . $api;

		$c = curl_init($url);
		curl_setopt($c, CURLOPT_POST, true);
		curl_setopt($c, CURLOPT_POSTFIELDS, json_encode($request));
		curl_setopt($c, CURLOPT_RETURNTRANSFER, true);
		curl_setopt($ch, CURLOPT_VERBOSE, $this->verbose);
		$headers = array("Content-Type: application/json",
					"X-Operation: " . $api,
					"Z-Authorization: " . $auth_token,
					"Expect: ");
		curl_setopt($c, CURLOPT_HTTPHEADER, $headers);
		return $c;
	}

	private function get_blobtype() {
		$config = new ConfigService();
		$blobtypes = $config->getBlobTypes();
		$blobtype = $blobtypes[0];
		//$blobtype = "game-world";
		return $blobtype;
	}

	//test for crossdomain.xml
	public function test_crossdomain() {
		$r = $this->request($this->auth_token_1, "$this->server_url/crossdomain.xml");
		$output = curl_exec($r);
		$http_code = curl_getinfo($r, CURLINFO_HTTP_CODE);

		$this->result["crossdomain.xml"] = array(
			"http_code" => $http_code,
			"error_code" => 0
		);
	}

	//test for auth token refresh
	public function test_authtoken_refresh() {
		$r = $this->request($this->auth_token_1, "$this->services_url/user.auth_token.refresh.php");
		$output = curl_exec($r);
		$http_code = curl_getinfo($r, CURLINFO_HTTP_CODE);

		$this->result["authtoken-refresh"] = array(
			"http_code" => $http_code,
			"error_code" => 0
		);
	}

	//blob get
	public function test_blob_get() {
		$r = $this->request($this->auth_token_1, "$this->services_url/user.blob.get.php/$this->blobtype");
		$output = curl_exec($r);
		$http_code = curl_getinfo($r, CURLINFO_HTTP_CODE);

		$result = json_decode($output, true);
		$error_code = $result["blobs"][$this->blobtype]["error"];

		$this->cas = $result["blobs"][$this->blobtype]["CAS"];

		$this->result["blob-get"] = array(
			"http_code" => $http_code,
			"error_code" => $error_code
		);
	}

	//blob set
	public function test_blob_set() {
		$setcas = $this->cas === null ? array() : array("If-Match: $this->cas"); //if no cas
		$r = $this->request($this->auth_token_1, "$this->services_url/user.blob.set.php/$this->blobtype", $this->content, $setcas);
		$output = curl_exec($r);
		$http_code = curl_getinfo($r, CURLINFO_HTTP_CODE);

		$result = json_decode($output, true);
		$error_code = $result["error"];

		$this->result["blob-set"] = array(
			"http_code" => $http_code,
			"error_code" => $error_code
		);
	}

	public function test_delta_add() {
		$r = $this->request($this->auth_token_2, "$this->services_url/friend.blob.addDelta.php/$this->zid1/visit", "water");
		$output = curl_exec($r);
		$http_code = curl_getinfo($r, CURLINFO_HTTP_CODE);

		$result = json_decode($output, true);
		$error_code = $result["error"];

		$this->result["add-delta"] = array(
			"http_code" => $http_code,
			"error_code" => $error_code
		);
	}

	public function test_query_delta() {
		$query = json_encode(array("query" => "select * from deltas where type = :type", "params" => array("type" => "visit")));
		$r = $this->request($this->auth_token_1, "$this->services_url/user.blob.queryDeltas.php", $query);
		$output = curl_exec($r);
		$http_code = curl_getinfo($r, CURLINFO_HTTP_CODE);

		$result = json_decode($output, true);
		$error_code = $result["error"];

		$this->result["query-delta"] = array(
			"http_code" => $http_code,
			"error_code" => $error_code
		);
	}

	public function test_query_friend_delta() {
		$query = json_encode(array("query" => "select * from deltas", "params" => array()));
		$r = $this->request($this->auth_token_2, "$this->services_url/friend.blob.queryDeltas.php/$this->zid1", $query);
		$output = curl_exec($r);
		$http_code = curl_getinfo($r, CURLINFO_HTTP_CODE);

		$result = json_decode($output, true);
		$error_code = $result["error"];

		if($error_code == 0) $this->deltas = $result["deltas"];

		$this->result["friend-query-delta"] = array(
			"http_code" => $http_code,
			"error_code" => $error_code
		);
	}

	public function test_delete_delta() {
		if($this->deltas == null) return;

		$ids = array();
		foreach($this->deltas as $delta)
		{
			$ids[] = $delta["delta_id"];
		}

		$deletions = implode(",", $ids);

		$r = request($this->auth_token_1, "$services_url/user.blob.deleteDeltas.php/$deletions");
		$output = curl_exec($r);
	}

	public function test_get_friend_blob() {
		$r = $this->request($this->auth_token_2, "$this->services_url/friend.blob.get.php/$this->zid1/$this->blobtype");
		$output = curl_exec($r);
		$http_code = curl_getinfo($r, CURLINFO_HTTP_CODE);

		$result = json_decode($output, true);
		$error_code = $result["blobs"][$this->blobtype]["error"];

		$this->result["friend-blob-get"] = array(
			"http_code" => $http_code,
			"error_code" => $error_code
		);
	}

	public function test_mqs_graph_add() {
		$graph_types = (defined('GRAPH_TYPES')) ? constant('GRAPH_TYPES') : array('test');

		$request = array();
		$request['graph-type'] = $graph_types[0];
		$request['uid-list'] = array($this->zid2);
		
		$r = $this->request_mqs($this->auth_token_1, "graph.user.add", $request);
		$output = curl_exec($r);
		$http_code = curl_getinfo($r, CURLINFO_HTTP_CODE);
		
		$result = json_decode($output, true);
		$error_code = $result["status"]["error"];

		$this->result["mqs-graph-add"] = array(
			"http_code" => $http_code,
			"error_code" => $error_code
		);
	}

	private function get_formatted_code($code) {
		$col = FG_YELLOW;
		switch($code) {
			case '403': $col = FG_RED; break;
			case '200': $col = FG_GREEN; break;
			case '0': $col = FG_GREEN; break;
		}
		return "\033[01;{$col}m$code\033[0m";
	}

	public function print_result() {
		echo "\n\n----------------\n";
		echo "TEST RESULTS";
		echo "\n----------------\n\n";
		echo "GH_SERVICES_URL: ".GH_SERVICES_URL."\n";
		echo "GH_APP_SECRET: ".GH_APP_SECRET."\n\n";
		foreach($this->result as $test => $info) {
			echo "Test: $test\n";
			echo "HTTP Response Code: {$this->get_formatted_code($info['http_code'])} \n";
			echo "Error Code: {$this->get_formatted_code($info['error_code'])} \n";
			echo "\n";
		}
	}
}

$o = new EnvCheck($verbose);
$o->test_crossdomain();
$o->test_authtoken_refresh();
$o->test_blob_get();
$o->test_blob_set();
$o->test_mqs_graph_add();
$o->test_delta_add();
$o->test_query_delta();
$o->test_query_friend_delta();
$o->test_delete_delta();
$o->test_get_friend_blob();
$o->print_result();
