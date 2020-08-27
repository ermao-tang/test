#!/bin/bash
dir_pre=$(dirname $(which $0))
pid=$(ps aux|grep 'get_cdn_domain.py' | grep python | awk '{print $2}')
bin=get_cdn_domain.py
day_str=`date +%F`
if [ "$pid" = "" ]; then
    BASE_PATH=$dir_pre/bin/
    set -x
    cd ${BASE_PATH}
    /usr/bin/python ${BASE_PATH}${bin} >> ../log/get_cdn_domain.error.$day_str 2>&1 &
    echo "succ"
    set +x
else
    echo "error"
    exit 0
fi
