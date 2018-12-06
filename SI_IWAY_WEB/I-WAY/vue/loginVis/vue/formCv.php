<!DOCTYPE html>
<?php session_start();
 ?>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Formulaire CV </title>
<meta property="og:url" content="http://www.valeron.net/index.html" />
<meta property="og:type" content="website" />
<meta property="og:title" content="Free responsive web template Istria - Contact" />
<meta property="og:description" content="Free responsive web template Istria by Valeron design studio - Contact" />
<meta property="og:image" content="http://www.valeron.net/img/valeron-artist.jpg" />
<meta name="description" content="Free responsive web template Istria by Valeron design studio - Contact" />
<meta name="msapplication-tap-highlight" content="no" />
<meta name="robots" content="index,follow,all" />
<meta name="keywords" content="Izrada web stranica, web studio Istra" />
<meta name="author" content="Valeron design studio" />
<link rel="apple-touch-icon" sizes="57x57" href="img/apple-touch-icon-57x57.png">
<link rel="apple-touch-icon" sizes="60x60" href="img/apple-touch-icon-60x60.png">
<link rel="apple-touch-icon" sizes="72x72" href="img/apple-touch-icon-72x72.png">
<link rel="apple-touch-icon" sizes="76x76" href="img/apple-touch-icon-76x76.png">
<link rel="apple-touch-icon" sizes="114x114" href="img/apple-touch-icon-114x114.png">
<link rel="apple-touch-icon" sizes="120x120" href="img/apple-touch-icon-120x120.png">
<link rel="apple-touch-icon" sizes="144x144" href="img/apple-touch-icon-144x144.png">
<link rel="apple-touch-icon" sizes="152x152" href="img/apple-touch-icon-152x152.png">
<link rel="apple-touch-icon" sizes="180x180" href="img/apple-touch-icon-180x180.png">
<link rel="icon" type="image/png" href="img/favicon-32x32.png" sizes="32x32">
<link rel="icon" type="image/png" href="img/android-chrome-192x192.png" sizes="192x192">
<link rel="icon" type="image/png" href="img/favicon-96x96.png" sizes="96x96">
<link rel="icon" type="image/png" href="img/favicon-16x16.png" sizes="16x16">
<link rel="manifest" href="img/manifest.json">
<meta name="msapplication-TileColor" content="#da532c">
<meta name="msapplication-TileImage" content="img/mstile-144x144.png">
<meta name="theme-color" content="#ffffff">
<link rel="stylesheet" href="css/animsition.min.css">
<link rel="stylesheet" type="text/css" href="css/grid.min.css" />
<link rel="stylesheet" type="text/css" href="css/style.css" />
<link rel="stylesheet" type="text/css" href="css/menu.css" />
<link rel="stylesheet" type="text/css" href="css/social.css" />
<link rel="stylesheet" type="text/css" href="css/slickform.css" />
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/3.5.1/animate.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.5.0/css/font-awesome.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome-animation/0.0.8/font-awesome-animation.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/modernizr/2.8.3/modernizr.min.js"></script>
</head>
<body>
<div class="animsition-overlay">
  <div class="horBar2Bxx wow fadeInLeftBig" data-wow-duration="3s"></div>
  <header class="main_h">
    <div class="menufix"> <a class="logo" href="index.html"><img src="images/iway.png" alt="Hello"></a>
      <div class="mobile-toggle"> <span></span> <span></span> <span></span> </div>
      <nav>
        <ul>
           <li  class="line"><a class="out animsition-link" href="index.html">ACCUEIL</a></li>
             <li class="line"><a class="out animsition-link" href="blog.php">EQUIPE</a></li>
            <li class="line"><a class="out animsition-link" href="company.php">ANNONCES</a></li>
          <li class="line"><a class="out animsition-link" href="contact.html">CONTACT</a></li> 
          <li class="line"><a class="out animsition-link" href="../../inscription.html">DECONNEXION</a></li>
        </ul>
      </nav>
    </div>
    <!-- / row --> 
	<script type="text/javaScript"> 
    function fAddText() { 
        c=document.getElementById('Cible');
		c.innerHTML ='<label>Diplôme 2</label><input  name="dip2" type="text" value=""><br /><br /><label>Année Diplôme2</label><input  name="andip2" type="number" value=""><br /><br /><label>Université 2</label><input  name="lieudip2" type="text" value=""><br /><br />'; 
    } 
	    function fAddLangue() { 
	var c,c2, ch;
 

c=document.getElementById('langue');
c2=c.getElementsByTagName('input');
ch=document.createElement('input');
 
ch.setAttribute('type','text');
ch.setAttribute('name','langue[]');
c.appendChild(ch);
    } 
	
		    function fAddSys() { 
	var c,c2, ch;
 

c=document.getElementById('syst');
c2=c.getElementsByTagName('input');
ch=document.createElement('input');
 
ch.setAttribute('type','text');
ch.setAttribute('name','sys[]');
c.appendChild(ch);

    } 
function fAddDev() { 
	var c,c2, ch;
 

c=document.getElementById('devprog');
c2=c.getElementsByTagName('input');
ch=document.createElement('input');
 
ch.setAttribute('type','text');
ch.setAttribute('name','dev[]');
c.appendChild(ch);
    } 
	
	function fAddProj() { 
	var c,c2, ch;
 

c=document.getElementById('proj');
c2=c.getElementsByTagName('input');
ch=document.createElement('input');
 
ch.setAttribute('type','text');
ch.setAttribute('name','proj[]');
c.appendChild(ch);
    } 
		function fAddProjs() { 
	var c,c2, ch;
 

c=document.getElementById('projs');
c2=c.getElementsByTagName('input');
ch=document.createElement('input');
 
ch.setAttribute('type','text');
ch.setAttribute('name','projs[]');
c.appendChild(ch);
    } 
	
		function fAddLangage() { 
	var c,c2, ch;
 

c=document.getElementById('lang');
c2=c.getElementsByTagName('input');
ch=document.createElement('input');
 
ch.setAttribute('type','text');
ch.setAttribute('name','lang[]');
c.appendChild(ch);
    } 
	
		function fAddCert() { 
	var c,c2, ch;
 

c=document.getElementById('cert');
c2=c.getElementsByTagName('input');
ch=document.createElement('input');
 
ch.setAttribute('type','text');
ch.setAttribute('name','cert[]');
c.appendChild(ch);
    } 
	
		function fAddInt() { 
	var c,c2, ch;
 

c=document.getElementById('int');
c2=c.getElementsByTagName('input');
ch=document.createElement('input');
 
ch.setAttribute('type','text');
ch.setAttribute('name','int[]');
c.appendChild(ch);
    } 
	
	
	
</script>
    
  </header>
  <div class="grid flex16">
    <div class="row">
      <div class="colw_6">
        <h1 id="title-sub1">I - WAY</h1>
        <h2 id="title-sub2">CURRICULUM VITAE</h2>
      </div>
      <!-- END colw_6 -->
      
      <div class="col_6">
        <div class="box-fix">
          <h3 class="centered">Find us on social media</h3>
          <div class="social"> <a href="https://www.facebook.com/Valeron-design-studio-245216518822368/" class="soc-btn facebook"><i class="fa fa-facebook"></i>Facebook</a>
        </div>
      </div>
      <!-- END col_6 --> 
      
    </div>
    <!-- END row --> 
    
  </div>
  <!-- End GRID FLEX16 -->
</div>
      <!-- END col_12 -->
              
                <?php
include"../Classes/visiteur.class.php";
$p=new visiteur();
$row=$p->selection_id($_SESSION['login'],$_SESSION['pass']);
$num= $_GET['numAnnonce'];
?>
              
                <form method="post" action="cv/cv.php">
            <fieldset> 
      <div class="colw_6 spec-r-cont border-right ">
 <h3>Info Personnel</h3>
        <div class="slickwrap">
          <div class="slickreporting">
            <div class="successcontainer"></div>
            <div class="errorcontainer">
              <div class="errorshutter"></div>
              <div class="slickerror"></div>
            </div>
          </div>
          <label><span>*</span>Photo</label>
             <input  name="photo" type="file">
              <br />
            <label><span>*</span>Nom</label>
            <input id="numAnnonce" name="numAnnonce" type="hidden" value="<?php echo $num ?>">
         
              <input id="name" name="nom" type="text" value="<?php echo $row[0]?>">
              <br />
              <label><span>*</span>Prénom</label>
              <input  name="pre" type="text" value="<?php echo $row[1]?>">
              <br />
              <label><span>*</span>Date Naissance</label>
              <input  name="dat" type="date" value="<?php echo $row[5]?>">
              <br />
              <label><span>*</span>Téléphone</label>
              <input id="phone" name="tel" type="number" value="">
              <br />
              <label><span>*</span>Adresse</label>
              <input  name="adr" type="text" value="">
              <br />
              <label><span>*</span>Region</label>
              <input  name="reg" type="text" value="<?php echo $row[3]?>">
              <br />
              <label><span>*</span>Email</label>
              <input id="email" name="email" type="email" value="<?php echo $row[2]?>">
              <br />
              
        </div>
        </div>
      <!-- END col_6 -->
      
      <div class="colw_6 spec-r-cont">
        <h3>Formation</h3>
        <div class="slickwrap">
          <div class="slickreporting">
            <div class="successcontainer"></div>
            <div class="errorcontainer">
              <div class="errorshutter"></div>
              <div class="slickerror"></div>
            </div>
          </div>
              <label><span></span>Type Baccalauréat</label>
              <input  name="bac" type="text" value="">
              <br /><br />
              <label><span></span>Année Baccalauréat</label>
              <input  name="anbac" type="number" value="">
              <br /><br />
              <label><span></span>Lycée</label>
              <input  name="lieubac" type="text" value="">
              <br /><br />
              <label><span></span>Diplôme</label>
              <input  name="dip" type="text" value="">
              <br /><br />
              <label><span></span>Année Diplôme</label>
              <input  name="andip" type="number" value="">
              <br /><br />
              <label><span></span>Université</label>
              <input  name="lieudip" type="text" value="">
              <br /><br />
			  <div id="Cible"></div> 
			      <input type="button" value="Ajouter d'autre diplôme" onclick="fAddText()" /> 
    <br>
            
        </div>
      </div>
      <div class="colw_6 spec-r-cont border-right ">
 <h3>Compétences</h3>
        <div class="slickwrap">
          <div class="slickreporting">
            <div class="successcontainer"></div>
            <div class="errorcontainer">
              <div class="errorshutter"></div>
              <div class="slickerror"></div>
            </div>
          </div>
             
              <label>Développement / Programmation<br/><br/>			  
			  <input type="button" value="+" onclick="fAddDev()" />  </label>
			  <input  name="dev[]" type="text" value=""><br><br><br><br/><br/>
              			  <div id="devprog"></div> <br>
              <br />  <br />
              <label>Systèmes d’exploitation   <br/><br/>
			  <input type="button" value="+" onclick="fAddSys()" />  </label>
			  <input  name="sys[]" type="text" value=""><br><br><br/><br/>
              			  <div id="syst"></div> <br/>
			      
              <br />  <br />
              <label>Langage  <br/><br/>  			 
			  <input type="button" value="+" onclick="fAddLangage()" />  </label>
			  <input  name="lang[]" type="text" value=""><br><br/> <br/>
              			  <div id="lang"></div> <br>
              <hr />
        </div>
        </div>
        
        <div class="colw_6 spec-r-cont">
        <h3>Experiences</h3>
        <div class="slickwrap">
          <div class="slickreporting">
            <div class="successcontainer"></div>
            <div class="errorcontainer">
              <div class="errorshutter"></div>
              <div class="slickerror"></div>
            </div>
          </div>
		   <label><span></span>Nom de la société </label>
              <input  name="nomsoc" type="text" value="">
              <br /><br />
		<label><span></span>Poste</label>
              <input  name="poste" type="text" value="">
              <br /><br />
			  <label><span></span>Projet<br /><br />
			  <input type="button" value="+" onclick="fAddProj()" /> </label>
              <input  name="proj[]" type="text" value=""><br /><br /><br />
			  <div id="proj"></div> <br>
              
			  <label><span></span>Période:</label><br /><br />
			  <label><span></span>Du</label>
              <input  name="debut" type="date" value="">
              <br /><br />
			  <label><span></span>Au</label>
              <input  name="fin" type="date" value="">
              <hr />
        </div>
      </div>
      <div class="row">
            <div class="colw_6 spec-r-cont border-right ">
<h3>Stages</h3>
        <div class="slickwrap">
          <div class="slickreporting">
            <div class="successcontainer"></div>
            <div class="errorcontainer">
              <div class="errorshutter"></div>
              <div class="slickerror"></div>
            </div>
          </div>
		   <label><span></span>Nom de la société </label>
              <input  name="nomsocs" type="text" value="">
              <br /><br />
		<label><span></span>Poste</label>
              <input  name="postes" type="text" value="">
              <br /><br />
			  <label><span></span>Projet<br /><br />
			  <input type="button" value="+" onclick="fAddProjs()" /> </label>
              <input  name="projs[]" type="text" value=""><br /><br /><br />
			  <div id="projs"></div> <br>
              
			  <label><span></span>Période:</label><br /><br />
			  <label><span></span>Du</label>
              <input  name="debuts" type="date" value="">
              <br /><br />
			  <label><span></span>Au</label>
              <input  name="fins" type="date" value="">
              <hr />
        </div>
        </div>
        
        <div class="colw_6 spec-r-cont">
         <h3>Autre Compétences</h3>
        <div class="slickwrap">
          <div class="slickreporting">
            <div class="successcontainer"></div>
            <div class="errorcontainer">
              <div class="errorshutter"></div>
              <div class="slickerror"></div>
            </div>
          </div>
             
              <label>Langues <br/><br/>			  
			  <input type="button" value="+" onclick="fAddLangue()" />  </label>
			  <input  name="langue[]" type="text" value=""><br><br><br><br/><br/>
              			  <div id="langue"></div> <br>
              <br />  <br />
              <label>Certificats<br/><br/>
			  <input type="button" value="+" onclick="fAddCert()" />  </label>
			  <input  name="cert[]" type="text" value=""><br><br><br/><br/>
              			  <div id="cert"></div> <br/>
			      
              <br />  <br />
              <label>Intérêt<br/><br/>  			 
			  <input type="button" value="+" onclick="fAddInt()" />  </label>
			  <input  name="int[]" type="text" value=""><br><br/> <br/>
              			  <div id="int"></div> <br>
              <br />  <br />

              
              <hr />
<input name="submit" type="submit" value="Valider" class="slickbutton">
        </div>
      </div>
      </div>
      
              
                </fieldset>
          </form>
      <!-- END col_6 -->
      
      

      <!-- END col_6 --> 
      
    </div>
    <!-- END row --> 

  <!-- End GRID FLEX16 -->

<!-- END .animsition-overlaj --> 

<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script> 
<script type="text/javascript" src="js/jquery.matchHeight-min.js"></script> 
<script src="js/wow.min.js"></script> 
<script src="js/animsition.min.js"></script> 
<script src="js/Slickform.js"></script> 
<script src="js/functions.js"></script> 
<script type="text/javascript">
  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-15815880-3']);
  _gaq.push(['_trackPageview']);
  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();
</script>
</body>
</html>