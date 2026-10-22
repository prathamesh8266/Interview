"""Azure and Terraform revision maps for original questions 27–33."""

def get_maps(branch):
    b = branch
    return [
        ('Your Azure architecture story', 'Explain the request, deployment and identity paths using your actual architecture.', [
            b('gap', 'Confirm the real environment', ('Scope & personal contribution', 'Supply the actual application, subscription, regions, resource groups and what you personally implemented or supported. This is an architecture template, not a verified live topology.'), ('Real network and services', 'Confirm the inbound route, AKS networking mode, database service, registry, secret delivery and monitoring. Do not present every example as a component you used.')),
            b('concept', 'Client to ready application', ('Ingress → Service → Pods', 'Explain the actual DNS, gateway or ingress path and how traffic reaches ready application Pods.'), ('AKS and Pod addressing', 'Illustrative node subnet: snet-app-aks. Pod addressing depends on the real AKS networking mode; it may use the node subnet, a separate Pod subnet or an overlay.')),
            b('concept', 'Application to private services', ('Endpoint subnet & private DNS', 'Illustrative Private Link placement: snet-private-endpoints. The endpoint is in the subnet; the PaaS database itself is not a VM placed there. Explain private DNS and the reachable route.'), ('Networking models differ', 'A delegated database subnet is distinct from a Private Link endpoint subnet. Describe the model actually used.')),
            b('concept', 'Images, secrets & identities', ('Registry pull versus app access', 'The kubelet identity normally pulls images. Pod-to-Azure service access can use Entra Workload ID; these are separate identity flows.'), ('Configuration & secret delivery', 'Describe the actual configuration source and Key Vault or other approved secret integration, including permissions and network access.')),
            b('evidence', 'Explain operations', ('Deployment & support evidence', 'Describe real Terraform ownership, state arrangement, application release flow, monitoring, egress and recovery boundaries. Walk through a real request or incident when available.'))
        ]),
        ('AKS to database private endpoint', 'Workload DNS → endpoint and route → TCP/TLS → database identity and permissions → real query.', [
            b('issue', 'Capture the failure', ('Workload-specific evidence', 'Record hostname, port, error, time and affected workloads without logging credentials. Test from the affected Pod or an approved equivalent environment.')),
            b('evidence', 'Resolve the normal hostname', ('Private DNS chain', 'Confirm the supported database hostname resolves to the expected endpoint IP. Check private DNS records, VNet links, CoreDNS, custom forwarding and resolver access.'), ('Azure SQL example', 'server.database.windows.net and privatelink.database.windows.net illustrate the SQL model. Keep the supported hostname for TLS and routing; do not substitute the private IP blindly.')),
            b('cause', 'Endpoint & transport', ('Approval and target', 'Check the endpoint is approved and points to the intended database service and subresource.'), ('Actual network path', 'Inspect source Pod/node network, endpoint subnet, peering, routes, policies, firewalls and applicable NSG/private-endpoint policy settings. Test protocol and required ports, not just ping.')),
            b('cause', 'TLS, identity & database health', ('Reachable does not mean authorized', 'Inspect TLS, credential/token audience, database user mapping, permissions, connection settings, pools and database health. A private AKS API endpoint is separate from the database endpoint.')),
            b('command', 'Collect workload-side evidence', ('Application logs', 'kubectl logs <pod> -n <namespace> -c <container> --tail=100'), ('DNS & TCP checks', 'kubectl exec <pod> -n <namespace> -c <container> -- nslookup <database-fqdn>\nkubectl exec <pod> -n <namespace> -c <container> -- nc -vz -w 5 <database-fqdn> <port>\n\nUse approved diagnostics if these tools are absent. Ports and connection policy are database-specific.')),
            b('resolution', 'Verify the workload query', ('Real operation across replicas', 'Correct the evidenced layer, then verify a real database operation from the application and review logs across affected replicas.'))
        ]),
        ('Environment configuration & isolation', 'Reuse modules, parameterize differences, and isolate state, identity and target scope deliberately.', [
            b('concept', 'Common modules, explicit inputs', ('Real environment differences', 'Parameterize naming, region, sizing, availability, network ranges, endpoints and retention. Avoid independent copies of the whole codebase.')),
            b('concept', 'Separate state & execution scope', ('Inputs are not isolation', '.tfvars changes values; it does not select an independent backend. Child modules normally share the calling root state.'), ('CLI workspaces versus boundaries', 'CLI workspaces provide separate state instances, not separate credentials or IAM boundaries by themselves. Use appropriate roots and backend controls for stronger isolation.')),
            b('evidence', 'Prove the target before apply', ('Tenant, subscription & backend', 'Select the intended root, tenant, subscription, state key, workspace and input set explicitly.'), ('Version & plan review', 'Use compatible pinned modules/providers, review dependency-lock changes and each environment plan. Validate resource group, region and subnet references.')),
            b('solution', 'Separate artifact & runtime config', ('One artifact, environment values', 'Promote the tested application image while reviewing environment configuration independently. Supply secrets through the approved mechanism, not committed variable files.')),
            b('resolution', 'Verify intended behavior', ('Resources and application', 'Confirm the expected infrastructure changes and user flows in the correct environment. A valid plan is not proof of correct target scope.'))
        ]),
        ('Identity, RBAC & Key Vault', 'Identity answers who; RBAC answers what and where; networking determines endpoint reachability.', [
            b('concept', 'Authentication versus authorization', ('Three independent checks', 'Authenticate the intended identity, authorize its operation at the right scope, and establish network/DNS access. A successful login is not proof of permission.')),
            b('concept', 'Managed identity & service principal', ('Azure-managed credential lifecycle', 'A managed identity is represented by a special service principal. System-assigned identity follows its resource lifecycle; user-assigned identity is a separate Azure resource.'), ('Federated pipeline access', 'Supported runners can exchange trusted OIDC tokens without a stored long-lived client secret. Configure issuer, subject, audience and the needed role assignments.')),
            b('cause', 'Control plane versus data plane', ('Deployment rights are not data rights', 'Azure resource deployment permissions do not automatically grant Blob state access or Key Vault secret reading.'), ('Scope to the actual operation', 'Storage Blob Data Contributor on the state container and Key Vault Secrets User address different data operations. Inspect the configured permission model and exact scope.')),
            b('solution', 'Separate deployment & runtime', ('AKS identity roles', 'Separate deployment, kubelet pull and workload identities. Ordinary RBAC registries commonly use AcrPull for image pulling; ABAC-enabled registries need repository permissions such as Container Registry Repository Reader.'), ('Secret consumption', 'Use approved Key Vault access with needed RBAC and private connectivity. Protect retrieved values in the consumer, logs, artifacts and state.')),
            b('resolution', 'Verify the identity path', ('Caller → token → role → endpoint', 'Confirm the actual calling identity, token target, permission scope and network route by testing the required operation without exposing the token or secret.'))
        ]),
        ('State security, locking & drift', 'Protect state as sensitive operational data, serialize writers, and review drift before reconciling it.', [
            b('concept', 'State binds addresses to objects', ('Ownership & metadata', 'State maps Terraform resource addresses to provider object IDs and records planning metadata. Keep one intentional state owner for a remote object.')),
            b('solution', 'Secure state and plans', ('Remote backend & recovery', 'Use restricted access, encryption and recoverable versions or backups. Keep state out of Git. sensitive redacts output but does not remove values from state; saved plans can be sensitive too.'), ('Azure Blob backend', 'AzureRM stores state in a Blob and supports native Blob locking. Entra-backed access needs the runner identity to have the appropriate Blob data permissions, separate from provider deployment rights.')),
            b('cause', 'Lock contention & stale locks', ('Identify the writer', 'Inspect active runs before acting. Locks serialize writers to a state, not all cloud changes or independent states.'), ('Safe contention handling', 'Use a reasonable lock wait. Force-unlock only a confirmed stale lock with no writer; do not routinely disable locking.')),
            b('evidence', 'Investigate drift', ('Normal plan versus refresh-only', 'A normal plan compares desired configuration with refreshed objects. A refresh-only plan reviews differences between remote reality and recorded state. Applying it changes state, not desired code or cloud resources.')),
            b('command', 'Inspect state scope and drift', ('Context, bindings & plans', 'terraform workspace show\nterraform state list\nterraform plan -lock-timeout=5m\nterraform plan -refresh-only\n\nUse the intended backend/root and protect plan output.')),
            b('prevention', 'Migrate deliberately', ('Reconfigure is not migration', 'Protect a recovery copy. init -reconfigure changes local backend setup without copying existing state; init -migrate-state is the distinct reviewed migration operation.'))
        ]),
        ('Why separate Terraform states?', 'Use meaningful lifecycle and ownership boundaries; account for cross-state coordination.', [
            b('gap', 'Supply your actual design', ('Roots, keys & ownership', 'Confirm the real independent roots, owned resources, backend/state keys and your role. This is a design explanation template, not evidence of current deployed infrastructure.'), ('Reason, dependencies & results', 'State why the split was needed, how values flowed between roots and what benefit you actually observed.')),
            b('concept', 'Operational boundaries', ('Lifecycle, access & change rate', 'For example, foundational networking may change less often than application resources. Group by ownership and lifecycle rather than automatically creating one state per resource.')),
            b('solution', 'Benefits of a justified split', ('Scoped changes & owners', 'Smaller plans and independent execution can reduce accidental-change scope and contention when resources and ownership are separated appropriately.')),
            b('cause', 'Tradeoffs and coupling', ('No single dependency graph', 'Coordinate apply/teardown order, stable outputs and concurrent changes. Independent state locks do not provide a global lock.'), ('More operations to maintain', 'Each root adds backend configuration, access, recovery and pipeline orchestration. Over-splitting tightly coupled resources adds work.')),
            b('concept', 'Modules, outputs & access', ('Module reuse is not state isolation', 'A child module normally shares root state. Independent roots own backend/provider setup; children declare requirements and receive provider configurations.'), ('Remote-state reader exposure', 'terraform_remote_state exposes root outputs, but retrieving them requires access to the state snapshot. Consider scoped data lookups or an explicit configuration store.')),
            b('prevention', 'Transfer ownership carefully', ('Avoid competing states', 'Moving an existing object requires a coordinated, reviewed state-ownership transfer with recovery copies and verification. A new key alone can leave the old owner or propose duplicate resources.'))
        ]),
        ('Recover a partially failed apply', 'Inspect cloud and state, reconcile ownership, fix the cause, review a fresh plan, then verify.', [
            b('issue', 'Partial changes remain', ('No automatic rollback', 'Stop competing applies, preserve run evidence and find the first failure. Successful operations may already be recorded and cloud resources may already have changed.')),
            b('evidence', 'Compare state with Azure', ('Confirm target context', 'Check tenant, subscription, root, backend and workspace, then compare resource IDs and real provisioning status with recorded state.'), ('Protected recovery snapshot', 'Preserve state recovery evidence securely before any repair. Overall command failure does not mean every resource operation failed.')),
            b('cause', 'Identify the real blocker', ('Permissions, quota or provider failure', 'Check invalid inputs, dependency conditions, permissions, quota, provider behavior and timeout results. Verify whether a reported timeout left an existing resource.')),
            b('solution', 'Reconcile before retry', ('Import only verified objects', 'If an object exists but its binding is missing, verify its ID and intended address and consider a reviewed import. Then inspect a fresh plan.'), ('State persistence failure', 'Preserve any reported recovery state file securely and restore backend access through the documented process. Do not blindly overwrite state, delete it, unlock an active writer or destroy successful resources.')),
            b('command', 'Inspect context and plan', ('Read the intended scope', 'az account show --query "{subscription:id,tenant:tenantId,name:name}"\nterraform workspace show\nterraform state list\nterraform plan\n\nPlan output can be sensitive; use restricted run logs.')),
            b('resolution', 'Apply reviewed recovery', ('Fresh plan & real health', 'Review proposed creates, replacements and destroys after fixing the cause. Do not reuse the old plan after state/infrastructure changes. Verify resource and application health and review a follow-up plan.'))
        ])
    ]

SOURCES = {
    27: [
        ('AKS networking concepts', 'https://learn.microsoft.com/en-us/azure/aks/concepts-network'),
        ('AKS and Container Registry integration', 'https://learn.microsoft.com/en-us/azure/aks/cluster-container-registry-integration'),
        ('Entra Workload ID for AKS', 'https://learn.microsoft.com/en-us/azure/aks/workload-identity-overview'),
        ('Private Endpoint DNS', 'https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-dns'),
    ],
    28: [
        ('Private Endpoint DNS values', 'https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-dns'),
        ('Azure SQL Private Link connectivity', 'https://learn.microsoft.com/en-us/azure/azure-sql/database/private-endpoint-overview?view=azuresql'),
    ],
    29: [
        ('Terraform configuration style and environments', 'https://developer.hashicorp.com/terraform/language/style'),
        ('CLI workspaces and isolation limits', 'https://developer.hashicorp.com/terraform/cli/workspaces'),
        ('HCP Terraform workspaces', 'https://developer.hashicorp.com/terraform/cloud-docs/workspaces'),
    ],
    30: [
        ('Managed identities', 'https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/overview'),
        ('AKS identity boundaries', 'https://learn.microsoft.com/en-us/azure/aks/operator-best-practices-identity'),
        ('Key Vault data-access roles', 'https://learn.microsoft.com/en-us/azure/key-vault/general/rbac-guide'),
        ('AzureRM backend authentication', 'https://developer.hashicorp.com/terraform/language/backend/azurerm'),
    ],
    31: [
        ('Terraform state purpose', 'https://developer.hashicorp.com/terraform/language/state'),
        ('Sensitive values and state', 'https://developer.hashicorp.com/terraform/language/manage-sensitive-data'),
        ('State locking', 'https://developer.hashicorp.com/terraform/language/state/locking'),
        ('AzureRM state backend', 'https://developer.hashicorp.com/terraform/language/backend/azurerm'),
        ('Refresh-only operation', 'https://developer.hashicorp.com/terraform/tutorials/cloud-get-started/cloud-refresh-only'),
        ('Backend initialization and migration', 'https://developer.hashicorp.com/terraform/cli/commands/init'),
    ],
    32: [
        ('Providers in root and child modules', 'https://developer.hashicorp.com/terraform/language/modules/develop/providers'),
        ('Configuration structure and state boundaries', 'https://developer.hashicorp.com/terraform/language/style'),
        ('Workspace boundaries', 'https://developer.hashicorp.com/terraform/enterprise/workspaces/best-practices'),
        ('Remote-state data access considerations', 'https://developer.hashicorp.com/terraform/language/state/remote-state-data'),
    ],
    33: [
        ('Apply errors and partial completion', 'https://developer.hashicorp.com/terraform/tutorials/cli/apply'),
        ('Importing existing resources', 'https://developer.hashicorp.com/terraform/language/import'),
        ('State locking and force-unlock conditions', 'https://developer.hashicorp.com/terraform/language/state/locking'),
    ],
}
