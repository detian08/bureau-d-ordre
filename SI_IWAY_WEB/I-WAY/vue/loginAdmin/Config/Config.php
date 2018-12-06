<?php
class connexion{
	public function CNXbase()
	{
		$dbc= new PDO('mysql:host=localhost;dbname=i-way','root','');
		return $dbc;
	}
}
?>