"""Revision relationships and primary references for original questions 11–18."""

def get_maps(branch):
    b = branch
    return [
        ('CrashLoopBackOff', 'Repeated restarts are a symptom. Use the last termination state and previous logs to find the cause.', [
            b('issue', 'Repeated container restarts', ('Back-off, not a root cause', 'Identify the affected namespace, workload and container. CrashLoopBackOff is not a Pod phase; it describes restart back-off.')),
            b('evidence', 'Inspect the failed instance', ('Events & last state', 'Read restart counts, termination reason and events. Include init containers and select the failing container in a multi-container Pod.'), ('Current & previous logs', 'Current logs can miss the crash. Inspect the previous container instance to recover the error before choosing a fix.')),
            b('cause', 'Test likely causes', ('Startup & configuration', 'Compare image, command, arguments, required configuration and file permissions with the expected runtime.'), ('Resources, probes & dependencies', 'Check OOMKilled, failed startup or liveness probes and dependency errors. Readiness failure alone does not restart a container.')),
            b('command', 'Collect diagnostic evidence', ('Describe the Pod', 'kubectl describe pod <pod> -n <namespace>'), ('Previous container logs', 'kubectl logs <pod> -n <namespace> -c <container> --previous --tail=100')),
            b('solution', 'Fix the evidenced failure', ('Correct or revert safely', 'Use the normal deployment process for the configuration or application fix. For a release regression, check compatibility before restoring a known-good version. Repeated Pod deletion does not remove a persistent cause.')),
            b('resolution', 'Verify stable recovery', ('Restarts, readiness & requests', 'Confirm restart counts stop rising, readiness succeeds and real user requests work. Add the missed validation or test.'))
        ]),
        ('Running but URL unreachable', 'Running does not mean Ready. Trace client → ingress → Service → ready Pod → listener.', [
            b('issue', 'Capture the failed request', ('URL, error & scope', 'Record the URL, timestamp, error and affected users. Check Running separately from Ready.')),
            b('evidence', 'Trace external routing', ('DNS, TLS & ingress', 'Check DNS, certificate, load balancer, controller health, ingress class and host/path rules. An Ingress requires a controller.')),
            b('cause', 'Inspect Service routing', ('Labels & ready endpoints', 'Compare Service selector with Pod labels. EndpointSlices show backend addresses and readiness.'), ('Ports & listener', 'Match Service port and targetPort to the real application listener. containerPort alone neither opens a socket nor exposes an external URL. Avoid a loopback-only listener.')),
            b('command', 'Inspect the request path', ('Service configuration', 'kubectl get service <service> -n <namespace> -o yaml'), ('EndpointSlices', 'kubectl get endpointslices -n <namespace> -l kubernetes.io/service-name=<service>'), ('Ingress events & rules', 'kubectl describe ingress <ingress> -n <namespace>')),
            b('solution', 'Fix the failing hop', ('Compare inside & outside', 'Test Pod and Service access from the cluster, then compare the external path. Check network policies, routing and firewalls where the request stops. Port-forward success does not validate the normal ingress path.')),
            b('resolution', 'Verify the original URL', ('Real user flow', 'Retest the original URL and affected operation after the correction, including readiness and application behavior.'))
        ]),
        ('Pending, pull failures & OOM', 'Separate placement, image startup and runtime memory failure before acting.', [
            b('cause', 'Pending', ('Placement or setup delay', 'Pending is a Pod phase. Inspect scheduling events, capacity, requests, selectors, affinity, taints, tolerations and volume/PVC conditions.')),
            b('cause', 'ImagePullBackOff', ('Image retrieval failed', 'Inspect the exact pull error: image name/digest, availability, registry credentials, node DNS/network/TLS access and platform compatibility. A laptop pull uses a different environment.')),
            b('cause', 'OOMKilled', ('Memory-related termination', 'Inspect last termination state, memory limit, historical usage and node pressure. Exit 137 alone does not establish OOM; node-pressure eviction is a separate condition.')),
            b('command', 'Find the specific blocker', ('Pod & storage events', 'kubectl describe pod <pod> -n <namespace>\nkubectl get pvc -n <namespace>'), ('Resources & node health', 'kubectl describe node <node>\nkubectl top pod <pod> -n <namespace> --containers\n\ntop requires the metrics API; a current sample does not show an earlier memory spike.')),
            b('solution', 'Use the matching fix', ('Placement, pull or memory', 'Correct the actual scheduling/storage constraint; repair the image reference or registry access; or address memory demand, leaks and concurrency. Tune capacity from evidence.')),
            b('resolution', 'Verify the original failure', ('Schedule → start → serve', 'Verify successful placement, image startup and memory stability as appropriate, then check the application flow.'))
        ]),
        ('Readiness, liveness & startup', 'Readiness controls traffic; liveness detects restart-worthy failure; startup protects initialization.', [
            b('concept', 'Readiness', ('Can this instance serve now?', 'Failed readiness marks the Pod not ready and normally excludes it from ready Service backends. The container keeps running; no restart is caused by readiness alone.')),
            b('concept', 'Liveness', ('Would a restart recover it?', 'Repeated failure to the configured threshold causes container termination; restart policy applies. Deployment containers normally restart.')),
            b('concept', 'Startup', ('Has initialization finished?', 'Liveness and readiness wait for startup to succeed. If the startup budget is exhausted, the container is terminated and restart policy applies.')),
            b('solution', 'Design useful checks', ('Timing & endpoint', 'Choose inexpensive, meaningful checks. Tune path, port, timeout, period and thresholds for the real application.'), ('Avoid restart cascades', 'A shared database outage is usually a poor liveness trigger. Restarting all replicas can worsen the incident; use readiness according to what the instance can serve.')),
            b('resolution', 'Test the failure behavior', ('Startup, traffic & restart', 'Test slow initialization, temporary unavailability and a stuck process. Confirm each probe causes the intended behavior.'))
        ]),
        ('Requests, limits & saturation', 'Requests guide scheduling. CPU limits throttle; memory limits can lead to an OOM kill.', [
            b('concept', 'Requests', ('Placement & contention', 'The scheduler accounts for requests when placing Pods. CPU requests also influence relative CPU share under contention. Requests are not a maximum usage cap.')),
            b('concept', 'CPU limit', ('Throttling & latency', 'Demand beyond the CPU time limit is typically throttled. This can slow requests; it does not itself kill the container.')),
            b('concept', 'Memory limit', ('OOM termination', 'Memory enforcement can kill a container when allocations exceed its limit. Restart policy applies. Usage above a request alone is not an automatic kill.')),
            b('evidence', 'Read units & effective values', ('250m CPU, Mi/Gi memory', '250m is one quarter of a CPU; 1000m is one CPU. Mi/Gi are binary memory units. Check namespace defaults and the final Pod configuration.'), ('Trends, not one sample', 'Correlate demand, CPU throttling, latency, memory history, termination reasons and node pressure.')),
            b('solution', 'Size from real behavior', ('Capacity & workload', 'Use measured peaks and load behavior. Increasing a limit may help a capacity constraint but does not cure a leak or create node capacity.')),
            b('resolution', 'Verify under expected load', ('Performance & stability', 'Confirm acceptable latency, stable memory and no unexpected OOM terminations or placement failures at representative demand.'))
        ]),
        ('How Kubernetes objects connect', 'Client → Ingress → Service → ready Pod; Deployment manages Pods and configuration is supplied separately.', [
            b('concept', 'Deployment', ('Manages desired workload', 'Defines a Pod template and replicas; manages ReplicaSets that maintain Pods and support controlled updates.')),
            b('concept', 'Service', ('Stable Pod access', 'A selector-based Service matches Pod labels and routes to backend endpoints described by EndpointSlices. port maps to targetPort; an ordinary ClusterIP is internal.')),
            b('concept', 'Ingress', ('HTTP routing rules', 'Host/path rules send HTTP(S) to Services through an ingress controller. DNS, TLS and controller exposure must also work. Ingress remains supported; Gateway API is the direction for new capabilities.')),
            b('concept', 'ConfigMap & Secret', ('Runtime configuration', 'ConfigMaps carry non-sensitive values; Secrets carry sensitive values. Consume them as environment variables or mounted files.'), ('Secret handling', 'Base64 is not encryption. Restrict access, protect storage and avoid exposing credentials.')),
            b('cause', 'Configuration not refreshed', ('Environment versus files', 'Existing process environment variables do not automatically refresh. Mounted configuration may update eventually but needs application reload; subPath mounts have update limitations.')),
            b('solution', 'Align the connections', ('Labels, ports & references', 'Verify Deployment labels, Service selectors, ports, ingress backend, namespace and configuration references. Plan a rollout or supported reload when configuration changes.'))
        ]),
        ('Rolling update & rollback', 'Watch workload health and real user behavior. Undo restores a Pod template, not the entire environment.', [
            b('evidence', 'Prepare the rollout', ('Artifact & compatibility', 'Confirm context and namespace, reviewed change, image digest, available capacity, readiness, and database/configuration compatibility.')),
            b('concept', 'RollingUpdate controls', ('maxSurge', 'Bounds extra Pods above desired replicas during rollout. Extra replicas require capacity.'), ('maxUnavailable', 'Bounds allowed unavailability during transition. A setting of 0 does not alone guarantee zero failed requests.')),
            b('command', 'Track the rollout', ('Status & history', 'kubectl rollout status deployment/<deployment> -n <namespace> --timeout=120s\nkubectl rollout history deployment/<deployment> -n <namespace>')),
            b('solution', 'Restore a known-good revision', ('Rollback decision', 'Significant impact tied to the release and no quick safe fix can support rollback. Inspect retained revisions and compatibility first.'), ('Undo & its limits', 'kubectl rollout undo deployment/<deployment> -n <namespace> --to-revision=<revision>\n\nUndo changes the Deployment Pod template. It does not undo database migrations or separately modified ConfigMaps/Secrets. Coordinate GitOps desired state.')),
            b('resolution', 'Verify rollout or recovery', ('Readiness & user outcomes', 'Watch Pods, events and rollout status; then test affected user flows, errors, latency and dependencies.')),
            b('prevention', 'Define failure handling', ('No automatic deadline rollback', 'A Deployment progress deadline reports a stalled rollout; the controller does not automatically roll it back. Define the release process and compatibility plan.'))
        ]),
        ('Works in Docker, fails in K8s', 'Compare the same image plus effective configuration, network, storage, security and resource settings.', [
            b('evidence', 'Match the artifact & symptom', ('Digest, platform & failure stage', 'Compare the image digest and supported platform. Inspect events and logs to distinguish image pull, startup, traffic or later application failure.')),
            b('cause', 'Configuration & storage differ', ('Runtime values & mounts', 'Compare local environment and bind mounts with ConfigMap/Secret references, volumes and mounted paths.'), ('Command & arguments', 'Compare working directory and startup overrides. Kubernetes command/args can replace the image startup defaults.')),
            b('cause', 'Network assumptions differ', ('localhost & exposure', 'localhost inside a Pod refers to that Pod, not your laptop or another Pod. Docker port publishing does not create Kubernetes Services or Ingress.'), ('Actual cluster path', 'Check listener interface, targetPort, cluster DNS, policy and dependency access from the failing environment.')),
            b('cause', 'Execution constraints differ', ('Identity & filesystem', 'Compare runtime UID, file permissions, read-only filesystem, security context and service-account permissions.'), ('Resources & probes', 'Check requests/limits and startup, readiness and liveness settings. Local unrestricted execution can hide cluster failures.')),
            b('solution', 'Reproduce the difference', ('Comparable runtime settings', 'Use the same artifact with the relevant constraints, fix the evidenced mismatch and update the controlled deployment.')),
            b('resolution', 'Verify environment parity', ('Real cluster workload', 'Retest the original URL and operation, then improve parity and release checks so local success predicts cluster behavior more reliably.'))
        ])
    ]

SOURCES = {
    11: [
        ('Pod lifecycle and container restarts', 'https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/'),
        ('Debug running Pods and previous logs', 'https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/'),
    ],
    12: [
        ('Debug Services', 'https://kubernetes.io/docs/tasks/debug/debug-application/debug-service/'),
        ('Ingress routing and controllers', 'https://kubernetes.io/docs/concepts/services-networking/ingress/'),
    ],
    13: [
        ('Debug Pods', 'https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/'),
        ('Images and ImagePullBackOff', 'https://kubernetes.io/docs/concepts/containers/images/'),
        ('Resource management', 'https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/'),
    ],
    14: [
        ('Probe concepts', 'https://kubernetes.io/docs/concepts/workloads/pods/probes/'),
        ('Configure probes and thresholds', 'https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/'),
    ],
    15: [('CPU and memory requests and limits', 'https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/')],
    16: [
        ('Deployments', 'https://kubernetes.io/docs/concepts/workloads/controllers/deployment/'),
        ('Services', 'https://kubernetes.io/docs/concepts/services-networking/service/'),
        ('Ingress', 'https://kubernetes.io/docs/concepts/services-networking/ingress/'),
        ('ConfigMaps and updates', 'https://kubernetes.io/docs/concepts/configuration/configmap/'),
        ('Good practices for Secrets', 'https://kubernetes.io/docs/concepts/security/secrets-good-practices/'),
    ],
    17: [('Deployment updates, history and rollback', 'https://kubernetes.io/docs/concepts/workloads/controllers/deployment/')],
    18: [
        ('Docker port publishing', 'https://docs.docker.com/get-started/docker-concepts/running-containers/publishing-ports/'),
        ('Docker bind mounts', 'https://docs.docker.com/engine/storage/bind-mounts/'),
        ('Kubernetes security contexts', 'https://kubernetes.io/docs/tasks/configure-pod-container/security-context/'),
        ('Container command and arguments', 'https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/'),
    ],
}
