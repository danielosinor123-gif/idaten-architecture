# Idaten Ce100: Pattern-Coded Magnonic Execution, Persistent Magnetic Results, and Dynamic Rails

**Research concept paper and agent context**  
**Revision:** 16 November 2026 — expanded with input-to-switch programming and concurrent-update cost analysis  
**Status:** Architecture hypothesis; not a report of a fabricated or validated device

## Abstract

Idaten Ce100 is proposed as an inference architecture in which a **spatially and temporally structured transistor/switch topology acts like an execution code**, and magnons perform the workload without repeated electrical conversion between operations. The key proposed result is not merely an outgoing wave to be sampled: magnonic computation is intended to **write a persistent, machine-readable magnetic-state pattern** into the rail/memory structure. That stored pattern is read electrically only after the individual workload completes. The fabricated transistor/switch placement defines the available code topology; an input-coded configuration pattern sets switch states; propagating waves then transform the live workload and write result states into the medium. Setup-then-compute, inline updates, and hybrid/pipelined operation are compared, with the hybrid recommended as the safest path to test before same-packet switching.

This paper formalizes that mechanism and distinguishes it from what has already been demonstrated. A 2023 YIG experiment established that propagating magnons can reverse bistable nanostripes and leave nonvolatile magnetic states; Idaten’s novel ambition is to extend such threshold-like magnonic writing into a richer, structured computation result pattern, generated and retained through a workload, then read at the end. The paper describes input encoding, pattern-mediated computation, persistent state writing, end-of-workload readout, dynamic-rail evolution, material choices, and experimental decision gates. The exact scalable write mechanism, pattern capacity, state fidelity, reset method, and energy advantage remain research questions. YIG, hematite, and Co–Fe are candidate materials to compare, not predetermined winners. The product objective remains measured energy per correct inference at a defined latency and quality target.

**Keywords:** magnonics; spin waves; pattern-coded execution; physical computing; reconfigurable routing; magnetic switch; input/output; direct magnonic cascade; inference efficiency

## 1. Corrected Conceptual Model

Idaten should be understood as a **pattern-programmed, magnon-executed, state-writing system**. Magnons carry and process the live workload pattern; their interactions are intended to write a persistent magnetic-state pattern representing the result. This stored state—not each intermediate wave—is the machine-readable output. The external electrical interface reads the stored pattern only after the workload is complete.

There are four distinct state objects:

1. **Fabricated topology, \(P_0\):** the physical placement and geometry of transistors/switches, magnetic regions, couplers, rails, and storage elements. This is fixed when the die is fabricated. It defines the repertoire of physical routes, couplings, and writable sites.
2. **Execution configuration, \(C_k\):** the electrical or magnetic state of switches during operation \(k\). This selects/configures a code pattern on the fixed topology. It may be loaded per task, model/layer, or inference, subject to measured setup cost.
3. **Live computational pattern, \(\Psi_k(x,y,t)\):** the propagating magnetic wavefield during execution. It carries current workload information through spatial distribution, routes, amplitude, phase, frequency, and timing.
4. **Persistent result pattern, \(M_k(x,y)\):** the remanent magnetic states written by the computation into storage/rail elements. These remain after the propagating waves have passed, encode the accumulated computation result, and are intended to be read at the end of the workload. They are distinct from both the preloaded route configuration and the transient wavefield.

The intended cycle is therefore:

> **Boundary input/program encoding → write or select rail configuration \(C\) → magnonic computation through the configured topology → magnons write/update persistent result pattern \(M\) → continue the workload without electrical intermediate readout → one final magnetic-state read and electrical decode.**

In the later inline mode, data-dependent updates to \(C\) may occur between wave packets or sub-operations while \(M\) is being formed; same-packet switching is a separate, higher-risk experiment.

The transistor locations do not physically move from one execution to another. Their designed placement establishes the codebook of possible routes and writable sites; runtime switch states choose/configure a pattern on that topology. The magnetic medium also holds persistent result states written by the workload. The design must keep configuration memory and result memory conceptually separate, even if one physical element eventually serves both roles.

## 2. Research Evidence and Limits

Existing work supports important pieces of the idea but does not establish the complete Idaten mechanism. A YIG study reported a passive waveguide network with 34 inputs, 34 outputs, and 198 crossings. It supports progress in multi-path magnonic routing, but does not demonstrate an active pattern-decoding switch array or an end-to-end inference processor.[^1](https://pmc.ncbi.nlm.nih.gov/articles/PMC12657222)

A closer precedent for the proposed output state is a 2023 experiment in which propagating magnons in a 100-nm YIG film irreversibly switched bistable permalloy nanostripes, leaving remanent, nonvolatile magnetic states after the wave passed. Switching was observed across a magnonic bus over tens of micrometres; magnetic-force microscopy confirmed the written states, while low-power RF scattering could sense the magnetic configuration. The article reports RF power applied to the coplanar-waveguide port in the tens-of-microwatts range for some switching conditions, and separately estimates much smaller power transferred into magnetic precession. Those are not full-system inference-energy figures and should not be presented as such. The experiment demonstrates a basic magnon-written magnetic memory effect, but the written information was threshold-dependent binary stripe reversal—not an arbitrary high-capacity inference-result pattern or a complete AI workload.[^9](https://pmc.ncbi.nlm.nih.gov/articles/PMC10060572)

A spin-wave neural-network study proposed that magnetic-field patterns scatter waves and create mappings between sources and detectors, using micromagnetic inverse design. This gives a precedent for treating a spatial magnetic pattern as a computation program; it does not prove Idaten’s proposed dynamic route handoff.[^2](https://pubmed.ncbi.nlm.nih.gov/34741047)

An experimental spin-wave interferometer used output antennas to detect inductive voltages that vary with wave interference. This supports electrical readout at a designated final boundary.[^3](https://www.nature.com/articles/s41598-017-11881-y) A spin-wave majority gate demonstrated electrical transducers and phase-coded wave inputs, a relevant example of waves carrying logic states through a patterned device.[^4](https://www.science.org/doi/10.1126/sciadv.abb4042)

The multi-stage path remains challenging. A reported magnonic repeater regenerated a decayed wave using an externally powered microwave pump, so an amplifier or active regenerator must be included in the energy budget.[^5](https://pmc.ncbi.nlm.nih.gov/articles/PMC11365973) A different material or geometry may improve speed or integration, but must be tested as a complete signal path. YIG is a useful low-damping reference with process-integration limitations; hematite has reported high group velocities in spectroscopy but is not yet an inference engine; Co–Fe offers a thin-film process candidate with higher damping than best-case YIG.[^6](https://pmc.ncbi.nlm.nih.gov/articles/PMC10533023)[^7](https://doi.org/10.1103/PhysRevMaterials.7.054407)

The key evidence gap is specifically: **Can a workload’s magnons write a sufficiently rich, spatially organized, repeatable, and readable persistent magnetic result pattern—across the required workload size—without electrical conversion between operations, and at lower total energy than conventional conversion-based processing?** Existing binary nanostripe switching motivates the idea, but Idaten still needs to show how many stable pattern states can be written, how they combine or update, how errors are corrected, how the pattern is reset/retained, and how the final readout scales. This is the central research question, not an established product capability.

## 3. Layered Physical Interpretation

### 3.1 Layer 1: fabricated execution topology and rail controls

The base layer contains the fixed physical placement of candidate transistor/switch cells, local drivers, control lines, and storage/control elements. It defines the possible geometric routes, couplings, and switching locations. During each operation, control states or biases select a particular route pattern, tune a local magnetic property, enable/disable a coupling, or set a path/phase condition.

A rail is not assumed to be a literal empty trench. It is a functional path whose transmission, phase, coupling, or magnetic state has been made favorable relative to alternatives. Its physical realization might involve a patterned magnetic region, local anisotropy modulation, a magnetic element, a waveguide boundary, or a hybrid structure. The exact device must be established experimentally.

A control transistor can set or maintain a route configuration, while magnon-driven state changes write the workload result into magnetic storage elements. If those retained states later alter a rail or control a subsequent operation, that is the future state-dependent rail mode described in Section 5; it is distinct from simply reading a transient wave at every stage.

### 3.2 Layer 2: magnonic pattern-processing fabric

The magnetic medium hosts the propagating wavefield. Each useful operation transforms a pattern rather than merely transporting a single bit. The relevant state may include:

\[
\Psi_k = \{A_i,\phi_i,f_i,t_i,r_i\}_{i=1}^{N},
\]

where for each active component \(i\), \(A_i\) is amplitude, \(\phi_i\) is phase, \(f_i\) is frequency, \(t_i\) is timing, and \(r_i\) denotes its spatial rail/path or mode. This notation is a proposed abstraction; an experiment must establish which dimensions can be independently controlled and robustly distinguished.

The fixed topology \(P_0\) and current configuration \(C_k\) together define the physical operator for that stage:

\[
\Psi_{k+1}=\mathcal{F}(\Psi_k;P_0,C_k)+\eta_k,
\]

where \(\mathcal{F}\) includes propagation, scattering, interference, and any validated nonlinear behavior; \(\eta_k\) includes loss, noise, reflections, unwanted modes, and drift. A small-signal linear subset may be approximated by a complex transfer matrix \(\mathbf{b}=\mathbf{H}(f;P_0,C_k)\mathbf{x}+\mathbf{n}\), but this is a local model of one operating condition—not the whole architectural concept.

### 3.3 Layer 3: boundary conversion and final electrical output

At the input boundary, conventional digital or electrical values must be encoded into the physical wave pattern using transducers and timing/phase control. During execution, magnons are intended to write a retained magnetic result pattern. At the workload boundary, Layer 3 senses that stored state and converts it to electrical output values. The architectural aim is to avoid repeated full electrical conversion between internal operations; it does not eliminate input encoding or final readout.

## 4. Input and Output Concept in Detail

### 4.1 Input: from activation vector to initial wave pattern

The host/CMOS controller holds the input values and selects a configuration. An encoder maps values to a physically controllable wave representation—candidate dimensions include amplitude, relative phase, pulse timing, frequency, and launch port. Input antennas or other electrical-to-magnetic transducers launch those signals into the magnetic substrate.

The first experiments should not use a vague “token pulse.” Specify, for every input channel:

- numerical range and precision;
- amplitude/phase/timing encoding;
- reference oscillator or phase origin;
- pulse shape, carrier frequency, and bandwidth;
- which physical antenna/rail launches it;
- expected variability and calibration method.

For a real-valued input, one possible encoding is amplitude for magnitude and a phase reversal of approximately \(\pi\) for sign. A complex encoding may carry two degrees of freedom in I/Q. A time-coded pulse pattern may use arrival times or pulse sequences to represent a vector. Each has trade-offs: phase needs coherence; amplitude is sensitive to loss; time coding needs reliable timing and bandwidth; multi-port spatial coding needs enough separate rails and low cross-talk. The architecture should retain the representation that gives the lowest **system** energy at required accuracy, not the most intuitive analogy.

### 4.2 In-core execution: computation writes the result pattern

The launched \(\Psi_0\) enters the fabricated topology \(P_0\) under the selected execution configuration \(C_0\). Interference, phase accumulation, scattering, and any validated nonlinear interactions perform the workload. In the proposed Idaten mechanism, those interactions do not merely create a transient output wave to be sensed. They also write or update magnetic storage states distributed along the rail structure. The retained magnetic-state map is the accumulated result pattern \(M_{k+1}(x,y)\).

The intended physical principle is magnon-to-magnetization state writing: the propagating wave transfers angular momentum, exerts an effective torque, or otherwise changes a nearby bistable magnetic element when its local excitation meets the element’s switching condition. The written state remains after the wave decays or passes, so the workload’s result can persist without converting each intermediate wave into a conventional electrical value. The 2023 YIG/permalloy nanostripe study provides a direct precedent for the base effect—propagating magnons can switch remanent magnetic bits over tens of micrometres—but it demonstrated threshold-like binary switching, not Idaten’s proposed dense, computation-shaped output pattern.[^9](https://pmc.ncbi.nlm.nih.gov/articles/PMC10060572)

A useful abstraction for one operation is:

\[
\Psi_{k+1}=\mathcal{F}(\Psi_k;P_0,C_k,M_k)+\eta_k,
\qquad
M_{k+1}=\mathcal{W}(M_k,\Psi_{k+1};P_0,C_k)+\xi_k.
\]

Here, \(\mathcal{F}\) is the magnonic computation; \(\mathcal{W}\) is the write/update process that converts local wave conditions into retained magnetic states; \(M_k\) is the prior stored pattern; and \(\eta_k,\xi_k\) collect propagation and write errors. The state pattern may be binary, multilevel, or spatially encoded, but its actual capacity must be measured. Do not assume analog-valued or arbitrary patterns can be retained merely because a binary nanomagnet can switch.

The basic memory-cell concept is a set of bistable magnetic elements with two remanent orientations. An incident wave can switch an element if a local write criterion is met; elements below threshold retain their prior state. Thus a spatially varying wave amplitude, phase, mode, or timing can potentially leave a spatially varying state pattern. The research challenge is to shape that threshold response into a useful result code—controlling write thresholds, selectivity, state retention, and update/reset behavior so that the resulting pattern represents the computation rather than merely recording where wave power exceeded a threshold.

**Conceptual example (illustrative, not a specified Idaten cell design):** an encoded input launches a sequence of waves through a configured rail topology; interference and propagation create local conditions that write some bistable cells and leave others unchanged; after the last wave, the device holds a spatial word such as \([m_1,m_2,\ldots,m_N]\); a final sensor array reads that stored word and the decoder maps it to the workload output. The central advantage sought is that intermediate computation leaves magnetic marks in place instead of repeatedly detecting each wave, converting it to an electrical number, and re-launching a new wave. The exact code, cell physics, and decoder remain to be designed and validated.

The following mechanism families are candidates for investigation, not settled choices:

- **Magnon torque / spin-transfer to an adjacent nanomagnet:** use angular-momentum transfer from the propagating magnon or associated spin current to switch a bistable element. Measure write threshold, switching probability, latency, and energy per written state.
- **Dipolar-field-assisted switching:** exploit the local oscillating magnetic field of the wave to assist nucleation or reversal in a designed magnetic element. Separate this from direct microwave exposure and thermal artifacts.
- **Resonant/threshold cells:** engineer elements whose switching response depends on local wave amplitude, frequency, phase, or mode, enabling more selective pattern writes. Characterize distributions and cross-talk across an array.
- **VCMA/strain-assisted magnetic writes:** use an electric field or strain to adjust a write threshold or state barrier, potentially lowering write energy or selecting which cells are receptive. The gate-drive and retention costs remain in the ledger.

The architectural ambition is not simply to let a live wave select a downstream route. It is to let magnonic computation write a durable state pattern that later operations can interact with or that the final output stage can read. Dynamic rails and result storage may share physical sites only if the roles are explicitly distinguished: a preloaded configuration \(C_k\) programs execution; a workload-written result \(M_k\) stores data. If a magnetic result state also changes later propagation, that coupling is part of the computation and must be modeled and tested.

### 4.3 Final output: read the retained magnetic pattern once per workload

After the individual workload has completed, the final output stage senses the stored magnetic-state pattern \(M_{final}(x,y)\), converts that pattern to electrical measurements, and decodes it into the requested inference result. This is the key architectural distinction: **the magnonic computation writes its result into magnetic states; the final electrical readout is deferred until the workload boundary.**

Candidate readout paths include:

- **Low-power spin-wave sensing:** launch a weak probe wave and measure how the stored magnetic configuration changes reflection/transmission. The 2023 nanostripe study used low-power RF scattering parameters to sense stripe states and magnetic-force microscopy to verify remanent state patterns in the laboratory.[^9](https://pmc.ncbi.nlm.nih.gov/articles/PMC10060572)
- **Magnetoresistive or magnetic-state sensors:** sense local magnetization electrically, potentially using an array of sensors. This is a direct magnetic-to-electrical read at the end; sensor and ADC energy, area, noise, and read disturb must be measured.
- **Inductive antenna readout:** use state-dependent wave transmission or resonance at output ports, then detect RF voltage with coherent I/Q or an appropriate envelope detector. This reads a magnetic pattern through its effect on the final wave response; it may require an applied probe and RF receiver.
- **Laboratory imaging:** magnetic-force microscopy or BLS can verify the pattern during research but should not be assumed to be the deployed chip readout.

The output decoder must specify how the spatial magnetic states map to numerical logits, class labels, activations, or other workload outputs. For binary state arrays, this may be a spatial code or population/counting code; for multilevel cells, calibration and noise margins are required. If the model requires high precision, the final readout may need multiple sensors, differential encoding, or digital postprocessing. Those costs do not invalidate the proposal, but they are part of its energy and latency.

The final boundary chain is:

> **completed workload → persistent magnetic result pattern \(M_{final}\) → one end-of-workload sensor/read sequence → electrical measurement array → calibration/decoding → inference output.**

Read energy, write energy, reset/erase energy, sensor noise, read disturb, retention time, and pattern capacity must be measured. Avoid repeated intermediate readout unless required by the tested architecture, because repeated conversion would give up the proposed advantage. Direct electrical feedthrough, substrate coupling, reflections, and heating must still be controlled in the test structures.

### 4.4 Input-to-switch programming: what changes the rails?

The next design problem is the path from the input to switch state. Separate two inputs that may otherwise be conflated:

- **Configuration/program input, \(U_{cfg}\):** tells the fabric which execution pattern or rail configuration to use. This may represent a model/layer, weights, or a selected computation path.
- **Workload/data input, \(X\):** the values being processed by the configured magnonic fabric. In an adaptive design, \(X\) may also cause data-dependent changes to selected magnetic switches.

If the data itself must change a route without an electrical read/decode/write loop, the physical switch cannot be only an ordinary CMOS transistor gate. It needs a magnon-sensitive state element or coupling path: for example, a bistable nanomagnet whose magnetization controls a nearby rail’s transmission, phase, or coupling, and which can be switched by the incident wave under a designed condition. A transistor may still bias, reset, or read the element, but if it detects the magnon and then electrically toggles a CMOS gate during every operation, that is an intermediate conversion and must be counted. The direct magnon-to-magnetic-state mechanism has experimental precedent in binary nanomagnet writing; the design challenge is to make the written state select a useful route and scale it into a code pattern.[^9](https://pmc.ncbi.nlm.nih.gov/articles/PMC10060572)

An input-to-switch sequence can therefore be represented as:

\[
C_{new}=\mathcal{G}(C_{old},U_{cfg},X;P_0),
\]

where \(\mathcal{G}\) is physically implemented by magnetic write elements, local thresholds, and their coupling to the rails—not assumed to be a free digital instruction decoder. The route-state map is then used by the computation:

\[
\Psi_{out}=\mathcal{F}(\Psi_{in};P_0,C_{new}),\qquad
M_{result}=\mathcal{W}(M_{old},\Psi_{out};P_0,C_{new}).
\]

This separates “the input that tells the switches what to change” from “the data wave that computes,” while allowing both to derive from one external input stream if it is encoded into different spatial regions, frequencies, phases, or time slots.

Three timing modes are possible:

1. **Setup then compute:** an input-coded magnon sequence writes the switch configuration; after the cells settle, a later wave sequence performs computation and writes the result pattern. This is easiest to measure and debug, but adds a configuration-write pass, its launch energy, switching delay, and possibly a reset/erase cycle. Its cost can be amortized if one configuration is reused across many input instances.
2. **Inline update:** the same evolving workload both computes and changes switch states. This can avoid a separate full configuration pass, but the wave may reach a junction before or after a cell switches, making the route depend on timing, threshold variation, and local history. Simultaneous same-packet switching and computation is not assumed to work; the switching response must be faster and more predictable than the relevant wavefront spacing, or updates must be scheduled between packets/time slots. Expect greater calibration, write-error, and accidental-reroute risk.
3. **Hybrid (recommended research path):** load a coarse configuration first, then permit data-dependent magnetic updates only at controlled boundaries—between wave packets, between sub-operations, or in a separate local region—while the rest of the fabric continues its current operation. Use distinct configuration cells \(C\) and result cells \(M\) in early prototypes. Later, pipeline configuration of one tile while another tile computes.

The hybrid is the best first architecture to test because it preserves the no-intermediate-electrical-readout goal without requiring a switch to change under the same wave packet. “Both at once” can mean concurrent activity in different cells/regions or stages; it should not be claimed as same-cell, same-instant operation until timing and state transitions demonstrate it.

## 5. Dynamic “Railways”: Future Structure and Progression

### 5.1 What changes dynamically

The future rail fabric has three distinct kinds of state:

- **Immutable code topology:** transistor/switch placement, fixed magnetic geometry, waveguide layout, coupling sites, writable magnetic cells, and basic connectivity. These are set during fabrication and define the repertoire of possible executions and result patterns.
- **Mutable execution configuration:** transistor on/off or bias states, switch/gate states, selected routes, and other preloaded settings. These configure how the next workload will execute.
- **Workload-written result state:** remanent magnetic cells written or updated by the propagating magnons during computation. This spatial state pattern holds the result and is read at the end of the workload.

The chip does not physically move transistors during inference. The fabricated placement supplies a codebook of possible physical patterns; switch configurations select a member or combination from that codebook; magnon activity computes and writes the run-specific result state. Configuration memory and result memory must be distinguished, even if future devices combine the roles.

### 5.2 Levels of railway and result-pattern capability

**R0 — Fixed wave path and one output detector.** Characterize launch, propagation, and readout. This is a device baseline, not yet the proposed stored-pattern architecture.

**R1 — One magnon-written magnetic bit.** Demonstrate a bistable cell that changes state after exposure to a propagating magnon above a measured write condition, then remains in the written state after the wave ends. A YIG/permalloy experiment provides a precedent for this basic effect.[^9](https://pmc.ncbi.nlm.nih.gov/articles/PMC10060572)

**R2 — Small spatial result pattern.** Place an array of independently readable/writable magnetic cells along or beside rails. Demonstrate that different wave amplitudes, paths, or modes produce repeatable spatial patterns of remanent states. Read only after the workload pulse sequence completes. Quantify pattern capacity, write errors, retention, read disturb, reset/erase cost, and cross-talk.

**R3 — Patterned execution topology.** Fabricate multiple rails and write sites so the same input workload can create different output patterns under different fixed magnetic layouts. Prove that the geometric pattern—not just total input power—determines the result map.

**R4 — Switch-programmed pattern codebook.** Add transistor/switch states on the fixed placement to select among validated rail configurations and write patterns. The execution configuration is a vector C; the result is the persistent magnetic map M. Measure each configuration-to-result mapping, its setup/hold cost, and repeatability.

**R5 — Dynamic rail updates and pattern-preserving cascade.** Let the written magnetic pattern influence subsequent propagation, local thresholds, or rail selection so later magnons can continue the same workload without electrical readout. This is the future “railroad” capability: the network is reconfigured or conditioned by the magnetic state left by earlier computation. First show one controlled state-dependent path; then test small cascades. Do not assume every arbitrary pattern can alter a route without a defined coupling mechanism.

**R6 — Workload-aware configuration and end readout.** A controller selects a pre-characterized physical code pattern for a model/layer, lets the magnonic workload write its result map, then performs one final read sequence. The schedule should minimize configuration, write, hold, reset, and final read energy per correct inference. If state-pattern transitions are data-dependent, test and account for their timing and energy explicitly.

### 5.3 Pattern memory and configuration retention

Two stored patterns must be kept conceptually distinct. **Configuration state** \(C\) is loaded before or during a task to choose how the rails execute. **Result state** \(M\) is written by the magnonic workload and records its output. The intended architecture reads \(M\) only at the end of the individual workload, while the rail configuration may remain in place for many workload instances. A magnetic cell may eventually serve both roles, but only if the design specifies how it is initialized, written, protected from accidental overwrites, and read without destroying a needed state.

The most conservative early system uses a static or semi-static rail configuration and a distinct result-cell array. Run the workload, let magnons write a result pattern, and then perform one final read sequence. Before the next workload, either preserve or reset/erase the result cells according to the task protocol. Measure write energy, retained-state lifetime, read energy, read disturb, reset energy, and state variability. Dynamic rails become more ambitious when the magnetic result pattern itself changes the propagation or enables the next rail; that state-dependent feedback should be added only after basic write/read operation is repeatable.

### 5.4 What simultaneous switch updates cost

“Configure and compute at the same time” has two meanings. At the system level, separate regions or tiles can act concurrently. At the device-event level, one wave may try to switch a cell while that same wavefront is using the route controlled by that cell. The first is a plausible pipelining objective; the second introduces a race that must be measured.

| Mode | Added cost | Main benefit | Principal risk |
|---|---|---|---|
| Setup then compute | Configuration-wave launch/write energy, settling time, possible erase/reset, extra magnetic cells | Stable route during computation; simplest calibration and error attribution | Setup overhead if configuration is changed too frequently |
| Inline, same evolving wave sequence | State-transition energy and delay still apply; often less idle/setup interval, but no cost is eliminated | Data-dependent route changes without a separate full configuration pass | Race between wave arrival and state transition; threshold variation, accidental writes, history dependence, nonrepeatable routes |
| Hybrid / pipelined | Coarse setup plus selected local updates; extra control regions and scheduling | Balances stable execution with adaptive routes; can overlap setup of one tile with compute on another | More area/control complexity; needs careful separation of configuration \(C\) and result \(M\) |

For each mode, measure the incremental cost rather than infer it from the magnetic material’s low dissipation:

\[
E_{per\;inference}=\frac{E_{configuration\;write}}{R}+E_{input}+E_{magnon\;compute}+E_{result\;write}+E_{reset}+E_{final\;read}+E_{control},
\]

where \(R\) is the number of inferences that reuse one configuration. If the configuration changes for every inference, \(R=1\). Inline operation still pays for changing magnetic state; it may only save a separate configuration pass or idle interval. The total advantage exists only if the avoided intermediate conversion energy exceeds added switch-write, control, reset, error-correction, and timing costs at the same quality and latency.

**Recommended development decision:** prototype setup-then-compute first with separate configuration and result cells; then add controlled inline updates between packets or sub-operations; finally test spatially pipelined simultaneous operation. This sequence makes each extra benefit measurable and prevents an apparent speed/energy gain from hiding state-write errors or an electrical control loop.

## 6. Material and Fabrication Strategy

Do not choose the magnetic medium based on group velocity alone. Compare candidate materials using the same device geometry and target operation where possible. Measure propagation delay, decay, usable bandwidth, pattern fidelity, phase coherence, fabrication spread, selector response, and electrical readout strength.

- **YIG:** low-loss reference and strong propagation baseline; epitaxial growth and substrate/thermal constraints can complicate CMOS integration.[^6](https://pmc.ncbi.nlm.nih.gov/articles/PMC10533023)
- **Hematite:** speed-oriented candidate due to reported high group velocities in relevant experiments, but resonance shape, electrical excitation/detection, nanoscale pattern control, and circuit integration need validation.[^7](https://doi.org/10.1103/PhysRevMaterials.7.054407)
- **Co–Fe alloy:** process-integration candidate with sputtering potential; compare its damping, propagation, and ability to support dense pattern selectors.[^6](https://pmc.ncbi.nlm.nih.gov/articles/PMC10533023)

A hybrid stack should be introduced only after the separate materials and coupling elements are characterized. The CMOS base may program gates without the magnetic layer becoming a silicon-foundry-native process; 3D integration, thermal budget, vertical interconnect parasitics, magnetic field compatibility, and assembly yield remain explicit integration questions.

## 7. Mathematical and Measurement Model for Persistent Pattern Writing

For each stage \(k\), record the fabricated topology \(P_0\), execution configuration \(C_k\), live wave pattern \(\Psi_k\), and persistent result state \(M_k\):

\[
\Psi_{k+1}=\mathcal{F}(\Psi_k;P_0,C_k,M_k)+\eta_k,
\]

\[
M_{k+1}=\mathcal{W}(M_k,\Psi_{k+1};P_0,C_k)+\xi_k.
\]

Here, \(\mathcal{F}\) describes magnonic computation and propagation; \(\mathcal{W}\) describes physical writing/updating of persistent magnetic cells by the local wave state; and \(\eta_k,\xi_k\) capture propagation and writing errors. If the stored result pattern changes later wave propagation, it enters as a state-dependent parameter in \(\mathcal{F}\). If it only records the completed computation, it remains an output memory state until final readout. These are different operating modes and should not be conflated.

At workload completion, a read function \(\mathcal{R}\) converts the retained state map to an electrical output:

\[
\mathbf{y}_{out}=\mathcal{R}(M_{final})+\epsilon_{read}.
\]

This model makes the central research questions explicit: what local wave conditions switch each cell; how many distinct result patterns are reliably representable; how writing changes with prior state; how the pattern persists; what read/reset costs apply; and whether the full write-compute-read cycle saves energy relative to repeated electrical conversion. If configuration is state-dependent, separately characterize \(C_{k+1}=\mathcal{G}(M_{k+1},C_k)\); that is an optional future dynamic-rail feedback function, not a substitute for the core result-writing process.

For a target workload, compare the decoded final result \(\mathbf{y}_{out}\) against the reference over held-out inputs and repeated runs. Record the full input/write/read/reset behavior, including latency, energy, accuracy, pattern capacity, and retention. Use simulation to suggest \(P_0\), \(C_k\), and cell geometry, then use measured write/read statistics to update the model. Simulation-only demonstrations must be labeled as such.

## 8. Iteration Plan and Decision Gates

### Gate 0 — Define the workload and result-pattern alphabet

Choose one small inference-relevant operation. Define the input encoding and what the output pattern means physically: which cells, orientations or levels represent which output values, what spatial code or aggregation is used, and what error/precision is acceptable. Freeze the quality, latency, baseline, and complete energy boundary before device optimization.

**Pass:** a test set maps each input to a reference output state-pattern and a decoded numerical result.

### Gate 1 — Replicate magnon-written nonvolatile state switching

Begin with a simple YIG bus and bistable magnetic cells, using a lab measurement of the wave and post-exposure magnetic state. Establish write threshold versus frequency, mode, duration, bias field, cell geometry, prior state, and distance. Use magnetic imaging or equivalent independent means to verify retained states; compare against low-power RF sensing.

**Pass:** propagating magnons—not direct RF feedthrough or heating—write a repeatable remanent state after the wave is gone, and the written state can be sensed without erasing it. This reproduces the basic published memory effect, not yet an inference processor.[^9](https://pmc.ncbi.nlm.nih.gov/articles/PMC10060572)

### Gate 2 — Characterize write selectivity, retention, and reset

Test arrays of bistable cells. Determine whether local wave amplitude, phase, frequency, mode, timing, or path can selectively write chosen cells while leaving others unchanged. Measure retention, write-error probability, read disturb, reset/erase method, state variability, cell-to-cell cross-talk, and write energy.

**Pass:** the array can hold more than a trivial uniform “above threshold” record, with measured spatial write contrast and a usable read margin.

### Gate 3 — Demonstrate a fixed topology that writes a target result pattern

Design the fabricated magnetic/transistor placement and fixed route pattern to map a small input workload to a target spatial result state. Use simulation for inverse design, then verify using measured device behavior. The criterion is not merely an output-wave transform: the post-workload remanent map must match the target result code.

**Pass:** held-out inputs produce the predicted persistent state pattern with repeatable decoded results and bounded write errors.

### Gate 4 — Add execution-specific switch configurations

On the same fixed placement, set two or more switch-state patterns. Measure how each configuration changes the magnon path and the resulting written map. Test both a setup-then-compute sequence (configuration write followed by a later compute sequence) and controlled inline updates between distinct wave packets or sub-operations. Do not initially switch a cell underneath the same packet whose route it controls. Distinguish preloaded configuration state \(C\) from result memory \(M\). Measure configuration loading/holding energy, write-state changes, settling time, latency, and cross-talk.

**Pass:** different configurations implement distinct, reproducible input-to-result-pattern mappings; the switch state is not confused with the workload result; and setup versus inline timing costs are separately measured. Demonstrate concurrent setup/compute only in distinct regions or tiles until same-path timing has been verified.

### Gate 5 — Demonstrate end-of-workload-only readout

Run a multi-step workload with no electrical sensing of intermediate outputs. At completion, sense the stored magnetic pattern using the proposed final detector/array, decode it to the numerical result, and compare against the reference. Characterize whether readout is destructive, requires a probe wave, or affects stored state.

**Pass:** the final decoded output is correct within the required tolerance, the magnetic result remains retained through readout if the workload needs it, and total write-plus-final-read energy is measured.

### Gate 6 — Develop dynamic rails from the written state

Test whether retained result/configuration states can alter later propagation or enable selected paths for the next operation. Start with one state-dependent rail or selector, then a small array. Map magnetic state to route response and measure switching thresholds, timing, selectivity, false activation, state reset, and energy. If dynamic behavior requires an electrical sense/decode/drive loop, record that as an intermediate conversion rather than calling it direct magnonic handoff.

**Pass:** the previous written pattern changes the next operation in a reproducible, workload-useful way with no hidden read/convert path; or the actual intermediate electronics are explicitly accounted for.

### Gate 7 — Cascade several operations before the final read

Run at least two computation/write stages while keeping the result in magnetic states and delaying electrical output readout until the workload ends. Measure accumulated write errors, state retention, propagation loss, interference with prior stored values, reset cost, latency, and any required regeneration.

**Pass:** the final pattern still decodes correctly and the energy/latency advantage survives the added stage.

### Gate 8 — Compare on a complete inference workload

Integrate memory, controller, rail configuration, magnonic compute/write fabric, final sensor, and output decoder. Run a frozen benchmark against a competent baseline. Include input conversion, configuration, all wave operations, state writes, resets, final read, host/package power, and idle behavior.

**Pass:** lower full-system energy per correct inference at the same quality and latency. MLPerf methodology can guide workload and power reporting; use its applicable current rules for any formal submission.[^8](https://github.com/mlcommons/inference_policies/blob/master/power_measurement.adoc)

## 9. Energy, Timing, and Failure Accounting

The relevant energy is not only the energy in the magnetic wave. Track:

\[
E_{total}=E_{input}+E_{configuration}+E_{switch}+E_{magnon}+E_{state\;write}+E_{state\;hold}+E_{reset/erase}+E_{final\;readout}+E_{decode}+E_{memory/control}+E_{package/host}.
\]

If configuration or written result state is reused across \(R\) inferences, report both setup/write energy and amortized energy per inference. If a result map is erased and rewritten every workload, measure that cost every time. Report active and idle power; do not infer zero idle power from absence of a global clock. Include any RF source or pump that launches, maintains, amplifies, triggers, or reads magnetic activity.

Latency is likewise decomposed into input encoding, launch, propagation, state-writing threshold/settling, any state-dependent route response, optional regeneration, final read, and output decoding. For a pipeline, show whether these stages overlap or serialize. The product-level claim uses measured energy and latency at the chosen system boundary; magnetic propagation energy alone is an internal diagnostic.

Primary failure modes to track include: insufficient magnon-induced switching probability; accidental writes or loss of selectivity; state relaxation or read disturb; insufficient pattern capacity; nonuniform cell thresholds; interference between writes; direct electrical feedthrough masquerading as a wave-written state; phase/amplitude drift; cross-talk between rails; cumulative attenuation; thermal sensitivity; costly reset/erase; excessive reconfiguration energy; and a need for active amplification that erases the energy advantage.

## 10. Agent Guidance

An AI agent working on Idaten should reason using the following canonical concepts:

- **Code topology:** the fabricated placement of transistors/switches and magnetic rails defines the physically available program patterns.
- **Execution configuration:** transistor/switch states select or bias one of the possible patterns for a given run. Distinguish configuration/program input \(U_{cfg}\) from workload/data input \(X\); they may share one external stream but need a defined encoding and timing.
- **Input-to-switch path:** specify what magnetic element the input changes, the write threshold/state, how the state alters a rail, and whether configuration is written before compute or updated inline/between packets.
- **Live inference pattern:** magnons carry a structured spatial-temporal field through the chosen configuration.
- **Pattern transformation and write:** physical geometry and switch configuration shape the waves; magnonic activity is intended to write a persistent magnetic result map. The measured post-workload state pattern—not an assumed ideal CAD map—is the effective stored output.
- **Persistent result memory:** distinguish preloaded execution configuration \(C\), transient live wavefield \(\Psi\), and workload-written magnetic result state \(M\). The concept reads \(M\) only at the end of the individual workload.
- **Dynamic rails:** future configurations may let stored magnetic states alter later routes. This requires measured state-dependent coupling; never imply a conventional transistor automatically decodes a magnonic pattern.
- **Boundary readout:** electrical conversion is intended at the end-of-workload sensor/read sequence. Any intermediate detector/ADC or electrical control loop must be disclosed and counted.
- **Dynamic rail future:** progress from one magnon-written bit to a spatial result array, fixed patterned topology, switch-selected codebook, then state-dependent rail updates and multi-stage execution. Treat direct magnetic feedback from stored result states into later routes as a future capability that requires its own experiment.
- **Evidence labels:** distinguish simulated, physically measured, calibrated, projected, and independently reproduced results.

Do not state “zero resistance,” “absolute zero idle power,” “free computation,” “instant switching,” or “world’s most efficient” as established facts. Treat them as hypotheses only if tied to measurable definitions and pass/fail tests. Whenever proposing a device element, specify: (1) what physical quantity it changes, (2) what launches or controls it, (3) how the state is retained/reset, (4) how the next stage detects its effect, (5) its energy and delay, and (6) the experiment that could disprove the proposed behavior.

## 11. Conclusion

The intended Idaten mechanism is a hierarchy of patterns: a fixed fabricated placement creates a repertoire of rails and writable sites; switch states select a code-like execution configuration; magnons perform the workload and write a persistent, machine-readable magnetic result pattern; the result remains in the magnetic medium while the individual workload completes; and an electrical read sequence decodes it only at the workload boundary. Later “railway” generations may let retained states condition or select subsequent paths, enabling richer pattern-coded execution without repeated wave-to-electrical-to-wave conversion.

The first decisive experiment is no longer merely a patterned waveguide with an output antenna. It is a magnon bus coupled to an array of bistable magnetic storage elements, where a known input pulse/workload writes a spatial result map that remains after the wave passes and can be read at the end. The minimum proof should establish (a) magnon-caused writing separate from direct RF or heating, (b) repeatable input-to-persistent-pattern mapping, (c) a usable write/read/reset protocol and error rate, and (d) a complete energy/latency ledger. The next milestone is to make switch placement and runtime states select different mapping patterns; only then should the project test state-dependent dynamic rails and multi-stage workloads.

A 2023 YIG experiment already demonstrates the important base phenomenon—magnons can write nonvolatile magnetic bits—so Idaten’s core research contribution is to extend this into a programmable, computation-shaped result pattern and a rail topology that can exploit it.[^9](https://pmc.ncbi.nlm.nih.gov/articles/PMC10060572) The key unanswered question is: **Can the same magnonic execution both perform useful inference work and write a sufficiently rich, reliable retained state pattern, with one final readout, at lower full-system energy and acceptable latency than electronic alternatives?**

## References

1. J. Bensmann et al., “Dispersion-tunable low-loss implanted spin-wave waveguides for large magnonic networks,” *Nature Materials* (2025). https://pmc.ncbi.nlm.nih.gov/articles/PMC12657222/
2. Á. Papp, W. Porod, and G. Csaba, “Nanoscale neural network using non-linear spin-wave interference,” *Nature Communications* 12, 6422 (2021). https://pubmed.ncbi.nlm.nih.gov/34741047/
3. “A Magnetometer Based on a Spin Wave Interferometer,” *Scientific Reports* (2017). https://www.nature.com/articles/s41598-017-11881-y
4. M. Balynsky et al., “Reconfigurable submicrometer spin-wave majority gate with electrical transducers,” *Science Advances* (2020). https://www.science.org/doi/10.1126/sciadv.abb4042
5. “All-magnonic repeater based on bistability,” *Nature Communications* (2024). https://pmc.ncbi.nlm.nih.gov/articles/PMC11365973/
6. S. S. Gaur and E. E. Marinero, “Emergent Magnonic Materials: Challenges and Opportunities,” *Materials* 16(18), 6299 (2023). https://pmc.ncbi.nlm.nih.gov/articles/PMC10533023/
7. M. Hamdi et al., “Spin wave dispersion of ultra-low damping hematite (α−Fe₂O₃) at GHz frequencies,” *Physical Review Materials* 7, 054407 (2023). https://doi.org/10.1103/PhysRevMaterials.7.054407
8. MLCommons, “MLPerf Inference Power Measurement Rules.” https://github.com/mlcommons/inference_policies/blob/master/power_measurement.adoc
9. K. Baumgaertl and D. Grundler, “Reversal of nanomagnets by propagating magnons in ferrimagnetic yttrium iron garnet enabling nonvolatile magnon memory,” *Nature Communications* 14, 1490 (2023). https://pmc.ncbi.nlm.nih.gov/articles/PMC10060572/
