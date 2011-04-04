#!/usr/bin/python

import re
import os
import sys
import glob

nginx_template = """
server {
    listen   80;
    charset utf-8;
    index  index.php index.html;
    server_name [DOMAIN-WITH-SUBDOMAIN];
    server_name [DOMAIN];
    if ($host ~* www\.(.*)) {
        set $host_without_www $1;
        rewrite ^(.*)$ http://$host_without_www$1 permanent;
    }
    location ~ \.php$ {
        root           [WWWDIR];
        fastcgi_index  index.php;
        fastcgi_param  SCRIPT_FILENAME [WWWDIR]$fastcgi_script_name;
        include        fastcgi_params;
        if (-e $request_filename) {
            fastcgi_pass   127.0.0.1:9000;
        }
    }
    location / {
        root  [WWWDIR];
        if (!-e $request_filename) {
            rewrite ^(.+)$ /index.php last;
        }
    }
}
"""

def add_to_etc_hosts(domain):
    with open('/etc/hosts', 'r') as f:
        hosts_txt = f.read()
    
    hosts_line = '127.0.0.1  %s  # local-http\n' % domain
    assert "'" not in hosts_line
    assert '"' not in hosts_line
    
    if hosts_line not in hosts_txt:
        os.system('echo \'%s\' >> /etc/hosts' % hosts_line)

def create_host(wwwdir):
    wwwdir = re.sub('/$', '', wwwdir)
    parts = wwwdir.split('/')
    subdomain = parts[-1]
    domain = parts[-2]
    domain_w_sub = '%s.%s' % (subdomain, domain)

    template = nginx_template
    template = template.replace('[WWWDIR]', wwwdir)
    template = template.replace('[DOMAIN-WITH-SUBDOMAIN]', domain_w_sub)
    if subdomain == 'www':
        template = template.replace('[DOMAIN]', domain)
    else:
        template = template.replace('server_name [DOMAIN];', '')

    with open('/tmp/1', 'w') as f:
        f.write(template)

    os.system('sudo cp /tmp/1 /etc/nginx/sites-enabled/' + domain_w_sub)
    
    os.unlink('/tmp/1')

    add_to_etc_hosts(domain)
    
def install_nginx():
    os.system('sudo apt-get -q -y install nginx php5-fpm mysql-server')
    os.system('sudo chkconfig nginx on')
    os.system('sudo chkconfig mysql on 2>/dev/null')
    os.system('sudo chkconfig php5-fpm on')

def restart_nginx():
    os.system('sudo /etc/init.d/nginx restart')

def create_http_dir(director):
    if not os.path.exists(directory):
        os.system('sudo mkdir ' + directory)
        os.system('sudo mkdir -p ' + os.path.join(directory, 'test.local/www'))
        os.system('sudo chown -R %s:%s %s' % (os.getlogin(), os.getgroups()[0], directory))
        os.system('chmod a+r ' + directory)
        os.system('chmod a+x ' + directory)
        with open(os.path.join(directory, 'test.local/www/index.php'), 'w') as f:
            f.write('<?php print "That\'s it!";')

def iter_hosts():
    all_dirs = glob.glob(os.path.join(directory, '*'))
    for host in filter(os.path.isdir, all_dirs):
        all_subdirs = glob.glob(os.path.join(host, '*'))
        for subhost in filter(os.path.isdir, all_subdirs):
            yield subhost

if os.getuid() == 0:
    print "No need to run as root"
    sys.exit(1)
    
directory = '/home/http/'

install_nginx()
create_http_dir(directory)
for subdir in iter_hosts():
    create_host(subdir)

restart_nginx()
