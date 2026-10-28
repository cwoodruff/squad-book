import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent
M = {
 "concepts/what-is-squad":1,"concepts/your-team":4,"reference/glossary":"C",
 "get-started/installation":2,"get-started/install-comprehensive":2,"features/standalone-install":2,"insider-program":2,"whatsnew":"J",
 "get-started/choosing-your-path":2,"get-started/choose-your-interface":2,"get-started/five-minute-start":2,"features/vscode":2,"guide/shell":2,"sdk-first-mode":2,"guide":2,"guide/personal-squad":2,
 "get-started/first-session":3,"tour-first-session":3,
 "features/team-setup":4,"features/built-in-roles":4,"features/human-team-members":4,"features/preset":4,
 "concepts/architecture":32,"docs/README.md":32,
 "features/routing":5,"features/capability-routing":5,"features/response-modes":5,"features/consult-mode":5,
 "reference/coordinator-restraint":33,
 "concepts/agent-identity-provenance":34,"docs/canary-identity-matrix.md":34,"docs/open-issue-runtime-identity-beacon.md":34,
 "concepts/parallel-work":6,"features/parallel-execution":6,"features/worktrees":6,"features/scratch-dir":6,
 "features/memory":15,"concepts/memory-and-knowledge":15,"docs/_internal/specs/memory-format.md":15,
 "features/tiered-memory":16,"features/reflect":16,"features/context-hygiene":16,"reference/compaction-recovery":16,
 "features/skills":17,"features/skill-security-scanner":17,"features/marketplace":17,
 "features/directives":18,"features/ceremonies":18,"features/reviewer-protocol":18,
 "features/error-recovery":19,
 "concepts/github-workflow":7,"features/github-issues":7,"features/labels":7,"features/issue-templates":7,"features/project-boards":7,"tour-github-issues":7,"scenarios/issue-driven-dev":7,"docs/demo-agentic-sdlc-walkthrough.md":7,
 "features/gitlab-issues":8,"tour-gitlab-issues":8,"features/enterprise-platforms":8,"docs/features/ado-configurable-work-items.md":8,
 "features/ralph":9,"features/loop":9,"docs/features/persistent-ralph.md":9,"docs/features/generic-scheduler.md":9,"docs/features/watch-next-gen.md":9,
 "features/prd-mode":10,"features/streams":10,"features/fleet-dispatch":10,"docs/_internal/specs/streams-prd.md":10,
 "features/copilot-coding-agent":11,"features/remote-control":11,"features/squad-rc":11,
 "features/model-selection":12,"scenarios/switching-models":12,"features/cost-tracking":12,"features/rate-limiting":12,
 "features/notifications":13,"features/notification-level":13,"features/teams-comms":13,"docs/features/teams-adapter.md":13,"docs/migration/teams-async-adapter.md":13,
 "features/cleanup":14,"features/self-upgrade":14,"scenarios/upgrading":14,"get-started/migration":14,
 "features/mcp":22,"features/mcp-frontmatter":22,"features/copilot-mcp-trust":22,
 "features/state-backends":23,"features/storage-provider":23,"features/external-state":23,"reference/state-backend-selection":23,"reference/result-persistence":23,"scenarios/team-state-storage":23,
 "features/cross-squad-discover":24,"docs/features/cross-squad-orchestration.md":24,"features/distributed-mesh":24,"scenarios/multiple-squads":24,
 "concepts/portability":25,"features/export-import":25,"features/upstream-inheritance":25,"scenarios/keep-my-squad":25,"scenarios/team-portability":25,"features/coordinator-as-agent-export":25,
 "features/dual-mode-deployment":28,"scenarios/client-compatibility":26,"scenarios/using-squad-across-clients":26,"docs/_internal/specs/platform-adapter-prd.md":8,
 "features/security-hardening":27,"reference/plugin-security":27,"scenarios/private-repos":27,"scenarios/cross-org-auth":27,"guide/github-auth-setup":27,
 "reference/container-image":28,"scenarios/azure-container-apps":28,"scenarios/aks-deployment":28,"features/keda-scaling":28,"scenarios/multi-codespace":28,
 "scenarios/ci-cd-integration":29,"scenarios/release-process":29,"guide/gh-aw":29,
 "scenarios/aspire-dashboard":30,"scenarios/production-observability":30,
 "scenarios/troubleshooting":31,"scenarios/production-troubleshooting":31,"reference/vscode-troubleshooting":31,"scenarios/disaster-recovery":31,"scenarios/remote-qa":31,
 "scenarios/solo-dev":20,"scenarios/new-project":20,"scenarios/existing-repo":20,"scenarios/mid-project":20,"scenarios/open-source":20,
 "scenarios/large-codebase":21,"scenarios/monorepo":21,"scenarios/scaling-workstreams":21,"scenarios/team-of-humans":21,
 "reference/sdk":35,"reference/api-reference":35,"reference/config":35,
 "features/plugins":36,"guide/building-extensions":36,"guide/extensibility":36,"reference/tools-and-hooks":36,
 "guide/build-autonomous-agent":37,"guide/building-resilient-agents":37,"guide/agent-framework-integration":37,"reference/integration":37,
 "guide/tips-and-tricks":44,"tips-and-tricks":44,"cookbook/recipes":44,"guide/sample-prompts":44,"sample-prompts":44,"guide/faq":44,
 "guide/contributing":46,"guide/contributors":46,"community":46,
 "reference/cli":"A",
}
rows=[]
for line in (HERE / 'sources.txt').read_text().splitlines():
    p=line.strip()
    key = p.replace('docs/src/content/docs/','').removesuffix('.md') if 'content/docs' in p else p
    if p.startswith('docs/specification/'): ch=38
    else: ch=M.get(key,'')
    if isinstance(ch,int): ch = f'vol1:{ch}' if ch <= 21 else f'vol2:{ch-21}'  # M uses the old continuous numbers
    rows.append((p,ch))
with (HERE / 'coverage.csv').open('w',newline='') as f:
    w=csv.writer(f); w.writerow(['source','chapter'])
    w.writerows(rows)
print('unmapped:',[r for r in rows if r[1]==''])
