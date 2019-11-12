<?php

class Views
{
    public static function Manut($f3)
    {
        $view = new View();
        echo $view->render("/pages/manut/index.html");
    }
}
