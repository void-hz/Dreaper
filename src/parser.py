"""Convert Nmap XML into a structured Python dictionary."""

import xml.etree.ElementTree as ET
from pathlib import Path


def parse_nmap_xml(xml_path: Path) -> dict:
    """Parse an Nmap XML file and return hosts and their port/service data."""
    try:
        tree = ET.parse(xml_path)
    except (ET.ParseError, OSError) as exc:
        raise ValueError(f"Could not read valid Nmap XML: {exc}") from exc

    root = tree.getroot()
    hosts = []

    for host in root.findall("host"):
        address_element = host.find("address")
        address = address_element.get("addr") if address_element is not None else "unknown"

        hostnames = [
            item.get("name")
            for item in host.findall("./hostnames/hostname")
            if item.get("name")
        ]

        ports = []
        ports_element = host.find("ports")

        if ports_element is not None:
            for port in ports_element.findall("port"):
                state_element = port.find("state")
                service_element = port.find("service")

                ports.append({
                    "port": int(port.get("portid")),
                    "protocol": port.get("protocol", "unknown"),
                    "state": state_element.get("state", "unknown") if state_element is not None else "unknown",
                    "service": service_element.get("name", "unknown") if service_element is not None else "unknown",
                    "product": service_element.get("product", "") if service_element is not None else "",
                    "version": service_element.get("version", "") if service_element is not None else "",
                    "extra_info": service_element.get("extrainfo", "") if service_element is not None else "",
                })

        hosts.append({
            "address": address,
            "hostnames": hostnames,
            "ports": ports,
        })

    return {
        "source": "Nmap XML",
        "hosts": hosts,
    }
