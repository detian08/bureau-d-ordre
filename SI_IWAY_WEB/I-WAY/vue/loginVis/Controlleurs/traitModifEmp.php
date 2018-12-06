<?php
include"../Classes/employe.class.php";
$c=new employer();
$c->nom=$_POST['nom'];
$c->prenom=$_POST['pre'];
$c->email=$_POST['email'];
$c->poste=$_POST['poste'];
$c->age=$_POST['age'];
$c->adresse=$_POST['adr'];
$c->tel=$_POST['tel'];
$res=$c->update($_POST['cin']);
header("location:../Vue/blogAdmin.php");

?>