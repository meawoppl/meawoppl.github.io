---
title: "Putting an FPGA Inside a Microcontroller Workflow"
date: 2026-03-21 12:00:00 +0000
---

<!-- OUTLINE - flesh out each section -->

Sometimes you need a device that can talk to the internet, show up as a USB peripheral, and also close a control loop at 1 MHz. No single chip does all three well. A microcontroller gives you WiFi and USB but can't hit deterministic sub-microsecond timing. An FPGA gives you the timing but has no networking stack. The answer is both, on one board, with one build system.

The [IcedEspresso](https://github.com/Blinkinlabs/iced_espresso) board pairs an ESP32-S2 with a Lattice ICE40UP5K FPGA. It was originally designed by [BlinkinLabs](https://blinkinlabs.com/) for driving massive LED installations — an FPGA can instantiate many parallel WS2812 output drivers simultaneously, so instead of bit-banging one or two data lines from a microcontroller, you get dozens of channels running in lockstep while the ESP32 handles WiFi and coordination. I've spent the last few years building tooling and projects on this platform — repurposing that same FPGA-does-the-real-time, ESP32-does-the-networking split for control applications, the most demanding being a tesla coil controller that needs all three capabilities at once.

## The Problem: Two Worlds, One Device

<!--
- Microcontrollers are great at connectivity: WiFi, USB, TCP/IP stacks, OTA updates
- FPGAs are great at deterministic real-time: cycle-accurate timing, parallel I/O, hard-real-time control loops
- For high-power control at MHz rates, you need both — networking for orchestration, FPGA for the actual switching
- Traditional approach: two separate dev environments, two build systems, two flash steps
- FPGA toolchain (Yosys, nextpnr, icestorm) and ESP-IDF are each complex on their own
- Getting them to cooperate is a mess of Makefiles and Docker volumes
-->

## Affogato: One CLI To Rule Them All

<!--
- Wraps entire toolchain in a single Docker container
- `affogato new`, `affogato build`, `affogato flash`, `affogato run`
- Bitstream gets embedded into ESP32 firmware binary at compile time
- Soft-loaded over SPI at boot — no external flash programmer needed
- ~310ms from power-on to FPGA running
-->

## The Boot Dance

<!--
- ESP32 boots FreeRTOS, initializes SPI, holds FPGA in reset via CRESET_B
- Implements Lattice TN1248 SPI slave configuration sequence:
  1. Assert CRESET_B low (hold FPGA in reset)
  2. Assert SPI_CS low
  3. Wait 200ns (reset setup time)
  4. Release CRESET_B high (exit reset)
  5. Wait 1200us (ICE40 internal initialization)
  6. 8 dummy clocks with CS high
  7. CS low, stream bitstream MSB-first at 1-25 MHz
  8. Wait for CDONE high, send 100+ trailing clocks
  9. 49+ additional clocks to activate user I/O
  10. Release CS — FPGA is running
- Bitstream is embedded in ESP32 flash at compile time via CMake target_add_binary_data()
- No RAM copy needed — read straight from flash during config
- Total boot budget: ~310ms power-on to FPGA running (~300ms ESP32 boot, ~7ms bitstream transfer at 20 MHz)
-->

## QSPI: The Inter-Chip Bus

<!--
- After FPGA configuration, the same SPI pins transition from config mode to user I/O
- The bus is reconfigured as QSPI for runtime communication (pins: SCLK=12, MOSI=11, MISO=13, CS=10, WP=14, HD=9)
- This gives 4-bit-wide data path between ESP32 and FPGA at up to 40 MHz
- SPI mode switches from Mode 3 (config, per TN1248) to application-specific mode
- ESP-IDF SPI master driver with DMA handles the host side
- FPGA side uses custom SPI slave modules (bulk read for streaming, register mode for command/address/data)
- Thread-safe access via mutex semaphore — multiple FreeRTOS tasks can talk to the FPGA
- Effectively turns the FPGA into a high-speed, programmable peripheral on the ESP32's bus
-->

## Reusable Pieces

<!--
- ESP-IDF ice40 component: loader + SPI mutex
- Verilog module library: SPI slave (bulk + register), sync_ff, edge detect, RGB LED driver
- These modules have been battle-tested across three projects now
-->

## Controlling Tesla Coils at 1 MHz

<!--
- The coup-de-foudre art collective builds large musical tesla coils for live performance
- The coil's interrupter needs to switch at ~1 MHz — timing jitter directly translates to arc instability
- A microcontroller alone can't do this: ISR latency, FreeRTOS scheduling, WiFi interrupts all create jitter
- The FPGA handles the hard-real-time loop:
  - ADC capture (TI ADS7884) at full speed — the FPGA clocks the ADC and captures samples every cycle
  - Output timing for the interrupter — deterministic pulse generation with sub-microsecond precision
  - No jitter from software interrupts, no missed deadlines from garbage collection or WiFi callbacks
- The ESP32 handles everything else:
  - WiFi connectivity for remote orchestration
  - Protobuf communication with a companion orchestration server (teslaserver)
  - Parameter updates, safety monitoring, telemetry
  - USB for local debug and configuration
- The split: FPGA owns the control loop, ESP32 owns the network stack
- ESP32 sends updated parameters to the FPGA over QSPI — the FPGA applies them on the next cycle
- If the ESP32 crashes, WiFi drops, or firmware updates — the FPGA keeps the control loop safe
- This architecture replaced earlier Raspberry Pi and Teensy-based controllers that couldn't hit the timing
- The same platform has been adapted for other high-power control applications
-->

## Other Projects on the Platform

<!--
- GPS Time Calibrator: Stratum 1 NTP server, FPGA counts 48 MHz clock cycles between GPS PPS pulses
  - Sub-microsecond NTP precision, rolling frequency calibration
  - Same pattern: FPGA owns the precision timing, ESP32 owns the networking
- The architecture generalizes: anything where you need connectivity + deterministic real-time
-->

## What I'd Do Differently

<!--
- Cocotb instead of raw iverilog testbenches
- Formal verification from the start (SymbiYosys)
- Consider ESP32-S3 for the extra SPI bandwidth
- Better incremental build support
-->

## Next: A Dedicated Dev Board

<!--
- The IcedEspresso is great but it was designed for a specific product (LED drivers) — many FPGA and ESP32 pins are not broken out
- For a general-purpose dev platform, you want access to everything
- Planning a custom board that exposes basically all available GPIO from both chips:
  - All free ICE40UP5K user I/O pins broken out to headers
  - All available ESP32 GPIO broken out alongside them
  - Integrated WiFi antenna on-board (not a module, not an external antenna — just works)
  - USB-C for power, programming, and device mode
- The goal: a single board where you can prototype any ESP32+FPGA application without immediately needing a custom PCB
- Current workflow with the IcedEspresso means you hit pin limitations fast and end up designing a carrier board anyway
- With full I/O breakout, the dev board itself becomes viable for small-run production, not just prototyping
- QSPI bus between chips stays internal, all remaining pins go to headers
- Keeps the same affogato toolchain — just a wider canvas to work with
-->

## Where the Software Is Going

<!--
- Watch mode with debounced rebuilds
- Resource utilization reporting after synthesis
- More IP cores (UART, I2C, async FIFO)
- Maybe ECP5/Gowin support someday
-->
