<?php
class cv {
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
	public $langue; 
	public $stage ;
	public $experience;
	public $certif;
	public $langage;
	public $numAnnonce; 
	
	public function __construct(){
		session_start(); 
		}
	
	public function insertion()
	{
    include "../config/config.php";
    $con=new connexion();
    $pdo=$con->CNXbase();
    $req="insert into visiteur values ('$this->numCv','$this->nom','$this->prenom','$this->datNaiss',$this->tel','$this->adresse','$this->region','$this->email','$this->experience','$this->formation', '$this->competence' ,'$this->stage','$this->poste')";
    $res=$pdo->exec($req)or print_r($pdo->errorInfo());
    return $res;
    }
	
public function __destruct(){
		//session_unset();
		}
}

?>