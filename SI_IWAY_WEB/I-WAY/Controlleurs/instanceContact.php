<?php
include "../Classes/contact.class.php";
$e=new contact();

	$e->nom=$_POST['nom'];
	$e->email=$_POST['email'];
	$e->tel=$_POST['tel']; 
	$e->comm=$_POST['comm']; 
	$e->insertion();
header("location:../Vue/index.html");
?>