<?php
include"../Classes/cv.class.php";
	$c= new  cv ();
	$c->$numCv=$_POST['numCv'];
	$c->$nom=$_POST['nom'];
	$c->$prenom=$_POST['prenom'];
	$c->$email=$_POST['email'];
	$c->$region=$_POST['region'];
	$c->$experience=$_POST['experience'];
	$c->$datNaiss=$_POST['datNaiss'];
	$c->$adresse=$_POST['adresse'];
	$c->$tel=$_POST['tel'];
	$c->$formation=$_POST['formation'] ; 
	$c->$competence=$_POST['competence']; 
	$c->$stage=$_POST['stage']; 
	$c->$poste=$_POST['poste']; 
$c->insertion();
header("location:../Vue/index.html");
 ?>