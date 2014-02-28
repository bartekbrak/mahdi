#!/usr/bin/env python
from bottle import route, run, request, response, static_file
from subprocess import Popen, PIPE
import shlex


def jsonp(request, dictionary):
    if (request.query.callback):
        return "%s(%s)" % (request.query.callback, dictionary)
    return dictionary


def get_disk_space(server, device='/dev/sda1'):
    space = Popen(
        shlex.split("ssh %s 'df %s | egrep -o \"[0-9]{2,3}%%\" | tr -d %%'" % (server, device)), stdout=PIPE
    ).stdout.read().strip()
    return space


def last_modification_time(server, myfile):
    mtime = Popen(
        shlex.split("ssh %s 'find %s -maxdepth 0 -printf \"%%Tm/%%Td %%TH:%%TM\"'" % (server, myfile)), stdout=PIPE
    ).stdout.read().strip()
    return mtime


@route('/')
def about():
    # response.content_type = "text/plain"
    return static_file('README.html', '.')


@route('/disk_usage')
def disk_usage():
    '''disk usage percentage values'''
    r = {}
    if (request.query.callback):
        response.content_type = "application/javascript"
    r['pko_qa_cmsf_sda1'] = get_disk_space('pko_qa_cmsf', '/dev/sda1')
    r['pko_qa_cmsf_sdd1'] = get_disk_space('pko_qa_cmsf', '/dev/sdd1')
    r['pko_qa_cmsf_sda3'] = get_disk_space('pko_qa_cmsf', '/dev/sda3')

    r['pko_qa_cmspub_sda1'] = get_disk_space('pko_qa_cmspub', '/dev/sda1')
    r['pko_qa_cmspub_sdb1'] = get_disk_space('pko_qa_cmspub', '/dev/sdb1')

    r['pko_qa_app_sda1'] = get_disk_space('pko_qa_app', '/dev/sda1')
    r['pko_qa_app_sdb1'] = get_disk_space('pko_qa_app', '/dev/sdb1')

    r['pko_pr_cmspub_sda1'] = get_disk_space('pko_pr_cmspub', '/dev/sda1')
    r['pko_pr_cmspub_mpath1'] = get_disk_space('pko_pr_cmspub', '/dev/mapper/mpath1')
    r['pko_pr_cmsf_sda1'] = get_disk_space('pko_pr_cmsf', '/dev/sda1')
    r['pko_pr_cmsf_sdb1'] = get_disk_space('pko_pr_cmsf', '/dev/sdb1')
    r['pko_pr_web1_df'] = get_disk_space('pko_pr_web1')
    r['pko_pr_web2_df'] = get_disk_space('pko_pr_web2')
    r['pko_pr_web3_df'] = get_disk_space('pko_pr_web3')
    r['pko_pr_web4_df'] = get_disk_space('pko_pr_web4')

    return jsonp(request, r)


@route('/ping.gif')
def ping():
    ''' Serves one pixel wide black pixel for the JS part to attempt to download
    to check if server is running. That's javascript for you. That's the easiest way.

    Discontinued. No checking. If server goes down, restart it and refresh frontend'''
    response.content_type = 'image/gif'
    gif = (b'\x47\x49\x46\x38\x37\x61\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00\xff'
           b'\xff\xff\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b')
    return gif


@route('/mtimes')
def mtimes():
    ''' Various log files modification times'''
    r = {}
    if (request.query.callback):
        response.content_type = "application/javascript"

    r['last_qa_publish_log'] = last_modification_time('pko_qa_cmspub', '/var/www/pkobp-portal/log/cmd_publish.log')
    r['last_pr_publish_log'] = last_modification_time('pko_pr_cmspub', '/var/www/pkobp-portal/log/cmd_publish.log')

    return jsonp(request, r)

run(host='127.0.0.1', port=8080, reloader=True)
