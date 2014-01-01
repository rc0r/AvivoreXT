<?php

if(!isset($_GET["tid"]))
	die('Wrong syntax!');

// only numbers are valid
$tid = preg_replace('/[^0-9]/', '', $_GET["tid"]);

// prep html
echo <<<EOD
<html>
<head>
	<title>AvivoreXT - Management Frontend</title>
</head>
<body>
EOD;

$db = new SQLite3('avivore.db') or die('Unable to open database');
$result = $db->query("SELECT User,Message FROM Data WHERE TID=$tid") or die('Query failed');
while ($row = $result->fetchArray())
{
	$msg = htmlentities($row['Message']);
	$user = htmlentities($row['User']);

	echo <<<EOD
	<p>
	<em><a href="https://twitter.com/$user/status/$tid" target="_blank">$user</a></em> &gt; $msg
	</p>
EOD;
}

// finish html
echo <<<EOD
</body>
</html>
EOD;

?>
