"""
Copyright 2023-2023 VMware Inc.
SPDX-License-Identifier: Apache-2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import click
import hcs_cli.service.admin as admin
import hcs_core.sglib.cli_options as cli
from hcs_core.ctxp import recent, util
import hcs_core.ctxp.cli_options as common_options
from hcs_core.util import duration


def _colorize(data: dict, name: str, mapping: dict):
    s = data[name]
    c = mapping.get(s)
    if c:
        if isinstance(c, str):
            data[name] = click.style(s, fg=c)
        else:
            color = c(data)
            data[name] = click.style(s, fg=color)


def _format_vm_table(data):
    for d in data:
        updatedAt = d["updatedAt"]
        d["stale"] = duration.stale(updatedAt)

        _colorize(
            d,
            "lifecycleStatus",
            {
                "DELETING": "bright_black",
                "ERROR": "red",
                "PROVISIONING": "blue",
                "PROVISIONED": "green",
                "MAINTENANCE": "yellow",
            },
        )

        _colorize(
            d,
            "powerState",
            {
                "PoweredOn": "green",
                "PoweringOn": "blue",
                "PoweredOff": "bright_black",
                "PoweringOff": "blue",
            },
        )

        _colorize(
            d,
            "agentStatus",
            {"AVAILABLE": "green", "ERROR": lambda d: "bright_black" if d["powerState"] != "PoweredOn" else "red"},
        )

        _colorize(
            d,
            "sessionPlacementStatus",
            {
                "AVAILABLE": "green",
                "UNAVAILABLE": lambda d: "bright_black" if d["powerState"] != "PoweredOn" else "red",
                "QUIESCING": "blue",
            },
        )

    fields_mapping = {}
    if data and "templateId" in data[0]:
        fields_mapping = {"templateId": "Template", "templateType": "Type"}

    fields_mapping |= {
        "id": "Id",
        "lifecycleStatus": "Status",
        "stale": "Stale",
        "powerState": "Power",
        "agentStatus": "Agent",
        "haiAgentVersion": "Agent Version",
        "sessionPlacementStatus": "Session",
        "vmFreeSessions": "Free Session",
    }
    return util.format_table(data, fields_mapping)


@click.command()
@click.argument("template-id", type=str, required=False)
@cli.org_id
@common_options.limit
@common_options.sort
@cli.formatter(_format_vm_table)
def list(template_id: str, org: str, **kwargs):
    """List template VMs"""
    org_id = cli.get_org_id(org)

    ret = []
    if template_id and template_id.lower() == "all":
        templates = admin.template.list(org_id=org_id, limit=2000)
        for t in templates:
            tid = t["id"]
            vms = admin.VM.list(tid, org_id=org_id, **kwargs)
            if vms:
                for v in vms:
                    v["templateId"] = tid
                    v["templateType"] = t["templateType"]
                ret += vms
    else:
        template_id = recent.require(template_id, "template")
        ret = admin.VM.list(template_id, org_id=org_id, **kwargs)
        recent.helper.default_list(ret, "vm")
    return ret
