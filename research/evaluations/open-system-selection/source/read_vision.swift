import Foundation
import Vision
import ImageIO

let source = URL(fileURLWithPath: CommandLine.arguments[1])
let destination = URL(fileURLWithPath: CommandLine.arguments[2])
try FileManager.default.createDirectory(at: destination, withIntermediateDirectories: true)
let files = try FileManager.default.contentsOfDirectory(at: source, includingPropertiesForKeys: nil).filter { ["jpg", "png", "jpeg"].contains($0.pathExtension.lowercased()) }.sorted { $0.lastPathComponent < $1.lastPathComponent }
for (index, file) in files.enumerated() {
    let output = destination.appendingPathComponent(file.deletingPathExtension().lastPathComponent + ".json")
    if FileManager.default.fileExists(atPath: output.path) { continue }
    var trials: [[String: Any]] = []
    for (orientation, rotation) in [(CGImagePropertyOrientation.up, 0)] {
        let request = VNRecognizeTextRequest()
        request.recognitionLevel = .accurate
        request.usesCPUOnly = true
        request.recognitionLanguages = ["ru-RU", "en-US"]
        request.usesLanguageCorrection = false
        let handler = VNImageRequestHandler(url: file, orientation: orientation)
        do {
            try handler.perform([request])
            let rows: [[String: Any]] = (request.results ?? []).compactMap { observation in
                guard let candidate = observation.topCandidates(1).first else { return nil }
                let box = observation.boundingBox
                return ["text": candidate.string, "confidence": candidate.confidence, "box": [box.minX, box.minY, box.width, box.height]]
            }
            let score = rows.reduce(0.0) { total, row in
                let text = row["text"] as! String
                let letters = text.unicodeScalars.filter { CharacterSet.letters.contains($0) }.count
                let cyrillic = text.unicodeScalars.filter { $0.value >= 0x0400 && $0.value <= 0x04ff }.count
                return total + Double(row["confidence"] as! Float) * Double(letters + cyrillic)
            }
            trials.append(["rotation_ccw": rotation, "score": score, "lines": rows])
        } catch {
            trials.append(["rotation_ccw": rotation, "score": -1.0, "error": error.localizedDescription])
        }
    }
    let record: [String: Any] = ["image_id": String(format: "I%02d", index + 1), "source": file.lastPathComponent, "engine": "Apple Vision VNRecognizeTextRequest accurate; language correction disabled", "trials": trials, "selected": trials.max { ($0["score"] as! Double) < ($1["score"] as! Double) } ?? [:]]
    try JSONSerialization.data(withJSONObject: record, options: [.prettyPrinted, .sortedKeys]).write(to: output)
    print("READ \(index + 1)/\(files.count) \(file.lastPathComponent)")
    fflush(stdout)
}
