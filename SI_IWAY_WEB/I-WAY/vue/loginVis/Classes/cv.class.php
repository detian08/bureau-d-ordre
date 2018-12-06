<?php
class cv {
	public $photo;
	public $nom;
	public $prenom;
	public $datNaiss;
	public $tel;
	public $adresse;
	public $region;
	public $email;
	public $typebac;
	public $annbac;
	public $lieubac;
	public $typedip;
	public $anndip;
	public $lieudip;
	public $devprog;
	public $sysexp;
	public $langage;
	public $nomsocex;
	public $postex;
	public $projex;
	public $debex;
	public $finex;
	public $nomsocs;
	public $posts;
	public $projs;
	public $debs;
	public $fins;
	public $langue; 
	public $certif;
	public $interet;
	public $numAnnonce; 
	
	public function __construct(){
		session_start(); 
		}
		
	public function insertion()
	{
    include "Config.php";
    $con=new connexion();
    $pdo=$con->CNXbase();
    $req="insert into cv values ('','$this->photo','$this->nom','$this->prenom','$this->datNaiss','$this->tel','$this->adresse','$this->region','$this->email','$this->typebac','$this->annbac','$this->lieubac','$this->typedip','$this->anndip','$this->lieudip','$this->devprog','$this->sysexp','$this->langage','$this->nomsocex','$this->postex','$this->projex','$this->debex','$this->finex','$this->nomsocs','$this->posts','$this->projs','$this->debs','$this->fins','$this->langue','$this->certif','$this->interet','$this->numAnnonce')";
    $res=$pdo->exec($req)or print_r($pdo->errorInfo());
    return $res;
    }
	
			public function selection_id($numAnnonce)
	{
    include_once "Config.php";
    $con=new connexion();
    $pdo=$con->CNXbase();
	$req="select * from cv where numAnnonce='$numAnnonce'";
	$res=$pdo->query($req);
	//$row=$res->fetch();
	return $res;
		}
		
	public function selection_cv($numCv)
	{
    include_once "Config.php";
    $con=new connexion();
    $pdo=$con->CNXbase();
	$req="select * from cv where numCv='$numCv'";
	$res=$pdo->query($req);
	$row=$res->fetch();
	return $row;
		}
		
		public function selection()
	{
    include"Config.php";
    $con=new connexion();
    $pdo=$con->CNXbase();
    $req="select * from cv ";
    $res=$pdo->query($req)or print_r($pdo->errorInfo());
    return $res;
    }
	

	
		
	
public function __destruct(){
		//session_unset();
		}



	}

?>