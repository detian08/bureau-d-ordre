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
		 
	public function update($numAnnonce){
    include_once "../config/config.php";
    $con=new connexion();
    $pdo=$con->CNXbase();
    $req="update annonce SET poste='$this->poste', competence='$this->competence', experience='$this->experience', salaire='$this->salaire', dateAnnonce='$this->dateAnnonce' where numAnnonce='$numAnnonce'";
    $res=$pdo->exec($req)or print_r($pdo->errorInfo());
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
		public function delete($numAnnonce){
    include "../config/config.php";
    $con=new connexion();
    $pdo=$con->CNXbase();
    $req="delete from annonce where numAnnonce='$numAnnonce'";
    $res=$pdo->exec($req)or print_r($pdo->errorInfo());
    }
	
	public function selection_id($numAnnonce)
	{
    include_once"../config/config.php";
    $con=new connexion();
    $pdo=$con->CNXbase();
	$req="select * from annonce where numAnnonce='$numAnnonce'";
	$res=$pdo->query($req)or print_r($pdo->errorInfo());
	$row=$res->fetch();
	return $row;
		}
	}
?>