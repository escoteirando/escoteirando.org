<?php

class Setup
{
    public static function Get()
    {

        return [
            "DB" => [
                "devel" => ["type" => "sqlite", "connectionstring" => "sqlite:database.db"],
                "production" => ["type" => "mysql", "connectionstring" => "localhost"],
            ],
        ];
    }
}
