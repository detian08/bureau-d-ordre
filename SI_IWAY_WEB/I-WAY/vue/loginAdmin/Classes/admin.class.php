<?php
class admin{
	public $login;
	public $pass;
	
	public function __construct(){
		session_start(); }
	
	public function insertion(){
    include "../config/config.php";
    $con=new connexion();
    $pdo=$con->CNXbase();
    $req="insert into admin values ('$this->login','$this->pass')";
    $res=$pdo->exec($req)or print_r($pdo->errorInfo());
    return $res;
    }
	public function rechsession(){
    include_once"../config/config.php";
    $con=new connexion();
    $pdo=$con->CNXbase();
    $req="select count(*)from admin where login='$this->login' and pass='$this->pass'";
	$res=$pdo->query($req)or print_r($pdo->errorInfo());
	return $res;
	}
public function __destruct(){
		//session_unset();
		}
}

?>