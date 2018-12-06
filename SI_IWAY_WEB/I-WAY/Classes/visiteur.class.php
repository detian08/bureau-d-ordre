<?php
class visiteur{
	public $nom;
	public $prenom;
	public $email;
	public $region;
	public $pass;
	public $datNaiss;
	public $sexe;
	public $type;
	
	public function __construct(){
		session_start(); }
	
	public function insertion(){
    include "../config/config.php";
    $con=new connexion();
    $pdo=$con->CNXbase();
    $req="insert into visiteur values ('$this->nom','$this->prenom','$this->email','$this->region','$this->pass','$this->datNaiss','$this->sexe')";
    $res=$pdo->exec($req)or print_r($pdo->errorInfo());
    return $res;
    }
	public function rechsession(){
    include_once"../config/config.php";
    $con=new connexion();
    $pdo=$con->CNXbase();
    $req="select count(*)from visiteur where email='$this->email' and pass='$this->pass'";
	$res=$pdo->query($req)or print_r($pdo->errorInfo());
	return $res;
	}
public function __destruct(){
		//session_unset();
		}
}

?>