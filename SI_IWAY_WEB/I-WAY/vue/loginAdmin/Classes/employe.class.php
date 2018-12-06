<?php
class employer{
	
	public $cin;
	public $nom;
	public $prenom;
	public $email;
	public $poste;
	public $age;
	public $adresse;
	public $tel ; 
	public $photo ; 
	
	public function __construct(){
		 }
	
		public function update($cin){
    include "../config/config.php";
    $con=new connexion();
    $pdo=$con->CNXbase();
    $req="update employer SET nom='$this->nom', prenom='$this->prenom', email='$this->email', poste='$this->poste', age='$this->age', adresse='$this->adresse', tel='$this->tel' where cin='$cin'";
    $res=$pdo->exec($req)or print_r($pdo->errorInfo());
	   }
	   
    public function insertion(){
    include"../config/config.php";
    $con=new connexion();
    $pdo=$con->CNXbase();
    $req="insert into employer values ('$this->cin','$this->nom','$this->prenom','$this->email','$this->poste','$this->age','$this->adresse','$this->tel','$this->photo')";
    $res=$pdo->exec($req)or print_r($pdo->errorInfo());
    return $res;
    }
	
	public function selection(){
    include"../config/config.php";
    $con=new connexion();
    $pdo=$con->CNXbase();
    $req="select * from employer";
    $res=$pdo->query($req)or print_r($pdo->errorInfo());
    return $res;
    }
	
	public function delete($cin){
    include "../config/config.php";
    $con=new connexion();
    $pdo=$con->CNXbase();
    $req="delete from employer where cin='$cin'";
    $res=$pdo->exec($req)or print_r($pdo->errorInfo());
    }
	
	public function selection_id($cin)
	{
    include_once"../config/config.php";
    $con=new connexion();
    $pdo=$con->CNXbase();
	$req="select * from employer where cin='$cin'";
	$res=$pdo->query($req)or print_r($pdo->errorInfo());
	$row=$res->fetch();
	return $row;
		}
		

	
}
?>