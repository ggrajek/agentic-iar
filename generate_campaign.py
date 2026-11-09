import json
import csv
from datetime import datetime

def assess_risk_tier(agent):
    critical_triggers = 0
    if agent.get("credential_age_days", 0) > 90:
        critical_triggers += 1
    if any("write" in s.lower() or "admin" in s.lower() for s in agent.get("assigned_scopes", [])):
        critical_triggers += 1
    if agent.get("autonomous_execution", False) and not agent.get("human_in_the_loop_required", True):
        critical_triggers += 1
    if "unassigned" in agent.get("owner_email", "").lower() or "orphan" in agent.get("owner_email", "").lower():
        critical_triggers += 2

    if critical_triggers >= 3:
        return "HIGH"
    elif critical_triggers >= 1:
        return "MEDIUM"
    return "LOW"

def generate_access_review(inventory_file="agent_identities.json", output_csv="iar_campaign_2026_q4.csv", output_md="IAR_REPORT.md"):
    with open(inventory_file, "r") as f:
        agents = json.load(f)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. Generate CSV Campaign Ledger (Ready for manual or automated auditor sign-off)
    csv_headers = [
        "Agent ID", "Display Name", "Platform", "Owner Email", "Risk Level",
        "Assigned Scopes", "Credential Age (Days)", "HITL Required",
        "Audit Status", "Reviewer Decision", "Sign-Off Timestamp", "Reviewer Notes"
    ]

    csv_rows = []
    for agent in agents:
        risk_level = assess_risk_tier(agent)
        # Suggested initial decision
        suggested_decision = "REVOKE" if risk_level == "HIGH" else ("CERTIFY" if risk_level == "LOW" else "REVIEW_REQUIRED")
        
        csv_rows.append({
            "Agent ID": agent["agent_id"],
            "Display Name": agent["display_name"],
            "Platform": agent["platform"],
            "Owner Email": agent["owner_email"],
            "Risk Level": risk_level,
            "Assigned Scopes": " | ".join(agent["assigned_scopes"]),
            "Credential Age (Days)": agent["credential_age_days"],
            "HITL Required": agent["human_in_the_loop_required"],
            "Audit Status": "PENDING_ATTESTATION",
            "Reviewer Decision": suggested_decision,
            "Sign-Off Timestamp": "",
            "Reviewer Notes": ""
        })

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=csv_headers)
        writer.writeheader()
        writer.writerows(csv_rows)

    # 2. Generate Executive Markdown Attestation Dossier
    md_content = f"""# AI Identity Access Review (IAR) Campaign Ledger

**Campaign Generated:** {timestamp}  
**Framework Alignment:** ISO/IEC 42001 (A.3.2, A.6.2.2), NIST AI RMF (GOVERN-1.2), Zero Trust NHI  

---

## Executive Attestation Summary

| Agent ID | Display Name | Platform | Accountable Owner | Inherent Risk | Recommended Action |
| :--- | :--- | :--- | :--- | :--- | :--- |
"""
    for row in csv_rows:
        badge = f"**{row['Risk Level']}**"
        action = f"`{row['Reviewer Decision']}`"
        md_content += f"| {row['Agent ID']} | {row['Display Name']} | {row['Platform']} | `{row['Owner Email']}` | {badge} | {action} |\n"

    md_content += """
---

## Detailed Agent Identity Profiles & Remediation Prompts

"""
    for agent in agents:
        risk = assess_risk_tier(agent)
        md_content += f"""### [{risk}] {agent['display_name']} (`{agent['agent_id']}`)
- **Platform / Type:** {agent['platform']} ({agent['identity_type']})
- **Designated Owner:** `{agent['owner_email']}`
- **Credential Posture:** {agent['credential_type']} (Age: {agent['credential_age_days']} days)
- **Autonomous Tool Execution:** {'Yes (Unrestricted)' if agent['autonomous_execution'] else 'Restricted / Read-Only'}
- **Human-in-the-Loop (HITL) Gate:** {'Enforced' if agent['human_in_the_loop_required'] else 'Missing (Direct Execution)'}
- **Assigned Scopes:** `{', '.join(agent['assigned_scopes'])}`
- **Flagged Risk Indicators:**
"""
        if agent["risk_indicators"]:
            for ind in agent["risk_indicators"]:
                md_content += f"  - [!] {ind}\n"
        else:
            md_content += "  - None identified. Compliant posture.\n"

        md_content += "\n---\n"

    with open(output_md, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"[+] Successfully generated CSV Ledger: {output_csv}")
    print(f"[+] Successfully generated Attestation Dossier: {output_md}")

if __name__ == "__main__":
    generate_access_review()