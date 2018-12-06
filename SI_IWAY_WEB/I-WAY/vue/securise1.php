<?php
include"../Classes/visiteur.class.php";
$s=new  visiteur();

if( isset($_SESSION['login']) && isset($_SESSION['pass']))
{
header("location:loginVis/vue/company.php");}
else 
header("location:err.html");
?>