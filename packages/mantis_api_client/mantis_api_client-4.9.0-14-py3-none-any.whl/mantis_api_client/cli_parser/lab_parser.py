# -*- coding: utf-8 -*-
import argparse
import json
import os
import pprint
import sys
from typing import Any

import mantis_api_client.scenario_api as scenario_api
from cr_api_client.cli_parser.provisioning_parser import add_provisioning_parser
from mantis_api_client.cli_parser.redteam_parser import add_redteam_parser
from mantis_api_client.oidc import oidc_client


#
# 'lab_info_handler' handler
#
def lab_info_handler(args: Any) -> None:
    # Parameters
    lab_id = args.lab_id

    try:
        lab = scenario_api.fetch_lab(lab_id)
    except Exception as e:
        print(f"Error when fetching lab: '{e}'")
        sys.exit(1)

    if args.json:
        print(json.dumps(lab))
        return

    print("[+] Lab information:")
    print(f"""  [+] \033[1mId\033[0m: {lab.get("id", None)}""")
    print(f"""  [+] \033[1mName\033[0m: {lab.get("name", None)}""")
    print(f"""  [+] \033[1mType\033[0m: {lab.get("content_type", None)}""")
    print(f"""  [+] \033[1mStatus\033[0m: {lab.get("info", None)}""")
    print(f"""  [+] \033[1mStart time\033[0m: {lab.get("start_time", None)}""")
    if lab.get("elapsed_time") is not None:
        time = float(lab.get("elapsed_time", "0")) / 60
        print(f"""  [+] \033[1mElapsed time (minutes)\033[0m: {round(time, 2)}""")
    print(f"""  [+] \033[1mCreated by\033[0m: {lab.get("created_by", None)}""")


#
# 'lab_api_handler' handler
#
def lab_api_handler(args: Any) -> None:
    # Parameters
    lab_id = args.lab_id

    active_profile_domain = oidc_client.get_active_profile_domain(raise_exc=False)
    if not active_profile_domain:
        print("[+] Not authenticated")
        return

    provisioning_api_url = (
        f"https://app.{active_profile_domain}/proxy/{lab_id}/api/provisioning"
    )
    redteam_api_url = f"https://app.{active_profile_domain}/proxy/{lab_id}/api/redteam"

    if args.json:
        print(
            json.dumps(
                {
                    "provisioning_api_url": provisioning_api_url,
                    "redteam_api_url": redteam_api_url,
                }
            )
        )
        return

    print("[+] Lab APIs:")
    print(f"""  [+] \033[1mProvisioning API URL\033[0m: {provisioning_api_url}""")
    print(f"""  [+] \033[1mRedteam API URL\033[0m:      {redteam_api_url}""")


#
# 'lab_stop_handler' handler
#
def lab_stop_handler(args: Any) -> None:
    # Parameters
    lab_id = args.lab_id

    try:
        scenario_api.stop_lab(lab_id)
    except Exception as e:
        print(f"Error when stopping lab: '{e}'")
        sys.exit(1)

    print(f"[+] Lab '{lab_id}' stopped")


#
# 'lab_delete_lab_handler' handler
#
def lab_delete_lab_handler(args: Any) -> None:
    # Parameters
    lab_id = args.lab_id

    try:
        scenario_api.delete_lab(lab_id)
    except Exception as e:
        print(f"Error when deleting lab ID {lab_id}: '{e}'")
        sys.exit(1)

    print(f"[+] Lab '{lab_id}' deleted")


#
# 'lab_resume_handler' handler
#
def lab_resume_handler(args: Any) -> None:
    # Parameters
    lab_id = args.lab_id

    try:
        scenario_api.resume_lab(lab_id)
    except Exception as e:
        print(f"Error when resume lab: '{e}'")
        sys.exit(1)

    print(f"[+] Lab '{lab_id}' resumed")


#
# 'lab_topology_handler' handler
#
def lab_topology_handler(args: Any) -> None:
    # Parameters
    lab_id = args.lab_id

    try:
        topology = scenario_api.fetch_lab_topology(lab_id)
    except Exception as e:
        print(f"Error when fetching scenario topology: '{e}'")
        sys.exit(1)

    if args.json:
        print(topology.json())
        return

    print("[+] Lab topology")
    print("  [+] Nodes")
    for node in topology.nodes:
        print(f"    [+] {node.name} ({node.type})")
    print("  [+] Links")
    for node in topology.nodes:
        if node.type == "switch":
            print(f"    [+] {node.name}")
            for link in topology.links:
                if link.switch.name == node.name:
                    print(f"      [+] {link.node.name} - {link.params.ip}")


#
# 'lab_nodes_handler' handler
#
def lab_nodes_handler(args: Any) -> None:
    # Parameters
    lab_id = args.lab_id

    try:
        nodes = scenario_api.fetch_lab_nodes(lab_id)
    except Exception as e:
        print(f"Error when fetching scenario nodes: '{e}'")
        sys.exit(1)

    if args.json:
        print(json.dumps(nodes))
        return

    print("[+] Lab nodes")
    for node in nodes:
        if node["type"] == "switch":
            continue
        print(f"  [+] {node['name']} ({node['type']})")
        print("    [+] network interfaces")

        for ni in node["network_interfaces"]:
            if ni["ip_address_runtime"] is not None:
                ip_address = ni["ip_address_runtime"]
            else:
                ip_address = ni["ip_address"]
            print(f"      - {ip_address}")

        if node["type"] == "virtual_machine":
            print("    [+] Credentials")
            print(
                f"      - username: {node['username']} - password: {node['password']}"
            )
            print(
                f"      - admin_username: {node['admin_username']} - admin_password: {node['admin_password']}"
            )


#
# 'lab_assets_handler' handler
#
def lab_assets_handler(args: Any) -> None:
    # Parameters
    lab_id = args.lab_id

    try:
        assets = scenario_api.fetch_lab_assets(lab_id)
    except Exception as e:
        print(f"Error when fetching scenario assets: '{e}'")
        sys.exit(1)

    if args.json:
        print(json.dumps(assets))
        return

    print("[+] Lab assets")
    for asset in assets:
        print(f"  [+] {asset['name']} ({asset['type']})")
        print(f"    [+] roles: {asset['roles']}")
        if asset["type"] == "virtual_machine":
            print(f"    [+] os: {asset['os']} ({asset['os_family']})")
            print("    [+] network interfaces")
            for ni in asset["network_interfaces"]:
                print(f"      - {ni['ipv4']}")
            print("    [+] cpe:")
            print(asset["cpe"])


#
# 'lab_attack_report_handler' handler
#
def lab_attack_report_handler(args: Any) -> None:
    # Parameters
    lab_id = args.lab_id

    try:
        attack_report = scenario_api.fetch_lab_attack_report(lab_id)
    except Exception as e:
        print(f"Error when fetching scenario attack_report: '{e}'")
        sys.exit(1)

    if args.json:
        print(json.dumps(attack_report))
        return

    print("[+] Lab attack report:")
    pp = pprint.PrettyPrinter(width=160)
    pp.pprint(attack_report)


#
# 'lab_attack_infras_handler' handler
#
def lab_attack_infras_handler(args: Any) -> None:
    # Parameters
    lab_id = args.lab_id

    try:
        attack_infras = scenario_api.fetch_lab_attack_infras(lab_id)
    except Exception as e:
        print(f"Error when fetching scenario attack_infras: '{e}'")
        sys.exit(1)

    if args.json:
        print(json.dumps(attack_infras))
        return

    print("[+] Lab attack infrastructures:")
    for infra in attack_infras:
        print(f"  [+] {infra}")


#
# 'lab_attack_sessions_handler' handler
#
def lab_attack_sessions_handler(args: Any) -> None:
    # Parameters
    lab_id = args.lab_id

    try:
        attack_sessions = scenario_api.fetch_lab_attack_sessions(lab_id)
    except Exception as e:
        print(f"Error when fetching scenario attack_sessions: '{e}'")
        sys.exit(1)

    if args.json:
        print(json.dumps(attack_sessions))
        return

    knowledge = scenario_api.fetch_lab_attack_knowledge(lab_id)

    print("[+] Lab attack sessions:")
    for session in attack_sessions:
        compromised_host_ip = None
        if "hosts" in knowledge:
            for host in knowledge["hosts"]:
                for nic in host:
                    if nic is not None:
                        if "ip" in nic and "idHost" in nic:
                            if nic["idHost"] == session["idHost"]:
                                compromised_host_ip = nic["ip"]
        print(
            f"  [+] {session['idAttackSession']} - compromised host: {compromised_host_ip} - type: {session['type']} - direct_access: {session['direct_access']} - privilege_level: {session['privilege_level']} - uuid: {session['identifier']}"
        )


#
# 'lab_attack_knowledge_handler' handler
#
def lab_attack_knowledge_handler(args: Any) -> None:
    # Parameters
    lab_id = args.lab_id

    try:
        attack_knowledge = scenario_api.fetch_lab_attack_knowledge(lab_id)
    except Exception as e:
        print(f"Error when fetching scenario attack_knowledge: '{e}'")
        sys.exit(1)

    if args.json:
        print(json.dumps(attack_knowledge))
        return

    print("[+] Lab attack knowledge:")
    pp = pprint.PrettyPrinter(compact=True, width=160)
    pp.pprint(attack_knowledge)


#
# 'lab_notifications_handler' handler
#
def lab_notifications_handler(args: Any) -> None:
    # Parameters
    lab_id = args.lab_id

    try:
        notifications = scenario_api.fetch_lab_notifications(lab_id)
    except Exception as e:
        print(f"Error when fetching scenario notifications: '{e}'")
        sys.exit(1)

    if args.json:
        print(json.dumps(notifications))
        return

    print("[+] Lab notifications")
    for notification in notifications:
        event = json.loads(notification)
        print(f"⚡ {event['event_datetime']} - {event['event_data']}")


#
# 'lab_scenario_run_config_handler' handler
#
def lab_scenario_run_config_handler(args: Any) -> None:
    # Parameters
    lab_id = args.lab_id

    try:
        scenario_run_config = scenario_api.fetch_lab_scenario_run_config(lab_id)
    except Exception as e:
        print(f"Error when fetching scenario run config: '{e}'")
        sys.exit(1)

    if args.json:
        print(scenario_run_config.json())
        return

    print("[+] Lab scenario_run_config:")
    pp = pprint.PrettyPrinter(width=160)
    pp.pprint(scenario_run_config.dict())


def lab_set_lab_handler(args: Any) -> None:
    # Parameters
    lab_id = args.lab_id

    active_profile_domain = oidc_client.get_active_profile_domain(raise_exc=False)
    if not active_profile_domain:
        print("[+] Not authenticated")
        return

    os.environ["PROVISIONING_API_URL"] = (
        f"https://app.{active_profile_domain}/proxy/{lab_id}/api/provisioning"
    )
    os.environ["REDTEAM_API_URL"] = (
        f"https://app.{active_profile_domain}/proxy/{lab_id}/api/redteam"
    )


def lab_unset_lab_handler(args: Any) -> None:
    del os.environ["PROVISIONING_API_URL"]
    del os.environ["REDTEAM_API_URL"]


#
# 'lab_get_remote_access_handler' handler
#
def lab_get_remote_access_handler(args: Any) -> None:
    # Parameters
    lab_id = args.lab_id

    try:
        remote_access_info = scenario_api.fetch_lab_remote_access(lab_id)
    except Exception as e:
        print(f"Error when fetching scenario run config: '{e}'")
        sys.exit(1)

    if args.json:
        print(json.dumps(remote_access_info))
        return

    print("[+] Lab remote access information:")
    print(f"[+] \033[1mLab ID\033[0m: {lab_id}")
    for node_info in remote_access_info:
        print(f"  [+] \033[1mNode name\033[0m: {node_info['name']}")
        print(f"    [+] \033[1mHTTP URL (noVNC)\033[0m: {node_info['http_url']}")
        print("    [+] \033[1mOS accounts\033[0m:")
        for credential in node_info["credentials"]:
            print("      ----")
            for key, value in credential.items():
                print(f"      [+] \033[1m{key}\033[0m: {value}")


def add_lab_parser(root_parser: argparse.ArgumentParser, subparsers: Any) -> None:
    # Subparser lab
    parser_lab = subparsers.add_parser(
        "lab",
        help="Scenario API related commands (lab)",
        formatter_class=root_parser.formatter_class,
    )
    parser_lab.set_defaults(set_lab=lab_set_lab_handler)
    parser_lab.set_defaults(unset_lab=lab_unset_lab_handler)
    parser_lab.add_argument("lab_id", type=str, help="The lab id")
    subparsers_lab = parser_lab.add_subparsers()

    # 'lab_info' command
    parser_lab_info = subparsers_lab.add_parser(
        "info",
        help="Get information about a lab",
        formatter_class=root_parser.formatter_class,
    )
    parser_lab_info.set_defaults(func=lab_info_handler)
    parser_lab_info.add_argument(
        "--json", help="Return JSON result.", action="store_true"
    )

    # 'lab_api' command
    parser_lab_api = subparsers_lab.add_parser(
        "api",
        help="Get API URLs to directly access the lab",
        formatter_class=root_parser.formatter_class,
    )
    parser_lab_api.set_defaults(func=lab_api_handler)
    parser_lab_api.add_argument(
        "--json", help="Return JSON result.", action="store_true"
    )

    # 'lab_stop' command
    parser_lab_stop = subparsers_lab.add_parser(
        "stop", help="Stop a specific lab", formatter_class=root_parser.formatter_class
    )
    parser_lab_stop.set_defaults(func=lab_stop_handler)

    # 'lab_delete_lab' command
    parser_lab_delete_lab = subparsers_lab.add_parser(
        "delete",
        help="Delete lab from its lab id",
        formatter_class=root_parser.formatter_class,
    )
    parser_lab_delete_lab.set_defaults(func=lab_delete_lab_handler)

    # 'lab_resume' command
    parser_lab_resume = subparsers_lab.add_parser(
        "resume",
        help="Resume a specific lab",
        formatter_class=root_parser.formatter_class,
    )
    parser_lab_resume.set_defaults(func=lab_resume_handler)

    # 'lab_topology' command
    parser_lab_topology = subparsers_lab.add_parser(
        "topology",
        help="Get scenario topology on current lab",
        formatter_class=root_parser.formatter_class,
    )
    parser_lab_topology.set_defaults(func=lab_topology_handler)
    parser_lab_topology.add_argument(
        "--json", help="Return JSON result.", action="store_true"
    )

    # 'lab_nodes' command
    parser_lab_nodes = subparsers_lab.add_parser(
        "nodes",
        help="Get scenario nodes on current lab",
        formatter_class=root_parser.formatter_class,
    )
    parser_lab_nodes.set_defaults(func=lab_nodes_handler)
    parser_lab_nodes.add_argument(
        "--json", help="Return JSON result.", action="store_true"
    )

    # 'lab_assets' command
    parser_lab_assets = subparsers_lab.add_parser(
        "assets",
        help="Get scenario assets on current lab",
        formatter_class=root_parser.formatter_class,
    )
    parser_lab_assets.set_defaults(func=lab_assets_handler)
    parser_lab_assets.add_argument(
        "--json", help="Return JSON result.", action="store_true"
    )

    # 'lab_attack_report' command
    parser_lab_attack_report = subparsers_lab.add_parser(
        "attack-report",
        help="Get scenario attack report on current lab",
        formatter_class=root_parser.formatter_class,
    )
    parser_lab_attack_report.set_defaults(func=lab_attack_report_handler)
    parser_lab_attack_report.add_argument(
        "--json", help="Return JSON result.", action="store_true"
    )

    # 'lab_attack_infras' command
    parser_lab_attack_infras = subparsers_lab.add_parser(
        "attack-infras",
        help="Get scenario attack infras on current lab",
        formatter_class=root_parser.formatter_class,
    )
    parser_lab_attack_infras.set_defaults(func=lab_attack_infras_handler)
    parser_lab_attack_infras.add_argument(
        "--json", help="Return JSON result.", action="store_true"
    )

    # 'lab_attack_sessions' command
    parser_lab_attack_sessions = subparsers_lab.add_parser(
        "attack-sessions",
        help="Get scenario attack sessions on current lab",
        formatter_class=root_parser.formatter_class,
    )
    parser_lab_attack_sessions.set_defaults(func=lab_attack_sessions_handler)
    parser_lab_attack_sessions.add_argument(
        "--json", help="Return JSON result.", action="store_true"
    )

    # 'lab_attack_knowledge' command
    parser_lab_attack_knowledge = subparsers_lab.add_parser(
        "attack-knowledge",
        help="Get scenario attack knowledge on current lab",
        formatter_class=root_parser.formatter_class,
    )
    parser_lab_attack_knowledge.set_defaults(func=lab_attack_knowledge_handler)
    parser_lab_attack_knowledge.add_argument(
        "--json", help="Return JSON result.", action="store_true"
    )

    # 'lab_notifications' command
    parser_lab_notifications = subparsers_lab.add_parser(
        "notifications",
        help="Get scenario notifications on current lab",
        formatter_class=root_parser.formatter_class,
    )
    parser_lab_notifications.set_defaults(func=lab_notifications_handler)
    parser_lab_notifications.add_argument(
        "--json", help="Return JSON result.", action="store_true"
    )

    # 'lab_scenario_run_config' command
    parser_lab_scenario_run_config = subparsers_lab.add_parser(
        "scenario-run-config",
        help="Get scenario run config on current lab",
        formatter_class=root_parser.formatter_class,
    )
    parser_lab_scenario_run_config.set_defaults(func=lab_scenario_run_config_handler)
    parser_lab_scenario_run_config.add_argument(
        "--json", help="Return JSON result.", action="store_true"
    )

    # 'lab_get_remote_access' command
    parser_lab_get_remote_access = subparsers_lab.add_parser(
        "get-remote-access",
        help="Get info for remote access to lab VMs",
    )
    parser_lab_get_remote_access.set_defaults(func=lab_get_remote_access_handler)
    parser_lab_get_remote_access.add_argument(
        "--json", help="Return JSON result.", action="store_true"
    )

    parser_lab.set_defaults(func=lambda _: parser_lab.print_help())

    # -------------------
    # --- Redteam actions on labs
    # -------------------

    add_redteam_parser(root_parser=root_parser, subparsers=subparsers_lab)

    # -------------------
    # --- Provisioning actions on labs
    # -------------------

    add_provisioning_parser(root_parser=root_parser, subparsers=subparsers_lab)
