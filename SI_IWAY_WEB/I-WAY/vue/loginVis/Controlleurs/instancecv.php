<?php
include"../Classes/cv.class.php";
	$c= new  cv ();
	
	$c->photo="../Images/".$_POST['photo'];
	$c->nom=$_POST['nom'];
	$c->prenom=$_POST['pre'];
	$c->datNaiss=$_POST['dat'];
	$c->tel=$_POST['tel'];
	$c->adresse=$_POST['adr'];
	$c->region=$_POST['reg'];
	$c->email=$_POST['email'];
	
	$c->typebac=$_POST['bac'];
	$c->annbac=$_POST['anbac'];
	$c->lieubac=$_POST['lieubac'];
	
	$c->typedip=$_POST['dip'];
	$c->anndip=$_POST['andip'];
	$c->lieudip=$_POST['lieudip'];
	$i=0;
	$d="";
	$s="";
	$l="";
	
while ($i<count($_POST['dev'])){
$d .=$_POST['dev'][$i];	
$i++;}
while ($i<count($_POST['sys'])){
$s .=$_POST['sys'][$i];	
$i++;}
while ($i<count($_POST['lang'])){
$l .=$_POST['lang'][$i];	
$i++;}
	
	$c->devprog=$d;
	$c->sysexp=$s;
	$c->langue=$l;
	$c->stage=$_POST['stage'];
	$c->experience=$_POST['exp'];
	$c->certif=$_POST['cerf'];
	$c->numAnnonce=$_POST['numAnnonce'];
	
	$c->insertion();

//header("location:../vue/cv/cv.php?numCv=$l[0]")

 ?>