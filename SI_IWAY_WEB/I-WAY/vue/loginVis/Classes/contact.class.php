<?php
class contact{

	public $nom;
	public $email;
	public $tel ; 
	public $comm ; 
	
	public function __construct(){
		 }
		     public function insertion(){
    include"../config/config.php";
    $con=new connexion();
    $pdo=$con->CNXbase();
    $req="insert into contact values ('','$this->nom','$this->tel','$this->email','$this->comm')";
    $res=$pdo->exec($req)or print_r($pdo->errorInfo());
    return $res;
    }
}
	?>