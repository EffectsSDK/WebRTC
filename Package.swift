// swift-tools-version:5.3
import PackageDescription

let package = Package(
    name: "WebRTC",
    platforms: [.iOS(.v10), .macOS(.v10_11)],
    products: [
        .library(
            name: "WebRTC",
            targets: ["WebRTC"]),
    ],
    dependencies: [ ],
    targets: [
        .binaryTarget(
            name: "WebRTC",
            url: "https://github.com/EffectsSDK/WebRTC/releases/download/136.0.0/WebRTC-M136.xcframework.zip",
            checksum: "45b088b4d40e58101d2fe4f305ee93ff1149439c947e4052e1d6a92cf5d1021f"
        ),
    ]
)
