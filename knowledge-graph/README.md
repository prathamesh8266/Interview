# Incident Atlas

Open `../production-support-map.html` in any modern browser. The file is self-contained: no server, installation, internet connection or external libraries are required.

- Choose one of five sections using the section selector: **Production support**, **Kubernetes & Docker**, **Jenkins, Git & Release Management**, **Azure, Infra & Terraform**, or **Python, Linux, Networking & Monitoring**. Original question numbering (01–40) is preserved.
- Click graph nodes to expand or collapse their connections. Node clicks preserve your zoom and pan; use **Fit map** when you want to reframe.
- Edge labels and colors distinguish issues, evidence, causes, mitigations, recovery verification, prevention, communication and details still to confirm.
- Select any node to read its explanation. Use **Read full answer** for the complete response. Kubernetes & Docker includes concept and command nodes and expandable **Official references** links.
- Drag the canvas to pan, scroll to zoom, and press **F** to fit. Use **All questions** for an overview.
- Search covers all 40 answers and graph summaries across all five sections. Results identify their section; selecting one switches to that section.
- **Practice recall** hides the answer until you reveal it. **Mark revised** stores question progress in this browser's local storage.
- Nodes support Tab and Enter/Space. Left/right shortcuts and practice arrows cycle within the current section; arrow keys pan a focused canvas.

Content covers the ten supplied Section 1 answers in `Production support and troubleshooting/answer.txt`, eight Section 2 answers in `Kubernetes and Docker/answer.txt`, eight Section 3 answers in `Jenkins Git and Release Management/answer.txt`, and seven Section 4 answers in `Azure Infrastructure and Terraform/answer.txt`. Prepared content includes official references and does not claim personal implementation experience. Questions 19, 27 and 32 include experience templates; their graph marks the actual project, topology, ownership or results as details to confirm. The OSI PI production fix and 30–60 minutes of log verification are recorded; personal ownership and downstream impact remain explicitly marked as gaps.

Section 5 adds questions 34–40 directly from the existing `Python Linux Networkig and Monitoring/answers.txt`. This exact file is the source of truth and the build reads it without rewriting it; no singular `answer.txt` is created. Full answers preserve its health-check, log-aggregation and retry examples, explanations, limitations and final practice material. Python example nodes display the exact source snippets in a monospace details panel. The page identifies the source filename. Question 35 includes annotated command groups for CPU/processes, memory/swap, filesystem space/inodes, and device I/O/logs; these graph nodes are extracted directly from the source comments. There are now 40 questions onboarded and 10 remaining.

To edit the summaries or page, update `build.py`, the relevant `*_content.py` module, or `template.html`; full answers live in the section folders. `operations_content.py` summarizes Section 5 and extracts its code blocks directly from the supplied source. Run `python knowledge-graph/build.py` from the interview folder. This regenerates the standalone file and the identical `dist/index.html` copy. The existing local-storage key is retained so previously revised questions stay marked.

Progress is local to the browser and file/origin; moving to a different file location or browser may start a separate progress record. If browser storage is blocked, progress remains available for the current session.
