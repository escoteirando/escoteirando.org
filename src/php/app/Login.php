<?php

define("CookieLogin", "LoginStatus");
/**
 * Classe de gerenciamento de login/logout
 */
class Login
{
    /**
     * Verifica a situação do login atual a partir do cookie
     * @return O nome do usuário logado ou false
     */
    public static function LoginStatus($f3)
    {
        if (!$f3->get("COOKIE." . CookieLogin)) {
            return false;
        }
        $loginStatus = self::Decrypt($f3->get('COOKIE.' . CookieLogin));

        $userLogin = new LoginStatus($loginStatus);

        if (!$f3->get("SESSION." . CookieLogin)) {
            return $userLogin->userName;
        }

    }

    /**
     * Define a situação de login a partir do cookie
     */
    public static function SetLogin($f3, $userName)
    {
        if ($userName) {
            $u = new LoginStatus();
            $u->userName = $userName;
            $f3->set('COOKIE.' . CookieLogin, $u->ToString());

        } else {
            $f3->set('COOKIE.' . CookieLogin, false);
        }
    }

    private static function Encrypt($text)
    {
        return $text;
    }

    private static function Decrypt($text)
    {
        return $text;
    }

    //! Display login form
    public function login($f3)
    {
        $f3->clear('SESSION');
        if ($f3->get('eurocookie')) {
            $loc = Web\Geo::instance()->location();
            if (isset($loc['continent_code']) && $loc['continent_code'] == 'EU') {
                $f3->set('message',
                    'The administrator pages of this Web site uses cookies ' .
                    'for identification and security. Without these ' .
                    'cookies, these pages would simply be inaccessible. By ' .
                    'using these pages you agree to this safety measure.');
            }

        }
        $f3->set('COOKIE.sent', true);
        if ($f3->get('message')) {
            $img = new Image;
            $f3->set('captcha', $f3->base64(
                $img->captcha('fonts/thunder.ttf', 18, 5, 'SESSION.captcha')->
                    dump(), 'image/png'));
        }
        $f3->set('inc', 'login.htm');
    }

    //! Process login form
    public function auth($f3)
    {
        if (!$f3->get('COOKIE.sent')) {
            $f3->set('message', 'Cookies must be enabled to enter this area');
        } else {
            $crypt = $f3->get('password');
            $captcha = $f3->get('SESSION.captcha');
            if ($captcha && strtoupper($f3->get('POST.captcha')) != $captcha) {
                $f3->set('message', 'Invalid CAPTCHA code');
            } elseif ($f3->get('POST.user_id') != $f3->get('user_id') ||
                crypt($f3->get('POST.password'), $crypt) != $crypt) {
                $f3->set('message', 'Invalid user ID or password');
            } else {
                $f3->clear('COOKIE.sent');
                $f3->clear('SESSION.captcha');
                $f3->set('SESSION.user_id', $f3->get('POST.user_id'));
                $f3->set('SESSION.crypt', $crypt);
                $f3->set('SESSION.lastseen', time());
                $f3->reroute('/admin/pages');
            }
        }
        $this->login($f3);
    }

    //! Terminate session
    public function logout($f3)
    {
        $f3->clear('SESSION');
        $f3->reroute('/login');
    }
}

class LoginStatus
{
    public $userName = false;

    public function __construct($text = false)
    {
        $this->Parse($text);
    }

    public function Parse($text)
    {
        try {
            $s = json_decode(base64_decode($text), true);
            if (isset($s['un'])) {
                $this->userName = $s['un'];
                return true;
            }
        } catch (Exception $e) {

        }
        return false;
    }

    public function ToString()
    {
        $s = ["un" => $this->userName];
        return base64_encode(json_encode($s));
    }
}
