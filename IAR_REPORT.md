# AI Identity Access Review (IAR) Campaign Ledger

**Campaign Generated:** 2026-11-08 17:37:45  
**Framework Alignment:** ISO/IEC 42001 (A.3.2, A.6.2.2), NIST AI RMF (GOVERN-1.2), Zero Trust NHI  

---

## Executive Attestation Summary

| Agent ID | Display Name | Platform | Accountable Owner | Inherent Risk | Recommended Action |
| :--- | :--- | :--- | :--- | :--- | :--- |
| AGT-001-FIN-RECON | Finance Reconciliation Autonomous Bot | Microsoft Entra ID | `cfo-ops@company.internal` | **HIGH** | `REVOKE` |
| AGT-002-IT-TRIAGE | Tier-1 Helpdesk Triage Copilot | Okta | `it-service-desk@company.internal` | **LOW** | `CERTIFY` |
| AGT-003-DEV-DEPLOYER | CI/CD Auto-Remediation Cloud Agent | AWS IAM | `unassigned-orphan@company.internal` | **HIGH** | `REVOKE` |

---

## Detailed Agent Identity Profiles & Remediation Prompts

### [HIGH] Finance Reconciliation Autonomous Bot (`AGT-001-FIN-RECON`)
- **Platform / Type:** Microsoft Entra ID (ServicePrincipal)
- **Designated Owner:** `cfo-ops@company.internal`
- **Credential Posture:** ClientSecret (Age: 185 days)
- **Autonomous Tool Execution:** Yes (Unrestricted)
- **Human-in-the-Loop (HITL) Gate:** Missing (Direct Execution)
- **Assigned Scopes:** `FinancialRecords.Write.All, Directory.Read.All`
- **Flagged Risk Indicators:**
  - [!] Stale credential > 90 days
  - [!] Unbounded write permissions to financial records without HITL approval

---
### [LOW] Tier-1 Helpdesk Triage Copilot (`AGT-002-IT-TRIAGE`)
- **Platform / Type:** Okta (OAuthClientApp)
- **Designated Owner:** `it-service-desk@company.internal`
- **Credential Posture:** WorkloadIdentityFederation (Age: 14 days)
- **Autonomous Tool Execution:** Restricted / Read-Only
- **Human-in-the-Loop (HITL) Gate:** Enforced
- **Assigned Scopes:** `tickets.read, tickets.comment`
- **Flagged Risk Indicators:**
  - None identified. Compliant posture.

---
### [HIGH] CI/CD Auto-Remediation Cloud Agent (`AGT-003-DEV-DEPLOYER`)
- **Platform / Type:** AWS IAM (IAMRole)
- **Designated Owner:** `unassigned-orphan@company.internal`
- **Credential Posture:** PersistentAccessKey (Age: 420 days)
- **Autonomous Tool Execution:** Yes (Unrestricted)
- **Human-in-the-Loop (HITL) Gate:** Missing (Direct Execution)
- **Assigned Scopes:** `AdministratorAccess`
- **Flagged Risk Indicators:**
  - [!] Orphan account with unassigned human owner
  - [!] Extreme standing privilege (AdministratorAccess)
  - [!] Unrotated access key > 1 year

---
