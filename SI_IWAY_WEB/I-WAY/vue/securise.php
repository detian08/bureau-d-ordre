<?php
include"../Classes/admin.class.php";
$s=new  admin();
if( isset($_SESSION['login']) && isset($_SESSION['pass']))
header("location:loginAdmin/vue/indexadmin.html");
else 
header("location:err.html");
?>