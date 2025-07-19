<h1>System Status Page</h1>
<h3>Purpose of the Service</h3>
<p style="font-size: 19px;">This service is to provide a single endpoint to quickly check the status of the services<br>
that is currently running in the SCE clubroom.</p>
<p style="font-size: 19px; color: darkorange;">This status page is NOT meant for public access.</p>

<h3>Features</h3>
<ul style="font-size: 19px;">
    <li>Provide the status information in a clean format</li>
    <li>Provide the status for the last 24 hours as additional information</li>
</ul>
<h3>Usage</h3>
<ol style="font-size: 19px;">
    <li>You must have VPN access to be able to run the service locally.
        <ul> <li>follow the instruction on <a>https://openvpn.net/client/</a> and contact an SCE officer for a VPN profile.</li>
        </ul>
    </li>
    <li>You must have the docker daemon running on your machine.
        <ul>
            <li>follow the instruction on <a>https://www.docker.com/products/docker-desktop/</a></li>
            <li>You might need to register for an account.(free)</li>
        </ul>
    </li>
    <li>In a terminal window, go to the project directory root</li>
    <li>Use 
        <code style="border: 2px solid darkgray; background-color: transparent">
        docker compose -f docker-compose.syssts.yml build --no-cache</code> to clean build the project.
    </li>
    <li>Use 
        <code style="border: 2px solid darkgray; background-color: transparent">
        docker compose -f docker-compose.syssts.yml up</code>
         to run the service.
    </li>
    <li>In a browser tab, go to <a>http://localhost:9100/system_status/</a> to see the status page
        <ul>
            <li>Contact Sean or an SCE officer if there's any issue</li>
        </ul>
    </li>
</ol>
<h3>Example Run</h3>
<img src="sample_run.jpg" alt="sample run screenshot">
