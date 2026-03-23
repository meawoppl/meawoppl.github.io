---
title: "Putting an FPGA Inside a Microcontroller Workflow"
date: 2026-03-21 12:00:00 +0000
---

Sometimes you need a device that talks to the internet, shows up as a USB peripheral, and also closes a control loop at 1 MHz. No single chip does all three. A microcontroller gets you WiFi and USB but will never hit deterministic sub-microsecond timing. An FPGA nails the timing but has no networking stack. You need both, on one board, with one build system that doesn't make you want to set your desk on fire.

The [IcedEspresso](https://github.com/Blinkinlabs/iced_espresso) board pairs an ESP32-S2 with a Lattice ICE40UP5K FPGA. [BlinkinLabs](https://blinkinlabs.com/) originally designed it for driving massive LED installations — the FPGA instantiates dozens of parallel WS2812 output drivers while the ESP32 handles WiFi and coordination. Instead of bit-banging one or two data lines from a microcontroller like some kind of animal, you get dozens of channels running in lockstep. I've spent the last few years repurposing that same split (FPGA does the real-time, ESP32 does the networking) for control applications. The most demanding? A tesla coil controller that needs all three capabilities simultaneously.

## Two Worlds, One Device

Microcontrollers are great at connectivity — WiFi, USB, TCP/IP stacks, OTA updates. FPGAs are great at deterministic real-time — cycle-accurate timing, parallel I/O, hard-real-time control loops. High-power control at MHz rates needs both: networking for orchestration, FPGA for the actual switching.

The traditional approach? Two separate dev environments, two build systems, two flash steps. The FPGA toolchain (Yosys, nextpnr, icestorm) and ESP-IDF are each a weekend of pain on their own. Getting them to cooperate on one project is a mess of Makefiles and Docker volumes that nobody wants to maintain and everybody inherits.

## Affogato

[Affogato](https://github.com/meawoppl/affogato) wraps the entire toolchain in a single Docker container. `affogato new`, `affogato build`, `affogato flash`, `affogato run`. That's it. The FPGA bitstream gets embedded into the ESP32 firmware binary at compile time and soft-loaded over SPI at boot. No external flash programmer. ~310ms from power-on to FPGA running.

The Docker container gets pulled automatically on first use. You don't install Yosys. You don't install nextpnr. You don't fight with icestorm. You type four commands and your FPGA is running.

## The Boot Dance

The ESP32 boots FreeRTOS, initializes SPI, and holds the FPGA in reset via CRESET_B. Then it implements the Lattice TN1248 SPI slave configuration sequence, which is exactly as fiddly as it sounds:

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

The bitstream lives in ESP32 flash, embedded at compile time via CMake `target_add_binary_data()`. No RAM copy needed — reads straight from flash during configuration. Total boot budget: ~300ms for the ESP32, ~7ms for the 104KB bitstream transfer at 20 MHz. If you blink, you miss it.

## QSPI: The Inter-Chip Bus

Here's the fun part. After FPGA configuration, the same SPI pins transition from config mode to user I/O. The bus gets reconfigured as QSPI for runtime communication — a 4-bit-wide data path between ESP32 and FPGA at up to 40 MHz.

SPI mode switches from Mode 3 (configuration, per TN1248) to whatever the application needs. ESP-IDF SPI master driver with DMA handles the host side. The FPGA side uses custom SPI slave modules — bulk read for streaming data, register mode for command/address/data exchanges. Thread-safe access via a mutex semaphore so multiple FreeRTOS tasks can talk to the FPGA concurrently.

Net effect: the FPGA becomes a high-speed, programmable peripheral on the ESP32's bus. You talk to it like any other SPI device, except this one does whatever you want in Verilog.

## Reusable Pieces

A library of components has emerged from building several projects on this platform:

- **ESP-IDF `ice40` component** — FPGA loader and SPI mutex management
- **`spi_slave_bulk.v`** — Streams N bytes on chip select for bulk data reads
- **`spi_slave_reg.v`** — Command/address/data register protocol
- **`sync_ff.v`** — Two flip-flop clock domain crossing
- **`edge_detect.v`** — Rising/falling/both edge detection
- **`rgb_led_driver.v`** — ICE40 `SB_RGBA_DRV` wrapper

Battle-tested across three projects now. They work. I trust them more than most people I've worked with.

## Controlling Tesla Coils at 1 MHz

The [coup-de-foudre](https://www.coupdefoud.re/) art collective builds large musical tesla coils for live performance. The coil's interrupter switches at ~1 MHz. Timing jitter directly translates to arc instability, and arc instability at these power levels translates to things-you-don't-want-happening.

A microcontroller alone can't do this. ISR latency, FreeRTOS scheduling, WiFi interrupts — they all inject jitter. Your real-time control loop is at the mercy of whatever the RTOS feels like doing with your thread priority this millisecond.

So the FPGA handles the hard-real-time loop. ADC capture (TI ADS7884) at full speed — the FPGA clocks the ADC and captures samples every cycle. Output timing for the interrupter with deterministic pulse generation at sub-microsecond precision. No jitter from software interrupts. No missed deadlines because someone's WiFi callback decided to run.

The ESP32 handles everything else: WiFi for remote orchestration, protobuf communication with a companion orchestration server, parameter updates, safety monitoring, telemetry, USB for local debug. The split is clean. FPGA owns the control loop. ESP32 owns the network stack.

Updated parameters flow from the ESP32 to the FPGA over QSPI. The FPGA applies them on the next cycle. If the ESP32 crashes, WiFi drops, or firmware is updating — the FPGA keeps the control loop safe. It doesn't care. It's hardware. It just keeps running.

This architecture replaced earlier Raspberry Pi and Teensy-based controllers that couldn't hit the timing requirements. Turns out "close enough" is not a thing when you're switching kilovolts at megahertz rates.

## ████████████████

The platform has also been adapted for ██████████ ███████ ████████ applications involving ████████ at ██████ ██████████ ██████. The ████████ ███████ required control rates ███████████ ████ ██ what the tesla coil work demanded, with ██████████ ████████████ constraints that ████████████ ██████████ the existing architecture to handle ██████████ ████ ███████████ ██████.

Unfortunately, the details ██████ ██████████ ██ ██████████ for contractual reasons. What I can say is that the same ESP32+FPGA split scaled to the requirements without fundamental changes. The architecture held. That felt good.

## Other Projects

The GPS Time Calibrator uses the same pattern. FPGA counts 48 MHz clock cycles between GPS pulse-per-second signals, rolling average provides stable frequency calibration. ESP32 parses GPS serial data, manages WiFi, runs a Stratum 1 NTP server with sub-microsecond precision. Same split: FPGA owns the timing, ESP32 owns the networking.

The architecture generalizes. Anything where you need connectivity and deterministic real-time in one package — this is the pattern.

## What I'd Do Differently

- Cocotb instead of raw iverilog testbenches. Python-based testbenches are just easier to maintain, and I say this as someone who has written a lot of Verilog testbenches.
- Formal verification from the start with SymbiYosys. Would have caught at least two bugs that took me days to find with simulation.
- ESP32-S3 for the extra SPI bandwidth. The S2 works, but you feel the ceiling.
- Better incremental build support. Full rebuilds get old fast.

## Next: A Dedicated Dev Board

The IcedEspresso is great, but it was designed for a specific product — lots of FPGA and ESP32 pins are not broken out. You hit pin limitations fast and end up designing a carrier board anyway, which sort of defeats the purpose of having a dev board.

The plan is a custom board that exposes basically all available GPIO from both chips. All free ICE40UP5K user I/O pins and all available ESP32 GPIO broken out to headers. Integrated WiFi antenna on-board. USB-C for power, programming, and device mode. QSPI bus between chips stays internal — everything else goes to headers.

The goal: a single board where you can prototype any ESP32+FPGA application without immediately needing a custom PCB. And with full I/O breakout, the dev board itself becomes viable for small-run production. Same affogato toolchain, just a wider canvas.

## Where the Software Is Going

- Watch mode with debounced rebuilds
- Resource utilization reporting after synthesis
- More IP cores — UART, I2C, async FIFO
- Maybe ECP5 or Gowin support someday (don't hold your breath)
