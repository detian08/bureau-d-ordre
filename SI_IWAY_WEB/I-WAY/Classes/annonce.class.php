<?php 
class annonce 
{ 
public $poste ; 
public $competence ; 
public $experience ; 
public $salaire ;
public $dateAnnonce ; 
public function __construct(){
		 }
public function insertion(){
    include "../config/config.php";
    $con=new connexion();
    $pdo=$con->CNXbase();
    $req="insert into annonce values ('','$this->poste','$this->competence','$this->experience','$this->salaire','$this->dateAnnonce')";
    $res=$pdo->exec($req)or print_r($pdo->errorInfo());
    return $res;
    }
	
	public function selection(){
    include"../config/config.php";
    $con=new connexion();
    $pdo=$con->CNXbase();
    $req="select * from annonce";
    $res=$pdo->query($req)or print_r($pdo->errorInfo());
    return $res;
    }
	}
?>