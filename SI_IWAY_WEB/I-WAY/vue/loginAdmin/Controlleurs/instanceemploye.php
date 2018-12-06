<?php
include "../Classes/employe.class.php";
$e=new employer();

	$e->cin=$_POST['cin'];
	$e->nom=$_POST['nom'];
	$e->prenom=$_POST['pre'];
	$e->email=$_POST['email'];
	$e->poste=$_POST['poste'];
	$e->age=$_POST['age'];
	$e->adresse=$_POST['adr'];
	$e->tel=$_POST['tel']; 
	$e->photo="../Images/".$_POST['photo']; 
	$e->insertion();
header("location:../Vue/blog.php");
?>