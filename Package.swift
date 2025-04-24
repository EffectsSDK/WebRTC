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
            url: "https://github.com/stasel/WebRTC/releases/download/135.0.0/WebRTC-M135.xcframework.zip",
            checksum: "179a8c35a7f622a3d98ca9fac98984ab8f334b19faa5f23a42f1826a4a1ea9eb"
        ),
    ]
)
