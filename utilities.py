
import xbmc, xbmcgui, xbmcaddon, xbmcvfs
import os, sys, time, fileinput, re
import urllib, urllib2

from resources.lib.Globals import *
from resources.lib.utils import *


def showText(heading, text):
    log("showText")
    id = 10147
    xbmc.executebuiltin('ActivateWindow(%d)' % id)
    xbmc.sleep(100)
    win = xbmcgui.Window(id)
    retry = 50
    while (retry > 0):
        try:
            xbmc.sleep(10)
            retry -= 1
            win.getControl(1).setLabel(heading)
            win.getControl(5).setText(text)
            return
        except:
            pass
            
            
def showChangelog(addonID=None):
    log("showChangelog")
    try:
        if addonID:
            ADDON = xbmcaddon.Addon(addonID)
        else: 
            ADDON = xbmcaddon.Addon(ADDONID)
        f = open(ADDON.getAddonInfo('changelog'))
        text  = f.read()
        title = "Changelog - PseudoTV Live"
        showText(title, text)
    except:
        pass


#DonorDownload
DonorURLPath = (PTVLURL + 'Donor.py')
LinkPath = (os.path.join(ADDON_PATH, 'resources', 'lib', 'links.py'))
DonorPath = (os.path.join(ADDON_PATH, 'resources', 'lib', 'Donor.pyo'))
DL_DonorPath = (os.path.join(ADDON_PATH, 'resources', 'lib', 'Donor.py'))


def DDautopatch():
    log("DDautopatch")
    REAL_SETTINGS.setSetting("AT_Donor", "false")
    REAL_SETTINGS.setSetting("COM_Donor", "false")
    REAL_SETTINGS.setSetting("TRL_Donor", "false")
    REAL_SETTINGS.setSetting("CAT_Donor", "false")

    try:
        if xbmcvfs.exists(xbmc.translatePath(DL_DonorPath)):
            xbmcvfs.delete(xbmc.translatePath(DL_DonorPath))
            log('Removed DL_DonorPath')  
            
        if xbmcvfs.exists(xbmc.translatePath(DonorPath)):
            xbmcvfs.delete(xbmc.translatePath(DonorPath))  
            log('Removed DonorPath')  
    except Exception:
        pass
        
    try:
        urllib.urlretrieve(DonorURLPath, (xbmc.translatePath(DL_DonorPath)))
        if xbmcvfs.exists(DL_DonorPath):
            log('DL_DonorPath Downloaded')  
            REAL_SETTINGS.setSetting("AT_Donor", "true")
            REAL_SETTINGS.setSetting("COM_Donor", "true")
            REAL_SETTINGS.setSetting("TRL_Donor", "true")
            REAL_SETTINGS.setSetting("CAT_Donor", "true")
            xbmc.executebuiltin("Notification( %s, %s, %d, %s)" % ("PseudoTV Live", "Donor Autoupdate Complete", 4000, THUMB) ) 
    except Exception:
        pass
    

def DonorDownloader():
    log('DonorDownloader')
    REAL_SETTINGS.setSetting("AT_Donor", "false")
    REAL_SETTINGS.setSetting("COM_Donor", "false")
    REAL_SETTINGS.setSetting("TRL_Donor", "false")
    REAL_SETTINGS.setSetting("CAT_Donor", "false")
    Install = False
    Verified = False
    InstallStatusMSG = 'Activate'  
    
    if xbmcvfs.exists(DonorPath):
        InstallStatusMSG = 'Update'
        if dlg.yesno("PseudoTV Live", str(InstallStatusMSG) + " Donor Features?"):
            try:
                xbmcvfs.delete(xbmc.translatePath(DonorPath))
                log('Removed DonorPath')  
                Install = True
            except Exception: 
                pass
    else:  
        Install = True
    
    if Install == True:
        try:                   
            urllib.urlretrieve(DonorURLPath, (xbmc.translatePath(DL_DonorPath)))
            if xbmcvfs.exists(DL_DonorPath):
                log('DL_DonorPath Downloaded')  
                REAL_SETTINGS.setSetting("AT_Donor", "true")
                REAL_SETTINGS.setSetting("COM_Donor", "true")
                REAL_SETTINGS.setSetting("TRL_Donor", "true")
                REAL_SETTINGS.setSetting("CAT_Donor", "true")
                xbmc.executebuiltin("UpdateLocalAddons")
            
                if REAL_SETTINGS.getSetting('AT_Donor') and REAL_SETTINGS.getSetting('COM_Donor') and REAL_SETTINGS.getSetting('TRL_Donor') and REAL_SETTINGS.getSetting('CAT_Donor'):
                    Verified = True

            if Verified == True:
                MSG = "Donor Features " + str(InstallStatusMSG) + "d"
            else:
                MSG = "Donor Features Not " + str(InstallStatusMSG) + "d"
                
            xbmc.executebuiltin("Notification( %s, %s, %d, %s)" % ("PseudoTV Live", MSG, 1000, THUMB) ) 
            REAL_SETTINGS.openSettings()
        except Exception:
            pass
           
            
def LogoDownloader():
    log('LogoDownloader')    
    if dlg.yesno("PseudoTV Live", "Download Color Logos or No, Download Mono Logos"):
        LogoDEST = os.path.join(LOCK_LOC,'PTVL_Color.zip')
        URLPath = PTVLURL + 'PTVL_Color.zip'
    else:
        LogoDEST = os.path.join(LOCK_LOC,'PTVL_Mono.zip')
        URLPath = PTVLURL + 'PTVL_Mono.zip'

    if not xbmcvfs.exists(LOCK_LOC):
        log('Creating LogoPath')  
        xbmcvfs.mkdir(LOCK_LOC)

    try:
        xbmcvfs.delete(xbmc.translatePath(LogoDEST))
        log('Removed old LogoDEST')  
    except Exception:
        pass
         
    try:
        download(URLPath, LogoDEST)
        all(LogoDEST, LOCK_LOC)
        REAL_SETTINGS.setSetting("ChannelLogoFolder", LOCK_LOC + 'logos')
        
        try:
            xbmcvfs.delete(LogoDEST)
            log('Removed LogoDEST')  
        except Exception:
            pass   
    except Exception:
        pass
       
    # Return to PTVL Settings
    REAL_SETTINGS.openSettings()
        
        
if sys.argv[1] == '-DDautopatch':
    DDautopatch()   
elif sys.argv[1] == '-DonorDownloader':
    if xbmcgui.Window(10000).getProperty("PseudoTVRunning") != "True":
        DonorDownloader()  
    else:
        xbmc.executebuiltin("Notification( %s, %s, %d, %s)" % ("PseudoTV Live", "Not available while running.", 1000, THUMB) )
elif sys.argv[1] == '-LogoDownloader':
    LogoDownloader()
elif sys.argv[1] == '-SimpleDownloader':
    xbmcaddon.Addon(id='script.module.simple.downloader').openSettings()
elif sys.argv[1] == '-showChangelog':
    showChangelog(ADDON_ID)
