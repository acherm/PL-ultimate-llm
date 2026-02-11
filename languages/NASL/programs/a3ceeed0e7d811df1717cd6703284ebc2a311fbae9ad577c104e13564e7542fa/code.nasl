if (description)
{
  script_id(10000);
  script_version("1.0");
  script_name(english:"Sample Banner Check");
  script_summary(english:"Checks for a service banner");
  
  script_description(english:"This script performs a simple banner grab.");
  
  exit(0);
}

port = get_kb_item("Services/www");
if (!port) port = 80;

if (!get_port_state(port)) exit(0);

soc = open_sock_tcp(port);
if (soc)
{
  banner = recv_line(socket:soc, length:1024);
  if (banner)
  {
    security_note(port:port, data:"Banner: " + banner);
  }
  close(soc);
}