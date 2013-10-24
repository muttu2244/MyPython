#!/usr/bin/python2.5

### Import the system libraries we need.
import sys, os, re

### path.
mydir = os.path.dirname(__file__)
qa_lib_dir = mydir
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)
from logging import getLogger
# grab the root logger.
log = getLogger()

def sa_check(self, dest_ip="20.1.1.2"):
	"""Checks the SA(Security Association) formation in SSX for a particular tunnel ip"""
        sa_exist=self.cmd("show ike-session detail remote %s | grep IPSEC-ESTABLISHED"  % dest_ip)
        if sa_exist and "ERROR:" not in sa_exist:
               return sa_exist
        else:
               return False


def verify_in_sa(self, dest_ip, search_word1, search_word2=""):
	"""Verifies the existance of key words(one or two) in SA(Security Association)"""
        if search_word2:
                search_in_sa=self.cmd("show ike-session detail remote %s | grep %s | grep %s"  % (dest_ip , search_word1, search_word2))
        else:
                search_in_sa=self.cmd("show ike-session detail remote %s | grep %s"  % (dest_ip , search_word1))
        if search_in_sa and "ERROR:" not in search_in_sa:
                return search_in_sa
        else:
                return False


def verify_in_debug(self, search_word1, search_word2=""):
	"""Verifies the existance of key words(one or two) in debug messages"""
        if search_word2:
#                search_result=self.cmd("show log  | grep %s | grep %s" % (search_word1 , search_word2))	#Version 2.0
                search_result=self.cmd("show log debug | grep %s | grep %s" % (search_word1 , search_word2))
        else:
 #               search_result=self.cmd("show log  | grep %s" % search_word1)	#Version 2.0
                search_result=self.cmd("show log debug | grep %s" % search_word1)
        if search_result and "ERROR:" not in search_result:
                return search_result
        else:
                return False

def parse_show_ike_session_detail(self,remote_ip="17.1.1.1"):
    """ Parses the details of ike session established with remote,
            and stores the SA attributes in a dictionary, and return it"""

    regex_list=['\s*SLOT\s+:\s*(?P<slot>\d+)',
                '\s*Session\s+handle\s+:\s*(?P<session_handle>\w+)',
                '\s*IKE\s+Version\s+:\s*(?P<ike_version>\d+)',
                '\s*Nat\s+Status\s+:\s*(?P<nat_status>.*)\r',
                '\s*MOBIKE\s+Status\s+:\s*(?P<mobike_status>.*)\r', 
                '\s*MOBIKE\s+Update\s+Status\s+:\s*(?P<mobike_update_status>.*)\r', 
                '\s*MOBIKE\s+Update\s+Count\s+:\s*(?P<mobike_update_count>.*)\r', 
                '\s*MOBIKE\s+Additional\s+Addr\s+Status\s+:\s*(?P<mobike_additional_address_status>.*)\r',
                '\s*MOBIKE\s+Additional\s+Addr\s+:\s*(?P<mobike_additional_address>.*)\r', 
                '\s*MOBIKE\s+Return-routability\s+:\s*(?P<mobike_return_routability>.*)\r', 
                '\s*Return-routability\s+Retries\s+:\s*(?P<return_routability_retries>.*)\r', 
                '\s*Last\s+Return-routability\s+Check\s+:\s*(?P<last_return_routability_check>.*)\r', 
                '\s*Last\s+Return-routability\s+Ack\s+:\s*(?P<last_return_routability_ack>.*)\r', 
                '\s*Remote\s+tunnel\s+end\s+point\s+:\s*(?P<remote_tunnel_end_point>\S+)\s+Port\s*:\s*(?P<remote_tunnel_end_point_port>\d+)',
                '\s*local\s+tunnel\s+end\s+point\s+:\s*(?P<local_tunnel_end_point>\S+)\s+Port\s*:\s*(?P<local_tunnel_end_point_port>\d+)',
                '\s*Cookie-pair\s+:\s*(?P<cookie_pair>\S+)',
                '\s*IKE-SA\s+ID\s+:\s*(?P<ike_sa_id>\S+)',
                '\s*IKE-SA\s+IDi\s+:\s*(?P<ike_sa_idi>\S+)',
                '\s*IKE-SA\s+IDr\s+:\s*(?P<ike_sa_idr>\S+)',
                '\s*IKE-SA\s+gw-auth\s+method\s+:\s*(?P<ike_sa_gw_auth_method>.*)\r',
                '\s*IKE-SA\s+peer-auth\s+method\s+:\s*(?P<ike_sa_peer_auth_method>.*)\r',
		'\s*IKE-SA\s+sec\s+policy\s+:\s*(?P<ike_sa_sec_policy>.*)\r',
                '\s*IKE-SA\s+PRF\s+:\s*(?P<ike_sa_prf>\S+)',
                '\s*IKE-SA\s+time\s+established\s+:\s*(?P<ike_sa_time_established>.*)\r',
                '\s*IKE-SA\s+life\s+time\s+:\s*(?P<ike_sa_life_time>.*)\r',
                '\s*IKE-SA\s+time\s+remaining\s+:\s*(?P<ike_sa_time_remaining>\d+)',
		'\s*IKE-SA\s+Negotiation\s+Count\s+:\s*(?P<ike_sa_negotiation_count>.*)\r',
                '\s*IP\s+config\s+assigned\s+:\s*IP\s+addr\s+:\s*(?P<ip_config_assigned>\S+)',
		'\s*Child-SA\s+sec\s+policy\s+:\s*(?P<child_sa_sec_policy>.*)\r',
                '\s*Child-SA\s+time\s+established\s+:\s*(?P<child_sa_time_established>.*)\r',
                '\s*Child-SA\s+life\s+time\s+:\s*(?P<child_sa_life_time>\d+)',
		'\s*Child-SA\s+time\s+remaining\s+:\s*(?P<child_sa_time_remaining>\d+)',
		'\s*Child-SA\s+Message\s+Id\s+:\s*(?P<child_sa_message_id>.*)\r',
		'\s*Child-SA\s+Negotiation\s+Count\s+:\s*(?P<child_sa_negotiation_count>.*)\r',
		'\s*In\s+Spi\s+:\s*(?P<in_spi>.*)\r',
		'\s*Out\s+Spi\s+:\s*(?P<out_spi>.*)\r',
		'\s*DPD\s+Status\s+:\s*(?P<dpd_status>.*)\r',
                '\s*DPD\s+ack\s+received\s+at\s+:\s*(?P<dpd_ack>.*)\r',
                '\s*Next\s+DPD\s+check\s+after\s+:\s*(?P<dpd_check>.*)\r',
                '\s*PDG-3GPP\s+State\s+:\s*(?P<pdg_3gpp_state>.*)\r',
                '\s*PDG-3GPP\s+W-APN\s+:\s*(?P<pdg_w_apn>.*)\r',
                '\s*Session\s+State\s+:\s*(?P<session_state>.*)\r',
                '\s*Protocol\s+:\s*(?P<protocol>.*)\r',
                '\s*IPSec\s+Mode\s+:\s*(?P<ipsec_mode>.*)\r']

    actual={}
    ssx_output = self.cmd("show ike-session detail remote %s"  % remote_ip)
    if "ERROR: Session (remote %s) not found on any Card"%remote_ip in ssx_output:
	actual= {'slot': 'None',
		 'session_handle':'None',
		 'ike_version': 'None',
		 'nat_status': 'None',
	  	 'mobike_status':'None',
		 'mobike_update_status':'None',
		 'mobike_update_count':'None',
	  	 'mobike_additional_address_status':'None',
		 'mobike_additional_address':'None',
		 'mobike_return_routability':'None',
		 'return_routability_retries':'None',
		 'last_return_routability_check':'None',
		 'last_return_routability_ack':'None',
	 	 'remote_tunnel_end_point': 'None',
	 	 'local_tunnel_end_point_port': 'None', 
	  	 'cookie_pair': 'None','ike_sa_id': 'None',
	  	 'ike_sa_idi': 'None','ike_sa_idr': 'None',
		 'ike_sa_gw_auth_method': 'None',
		 'ike_sa_peer_auth_method':'None',
		 'ike_sa_sec_policy': 'None',
		 'ike_sa_prf': 'None',
		 'ike_sa_time_established': 'None',
		 'ike_sa_life_time': 'None',
	 	 'ike_sa_time_remaining': 'None',
		 'ike_sa_negotiation_count': 'None',
		 'ip_config_assigned': 'None',
		 'child_sa_sec_policy': 'None', 
		 'child_sa_time_established': 'None', 
		 'local_tunnel_end_point_port': 'None',
		 'remote_tunnel_end_point_port': 'None',
		 'child_sa_life_time': 'None', 
	 	 'child_sa_time_remaining': 'None',
		 'dpd_status': 'None', 
		 'nat_status': 'None', 
		 'session_state': 'None', 
		 'child_sa_message_id': 'None',
		 'child_sa_negotiation_count': 'None',
		 'child_sa_sec_policy': 'None',
		 'in_spi':'None',
		 'out_spi':'None',
                 'dpd_ack':'None',
                 'dpd_check':'None',
                 'pdg_3gpp_state':'None',
                 'pdg_w_apn':'None',
                 'protocol':'None',
                 'ipsec_mode':'None',
                 'dpd_check':'None'}
	return actual
    for regex in regex_list:
        obj=re.compile(regex,re.I)
        m=obj.search(ssx_output)
        if m:
             dict=m.groupdict()
             for key in dict.keys():
                 actual[key]=dict[key]
    return actual

def parse_show_ike_session_detail_glcr_ikev1(self,remote_ip="17.1.1.1"):
    """ Parses the details of ike session established with remote,
            and stores the SA attributes in a dictionary, and return it"""

    regex_list=['\s*SLOT\s+:\s*(?P<slot>\d+)',
                '\s*Session\s+handle\s+:\s*(?P<session_handle>\w+)',
                '\s*IKE\s+Version\s+:\s*(?P<ike_version>\d+)',
                '\s*Nat\s+Status\s+:\s*(?P<nat_status>.*)\r',
                '\s*MOBIKE\s+Status\s+:\s*(?P<mobike_status>.*)\r', 
                '\s*MOBIKE\s+Update\s+Status\s+:\s*(?P<mobike_update_status>.*)\r', 
                '\s*MOBIKE\s+Update\s+Count\s+:\s*(?P<mobike_update_count>.*)\r', 
                '\s*MOBIKE\s+Additional\s+Addr\s+Status\s+:\s*(?P<mobike_additional_address_status>.*)\r',
                '\s*MOBIKE\s+Additional\s+Addr\s+:\s*(?P<mobike_additional_address>.*)\r', 
                '\s*MOBIKE\s+Return-routability\s+:\s*(?P<mobike_return_routability>.*)\r', 
                '\s*Return-routability\s+Retries\s+:\s*(?P<return_routability_retries>.*)\r', 
                '\s*Last\s+Return-routability\s+Check\s+:\s*(?P<last_return_routability_check>.*)\r', 
                '\s*Last\s+Return-routability\s+Ack\s+:\s*(?P<last_return_routability_ack>.*)\r', 
                '\s*Remote\s+tunnel\s+end\s+point\s+:\s*(?P<remote_tunnel_end_point>\S+)\s+Port\s*:\s*(?P<remote_tunnel_end_point_port>\d+)',
                '\s*local\s+tunnel\s+end\s+point\s+:\s*(?P<local_tunnel_end_point>\S+)\s+Port\s*:\s*(?P<local_tunnel_end_point_port>\d+)',
                '\s*Cookie-pair\s+:\s*(?P<cookie_pair>\S+)',
                '\s*Phase1\s+ID\s+:\s*(?P<phase1_id>\S+)',
                '\s*Phase1\s+mode\s+:\s*(?P<phase1_mode>.*)\r',
                '\s*Phase1\s+auth\s+method\s+:\s*(?P<phase1_auth_method>.*)\r',
		'\s*Phase1\s+sec\s+policy\s+:\s*(?P<phase1_sec_policy>.*)\r',
                '\s*Phase1\s+time\s+established\s+:\s*(?P<phase1_time_established>.*)\r',
                '\s*Phase1\s+life\s+time\s+:\s*(?P<phase1_life_time>.*)\r',
                '\s*Phase1\s+time\s+remaining\s+:\s*(?P<phase1_time_remaining>\d+)',
		'\s*Phase1\s+Negotiation\s+Count\s+:\s*(?P<phase1_negotiation_count>.*)\r',
                '\s*IP\s+config\s+assigned\s+:\s*IP\s+addr\s+:\s*(?P<ip_config_assigned>\S+)',
		'\s*Phase2\s+sec\s+policy\s+:\s*(?P<phase2_sec_policy>.*)\r',
                '\s*Phase2\s+time\s+established\s+:\s*(?P<phase2_time_established>.*)\r',
                '\s*Phase2\s+life\s+time\s+:\s*(?P<phase2_life_time>\d+)',
		'\s*Phase2\s+time\s+remaining\s+:\s*(?P<phase2_time_remaining>\d+)',
		'\s*Phase2\s+Negotiation\s+Count\s+:\s*(?P<phase2_negotiation_count>.*)\r',
		'\s*In\s+Spi\s+:\s*(?P<in_spi>.*)\r',
		'\s*Out\s+Spi\s+:\s*(?P<out_spi>.*)\r',
		'\s*DPD\s+Status\s+:\s*(?P<dpd_status>.*)\r',
                '\s*Session\s+State\s+:\s*(?P<session_state>.*)\r']

    actual={}
    ssx_output = self.cmd("show ike-session detail remote %s"  % remote_ip)
    if "ERROR: Session (remote %s) not found on any Card"%remote_ip in ssx_output:
	actual= {'slot': 'None',
		 'session_handle':'None',
		 'ike_version': 'None',
		 'nat_status': 'None',
	  	 'mobike_status':'None',
		 'mobike_update_status':'None',
		 'mobike_update_count':'None',
	  	 'mobike_additional_address_status':'None',
		 'mobike_additional_address':'None',
		 'mobike_return_routability':'None',
		 'return_routability_retries':'None',
		 'last_return_routability_check':'None',
		 'last_return_routability_ack':'None',
	 	 'remote_tunnel_end_point': 'None',
	 	 'local_tunnel_end_point_port': 'None', 
	  	 'cookie_pair': 'None',
		 'phase1_id': 'None',
		 'phase1_auth_method': 'None',
		 'phase1_sec_policy': 'None',
		 'phase1_time_established': 'None',
		 'phase1_life_time': 'None',
	 	 'phase1_time_remaining': 'None',
		 'phase1_negotiation_count': 'None',
		 'ip_config_assigned': 'None',
		 'phase2_sec_policy': 'None', 
		 'phase2_time_established': 'None', 
		 'local_tunnel_end_point_port': 'None',
		 'remote_tunnel_end_point_port': 'None',
		 'phase2_life_time': 'None', 
	 	 'phase2_time_remaining': 'None',
		 'dpd_status': 'None', 
		 'nat_status': 'None', 
		 'session_state': 'None', 
		 'phase2_negotiation_count': 'None',
		 'in_spi':'None',
		 'out_spi':'None'}
	return actual
    for regex in regex_list:
        obj=re.compile(regex,re.I)
        m=obj.search(ssx_output)
        if m:
             dict=m.groupdict()
             for key in dict.keys():
                 actual[key]=dict[key]
    return actual


def get_ses_counters(self, rem_ip):
        actual=parse_show_ike_session_detail(self,rem_ip)
        session_handle=actual['session_handle']
        lines= self.cmd("show session counters handle %s"  % session_handle)
        if lines and "ERROR:" not in lines:
           if '@' in lines:
              split_lines=lines.split('@')[1].split()
           else:
              split_lines=lines.split('\s+')[0].split()
           rx_pkts=split_lines[2]
           tx_pkts=split_lines[3]
           return int(rx_pkts), int(tx_pkts)
        else:
           return False

def get_ike_ses_counters(self):
        actualCmd = self.cmd("sh ike-session counters")
        count=self.cmd("sh ike-session counters | grep \"Active Sessions\"",timeout = 120)
        if count :
           count_regex=re.search("Active Sessions:\s+(\d+)", count, re.I)
           #self.failUnless(not re.match("ERROR: No counters found in context", count), " No sessions found on any Card ")
        else:
           log.output("No sessions found")
           return 0
        if count_regex:
           log.output("Total number of sessions %s" % count_regex.group(1))
           count=int(count_regex.group(1))
        else:
           log.output("No sessions found")
        return count


def parse_show_pdif_session_detail(self,remote_ip="10.1.1.2"):
    """ Parses the details of ike session established with remote,
            and stores the SA attributes in a dictionary, and return it"""

    regex_list=['\s*SLOT\s+:\s*(?P<slot>\d+)',
                '\s*Session\s+handle\s+:\s*(?P<session_handle>\w+)',
                '\s*IKE\s+Version\s+:\s*(?P<ike_version>\d+)',
                '\s*Nat\s+Status\s+:\s*(?P<nat_status>.*)\r',
                '\s*MOBIKE\s+Status\s+:\s*(?P<mobike_status>.*)\r', 
                '\s*MOBIKE\s+Update\s+Status\s+:\s*(?P<mobike_update_status>.*)\r', 
                '\s*MOBIKE\s+Update\s+Count\s+:\s*(?P<mobike_update_count>.*)\r', 
                '\s*MOBIKE\s+Additional\s+Addr\s+Status\s+:\s*(?P<mobike_additional_address_status>.*)\r',
                '\s*Remote\s+tunnel\s+end\s+point\s+:\s*(?P<remote_tunnel_end_point>\S+)\s+Port\s*:\s*(?P<remote_tunnel_end_point_port>\d+)',
                '\s*local\s+tunnel\s+end\s+point\s+:\s*(?P<local_tunnel_end_point>\S+)\s+Port\s*:\s*(?P<local_tunnel_end_point_port>\d+)',
                '\s*Cookie-pair\s+:\s*(?P<cookie_pair>\S+)',
                '\s*IKE-SA\s+ID\s+:\s*(?P<ike_sa_id>\S+)',
                '\s*IKE-SA\s+gw-auth\s+method\s+:\s*(?P<ike_sa_gw_auth_method>.*)\r',
                '\s*IKE-SA\s+peer-auth\s+method\s+:\s*(?P<ike_sa_peer_auth_method>.*)\r',
		'\s*IKE-SA\s+sec\s+policy\s+:\s*(?P<ike_sa_sec_policy>.*)\r',
                '\s*IKE-SA\s+PRF\s+:\s*(?P<ike_sa_prf>\S+)',
                '\s*IKE-SA\s+time\s+established\s+:\s*(?P<ike_sa_time_established>.*)\r',
                '\s*IKE-SA\s+life\s+time\s+:\s*(?P<ike_sa_life_time>.*)\r',
                '\s*IKE-SA\s+time\s+remaining\s+:\s*(?P<ike_sa_time_remaining>\d+)',
		'\s*IKE-SA\s+Negotiation\s+Count\s+:\s*(?P<ike_sa_negotiation_count>.*)\r',
                '\s*IP\s+config\s+assigned\s+:\s*IP\s+addr\s+:\s*(?P<ip_config_assigned>\S+)',
		'\s*Child-SA\s+sec\s+policy\s+:\s*(?P<child_sa_sec_policy>.*)\r',
                '\s*Child-SA\s+time\s+established\s+:\s*(?P<child_sa_time_established>.*)\r',
                '\s*Child-SA\s+life\s+time\s+:\s*(?P<child_sa_life_time>\d+)',
		'\s*Child-SA\s+time\s+remaining\s+:\s*(?P<child_sa_time_remaining>\d+)',
		'\s*Child-SA\s+Message\s+Id\s+:\s*(?P<child_sa_message_id>\d+)',
		'\s*Child-SA\s+Negotiation\s+Count\s+:\s*(?P<child_sa_negotiation_count>.*)\r',
		'\s*In\s+Spi\s+:\s*(?P<out_spi>.*)\r',
		'\s*Out\s+Spi\s+:\s*(?P<out_spi>.*)\r',
		'\s*DPD\s+Status\s+:\s*(?P<dpd_status>.*)\r',
		'\s*MOBIKE\s+Return-routability\s+:\s*(?P<mobike_return_routability>.*)\r',
		'\s*PDIF-3GPP2\s+State\s+:\s*(?P<pdif_3gpp2_state>.*)\r',
		'\s*PDIF-3GPP2\s+MIP\s+Mode\s+:\s*(?P<pdif_3gpp2_mip_mode>.*)\r',
		'\s*PDIF-3GPP2\s+MIP\s+HA\s+:\s*(?P<pdif_3gpp2_mip_ha>.*)\r',
		'\s*PDIF-3GPP2\s+MIP\s+HoA\s+:\s*(?P<pdif_3gpp2_mip_hoa>.*)\r',
		'\s*PDIF-3GPP2\s+MIP\s+Tunnel\s+Handle\s+:\s*(?P<pdif_3gpp2_mip_tunnel_handle>.*)\r',
                '\s*Session\s+State\s+:\s*(?P<session_state>.*)\r']

    actual={}
    ssx_output = self.cmd("show ike-session detail remote %s"  % remote_ip)
    if "ERROR: Session (remote %s) not found on any Card"%remote_ip in ssx_output:
	actual= {'slot': 'None',
		 'session_handle':'None',
		 'ike_version': 'None',
		 'nat_status': 'None',
	  	 'mobike_status':'None',
		 'mobike_update_status':'None',
		 'mobike_update_count':'None',
	  	 'mobike_additional_address_status':'None',
	 	 'remote_tunnel_end_point': 'None',
	 	 'local_tunnel_end_point': 'None', 
		 'local_tunnel_end_point_port': 'None',
		 'remote_tunnel_end_point_port': 'None',
	  	 'cookie_pair': 'None',
                 'ike_sa_id': 'None',
		 'ike_sa_gw_auth_method': 'None',
		 'ike_sa_peer_auth_method':'None',
		 'ike_sa_sec_policy': 'None',
		 'ike_sa_prf': 'None',
		 'ike_sa_time_established': 'None',
		 'ike_sa_life_time': 'None',
	 	 'ike_sa_time_remaining': 'None',
		 'ike_sa_negotiation_count': 'None',
		 'ip_config_assigned': 'None',
		 'child_sa_sec_policy': 'None', 
		 'child_sa_time_established': 'None', 
		 'child_sa_life_time': 'None', 
	 	 'child_sa_time_remaining': 'None',
	 	 'child_sa_message_id': 'None',
		 'child_sa_negotiation_count': 'None',
		 'in_spi':'None',
		 'out_spi':'None',
		 'dpd_status': 'None', 
		 'mobike_return_routability': 'None', 
		 'pdif_3gpp2_state': 'None', 
		 'pdif_3gpp2_mip_mode': 'None', 
		 'pdif_3gpp2_mip_ha': 'None', 
		 'pdif_3gpp2_mip_hoa': 'None', 
		 'pdif_3gpp2_mip_tunnel_handle': 'None', 
		 'session_state': 'None'} 
	return actual
    for regex in regex_list:
        obj=re.compile(regex,re.I)
        m=obj.search(ssx_output)
        if m:
             dict=m.groupdict()
             for key in dict.keys():
                 actual[key]=dict[key]
    return actual


def tunnel_check(self, fa_coa_ip="123.123.123.123", ha_ip="100.1.1.2"):
        """Checks the SA(Security Association) formation in SSX for a particular tunnel ip"""
        fa_ip_exist=self.cmd("show tunnel | grep %s"  % fa_coa_ip)
        ha_ip_exist=self.cmd("show tunnel | grep %s"  % ha_ip)
        if fa_ip_exist and  ha_ip_exist and "ERROR:" not in fa_ip_exist and "ERROR:" not in ha_ip_exist:
               return fa_ip_exist
        else:
               return False

def parse_show_pdif_session_detail_mobike(self,remote_ip="10.1.1.2"):
    """ Parses the details of ike session established with remote,
            and stores the SA attributes in a dictionary, and return it"""

    regex_list=['\s*SLOT\s+:\s*(?P<slot>\d+)',
                '\s*Session\s+handle\s+:\s*(?P<session_handle>\w+)',
                '\s*IKE\s+Version\s+:\s*(?P<ike_version>\d+)',
                '\s*Nat\s+Status\s+:\s*(?P<nat_status>.*)\r',
                '\s*MOBIKE\s+Status\s+:\s*(?P<mobike_status>.*)\r', 
                '\s*MOBIKE\s+Update\s+Status\s+:\s*(?P<mobike_update_status>.*)\r', 
                '\s*MOBIKE\s+Update\s+Count\s+:\s*(?P<mobike_update_count>.*)\r', 
                '\s*MOBIKE\s+Additional\s+Addr\s+Status\s+:\s*(?P<mobike_additional_address_status>.*)\r',
                '\s*Remote\s+tunnel\s+end\s+point\s+:\s*(?P<remote_tunnel_end_point>\S+)\s+Port\s*:\s*(?P<remote_tunnel_end_point_port>\d+)',
                '\s*Last\s+Remote\s+tunnel\s+end\s+point\s+:\s*(?P<last_remote_tunnel_end_point>\S+)\s+Port\s*:\s*(?P<last_remote_tunnel_end_point_port>\d+)',
                '\s*local\s+tunnel\s+end\s+point\s+:\s*(?P<local_tunnel_end_point>\S+)\s+Port\s*:\s*(?P<local_tunnel_end_point_port>\d+)',
                '\s*Cookie-pair\s+:\s*(?P<cookie_pair>\S+)',
                '\s*IKE-SA\s+ID\s+:\s*(?P<ike_sa_id>\S+)',
                '\s*IKE-SA\s+gw-auth\s+method\s+:\s*(?P<ike_sa_gw_auth_method>.*)\r',
                '\s*IKE-SA\s+peer-auth\s+method\s+:\s*(?P<ike_sa_peer_auth_method>.*)\r',
		'\s*IKE-SA\s+sec\s+policy\s+:\s*(?P<ike_sa_sec_policy>.*)\r',
                '\s*IKE-SA\s+PRF\s+:\s*(?P<ike_sa_prf>\S+)',
                '\s*IKE-SA\s+time\s+established\s+:\s*(?P<ike_sa_time_established>.*)\r',
                '\s*IKE-SA\s+life\s+time\s+:\s*(?P<ike_sa_life_time>.*)\r',
                '\s*IKE-SA\s+time\s+remaining\s+:\s*(?P<ike_sa_time_remaining>\d+)',
		'\s*IKE-SA\s+Negotiation\s+Count\s+:\s*(?P<ike_sa_negotiation_count>.*)\r',
                '\s*IP\s+config\s+assigned\s+:\s*IP\s+addr\s+:\s*(?P<ip_config_assigned>\S+)',
		'\s*Child-SA\s+sec\s+policy\s+:\s*(?P<child_sa_sec_policy>.*)\r',
                '\s*Child-SA\s+time\s+established\s+:\s*(?P<child_sa_time_established>.*)\r',
                '\s*Child-SA\s+life\s+time\s+:\s*(?P<child_sa_life_time>\d+)',
		'\s*Child-SA\s+time\s+remaining\s+:\s*(?P<child_sa_time_remaining>\d+)',
		'\s*Child-SA\s+Message\s+Id\s+:\s*(?P<child_sa_message_id>\d+)',
		'\s*Child-SA\s+Negotiation\s+Count\s+:\s*(?P<child_sa_negotiation_count>.*)\r',
		'\s*In\s+Spi\s+:\s*(?P<out_spi>.*)\r',
		'\s*Out\s+Spi\s+:\s*(?P<out_spi>.*)\r',
		'\s*DPD\s+Status\s+:\s*(?P<dpd_status>.*)\r',
		'\s*MOBIKE\s+Return-routability\s+:\s*(?P<mobike_return_routability>.*)\r',
		'\s*PDIF-3GPP2\s+State\s+:\s*(?P<pdif_3gpp2_state>.*)\r',
		'\s*PDIF-3GPP2\s+MIP\s+Mode\s+:\s*(?P<pdif_3gpp2_mip_mode>.*)\r',
		'\s*PDIF-3GPP2\s+MIP\s+HA\s+:\s*(?P<pdif_3gpp2_mip_ha>.*)\r',
		'\s*PDIF-3GPP2\s+MIP\s+HoA\s+:\s*(?P<pdif_3gpp2_mip_hoa>.*)\r',
		'\s*PDIF-3GPP2\s+MIP\s+Tunnel\s+Handle\s+:\s*(?P<pdif_3gpp2_mip_tunnel_handle>.*)\r',
                '\s*Session\s+State\s+:\s*(?P<session_state>.*)\r']

    actual={}
    ssx_output = self.cmd("show ike-session detail remote %s"  % remote_ip)
    if "ERROR: Session (remote %s) not found on any Card"%remote_ip in ssx_output:
	actual= {'slot': 'None',
		 'session_handle':'None',
		 'ike_version': 'None',
		 'nat_status': 'None',
	  	 'mobike_status':'None',
		 'mobike_update_status':'None',
		 'mobike_update_count':'None',
	  	 'mobike_additional_address_status':'None',
	 	 'remote_tunnel_end_point': 'None',
	 	 'last_remote_tunnel_end_point': 'None',
	 	 'local_tunnel_end_point': 'None', 
		 'local_tunnel_end_point_port': 'None',
		 'remote_tunnel_end_point_port': 'None',
		 'last_remote_tunnel_end_point_port': 'None',
	  	 'cookie_pair': 'None',
                 'ike_sa_id': 'None',
		 'ike_sa_gw_auth_method': 'None',
		 'ike_sa_peer_auth_method':'None',
		 'ike_sa_sec_policy': 'None',
		 'ike_sa_prf': 'None',
		 'ike_sa_time_established': 'None',
		 'ike_sa_life_time': 'None',
	 	 'ike_sa_time_remaining': 'None',
		 'ike_sa_negotiation_count': 'None',
		 'ip_config_assigned': 'None',
		 'child_sa_sec_policy': 'None', 
		 'child_sa_time_established': 'None', 
		 'child_sa_life_time': 'None', 
	 	 'child_sa_time_remaining': 'None',
	 	 'child_sa_message_id': 'None',
		 'child_sa_negotiation_count': 'None',
		 'in_spi':'None',
		 'out_spi':'None',
		 'dpd_status': 'None', 
		 'mobike_return_routability': 'None', 
		 'pdif_3gpp2_state': 'None', 
		 'pdif_3gpp2_mip_mode': 'None', 
		 'pdif_3gpp2_mip_ha': 'None', 
		 'pdif_3gpp2_mip_hoa': 'None', 
		 'pdif_3gpp2_mip_tunnel_handle': 'None', 
		 'session_state': 'None'} 
	return actual
    for regex in regex_list:
        obj=re.compile(regex,re.I)
        m=obj.search(ssx_output)
        if m:
             dict=m.groupdict()
             for key in dict.keys():
                 actual[key]=dict[key]
    return actual

def getDeletedHndl(self,delReason=""):
	""" Returns the List of session handles for the deleted sessions
	API accepts Delete Reason as input, If no session deleted for the 
	given reason returns 1
	"""
        reason_op = self.cmd("diag ipsec session all | grep -i \"%s\""%delReason)
        if not reason_op:
                log.output("No session deleted with the reason - %s"%delReason)
                return 1
        log.info("There are '%d' sessions deleted with the reason '%s'"%(len(reason_op.splitlines())-1,delReason))
        op = self.cmd("diag ipsec session all")
        log.info("Getting the Remote IP for the Deleted sessions")
        rem_op = op.split("Remote IP")
        length = len(op.split("Remote IP"))
        wantedList = []
        ses_hndl = []
        wantedListIndex = 0
        for index in range(1,length+1):
		index = index - 1
                if delReason.upper() in rem_op[index].upper():
                        wantedList[wantedListIndex] = wantedList.append("")
                        ses_hndl[wantedListIndex] = ses_hndl.append("")
                        wantedList[wantedListIndex] = rem_op[index]
                        #Getting the remote IP
                        wantedList[wantedListIndex] = wantedList[wantedListIndex].split()[1]
                        #Getting the session handle
                        ses_op = self.cmd("show ike-session detail remote %s | grep -i \"Session handle\""%wantedList[wantedListIndex])
                        if "ERROR:" in ses_op:
                                log.error("Can not find detail for the remote or No Remote IP for the Given Delete Reason")
                        else :
                                ses_hndl[wantedListIndex] = ses_op.splitlines()[1].split(":")[1].strip()
                        wantedListIndex = wantedListIndex + 1

        return ses_hndl

