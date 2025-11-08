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
        "page_content": "How to configure proxy settings on Windows: Go to Settings > Network & Internet > Proxy. For automatic proxy, enable 'Automatically detect settings'. For manual proxy, enable 'Use a proxy server', enter proxy address (e.g., proxy.company.com) and port (e.g., 8080). For authentication, enter username and password. Click 'Save'. Restart browser to apply changes. If proxy is not working, check firewall settings and ensure proxy server is accessible.",
        "metadata": {"source": "IT Helpdesk - Proxy Configuration Windows", "category": "Proxy", "priority": "high"}
    },
    {
        "page_content": "How to configure proxy settings on macOS: Go to System Preferences > Network > Advanced > Proxies. Select protocol (HTTP, HTTPS, SOCKS). For HTTP/HTTPS proxy, enter proxy server address and port. Check 'Proxy server requires password' if authentication is needed. Click 'OK' and 'Apply'. Restart applications to apply changes. If connection fails, verify proxy credentials and check if proxy server is running.",
        "metadata": {"source": "IT Helpdesk - Proxy Configuration macOS", "category": "Proxy", "priority": "high"}
    },
    {
        "page_content": "Proxy authentication errors and solutions: Error '407 Proxy Authentication Required' means credentials are missing or incorrect. Verify username and password in proxy settings. Check if account is locked or expired. Contact IT to reset proxy credentials. Error '502 Bad Gateway' indicates proxy server is down or unreachable. Check network connectivity, ping proxy server, verify firewall rules allow proxy traffic. Temporarily disable proxy to test direct connection.",
        "metadata": {"source": "IT Helpdesk - Proxy Authentication Issues", "category": "Proxy", "priority": "high"}
    },
    {
        "page_content": "Proxy connection timeout troubleshooting: If proxy connection times out, check network cable and WiFi connection. Ping proxy server to test connectivity (ping proxy.company.com). Verify proxy server address and port are correct. Check if proxy is required for your network (some networks only need proxy for external sites). Test with different proxy protocol (HTTP vs HTTPS). Clear browser cache and cookies. Restart network adapter or reboot computer. Contact IT if proxy server is down.",
        "metadata": {"source": "IT Helpdesk - Proxy Timeout Issues", "category": "Proxy", "priority": "medium"}
    },
    {
        "page_content": "How to check if a domain is blocked: If you cannot access a website, first verify the URL is correct. Try accessing from different browser or incognito mode. Check company firewall or content filter settings. Use command 'nslookup domain.com' to verify DNS resolution. Try accessing from mobile hotspot to test if it's network-wide blocking. Check browser console for error messages (F12). Contact IT helpdesk with domain name and error message for whitelist request.",
        "metadata": {"source": "IT Helpdesk - Domain Blocking Check", "category": "Domain Blocking", "priority": "high"}
    },
    {
        "page_content": "How to request domain whitelist: If a legitimate business website is blocked, submit whitelist request to IT helpdesk. Include business justification, domain name, and reason for access. Common reasons include accessing work-related tools, client websites, or required services. IT will review request within 24 hours. For urgent requests, call IT helpdesk directly. Approved domains are typically whitelisted within 1 business day. Check firewall rules if domain is still blocked after approval.",
        "metadata": {"source": "IT Helpdesk - Domain Whitelist Request", "category": "Domain Blocking", "priority": "medium"}
    },
    {
        "page_content": "Domain blocked by firewall - troubleshooting steps: Error 'This site can't be reached' or 'Connection refused' may indicate firewall blocking. Check if domain is in blocked category (gaming, social media, etc.). Verify you're on correct network (corporate vs guest WiFi). Try accessing from different device to isolate issue. Clear DNS cache: Windows (ipconfig /flushdns), macOS (sudo dscacheutil -flushcache), Linux (sudo systemd-resolve --flush-caches). Use alternative DNS servers (8.8.8.8 or 1.1.1.1) to test. Contact IT if domain should be accessible.",
        "metadata": {"source": "IT Helpdesk - Firewall Domain Blocking", "category": "Domain Blocking", "priority": "high"}
    },
    {
        "page_content": "Legacy domains blocked by proxy - solution options: Legacy domains (old internal systems, deprecated URLs, historical applications) are often blocked by corporate proxy for security reasons. You have three solution options. Option 1 - Add URL to proxy exceptions: Configure proxy to bypass specific legacy domains. Windows: Settings > Network & Internet > Proxy > Advanced settings > Add URLs to 'Don't use proxy server for these addresses' (use wildcards like *.legacy-domain.com). macOS: System Preferences > Network > Advanced > Proxies > Bypass proxy settings for these hosts. Option 2 - Disable proxy and use VPN: Turn off proxy settings completely, then connect to GlobalProtect VPN or company VPN. VPN routes traffic directly, bypassing proxy restrictions. Option 3 - Request proxy whitelist: Submit request to IT helpdesk to whitelist legacy domain in corporate proxy policy. Include business justification and domain URLs. Try Option 1 first as it's fastest for individual use.",
        "metadata": {"source": "IT Helpdesk - Legacy Domain Proxy Blocking", "category": "Domain Blocking", "priority": "high"}
    },
    {
        "page_content": "How to add URLs to proxy exceptions on Windows: To allow specific legacy domains to bypass proxy, add them to proxy exception list. Steps: 1) Open Settings > Network & Internet > Proxy. 2) Scroll down to 'Manual proxy setup' section. 3) Click 'Edit' or 'Use a proxy server' to enable manual proxy. 4) Click 'Advanced' button. 5) In 'Exceptions' or 'Don't use proxy server for addresses beginning with' field, enter legacy domain URLs. Use format: *.legacy-domain.com or legacy-domain.com or 192.168.1.* for IP ranges. Separate multiple domains with semicolons. 6) Click 'Save'. 7) Restart browser or application. Legacy domains in exception list will bypass proxy. Note: You may need administrator rights to modify proxy settings. Contact IT if you don't have permission to change proxy configuration.",
        "metadata": {"source": "IT Helpdesk - Proxy Exceptions Windows", "category": "Proxy", "priority": "high"}
    },
    {
        "page_content": "How to add URLs to proxy exceptions on macOS: To configure proxy exceptions for legacy domains on macOS, follow these steps. 1) Open System Preferences > Network. 2) Select your active network connection (WiFi or Ethernet). 3) Click 'Advanced' button. 4) Go to 'Proxies' tab. 5) Check the proxy protocols you're using (HTTP, HTTPS, SOCKS). 6) In 'Bypass proxy settings for these Hosts & Domains' field, enter legacy domain URLs. Format: *.legacy-domain.com, legacy-domain.com, 192.168.1.0/24 (for IP ranges). Separate multiple entries with commas. 7) Click 'OK' to save. 8) Click 'Apply' in Network preferences. 9) Restart applications accessing legacy domains. Domains in bypass list will connect directly without proxy. For system-wide changes, you may need administrator password. Contact IT if proxy settings are managed by MDM and cannot be modified.",
        "metadata": {"source": "IT Helpdesk - Proxy Exceptions macOS", "category": "Proxy", "priority": "high"}
    },
    {
        "page_content": "Legacy domain access - disable proxy and use VPN: If legacy domains are blocked by proxy and you cannot modify proxy exceptions, disable proxy and use VPN instead. Steps: 1) Disable proxy: Windows - Settings > Network & Internet > Proxy > Turn off 'Use a proxy server'. macOS - System Preferences > Network > Advanced > Proxies > Uncheck all proxy options. 2) Connect to company VPN (GlobalProtect or corporate VPN): Launch VPN client, enter credentials, wait for connection confirmation. 3) Access legacy domain: VPN routes all traffic directly, bypassing proxy. Legacy domains should now be accessible. 4) Keep VPN connected while using legacy systems. 5) Re-enable proxy when finished if required by company policy. Note: VPN provides secure direct access but may have performance implications. For frequent access to legacy domains, request proxy whitelist from IT helpdesk for permanent solution.",
        "metadata": {"source": "IT Helpdesk - Legacy Domain VPN Access", "category": "VPN", "priority": "medium"}
    },
    {
        "page_content": "Proxy configuration for legacy systems: Legacy systems and old internal applications often require proxy exceptions to function properly. Common legacy domains include: old internal tools (legacy-app.company.com), deprecated APIs (api-v1.legacy.com), historical systems (legacy-system.internal), old file servers (files-legacy.company.local). Solution: Add these domains to proxy bypass list in system proxy settings. Windows: Proxy settings > Advanced > Exceptions list. macOS: Network > Advanced > Proxies > Bypass settings. Use wildcards (*.legacy-domain.com) to cover subdomains. For multiple legacy domains, separate with semicolons (Windows) or commas (macOS). Test access after adding exceptions. If proxy exceptions don't work, disable proxy and use VPN. For company-wide legacy domain access, request IT to whitelist domains in corporate proxy policy. Document legacy domains that require proxy exceptions for your team.",
        "metadata": {"source": "IT Helpdesk - Legacy Systems Proxy Config", "category": "Proxy", "priority": "medium"}
    },
    {
        "page_content": "Legacy domain connection errors - troubleshooting: If you receive 'Proxy error', 'Connection refused', or 'Cannot reach legacy-domain.com' errors, the legacy domain is likely blocked by proxy. Symptoms: Domain works on mobile hotspot but not corporate network, error mentions proxy authentication, connection times out after proxy handshake. Solutions: 1) Quick fix - Add domain to proxy exceptions: Configure proxy to bypass legacy domain (see proxy exception guides). 2) Alternative - Disable proxy and use VPN: Turn off proxy, connect to VPN, access legacy domain through VPN. 3) Permanent - Request proxy whitelist: Submit IT ticket to whitelist legacy domain in corporate proxy. Include: domain name, business justification, who needs access, why legacy domain is required. IT will review and whitelist if approved. Test each solution to determine which works best for your legacy domain. Contact IT helpdesk if all solutions fail.",
        "metadata": {"source": "IT Helpdesk - Legacy Domain Connection Errors", "category": "Domain Blocking", "priority": "high"}
    },
    {
        "page_content": "When to use proxy exceptions vs VPN for legacy domains: Use proxy exceptions when: You need quick access to specific legacy domains, you have permission to modify proxy settings, legacy domain access is occasional, you want to keep proxy enabled for other traffic. Add legacy domains to proxy bypass list in system settings. Use VPN when: Proxy exceptions don't work, you cannot modify proxy settings (MDM managed), you need access to multiple legacy systems, legacy domains require different network routes, proxy modifications require IT approval that takes time. Disable proxy and connect to VPN for immediate access. Request proxy whitelist from IT when: Legacy domain access is required by multiple users, access is frequent or permanent, you need company-wide solution, proxy exceptions are not allowed by policy. IT will whitelist domain in corporate proxy policy. Choose solution based on your access needs and IT policies.",
        "metadata": {"source": "IT Helpdesk - Proxy Exceptions vs VPN for Legacy", "category": "Proxy", "priority": "medium"}
    },
    {
        "page_content": "VPN connection failed - initial troubleshooting: If VPN won't connect, check internet connection first. Verify VPN server address and credentials are correct. Check if VPN client software is up to date. Try different VPN server location. Disable firewall temporarily to test if it's blocking VPN. Check VPN service status page for outages. Verify your account is active and not expired. Restart VPN client and computer. Check if port 500 (IKE), 4500 (IPSec), or 1194 (OpenVPN) is blocked.",
        "metadata": {"source": "IT Helpdesk - VPN Connection Failed", "category": "VPN", "priority": "high"}
    },
    {
        "page_content": "VPN authentication errors: Error 'Invalid credentials' means username or password is wrong. Verify credentials are correct and account is not locked. Check if two-factor authentication (2FA) code is required. Reset VPN password through IT portal if forgotten. Error 'Certificate validation failed' means VPN certificate is expired or invalid. Update VPN client to latest version. Delete old VPN profile and recreate connection. Contact IT to issue new certificate if needed. Error 'Remote server not responding' indicates VPN server is down or unreachable.",
        "metadata": {"source": "IT Helpdesk - VPN Authentication Errors", "category": "VPN", "priority": "high"}
    },
    {
        "page_content": "VPN connection drops frequently - solutions: If VPN disconnects often, check internet stability (run ping test). Move closer to WiFi router or use wired connection. Update VPN client software to latest version. Change VPN protocol (IKEv2, OpenVPN, L2TP) in settings. Increase VPN timeout settings. Disable power saving mode on network adapter. Check if antivirus or firewall is interfering with VPN. Try different VPN server that's closer geographically. Contact IT if issue persists for network configuration review.",
        "metadata": {"source": "IT Helpdesk - VPN Connection Drops", "category": "VPN", "priority": "medium"}
    },
    {
        "page_content": "VPN connected but cannot access internal resources: If VPN connects but you can't access internal servers or applications, check routing table (route print on Windows, netstat -rn on macOS). Verify VPN is using correct DNS servers. Flush DNS cache and renew IP address. Check if split tunneling is enabled (may bypass VPN for some traffic). Verify internal resource IP addresses are reachable (ping test). Check firewall rules allow traffic to internal network. Contact IT to verify VPN routing configuration and DNS settings.",
        "metadata": {"source": "IT Helpdesk - VPN Routing Issues", "category": "VPN", "priority": "high"}
    },
    {
        "page_content": "VPN slow connection speed troubleshooting: If VPN is slow, test internet speed without VPN first to establish baseline. Try different VPN server location closer to your physical location. Change VPN protocol (OpenVPN UDP is usually faster than TCP). Disable encryption if not required (less secure but faster). Close bandwidth-intensive applications. Check if QoS (Quality of Service) is limiting VPN traffic. Try during off-peak hours. Upgrade internet plan if consistently slow. Contact IT if corporate VPN is always slow for infrastructure review.",
        "metadata": {"source": "IT Helpdesk - VPN Speed Issues", "category": "VPN", "priority": "medium"}
    },
    {
        "page_content": "VPN not working on public WiFi: Many public WiFi networks block VPN connections. Try using mobile hotspot instead. Use different VPN port (some networks only block standard ports). Try obfuscated VPN servers if available. Use VPN protocol that mimics HTTPS traffic. Connect to VPN before connecting to public WiFi. If corporate VPN, contact IT for VPN alternative or travel router solution. For personal VPN, try different VPN provider that works on restricted networks.",
        "metadata": {"source": "IT Helpdesk - VPN Public WiFi Issues", "category": "VPN", "priority": "medium"}
    },
    {
        "page_content": "Proxy and VPN conflict resolution: If both proxy and VPN are configured, conflicts can occur. VPN typically takes precedence over proxy settings. Disable proxy when using VPN, or configure proxy within VPN client if needed. Check application-specific proxy settings (browser, email client). For corporate environments, VPN usually handles routing automatically. If you need both, configure proxy as SOCKS5 proxy in VPN client. Test connection with proxy disabled first, then enable if needed. Contact IT for network architecture guidance.",
        "metadata": {"source": "IT Helpdesk - Proxy VPN Conflict", "category": "Proxy", "priority": "medium"}
    },
    {
        "page_content": "ALKS access blocked by proxy - solution: If you cannot access ALKS (Application Lifecycle Management System) and receive connection errors, the corporate proxy may be blocking the application. Solution options: 1) Switch WiFi networks: Disconnect from WiFi Corporate and connect to WiFi Project. WiFi Project typically has different proxy settings and may allow ALKS access. On Windows: Click WiFi icon > Select 'WiFi Project' network. On macOS: Click WiFi icon > Choose 'WiFi Project'. 2) Alternative: Disable proxy settings temporarily and connect to GlobalProtect VPN. GlobalProtect VPN will handle network routing and allow ALKS access without proxy. Restart ALKS application after switching networks or connecting to GlobalProtect. If issue persists, contact IT helpdesk for assistance.",
        "metadata": {"source": "IT Helpdesk - ALKS Proxy Blocking", "category": "Proxy", "priority": "high"}
    },
    {
        "page_content": "Rally access blocked by proxy - solution: If Rally (project management tool) cannot connect or times out, corporate proxy may be blocking the connection. Solution options: 1) Switch WiFi networks: Change from WiFi Corporate to WiFi Project. WiFi Project network often has different proxy configurations that allow Rally access. Windows: Disconnect from current WiFi > Connect to 'WiFi Project'. macOS: Click WiFi icon > Switch to 'WiFi Project' network. 2) Alternative: Disable proxy settings completely and connect to GlobalProtect VPN. GlobalProtect will route traffic properly and bypass proxy restrictions. Launch Rally after switching to WiFi Project or after GlobalProtect connection is established. Clear Rally cache if connection issues continue. Contact IT if Rally still doesn't work after these steps.",
        "metadata": {"source": "IT Helpdesk - Rally Proxy Blocking", "category": "Proxy", "priority": "high"}
    },
    {
        "page_content": "Development tools blocked by proxy - Jira, Confluence, Git: If development tools like Jira, Confluence, or Git are blocked or timing out, corporate proxy is likely blocking these applications. Solution: Disable system proxy settings. Then connect to GlobalProtect VPN which provides direct network access without proxy interference. Steps: 1) Turn off proxy in system settings (Windows: Network & Internet > Proxy, macOS: Network > Advanced > Proxies). 2) Connect to GlobalProtect VPN. 3) Restart the development tool. GlobalProtect handles all network routing automatically. For Git, you may need to configure Git to use GlobalProtect routes. Contact IT if specific tools still fail after VPN connection.",
        "metadata": {"source": "IT Helpdesk - Development Tools Proxy Block", "category": "Proxy", "priority": "high"}
    },
    {
        "page_content": "How to disable proxy and use GlobalProtect VPN: When applications are blocked by proxy, use GlobalProtect VPN instead. Steps: 1) Disable proxy: Windows - Settings > Network & Internet > Proxy > Turn off proxy server. macOS - System Preferences > Network > Advanced > Proxies > Uncheck all. 2) Install GlobalProtect client from IT portal if not installed. 3) Launch GlobalProtect, enter portal address: vpn.company.com. 4) Sign in with domain credentials (username@company.com). 5) Enable 2FA if prompted. 6) Wait for connection confirmation. 7) Restart blocked applications. GlobalProtect routes all traffic securely without proxy. Contact IT if GlobalProtect won't connect.",
        "metadata": {"source": "IT Helpdesk - Disable Proxy Use GlobalProtect", "category": "VPN", "priority": "high"}
    },
    {
        "page_content": "Application timeout errors due to proxy - troubleshooting: If applications show 'Connection timeout', 'Server unreachable', or 'Proxy error' messages, corporate proxy may be blocking them. Common affected applications: ALKS, Rally, Jira, Confluence, Git, development IDEs. Quick fixes: 1) Switch WiFi: Change from WiFi Corporate to WiFi Project network. WiFi Project has different proxy settings that often allow blocked applications to work. This is the fastest solution for ALKS and Rally. 2) Use GlobalProtect VPN: Disable proxy settings completely in system network settings, then connect to GlobalProtect VPN which bypasses proxy restrictions. GlobalProtect provides secure direct network access. After switching WiFi or connecting to VPN, restart the application. If multiple team members report same issue, it's likely a proxy policy blocking the application. Report to IT helpdesk with application name and error message for proxy whitelist consideration.",
        "metadata": {"source": "IT Helpdesk - Application Timeout Proxy Issues", "category": "Proxy", "priority": "medium"}
    },
    {
        "page_content": "GlobalProtect VPN setup for proxy-blocked applications: GlobalProtect VPN is the recommended solution when corporate proxy blocks applications like ALKS, Rally, or development tools. Setup: Download GlobalProtect from IT portal (portal.company.com/vpn). Install and launch GlobalProtect. Enter portal address provided by IT (usually vpn.company.com). Sign in with your domain username and password. Complete 2FA if enabled. Once connected, GlobalProtect icon turns green in system tray. All network traffic routes through GlobalProtect, bypassing proxy. Applications blocked by proxy should now work. Keep GlobalProtect connected while using these applications. Disconnect only when finished. Contact IT for GlobalProtect portal address or connection issues.",
        "metadata": {"source": "IT Helpdesk - GlobalProtect VPN Setup", "category": "VPN", "priority": "high"}
    },
    {
        "page_content": "Proxy blocking ALKS - common error messages: Users report 'Unable to connect to ALKS server', 'Proxy authentication failed', or 'Connection refused' errors when accessing ALKS. This indicates proxy is blocking ALKS connections. Resolution options: 1) Switch to WiFi Project: If on WiFi Corporate, switch to WiFi Project network which may have proxy settings that allow ALKS. Windows: Click WiFi icon > Select 'WiFi Project'. macOS: WiFi menu > Choose 'WiFi Project'. 2) Use GlobalProtect VPN: Turn off proxy in system settings and connect to GlobalProtect VPN. GlobalProtect provides direct network access without proxy. After switching networks or GlobalProtect connection, ALKS should work normally. If ALKS still fails, check firewall isn't blocking it separately. Verify ALKS server address is correct. Clear ALKS application cache. Contact IT helpdesk with error message if problem continues.",
        "metadata": {"source": "IT Helpdesk - ALKS Connection Errors", "category": "Proxy", "priority": "high"}
    },
    {
        "page_content": "Rally connection issues - proxy blocking resolution: Rally users experiencing 'Cannot reach Rally server', 'Proxy error 502', or continuous loading screens have two solution options. Option 1 - Switch WiFi: Change from WiFi Corporate to WiFi Project network. WiFi Project often has proxy settings that allow Rally access. Steps: Disconnect from current WiFi > Connect to 'WiFi Project' > Close Rally > Reopen Rally. Option 2 - Use GlobalProtect VPN: Disable all proxy configurations in system network settings, connect to GlobalProtect VPN with domain credentials, wait for connection confirmation, then launch Rally. Rally should connect successfully through WiFi Project or GlobalProtect. If Rally works on some networks but not others, proxy is likely the issue. For teams frequently using Rally, consider requesting proxy whitelist exception from IT. Document the issue in IT helpdesk ticket for tracking.",
        "metadata": {"source": "IT Helpdesk - Rally Connection Issues", "category": "Proxy", "priority": "high"}
    },
    {
        "page_content": "When to disable proxy and use GlobalProtect VPN or switch WiFi: When applications like ALKS or Rally are blocked, you have multiple solutions. Option 1 - Switch WiFi: If connected to WiFi Corporate, switch to WiFi Project network. WiFi Project has different proxy settings that often allow ALKS and Rally access. This is the quickest solution. Option 2 - Use GlobalProtect VPN: Disable proxy and connect to GlobalProtect VPN for applications timeout or can't connect (ALKS, Rally, Jira, Confluence), receiving proxy authentication errors (407, 502), development tools blocked (Git, IDEs, build servers), API connections failing through proxy. GlobalProtect VPN provides secure direct access without proxy interference. Try WiFi switching first as it's faster, then use GlobalProtect if WiFi Project is not available. For permanent access to blocked apps, request proxy whitelist through IT helpdesk.",
        "metadata": {"source": "IT Helpdesk - When to Use GlobalProtect vs Proxy", "category": "VPN", "priority": "medium"}
    },
    {
        "page_content": "GlobalProtect VPN connection problems: If GlobalProtect won't connect, verify portal address is correct (usually vpn.company.com or provided by IT). Check internet connection is working. Verify domain credentials are correct and account is active. Ensure 2FA code is entered if prompted. Check if GlobalProtect client is up to date - update from IT portal if needed. Disable firewall temporarily to test if it's blocking GlobalProtect. Try different network connection (WiFi vs ethernet). Restart GlobalProtect service: Windows (Services > GlobalProtect) or macOS (Activity Monitor). Check if corporate network allows VPN connections. Contact IT with error message for assistance. GlobalProtect is required for accessing proxy-blocked applications.",
        "metadata": {"source": "IT Helpdesk - GlobalProtect Connection Issues", "category": "VPN", "priority": "high"}
    },
    {
        "page_content": "Switch WiFi networks for ALKS and Rally access: When ALKS or Rally is blocked on WiFi Corporate, switch to WiFi Project network. WiFi Project has different proxy configurations that typically allow access to these applications. Steps to switch: Windows - Click WiFi icon in system tray > Select 'WiFi Project' network > Enter password if required > Wait for connection. macOS - Click WiFi icon in menu bar > Choose 'WiFi Project' network > Enter credentials > Connect. After switching, close and restart ALKS or Rally application. Applications should connect successfully on WiFi Project. If you need to switch back to WiFi Corporate, use same steps. Note: WiFi Project may have limited internet access for security, so switch back to Corporate WiFi for general browsing. Contact IT if WiFi Project network is not available or password is unknown.",
        "metadata": {"source": "IT Helpdesk - WiFi Network Switching for ALKS Rally", "category": "Network", "priority": "high"}
    },
    {
        "page_content": "WiFi Corporate vs WiFi Project - when to use which: WiFi Corporate is the standard corporate network with full proxy enforcement. Use WiFi Corporate for: General internet browsing, email access, standard office applications, accessing corporate resources. WiFi Project is a separate network with relaxed proxy settings for development tools. Use WiFi Project when: ALKS is blocked on Corporate WiFi, Rally cannot connect on Corporate WiFi, development tools are blocked, you need direct access to project management tools. To switch: Windows - Click WiFi icon > Select desired network. macOS - Click WiFi menu > Choose network. Switch back to Corporate WiFi after finishing work with blocked applications. Note: WiFi Project may restrict access to certain corporate resources. Contact IT if you're unsure which network to use or if access issues persist.",
        "metadata": {"source": "IT Helpdesk - WiFi Corporate vs Project Network", "category": "Network", "priority": "medium"}
    },
    {
        "page_content": "ALKS and Rally not working - quick fix by switching WiFi: Many users report ALKS and Rally connection issues when connected to WiFi Corporate. Quick solution: Switch to WiFi Project network. WiFi Corporate enforces strict proxy policies that block these applications, while WiFi Project has proxy configurations that allow access. How to switch: Disconnect from current WiFi network, select 'WiFi Project' from available networks, enter network password if prompted, wait for connection confirmation, close ALKS or Rally application completely, reopen the application. The application should now connect successfully. This is often faster than configuring GlobalProtect VPN. Switch back to WiFi Corporate when done if you need access to other corporate resources. If WiFi Project is not available or doesn't work, use GlobalProtect VPN as alternative solution. Document which network works for your team in IT helpdesk tickets.",
        "metadata": {"source": "IT Helpdesk - ALKS Rally WiFi Switch Quick Fix", "category": "Network", "priority": "high"}
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
        "page_content": "How to set up multi-factor authentication (2FA/MFA): Enable 2FA for additional security. Download authenticator app (Microsoft Authenticator, Google Authenticator) on your mobile device. Go to security settings in IT portal, select 'Enable 2FA', scan QR code with authenticator app. Enter verification code to complete setup. Backup codes are provided - store them securely. 2FA is required for VPN, email, and sensitive systems. If you lose access to authenticator, contact IT immediately with backup code.",
        "metadata": {"source": "FAQ - Multi-Factor Authentication Setup", "category": "Authentication", "priority": "high"}
    },
    {
        "page_content": "Remote desktop connection troubleshooting: To connect to remote desktop, ensure Remote Desktop is enabled on target computer. Use RDP client (mstsc.exe on Windows, Microsoft Remote Desktop on Mac). Enter computer name or IP address. Use domain credentials (domain\\username). If connection fails, check firewall allows RDP (port 3389). Verify target computer is powered on and connected to network. For external connections, use VPN first then RDP. Contact IT if you need remote desktop access enabled.",
        "metadata": {"source": "FAQ - Remote Desktop Connection", "category": "Remote Access", "priority": "medium"}
    },
    {
        "page_content": "Backup and recovery procedures: Company files are automatically backed up to network drives daily. Personal files should be saved to OneDrive or network drive, not local C: drive. To restore files, contact IT with file name and approximate date. Backups are retained for 30 days. Critical files should be saved to multiple locations. For accidental deletion, check Recycle Bin first. Use File History on Windows for personal backups. Cloud storage (OneDrive) provides version history for recovery.",
        "metadata": {"source": "FAQ - Backup and Recovery", "category": "Data Management", "priority": "high"}
    },
    {
        "page_content": "Browser issues and troubleshooting: If browser is slow or crashing, clear cache and cookies (Ctrl+Shift+Delete). Disable unnecessary extensions and add-ons. Update browser to latest version. Reset browser settings if issues persist. For compatibility issues, try different browser (Chrome, Edge, Firefox). Clear browsing data regularly. Disable hardware acceleration if experiencing crashes. Check if issue occurs in incognito/private mode to isolate extension problems. Contact IT if browser won't start or displays errors.",
        "metadata": {"source": "FAQ - Browser Troubleshooting", "category": "Software", "priority": "medium"}
    },
    {
        "page_content": "File and folder permission issues: If you can't access files or folders, check if you have proper permissions. Right-click folder > Properties > Security tab to view permissions. Contact file owner or your manager to request access. Network drives require VPN connection for remote access. Shared folders may require specific group membership. If you recently changed departments, permissions may need updating. Temporary access can be granted by IT for urgent needs. Document access requests through IT portal.",
        "metadata": {"source": "FAQ - File Permissions", "category": "Security", "priority": "medium"}
    },
    {
        "page_content": "Windows updates and system patching: Windows updates are managed by IT and deployed automatically. Updates typically install during off-hours or scheduled maintenance windows. Don't turn off computer when 'Update and restart' message appears. If update fails, run Windows Update troubleshooter. Check for updates manually: Settings > Update & Security > Windows Update. Critical security updates are deployed immediately. Feature updates are scheduled quarterly. If update causes issues, contact IT for rollback. Keep computer connected to network for updates.",
        "metadata": {"source": "FAQ - System Updates", "category": "Software", "priority": "high"}
    },
    {
        "page_content": "Disk cleanup and storage management: Low disk space can cause performance issues. Use Disk Cleanup tool (cleanmgr.exe) to remove temporary files. Uninstall unused programs through Control Panel. Move large files to network drive or OneDrive. Empty Recycle Bin regularly. Clear browser cache and downloads folder. Use Storage Sense on Windows 10/11 for automatic cleanup. Check for large files using File Explorer size view. Contact IT if you need additional storage or have questions about file locations. Aim to keep at least 15% free space.",
        "metadata": {"source": "FAQ - Disk Cleanup", "category": "Hardware", "priority": "medium"}
    },
    {
        "page_content": "Email security - phishing and spam: Be cautious of suspicious emails. Don't click links or download attachments from unknown senders. Check sender email address carefully - scammers often use similar addresses. Look for spelling errors and urgent language. Verify requests for credentials or payments by phone. Report phishing emails to IT immediately. Don't reply to spam - use 'Report Spam' button. Company email filters most spam automatically. If legitimate emails go to spam, add sender to contacts. Enable email encryption for sensitive communications.",
        "metadata": {"source": "FAQ - Email Security", "category": "Security", "priority": "high"}
    },
    {
        "page_content": "Antivirus and security software: Company computers have corporate antivirus installed and managed by IT. Don't install additional antivirus software as it may conflict. Antivirus updates automatically and scans regularly. If you suspect malware, run full scan immediately. Quarantine suspicious files - don't delete until verified. Keep antivirus enabled at all times. For personal devices, use company-approved antivirus if connecting to corporate network. Report security incidents to IT immediately. Don't disable antivirus for any reason.",
        "metadata": {"source": "FAQ - Antivirus Protection", "category": "Security", "priority": "high"}
    },
    {
        "page_content": "Microsoft Teams troubleshooting: If Teams won't start, restart application and check for updates. Clear Teams cache: Close Teams, delete %appdata%\\Microsoft\\Teams folder, restart. Check internet connection and firewall settings. For audio/video issues, check device permissions in Windows Settings. Test microphone and camera in Teams settings. Update audio and video drivers. For screen sharing issues, ensure you have proper permissions. Try web version of Teams if desktop app fails. Contact IT if Teams won't connect to organization.",
        "metadata": {"source": "FAQ - Teams Troubleshooting", "category": "Collaboration", "priority": "medium"}
    },
    {
        "page_content": "OneDrive sync issues: If OneDrive files aren't syncing, check internet connection. Right-click OneDrive icon in system tray, check sync status. Pause and resume sync to reset connection. Check if you're signed in with correct account. Clear OneDrive cache: Close OneDrive, delete %localappdata%\\Microsoft\\OneDrive\\cache, restart. Ensure sufficient storage space in OneDrive. Check file names for invalid characters. Large files may take longer to sync. For shared files, verify you have access permissions. Contact IT if sync consistently fails.",
        "metadata": {"source": "FAQ - OneDrive Sync Issues", "category": "Cloud Storage", "priority": "medium"}
    },
    {
        "page_content": "Mobile device management and setup: Company mobile devices are managed through MDM (Mobile Device Management). Install company portal app from app store. Sign in with company credentials to enroll device. Follow setup instructions to configure email, VPN, and security policies. Corporate devices have restrictions on app installation. Personal devices used for work must comply with security policies. Report lost or stolen devices immediately to IT and remote wipe may be performed. Keep devices updated with latest OS and security patches.",
        "metadata": {"source": "FAQ - Mobile Device Management", "category": "Mobile", "priority": "medium"}
    },
    {
        "page_content": "Network troubleshooting advanced steps: If basic network troubleshooting doesn't work, check IP configuration (ipconfig /all on Windows). Verify you're getting IP address from DHCP server. Test connectivity with ping to gateway and DNS servers. Check network adapter status in Device Manager. Update network drivers from manufacturer website. Try different network cable or WiFi connection. Check if issue is device-specific or network-wide. Use network diagnostic tools built into OS. Review Windows Event Viewer for network errors. Contact IT with diagnostic information for further assistance.",
        "metadata": {"source": "FAQ - Advanced Network Troubleshooting", "category": "Network", "priority": "medium"}
    },
    {
        "page_content": "Firewall and security policies: Company firewall blocks unauthorized access and malicious traffic. Some applications may require firewall exceptions - contact IT to request. Don't disable Windows Firewall unless instructed by IT. Corporate security policies restrict certain websites and applications. Software installation requires IT approval for compliance. USB devices may be restricted for security. File sharing policies limit external sharing. VPN is required for remote access to internal resources. Follow security policies to protect company data. Report security violations immediately.",
        "metadata": {"source": "FAQ - Firewall and Security Policies", "category": "Security", "priority": "high"}
    },
    {
        "page_content": "Screen sharing and remote support: IT may request screen sharing for remote support. Use approved tools like Teams screen share or remote desktop. Never share screen with unknown callers. Verify IT support identity before granting access. Screen sharing requires your explicit permission. IT can view your screen but cannot control without permission. End session immediately if suspicious activity occurs. Use secure channels for screen sharing - never use personal tools. Report any unauthorized access attempts. Screen sharing sessions are logged for security audit.",
        "metadata": {"source": "FAQ - Screen Sharing Support", "category": "Remote Access", "priority": "low"}
    },
    {
        "page_content": "Outlook email configuration and issues: Configure Outlook with Exchange server: exchange.company.com. Use autodiscover for automatic setup with email address and password. If autodiscover fails, manually configure server settings. Check account settings: File > Account Settings > Account Settings. For sync issues, recreate Outlook profile. Clear Outlook cache: Close Outlook, delete .ost file, restart. Check if issue affects all emails or specific folders. Verify email rules aren't moving messages. Check Junk Email folder for legitimate messages. Update Outlook to latest version. Contact IT if authentication fails.",
        "metadata": {"source": "FAQ - Outlook Configuration", "category": "Email", "priority": "medium"}
    },
    {
        "page_content": "Password policy and requirements: Company passwords must be at least 12 characters with uppercase, lowercase, numbers, and special characters. Passwords expire every 90 days - you'll receive reminder emails. Don't reuse last 12 passwords. Don't share passwords with anyone including IT support. Use password manager for secure storage. Enable multi-factor authentication for additional security. Change password immediately if compromised. Use unique passwords for different systems. Don't write passwords on paper or store in plain text. Contact IT if you forget password - they cannot retrieve it, only reset.",
        "metadata": {"source": "FAQ - Password Policy", "category": "Authentication", "priority": "high"}
    },
    {
        "page_content": "How to get ServiceNow token from SLED Slack channel? Step 1: Open Slack application and navigate to the SLED workspace. Step 2: Search for or join the #sled channel (SLED - Service Level Engineering & Development). Step 3: In the SLED channel, use the slash command '/snow-token' or search for pinned messages containing 'ServiceNow token' or 'SNOW token'. Step 4: The bot will respond with your personal ServiceNow API token. Alternatively, type '@SLED Bot get token' or '@SLED Bot snow token' to request your token. Step 5: Copy the token immediately - tokens are sensitive and should not be shared. Step 6: Use the token in your ServiceNow API requests or configuration. Token format is typically a long alphanumeric string. Tokens expire after 90 days - you'll need to request a new one. If the bot doesn't respond, check if you have access to the SLED channel. Contact SLED team admin if you cannot access the channel. Never share your ServiceNow token with others or commit it to version control.",
        "metadata": {"source": "FAQ - ServiceNow Token from SLED Slack", "category": "ServiceNow", "priority": "high", "ticket_id": "SNOW-2024-001", "difficulty": "low", "resolution_time": "2-5 minutes", "affected_systems": ["ServiceNow", "Slack", "SLED Channel"], "related_software": ["Slack Desktop", "ServiceNow API"], "tags": ["servicenow", "token", "sled", "slack", "api", "authentication"], "channel": "#sled", "bot_command": "/snow-token", "token_validity": "90 days", "access_requirement": "SLED channel membership"}
    },
    {
        "page_content": "ServiceNow token usage and configuration: After obtaining your ServiceNow token from SLED Slack channel, configure it in your application. For API requests, include token in Authorization header: 'Authorization: Bearer YOUR_TOKEN_HERE'. For ServiceNow CLI, set environment variable: export SNOW_TOKEN='your_token_here'. For Python scripts, store token securely in environment variables or secure vault, never hardcode. Token format: Usually 40-64 character alphanumeric string. Use token in REST API calls to ServiceNow instance. Example API endpoint: https://your-instance.service-now.com/api/now/table/incident. Include headers: 'Content-Type: application/json' and 'Authorization: Bearer TOKEN'. Test token with simple GET request to verify it works. If token is invalid or expired, request new one from SLED Slack channel. Tokens are user-specific and cannot be shared between accounts.",
        "metadata": {"source": "FAQ - ServiceNow Token Configuration", "category": "ServiceNow", "priority": "medium", "ticket_id": "SNOW-2024-002", "difficulty": "medium", "resolution_time": "10-15 minutes", "affected_systems": ["ServiceNow API", "Development Environment"], "related_software": ["ServiceNow CLI", "Python", "REST API"], "tags": ["servicenow", "token", "api", "configuration", "authentication"], "api_endpoint_example": "https://instance.service-now.com/api/now/table/incident", "header_format": "Authorization: Bearer TOKEN"}
    },
    {
        "page_content": "ServiceNow token expired or invalid - how to renew: If your ServiceNow token has expired (typically after 90 days) or returns '401 Unauthorized' errors, you need to get a new token. Go to SLED Slack channel (#sled) and use command '/snow-token' or '@SLED Bot get token' to request a new token. The bot will generate a fresh token for your account. Replace old token in your configuration with the new one. Update environment variables, configuration files, or secure vaults where token is stored. Test the new token with a simple API call to verify it works. If you continue to get authentication errors after updating token, verify: 1) Token was copied correctly without extra spaces, 2) Token is for correct ServiceNow instance, 3) Your account has proper permissions, 4) Token hasn't been revoked. If issues persist, contact SLED team in Slack channel or IT helpdesk.",
        "metadata": {"source": "FAQ - ServiceNow Token Renewal", "category": "ServiceNow", "priority": "medium", "ticket_id": "SNOW-2024-003", "difficulty": "low", "resolution_time": "5 minutes", "affected_systems": ["ServiceNow API", "SLED Slack Channel"], "related_software": ["Slack", "ServiceNow"], "tags": ["servicenow", "token", "expired", "renewal", "sled", "authentication"], "token_lifetime": "90 days", "renewal_method": "SLED Slack channel /snow-token command"}
    },
    {
        "page_content": "Cannot access SLED Slack channel for ServiceNow token: If you cannot find or access the #sled channel in Slack, you may not have the required permissions. Verify you're in the correct Slack workspace (SLED workspace). Check if you're a member of the SLED channel - you may need to be added by a channel admin. Contact SLED team lead or IT administrator to request access to #sled channel. Alternative methods: If you cannot access SLED channel, contact IT helpdesk directly and request ServiceNow token. Provide your employee ID and business justification. IT will verify your access needs and provide token through secure channel. For urgent requests, call IT helpdesk hotline. Once you have channel access, use '/snow-token' command to get your token. Channel access is typically granted within 1 business day after approval.",
        "metadata": {"source": "FAQ - SLED Channel Access Issues", "category": "ServiceNow", "priority": "high", "ticket_id": "SLACK-2024-001", "difficulty": "low", "resolution_time": "1 business day", "affected_systems": ["Slack", "SLED Channel"], "tags": ["sled", "slack", "channel", "access", "permissions", "servicenow"], "alternative_method": "Contact IT helpdesk directly", "approval_required": True}
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
    },
    {
        "keywords": ["proxy", "proxy server", "proxy settings", "proxy authentication", "407", "502"],
        "category": "Proxy",
        "solution": "Check proxy configuration in system settings, verify credentials, and ensure proxy server is accessible. Contact IT if proxy server is down."
    },
    {
        "keywords": ["alks", "alks blocked", "alks connection", "alks timeout", "alks error"],
        "category": "Proxy",
        "solution": "ALKS is blocked by proxy. Quick fix: Switch from WiFi Corporate to WiFi Project network. Alternative: Disable proxy settings and connect to GlobalProtect VPN. Both solutions allow ALKS access."
    },
    {
        "keywords": ["rally", "rally blocked", "rally connection", "rally timeout", "rally error"],
        "category": "Proxy",
        "solution": "Rally is blocked by proxy. Quick fix: Switch from WiFi Corporate to WiFi Project network. Alternative: Turn off proxy and connect to GlobalProtect VPN, then restart Rally. WiFi Project often works faster."
    },
    {
        "keywords": ["wifi project", "wifi corporate", "switch wifi", "wifi network", "project wifi", "corporate wifi"],
        "category": "Network",
        "solution": "Switch WiFi networks when applications are blocked. Change from WiFi Corporate to WiFi Project for ALKS and Rally access. WiFi Project has different proxy settings that allow these applications. Switch back to Corporate WiFi when done."
    },
    {
        "keywords": ["globalprotect", "globalprotect vpn", "globalprotect connection", "globalprotect setup"],
        "category": "VPN",
        "solution": "Use GlobalProtect VPN when applications are blocked by proxy. Disable proxy, install GlobalProtect from IT portal, connect with domain credentials. GlobalProtect bypasses proxy restrictions."
    },
    {
        "keywords": ["development tools blocked", "jira blocked", "confluence blocked", "git blocked", "ide blocked"],
        "category": "Proxy",
        "solution": "Development tools blocked by proxy. Disable system proxy settings, connect to GlobalProtect VPN, restart the application. GlobalProtect handles network routing without proxy."
    },
    {
        "keywords": ["domain", "blocked", "website blocked", "cannot access", "firewall", "whitelist"],
        "category": "Domain Blocking",
        "solution": "Verify URL is correct, check firewall settings, try different network, or request domain whitelist from IT helpdesk."
    },
    {
        "keywords": ["legacy domain", "legacy system", "legacy url", "old domain", "deprecated domain", "historical system"],
        "category": "Domain Blocking",
        "solution": "Legacy domains blocked by proxy. Option 1: Add URL to proxy exceptions in system settings. Option 2: Disable proxy and use VPN. Option 3: Request proxy whitelist from IT helpdesk."
    },
    {
        "keywords": ["proxy exception", "proxy bypass", "proxy whitelist", "proxy exclusion", "bypass proxy"],
        "category": "Proxy",
        "solution": "Add domain URLs to proxy exception list in system proxy settings. Windows: Proxy settings > Advanced > Exceptions. macOS: Network > Advanced > Proxies > Bypass settings. Use wildcards for subdomains."
    },
    {
        "keywords": ["vpn", "vpn connection", "vpn error", "vpn authentication", "vpn slow", "vpn drops"],
        "category": "VPN",
        "solution": "Check internet connection, verify VPN credentials, update VPN client, try different server location, or contact IT support."
    },
    {
        "keywords": ["2fa", "mfa", "multi-factor", "authenticator", "two-factor"],
        "category": "Authentication",
        "solution": "Enable 2FA through IT portal, use authenticator app, store backup codes securely, contact IT if access is lost."
    },
    {
        "keywords": ["remote desktop", "rdp", "remote access", "mstsc"],
        "category": "Remote Access",
        "solution": "Use RDP client, ensure Remote Desktop is enabled, check firewall allows port 3389, use VPN for external access."
    },
    {
        "keywords": ["backup", "recovery", "restore", "file recovery", "data backup"],
        "category": "Data Management",
        "solution": "Save files to network drive or OneDrive, contact IT for file restoration, check Recycle Bin, use version history."
    },
    {
        "keywords": ["browser", "chrome", "edge", "firefox", "browser crash", "browser slow"],
        "category": "Software",
        "solution": "Clear cache and cookies, disable extensions, update browser, try different browser, reset browser settings."
    },
    {
        "keywords": ["permission", "access denied", "file access", "folder access", "unauthorized"],
        "category": "Security",
        "solution": "Check file permissions, contact file owner for access, verify group membership, request access through IT portal."
    },
    {
        "keywords": ["update", "windows update", "system update", "patch", "patching"],
        "category": "Software",
        "solution": "Updates are managed automatically by IT, keep computer connected, don't interrupt updates, contact IT if update fails."
    },
    {
        "keywords": ["disk space", "storage", "low disk", "cleanup", "disk cleanup"],
        "category": "Hardware",
        "solution": "Use Disk Cleanup tool, uninstall unused programs, move files to network drive, clear browser cache, aim for 15% free space."
    },
    {
        "keywords": ["phishing", "spam", "suspicious email", "email security", "malicious email"],
        "category": "Security",
        "solution": "Don't click suspicious links, verify sender identity, report phishing to IT, use spam reporting, enable email encryption."
    },
    {
        "keywords": ["antivirus", "malware", "virus", "security scan", "threat"],
        "category": "Security",
        "solution": "Run full antivirus scan, keep antivirus enabled, don't install additional antivirus, report security incidents to IT."
    },
    {
        "keywords": ["teams", "microsoft teams", "teams crash", "teams audio", "teams video"],
        "category": "Collaboration",
        "solution": "Clear Teams cache, check device permissions, update drivers, test in web version, verify internet connection."
    },
    {
        "keywords": ["onedrive", "cloud storage", "sync", "onedrive sync", "file sync"],
        "category": "Cloud Storage",
        "solution": "Check internet connection, pause and resume sync, clear OneDrive cache, verify account, check storage space."
    },
    {
        "keywords": ["mobile", "mdm", "mobile device", "company portal", "device management"],
        "category": "Mobile",
        "solution": "Install company portal app, enroll device with company credentials, follow security policies, report lost devices immediately."
    },
    {
        "keywords": ["firewall", "security policy", "blocked", "access restricted"],
        "category": "Security",
        "solution": "Contact IT for firewall exceptions, don't disable firewall, follow security policies, request access through proper channels."
    },
    {
        "keywords": ["outlook", "email configuration", "exchange", "email sync", "outlook error"],
        "category": "Email",
        "solution": "Recreate Outlook profile, clear cache, check account settings, verify autodiscover, update Outlook, contact IT if authentication fails."
    },
    {
        "keywords": ["password policy", "password expired", "password requirements", "change password"],
        "category": "Authentication",
        "solution": "Use strong password with 12+ characters, don't reuse passwords, change password every 90 days, enable 2FA, contact IT to reset."
    },
    {
        "keywords": ["servicenow", "snow", "token", "sled", "slack", "snow-token"],
        "category": "ServiceNow",
        "solution": "Get ServiceNow token from SLED Slack channel. Open #sled channel in Slack, use command '/snow-token' or '@SLED Bot get token'. The bot will provide your personal API token. Token expires after 90 days."
    },
    {
        "keywords": ["snow token", "servicenow api", "snow api", "servicenow authentication"],
        "category": "ServiceNow",
        "solution": "Request ServiceNow token from SLED Slack channel using '/snow-token' command. Configure token in Authorization header: 'Authorization: Bearer TOKEN'. If you don't have access to #sled channel, contact IT helpdesk."
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
