<?php
require 'vendor/autoload.php';
/// Identificar o usuário logado
$f3 = \Base::instance();
Login::SetLogin($f3,"Guionardo");

// Initialize CMS
$f3->config('/app/config.ini');

// Define routes
$f3->config('/app/routes.ini');


$f3->route('GET /manut',function($f3){
    include("pages/manut/index.html");
});

$f3->run();