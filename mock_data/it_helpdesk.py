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
    "laptop02": {"status": "Warning", "details": "Low disk space: 5% remaining.", "location": "Floor 1, Desk 8"}
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
