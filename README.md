This creates `/home/http` directory that will serve PHP-enabled sites via pre-configured `nginx` and `php-fpm` (currently for *Ubuntu* ONLY).

For example:

    /home/http/test.local/www/index.php

becomes

    http://test.local/

Path mangling pre-enabled for all hosts, so any non-file will be routed to index.php (URL rewriting).

To install run (from Terminal via `Ctrl+Alt+T`):

    sudo sh -c "wget --no-check-certificate \
    https://github.com/yappie/simple-php-fpm-nginx/raw/master/nginx.py \
    -O /bin/nginx.py; chmod a+x /bin/nginx.py "; nginx.py

Then create directories in `/home/http/` as `domain/subdomain` and run `nginx.py` (it will request sudo password to install nginx/php-fpm/mysql).

