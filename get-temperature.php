<?php

function mysqli_result($res,$row=0,$col=0){
    $numrows = mysqli_num_rows($res);
    if ($numrows && $row <= ($numrows-1) && $row >=0){
        mysqli_data_seek($res,$row);
        $resrow = (is_numeric($col)) ? mysqli_fetch_row($res) : mysqli_fetch_assoc($res);
        if (isset($resrow[$col])){
            return $resrow[$col];
        }
    }
    return false;
}

$serverip=ip-adres
$portnumber=port-number
$username="username";
$password="password";
$database="temperatuur_database";

$con=mysqli_connect($serverip:$portnumber,$username,$password);

if (mysqli_connect_errno()) {
  echo "Failed to connect to the SQL-database: " . mysqli_connect_error();
  exit;
}

mysqli_select_db($con,$database) or die( "Unable to select the database");

$query="SELECT * FROM temperatuurLog ORDER BY temperatuurLog.date DESC , temperatuurLog.time DESC LIMIT 1";
$result=mysqli_query($con,$query);

$num=mysqli_fetch_row($result)[0];

mysqli_close($con);


        $dateAndTemps = array();
        $origdate = mysqli_result($result,0,"date");
        $date = date("d/m/Y", strtotime($origdate));
        $origtime = mysqli_result($result,0,"time");
        $time = date("H:i", strtotime($origtime));
        $temp = mysqli_result($result,0,"temperature");

        $dateAndTemps["Date"] = $date;
        $dateAndTemps["Time"] = $time;
        $dateAndTemps["Temperature"] = $temp;
        $tempValues=$dateAndTemps;

header('Content-Type: application/json');
echo json_encode($tempValues);

?>
