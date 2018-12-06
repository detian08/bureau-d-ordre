<?php
include"../Classes/annonce.class.php";
$c=new annonce();
$c->delete($_GET['numAnnonce']);
header("location:../Vue/company.php");
?>