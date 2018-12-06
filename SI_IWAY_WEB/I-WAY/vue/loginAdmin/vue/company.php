<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Annonces</title>
<meta property="og:url" content="http://www.valeron.net/index.html" />
<meta property="og:type" content="website" />
<meta property="og:title" content="Free responsive web template Istria" />
<meta property="og:description" content="Free responsive web template Istria by Valeron design studio" />
<meta property="og:image" content="http://www.valeron.net/img/valeron-artist.jpg" />
<meta name="description" content="Free responsive web template Istria by Valeron design studio" />
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
<link rel="stylesheet" type="text/css" href="css/overlay.css" />
<link rel="stylesheet" href="css/social.css">
<link rel="stylesheet" href="css/imgover.css">
<link rel="stylesheet" href="css/triangle.css">
<link rel="stylesheet" href="css/banner.css">
<link href="css/lightgallery.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/3.5.1/animate.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.5.0/css/font-awesome.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome-animation/0.0.8/font-awesome-animation.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/modernizr/2.8.3/modernizr.min.js"></script>
</head>
<body>
<div class="animsition-overlay">
  <section id="section-6">
    <div class="horBar2Bxx wow fadeInLeftBig" data-wow-duration="3s"></div>
    <header class="main_h">
      <div class="menufix"> <a class="logo" href="index.html"><img src="images/iway.png" alt="Hello"></a>
        <div class="mobile-toggle"> <span></span> <span></span> <span></span> </div>
        <nav>
          <ul>
            <li class="line"><a class="out animsition-link" href="indexAdmin.html">ACCUEIL</a></li>
             <li class="line"><a class="out animsition-link" href="blogAdmin.php">EQUIPE</a></li>
            <li><a class="out active animsition-link" href="company.php">ANNONCES</a></li>
          <li class="line"><a class="out animsition-link" href="../../inscription.html">DECONNEXION</a></li>
          </ul>
        </nav>
      </div>
      <!-- / row --> 
      
    </header>
    <div class="grid flex">
      <div class="row">
        <div class="colw_6">
          <h1 id="title-sub1">I - WAY</h1>
          <h2 id="title-sub2">ANNONCES</h2>
        </div>
        <!-- END colw_6 -->
                      <div class="col_6">
        <div class="bannerbox">
          <div class="banner">
            <div class="phrase-1">Ajouter des Annonces</div>
            <div class="phrase-2" ><a href="formannonce.html"  > Ajouter </a></div>
            <div class="blob-1"></div>
            <div class="blob-2"></div>
            <div class="blob-3"></div>
          </div>
        </div>
      </div>
        <!-- END col_6 --> 
        
      </div>
      <!-- END row -->
      

      <!-- END row --> 
      
    </div>
    <!-- End GRID FLEX --> 
    
  </section>
  <!-- END #section-2 -->
  
  <div class="backimg" id="section-7">
    <div class="bghover7 wow fadeInUp" data-wow-duration="1.5s" data-wow-delay=".1s">
      <div class="grid flex">
        <div class="row paddtop5">
          <div class="colw_8 column wow fadeInUpBig" data-wow-duration="1s" data-wow-delay=".2s">
<?php
include "../Classes/annonce.class.php";
$c=new annonce();
$res=$c->selection();
foreach($res as $l)
	{
?>  
            <div class="col_6 beta">
              <div class="box90 boxwsha reladiv column2">
                <h4 class="color wow fadeInDown" data-wow-duration="0.5s" data-wow-delay="0.5s">Profil: <?php echo "$l[1]" ; ?></h4>
                <p><h5>Compétence</h5><?php echo "$l[2]" ; ?></p>
                <p><h5>Experience</h5><?php echo "$l[3]" ; ?></p>
                <p><h5>Salaire</h5><?php echo "$l[4]" ; ?></p>
                <p><h5>Date Annonce</h5><?php echo "$l[5]" ; ?></p><br/><br/><br/>
            <div class="clear"></div>
            <div class="fix-btn-blog"> <a href="modifAnn.php?numAnnonce=<?php echo"$l[0]";?>" class="istria-btn">Modifier</a>
              <div class="istria-over"></div>
              <div class="istria-line left">
                <div class="inner"></div>
              </div>
              
              <!-- END istria-line left -->
              <div class="istria-line right">
                <div class="inner"></div>
              </div>
              <!-- END istria-line right --> 
            </div>
            <div class="clear"></div>
            <div class="fix-btn-blog"> <a href="../Controlleurs/supAnn.php?numAnnonce=<?php echo"$l[0]";?>" class="istria-btn">Supprimer</a>
              <div class="istria-over"></div>
              <div class="istria-line left">
                <div class="inner"></div>
              </div>
              
              <!-- END istria-line left -->
              <div class="istria-line right">
                <div class="inner"></div>
              </div>
              <!-- END istria-line right --> 
            </div>
            
            <div class="clear"></div>
            <div class="fix-btn-blog"> <a href="liste cv/listecv.php?numAnnonce=<?php echo"$l[0]";?>" class="istria-btn">Consulter Les  CV</a>
              <div class="istria-over"></div>
              <div class="istria-line left">
                <div class="inner"></div>
              </div>
              
              <!-- END istria-line left -->
              <div class="istria-line right">
                <div class="inner"></div>
              </div>
              <!-- END istria-line right --> 
            </div>
                <div class="istria-line left">
                  <div class="inner"></div>
                </div>
                <div class="istria-line right">
                  <div class="inner"></div>
                </div>
              </div>
              <!-- END box80 --> 
            </div><?php } ?>
            <!-- END col_6 -->
            
            <!-- END col_6 --> 
            
          </div>
          <!-- END col_6 -->
          
          <!-- END col_4 --> 
          
        </div>
        <!-- END row --> 
      </div>
      <!-- END .GRID FLEX --> 
    </div>
    <!-- END bghover --> 
  </div>
  <!-- END #section-3 -->
  

  <!-- END #section-door --> 
</div>
<!-- END .animsition-overla --> 

<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script> 
<script type="text/javascript" src="js/jquery.matchHeight-min.js"></script> 
<script src="js/wow.min.js"></script> 
<script src="js/animsition.min.js"></script> 
<script src="js/lightgallery-all.min.js"></script> 
<script type="text/javascript">
        $(document).ready(function(){
            $('#lightgallery').lightGallery();
        });
    $('#lightgallery2').lightGallery({
        thumbnail:true,
        animateThumb: false,
        showThumbByDefault: false,		
		speed: 1200
    });
	    $('#gallery-99').lightGallery({
        thumbnail:true,
        animateThumb: false,
        showThumbByDefault: false,		
		speed: 1200
    });
        </script> 
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