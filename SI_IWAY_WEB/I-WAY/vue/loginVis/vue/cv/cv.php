<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>C.V.</title>
<link type="text/css" rel="stylesheet" href="css/brown.css" />
<link type="text/css" rel="stylesheet" href="css/print.css" media="print"/>
<!--[if IE 7]>
<link href="css/ie7.css" rel="stylesheet" type="text/css" />
<![endif]-->
<!--[if IE 6]>
<link href="css/ie6.css" rel="stylesheet" type="text/css" />
<![endif]-->
<script type="text/javascript" src="js/jquery-1.4.2.min.js"></script>
<script type="text/javascript" src="js/jquery.tipsy.js"></script>
<script type="text/javascript" src="js/cufon.yui.js"></script>
<script type="text/javascript" src="js/scrollTo.js"></script>
<script type="text/javascript" src="js/myriad.js"></script>
<script type="text/javascript" src="js/jquery.colorbox.js"></script>
<script type="text/javascript" src="js/custom.js"></script>
<script type="text/javascript">
		Cufon.replace('h1,h2');
</script>
</head>
<body>
<!-- Begin Wrapper --><br/><br />
 <center><div style="font-size:24px">Nous avons bien reçu votre candidature et nous vous remercions de l’intérêt que vous portez à notre entreprise.<br /><br />Nous examinons votre candidature avec intérêt et nous vous donnerons une réponse</div></center>
<div id="wrapper">
  <div class="wrapper-top"></div>
  <div class="wrapper-mid">
    <!-- Begin Paper -->
      <?php
include"../../Classes/cv.class.php";
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
	$j=0;
	$k=0;
	$d="";
	$s="";
	$l="";
	
while ($i<count($_POST['dev'])){
$d .="<br/>".$_POST['dev'][$i];	
$i++;}
while ($j<count($_POST['sys'])){
$s .="<br/>".$_POST['sys'][$j];	
$j++;}
while ($k<count($_POST['lang'])){
$l .="<br/>".$_POST['lang'][$k];	
$k++;}
	
	$c->devprog=$d;
	$c->sysexp=$s;
	$c->langage=$l;
	
	$a=0;
	$pex="";
	
while ($a<count($_POST['proj'])){
$pex .="<br/>".$_POST['proj'][$a];	
$a++;}	

	$c->nomsocex=$_POST['nomsoc'];
	$c->postex=$_POST['poste'];
	$c->projex=$pex;
	$c->debex=$_POST['debut'];
	$c->finex=$_POST['fin'];


	$b=0;
	$ps="";
	
while ($b<count($_POST['projs'])){
$ps .="<br/>".$_POST['projs'][$b];	
$b++;}	
	
	$c->nomsocs=$_POST['nomsocs'];
	$c->posts=$_POST['postes'];
	$c->projs=$ps;
	$c->debs=$_POST['debuts'];
	$c->fins=$_POST['fins'];

	$xx=0;
	$la="";
while ($xx<count($_POST['langue'])){
$la .="<br/>".$_POST['langue'][$xx];	
$xx++;}	
	$c->langue=$la;
	
	$x=0;
	$cer="";
while ($x<count($_POST['cert'])){
$cer .="<br/>".$_POST['cert'][$x];	
$x++;}	
	$c->certif=$cer;

	$xxx=0;
	$int="";
while ($xxx<count($_POST['int'])){
$int .="<br/>".$_POST['int'][$xxx];	
$xxx++;}
	$c->interet=$int;
	$c->numAnnonce=$_POST['numAnnonce'];
	
	$c->insertion();
?>
    <div id="paper">
      <div class="paper-top"></div>
      <div id="paper-mid">
        <div class="entry">
          <!-- Begin Image -->
         <?php echo' <img class="portrait" src="../../Images/'.$_POST['photo'].'" alt="John Smith" />';?>
          <!-- End Image -->
          <!-- Begin Personal Information -->
          
          <div class="self">
            <h1 class="name"><?php echo $_POST['nom']?> <?php echo $_POST['pre']?> <br />
              <span></span></h1>
            <ul>
              <li class="ad"><?php echo $_POST['adr']?>, <?php echo $_POST['reg']?></li>
              <li class="mail"><?php echo $_POST['email']?></li>
              <li class="tel"><?php echo $_POST['tel']?></li>
              <li >Date Naissance: <?php echo $_POST['dat']?></li>
              
            </ul>
          </div>
          <!-- End Personal Information -->
          <!-- Begin Social -->
          <div class="social">
            <ul>
            
              <li><a class='north' href="javascript:window.print()" title="Imprimer/Enregistrer"><img src="images/icn-print.jpg" alt="" /></a></li>
            </ul>
          </div>
          <!-- End Social -->
        </div>
        <!-- Begin 1st Row -->
        <!-- End 1st Row -->
        <!-- Begin 2nd Row -->
        <div class="entry">
          <h2>EDUCATION</h2>
          <div class="content">
            <h3><?php echo $_POST['anbac']?></h3>
            <p><?php echo $_POST['bac']?><br />
              <em><?php echo $_POST['lieubac']?></em></p>
          </div>
          <div class="content">
            <h3><?php echo $_POST['andip']?></h3>
            <p><?php echo $_POST['dip']?><br />
              <em><?php echo $_POST['lieudip']?></em></p>
          </div>
        </div>
        <!-- End 2nd Row -->
        <!-- Begin 3rd Row -->
                <div class="entry">
          <h2>EXPERIENCE</h2>
          <div class="content">
            <h3><?php echo $_POST['debut']?> / <?php echo $_POST['fin']?></h3>
            <p><?php echo $_POST['nomsoc']?><br /><?php echo $_POST['poste']?>
              <em><?php echo $pex?></em></p>
          </div></div>
                <div class="entry">
          <h2>Stage</h2>
          <div class="content">
            <h3><?php echo $_POST['debuts']?> / <?php echo $_POST['fins']?></h3>
            <p><?php echo $_POST['nomsocs']?><br /><?php echo $_POST['postes']?>
              <em><?php echo $ps?></em></p>
          </div></div>

        <!-- End 3rd Row -->
        <!-- Begin 4th Row -->
        <div class="entry">
          <h2>COMPETENCE</h2>
          <div class="content">
            <h3>Programmation</h3>
            <ul class="skills">
              <?php echo $d?>
            </ul>
          </div>
          <div class="content">
            <h3>Systéme d'éxploitation</h3>
            <ul class="skills">
              <?php echo $s?>
            </ul>
          </div>
          <div class="content">
            <h3>Langage</h3>
            <ul class="skills">
              <?php echo $l?>
            </ul>
          </div></div>
          <div class="entry">
          <h2>AUTRE COMPETENCE</h2><br /><br />
          <div class="content">
            <h3>Langues</h3>
            <ul class="skills">
              <?php echo $la?>
            </ul>
          </div>
          <div class="content">
            <h3>Certificats</h3>
            <ul class="skills">
              <?php echo $cer?>
            </ul>
          </div>
                    <div class="content">
            <h3>Intérêt</h3>
            <ul class="skills">
              <?php echo $int?>
            </ul>
          </div>
        </div>
        <!-- End 4th Row -->
         <!-- Begin 5th Row -->

        <!-- Begin 5th Row -->
      </div>
      <div class="clear"></div>
      <div class="paper-bottom"></div>
    </div>
    <!-- End Paper -->
  </div>
  <div class="wrapper-bottom"></div>
</div>
<div id="message"><a href="#top" id="top-link">Go to Top</a></div>
<!-- End Wrapper -->
</body>
</html>
