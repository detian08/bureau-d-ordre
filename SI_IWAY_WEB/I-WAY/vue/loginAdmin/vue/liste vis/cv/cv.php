<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>Resume</title>
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
<!-- Begin Wrapper -->
<div id="wrapper">
  <div class="wrapper-top"></div>
  <div class="wrapper-mid">
    <!-- Begin Paper -->
      <?php
include"../../Classes/cv.class.php";
$p=new cv();
$l=$p->selection_cv($_GET['numCv']);
?>
    <div id="paper">
      <div class="paper-top"></div>
      <div id="paper-mid">
        <div class="entry">
          <!-- Begin Image -->
         <?php echo' <img class="portrait" src="../'.$l[1].'" alt="John Smith" />';?>
          <!-- End Image -->
          <!-- Begin Personal Information -->
          <div class="self">
            <h1 class="name"><?php echo $l[2]?> <?php echo $l[3]?> <br />
              <span></span></h1>
            <ul>
              <li class="ad"><?php echo $l[6]?>, <?php echo $l[7]?></li>
              <li class="mail"><?php echo $l[8]?></li>
              <li class="tel"><?php echo $l[5]?></li>
              <li >Date Naissance: <?php echo $l[4]?></li>
              
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
            <h3><?php echo $l[10]?></h3>
            <p><?php echo $l[11]?><br />
              <em><?php echo $l[9]?></em></p>
          </div>
          <div class="content">
            <h3><?php echo $l[13]?></h3>
            <p><?php echo $l[14]?><br />
              <em><?php echo $l[12]?></em></p>
          </div>
        </div>
        <!-- End 2nd Row -->
        <!-- Begin 3rd Row -->
        <div class="entry">
          <h2>STAGE</h2>
          <div class="content">
            
            <p><?php echo $l[18]?> <br />
              </p>
          </div>
        </div>
        
        <div class="entry">
          <h2>EXPERIENCE</h2>
          <div class="content">
            
            <p><?php echo $l[19]?> <br />
              </p>
          </div>
        </div>
        <!-- End 3rd Row -->
        <!-- Begin 4th Row -->
        <div class="entry">
          <h2>COMPETENCE</h2>
          <div class="content">
            <h3>Programmation</h3>
            <ul class="skills">
              <?php echo $l[15]?>
            </ul>
          </div>
          <div class="content">
            <h3>Systéme d'éxploitation</h3>
            <ul class="skills">
              <?php echo $l[16]?>
            </ul>
          </div>
          <div class="content">
            <h3>Langues</h3>
            <ul class="skills">
              <?php echo $l[17]?>
            </ul>
          </div>
          <div class="content">
            <h3>Certificats</h3>
            <ul class="skills">
              <?php echo $l[20]?>
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
