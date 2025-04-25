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
            url: "https://github.com/EffectsSDK/WebRTC/releases/download/135.0.0/WebRTC-M135.xcframework.zip",
            checksum: "5a4fa89a3860c2e05cc98c62f1cc5901778ce856599014763dd05dfd9aa2b80a"
        ),
    ]
)
