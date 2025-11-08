"""IT Helpdesk mock data for RAG chatbot system."""

from typing import List, Dict, Any

# IT Helpdesk FAQ Documents
IT_HELPDESK_DOCS = [
    {
        "page_content": "How to reset my password? Visit the password reset page at portal.company.com/reset, enter your username or email, and follow the instructions sent to your email. If you don't receive the email, check your spam folder and contact IT support.",
        "metadata": {"source": "FAQ - Password Reset", "category": "Authentication", "priority": "high"}
    },
    {
        "page_content": "My computer is slow. First, restart your computer to clear temporary files and refresh memory. Close unused applications and browser tabs. Run a full antivirus scan to check for malware. Clear browser cache and temporary files. If the issue persists, check available storage space - aim for at least 15% free space.",
        "metadata": {"source": "FAQ - Performance Issues", "category": "Hardware", "priority": "medium"}
    },
    {
        "page_content": "To connect to company VPN, download and install the VPN client from the IT portal at portal.company.com/vpn. Use your domain credentials (username@company.com) to login. If you're working remotely, ensure your internet connection is stable. For connection issues, try different server locations or contact IT support.",
        "metadata": {"source": "FAQ - VPN Setup", "category": "Network", "priority": "high"}
    },
    {
        "page_content": "Printer not working? First, check if the printer is powered on and all cables are securely connected. Verify there's paper in the tray and sufficient ink/toner. Check the printer queue for stuck jobs and clear if necessary. Try printing a test page. If wireless, ensure printer is connected to the correct network.",
        "metadata": {"source": "FAQ - Printer Troubleshooting", "category": "Hardware", "priority": "medium"}
    },
    {
        "page_content": "Email not syncing on mobile device? Ensure you're connected to Wi-Fi or cellular data. Check email settings - use IMAP server: mail.company.com, port 993, SSL enabled. For Exchange, use autodiscover or server: exchange.company.com. Verify username format is correct (usually email address).",
        "metadata": {"source": "FAQ - Email Mobile Setup", "category": "Email", "priority": "medium"}
    },
    {
        "page_content": "Can't access shared network drives? Verify you're connected to company network or VPN. Check if your account has proper permissions. Try accessing via UNC path \\\\server\\sharename. Clear cached credentials in Windows Credential Manager if needed. Contact your manager if you need access to specific folders.",
        "metadata": {"source": "FAQ - Network Drive Access", "category": "Network", "priority": "medium"}
    },
    {
        "page_content": "Software installation requests must be submitted through the IT Service Portal. Include software name, version, business justification, and department approval. IT will review for security compliance and licensing. Installation typically takes 2-3 business days after approval.",
        "metadata": {"source": "FAQ - Software Installation", "category": "Software", "priority": "low"}
    },
    {
        "page_content": "Blue screen errors (BSOD) indicate serious system issues. Note the error code if possible. Restart the computer and check if the issue persists. Run Windows Memory Diagnostic tool. Update device drivers, especially graphics and network adapters. If frequent BSODs occur, contact IT immediately for hardware diagnostics.",
        "metadata": {"source": "FAQ - Blue Screen Errors", "category": "Hardware", "priority": "high"}
    },
    {
        "page_content": "Wi-Fi connection problems? Forget and reconnect to the network. Check if other devices can connect to the same network. Restart your network adapter in Device Manager. Update Wi-Fi drivers. For corporate networks, ensure you're using the correct authentication method (usually WPA2-Enterprise with domain credentials).",
        "metadata": {"source": "FAQ - WiFi Issues", "category": "Network", "priority": "medium"}
    },
    {
        "page_content": "Laptop battery draining quickly? Check battery health in system settings. Close power-hungry applications and reduce screen brightness. Disable unnecessary startup programs. Use power saving mode when on battery. If battery health is below 80%, request a replacement through IT portal.",
        "metadata": {"source": "FAQ - Battery Issues", "category": "Hardware", "priority": "low"}
    },
    {
        "page_content": "How to enable two-factor authentication (2FA)? Go to portal.company.com/security, navigate to Security Settings, click Enable 2FA, scan the QR code with your authenticator app (Google Authenticator, Microsoft Authenticator, or Authy), enter the verification code, and save your backup codes. 2FA is mandatory for all employees accessing sensitive systems.",
        "metadata": {"source": "FAQ - Two-Factor Authentication", "category": "Security", "priority": "high", "ticket_id": "SEC-2024-001", "difficulty": "medium", "resolution_time": "10 minutes", "affected_systems": ["Portal", "Email", "VPN"], "tags": ["security", "authentication", "2fa"]}
    },
    {
        "page_content": "Outlook not receiving emails? Check if Outlook is in offline mode (File > Account Settings > Account Settings > select account > More Settings > Advanced tab). Verify Send/Receive settings are enabled. Check Junk Email folder. Restart Outlook in safe mode (outlook.exe /safe). If issue persists, recreate Outlook profile or contact IT support.",
        "metadata": {"source": "FAQ - Outlook Email Issues", "category": "Email", "priority": "high", "ticket_id": "EMAIL-2024-015", "difficulty": "medium", "resolution_time": "15-30 minutes", "affected_systems": ["Outlook", "Exchange Server"], "related_software": ["Microsoft Office"], "tags": ["email", "outlook", "sync"]}
    },
    {
        "page_content": "Cannot access SharePoint sites? Verify you have proper permissions assigned by site owner. Clear browser cache and cookies. Try accessing in incognito/private mode. Check if site URL is correct. Ensure you're logged in with correct domain account. If using VPN, ensure VPN connection is active. Contact site administrator if access is still denied.",
        "metadata": {"source": "FAQ - SharePoint Access", "category": "Collaboration", "priority": "medium", "ticket_id": "SP-2024-008", "difficulty": "low", "resolution_time": "5-10 minutes", "affected_systems": ["SharePoint Online", "Office 365"], "tags": ["sharepoint", "access", "permissions"]}
    },
    {
        "page_content": "Webcam not working in Teams/Zoom? Check if webcam is enabled in device settings (Settings > Privacy > Camera). Ensure no other application is using the webcam. Test webcam in Windows Camera app first. Update webcam drivers from manufacturer website. Check Teams/Zoom camera settings and permissions. Restart the application. If hardware issue, contact IT for replacement.",
        "metadata": {"source": "FAQ - Webcam Issues", "category": "Hardware", "priority": "medium", "ticket_id": "HW-2024-022", "difficulty": "low", "resolution_time": "10-15 minutes", "affected_systems": ["Microsoft Teams", "Zoom", "Windows"], "related_devices": ["laptop01", "laptop02", "workstation01"], "tags": ["webcam", "video", "teams", "zoom"]}
    },
    {
        "page_content": "How to request access to a network folder? Submit access request through IT Service Portal (portal.company.com/requests). Include folder path (\\\\server\\sharename), business justification, manager approval, and required access level (Read, Write, or Full). IT will process within 2 business days. For urgent requests, contact IT support directly with ticket number.",
        "metadata": {"source": "FAQ - Network Folder Access", "category": "Network", "priority": "medium", "ticket_id": "NET-2024-012", "difficulty": "low", "resolution_time": "2 business days", "affected_systems": ["File Server", "Active Directory"], "tags": ["network", "permissions", "file access"]}
    },
    {
        "page_content": "Microsoft Teams audio not working? Check system audio settings and volume levels. Ensure correct audio device is selected in Teams (Settings > Devices). Test audio in Windows Sound settings. Restart Teams application. Check if audio drivers are up to date. Try joining meeting with phone audio as backup. If issue persists, reinstall Teams or contact IT support.",
        "metadata": {"source": "FAQ - Teams Audio Issues", "category": "Collaboration", "priority": "high", "ticket_id": "TEAMS-2024-019", "difficulty": "medium", "resolution_time": "15-20 minutes", "affected_systems": ["Microsoft Teams", "Windows Audio"], "related_software": ["Microsoft Teams"], "tags": ["teams", "audio", "meetings"]}
    },
    {
        "page_content": "How to install approved software? Log into IT Service Portal, navigate to Software Catalog, search for desired software, click Request Installation, fill in business justification, and submit. For pre-approved software (Office, Adobe Reader, etc.), installation is automatic. For restricted software, manager approval required. Installation typically completes within 24 hours.",
        "metadata": {"source": "FAQ - Software Installation Process", "category": "Software", "priority": "low", "ticket_id": "SW-2024-005", "difficulty": "low", "resolution_time": "24 hours", "affected_systems": ["IT Service Portal", "Software Deployment"], "tags": ["software", "installation", "approval"]}
    },
    {
        "page_content": "External monitor not detected? Check cable connections (HDMI, DisplayPort, USB-C). Try different cable or port. Press Windows + P to cycle display modes (PC screen only, Duplicate, Extend, Second screen only). Update graphics drivers. Check if monitor is powered on. Test monitor with different device. If laptop, ensure external display is enabled in BIOS settings.",
        "metadata": {"source": "FAQ - External Monitor Issues", "category": "Hardware", "priority": "medium", "ticket_id": "HW-2024-014", "difficulty": "low", "resolution_time": "10 minutes", "affected_systems": ["Windows Display", "Graphics Drivers"], "related_devices": ["laptop01", "laptop02", "workstation01"], "tags": ["monitor", "display", "external"]}
    },
    {
        "page_content": "How to backup files to OneDrive? OneDrive syncs automatically when files are saved in OneDrive folder. To manually sync, right-click OneDrive icon in system tray > Sync now. Check sync status in OneDrive settings. Ensure you have sufficient OneDrive storage (check quota in portal). Files in Desktop, Documents, and Pictures folders can be automatically backed up if enabled in OneDrive settings.",
        "metadata": {"source": "FAQ - OneDrive Backup", "category": "Cloud Storage", "priority": "medium", "ticket_id": "CLOUD-2024-007", "difficulty": "low", "resolution_time": "5 minutes", "affected_systems": ["OneDrive", "Office 365"], "tags": ["onedrive", "backup", "sync", "cloud"]}
    },
    {
        "page_content": "Keyboard or mouse not responding? Unplug and reconnect USB device. Try different USB port. Test device on another computer to rule out hardware failure. Check Device Manager for driver issues (yellow exclamation mark). Update or reinstall device drivers. For wireless devices, check battery levels and reconnect receiver. If Bluetooth, remove and re-pair device.",
        "metadata": {"source": "FAQ - Input Device Issues", "category": "Hardware", "priority": "medium", "ticket_id": "HW-2024-011", "difficulty": "low", "resolution_time": "5-10 minutes", "affected_systems": ["Windows", "USB Drivers"], "related_devices": ["workstation01", "workstation02"], "tags": ["keyboard", "mouse", "usb", "input"]}
    },
    {
        "page_content": "How to report a security incident? Immediately contact IT Security at security@company.com or call IT Security hotline (ext. 9111). Do not forward suspicious emails. Do not click suspicious links. Preserve evidence (screenshot, email headers). Report phishing attempts, malware detections, unauthorized access, or data breaches. IT Security will investigate and provide guidance.",
        "metadata": {"source": "FAQ - Security Incident Reporting", "category": "Security", "priority": "critical", "ticket_id": "SEC-2024-URGENT", "difficulty": "low", "resolution_time": "Immediate response", "affected_systems": ["All Systems"], "tags": ["security", "incident", "phishing", "malware", "urgent"]}
    },
    {
        "page_content": "Cannot connect to WiFi? Ensure WiFi is enabled (check function key or settings). Forget and reconnect to network (Settings > Network > WiFi > Manage known networks > Forget). Restart network adapter (Device Manager > Network adapters > right-click > Disable, then Enable). Update WiFi drivers. Check if other devices can connect. For corporate WiFi, ensure using WPA2-Enterprise with domain credentials.",
        "metadata": {"source": "FAQ - WiFi Connection Problems", "category": "Network", "priority": "high", "ticket_id": "NET-2024-018", "difficulty": "medium", "resolution_time": "15 minutes", "affected_systems": ["WiFi Network", "Network Adapter"], "related_devices": ["laptop01", "laptop02"], "tags": ["wifi", "network", "wireless", "connection"]}
    },
    {
        "page_content": "How to access company email on mobile? For iOS: Settings > Mail > Accounts > Add Account > Exchange, enter email and password, server: exchange.company.com. For Android: Settings > Accounts > Add Account > Exchange, enter credentials. Use Outlook mobile app for better experience. Enable remote wipe capability. Contact IT if you need help with setup or encounter sync issues.",
        "metadata": {"source": "FAQ - Mobile Email Setup", "category": "Email", "priority": "medium", "ticket_id": "EMAIL-2024-009", "difficulty": "low", "resolution_time": "10 minutes", "affected_systems": ["Exchange Server", "Mobile Devices"], "tags": ["email", "mobile", "ios", "android", "outlook"]}
    },
    {
        "page_content": "Computer freezing or crashing frequently? Check Task Manager for high CPU or memory usage processes. Run Windows Memory Diagnostic (Windows + R > mdsched.exe). Update all device drivers, especially graphics and chipset. Check Windows Event Viewer for error logs. Run System File Checker (sfc /scannow in Command Prompt as admin). If issue persists, may indicate hardware failure - contact IT for diagnostics.",
        "metadata": {"source": "FAQ - System Freezing", "category": "Hardware", "priority": "high", "ticket_id": "HW-2024-025", "difficulty": "high", "resolution_time": "1-2 hours", "affected_systems": ["Windows OS", "Hardware Components"], "related_devices": ["workstation01", "workstation02", "laptop01"], "tags": ["freezing", "crash", "performance", "hardware"]}
    }
]

# Device Status Mock Database
DEVICE_STATUS_DB = {
    "printer01": {"status": "Online", "details": "Functioning normally. Toner at 75%.", "location": "Floor 3, Room 301"},
    "printer02": {"status": "Offline", "details": "Paper jam detected. Requires maintenance.", "location": "Floor 2, Room 205"},
    "server01": {"status": "Online", "details": "Running normally. CPU usage: 45%.", "location": "Data Center"},
    "server02": {"status": "Warning", "details": "High CPU usage: 89%. Memory: 78%.", "location": "Data Center"},
    "router01": {"status": "Offline", "details": "Network unreachable. Requires restart.", "location": "Network Closet A"},
    "router02": {"status": "Online", "details": "Operating normally. 124 active connections.", "location": "Network Closet B"},
    "workstation01": {"status": "Online", "details": "User logged in. Last update: 2 days ago.", "location": "Floor 1, Desk 15"},
    "workstation02": {"status": "Offline", "details": "Powered off or hibernating.", "location": "Floor 2, Desk 23"},
    "laptop01": {"status": "Online", "details": "VPN connected. Battery: 67%.", "location": "Remote"},
    "laptop02": {"status": "Warning", "details": "Low disk space: 5% remaining.", "location": "Floor 1, Desk 8"},
    "printer03": {"status": "Online", "details": "Functioning normally. Toner at 45%. Paper tray 80% full.", "location": "Floor 4, Room 401", "device_type": "Laser Printer", "model": "HP LaserJet Pro M404dn", "ip_address": "192.168.1.103", "last_maintenance": "2024-01-15", "next_maintenance": "2024-04-15"},
    "printer04": {"status": "Online", "details": "Functioning normally. Toner at 90%. All systems operational.", "location": "Floor 1, Reception", "device_type": "Multifunction Printer", "model": "Canon imageRUNNER ADVANCE C5535i", "ip_address": "192.168.1.104", "last_maintenance": "2024-02-01", "next_maintenance": "2024-05-01"},
    "server03": {"status": "Online", "details": "Running normally. CPU: 32%, Memory: 58%, Disk: 45% used.", "location": "Data Center Rack 5", "device_type": "Application Server", "model": "Dell PowerEdge R740", "ip_address": "10.0.1.33", "os": "Windows Server 2022", "uptime_days": 45},
    "server04": {"status": "Online", "details": "Running normally. CPU: 28%, Memory: 52%, Disk: 38% used.", "location": "Data Center Rack 3", "device_type": "Database Server", "model": "Dell PowerEdge R750", "ip_address": "10.0.1.34", "os": "Windows Server 2022", "uptime_days": 62},
    "switch01": {"status": "Online", "details": "Operating normally. 48 ports active, 12 ports available.", "location": "Network Closet A", "device_type": "Network Switch", "model": "Cisco Catalyst 2960-X", "ip_address": "192.168.1.201", "ports_total": 48, "ports_active": 36},
    "switch02": {"status": "Online", "details": "Operating normally. 24 ports active, 8 ports available.", "location": "Network Closet B", "device_type": "Network Switch", "model": "Cisco Catalyst 2960-X", "ip_address": "192.168.1.202", "ports_total": 32, "ports_active": 24},
    "firewall01": {"status": "Online", "details": "All security policies active. No threats detected. Throughput: 850 Mbps.", "location": "Network Closet A", "device_type": "Firewall", "model": "Fortinet FortiGate 100F", "ip_address": "192.168.1.1", "threats_blocked_today": 1247},
    "backup_server01": {"status": "Online", "details": "Last backup completed successfully at 02:00 AM. Storage: 8.2 TB used of 20 TB.", "location": "Data Center Rack 7", "device_type": "Backup Server", "model": "Dell PowerEdge R740xd", "ip_address": "10.0.1.50", "last_backup": "2024-01-20 02:00:00", "backup_schedule": "Daily at 2:00 AM"},
    "workstation03": {"status": "Online", "details": "User logged in. Windows 11 Pro. Last update: 1 day ago. Antivirus: Up to date.", "location": "Floor 2, Desk 31", "device_type": "Desktop", "model": "Dell OptiPlex 7090", "ip_address": "192.168.1.131", "os": "Windows 11 Pro", "user": "john.doe@company.com"},
    "workstation04": {"status": "Online", "details": "User logged in. Windows 11 Pro. Last update: 3 days ago. Antivirus: Up to date.", "location": "Floor 3, Desk 42", "device_type": "Desktop", "model": "HP EliteDesk 800 G8", "ip_address": "192.168.1.132", "os": "Windows 11 Pro", "user": "jane.smith@company.com"},
    "laptop03": {"status": "Online", "details": "VPN connected. Battery: 89%. Last sync: 5 minutes ago.", "location": "Remote", "device_type": "Laptop", "model": "Dell Latitude 7420", "ip_address": "10.0.2.45", "os": "Windows 11 Pro", "user": "mike.johnson@company.com", "vpn_status": "Connected"},
    "laptop04": {"status": "Warning", "details": "Battery health: 72%. Consider replacement. Last update: 2 days ago.", "location": "Floor 1, Desk 12", "device_type": "Laptop", "model": "Lenovo ThinkPad X1 Carbon", "ip_address": "192.168.1.134", "os": "Windows 11 Pro", "user": "sarah.williams@company.com", "battery_health": "72%"},
    "access_point01": {"status": "Online", "details": "Operating normally. 45 devices connected. Signal strength: Excellent.", "location": "Floor 2, Ceiling", "device_type": "WiFi Access Point", "model": "Cisco Aironet 2800", "ip_address": "192.168.1.251", "connected_devices": 45, "signal_strength": "Excellent"},
    "access_point02": {"status": "Online", "details": "Operating normally. 38 devices connected. Signal strength: Good.", "location": "Floor 3, Ceiling", "device_type": "WiFi Access Point", "model": "Cisco Aironet 2800", "ip_address": "192.168.1.252", "connected_devices": 38, "signal_strength": "Good"},
    "nas01": {"status": "Online", "details": "All volumes healthy. Storage: 12.5 TB used of 24 TB. RAID status: Normal.", "location": "Data Center Rack 6", "device_type": "Network Attached Storage", "model": "Synology DS1821+", "ip_address": "10.0.1.60", "storage_used": "12.5 TB", "storage_total": "24 TB", "raid_status": "Normal"}
}

# Software Catalog
SOFTWARE_CATALOG = {
    "microsoft_office": {
        "name": "Microsoft Office 365",
        "version": "2023",
        "license_type": "Corporate",
        "approval_required": False,
        "install_time": "30 minutes"
    },
    "adobe_reader": {
        "name": "Adobe Acrobat Reader",
        "version": "2023.008.20470",
        "license_type": "Free",
        "approval_required": False,
        "install_time": "10 minutes"
    },
    "visual_studio": {
        "name": "Visual Studio Professional",
        "version": "2022",
        "license_type": "Corporate",
        "approval_required": True,
        "install_time": "60 minutes"
    },
    "slack": {
        "name": "Slack Desktop",
        "version": "4.35.0",
        "license_type": "Corporate",
        "approval_required": False,
        "install_time": "15 minutes"
    },
    "zoom": {
        "name": "Zoom Client for Meetings",
        "version": "5.17.0",
        "license_type": "Corporate",
        "approval_required": False,
        "install_time": "10 minutes",
        "category": "Communication",
        "vendor": "Zoom Video Communications",
        "support_url": "https://support.zoom.us",
        "minimum_os": "Windows 10 / macOS 10.13"
    },
    "chrome": {
        "name": "Google Chrome",
        "version": "120.0.6099.109",
        "license_type": "Free",
        "approval_required": False,
        "install_time": "5 minutes",
        "category": "Web Browser",
        "vendor": "Google",
        "auto_updates": True,
        "minimum_os": "Windows 10 / macOS 10.15"
    },
    "firefox": {
        "name": "Mozilla Firefox",
        "version": "121.0",
        "license_type": "Free",
        "approval_required": False,
        "install_time": "5 minutes",
        "category": "Web Browser",
        "vendor": "Mozilla",
        "auto_updates": True,
        "minimum_os": "Windows 10 / macOS 10.15"
    },
    "vscode": {
        "name": "Visual Studio Code",
        "version": "1.85.0",
        "license_type": "Free",
        "approval_required": False,
        "install_time": "10 minutes",
        "category": "Development",
        "vendor": "Microsoft",
        "auto_updates": True,
        "minimum_os": "Windows 10 / macOS 10.15 / Linux"
    },
    "git": {
        "name": "Git for Windows",
        "version": "2.43.0",
        "license_type": "Free",
        "approval_required": False,
        "install_time": "5 minutes",
        "category": "Development",
        "vendor": "Git",
        "auto_updates": False,
        "minimum_os": "Windows 10"
    },
    "python": {
        "name": "Python",
        "version": "3.11.5",
        "license_type": "Free",
        "approval_required": True,
        "install_time": "15 minutes",
        "category": "Development",
        "vendor": "Python Software Foundation",
        "auto_updates": False,
        "minimum_os": "Windows 10 / macOS 10.15 / Linux",
        "business_justification_required": True
    },
    "nodejs": {
        "name": "Node.js",
        "version": "20.10.0",
        "license_type": "Free",
        "approval_required": True,
        "install_time": "10 minutes",
        "category": "Development",
        "vendor": "Node.js Foundation",
        "auto_updates": False,
        "minimum_os": "Windows 10 / macOS 10.15 / Linux",
        "business_justification_required": True
    },
    "docker": {
        "name": "Docker Desktop",
        "version": "4.25.0",
        "license_type": "Corporate",
        "approval_required": True,
        "install_time": "20 minutes",
        "category": "Development",
        "vendor": "Docker Inc.",
        "auto_updates": True,
        "minimum_os": "Windows 10 / macOS 10.15",
        "business_justification_required": True,
        "requires_virtualization": True
    },
    "postman": {
        "name": "Postman",
        "version": "10.20.0",
        "license_type": "Corporate",
        "approval_required": False,
        "install_time": "10 minutes",
        "category": "Development",
        "vendor": "Postman Inc.",
        "auto_updates": True,
        "minimum_os": "Windows 10 / macOS 10.15 / Linux"
    },
    "7zip": {
        "name": "7-Zip",
        "version": "23.01",
        "license_type": "Free",
        "approval_required": False,
        "install_time": "5 minutes",
        "category": "Utilities",
        "vendor": "Igor Pavlov",
        "auto_updates": False,
        "minimum_os": "Windows 10"
    },
    "winrar": {
        "name": "WinRAR",
        "version": "6.24",
        "license_type": "Corporate",
        "approval_required": False,
        "install_time": "5 minutes",
        "category": "Utilities",
        "vendor": "RARLAB",
        "auto_updates": False,
        "minimum_os": "Windows 10"
    },
    "notepad_plus_plus": {
        "name": "Notepad++",
        "version": "8.6.0",
        "license_type": "Free",
        "approval_required": False,
        "install_time": "5 minutes",
        "category": "Text Editor",
        "vendor": "Don Ho",
        "auto_updates": True,
        "minimum_os": "Windows 10"
    }
}

# Common IT Issues with Solutions
COMMON_ISSUES = [
    {
        "keywords": ["slow", "performance", "lag", "freeze"],
        "category": "Performance",
        "solution": "Try restarting your computer, closing unnecessary applications, and running a disk cleanup."
    },
    {
        "keywords": ["password", "login", "access", "authenticate"],
        "category": "Authentication",
        "solution": "Use the password reset portal or contact IT support for account unlocking."
    },
    {
        "keywords": ["printer", "print", "printing", "paper jam"],
        "category": "Printing",
        "solution": "Check printer power, paper, ink levels, and clear any paper jams."
    },
    {
        "keywords": ["network", "internet", "wifi", "connection"],
        "category": "Network",
        "solution": "Check network cables, restart network adapters, or try connecting to a different network."
    },
    {
        "keywords": ["email", "outlook", "mail", "sync"],
        "category": "Email",
        "solution": "Restart Outlook, check internet connection, or reconfigure email settings."
    },
    {
        "keywords": ["2fa", "two-factor", "authentication", "mfa"],
        "category": "Security",
        "solution": "Enable 2FA through portal.company.com/security. Use authenticator app (Google Authenticator, Microsoft Authenticator) to scan QR code and verify setup."
    },
    {
        "keywords": ["sharepoint", "share", "site", "access"],
        "category": "Collaboration",
        "solution": "Verify permissions with site owner. Clear browser cache. Try incognito mode. Ensure VPN is connected if working remotely."
    },
    {
        "keywords": ["webcam", "camera", "video", "not working"],
        "category": "Hardware",
        "solution": "Check camera privacy settings (Settings > Privacy > Camera). Ensure no other app is using camera. Test in Windows Camera app. Update webcam drivers."
    },
    {
        "keywords": ["teams", "audio", "microphone", "sound"],
        "category": "Collaboration",
        "solution": "Check system audio settings. Select correct audio device in Teams (Settings > Devices). Test audio in Windows Sound settings. Restart Teams application."
    },
    {
        "keywords": ["monitor", "display", "external", "screen"],
        "category": "Hardware",
        "solution": "Check cable connections. Press Windows + P to cycle display modes. Update graphics drivers. Test monitor with different device."
    },
    {
        "keywords": ["onedrive", "backup", "sync", "cloud"],
        "category": "Cloud Storage",
        "solution": "OneDrive syncs automatically. Right-click OneDrive icon > Sync now. Check sync status in OneDrive settings. Ensure sufficient storage quota."
    },
    {
        "keywords": ["keyboard", "mouse", "not working", "usb"],
        "category": "Hardware",
        "solution": "Unplug and reconnect USB device. Try different USB port. Test on another computer. Check Device Manager for driver issues. Update device drivers."
    },
    {
        "keywords": ["security", "phishing", "malware", "incident"],
        "category": "Security",
        "solution": "Immediately contact IT Security at security@company.com or ext. 9111. Do not click suspicious links. Preserve evidence (screenshot). Report all security incidents."
    },
    {
        "keywords": ["mobile", "phone", "email", "ios", "android"],
        "category": "Email",
        "solution": "Configure Exchange account in device settings. Server: exchange.company.com. Use Outlook mobile app for better experience. Contact IT for setup assistance."
    },
    {
        "keywords": ["freezing", "crash", "blue screen", "bsod"],
        "category": "Hardware",
        "solution": "Check Task Manager for high resource usage. Run Windows Memory Diagnostic. Update device drivers. Run System File Checker (sfc /scannow). Contact IT if issue persists."
    },
    {
        "keywords": ["software", "install", "application", "program"],
        "category": "Software",
        "solution": "Request through IT Service Portal. Include software name, version, business justification. Pre-approved software installs automatically. Restricted software requires manager approval."
    },
    {
        "keywords": ["folder", "network", "drive", "permissions"],
        "category": "Network",
        "solution": "Submit access request through IT Service Portal with folder path, business justification, and manager approval. IT processes within 2 business days."
    }
]

def get_it_helpdesk_data() -> List[Dict[str, Any]]:
    """Get all IT helpdesk documents."""
    return IT_HELPDESK_DOCS

def get_device_status(device_id: str) -> Dict[str, str]:
    """Get device status by device ID."""
    return DEVICE_STATUS_DB.get(device_id, {
        "status": "Unknown",
        "details": "Device not found in system.",
        "location": "Unknown"
    })

def get_software_info(software_name: str) -> Dict[str, Any]:
    """Get software information by name."""
    return SOFTWARE_CATALOG.get(software_name.lower().replace(" ", "_"), {
        "name": "Software not found",
        "status": "Not available in catalog"
    })

def search_solutions(keywords: List[str]) -> List[Dict[str, str]]:
    """Search for solutions based on keywords."""
    solutions = []
    for issue in COMMON_ISSUES:
        if any(keyword.lower() in " ".join(issue["keywords"]) for keyword in keywords):
            solutions.append({
                "category": issue["category"],
                "solution": issue["solution"]
            })
    return solutions
