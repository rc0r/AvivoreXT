<?php

// prep html
echo <<<EOD
<html>
<head>
	<title>AvivoreXT - Management Frontend</title>
</head>
<body>
	<table>
		<tr>
			<td>Timestamp</td>
			<td>Type</td>
			<td>Object</td>
			<td>User</td>
			<td>UserId</td>
			<!--<td>StatusId</td>-->
			<td>Actions</td>
		</tr>
EOD;

$db = new SQLite3('avivore.db') or die('Unable to open database');
// $query = <<<EOD
//   CREATE TABLE IF NOT EXISTS users (
//     username STRING PRIMARY KEY,
//     password STRING)
// EOD;
// $db->exec($query) or die('Create db failed');
// $user = sanitize($_POST['username']);
// $pass = sanitize($_POST['password']);
// $query = <<<EOD
//   INSERT INTO users VALUES ( '$user', '$pass' )
// EOD;
// $db->exec($query) or die("Unable to add user $user");
$result = $db->query('SELECT * FROM Data ORDER BY Type') or die('Query failed');
while ($row = $result->fetchArray())
{ // $row['Message']
	$timestamp= htmlentities( $row['TimeRecv'] );
	$type = htmlentities( $row['Type'] );
	$value = htmlentities( $row['Value'] );
	$user = htmlentities( $row['User'] );
	$userid = htmlentities( $row['UserId'] );
	$tid = htmlentities( $row['TID'] );

	echo <<<EOD
		<tr>
			<td>$timestamp</td>
			<td>$type</td>
			<td>$value</td>
			<td>$user</td>
			<td>$userid</td>
			<!--<td>$tid</td>-->
			<td><a href="fulltext.php?tid=$tid">+</td>
		</tr>
EOD;
}

// finish html
echo <<<EOD
	</table>
</body>
</html>
EOD;

?>
