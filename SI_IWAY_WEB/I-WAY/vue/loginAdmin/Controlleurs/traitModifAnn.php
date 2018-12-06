<?php
include"../Classes/annonce.class.php";
$c=new annonce();
$c->poste=$_POST['poste'];
$c->competence=$_POST['competence'];
$c->experience=$_POST['experience'];
$c->salaire=$_POST['salaire'];
$c->dateAnnonce=$_POST['dateAnnonce'];
$res=$c->update($_POST['numAnnonce']);
header("location:../Vue/company.php");

?>