"""Graph summaries of the user's exact Section 5 answers.txt source."""
from pathlib import Path
import re

SOURCE_FILE = 'Python Linux Networkig and Monitoring/answers.txt'


def get_maps(branch):
    b = branch
    source = (Path(__file__).resolve().parent.parent / SOURCE_FILE).read_text(encoding='utf-8').replace('\r\n', '\n')
    parts = re.split(r'\nQUESTION (\d+)\n', source)
    questions = {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}

    def example(number, start, end):
        return questions[number].split(start, 1)[1].split(end, 1)[0].strip()

    health_code = example(34, 'EXAMPLE SCRIPT\n\n', '\n\nEXPLAIN THE CODE')
    log_code = example(36, 'EXAMPLE SCRIPT\n\n', '\n\nSAMPLE INPUT LINE')
    retry_code = example(37, 'ILLUSTRATIVE RETRY HELPER\n\n', '\n\nThe operation must classify')
    practice = example(40, 'FINAL PRACTICE CHECK\n\n', '\n\nLINK TO YOUR EXPERIENCE')
    diagnostic_blocks = [
        ('CPU & processes', example(35, 'CPU AND PROCESSES\n\n', '\n\nMEMORY AND SWAP')),
        ('Memory & swap', example(35, 'MEMORY AND SWAP\n\n', '\n\nDISK SPACE AND INODES')),
        ('Disk space & inodes', example(35, 'DISK SPACE AND INODES\n\n', '\n\nDISK I/O AND ERROR EVIDENCE')),
        ('Disk I/O & logs', example(35, 'DISK I/O AND ERROR EVIDENCE\n\n', '\n\nSome tools require')),
    ]
    diagnostic_review = example(35, 'AFTER THE CHECKS\n\n', '\n\nKEY POINT TO REMEMBER')

    return [
        ('Python endpoint health checks', 'Use timeouts, meaningful health criteria, per-endpoint errors and a useful exit status.', [
            b('concept', 'Define the check result', ('Name, health & duration', 'Accept an endpoint name, URL and timeout; return a structured result with status, health and elapsed duration measured with time.monotonic.')),
            b('cause', 'Distinguish failure modes', ('HTTP versus network error', 'Catch HTTPError before URLError because it is a subclass. Preserve the HTTP status; classify network, DNS, TLS and timeout failures without printing sensitive URLs.'), ('A 2xx may not prove readiness', 'Define health per endpoint, including content where needed. The supplied urllib example follows redirects; a login redirect can conceal a failed check unless final-URL/redirect and response policies are added.')),
            b('code', 'Read the supplied Python example', ('Complete health-check script', health_code)),
            b('resolution', 'Report failures clearly', ('Continue checks & set exit code', 'Handle exceptions per endpoint so one failure does not skip others. Report JSON results and exit nonzero if any endpoint is unhealthy. Successful responses are closed by the context manager.')),
            b('prevention', 'Bound the monitor', ('Timeout & concurrency limits', 'The example is sequential. More endpoints can use bounded I/O threads. Its timeout is not a strict end-to-end program deadline.'), ('Recurring alert behavior', 'For a recurring monitor, consider repeated-failure thresholds, deduplication and recovery notifications; these are additions, not implemented in the example.'))
        ]),
        ('Linux CPU, memory & disk pressure', 'Distinguish utilization from pressure and verify the bottleneck before mitigating it.', [
            b('issue', 'Confirm host & application impact', ('Time, baseline & changes', 'Identify the affected host and start time. Compare normal behavior with traffic, jobs, configuration and deployment changes before restarting anything.')),
            b('evidence', 'High CPU', ('Processes, threads & CPU time', 'Identify busy processes and threads. Compare user, kernel and I/O-related activity, runnable work and application traffic. Load average is not CPU utilization; it includes uninterruptible tasks.'), ('Application and container context', 'Investigate expensive code paths, loops, concurrency, garbage collection and jobs. Check container CPU throttling even when host CPU does not look saturated.')),
            b('evidence', 'High memory', ('Available memory & swap', 'Low free memory alone is not proof of pressure because Linux uses cache. Inspect available memory, sustained swap, process RSS, OOM events and application impact.'), ('Trend versus spike', 'Continuous growth can support a leak hypothesis. Spikes may correlate with input size or concurrency; use historical evidence.')),
            b('evidence', 'Full disk', ('Space versus inodes', 'Find the affected filesystem. Inspect capacity, inode usage, scoped directory sizes, logs, temporary files and application output.'), ('Deleted but still open', 'A file removed from directory listings can keep using space while a process holds it open. Investigate this when df and visible file sizes disagree.')),
            b('command', 'Annotated diagnostic commands', *diagnostic_blocks),
            b('solution', 'Recover using evidence', ('Target the actual pressure', 'Fix expensive work or add justified capacity; rotate or remove approved disposable files. Do not blindly delete database files, persistent storage or active logs.')),
            b('resolution', 'Verify and prevent recurrence', ('Application and resource recovery', 'Verify application behavior and the resource trend after mitigation. Address retention, sizing or application-code causes.'), ('After-checks review', diagnostic_review))
        ]),
        ('Python log error aggregation', 'Stream records, validate input, normalize time and report malformed data.', [
            b('concept', 'Define the log contract', ('JSON lines & grouping', 'The supplied script expects timestamp, level and error_type fields in JSON objects, one per line. It counts ERROR records by error type and UTC minute.')),
            b('solution', 'Process and validate records', ('Stream the file', 'Read one line at a time, skip blank lines and parse each JSON object. Check ERROR level, timestamp type and error category.'), ('Normalize timestamp buckets', 'Accept an explicit timezone, convert to UTC and truncate to the minute. Missing timezone information is rejected rather than guessed.')),
            b('code', 'Read the supplied Python example', ('Complete log-summary script', log_code)),
            b('evidence', 'Interpret the output', ('Counts and malformed records', 'Return the Counter and invalid-record count; print sorted minute/category counts. File-open and permission errors should fail clearly, not become an empty log.')),
            b('prevention', 'Control memory and sensitive data', ('Aggregation cardinality', 'Streaming bounds input buffering, but Counter memory still grows with distinct groups. Limit the analysis window or use an external aggregator for very large group sets.'), ('Stable error categories', 'Avoid grouping by every request ID, user ID or raw message. Keep sensitive payloads out of summaries; define a stable parser for plain-text logs.'))
        ]),
        ('Safe, bounded automation retries', 'Retry transient failures only when repetition is safe, with explicit time and attempt limits.', [
            b('concept', 'Classify retryable failures', ('Transient and operation-specific', 'Some connection failures, selected unavailable responses and rate limits may merit retry. Do not retry every 5xx or assume a connection failure means no work happened.')),
            b('solution', 'Bound the retry policy', ('Backoff, jitter & budget', 'Use maximum attempts, per-attempt timeouts and an overall time budget. Exponential backoff with jitter avoids clients retrying in lockstep.'), ('Retry-After & final outcome', 'Respect valid Retry-After guidance within the allowed budget. Record attempts without secrets and report clear failure after exhaustion.')),
            b('cause', 'Do not blindly repeat', ('Permanent failures', 'Invalid input, missing configuration and permission failures require a changed condition. Authentication may need controlled refresh; investigate certificate errors rather than disabling verification.'), ('Ambiguous writes', 'A timed-out write may already have succeeded. Use supported idempotency keys or check operation status before repeating creates, emails or payments.')),
            b('code', 'Read the supplied retry helper', ('TransientError with full jitter', retry_code)),
            b('evidence', 'Know the helper limitations', ('What is not implemented', 'The operation must classify TransientError and enforce its own timeout. The helper does not implement Retry-After or a strict overall deadline.')),
            b('prevention', 'Avoid retry amplification', ('Coordinate retry layers', 'Nested retries can multiply requests and overload an unhealthy service. Retries cannot replace fixing invalid input or missing capacity.'))
        ]),
        ('DNS, TCP & TLS troubleshooting', 'Test from the affected environment and separate name resolution, transport, TLS and application behavior.', [
            b('issue', 'Collect the precise error', ('Actual network context', 'Confirm hostname, port, protocol, proxies and recent changes. A laptop, cluster and private network may use different DNS answers and routes.')),
            b('cause', 'DNS failure', ('Name versus resolver problem', 'Distinguish nonexistent names from resolver timeouts or server failure. Inspect records, resolver settings, Service/namespace names, cluster DNS, policy and private-zone linkage or forwarding.')),
            b('cause', 'Connection timeout', ('Connection did not complete', 'Investigate dropped packets, routes, firewalls, unreachable targets or service pressure. A timeout alone does not identify the responsible component.')),
            b('cause', 'Connection refusal', ('Active rejection', 'Check destination address/port, listener and interface, Service targetPort and ready endpoints. A firewall or proxy may reject too, so refusal is not proof of an application-originated error.')),
            b('cause', 'TLS error', ('Certificate and trust checks', 'Inspect chain, hostname match, expiry, trust store, SNI and system time. For mTLS, inspect client certificates and policy. Repair the cause rather than disabling verification.')),
            b('command', 'Layer-specific checks', ('Resolution, transport & request', 'getent hosts <hostname>\ndig <hostname>\nnc -vz -w 5 <hostname> <port>\ncurl -v --connect-timeout 5 --max-time 15 https://<hostname>/health'), ('Certificate & listener inspection', 'openssl s_client -connect <hostname>:443 -servername <hostname> -showcerts\nss -lntp\n\nTool availability and flags vary. Redact sensitive diagnostics; s_client inspection alone does not prove normal application verification succeeds.')),
            b('resolution', 'Verify the complete request', ('Beyond DNS and TCP', 'Verify HTTP, authentication and downstream processing from the affected environment. Ping alone is not a service-accessibility test.'))
        ]),
        ('HTTP errors as diagnostic clues', 'Identify the responding component and correlate evidence before assigning a cause.', [
            b('evidence', 'Find the responder', ('Gateway, proxy, app or dependency', 'Use request context, logs and traces to identify which component generated the status. The code narrows the investigation but is not a complete diagnosis.')),
            b('cause', '401 and 403', ('401 — authentication', 'Check missing, expired or malformed credentials and wrong token audience or issuer. Do not log tokens.'), ('403 — request refused', 'Check roles, policies, resource restrictions or WAF behavior at the responder. A 403 is not proof that every implementation authenticated the caller successfully.')),
            b('cause', '404', ('Route or resource missing/hidden', 'Check host, path, API version, route matching and resource ID. A default ingress route may return 404 even when the application is healthy.')),
            b('cause', '500', ('Unexpected server condition', 'Inspect exceptions, request traces and dependency failures. The status alone does not locate a line of code or establish infrastructure health.')),
            b('cause', '502 and 504', ('502 — invalid upstream response', 'Inspect proxy/gateway upstream protocol errors, connection closure and relevant logs. Exact response mapping depends on the implementation.'), ('504 — upstream deadline', 'Compare gateway timeout and upstream latency, tracing application and database work. Increasing a timeout can hide the bottleneck.')),
            b('cause', '503', ('Temporarily unable to serve', 'Check ready backends, overload, maintenance and dependency health at the responder. Inspect Retry-After if present and retry only when safe.'))
        ]),
        ('Metrics and actionable alerts', 'Page on actionable impact; use resource evidence and give each alert an owner and response path.', [
            b('evidence', 'User-facing service signals', ('Traffic, errors, latency, saturation', 'Monitor successful requests and acceptable response times for important operations. Use latency distributions and distinguish expected client errors from service failures.')),
            b('evidence', 'Architecture-specific signals', ('Kubernetes, database & queues', 'Track ready versus desired replicas, restarts, OOM, scheduling, throttling and memory; database queries, connections and locks; queue age/depth versus arrival, processing and business deadlines.'), ('GenAI operations versus quality', 'Model latency, API errors/rate limits, tokens, retrieval latency and user-flow success are useful operational signals. Answer quality needs its own appropriate measurements.')),
            b('concept', 'Monitoring stack responsibilities', ('Prometheus, Alertmanager & Grafana', 'Prometheus collects metrics and can evaluate alert rules; Alertmanager groups/routes notifications; Grafana provides dashboards. Grafana-managed alerting and other stack arrangements may differ.')),
            b('solution', 'Reduce noise', ('Windows, baselines & objectives', 'Use actionable user impact or credible risk, sensible windows, traffic requirements and baseline/SLO-based thresholds. One request failure or CPU spike should not automatically page.'), ('Group, inhibit, deduplicate', 'Group related failures, inhibit secondary alerts behind a known parent problem and use time-limited maintenance silences. Review alerts nobody acts on and monitor recovery.')),
            b('concept', 'SLI, SLO, SLA & error budget', ('Measurement, target & agreement', 'SLI measures service behavior; SLO sets a target over a defined window; SLA defines stakeholder commitments and may include consequences. Define eligibility and exclusions.'), ('Budget and burn rate', 'The error budget is unreliability permitted by the SLO. Burn rate measures how quickly it is consumed, helping distinguish urgency.')),
            b('prevention', 'Own and bound the monitoring', ('Runbooks and label cardinality', 'Every important alert needs an owner, severity, dashboard and runbook. Avoid unbounded user IDs, request IDs or raw URLs as metric labels; use controlled logs/traces for that context.')),
            b('evidence', 'Final practice checklist', ('Twelve source review prompts', practice))
        ])
    ]


SOURCES = {
    35: [
        ('top: processes, threads and CPU states', 'https://man7.org/linux/man-pages/man1/top.1.html'),
        ('ps: process CPU and resident memory', 'https://man7.org/linux/man-pages/man1/ps.1.html'),
        ('free: available memory and cache', 'https://man7.org/linux/man-pages/man1/free.1.html'),
        ('vmstat: interval statistics and swap activity', 'https://man7.org/linux/man-pages/man8/vmstat.8.html'),
        ('pidstat: per-process CPU, memory and I/O', 'https://man7.org/linux/man-pages/man1/pidstat.1.html'),
        ('df: filesystem capacity and inodes', 'https://www.gnu.org/software/coreutils/manual/html_node/df-invocation.html'),
        ('du: directory usage and filesystem boundaries', 'https://www.gnu.org/software/coreutils/manual/html_node/du-invocation.html'),
        ('iostat: latency, queues and device utilization', 'https://man7.org/linux/man-pages/man1/iostat.1.html'),
        ('lsof: deleted but open files', 'https://github.com/lsof-org/lsof/blob/master/docs/manpage.md'),
        ('journalctl: kernel and unit log filters', 'https://www.freedesktop.org/software/systemd/man/255/journalctl.html'),
    ],
}
