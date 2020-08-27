#-*- coding:utf-8 -*-#
#author chunjietang@tencent.com
import config
import requests
import zlog
import os
import json
import time

conf_log = zlog.Logger('domain_log', stream=True, logfile='%s/get_cdn_domain.log'%config.LOG_PATH)

#本地cdn domain文件
LOCAL_CDN_DOMAIN_FILE = os.path.join(config.BASE_PATH, 'conf', 'cdn_domain.json')
LOCAL_CDN_DOMAIN_TMP_FILE = os.path.join(config.BASE_PATH, 'conf', 'cdn_domain.json.tmp')

#请求domain文件的url
GET_CDN_DOMAIN_URL  = 'http://'+config.get_config_ip+':'+'8888'+'/cdn_domain?md5=%s'

if __name__ == '__main__':
    start_delay_ts = int(hash(config.local_ip) % 180)
    conf_log.info("sleep %s s"%start_delay_ts)
    time.sleep(start_delay_ts)

    local_md5 = "d41d8cd98f00b204e9800998ecf8427e"
    if os.path.exists(LOCAL_CDN_DOMAIN_FILE):
        with open(LOCAL_CDN_DOMAIN_FILE, "r") as f:
            local_cfg = json.loads(f.read())
            local_md5 = local_cfg['md5']

    reqUrl = GET_CDN_DOMAIN_URL%(local_md5)
    r = requests.get(reqUrl, timeout=120)
    if r.status_code != 200:
        conf_log.error("get conf error:%s url:%s"%(r.status_code, reqUrl))
        exit(0)
    conf_log.info("get config url:%s"% reqUrl)

    #返回内容解析
    data = dict()
    data = json.loads(r.text)

    if data['status_code'] != 200:
        conf_log.error("domain server error:%s, status_code:%s"%(data['msg'], data['status_code']))
        exit(0)

    if not data['is_update']:
        conf_log.info("domain list no need update.")
        exit(0)  

    with open(LOCAL_CDN_DOMAIN_TMP_FILE,'wb') as f:
        f.write(json.dumps(data))

    os.rename(LOCAL_CDN_DOMAIN_TMP_FILE, LOCAL_CDN_DOMAIN_FILE)
    conf_log.info("make new domain file:%s", LOCAL_CDN_DOMAIN_FILE)
    conf_log.info("old md5:%s, new md5:%s", local_md5, data['md5'])

