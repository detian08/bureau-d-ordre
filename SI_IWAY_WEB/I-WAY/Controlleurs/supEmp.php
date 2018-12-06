<?php
include"../Classes/employe.class.php";
$c=new employer();
$c->delete($_GET['cin']);
header("location:../Vue/blogAdmin.php");
?>