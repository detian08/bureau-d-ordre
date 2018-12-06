<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>I-Way</title>
<meta property="og:url" content="http://www.valeron.net/index.html" />
<meta property="og:type" content="website" />
<meta property="og:title" content="Free responsive web template Istria" />
<meta property="og:description" content="Free responsive web template Istria by Valeron design studio" />
<meta property="og:image" content="http://www.valeron.net/img/valeron-artist.jpg" />
<meta name="description" content="Free responsive web template Istria by Valeron design studio" />
<meta name="msapplication-tap-highlight" content="no" />
<meta name="robots" content="index,follow,all" />
<meta name="keywords" content="Izrada web stranica, web studio Istra, blog" />
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
<link href="css/lightgallery.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/3.5.1/animate.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.5.0/css/font-awesome.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome-animation/0.0.8/font-awesome-animation.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/modernizr/2.8.3/modernizr.min.js"></script>
</head>
<body>
<div class="animsition-overlay">
  <section id="section-1">
    <div class="horBar2Bxx wow fadeInLeftBig" data-wow-duration="3s"></div>
    <header class="main_h">
      <div class="menufix"> <a class="logo" href="index.html"><img src="images/iway.png" alt="Hello"></a>
        <div class="mobile-toggle"> <span></span> <span></span> <span></span> </div>
        <nav>
          <ul>
             <li class="line"><a class="out animsition-link" href="index.html">ACCUEIL</a></li>
             <li ><a class="out active animsition-link" href="blog.php">EQUIPE</a></li>
            <li class="line"><a class="out animsition-link" href="company.php">ANNONCES</a></li>
          <li class="line"><a class="out animsition-link" href="contact.html">CONTACT</a></li> 
          <li class="line"><a class="out animsition-link" href="../../inscription.html">DECONNEXION</a></li>
          </ul>
        </nav>
      </div>
      <!-- / row --> 
      
    </header>
    <div class="grid flex">
      <div class="row">
        <div class="colw_6">
          <h1 id="title-sub1">Notre Equipe</h1>
          <h2 id="title-sub2">I-Way</h2>
        </div>
        <!-- END colw_6 -->
        
        <div class="colw_6 wow zoomIn">
          <div class="box-fix">
            <h3 class="centered">Find us on social media</h3>
            <div class="social"> <a href="https://www.facebook.com/Valeron-design-studio-245216518822368/" class="soc-btn facebook"> <i class="fa fa-facebook"></i> Facebook </a> </div>
          </div>
        </div>
        <!-- END col_6 --> 
        
      </div>
      <!-- END row --> 
    </div>
    <!-- End GRID FLEX --> 
    
  </section>
  <!-- END #section-1 -->
  
  <section id="blog">
    <div class="grid flex16">
      <div class="row">
        <h2 class="title-blog wow fadeInUp" data-wow-duration="2s" style="visibility: visible; animation-duration: 2s; animation-name: fadeInUp;">La réussite appartient à tout le monde. C’est au travail d’équipe qu’en revient le mérite.</span></h2>
                    <?php
include "../Classes/employe.class.php";
$c=new employer();
$res=$c->selection();
foreach($res as $l)
	{
?>
        <div class="col_4 beta">
          <div class="horBar2Bxx wow fadeInLeftBig" data-wow-duration="3s"></div>
          <div class="boxwsha column3">
            <div class="zoomimg" id="gallery-1">
              <div class="zoom-wrap" data-responsive="images/blog-1-375.jpg 375, images/blog-1-480.jpg 480, images/blog-1-800.jpg 800" data-src="images/blog-1-1600.jpg" data-sub-html="<h4>Hello Istria</h4>"> <a href="" class="fixico"><i class="fa fa-search fa-2x"></i></a><?php echo'<img src="'.$l[8].'"style="width:350px; height:200px;"/>';?> <span class="fadef"></span> </div>
              <!-- END data-responsive --> 	
              
            </div>

            <!-- END .zoomimg #lightgallery  -->
            <div class="clear"></div>
            <div class="col_6">
              <div class="date"> <i class="fa fa-calendar"></i> <span class="italic"><?php echo "$l[5]" ; ?> ans</span><br/> <?php echo "$l[1]" ; ?> <?php echo "$l[2]" ; ?> </div>
              <!-- END date --> 
            </div>
            <!-- END col_6 -->
            
            <div class="col_6">
              <div class="soc-wrap">

              </div>
              <!-- soc Wrap --> 
            </div>
            <!-- END col_6 -->
            <div class="clear"></div>
            <h3 class="title-post"><?php echo "$l[4]" ; ?></h3>
            <p class="textlimit"><?php echo "$l[3]" ; ?><br/><?php echo "$l[6]" ; ?><br/><?php echo "$l[7]" ; ?><br/></p>
            <div class="clear"></div>
            <div class="fix-btn-blog"> <a href="#" class="istria-btn trigger">Continue Reading</a>
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
            <!-- END fix-btn --> 
            
          </div>
          <!-- END boxwsha --> 
        </div><?php } ?>
        <!-- END col_4 -->
        
       
          <!-- END boxwsha --> 
        </div>
        <!-- END col_4 --> 
        
      </div>
      <!-- END row --> 
    </div>
    <!-- End GRID FLEX --> 
    
  </section>
  <!-- END #section-1 -->
  
  
</div>
<!-- END .animsition-overlaj -->

<div class="modal" id="test-modal" style="display: none"> <a href="#" class="close">&times;</a>
  <h5>Hi, I'm the modal demo</h5>
  <div class="more">
    <p>Integer eleifend eros nec nunc venenatis ultrices. Maecenas sollicitudin feugiat urna. Maecenas tellus. Vestibulum semper, lacus in blandit blandit, neque lectus ullamcorper nulla, at viverra elit justo ac lacus. Proin gravida enim non neque ultricies dictum. In vulputate mattis lacus. In mollis nibh a lacus. Aenean a ipsum. Vivamus egestas adipiscing eros. Cras gravida suscipit risus. Maecenas varius sagittis velit. Phasellus rhoncus risus. Nunc quis urna at neque convallis hendrerit. Mauris metus. Integer eleifend eros nec nunc venenatis ultrices. Curabitur placerat. Nam eros dui, semper vitae, tincidunt quis, tincidunt eu, risus. Ut in pede a neque condimentum feugiat. Maecenas dictum tortor non neque.</p>
    <p><a href="#more" class="more-toggle">Add more content</a>.</p>
  </div>
  <div class="more" style="display: none">
    <p>Maecenas sollicitudin feugiat urna. Maecenas tellus. Vestibulum semper, lacus in blandit blandit, neque lectus ullamcorper nulla, at viverra elit justo ac lacus. Proin gravida enim non neque ultricies dictum. In vulputate mattis lacus. In mollis nibh a lacus. Aenean a ipsum. Vivamus egestas adipiscing eros. Cras gravida suscipit risus. Maecenas varius sagittis velit. Phasellus rhoncus risus. Nunc quis urna at neque convallis hendrerit. Mauris metus. Integer eleifend eros nec nunc venenatis ultrices. Curabitur placerat. Nam eros dui, semper vitae, tincidunt quis, tincidunt eu, risus. Ut in pede a neque condimentum feugiat. Maecenas dictum tortor non neque.</p>
    <p>Maecenas sollicitudin feugiat urna. Maecenas tellus. Vestibulum semper, lacus in blandit blandit, neque lectus ullamcorper nulla, at viverra elit justo ac lacus. Proin gravida enim non neque ultricies dictum. In vulputate mattis lacus. In mollis nibh a lacus. Aenean a ipsum. Vivamus egestas adipiscing eros. Cras gravida suscipit risus. Maecenas varius sagittis velit. Phasellus rhoncus risus. Nunc quis urna at neque convallis hendrerit. Mauris metus. Integer eleifend eros nec nunc venenatis ultrices. Curabitur placerat. Nam eros dui, semper vitae, tincidunt quis, tincidunt eu, risus. Ut in pede a neque condimentum feugiat. Maecenas dictum tortor non neque.</p>
    <p>Maecenas sollicitudin feugiat urna. Maecenas tellus. Vestibulum semper, lacus in blandit blandit, neque lectus ullamcorper nulla, at viverra elit justo ac lacus. Proin gravida enim non neque ultricies dictum. In vulputate mattis lacus. In mollis nibh a lacus. Aenean a ipsum. Vivamus egestas adipiscing eros. Cras gravida suscipit risus. Maecenas varius sagittis velit. Phasellus rhoncus risus. Nunc quis urna at neque convallis hendrerit. Mauris metus. Integer eleifend eros nec nunc venenatis ultrices. Curabitur placerat. Nam eros dui, semper vitae, tincidunt quis, tincidunt eu, risus. Ut in pede a neque condimentum feugiat. Maecenas dictum tortor non neque.</p>
    <p>Maecenas sollicitudin feugiat urna. Maecenas tellus. Vestibulum semper, lacus in blandit blandit, neque lectus ullamcorper nulla, at viverra elit justo ac lacus. Proin gravida enim non neque ultricies dictum. In vulputate mattis lacus. In mollis nibh a lacus. Aenean a ipsum. Vivamus egestas adipiscing eros. Cras gravida suscipit risus. Maecenas varius sagittis velit. Phasellus rhoncus risus. Nunc quis urna at neque convallis hendrerit. Mauris metus. Integer eleifend eros nec nunc venenatis ultrices. Curabitur placerat. Nam eros dui, semper vitae, tincidunt quis, tincidunt eu, risus. Ut in pede a neque condimentum feugiat. Maecenas dictum tortor non neque.</p>
  </div>
</div>
<div class="modal" id="test-modal2" style="display: none"> <a href="#" class="close">&times;</a>
  <h5>I'm the modal demo 2</h5>
  <div class="more">
    <p>Integer eleifend eros nec nunc venenatis ultrices. Maecenas sollicitudin feugiat urna. Maecenas tellus. Vestibulum semper, lacus in blandit blandit, neque lectus ullamcorper nulla, at viverra elit justo ac lacus. Proin gravida enim non neque ultricies dictum. In vulputate mattis lacus. In mollis nibh a lacus. Aenean a ipsum. Vivamus egestas adipiscing eros. Cras gravida suscipit risus. Maecenas varius sagittis velit. Phasellus rhoncus risus. Nunc quis urna at neque convallis hendrerit. Mauris metus. Integer eleifend eros nec nunc venenatis ultrices. Curabitur placerat. Nam eros dui, semper vitae, tincidunt quis, tincidunt eu, risus. Ut in pede a neque condimentum feugiat. Maecenas dictum tortor non neque.</p>
    <p><a href="#more" class="more-toggle">Add more content</a>.</p>
  </div>
  <div class="more" style="display: none">
    <p>Maecenas sollicitudin feugiat urna. Maecenas tellus. Vestibulum semper, lacus in blandit blandit, neque lectus ullamcorper nulla, at viverra elit justo ac lacus. Proin gravida enim non neque ultricies dictum. In vulputate mattis lacus. In mollis nibh a lacus. Aenean a ipsum. Vivamus egestas adipiscing eros. Cras gravida suscipit risus. Maecenas varius sagittis velit. Phasellus rhoncus risus. Nunc quis urna at neque convallis hendrerit. Mauris metus. Integer eleifend eros nec nunc venenatis ultrices. Curabitur placerat. Nam eros dui, semper vitae, tincidunt quis, tincidunt eu, risus. Ut in pede a neque condimentum feugiat. Maecenas dictum tortor non neque.</p>
    <p>Maecenas sollicitudin feugiat urna. Maecenas tellus. Vestibulum semper, lacus in blandit blandit, neque lectus ullamcorper nulla, at viverra elit justo ac lacus. Proin gravida enim non neque ultricies dictum. In vulputate mattis lacus. In mollis nibh a lacus. Aenean a ipsum. Vivamus egestas adipiscing eros. Cras gravida suscipit risus. Maecenas varius sagittis velit. Phasellus rhoncus risus. Nunc quis urna at neque convallis hendrerit. Mauris metus. Integer eleifend eros nec nunc venenatis ultrices. Curabitur placerat. Nam eros dui, semper vitae, tincidunt quis, tincidunt eu, risus. Ut in pede a neque condimentum feugiat. Maecenas dictum tortor non neque.</p>
    <p>Maecenas sollicitudin feugiat urna. Maecenas tellus. Vestibulum semper, lacus in blandit blandit, neque lectus ullamcorper nulla, at viverra elit justo ac lacus. Proin gravida enim non neque ultricies dictum. In vulputate mattis lacus. In mollis nibh a lacus. Aenean a ipsum. Vivamus egestas adipiscing eros. Cras gravida suscipit risus. Maecenas varius sagittis velit. Phasellus rhoncus risus. Nunc quis urna at neque convallis hendrerit. Mauris metus. Integer eleifend eros nec nunc venenatis ultrices. Curabitur placerat. Nam eros dui, semper vitae, tincidunt quis, tincidunt eu, risus. Ut in pede a neque condimentum feugiat. Maecenas dictum tortor non neque.</p>
    <p>Maecenas sollicitudin feugiat urna. Maecenas tellus. Vestibulum semper, lacus in blandit blandit, neque lectus ullamcorper nulla, at viverra elit justo ac lacus. Proin gravida enim non neque ultricies dictum. In vulputate mattis lacus. In mollis nibh a lacus. Aenean a ipsum. Vivamus egestas adipiscing eros. Cras gravida suscipit risus. Maecenas varius sagittis velit. Phasellus rhoncus risus. Nunc quis urna at neque convallis hendrerit. Mauris metus. Integer eleifend eros nec nunc venenatis ultrices. Curabitur placerat. Nam eros dui, semper vitae, tincidunt quis, tincidunt eu, risus. Ut in pede a neque condimentum feugiat. Maecenas dictum tortor non neque.</p>
  </div>
</div>
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script> 
<script type="text/javascript" src="js/jquery.matchHeight-min.js"></script> 
<script src="js/wow.min.js"></script> 
<script src="js/animsition.min.js"></script> 
<script src="js/lightgallery-all.min.js"></script> 
<script type="text/javascript">
        $(document).ready(function(){
            $('#gallery-1, #gallery-2, #gallery-3').lightGallery();
        });
    $('#gallery-99').lightGallery({
        thumbnail:true,
        animateThumb: false,
        showThumbByDefault: false,		
		speed: 1200
    });
 
</script> 
<script src="js/jquery.the-modal.js"></script> 
<script type="text/javascript">
		jQuery(function($){
			// bind event handlers to modal triggers
			$('body').on('click', '.trigger', function(e){
				e.preventDefault();
				$('#test-modal').modal().open();
			});
				$('body').on('click', '.trigger2', function(e){
				e.preventDefault();
				$('#test-modal2').modal().open();
			});

			// attach modal close handler
			$('.modal .close').on('click', function(e){
				e.preventDefault();
				$.modal().close();
			});

			// below isn't important (demo-specific things)
			$('.modal .more-toggle').on('click', function(e){
				e.stopPropagation();
				$('.modal .more').toggle();
			});
		});
	</script> 
<script src="js/functions.js"></script> 
<script type="text/javascript">
$( document ).ready(function() {
$('.menu-item').hover(function () {
    $('#active', this).toggleClass('active');
    $('#active', this).css({'display':'block'});
});
});
</script> 
<script type="text/javascript">
$(function(){
  $(".textlimit").each(function(i){
    len=$(this).text().length;
    if(len>100)
    {
      $(this).text($(this).text().substr(0,100)+'...');
    }
  });
});
</script> 
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