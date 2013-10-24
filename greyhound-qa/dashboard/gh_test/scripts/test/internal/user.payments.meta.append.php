<?
require_once(dirname(__FILE__).'/../../shared/includes/admin.inc.php');

//check user Auth
$auth = AuthService::authenticate();

#Check to see if the Auth is valid. If so go ahead else deny
if($auth === null || $auth->authenticated !== true || ($auth->flags->impersonated !== true && $auth->flags->trusted !== true))
{
        $envelope = array("error" => 403, "errorMessage" => "Forbidden");
        output_write_contents($envelope);
        exit();
}


# Parse the various parameters that are obtained from the POST body
$params = json_decode(upload_get_contents(), true);
$payment = $params["payment"];
$paymentObj = new PaymentsMetaService($auth);
$envelope = $paymentObj->append($payment);

output_write_contents($envelope);

