# from base_logger import logging
# from Config import Config
# import utils as Utils

from bomancli import utils as Utils
from bomancli.base_logger import logging
from bomancli.Config import Config


import yaml
import json
import requests
import os


#### read the input from the yaml file -- MM ------------------------------------------------------------

def yamlValidation():

    logging.info('Finding boman.yaml file')

    #Config.boman_config_file 

    try: 
        with open(Config.boman_config_file, 'r') as file:
            Config.config_data = yaml.safe_load(file)    
        logging.info('Config yaml file found')    
    except:
        
        logging.error('No config yaml file found')
        exit(4) ## validation error 

    logging.info('Prasing and Validating the config yaml file')
   


    try:
        Config.config_data['Auth']
        if Config.config_data['Auth'] != '':
            Config.app_token = Config.config_data['Auth']['project_token']
            Config.customer_token =Config.config_data['Auth']['customer_token']


    except KeyError:

        logging.error('Project and Customer token is mandatory to run the scan. Refer the documentation.')    


    try: 

        if  Config.config_data['SAST'] != '':
            Config.sast_lang = Config.config_data['SAST']['language'].split(",") ## comma sperated if mulitple
            
            Config.sast_present = True
            Config.sast_message = 'SAST is properly configured'
            logging.info('SAST is properly configured with %s and ready to scan',Config.sast_lang)

            try:
                logging.info('choosing the sast working directory')
                Config.sast_build_dir  = Config.config_data['SAST']['work_dir']
            except KeyError: 
                logging.info('work dir not specified in config, choosing the default sast working directory')
                Config.sast_build_dir = os.getcwd()+'/'
                
            try:
                logging.info('Ignoring file and folder check')
                Config.sast_ignore =  Config.config_data['SAST']['ignore_files']
            except KeyError: 
                logging.info('ignore_files config was not found')
                

            #logging.info('snyk is choosen, and the env var declared was %s', str('s'))


            



        if 'java' in Config.sast_lang:

            try:
                Config.sast_target =  Config.config_data['SAST']['target']
            except KeyError: 
                logging.error('Java requires a target file to be mentioned in the boman.yaml file. refer the documentation')
                Config.sast_present = False       
                Config.sast_message = 'SAST is not configured properly, Java requires a target file to be mentioned in the boman.yaml file. refer the documentation'    
        


        # if 'python-snyk' in Config.sast_lang:

        #         try:
        #             Config.sast_env = Config.config_data['SAST']['env']
        #             logging.info('snyk is choosen, and the env var declared was %s', str(Config.sast_env))
        #         except KeyError: 
        #             logging.error('Snyk requires a enviromenet var for snyk auth token to be mentioned in the boman.yaml file. refer the documentation')
        #             Config.sast_present = False 

        
    except KeyError:    
        Config.sast_present = False
        Config.sast_message = 'SAST was not properly defined in the config, Please check your boman.yaml file.'
        logging.warning('SAST was not properly defined in the config')
        logging.warning('Ignoring SAST, Please provide all mandatory inputs incase you like to run SAST scan.')
        

    
    ## DAST

    try: 
        Config.dast_target = Config.config_data['DAST']['URL']
        Config.dast_type = Config.config_data['DAST']['type']

        Config.dast_present = True

        try:        
            if Config.config_data['DAST']['auth'] == 'yes':
                Config.dast_auth_present = True
        except KeyError: 
            Config.dast_auth_present = False 


        if Utils.testDastUrl(Config.dast_target):
            logging.info('DAST is properly configured and ready to scan')
            
            if Config.dast_type == 'API':
                try:  
                    logging.info('DAST is configured for API scan, checking API type.')    
                    Config.dast_api_type = Config.config_data['DAST']['api_type']
                    
                except KeyError:
                    logging.info('DAST API type is not given, proceeding with default value: OPENAPI')
                    Config.dast_api_type = 'openapi'  


        else:    
            logging.info('DAST target is not reachable, ignoring DAST scan')
            Config.dast_present = False
            Config.dast_message = 'DAST target is not reachable. DAST scan was ignored'
                
    except KeyError:    
        Config.dast_present = False
        Config.dast_message = 'DAST was not properly defined in the config.'
        logging.warning('DAST was not properly defined in the config.')
        logging.warning('Ignoring DAST, Please provide all mandatory inputs incase you like to run DAST scan.')
        

        
               


    ## SCA

    try: 
        if  Config.config_data['SCA'] != '':
            Config.sca_lang = Config.config_data['SCA']['language'].split(",") ## comma sperated if mulitple
            
            Config.sca_present =  True
            Config.sca_build_dir = os.getcwd()+'/'
            
            try:
                logging.info('Configuring scan type for SCA')
                Config.sca_type = Config.config_data['SCA']['type']
                logging.info(f'Scan type configured for SCA: {Config.sca_type}')
            except KeyError: 
                logging.info('Scan type for SCA not found. SCA will run with default scan type directory')
                Config.sca_type = "directory" # other options sbom and lockfile

            #depricated

            # try:
            #     logging.info('Configuring work directory for SCA')
            #     Config.sca_build_dir = Config.config_data['SCA']['work_dir']
            #     logging.info('Work directory found for SCA')
            # except KeyError: 
            #     logging.info('No work directory for SCA. Default work directory is set')
            #     ##after sbom and lockfile type check
            #     Config.sca_build_dir = os.getcwd()+'/'
                
            try:
                logging.info('Ignoring file and folder check')
                Config.sca_ignore =  Config.config_data['SCA']['ignore_files']
            except KeyError: 
                logging.info('ignore_files config was not found')    
                
            try:
                logging.info('Configuring target for SCA')
                Config.sca_target = Config.config_data['SCA']['target']
                logging.info(f'Target configured for SCA: {Config.sca_target}')
            except KeyError: 
                if Config.sca_type == "directory":
                    logging.info(f'Target for SCA not found. SCA will run with default scan type directory: {Config.sca_build_dir}')
                    # Config.sca_target = Config.sca_build_dir
                else:
                    logging.error("Target parameter missing. Target parameter is required for sbom or lockfile type")
                    exit(4)
                             
            Config.sca_message ='SCA is properly configured'
            logging.info('SCA is properly configured and ready to scan')    
    except KeyError:    
        Config.sca_present =  False
        Config.sca_message ='SCA was not properly defined in the config'
        logging.warning('SCA was not properly defined in the config')
        logging.warning('Ignoring SCA, Please provide all mandatory inputs incase you like to run SCA scan.')
        
#ss
    try:
        if Config.config_data['Secret_Scan'] == False:
            Config.secret_scan_present = False
        else:   
            try:
                Config.sast_build_dir  = Config.config_data['SAST']['work_dir']
            except KeyError: 
                Config.sast_build_dir = os.getcwd()+'/'
                 
            try:
                Config.secret_scan_present =  True if Utils.isGitDirectory(Config.sast_build_dir) else False

                if Config.secret_scan_present:
                    logging.info('Secret scanning is properly configured and ready to scan')
                    Config.secret_scan_message ='Secret scanning is properly configured and ready to scan'
                else:
                    logging.warning('Secret scanning is properly configured, but working directory is not a git repository.') 
                    logging.warning('Ignoring Secret scanning.')    
                    Config.secret_scan_message ='Secret scanning is properly configured, but working directory is not a git repository.'       
            except KeyError:
                Config.secret_scan_present = False
                logging.warning('Secret scanning is not properly configured, Working directory is not git.') 
                Config.secret_scan_message ='Secret scanning is not properly configured'     
    except KeyError:
        Config.secret_scan_present = False  
        logging.warning('Secret scanning is not properly configured. Cant read the Secret_Scan configuration.')   
        Config.secret_scan_message ='Secret scanning is not properly configured'  

    try:
        if "container_scan" in Config.config_data:
            Config.con_scan_present = True
            Config.con_scan_build_dir= os.getcwd()+'/'
            try:
                logging.info('Configuring type for Container Scan')
                Config.con_scan_type = str(Config.config_data['container_scan']['type']).lower()
                if not (Config.con_scan_type == "config" or Config.con_scan_type == "image"):
                    logging.error(f"Invalid 'type': {Config.con_scan_type}. 'type' parameter must be 'config' or 'image' for container scanning")
                    exit(4)
                logging.info(f'Type configured for Container Scan: {Config.con_scan_type}')
            except KeyError: 
                logging.error("Type parameter is missing. 'type' parameter is required for container scanning")
                exit(4)
                
            try:
                logging.info('Configuring target for Container Scan')
                Config.con_scan_target = Config.config_data['container_scan']['target']
                if Config.con_scan_target is None:
                    if Config.con_scan_type == "config":
                        Config.con_scan_target= ""
                    else:
                        logging.error("Target is missing. Please configure target properly eg: target: myimage:version")
                        exit(4)
                logging.info(f'Target configured for Container Scan: {Config.con_scan_target}')
            except KeyError:
                if Config.con_scan_type=="config":
                    Config.con_scan_target="/"
                else:     
                    logging.error("Target parameter is missing. 'target' parameter is required for container scanning")
                    exit(4)
            
            logging.info('Container Scan is properly configured and ready to scan')
            Config.con_scan_message ='Container Scan is properly configured and ready to scan'
        else:
            Config.con_scan_present = False
            logging.warning('Container Scan is not properly configured. Cant read the "container_scan" configuration.')   
            Config.con_scan_message ='Container Scan is not properly configured'
    except:
        Config.con_scan_present = False
        logging.warning('Container Scan is not properly configured. Cant read the "container_scan" configuration.')   
        Config.con_scan_message ='Container Scan is not properly configured'

    try:
        if "SBOM" in Config.config_data:
            if Config.config_data['SBOM']:
                Config.sbom_present = True
                Config.sbom_build_dir = os.getcwd()+"/"
                logging.info('SBOM is properly configured and ready to scan')
            else:
                Config.sbom_present = False
                logging.warning('SBOM is not properly configured. Cant read the "sbom" configuration.')   
                Config.sbom_message ='sbom is not properly configured'
           
        else:
            Config.sbom_present = False
            logging.warning('SBOM is not properly configured. Cant read the "sbom" configuration.')   
            Config.sbom_message ='sbom is not properly configured'
    except:
        Config.sbom_present = False  
        logging.warning('SBOM is not properly configured. Cant read the "sbom" configuration.')   
        Config.sbom_message ='sbom is not properly configured'
    
    # Validation of boman.yaml for IaC scanning
    try:
        if "IAC" in Config.config_data:
            Config.iac_scan_present = True
            Config.iac_scan_build_dir= os.getcwd()+'/'
                
            try:
                logging.info('Configuring target for IaC Scan.')
                Config.iac_scan_target = Config.config_data['IAC']['target']
                logging.info(f'Target configured for IaC Scan: {Config.iac_scan_target}')
            except KeyError:
                Config.iac_scan_target="/"
                logging.info("KEY ERROR")
                logging.info('target is missing for IaC Scan. target configured to default path')
            except TypeError:
                Config.iac_scan_target="/"
                logging.info("TYPE ERROR")
                logging.info('target is missing for IaC Scan. target configured to default path')
            
            logging.info('IaC Scan is properly configured and ready to scan')
            Config.iac_scan_message ='IaC Scan is properly configured and ready to scan'
        else:
            Config.iac_scan_present = False
            logging.warning('IaC Scan is not properly configured. Cant read the "IAC" configuration.')   
            Config.iac_scan_message ='IaC Scan is not properly configured'
    except:
        Config.iac_scan_present = False
        logging.warning('IaC Scan is not properly configured. Cant read the "IAC" configuration.')   
        Config.iac_scan_message ='IaC Scan is not properly configured'    
   

## need to use lingudetect here, but the results are not trustable and misleading ------ MM -------------------
def findLang():
    print('[INFO]: Detecting Language')
