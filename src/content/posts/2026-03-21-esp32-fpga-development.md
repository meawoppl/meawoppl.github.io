---
title: "Putting an FPGA Inside a Microcontroller Workflow"
date: 2026-03-21 12:00:00 +0000
---

Sometimes you need a device that can talk to the internet, show up as a USB peripheral, and also close a control loop at 1 MHz. No single chip does all three well. A microcontroller gives you WiFi and USB but can't hit deterministic sub-microsecond timing. An FPGA gives you the timing but has no networking stack. The answer is both, on one board, with one build system.

The [IcedEspresso](https://github.com/Blinkinlabs/iced_espresso) board pairs an ESP32-S2 with a Lattice ICE40UP5K FPGA. It was originally designed by [BlinkinLabs](https://blinkinlabs.com/) for driving massive LED installations — an FPGA can instantiate many parallel WS2812 output drivers simultaneously, so instead of bit-banging one or two data lines from a microcontroller, you get dozens of channels running in lockstep while the ESP32 handles WiFi and coordination. I've spent the last few years building tooling and projects on this platform — repurposing that same FPGA-does-the-real-time, ESP32-does-the-networking split for control applications, the most demanding being a tesla coil controller that needs all three capabilities at once.

## The Problem: Two Worlds, One Device

Microcontrollers are great at connectivity — WiFi, USB, TCP/IP stacks, OTA updates. FPGAs are great at deterministic real-time — cycle-accurate timing, parallel I/O, hard-real-time control loops. For high-power control at MHz rates, you need both: networking for orchestration, FPGA for the actual switching.

The traditional approach is two separate dev environments, two build systems, two flash steps. The FPGA toolchain (Yosys, nextpnr, icestorm) and ESP-IDF are each complex on their own. Getting them to cooperate on one project is a mess of Makefiles and Docker volumes.

## Affogato: One CLI To Rule Them All

[Affogato](https://github.com/meawoppl/affogato) wraps the entire toolchain in a single Docker container. `affogato new`, `affogato build`, `affogato flash`, `affogato run` — that's the whole workflow. The FPGA bitstream gets embedded into the ESP32 firmware binary at compile time and soft-loaded over SPI at boot. No external flash programmer needed. About 310ms from power-on to FPGA running.

## The Boot Dance

The ESP32 boots FreeRTOS, initializes SPI, and holds the FPGA in reset via CRESET_B. Then it implements the Lattice TN1248 SPI slave configuration sequence:

1. Assert CRESET_B low — hold FPGA in reset
2. Assert SPI_CS low
3. Wait 200ns — reset setup time
4. Release CRESET_B high — exit reset
5. Wait 1200&micro;s — ICE40 internal initialization
6. 8 dummy clocks with CS high
7. CS low, stream bitstream MSB-first at 1-25 MHz
8. Wait for CDONE high, send 100+ trailing clocks
9. 49+ additional clocks to activate user I/O
10. Release CS — FPGA is running

The bitstream is embedded in ESP32 flash at compile time via CMake `target_add_binary_data()`. No RAM copy needed — it reads straight from flash during configuration. Total boot budget: ~300ms for the ESP32, ~7ms for the bitstream transfer at 20 MHz.

## QSPI: The Inter-Chip Bus

After FPGA configuration, the same SPI pins transition from config mode to user I/O. The bus is reconfigured as QSPI for runtime communication — a 4-bit-wide data path between ESP32 and FPGA at up to 40 MHz.

The SPI mode switches from Mode 3 (configuration, per TN1248) to whatever the application needs. The ESP-IDF SPI master driver with DMA handles the host side. The FPGA side uses custom SPI slave modules — bulk read for streaming data, register mode for command/address/data exchanges. Thread-safe access via a mutex semaphore means multiple FreeRTOS tasks can talk to the FPGA concurrently.

This effectively turns the FPGA into a high-speed, programmable peripheral on the ESP32's bus.

## Reusable Pieces

A library of components has emerged from building several projects on this platform:

- **ESP-IDF `ice40` component** — FPGA loader and SPI mutex management
- **`spi_slave_bulk.v`** — Streams N bytes on chip select for bulk data reads
- **`spi_slave_reg.v`** — Command/address/data register protocol
- **`sync_ff.v`** — Two flip-flop clock domain crossing
- **`edge_detect.v`** — Rising/falling/both edge detection
- **`rgb_led_driver.v`** — ICE40 `SB_RGBA_DRV` wrapper

These modules have been battle-tested across three projects now.

## Controlling Tesla Coils at 1 MHz

The [coup-de-foudre](https://www.coupdefoud.re/) art collective builds large musical tesla coils for live performance. The coil's interrupter needs to switch at ~1 MHz — timing jitter directly translates to arc instability.

A microcontroller alone can't do this. ISR latency, FreeRTOS scheduling, and WiFi interrupts all create jitter. So the FPGA handles the hard-real-time loop: ADC capture (TI ADS7884) at full speed — the FPGA clocks the ADC and captures samples every cycle — and output timing for the interrupter with deterministic pulse generation at sub-microsecond precision. No jitter from software interrupts, no missed deadlines from WiFi callbacks.

The ESP32 handles everything else: WiFi connectivity for remote orchestration, protobuf communication with a companion orchestration server, parameter updates, safety monitoring, telemetry, and USB for local debug. The split is clean — FPGA owns the control loop, ESP32 owns the network stack.

Updated parameters flow from the ESP32 to the FPGA over QSPI, and the FPGA applies them on the next cycle. If the ESP32 crashes, WiFi drops, or firmware is updating — the FPGA keeps the control loop safe. This architecture replaced earlier Raspberry Pi and Teensy-based controllers that couldn't hit the timing requirements.

## ████████████████

The platform has also been adapted for ██████████ ███████ ████████ applications involving ████████ at ██████ ██████████ ██████. The ████████ ███████ required control rates ███████████ ████ ██ what the tesla coil work demanded, with ██████████ ████████████ constraints that ████████████ ██████████ the existing architecture to handle ██████████ ████ ███████████ ██████.

Unfortunately, the details of this work ██████ ██████████ ██ ██████████ for contractual reasons. What can be said is that the same ESP32+FPGA split — networking and orchestration on the microcontroller, hard-real-time control on the FPGA — scaled to the requirements without fundamental changes to the architecture.

## Other Projects on the Platform

The GPS Time Calibrator uses the same pattern for precision timing. The FPGA counts 48 MHz clock cycles between GPS pulse-per-second signals, and a rolling average provides stable frequency calibration. The ESP32 parses GPS serial data, manages WiFi, and runs a Stratum 1 NTP server with sub-microsecond precision. Same split: FPGA owns the timing, ESP32 owns the networking.

The architecture generalizes to anything where you need connectivity and deterministic real-time in one package.

## What I'd Do Differently

- Cocotb instead of raw iverilog testbenches — Python-based testbenches are easier to maintain
- Formal verification from the start with SymbiYosys
- Consider the ESP32-S3 for extra SPI bandwidth
- Better incremental build support to speed up iteration

## Next: A Dedicated Dev Board

The IcedEspresso is great, but it was designed for a specific product — many FPGA and ESP32 pins are not broken out. For a general-purpose dev platform, you want access to everything.

The plan is a custom board that exposes basically all available GPIO from both chips: all free ICE40UP5K user I/O pins and all available ESP32 GPIO broken out to headers, with an integrated WiFi antenna on-board and USB-C for power, programming, and device mode.

The goal is a single board where you can prototype any ESP32+FPGA application without immediately needing a custom PCB. The current workflow with the IcedEspresso means you hit pin limitations fast and end up designing a carrier board anyway. With full I/O breakout, the dev board itself becomes viable for small-run production, not just prototyping. The QSPI bus between chips stays internal — all remaining pins go to headers. Same affogato toolchain, just a wider canvas to work with.

## Where the Software Is Going

- Watch mode with debounced rebuilds
- Resource utilization reporting after synthesis
- More IP cores — UART, I2C, async FIFO
- Maybe ECP5 or Gowin support someday
