"""Build a standalone revision page from the supplied answers and curated map."""
import json
import re
from pathlib import Path
from kubernetes_content import get_maps, SOURCES
from release_content import get_maps as get_release_maps, SOURCES as RELEASE_SOURCES
from azure_content import get_maps as get_azure_maps, SOURCES as AZURE_SOURCES
from operations_content import get_maps as get_operations_maps, SOURCE_FILE as OPERATIONS_SOURCE, SOURCES as OPERATIONS_SOURCES

HERE = Path(__file__).resolve().parent
source = (HERE.parent / 'Production support and troubleshooting' / 'answer.txt').read_text(encoding='utf-8')
sections = re.split(r'\nQUESTION (\d+)\n', source.replace('\r\n', '\n'))
raw = {int(sections[i]): sections[i + 1].split('\n\nFINAL PRACTICE CHECK')[0].strip() for i in range(1, len(sections), 2)}

# Each branch is a relationship; each leaf retains the reasoning behind the cue.
def branch(kind, label, *items):
    return {'kind': kind, 'label': label, 'items': [{'label': a, 'text': b} for a, b in items]}

maps = [
('Application unavailable', 'Confirm impact → collect evidence → isolate → restore → verify → prevent.', [
 branch('issue','Confirm the impact',('Scope & start time','Check availability, error rates, affected endpoints and users. Is the whole application down or only part of it?'),('Severity & ownership','Assess business impact, acknowledge the alert and involve the relevant teams early.')),
 branch('evidence','Gather evidence',('Recent changes','Review releases, configuration, secrets, infrastructure and dependency changes. A recent release is a clue, not proof.'),('Workload health','Check pod health, restart counts, events, logs, resource use and node health. Compare healthy and failing replicas.'),('Trace the request path','Follow ingress or gateway → Service → application → database and other dependencies.')),
 branch('cause','Isolate the cause',('Release regression','Correlate failures with the new release and compare against the known-good version.'),('Dependency or capacity','Check dependency availability and resource exhaustion; bring evidence to the responsible owner.')),
 branch('solution','Restore safely',('Compatible rollback','Roll back when evidence supports a release failure. Check compatibility with current configuration and database schema.'),('Targeted mitigation','Address the failing dependency or exhausted resource. Capture useful evidence without delaying recovery.')),
 branch('resolution','Verify recovery',('Real requests & metrics','Exercise affected user flows. Confirm availability and error rates recover and monitoring supports the result.')),
 branch('prevention','Prevent recurrence',('Timeline & RCA','Update stakeholders, record the timeline and create owned actions based on the root cause.'))
]),
('Errors after deployment', 'A green pipeline does not prove that user requests work.', [
 branch('issue','Assess the regression',('User-facing failures','Collect affected endpoints, status codes, user scope and whether errors started after release.')),
 branch('evidence','Compare old & new',('Release differences','Compare image, code, environment variables, ConfigMaps, Secrets, deployment settings and migrations.'),('Runtime evidence','Inspect readiness, events, restarts, current and previous container logs, and dependency connectivity.'),('Trace a failing request','Check lazy initialization, missing configuration, invalid credentials and dependencies. Compare old versus new replicas.')),
 branch('solution','Decide on rollback',('Rollback criteria','Significant impact + evidence against the release + no quick, well-understood fix support restoring the known-good version.'),('Schema compatibility gate','Check schema and data compatibility first. An incompatible migration may require coordinated recovery or a forward fix.')),
 branch('resolution','Verify user recovery',('Affected flow & baseline','Retest the actual failed flow and confirm error rate and latency return to normal.')),
 branch('prevention','Improve release safety',('Close the testing gap','Investigate why tests missed the issue. Improve readiness, deployment validation and release tests.'))
]),
('Your OSI PI incident', 'Separate invalid input from dependency unavailability. Keep your story factual.', [
 branch('issue','Processing runs failed',('Application reads OSI PI','Processing failures prompted investigation of application input and source-system availability. Actual user impact still needs confirmation.')),
 branch('evidence','Trace the failing request',('Identify the tag ID','Trace the code making the request and check whether the tag ID exists on the PI server.')),
 branch('cause','Two different scenarios',('Invalid operator-supplied tag','An invalid tag was identified as a failure scenario. Do not conflate it with an unavailable source.'),('OSI PI unavailable','Source unavailability was observed separately and needs a different response.')),
 branch('solution','Production quick fix',('Feature branch deployed','A quick fix was deployed to production using a feature branch to address the invalid-tag failure.'),('Check before requesting','Check whether the PI tag exists on the PI server. Send the data request only when the tag exists.'),('Monitor the connection','A separate health-check application sends an email when the OSI PI connection fails. Detection does not itself restore the source.')),
 branch('resolution','Validate the production fix',('Monitor logs for 30–60 min','After deployment, the team monitored application logs for approximately 30 minutes to one hour.'),('Same tag, no application failure','Log monitoring confirmed that the same tag was handled without the application failing. This verifies the input-validation fix; it does not establish recovery of an unavailable PI server.')),
 branch('gap','Confirm before interview',('Downstream impact','Supply the actual downstream processing or user impact. This is still unconfirmed.'),('Your personal contribution','State which investigation, implementation, deployment and monitoring steps you performed personally versus the team.')),
 branch('prevention','Prepare follow-ups',('Batch behavior & error types','Could one tag fail a batch? How did you distinguish invalid input from permissions or connection errors?'),('Alert cadence & resumption','Explain the actual health-check interval, duplicate-alert handling and how processing resumed. These are prompts, not established facts.'))
]),
('Slow without a deployment', 'Locate the bottleneck before choosing a mitigation.', [
 branch('issue','Scope the slowdown',('Baseline & tail latency','Compare current latency with normal, including high percentiles. Identify endpoints, users and start time.')),
 branch('evidence','Correlate the signals',('Traffic & saturation','Compare latency with request rate, concurrency, CPU, memory and worker-thread usage.'),('Other changes','Check configuration, infrastructure and scheduled jobs. No deployment does not mean nothing changed.'),('Memory trends','Look for continuing growth, restarts, garbage collection and profiling evidence before claiming a leak.')),
 branch('cause','Inspect dependencies',('Database bottlenecks','Review slow queries, locks, connection usage, query latency and resource pressure.'),('Downstream API delays','Check response times, failures, retries and rate limits. Use traces to locate time spent.')),
 branch('solution','Match fix to bottleneck',('Scale with evidence','Extra replicas may help a saturated application but worsen database overload by adding connections.'),('Control expensive work','Address a blocking query or expensive workload when the evidence supports it.')),
 branch('resolution','Check improvement',('Latency & underlying issue','Verify latency improves and identify the capacity, application or dependency issue.'))
]),
('Identify the failing layer', 'Follow an affected request; use evidence before assigning ownership.', [
 branch('evidence','Anchor the investigation',('Request-level context','Collect timestamp, endpoint, error and request ID; correlate logs, metrics and traces.')),
 branch('cause','Application',('Exceptions & code paths','Look for validation failures, incorrect responses, thread exhaustion and version-specific failures. Healthy dependencies support investigating application behavior.')),
 branch('cause','Database',('Beyond a connection test','Inspect query time, locks, pool exhaustion, permissions and resources. Reachable does not mean healthy; slow queries may originate in application behavior.')),
 branch('cause','Network',('Test from the workload','Check DNS, timeouts, refusal, TLS, routing, firewall and network policies from the affected application environment. A laptop test uses a different path and identity.')),
 branch('cause','Infrastructure',('Shared resource health','Inspect node or VM health, CPU, memory, disk capacity, I/O and restarts. Check whether unrelated applications sharing infrastructure are affected.')),
 branch('solution','Coordinate recovery',('Connect symptoms to causes','Connection exhaustion could come from a leak or traffic spike. Engage owners with collected evidence and coordinate restoration.'))
]),
('Resolution, workaround & RCA', 'Service restoration and permanent cause removal are different milestones.', [
 branch('resolution','Incident resolution',('Restore normal service','Restore service and verify that the incident impact has ended. Full RCA can follow recovery. Detection can come from monitoring, users or another team.')),
 branch('solution','Workaround',('Temporary impact reduction','A controlled restart may recover a leaking application temporarily. Rollback or routing away from an unhealthy instance can also be workarounds.')),
 branch('cause','Root-cause analysis',('Why it happened','Use timeline, logs, metrics, changes and reproduction evidence. Distinguish the trigger, underlying cause and contributing conditions.')),
 branch('prevention','Permanent correction',('Memory-leak example','Restart restores service; finding and fixing the leak addresses its cause. Validate the fix and improve monitoring or testing.'),('Owned follow-up','Track longer-term corrective and preventive actions separately, with owners and target dates.'))
]),
('Prioritize & escalate', 'Business impact and urgency determine priority.', [
 branch('issue','Assess impact & urgency',('Business consequences','Consider affected users, critical functions, financial impact, data integrity, available workaround, growing impact and response targets.'),('Symptoms need context','High latency or a queue backlog can be critical depending on the business effect. A low-use feature with a workaround may be lower priority.')),
 branch('cause','Look for shared failure',('Correlate related alerts','Several application failures may share a database or other dependency. Addressing that cause can restore multiple services.')),
 branch('communication','Escalate early when needed',('Escalation triggers','Major incident, stalled progress, missing expertise or permissions, a decision outside your authority, possible data loss or an approaching SLA target.'),('Useful escalation packet','Include impact, start time, evidence, checks, mitigation attempts and the specific help needed. Keep ownership explicit.')),
 branch('solution','Coordinate incident work',('Parallel ownership','Assign clear owners for simultaneous incidents and reassess priority as impact and evidence change.'))
]),
('Write an actionable RCA', 'Explain what happened, why, how recovery worked, and what will change.', [
 branch('issue','Summary & impact',('Verified incident facts','State affected service, time window, severity, users or processes and business impact. Use verified measurements.')),
 branch('evidence','Timeline & evidence',('Consistent timezone','Record impact start, detection, acknowledgment, findings, mitigation, recovery and final verification.'),('Supporting artifacts','Use logs, metrics, traces, configuration differences and reproduction results. State uncertainty explicitly.')),
 branch('cause','Cause & contributing factors',('Trigger versus weakness','A deployment may trigger an outage while missing configuration validation lets an invalid setting reach production. Keep the analysis blameless.')),
 branch('resolution','Recovery & response review',('What worked and how verified','Record tested hypotheses, mitigation, recovery verification and response gaps, such as missing alerts or incomplete runbooks.')),
 branch('prevention','Corrective actions',('Owner + date + validation','Give each code fix, release check, monitoring change, runbook or recovery procedure an owner, target date and completion criterion.'))
]),
('Intermittent, unreproducible issue', 'Investigate the original occurrence and prepare to capture the next one.', [
 branch('issue','Capture the occurrence',('Precise incident context','Collect timestamp and timezone, tenant or user, endpoint, input conditions, error and correlation ID. Follow access and privacy requirements.')),
 branch('evidence','Compare failure & success',('Find patterns','Use logs, traces and dependency errors. Compare replica, version, user group, payload size, operation and peak-traffic periods.')),
 branch('cause','Check transient conditions',('Short-lived failures','Inspect resource spikes, exhausted connections, locks, dependency timeouts, network failure, token expiry and rate limits.'),('Replica differences','Compare configuration and environment when one replica fails while others remain healthy.')),
 branch('solution','Investigate safely',('Controlled reproduction','Recreate relevant input or concurrency in a controlled environment without generating uncontrolled production impact.'),('Targeted observability','Add structured logs, correlation IDs, dependency timings or focused traces. Keep capture proportionate and exclude secrets or sensitive payloads.')),
 branch('communication','Track unresolved work',('Facts, hypotheses & owner','Record evidence, impact and next actions, assign follow-up ownership and escalate based on impact. Cannot reproduce does not mean resolved.'))
]),
('Communicate during an outage', 'Communicate early, accurately and at an agreed cadence.', [
 branch('issue','Initial update',('Confirmed impact & next update','State affected service, impact, detection time, investigation status and when the next update will arrive. Do not wait for the complete diagnosis.')),
 branch('communication','Technical responders',('Evidence & task ownership','Share request IDs, errors, affected versions, logs, changes and hypotheses. Assign explicit owners to prevent duplicate or conflicting actions.')),
 branch('communication','Business stakeholders',('Plain-language progress','Explain affected functions, scope, workaround and recovery progress. Separate fact from suspicion; avoid unsupported recovery promises.')),
 branch('communication','Onshore handover',('Accepted ownership','Include timeline, impact, completed checks, actions and results, pending tasks and owners. Confirm the receiving team accepts ownership.')),
 branch('resolution','Recovery announcement',('Verify before announcing','Confirm recovery through user flows and monitoring, communicate remaining limitations, and share RCA or follow-up actions via the agreed process.')),
 branch('prevention','Maintain the incident record',('Cadence & updates','Use the agreed ticket, channel or bridge. Update when impact changes or mitigation occurs; state next steps even when there is no fix yet.'))
])]

data = []
for i, (title, takeaway, branches) in enumerate(maps, 1):
    question, answer = re.split(r'\n\nCANDIDATE ANSWER[^\n]*\n', raw[i], maxsplit=1)
    data.append({'id': i, 'section': 'production', 'title': title, 'question': ' '.join(question.split()), 'takeaway': takeaway, 'branches': branches, 'answer': answer.strip()})

for section_key, source_file, first_id, map_factory, references, is_prepared in [
    ('kubernetes', 'Kubernetes and Docker/answer.txt', 11, get_maps, SOURCES, True),
    ('release', 'Jenkins Git and Release Management/answer.txt', 19, get_release_maps, RELEASE_SOURCES, True),
    ('azure', 'Azure Infrastructure and Terraform/answer.txt', 27, get_azure_maps, AZURE_SOURCES, True),
    ('operations', OPERATIONS_SOURCE, 34, get_operations_maps, OPERATIONS_SOURCES, False),
]:
    prepared_source = (HERE.parent / source_file).read_text(encoding='utf-8')
    prepared_sections = re.split(r'\nQUESTION (\d+)\n', prepared_source.replace('\r\n', '\n'))
    prepared_raw = {int(prepared_sections[i]): prepared_sections[i + 1].strip() for i in range(1, len(prepared_sections), 2)}
    for i, (title, takeaway, branches) in enumerate(map_factory(branch), first_id):
        question, answer = re.split(r'\n\nCANDIDATE ANSWER[^\n]*\n', prepared_raw[i], maxsplit=1)
        item = {'id': i, 'section': section_key, 'title': title, 'question': ' '.join(question.split()), 'takeaway': takeaway, 'branches': branches, 'answer': answer.strip(), 'sources': references.get(i, []), 'prepared': is_prepared}
        if section_key == 'operations':
            item['sourceFile'] = source_file
        data.append(item)

template = (HERE / 'template.html').read_text(encoding='utf-8')
output = template.replace('/*__DATA__*/', 'const DATA = ' + json.dumps(data, ensure_ascii=False).replace('</', '<\\/') + ';')
(HERE / 'dist').mkdir(exist_ok=True)
(HERE / 'dist' / 'index.html').write_text(output, encoding='utf-8')
(HERE.parent / 'production-support-map.html').write_text(output, encoding='utf-8')
print(f'Built {len(data)} questions, {sum(len(q["branches"]) for q in data)} branches, {sum(len(b["items"]) for q in data for b in q["branches"])} detail nodes.')
