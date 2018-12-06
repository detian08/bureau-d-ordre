<?php
include"../Classes/admin.class.php";
$s=new admin();
$s->login=$_POST['email'];
$s->pass=$_POST['pass'];
$res=$s->rechsession();
$l=$res->fetchColumn(0);
if($l==0)
{
header("location:../Vue/inscription.html");}
else{
$_SESSION['login']=$s->login;
$_SESSION['pass']=$s->pass;
header("location:../Vue/securise.php");
}
?>