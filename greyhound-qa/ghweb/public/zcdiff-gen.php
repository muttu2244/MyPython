<?php

define("ZCDIFF_NOP", 0x00);
define("ZCDIFF_COPY", 0x01);
define("ZCDIFF_ADD", 0x02);

function zcdiff_generate($old, $new, $verbose=false)
{
	$old_len = strlen($old);
	$new_len = strlen($new);
	$n = min($old_len, $new_len);
	$prefix = 0;
	$suffix = 0;
	for($i = 0; $i < $n; $i++)
	{
		if($old[$i] != $new[$i])
		{
			$prefix = $i;
			break;
		}
	}

	if($prefix < $old_len)
	{
		$suffix = $old_len - $prefix;
		for($i = 1; $i <= $old_len; $i++)
		{
			if($old[$old_len - $i] != $new[$new_len - $i])
			{
				$suffix = $i - 1;
				break;
			}
		}
	}
	
	$header="ZCD\001".pack("N", 1)."12345678"; # header(nwindows=1,padding=<8-bytes>)
	$ops = array();
	if($prefix != 0)
	{
		$ops[] = pack("CNN", ZCDIFF_COPY, $prefix, 0); # copy $prefix bytes from src offset 0
		if($verbose) echo "\n\n\nCOPY($prefix, 0)\n\n\n";
	}

	if($prefix+$suffix < $new_len)
	{
		$middle = substr($new, $prefix, $new_len-($prefix+$suffix));
		$ops[] = pack("CN", ZCDIFF_ADD, strlen($middle)).$middle; # Add middle_len bytes from diff
		if($verbose) echo "\n\n\nADD('$middle');\n\n\n";
	}

	if($suffix != 0) 
	{
		$ops[] = pack("CNN", ZCDIFF_COPY, $suffix, ($old_len - $suffix)); # copy $suffix bytes from src offset $old_len - $suffix
		if($verbose) echo "\n\n\nCOPY($suffix,".($old_len-$suffix)." )\n\n\n";
	}

	$window=pack("CN3N2", 0, 0, strlen($old), strlen($new), /* reserved */ 0, 0);
	$numops = count($ops);
	$ops = implode($ops);
	$delta = pack("NN", strlen($ops), $numops);

	$zcdiff = $header.$window.$delta.$ops;

	return $zcdiff;
}

$options = getopt("o:");
$pruneargv = array();
foreach ($options as $option => $value) {
  foreach ($argv as $key => $chunk) {
    $regex = '/^'. (isset($option[1]) ? '--' : '-') . $option . '/';
    if ($chunk == $value && $argv[$key-1][0] == '-' || preg_match($regex, $chunk)) {
      array_push($pruneargv, $key);
    }
  }
}

while ($key = array_pop($pruneargv)) unset($argv[$key]);

$program = array_shift($argv);

if(count($argv) < 2)
{
	echo ("Usage: zcdiff-gen.php [-o out.zcdiff] old.blob new.blob\n");
}

$old = file_get_contents($argv[0]);
$new = file_get_contents($argv[1]);


if(isset($options["o"]))
{
	$diff = zcdiff_generate($old, $new, false); #Originally it was True, Made False for not printing the contents of zcdiff file
	file_put_contents($options["o"], $diff);
}
else
{
	$diff = zcdiff_generate($old, $new, false);
	echo $diff;
}
