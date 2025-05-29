# WebRTC Binaries for iOS and macOS with API for audio custom processing

This patched WebRTC version simplify integration with [Audio Effects SDK](https://github.com/EffectsSDK/audio-effects-sdk-swift-package).

This repository contains a distribution of WebRTC framework binaries for iOS and macOS with added **RTCAudioCustomProcessing** delegate. 
This repository is fork of [WebRTC community-driven build](https://github.com/stasel/WebRTC).

* All binaries in this repository are compiled from the official WebRTC [source code](https://webrtc.googlesource.com/src/).
* scripts/build.sh downloads official WebRTC and applies patch that adds Objective-C/Swift API for custom audio processing.
* Dynamic framework (xcframework format) which contains multiple binaries for macOS and iOS.

## 📢 Requirements
* iOS 12+
* macOS 10.11+
* macOS Catalyst 11.0+

## 📀 Binaries included
| **Platform / arch** | arm64  | x86_x64 |
|---------------------|--------|---------|
| **iOS (device)**    |   ✅   |   N/A   |
| **iOS (simulator)** |   ✅   |    ✅   |
| **macOS**           |   ✅   |    ✅   |
| **macOS Catalyst**  |   ✅   |    ✅   | 

*Looking for 32 bit binaries? Please use [Version M94](https://github.com/stasel/WebRTC/releases/tag/94.0.0) or lower*

## 🚚 Installation

### Swift package manager
Xcode has a built-in support for Swift package manager. You can easily add the package by selecting File > Swift Packages > Add Package Dependency. Read more in [Apple documentation](https://developer.apple.com/documentation/xcode/adding_package_dependencies_to_your_app).

Or, you can add the following dependency to your `Package.swift` file:
```swift
dependencies: [
    .package(url: "https://github.com/EffectsSDK/WebRTC.git", .upToNextMajor("136.0.0"))
]
```

Use the `latest` branch to get the most up to date binary:

```swift
dependencies: [
    .package(url: "https://github.com/EffectsSDK/WebRTC.git", branch: "latest")
]
```

### Manual
1. Download the framework from the [releases](https://github.com/EffectsSDK/WebRTC/releases) section.
2. Unzip the file.
3. Add the xcframework to your target(s) embedded frameworks.


## 👷 Usage
To import WebRTC to your code add the following import statement
```swift
import WebRTC
```

## 📃 License
* BSD 3-Clause License
* WebRTC License: https://webrtc.org/support/license
