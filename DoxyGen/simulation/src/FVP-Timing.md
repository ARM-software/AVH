# FVP Simulation Model Timing

The timing in AVH FVP models is based on a instruction count, therefore it is not timing accurate. However the results can still be used for performance estimation and A/B comparison of algorithms.

In real hardware systems there are multiple factors that influence timing.

Factors that slow-down execution when measured on real hardware:

- Wait states caused by the BUS or memory systems.
- CPU instructions take more then one cycle are simulated with the wrong timing.
- Stalls that are caused by pipeline effects.

Factors that speed-up execution when measured on real hardware:

- Instructions that are folded and take therefore effectively no cycles.

Fortunately, the Arm Cortex-M processors contain [Event Counters](https://developer.arm.com/documentation/101407/0540/Debugging/Debug-Windows-and-Dialogs/Event-Counters) that indicate this scenarios.

- The value of `CPICNT` and `LSUCNT` are incremented on additional wait states. These value should be added to the cycles measured in simulation.
- The value of `FOLDCNT` is incremented when instructions are folded. This value should be subtracted from the cycles measured in simulation.

Using the uVision Debugger (or any other debugger with access to these counters) lets you evaluate the values of that counters.

Example measured on Corstone-300 targets.

Value                             | Cycles
:---------------------------------|:-------------------------
Cycles in Hardware                | 58,623,072
CPI value                         | 23,811,197
LSU value                         | 11,274,432
FOLD value                        | 954,246
Cycles in Simulation              | 30,357,120
Cycles im Simulation (corrected)  | 64,488,503

An alternative method is to evaluate a correction factor that could be applied on similar workload runs in FVP.

`Factor = (Cycles in Hardware) / (Cycles in Simulation) =  1.913`
