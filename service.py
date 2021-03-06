﻿
import os, shutil, datetime, time, random
import xbmc, xbmcgui, xbmcaddon, xbmcvfs

from time import sleep
from resources.lib.utils import *

# Plugin Info
ADDON_ID = 'script.pseudotv.live'
REAL_SETTINGS = xbmcaddon.Addon(id=ADDON_ID)
ADDON_ID = REAL_SETTINGS.getAddonInfo('id')
ADDON_NAME = REAL_SETTINGS.getAddonInfo('name')
ADDON_PATH = REAL_SETTINGS.getAddonInfo('path')
ADDON_VERSION = REAL_SETTINGS.getAddonInfo('version')
THUMB = (xbmc.translatePath(os.path.join(ADDON_PATH, 'resources', 'images')) + '/' + 'icon.png')

def HubSwap(): # Swap Org/Hub versions if 'Hub Installer' found.
    icon = ADDON_PATH + '/icon'
    HUB = xbmc.getCondVisibility('System.HasAddon(plugin.program.addoninstaller)') == 1
    
    if HUB == True:
        xbmc.log('script.pseudotv.live-Service: HubSwap = Hub Edition')
        if REAL_SETTINGS.getSetting('Hub') == 'false':
            xbmc.executebuiltin("Notification( %s, %s, %d, %s)" % ("PseudoTV Live","Hub-Edition Activated", 4000, THUMB) )
            REAL_SETTINGS.setSetting("Hub","true")
    else:
        xbmc.log('script.pseudotv.live-Service: HubSwap = Master')
        REAL_SETTINGS.setSetting("Hub","false")
    return
          
          
def donorCHK():
    DonorPath = (os.path.join(ADDON_PATH, 'resources', 'lib', 'Donor.pyo'))
    DL_DonorPath = (os.path.join(ADDON_PATH, 'resources', 'lib', 'Donor.py'))
    
    if xbmcvfs.exists(DonorPath) or xbmcvfs.exists(DL_DonorPath):
        xbmc.log('script.pseudotv.live-Service: donorCHK = Donor')  
        REAL_SETTINGS.setSetting("AT_Donor", "true")
        REAL_SETTINGS.setSetting("COM_Donor", "true")
        REAL_SETTINGS.setSetting("TRL_Donor", "true")
        REAL_SETTINGS.setSetting("CAT_Donor", "true")
        # REAL_SETTINGS.setSetting("autoFindCommunity_Source", "1")  
    else:
        xbmc.log('script.pseudotv.live-Service: donorCHK = FreeUser')  
        REAL_SETTINGS.setSetting("AT_Donor", "false")
        REAL_SETTINGS.setSetting("COM_Donor", "false")
        REAL_SETTINGS.setSetting("TRL_Donor", "false")
        REAL_SETTINGS.setSetting("CAT_Donor", "false")
        # REAL_SETTINGS.setSetting("autoFindCommunity_Source", "0")
    return
        
        
def service():
    xbmc.log('script.pseudotv.live-Service: Init')
    try:
        while (not xbmc.abortRequested):
            if xbmcgui.Window(10000).getProperty("PseudoTVRunning") != "True":
                xbmc.log("script.pseudotv.live-Service: Started")
                donorCHK()
                HubSwap()
                
                if REAL_SETTINGS.getSetting("SyncXMLTV_Enabled") == "true":
                    SyncXMLTV()

                if REAL_SETTINGS.getSetting("Auto_Start") == "true" and xbmcgui.Window(10000).getProperty("PseudoTVautostart") != "True":
                    xbmcgui.Window(10000).setProperty("PseudoTVautostart", "True")
                    autostart()
                
            xbmc.log('script.pseudotv.live-Service: Idle')
            xbmc.sleep(100000)
    except:
        pass
        

def autostart():
    xbmc.log('script.pseudotv.live-Service: autostart')   
    xbmc.executebuiltin("Notification( %s, %s, %d, %s)" % ("AutoStart PseudoTV Live","Service Starting...", 4000, THUMB) )
    AUTOSTART_TIMER = [0,5,10,15,20]#in seconds
    IDLE_TIME = AUTOSTART_TIMER[int(REAL_SETTINGS.getSetting('timer_amount'))] 
    sleep(IDLE_TIME)
    xbmc.executebuiltin('RunScript("' + ADDON_PATH + '/default.py' + '")')
    return
    
service()