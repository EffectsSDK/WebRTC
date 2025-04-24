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
            checksum: "94d4af882caaa04b3b44db9ba36b45854ca5b5b773ec60016f7ea16333b53757"
        ),
    ]
)
