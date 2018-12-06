<?php
include "../Classes/visiteur.class.php";
$p=new visiteur();
$p->nom=$_POST['nom'];
$p->prenom=$_POST['pre'];
$p->email=$_POST['email'];
$p->region=$_POST['reg'];
$p->pass=$_POST['pass'];
$p->datNaiss=$_POST['dat'];
$p->sexe=$_POST['s'];
$p->insertion();
header("location:../Vue/index.html");
?>