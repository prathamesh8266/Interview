"""Revision maps and primary references for original questions 19–26."""

def get_maps(branch):
    b = branch
    return [
        ('Your end-to-end CI/CD story', 'Explain a real pipeline: problem → flow → personal contribution → verified outcome.', [
            b('gap', 'Start with actual experience', ('Project & platform', 'Identify the real application, original problem and CI/CD tool you used. This is an experience template, not a claim that you implemented Jenkins.'), ('Personal ownership', 'Separate your implementation and troubleshooting work from team responsibilities. Supply a factual result; use numbers only when supported.')),
            b('concept', 'Commit to tested artifact', ('Trigger & source revision', 'Describe the actual reviewed branch, trigger and checked-out revision.'), ('Tests, build & traceability', 'Name the real checks and artifact. Explain how commit, build and artifact version or digest were recorded.')),
            b('concept', 'Artifact to environments', ('Configuration & secrets', 'Explain the actual environment-specific configuration and approved credential handling.'), ('Promotion & authorization', 'Describe the real test environments, validation, production gate and deployment strategy.')),
            b('resolution', 'Verification & recovery', ('Actual validation', 'Supply the real smoke tests, user flows and monitoring used to validate the release.'), ('Recovery procedure', 'Describe the known-good artifact or forward-fix process and compatibility checks that actually existed.')),
            b('prevention', 'Result & lesson', ('Evidence-backed outcome', 'State what improved and one lesson learned. If your implementation used another platform, explain it honestly and map the concepts to Jenkins when asked.'))
        ]),
        ('Design a Jenkins delivery pipeline', 'Test → build once → scan → publish → deploy the verified digest → verify user behavior.', [
            b('concept', 'Pipeline as code', ('Reviewed Jenkinsfile & agent', 'Version the Jenkinsfile and select a trusted agent with the required tools. Define timeouts, result handling and environment concurrency controls.')),
            b('evidence', 'Checkout & tests', ('Validate the triggering revision', 'Check out the intended commit and locked dependencies. Run project checks, retain test reports and block deployment on failed or disallowed unstable results.')),
            b('solution', 'Build, scan & publish', ('Build the artifact once', 'Create a traceable image and scan it. Use the agreed security gate; scanner execution errors are not clean scans.'), ('Publish the tested image', 'Authenticate with narrowly scoped credentials, push the artifact and record its registry digest.')),
            b('command', 'Illustrative toolchain', ('Build & vulnerability gate', 'docker build -t <registry>/<repository>:<release-id> .\ntrivy image --exit-code 1 --severity HIGH,CRITICAL <registry>/<repository>:<release-id>\n\nAdapt severity policy and tooling to the project; these commands are examples.'), ('Push & watch rollout', 'docker push <registry>/<repository>:<release-id>\nkubectl rollout status deployment/<deployment> -n <namespace> --timeout=120s\n\nLogin, digest capture and the reviewed deployment manifest are separate required steps.')),
            b('solution', 'Promote & deploy', ('Environment gates', 'Deploy by digest through required non-production validation and the approved production gate. Supply target configuration and credentials separately; serialize competing changes to the environment.')),
            b('resolution', 'Verify or recover', ('Beyond a green pipeline', 'Test user flows, rollout status, errors and latency. Use an explicit recovery plan with schema/data compatibility checks. Preserve reports, clean up and notify owners.'))
        ]),
        ('Jenkins building blocks', 'Controller coordinates; agents execute; stages organize; Jenkinsfile defines the flow.', [
            b('concept', 'Controller', ('Coordinates Jenkins', 'Maintains configuration and jobs, schedules work and presents results. Avoid normal application builds on the built-in node because of controller filesystem access.')),
            b('concept', 'Agent & executor', ('Workspace and tools', 'An agent supplies the execution environment. Labels select a suitable OS/toolchain; executors are work slots, with resource and isolation implications.')),
            b('concept', 'Stage & step', ('Organize versus execute', 'Stages group work such as Test, Build and Deploy. Steps perform operations within them. Stages can include parallel branches where appropriate.')),
            b('concept', 'Jenkinsfile', ('Versioned pipeline definition', 'Reviewed text in source control defines the pipeline. Jenkins supports Declarative and Scripted syntax.'), ('Declarative structure', 'agent, stages and steps describe execution; environment, options and post configure context and result handling. The pipeline invokes the project tools rather than replacing them.')),
            b('prevention', 'Separation of responsibilities', ('Reliable execution environments', 'Choose agents deliberately, maintain tool dependencies and isolate workloads according to their trust and credential needs.'))
        ]),
        ('Credentials without log leakage', 'Scope and isolate secrets. Log masking is not a security boundary.', [
            b('solution', 'Store & scope credentials', ('Credential IDs, not literals', 'Use the appropriate Jenkins store or approved secret-manager integration. Reference IDs, restrict access and separate environment permissions.'), ('Bind only when needed', 'Use a narrow withCredentials scope. Keep credentials out of source control, generated reports and archived artifacts.')),
            b('cause', 'How secrets leak', ('Interpolation & tracing', 'Avoid Groovy interpolation of secrets into shell steps; let the shell expand bound variables. Disable tracing and avoid printing the environment or verbose requests.'), ('Masking has limits', 'Transformed values, tool output, files or malicious build code can bypass masking. Other processes in a shared execution environment may read secrets.')),
            b('command', 'Safe login pattern', ('Password via stdin', 'Inside a scoped credential binding on a Unix-like agent:\nset +x\nprintf \'%s\' "$REGISTRY_PASSWORD" | docker login "$REGISTRY" --username "$REGISTRY_USER" --password-stdin\n\nUse a single-quoted Groovy shell script; configure REGISTRY separately and isolate/clean up login state.')),
            b('prevention', 'Protect execution & lifecycle', ('Trusted jobs and agents', 'Keep untrusted pull requests away from production secrets. Use appropriate agent isolation and handle secret files outside browsable workspace paths.'), ('Rotate & respond', 'Review access, rotate credentials and revoke suspected leaks. Masked console output alone does not demonstrate confidentiality.')),
            b('resolution', 'Review all outputs', ('Logs, files & reports', 'Verify commands and tooling do not expose secrets through logs, workspace files, reports or artifacts. Check the binding scope and actual account permissions.'))
        ]),
        ('Pipeline fails with unchanged code', 'The application commit is only one input. Compare the entire execution context.', [
            b('issue', 'Locate the first failure', ('Queued or executing?', 'Identify the first failed stage and exact error. Distinguish an unavailable agent from a step that actually ran and failed.')),
            b('evidence', 'Compare with last success', ('Complete input set', 'Compare commit, Jenkinsfile revision, submodules, shared libraries, parameters, agent, OS, tool versions, image digests, plugins and configuration.'), ('Workspace & resources', 'Inspect workspace state, disk, memory and capacity. Preserve focused evidence without printing secrets.')),
            b('cause', 'External changes', ('Access & dependencies', 'Check repositories, registries, DNS/TLS/network, expired credentials, permissions, rate limits and target-environment health.'), ('New security finding', 'An updated vulnerability database may legitimately block the same image. Investigate the finding rather than bypassing the gate.')),
            b('solution', 'Reproduce & fix the cause', ('Controlled comparison', 'Use known inputs or a clean controlled workspace, changing one variable at a time where possible.'), ('Bounded, appropriate retry', 'Retry a transient operation only when safe. Repeated deployment or migration attempts can duplicate side effects.')),
            b('resolution', 'Verify repaired behavior', ('Stages & application outcome', 'Verify the relevant build stages and deployed behavior after the correction.')),
            b('prevention', 'Make inputs reproducible', ('Pin & record', 'Use locked dependencies and pinned tool/image versions where appropriate. Retain build metadata so the next failure can be compared with evidence.'))
        ]),
        ('Promote one application version', 'Build once and promote a verified artifact; keep environment configuration separate.', [
            b('concept', 'Immutable artifact identity', ('Commit versus digest', 'The same commit can rebuild to different bytes. Record and deploy the container digest; a mutable tag such as latest is insufficient identity.')),
            b('solution', 'Environment configuration', ('One image, different settings', 'Supply endpoints, resources and feature configuration outside the image, using the approved mechanism for secrets. Do not build production credentials into the artifact.')),
            b('evidence', 'Promotion evidence', ('Tests, policy & authorization', 'Check the required functional, security and environment validation plus the agreed production release gate.'), ('Trace the deployed state', 'Record commit, build, image digest, configuration revision and promotion evidence.')),
            b('cause', 'Registry & data pitfalls', ('Copy is not proof', 'Verify the destination manifest identity when moving artifacts between registries. A destination tag alone does not establish identical content.'), ('Schema compatibility', 'Database changes are part of release planning; image rollback does not undo data changes.')),
            b('resolution', 'Verify each promotion', ('User flow & recovery artifact', 'Check real behavior in each environment and retain the prior approved image and compatible configuration for recovery.'))
        ]),
        ('Merge, rebase, revert & reset', 'For a normal undo on a shared branch, prefer a reviewed revert commit.', [
            b('concept', 'Merge', ('Integrate histories', 'Merge may fast-forward or create a merge commit. Integrating the branch does not by itself rewrite its existing commits.')),
            b('concept', 'Rebase', ('Replay onto a new base', 'Reapplies commits and typically creates new commit IDs. Coordinate before rewriting history that others depend on.')),
            b('solution', 'Revert on shared history', ('New undo commit', 'Revert reverses a selected commit through a new commit while preserving history. Review and test it; conflicts are possible.'), ('Merge commits need care', 'Reverting a merge requires a deliberate mainline-parent choice and affects later merge behavior. Inspect the history first.')),
            b('concept', 'Reset', ('Commit-form behavior', 'Moves the current branch: --soft keeps index/worktree changes; --mixed resets the index; --hard also resets tracked working-tree content and can discard local work.'), ('Path-form distinction', 'Path-based reset updates selected index entries without moving the branch. Do not confuse it with resetting branch history.')),
            b('command', 'Inspect before undo', ('History & candidate change', 'git status\ngit log --oneline --graph -n 12\ngit show <commit>'), ('Shared-branch undo cue', 'git revert <commit>\n\nThis changes files and normally creates a commit. Review and test through the team workflow; this is not an instruction to execute it now.')),
            b('resolution', 'Source undo versus rollback', ('Verify the deployed result', 'A revert changes source history. Production behavior changes through the release process; operational rollback and database compatibility are separate considerations.'))
        ]),
        ('Rolling, blue-green & canary', 'Choose how to replace instances, switch environments or limit real-user exposure.', [
            b('concept', 'Rolling update', ('Replace instances gradually', 'Old and new versions coexist. Useful for compatible changes with controlled availability and moderate extra capacity; readiness and compatibility matter.')),
            b('concept', 'Blue-green', ('Validate then switch routing', 'Run current and new environments side by side. Validate the new version, switch routing and retain the old one for the recovery window. Budget duplicate capacity.')),
            b('concept', 'Canary', ('Limit exposure, then expand', 'Send a controlled subset or cohort to the new version. Promote only when version-specific health criteria pass; define stop conditions.')),
            b('evidence', 'Choose by constraints', ('Risk, capacity & visibility', 'Compare blast radius, capacity, representative traffic, routing control, observability and recovery needs.'), ('Routing precision', 'Pod replica ratios behind one Service do not guarantee a precise request percentage. Use suitable routing when controlled exposure matters.')),
            b('cause', 'Shared-state recovery risks', ('Traffic reversal is not data undo', 'Database writes, background workers, sessions and connections need a compatibility and recovery plan. Switching traffic back does not reverse data changes.')),
            b('resolution', 'Verify rollout & recovery', ('Health model and stop criteria', 'Monitor errors, latency and meaningful business behavior. Verify rollback or traffic reversal; no strategy automatically guarantees zero downtime.'))
        ])
    ]

SOURCES = {
    19: [('Pipeline as code and delivery flow', 'https://www.jenkins.io/doc/book/pipeline/jenkinsfile/')],
    20: [
        ('Jenkins pipeline syntax and result handling', 'https://www.jenkins.io/doc/book/pipeline/syntax/'),
        ('Trivy image scan options', 'https://trivy.dev/docs/dev/references/configuration/cli/trivy_image/'),
        ('Kubernetes image digests', 'https://kubernetes.io/docs/concepts/containers/images/'),
        ('Kubernetes rollout verification', 'https://kubernetes.io/docs/concepts/workloads/controllers/deployment/'),
    ],
    21: [
        ('Jenkins Pipeline and Jenkinsfile', 'https://www.jenkins.io/doc/book/pipeline/'),
        ('Controller isolation', 'https://www.jenkins.io/doc/book/security/controller-isolation/'),
        ('Jenkins glossary', 'https://www.jenkins.io/doc/book/glossary/'),
    ],
    22: [
        ('Using credentials', 'https://www.jenkins.io/doc/book/using/using-credentials/'),
        ('Credentials binding and masking limitations', 'https://www.jenkins.io/doc/pipeline/steps/credentials-binding/'),
        ('Docker login and password-stdin', 'https://docs.docker.com/reference/cli/docker/login/'),
    ],
    23: [
        ('Jenkins Pipeline tools and environment', 'https://www.jenkins.io/doc/book/pipeline/jenkinsfile/'),
        ('Pipeline timeouts and controls', 'https://www.jenkins.io/doc/book/pipeline/syntax/'),
        ('Trivy vulnerability database behavior', 'https://trivy.dev/docs/latest/scanner/vulnerability/'),
    ],
    24: [
        ('Image digests and identity', 'https://kubernetes.io/docs/concepts/containers/images/'),
        ('CI/CD and release strategies', 'https://learn.microsoft.com/azure/architecture/microservices/ci-cd'),
    ],
    25: [
        ('git merge', 'https://git-scm.com/docs/git-merge'),
        ('git rebase', 'https://git-scm.com/docs/git-rebase'),
        ('git revert', 'https://git-scm.com/docs/git-revert'),
        ('git reset', 'https://git-scm.com/docs/git-reset'),
    ],
    26: [
        ('Kubernetes rolling updates', 'https://kubernetes.io/docs/concepts/workloads/controllers/deployment/'),
        ('Blue-green and canary comparison', 'https://learn.microsoft.com/azure/architecture/microservices/ci-cd'),
        ('Kubernetes canary example', 'https://kubernetes.io/docs/tutorials/stateless-application/canary-deployment/'),
    ],
}
