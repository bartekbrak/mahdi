#!/usr/bin/env python
from bottle import route, run, request, response
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


@route('/')
def index():
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
    r['pko_pr_cmspub_df'] = get_disk_space('pko_pr_cmspub')
    r['pko_pr_cmsf_df'] = get_disk_space('pko_pr_cmsf')
    r['pko_pr_web1_df'] = get_disk_space('pko_pr_web1')
    r['pko_pr_web2_df'] = get_disk_space('pko_pr_web2')
    r['pko_pr_web3_df'] = get_disk_space('pko_pr_web3')
    r['pko_pr_web4_df'] = get_disk_space('pko_pr_web4')

    return jsonp(request, r)

run(host='0.0.0.0', port=8080, reloader=True)
