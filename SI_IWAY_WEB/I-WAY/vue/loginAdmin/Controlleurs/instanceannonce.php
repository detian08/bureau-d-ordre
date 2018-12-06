<?php 
include"../Classes/annonce.class.php";
$a = new annonce ();

$a->poste=$_POST['poste'];
$a->competence=$_POST['competence'];
$a->experience=$_POST['experience'];
$a->salaire=$_POST['salaire'];
$a->dateAnnonce=$_POST['dateAnnonce'];
$a->insertion();
header("location:../vue/company.php");

 
?>