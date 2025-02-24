#!/usr/bin/python3
import enum
import os


class FwutechEnum(enum.Enum):

    RESTART_AGENT_CMD = 'systemctl restart fwutech'
    DATE_CMD = "bash %s/lateral_tools/setDate.sh"
    IP_LINK_CMD = "ip link"
    MOUNT_READONLY_CMD="mount -o remount,ro /home"
    MOUNT_WRITEABLE_CMD="mount -o remount,rw /home"

    CONFIG_PATH = "%sconf.json"
    INFO_PATH = "%sinfo.json"
    USR_SEC_PATH = "%susr_sec.json"
    RESULT_DIR_PATH = "/tmp/scen_res_dir/"
    CHANGE_IP_SCRPT_PATH = "%s/lateral_tools/net_scripts/change_config.sh"

    SEND_RESULT_URL = "http://%s:%s/result/exec"
    DATE_URL = "\"http://%s:%s/uitls/getIpAndDate?mid=%s&parent=%s&operator=%s&model=%s&type=%s\""
    GET_PARENT_MID_URL = "http://%s/probe/interface/mid/get"
    CHECK_UPDATE_URL="http://%s:%s/update/config/checkUpdate?mid=%s"
    CHECK_WEB_PASSWD_URL="http://%s:%s/update/config/web/check/sec?mid=%s"
    UPDATE_WEB_PASSWD_URL="http://%s:%s/update/config/web/update/sec?mid=%s"
    UPDATE_WEB_PASSWD_COMPLATE_URL="http://%s:%s/update/config/web/update/sec/complate?mid=%s"
    UPDATE_CONFIG_URL="http://%s:%s/update/config?mid=%s"
    UPDATE_COMPLATE_URL="http://%s:%s/update/config/complete?mid=%s"
    UPGRADE_COMPLATE_URL="http://%s:%s/update/tool/upgrade/complate?mid=%s&tool=%s"
    UPGRADE_TOOLS_LIST_URL="http://%s:%s/update/tools/upgrade/list?mid=%s"
    DOWNLOAD_TOOL_URL = "http://%s:%s/update/tools/upgrade?mid=%s&tool="

    DATE_FAILD_MSG = "there is some wrong in Date Syncing!"
    RESULT_SEND_FAILD_MSG = "Can not send result to Server.(faild) !"
    RESULT_SEND_SUCCESS_MSG = "Send Result to Sever successfuly !"
    SUCCESS_REMOVE_RSLT_MSG = "File: %s removed!"
    FAILD_REMOVE_RSLT_MSG = "Can not remove File: %s !"
    SAVE_RSLT_TO_TEMP_SUCC_MSG = "result saved !"
    SAVE_RSLT_TO_TEMP_FAILD_MSG = "Cant result saved!"
    SAVE_INFO_SUCC_MSG = "info saved!"
    SAVE_SCENARIO_SUCC_MSG = "Scenario updated!"
    SAVE_WEB_SEC_SUCC_MSG = "web security updated!"
    CHECKING_UPDATE_SCENARIO_MSG="checking Config Update"
    CHECKING_CHECK_WEB_PASSWORD="checking Web Password"
    NOTHING_UPDATE_SCEN_MSG="There is not any scenario update !"
    NOTHING_UPDATE_WEB_SEC_MSG="There is not any WEB SECURITY update !"
    CHECK_SCENARIO_FAILD_MSG="Error: check scenario is faild !"
    CHECK_WEB_SEC_FAILD_MSG="Error: check Update WEB SECURITY is faild !"
    UPGRADE_COMPLATED_SUCCESS_MSG="%s upgrate Complated !"
    CHECKING_UPDATE_TOOLS_MSG="checking upgrade tools!"
    NOTHING_TO_UPGRADE_TOOLS="There isnt any upgrade tool!"


#   for web command
    PIN1_FIND_IP_CMD="cat /etc/network/interfaces.d/eth0 |grep -b0 address | awk '{print $3}'"
    PIN2_FIND_IP_CMD="cat /etc/network/interfaces.d/eth1 |grep -b0 address | awk '{print $3}'"
    PIN1_FIND_NETMASK_CMD="cat /etc/network/interfaces.d/eth0 |grep -b0 netmask | awk '{print $3}'"
    PIN2_FIND_NETMASK_CMD="cat /etc/network/interfaces.d/eth1 |grep -b0 netmask | awk '{print $3}'"
    PIN1_FIND_GATEWAY_CMD="ip route |grep default |  awk '{print $3}'"
    PIN2_FIND_GATEWAY_CMD="ip route |grep default |  awk '{print $3}'"

    DNS_FIND_CMD="cat /etc/resolv.conf | grep -b0 nameserver  | awk '{print $2}'"
    
    
