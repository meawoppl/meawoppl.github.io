---
date: 2022-10-01
name: Embedded FPGA
thumb: /images/embedded-fpga/logo.svg
---

Two projects built around the IcedEspresso board — an ESP32-S2 paired with a Lattice ICE40UP5K FPGA.

## Affogato

[Affogato](https://github.com/meawoppl/affogato) is a CLI tool that wraps the entire ESP32 + ICE40 development workflow into a single command. It manages a Docker container with the full FPGA toolchain (Yosys, nextpnr, icestorm) and ESP-IDF, so there's no host installation to fight with.

`affogato build` synthesizes the Verilog, packs the bitstream, embeds it into the ESP32 firmware binary, and compiles everything. The FPGA bitstream gets soft-loaded over SPI at boot. It also supports watch mode with debounced rebuilds, testbench discovery and simulation via iverilog, and Verilator linting.

The tool ships with a library of reusable Verilog modules — SPI slave (bulk and register modes), clock domain crossing, edge detection, and an RGB LED driver — plus an ESP-IDF component that handles FPGA loading and SPI communication.

## GPS Time Calibrator

[GPS Time Calibrator](https://github.com/meawoppl/gps-time-calibrator) is a precision timing system that synchronizes camera timestamps using GPS pulse-per-second signals. The FPGA measures clock cycles between PPS pulses at 48 MHz resolution, and a rolling average provides stable frequency calibration. The ESP32 parses GPS serial data, manages WiFi, and runs a Stratum 1 NTP server with sub-microsecond precision.

The FPGA side is built from modular Verilog — an interval counter, health monitor (tracks consecutive good pulses before reporting lock), and frequency averager, each with independent testbenches. The ESP32 reads FPGA state over a clean SPI register interface with value latching to avoid torn reads across clock domains.

## Widlar

[Widlar](https://github.com/coup-de-foudre/widlar) is a tesla coil controller built for the [coup-de-foudre](https://www.coupdefoud.re/) art collective. The FPGA handles real-time ADC capture (TI ADS7884) and output timing for the interrupter, while the ESP32 manages orchestration and networking. The FPGA bitstream is bundled into the ESP32 firmware and soft-loaded over SPI at boot.

The project is part of a larger system — a companion [orchestration server](https://github.com/coup-de-foudre/teslaserver) coordinates control, and communication uses protobuf over the wire. It represents the culmination of several earlier coup-de-foudre projects that progressed from Raspberry Pi and Teensy-based controllers to a dedicated FPGA solution. The platform has also been adapted for very high power control applications that cannot be described here for contractual reasons.
